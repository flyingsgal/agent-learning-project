#list
# scores = [3, 1, 5, 2]
# scores.append(4)
# print(scores)  # Output: [3, 1, 5, 2, 4]
# scores.remove(1)
# print(scores)  # Output: [3, 5, 2, 4]
# print(scores[:2])
# # scores.sort()
# # print(scores)  # Output: [2, 3, 4, 5]
# # for score in scores:
# #     print(score)
# print(scores[1:3]) #左闭右开

#dictionary
# source = {"id": 1, "source": "regulation_a", "content": "银行贷款需要进行风险管理"}
# print(source)
# source["score"] = 100
# for key in source:
#     print(key, source[key])
# source.pop("score")
# print(source)

#set
# keywords = {"银行", "贷款", "银行", "风险"}
# print(keywords)  # Output: {'银行', '贷款', '风险'}
# keywords.add("管理")
# print(keywords)  # Output: {'银行', '贷款', '风险', '管理'}
# if "银行" in keywords:
#     print("银行 is in the set")

#tuple
# tup = ("qwe",3)
# print(tup[0])  # Output: qwe
# tup[0] = "asd"  # This will raise an error because tuples are immutable

#list 和 tuple 最大区别是什么？ 可变性，list可以修改，tuple不行，list只有一种类型，tuple有多种类型
#dict 为什么适合表示一篇 document？ 有键值对
#set 为什么适合保存关键词？ 每个元素不重复
#list 和 C++ vector 有哪些相似点？ 都是动态数组，支持随机访问和动态扩展

from models import Document,SearchResult,RegulationDocument
doc1 = Document(1, "regulation_a", "银行贷款需要进行风险管理")
doc2 = Document(2, "regulation_b", "银行9点开门上班")
# doc = RegulationDocument(
#     1,
#     "regulation_a",
#     "银行贷款需要进行风险管理",
#     "risk_management"
# )
doc = RegulationDocument(doc1.id, doc1.source, doc1.content, "risk_management")
print(isinstance(doc, RegulationDocument))
print(isinstance(doc, Document))
print(doc1.get_label())
print(doc.get_label())