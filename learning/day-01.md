# Day 1 - Python 容器与简单文档检索

## 1. 今日目标

- 复习 Python 常用容器：`list`、`dict`、`set`、`tuple`
- 熟悉遍历、成员判断和排序
- 理解 mutable / immutable 与引用关系
- 使用 Python 基础数据结构实现简单内存文档检索器

---

## 2. 知识点学习过程

### 2.1 `list`

`list` 用于保存一组有顺序的数据。

项目中：

```python
documents = [
    {...},
    {...},
    {...}
]
```

用于保存多篇文档。

检索结果使用新的 list：

```python
documents_with_scores = []
```

常用操作：

```python
my_list.append(x)
my_list[0]
my_list[-1]
```

`my_list[-1]` 表示最后一个元素。

### 2.2 `dict`

单篇文档使用 dict：

```python
{
    "id": 1,
    "source": "regulation_a",
    "content": "银行贷款需要进行风险管理"
}
```

因为一篇文档包含多个有明确语义的字段：`id`、`source`、`content`。

### 2.3 `dict["key"]` 与 `dict.get()`

严格访问：

```python
doc["score"]
```

字段不存在会抛出 `KeyError`。

宽容访问：

```python
doc.get("score", 0)
```

字段不存在时返回默认值 `0`。

当前项目中，排序后的结果理论上一定具有 `score`，因此使用 `doc["score"]` 更适合暴露逻辑错误。

### 2.4 `set`

关键词使用：

```python
keywords = {"银行", "贷款", "风险", "管理"}
```

`set` 适合去重和成员判断。

不能写：

```python
set = {...}
```

因为会覆盖 Python 内置的 `set()`。

### 2.5 `tuple`

`tuple` 与 list 都能保存多个元素。

主要区别：

```text
list  → 可修改
tuple → 创建后不能修改
```

由此开始理解 mutable 与 immutable。

### 2.6 计算 score

```python
score = 0

for keyword in keywords:
    if keyword in doc["content"]:
        score += 1
```

当前 score 表示一篇文档命中了多少个关键词。

### 2.7 `sorted` 对 dict 列表排序

```python
sorted_documents = sorted(
    documents_with_scores,
    key=lambda x: x["score"],
    reverse=True
)
```

其中：

```python
lambda x: x["score"]
```

表示使用每个 dict 的 `score` 作为排序依据。

它可以暂时理解为：

```python
def get_score(x):
    return x["score"]
```

`reverse=True` 表示从高到低排序。

### 2.8 mutable 与引用

最开始：

```python
doc["score"] = score
documents_with_scores.append(doc)
```

后来发现原始 `documents` 中对应的 dict 也出现了 `score`。

原因：`doc` 不是副本，而是指向原 dict 对象的引用。

```text
documents 中的 dict
        ↑
       doc
        ↓
documents_with_scores
```

所以修改 `doc` 实际上就是修改原对象。

### 2.9 创建新的 dict

为了保留原始 `documents`，改为创建新 dict。

最直观：

```python
{
    "id": doc["id"],
    "source": doc["source"],
    "content": doc["content"],
    "score": score
}
```

更简洁：

```python
{
    **doc,
    "score": score
}
```

也认识了：

```python
doc.copy()
```

可以创建一个新的浅拷贝。

---

## 3. 遇到的问题并解决

### 问题 1：遍历 list 时同时删除元素

最开始：

```python
for doc in documents:
    ...
    documents.remove(doc)
```

问题：遍历过程中删除元素会改变 list 结构，可能导致元素被跳过。

解决：不修改原始 `documents`，新建结果集合：

```python
documents_with_scores = []
```

符合条件时 append 新结果。

### 问题 2：不知道 dict 列表如何按 score 排序

解决：

```python
sorted(
    documents_with_scores,
    key=lambda x: x["score"],
    reverse=True
)
```

掌握了 `key` 与 `lambda` 的基本用途。

### 问题 3：`append(doc)` 后原始数据也发生变化

原因：`append(doc)` 不会复制 dict，而是保存同一个对象的引用。

解决：

```python
# 写法 1：最直观
new_doc = doc.copy()
new_doc["score"] = score
documents_with_scores.append(new_doc)
# 写法 2：“append 后再改最后一个”
documents_with_scores.append(doc.copy()) #注意这里是copy，直接使用doc还是会修改documents
documents_with_scores[-1]["score"] = score
# 写法 3：更 Pythonic
documents_with_scores.append({**doc,"score":score})
```

这样原始 `documents` 保持不变，新的结果 list 保存带 `score` 的文档。

### 问题 4：想先 append，再给新元素增加 score

可以用：

```python
documents_with_scores[-1]
```

访问刚 append 的最后一个元素。

例如：

```python
documents_with_scores.append(doc.copy())
documents_with_scores[-1]["score"] = score
```

但当前更推荐直接构造新 dict，语义更清晰。

### 问题 5：变量名使用 `set`

最初：

```python
set = {"银行", "贷款", "风险", "管理"}
```

会覆盖 Python 内置 `set()`。

解决：

```python
keywords = {"银行", "贷款", "风险", "管理"}
```

### 问题 6：GitHub push 再次失败

出现：

```text
Failed to connect to github.com port 443
Could not connect to server
```

`git remote -v` 正常，而 `git ls-remote origin` 仍失败，因此判断是网络到 GitHub 的连接问题，不是 Git 配置问题。

本地可以继续开发并 commit，网络恢复后再 push。

### 问题 7：Codex 每次先重连 5 次

日志：

```text
stream disconnected
retrying sampling request (1/5)
...
retrying sampling request (5/5)
falling back to HTTP
```

说明 Codex 流式连接反复断开，5 次重试失败后退回普通 HTTP。

该问题与 Python 项目代码无关，因此不阻塞学习主线。

---

## 4. 今日项目结果

实现：

```text
documents
    ↓
遍历文档
    ↓
遍历 keywords
    ↓
判断 keyword 是否在 content 中
    ↓
计算 score
    ↓
保留 score > 0
    ↓
生成新的带 score 文档
    ↓
按 score 降序排序
    ↓
打印结果
```

项目从“只能打印启动信息”演进到：

```text
V0.1 简单内存文档检索器
```

---

## 5. 今日需要记住

- 多篇文档：`list`
- 单篇文档：`dict`
- 无重复关键词：`set`
- `tuple` 不可修改
- 遍历 list 时不要同时删除元素
- `dict["key"]` 与 `dict.get()` 的使用场景不同
- `sorted(..., key=..., reverse=True)` 可以按照 dict 字段排序
- `lambda` 可以表达一个很短的匿名函数
- `append(doc)` 不代表复制对象
- list / dict 属于 mutable 对象
- `doc.copy()` 或 `{**doc, ...}` 可以生成新的 dict
