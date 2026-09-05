def main():
    print("Agent learning project started.")
    documents = [{"id":1,"source":"regulation_a","content":"银行贷款需要进行风险管理"},
                 {"id":2,"source":"regulation_b","content":"银行9点开门上班"},
                 {"id":3,"source":"regulation_c","content":"贷款需要去银行办理"},
                 {"id":4,"source":"regulation_d","content":"我要管理银行的贷款"},
                 {"id":5,"source":"regulation_e","content":"we are the champions"}]
    keywords = {"银行", "贷款", "风险", "管理"}
    documents_with_scores = []
    for doc in documents:
        score = 0
        for keyword in keywords:
            if keyword in doc["content"]:
                score += 1
        if score > 0:
            #这么做原始 documents 里的命中文档也已经多了 "score"，
            # doc["score"] = score
            # documents_with_scores.append(doc)
            #不修改原始 documents，使用一个新的 dict

            documents_with_scores.append({"id":doc['id'],"source":doc['source'],"content":doc['content'],"score":score})
            # 写法 1：最直观
            new_doc = doc.copy()
            new_doc["score"] = score
            documents_with_scores.append(new_doc)

            # 写法 2：“append 后再改最后一个”
            documents_with_scores.append(doc.copy()) #注意这里是copy，直接使用doc还是会修改documents
            documents_with_scores[-1]["score"] = score

            # 写法 3：更 Pythonic
            documents_with_scores.append({**doc,"score":score})

        #不用边遍历list边删除元素，容易出错，要修改一般是新建一个list
        # else:
        #     documents.remove(doc)

    sorted_documents = sorted(documents_with_scores,key = lambda x : x["score"],reverse=True)   
    # for doc in sorted_documents:
    #     # print(f"Document ID: {doc['id']}, Source: {doc['source']}, Content:{doc['content']}, Score: {doc.get('score', 0)}")
    #     print(f"Document ID: {doc['id']}, Source: {doc['source']}, Content:{doc['content']}, Score: {doc['score']}")
    print(documents)
    print(sorted_documents)

if __name__ == "__main__":
    main()