# main.py - Streamlit App
from main import RAG
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# ============ CONFIG ============
st.set_page_config(page_title="📄 AskYourPDF")
st.title("📄 AskYourPDF - Chat with any document")


def mode_toggle_minimal():
    """Minimal online/offline toggle"""
    
    # Initialize
    if 'online' not in st.session_state:
        st.session_state.online = False
    
    # Toggle button
    if st.session_state.online:
        if st.button("🟢 Switch to Offline"):
            st.session_state.online = False
            st.rerun()
    else:
        if st.button("⚪ Switch to Online"):
            st.session_state.online = True
            st.rerun()
    
    return st.session_state.online

# Usage in sidebar
online = mode_toggle_minimal()

if online:
    st.caption("🟢 Online Mode (Gemini)")
    online = True 
else:
    online = False 
    st.caption("⚪ Offline Mode (Ollama)")


API_KEY = os.getenv("GOOGLE_GEMINI")

# ============ LLM SETUP ============
llm_model = ChatOllama(model="gemma2:latest")

if online:
    llm_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=API_KEY
    )

# ============ EMBEDDING MODEL ============
@st.cache_resource
def load_embedding_model():
    try:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return model
    except Exception as e:
        st.error(f"Can't load the model: {e}")
        return None

model = load_embedding_model()

# ============ RAG INIT ============
rag = RAG(llm_model, model)

# ============ FILE UPLOAD ============
files = st.file_uploader(
    "Upload PDF files", 
    type="pdf", 
    accept_multiple_files=True, 
    help="Upload one or more PDF files"
)

# ============ EXAMPLE QUESTIONS ============
with st.expander("💡 Example questions"):
    st.markdown("""
    - "What is this document about?"
    - "Summarize the key points"
    - "List all the dates mentioned"
    - "What are the action items?"
    """)

# ============ PROCESS FILES ============
if files:
    with st.spinner("Loading and indexing documents..."):
        try:
            # ✅ FIXED: Pass files as a list
            pages = rag.load_file(files)
            
            # ✅ FIXED: Pass pages with metadata
            chunks = rag.text_splitter(pages, size=500, overlap=100)
            
            # Encode and store
            embeddings = rag.encoding_text(chunks)
            index = rag.store(embeddings)
            
            # Store in session state
            st.session_state['index'] = index
            st.session_state['chunks'] = chunks
            st.session_state['pages'] = pages
            st.session_state['is_loaded'] = True
            
            # Show stats
            total_pages = len(pages)
            total_chunks = len(chunks)
            sources = set([c['source'] for c in chunks])
            
            st.success(f"✅ Indexed {total_chunks} chunks from {len(sources)} PDFs ({total_pages} pages)")
            
        except Exception as e:
            st.error(f"Error processing documents: {e}")
            st.stop()

# ============ QUERY INTERFACE ============
if 'is_loaded' in st.session_state and st.session_state['is_loaded']:
    
    with st.form("question_form"):
        question = st.text_input("Ask a question about your documents...")
        submit = st.form_submit_button("🔍 Ask")
    
    if question and submit:
        with st.spinner("Generating answer..."):
            try:
                # Search
                context = rag.search_query(
                    st.session_state['index'],
                    question,
                    st.session_state['chunks'],
                    top_k=5
                )
                
                # Get response
                response = rag.result(context, question)
                
                # Display answer
                st.success("✅ Answer generated!")
                st.markdown("---")
                st.markdown("### 💬 Answer")
                st.write(response.content)
                
                # Show sources
                with st.expander("📚 Sources"):
                    # Extract sources from context
                    lines = context.split('\n')
                    source_lines = [l for l in lines if l.startswith('[Source')]
                    if source_lines:
                        for line in source_lines:
                            st.write(line)
                    else:
                        st.write("Sources not available")
                
                # Show context (debug)
                with st.expander("🔍 Context used"):
                    st.text(context[:1000] + "..." if len(context) > 1000 else context)
                    
            except Exception as e:
                st.error(f"Error generating answer: {e}")

else:
    st.info("👈 Please upload one or more PDF files to get started.")

# ============ FOOTER ============
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, FAISS, and LangChain")
