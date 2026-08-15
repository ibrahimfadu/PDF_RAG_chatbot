from integrations/loader import Loader
from chunking/chunk import Splitter
from embeddings/embedding import Embedding
import fasiss 
form fastapi import FastAPI 
import numpy as np

app=FastAPI()


def rag(file):
    load = Loader()
    chunk = Splitter(size,overlap)
    embedd = Embedding()
    
    data = load.load_file(file)
    
    data = chunk.text_splitter(data)
    
    embedd=embedd.encoding_text(chunk)
    
    def store(embedded : np.ndarray):
            index = faiss.IndexFlatL2(embedded.shape[1])
            index.add(np.array(embedded,dtype=np.float32))
            return index
    
store(embedd);

app.get("/")


