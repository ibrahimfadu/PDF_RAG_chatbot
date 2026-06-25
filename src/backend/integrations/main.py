from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI

class RAG():
    def __init__(self,llm_model,embedding_model):
        self.llm_model = llm_model
        self.embedding_model  = embedding_model

    #load file 
    def load_file(self,file) ->str:
        if not file:
            raise ValueError("InValued File..")
        file.seek(0)
        documents = PdfReader(file,strict=False)
        text = " "
        for page in documents.pages:
            text += page.extract_text() + "\n"
        return text       

    #text split
    def text_splitter(self,text : str,size: int|float , overlap: int|float) ->list[str]:
        if not text:
            raise ValueError("No Text...")
        model_chunk = RecursiveCharacterTextSplitter(chunk_size = size,chunk_overlap = overlap)
        chunk = model_chunk.split_text(text)
        return chunk

    #encoding 
    def encoding_text(self,chunks : list[str] | str)->list[float]:
        if not chunks:
            raise ValueError("No chunks found..")
        clean_chunks = [ c.encode("utf-8", errors="ignore").decode("utf-8") for c in chunks ]
        try:
            embedded = self.embedding_model.encode(clean_chunks)
            return embedded
        except Exception as e:
            raise RuntimeError(f"Error {e}")

    #database (vector database)
    def store(self,embedded : np.ndarray):
        index = faiss.IndexFlatL2(embedded.shape[1])
        index.add(np.array(embedded,dtype=np.float32))
        return index
    
    def search_query(self,index, question :list | str,chunks :list[str]) ->str:
        if not question:
            raise ValueError("Invalid Question")
        embedded_query = self.encoding_text(question)
        d,i = index.search(np.array(embedded_query),k=5)
        context = ""
        if len(i)==0:
            raise ValueError("search invalid")
        for idx in i[0]:
            context += chunks[idx] + "\n"
        return context

    def result(self,context: str,question: str):
        prompt = f""" 
            context: {context}, question:{question}
            answer only from context
        """
        response = self.llm_model.invoke(prompt)
        return response
          
