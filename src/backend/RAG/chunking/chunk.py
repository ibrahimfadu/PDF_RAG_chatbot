from langchain.text_splitter import RecursiveCharacterTextSplitter

#RecursiveCharacterTextSplitter used seprating the text based on the (.,"",;etc)
class Splitter():
    def __init__(self,size: int|float, overlap: int|float):
        self.size = size
        self.overlap = overlap

    def text_splitter(self,text : str)-> list[str]:
        if not text:
            raise ValueError("No Text...")
        model_chunk = RecursiveCharacterTextSplitter(chunk_size = self.size,chunk_overlap = self.overlap)
        chunk = model_chunk.split_text(text)
        return chunk

