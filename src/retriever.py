from models import Document, SearchResult
from collections.abc import Iterator
from utils import timer
def calculate_score(doc:Document, keywords:set[str]) -> int:
    score = 0
    for keyword in keywords:
        if doc.contains_keyword(keyword):
            score +=1
    return score

@timer
def retrieve_documents(documents:list[Document], keywords:set[str], reverse:bool=True) -> list[SearchResult]:
    documents_with_scores = []
    for doc in documents:
        score = calculate_score(doc,keywords)
        if score > 0:
            doc_with_score = SearchResult(doc,score)
            documents_with_scores.append(doc_with_score)
    #此处x为SearchResult 对象，x.score为其score属性,不能再使用dict的形式x["score"]去访问
    return sorted(documents_with_scores,key = lambda x:x.score,reverse = reverse)

def generate_search_results(document : list[Document], key : set[str]) ->Iterator[SearchResult]:
    for doc in document:
        score = calculate_score(doc,key)
        if score > 0:
            yield SearchResult(doc,score)

def sorted_results(documents : list[Document], keywords : set[str])-> list[SearchResult]:
    #<class 'generator'>
    generator = generate_search_results(documents, keywords)
    #<class 'list'>。Python 内置函数 sorted(iterable) 的返回值规范就是一个新的 list。
    search_results=sorted(generator,key=lambda x:x.score,reverse=True) 
    return search_results
