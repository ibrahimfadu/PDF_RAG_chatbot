from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import hashlib
import os

class RAG():
    def __init__(self, llm_model, embedding_model):
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.chunks = []  # Store chunks with metadata
        self.index = None
        self.chunk_texts = []  # For backward compatibility

    # ============ load_file - Fixed ============
    def load_file(self, files):
        """
        Load PDFs and extract text with page numbers and filenames
        
        Args:
            files: List of file objects OR a single file object
        
        Returns:
            List of dicts with text, page number, and source file
        """
        if not files:
            raise ValueError("No files provided")
        
        # Handle both single file and list of files
        if not isinstance(files, list):
            files = [files]
        
        all_pages = []
        
        for file in files:
            # Get filename correctly
            if hasattr(file, 'name'):
                file_name = os.path.basename(file.name)
            elif isinstance(file, str):
                file_name = os.path.basename(file)
            else:
                file_name = "unknown.pdf"
            
            # Read the PDF
            try:
                documents = PdfReader(file, strict=False)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue
            
            # Process each page
            for page_num, page in enumerate(documents.pages, start=1):
                text = page.extract_text() or ""
                
                if not text.strip():
                    continue
                
                # Create page ID
                raw_id = f"{file_name}_page_{page_num}"
                page_id = hashlib.md5(raw_id.encode()).hexdigest()[:12]
                
                all_pages.append({
                    'text': text,
                    'page_num': page_num,
                    'source': file_name,
                    'page_id': page_id,
                    'total_pages': len(documents.pages)
                })
        
        # ✅ Store for later use
        self.pages = all_pages
        return all_pages

    # ============ text_splitter - Fixed ============
    def text_splitter(self, pages_with_metadata, size=500, overlap=50):
        """
        Split text into chunks while preserving metadata
        
        Args:
            pages_with_metadata: List from load_file() OR string text
            size: Chunk size
            overlap: Chunk overlap
        
        Returns:
            List of chunks (with metadata if available)
        """
        if not pages_with_metadata:
            raise ValueError("No text to split...")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # ✅ Handle both cases: metadata dicts OR plain text string
        if isinstance(pages_with_metadata, str):
            # Old style: just text string
            chunks = splitter.split_text(pages_with_metadata)
            self.chunk_texts = chunks
            return chunks
        
        # New style: list of dicts with metadata
        all_chunks = []
        
        for page_data in pages_with_metadata:
            page_text = page_data['text']
            file_name = page_data['source']
            page_num = page_data['page_num']
            page_id = page_data['page_id']
            
            page_chunks = splitter.split_text(page_text)
            
            for chunk_idx, chunk_text in enumerate(page_chunks):
                chunk_raw = f"{file_name}_p{page_num}_c{chunk_idx}"
                chunk_id = hashlib.md5(chunk_raw.encode()).hexdigest()[:12]
                
                all_chunks.append({
                    'chunk_id': chunk_id,
                    'page_id': page_id,
                    'text': chunk_text,
                    'source': file_name,
                    'page': page_num,
                    'chunk_index': chunk_idx
                })
        
        self.chunks = all_chunks
        
        # ✅ For backward compatibility: store just the text
        self.chunk_texts = [c['text'] for c in all_chunks]
        
        return all_chunks

    # ============ encoding_text - Fixed ============
    def encoding_text(self, chunks):
        """
        Encode text chunks to embeddings
        """
        if not chunks:
            raise ValueError("No chunks found..")
        
        # Handle different input types
        if isinstance(chunks, list):
            if len(chunks) == 0:
                raise ValueError("Empty chunks list")
            
            # Check if chunks are dicts with 'text' or plain strings
            if isinstance(chunks[0], dict):
                texts = [c['text'] for c in chunks]
            else:
                texts = chunks
        else:
            texts = [chunks]
        
        clean_chunks = [t.encode("utf-8", errors="ignore").decode("utf-8") for t in texts]
        
        try:
            embedded = self.embedding_model.encode(clean_chunks)
            return embedded
        except Exception as e:
            raise RuntimeError(f"Error encoding: {e}")

    # ============ store ============
    def store(self, embedded):
        """
        Create FAISS index from embeddings
        """
        if embedded is None or len(embedded) == 0:
            raise ValueError("No embeddings to store")
        
        # Handle both 1D and 2D arrays
        if len(embedded.shape) == 1:
            embedded = embedded.reshape(1, -1)
        
        dimension = embedded.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embedded, dtype=np.float32))
        return self.index

    # ============ search_query - Fixed ============
    def search_query(self, index, question, chunks, top_k=5):
        """
        Search for relevant chunks and return context
        
        Args:
            index: FAISS index
            question: User question
            chunks: List of chunks (dicts or strings)
            top_k: Number of chunks to retrieve
        
        Returns:
            Context string with sources
        """
        if not question:
            raise ValueError("Invalid Question")
        
        if index is None:
            raise ValueError("Index not built. Call store() first.")
        
        if not chunks:
            raise ValueError("No chunks available. Load documents first.")
        
        # Encode question
        embedded_query = self.encoding_text([question])
        
        # Search
        distances, indices = index.search(
            np.array(embedded_query, dtype=np.float32), 
            k=min(top_k, len(chunks))
        )
        
        # Build context with sources
        context_parts = []
        
        for i, idx in enumerate(indices[0]):
            if idx < len(chunks):
                chunk = chunks[idx]
                
                # Handle both dict and string
                if isinstance(chunk, dict):
                    text = chunk['text']
                    source = chunk.get('source', 'unknown')
                    page = chunk.get('page', '?')
                    context_parts.append(f"[Source {i+1}] From: {source}, Page: {page}\n{text}")
                else:
                    context_parts.append(f"[Source {i+1}]\n{chunk}")
        
        context = "\n\n".join(context_parts)
        
        # ✅ Store for debugging
        self.last_context = context
        
        return context

    # ============ get_context (NEW) ============
    def get_context(self, results):
        """Create context string from search results"""
        if not results:
            return "No relevant information found."
        
        context_parts = []
        for i, chunk in enumerate(results, 1):
            if isinstance(chunk, dict):
                context_parts.append(
                    f"[Source {i}] From: {chunk.get('source', 'unknown')}, Page: {chunk.get('page', '?')}\n{chunk['text']}"
                )
            else:
                context_parts.append(f"[Source {i}]\n{chunk}")
        
        return "\n\n".join(context_parts)

    # ============ result ============
    def result(self, context, question):
        """
        Get LLM response with context
        """
        prompt = f"""
You are a helpful assistant. Answer the question based ONLY on the provided context.

CONTEXT:
{context}

QUESTION: {question}

INSTRUCTIONS:
1. Answer only using information from the context.
2. If the answer is not in the context, say "I don't have this information."
3. Be concise and clear.

ANSWER:
"""
        response = self.llm_model.invoke(prompt)
        return response

    # ============ One-shot ask ============
    def ask(self, question, files=None, top_k=5):
        """Complete RAG pipeline"""
        if files:
            pages = self.load_file(files)
            chunks = self.text_splitter(pages)
            embeddings = self.encoding_text(chunks)
            self.store(embeddings)
            self.chunks = chunks
        
        if self.index is None:
            raise ValueError("No index found. Load documents first.")
        
        context = self.search_query(self.index, question, self.chunks, top_k)
        answer = self.result(context, question)
        
        return {
            'answer': answer,
            'context': context
        }
