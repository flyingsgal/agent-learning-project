from retriever import retrieve_documents
from data_loader import load_documents
import json
def print_search_results(documents_with_scores:list[dict]) -> None:
    for doc in documents_with_scores:
        print(f"Document ID: {doc['id']},Source:{doc['source']},Content:{doc['content']},Score:{doc['score']}")

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
    # documents_with_scores = retrieve_documents(documents, keywords)
    # print_search_results(documents_with_scores)
    print(type(documents))
    print(type(documents[0]))
    print(documents[0])
if __name__ == "__main__":
    main()