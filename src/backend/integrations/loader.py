from pypdf import PdfReader

class Loader():
def load_file(self,file) ->str:
    if not file:
        raise ValueError("InValued File..")
    file.seek(0)
    documents = PdfReader(file,strict=False)
    text = " "
    for page in documents.pages:
        text += page.extract_text() + "\n"
    return text       
