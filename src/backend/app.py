from integrations/loader import Loader
from chunking/chunk import Splitter
from embeddings/embedding import Embedding


load = Loader()
chunk = Splitter(size,overlap)
embedd = Embedding()

data = load.load_file(file)

data = chunk.text_splitter(data)

embedd.encoding_text(chunk)




