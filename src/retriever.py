def calculate_score(doc:dict, keywords:set[str]) -> int:
    score = 0
    for keyword in keywords:
        if keyword in doc["content"]:
            score +=1
    return score

def retrieve_documents(documents:list[dict], keywords:set[str], reverse:bool=True) -> list[dict]:
    documents_with_scores = []
    for doc in documents:
        score = calculate_score(doc,keywords)
        if score > 0:
            documents_with_scores.append({**doc,"score":score})
    return sorted(documents_with_scores,key = lambda x:x["score"],reverse = True)