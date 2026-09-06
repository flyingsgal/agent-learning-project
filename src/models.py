class Document:
    object_type = "document"
    def __init__(self,id:int,source:str,content:str):
        self.id = id
        self.source = source
        self.content = content
    
    def contains_keyword(self,keyword:str) -> bool:
        return keyword in self.content
    
    def get_label(self) -> str:
        return "普通文档"

    def __repr__(self):
        # return f"Document(id = {self.id},source = '{self.source}',content = '{self.content}')"
        # !r表示用这个值自己的 repr() 形式输出。
        return (
            f"Document("
            f"id={self.id!r}, "
            f"source={self.source!r}, "
            f"content={self.content!r}"
            f")"
        )
    
class SearchResult:
    def __init__(self,document:Document,score:int):
        self.document = document
        self.score = score
    
    #使用@property装饰器将方法变为属性，这样可以通过result.id访问，而不是result.document.id
    #如果复制一份self.id = document.id，会产生两套状态，result.document.content和result.content
    @property
    def id(self) -> int:
        return self.document.id
    @property
    def source(self) -> str:
        return self.document.source
    @property
    def content(self) -> str:
        return self.document.content
    #目前这种写法只有getter，没有setter，如果需要修改属性，修改参数：
    @content.setter
    def content(self,value : str) -> None:
        self.document.content = value

    def __repr__(self):
        # return f"SearchResult(document = {self.document!r},score = {self.score})"
        return (
            f"SearchResult("
            f"document={self.document!r}, "
            f"score={self.score!r}"
            f")"
        )

class RegulationDocument(Document):
    def __init__(self, id:int, source:str, content:str,department:str):
        super().__init__(id, source, content)
        self.department = department

    def get_label(self) -> str:
        return "监管文档"
