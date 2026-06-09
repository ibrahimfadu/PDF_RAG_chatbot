from main import RAG     
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer
import streamlit as st 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_GEMINI")

llm_model = ChatGoogleGenerativeAI(  model="gemini-2.5-flash",
    api_key = API_KEY 
)


model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2")

file = st.file_uploader("Select the url...")

rag = RAG(llm_model,model)

@st.cache_resource
def rag_load(file_data):
    text = rag.load_file(file_data)
    size = 500
    overlap = 100
    
    chunks = rag.text_splitter(text,size,overlap)
    
    encoding_text = rag.encoding_text(chunks)
    
    index = rag.store(encoding_text);
    return index,chunks

if file:
    with st.spinner("loading file...."):
        index,chunks = rag_load(file)

    st.success("Document indexed!")

    with st.form("question_form"):
        question = st.text_input("Enter your question..")
        submit = st.form_submit_button("Submit")

    if question and submit:
        with st.spinner("Generating the result..."):
            context = rag.search_query(index,question,chunks)
            response = rag.result(context,question)

        st.success("generating result...")
        st.write(response.content)

    
