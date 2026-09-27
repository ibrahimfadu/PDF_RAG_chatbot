from cleanFile import fileData
from chunks import chunk

data = fileData("/home/ibrahimfadu/project/RAG/src/backend/test_docs/Hands-On_Machine_Learning_with_Scikit-Learn-Keras-and-TensorFlow-2nd-Edition-Aurelien-Geron.pdf")

#print(len(data))
print(chunk(data)[0])

