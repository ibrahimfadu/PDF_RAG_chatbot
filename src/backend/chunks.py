from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk(data: list[dict])->list[dict]:
    result = []
    text_split = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap = 100)
    for item_id,item in enumerate(data,start=1):

        pices = text_split.split_text(item.get("text"))
        for ix,pice in enumerate(pices,start=1):
            new_item = {
                **item,
                "id": f"p{item.get("page_no")}f{item.get("filename")}i{ix}",
                "chunk_id": ix,
            }
            result.append(new_item)

    return result;

