import json
from models import Document, SearchResult
def load_documents(file_path:str) -> list[Document]:
    # data_loader.py负责加载数据，main.py负责“加载失败以后程序怎么办”，这里只写正常逻辑,不写异常处理
    # 更好的职责边界是：底层函数负责做事；上层调用者决定错误怎么处理。
    with open(file_path,"r",encoding = "utf-8") as file:
        documents = json.load(file) # file是文件对象，使用load；如果是字符串，使用loads
    doc = []
    for d in documents:
        # d = Document(d)
        d = Document(d["id"],d["source"],d["content"])
        doc.append(d)
    return doc