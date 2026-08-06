from pypdf import PdfReader

class Loader:
    def load_file(self,file: str) ->str:
        if not file:
            raise ValueError("InValued File..")
        documents = PdfReader(file,strict=False)
        text = " "
        for page in documents.pages:
            text += page.extract_text() + "\n"
        return text
