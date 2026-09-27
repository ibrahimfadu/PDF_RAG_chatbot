from pypdf import PdfReader
from urllib.parse import urlparse
import os

def file_name(file_path: str)->str:
    filename = os.path.basename(urlparse(file_path).path)
    return filename



def fileData(file_path :str) -> list[dict]:
    list_text = [];
    data = PdfReader(file_path)
    filename = file_name(file_path) 
    for page_no,page in enumerate(data.pages,start=1):
        dic = { 
            "filename":filename,
            "url":file_path,
            "text" : (page.extract_text()) ,
            "page_no": page_no 
        }
        list_text.append(dic)
    return list_text

    



