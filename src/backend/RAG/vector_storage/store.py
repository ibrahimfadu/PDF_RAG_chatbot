import faiss
import numpy as np

def store(self,embedded : np.ndarray):
        index = faiss.IndexFlatL2(embedded.shape[1])
        index.add(np.array(embedded,dtype=np.float32))
        return index