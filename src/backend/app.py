from integrations/loader import Loader
from fastapi import FastApi
from chunking/chunk import Splitter

load = Loader()
Splitter = Splitter()
app = FastApi()

file = "/home/ibrahimfadu/books/ABUIABA9GAAghIK0ugYowM2h3QY.pdf"

print(text)

@app.post("/upload")
def fileHandle(file):
  text = load.load_file(file)
  chunks = 

