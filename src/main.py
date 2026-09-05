from retriever import retrieve_documents
def print_search_results(documents_with_scores:list[dict]) -> None:
    for doc in documents_with_scores:
        print(f"Document ID: {doc['id']},Source:{doc['source']},Content:{doc['content']},Score:{doc['score']}")

def print_dict(d:list[dict]) ->None:
    for key,value in d.item():
        print(f"{key}:{value}")
    print()

def main():
    print("Agent learning project started.")
    documents = [{"id":1,"source":"regulation_a","content":"银行贷款需要进行风险管理"},
                 {"id":2,"source":"regulation_b","content":"银行9点开门上班"},
                 {"id":3,"source":"regulation_c","content":"贷款需要去银行办理"},
                 {"id":4,"source":"regulation_d","content":"我要管理银行的贷款"},
                 {"id":5,"source":"regulation_e","content":"we are the champions"}]
    keywords = {"银行", "贷款", "风险", "管理"}
    documents_with_scores = retrieve_documents(documents, keywords)
    print_search_results(documents_with_scores)

if __name__ == "__main__":
    main()