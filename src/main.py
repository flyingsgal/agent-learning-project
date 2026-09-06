from retriever import retrieve_documents,generate_search_results
from data_loader import load_documents
from models import Document, SearchResult
import json
def print_search_results(searchResults:list[SearchResult]) -> None:
    for result in searchResults:
        # print(f"Document ID: {doc['id']},Source:{doc['source']},Content:{doc['content']},Score:{doc['score']}")
        # print(f"Document ID: {result.document.id},Source:{result.document.source},Content:{result.document.content},Score:{result.score}")
        print(f"Document ID: {result.id},Source:{result.source},Content:{result.content},Score:{result.score}")

def main():
    try:
        documents = load_documents("data/documents.json")
    except FileNotFoundError as e:
        print(f"文件不存在，请检查文件路径:{e}")
        return
    except json.JSONDecodeError as e:
        print(f"JSON解码错误，请检查文件内容是否为有效的JSON格式。:{e}")
        return
    except UnicodeDecodeError as e:
        print(f"文件编码错误，请检查文件编码格式。:{e}")
        return
    keywords = {"银行", "贷款", "风险", "管理"}
    # print(type(documents))
    # print(type(documents[0]))
    # print(documents[0])
    documents_with_scores = retrieve_documents(documents, keywords)
    print_search_results(documents_with_scores)
    # generator = generate_search_results(documents, keywords)
    # search_results = sorted(
    #     generator,
    #     key=lambda x: x.score,
    #     reverse=True
    # )
    # for result in generator:
    #     print(result)
    print(retrieve_documents.__name__)

if __name__ == "__main__":
    main()