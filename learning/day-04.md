# Day 4 - 面向对象、组合、继承与 Property

## 1. 今日目标

- 使用 Python `class` 表达明确的数据模型
- 理解 `__init__`、实例属性、类属性与实例方法
- 学会使用 `__repr__()` 改善自定义对象的调试输出
- 理解继承、`super()`、方法重写与多态
- 理解组合（composition）与继承（inheritance）的语义区别
- 将项目中的 `dict` 数据逐步迁移为 `Document` / `SearchResult`
- 理解 `@property` 如何在不破坏组合关系的前提下简化访问接口

---

## 2. 从 dict 到自定义类

原来一篇文档使用：

```python
{
    "id": 1,
    "source": "regulation_a",
    "content": "银行贷款需要进行风险管理"
}
```

访问：

```python
doc["id"]
doc["source"]
doc["content"]
```

Day 4 创建：

```python
class Document:
    def __init__(self, id: int, source: str, content: str):
        self.id = id
        self.source = source
        self.content = content
```

访问改为：

```python
doc.id
doc.source
doc.content
```

项目开始从 `dict["key"]` 迁移到 `object.attribute`。

---

## 3. `self` 与实例属性

`self` 可以先粗略类比 C++ 中的 `this`。

```python
def __init__(self, id: int):
    self.id = id
```

其中：

```text
id
→ 当前函数调用的参数

self.id
→ 当前实例自己的属性
```

不同实例拥有独立状态。

---

## 4. 类属性与实例方法

类属性示例：

```python
class Document:
    object_type = "document"
```

其中：

```text
self.id / self.source / self.content
→ instance attribute

Document.object_type
→ class attribute
```

实例方法：

```python
def contains_keyword(self, keyword: str) -> bool:
    return keyword in self.content
```

形成：

```text
属性 → 对象有什么数据
方法 → 对象能做什么
```

---

## 5. `__repr__()` 与对象输出

直接：

```python
print(res1)
```

默认可能得到：

```text
<models.SearchResult object at 0x...>
```

表示这是 `models.SearchResult` 的一个对象实例。

可以定义：

```python
def __repr__(self) -> str:
    return (
        f"Document("
        f"id={self.id}, "
        f"source={self.source!r}, "
        f"content={self.content!r}"
        f")"
    )
```

`!r` 使用对象自己的 `repr()` 表示，更适合调试字符串和嵌套对象。

---

## 6. 组合：`SearchResult has a Document`

```python
class SearchResult:
    def __init__(self, document: Document, score: int):
        self.document = document
        self.score = score
```

结构：

```text
SearchResult
├── document → Document
└── score
```

这是组合：

```text
SearchResult has a Document
```

而不是：

```text
SearchResult is a Document
```

---

## 7. 组合、继承与独立扁平模型

### 组合

```text
SearchResult
├── document → Document
└── score
```

特点：

- 语义清晰
- 保留同一个 Document 实例
- 适合 has-a 关系

### 继承

```text
RegulationDocument is a Document
```

适合真正的 is-a 关系。

### 独立扁平模型

```text
SearchResult
├── id
├── source
├── content
└── score
```

这不是继承，只是另一个独立类拥有相似字段。

主要风险不是简单的内存成本，而是可能形成：

```text
Document.content
SearchResult.content
```

两套状态来源。

---

## 8. 项目从 dict 迁移到对象

原数据流：

```text
documents.json
↓
json.load()
↓
list[dict]
↓
retrieve_documents()
↓
list[dict]
```

迁移为：

```text
documents.json
↓
json.load()
↓
list[dict]
↓
data_loader 转换
↓
list[Document]
↓
retriever
↓
list[SearchResult]
```

### `data_loader.py`

目标：

```python
def load_documents(file_path: str) -> list[Document]:
```

### `retriever.py`

目标：

```python
def calculate_score(
    doc: Document,
    keywords: set[str]
) -> int:
```

原来：

```python
doc["content"]
```

变成：

```python
doc.content
```

或：

```python
doc.contains_keyword(keyword)
```

---

## 9. 今日遇到的问题

### 问题 1：`Document` 不能使用 `**doc`

原代码：

```python
documents_with_scores.append({
    **doc,
    "score": score
})
```

报错：

```text
'Document' object is not a mapping
```

原因：

```python
**doc
```

要求 `doc` 是 mapping，例如 dict。

解决：

```python
documents_with_scores.append(
    SearchResult(doc, score)
)
```

---

### 问题 2：`sorted()` 仍然可以排序自定义对象

原来：

```python
key=lambda x: x["score"]
```

现在 `x` 是 `SearchResult`：

```python
key=lambda x: x.score
```

因此不需要自己重写排序算法。

---

### 问题 3：组合后访问链变长

原来：

```python
doc["id"]
```

迁移后：

```python
result.document.id
```

首先需要把变量名从 `doc` 改成更准确的：

```python
result
```

因为当前元素已经是 `SearchResult`。

---

## 10. 继承、`super()` 与多态

真正满足 is-a 关系时可以继承：

```python
class RegulationDocument(Document):
    def __init__(
        self,
        id: int,
        source: str,
        content: str,
        department: str
    ):
        super().__init__(id, source, content)
        self.department = department
```

`super().__init__()` 调用父类初始化逻辑。

父类和子类可以定义同名方法：

```python
def get_label(self) -> str:
    ...
```

子类重新实现叫 method overriding（方法重写）。

通过：

```python
isinstance(regulation_doc, Document)
```

可以验证继承关系。

父类接口可以接收子类对象，并根据实际对象调用对应方法，这体现了多态。

---

## 11. `@property`

为了避免：

```python
result.document.id
result.document.source
result.document.content
```

可以在 `SearchResult` 中提供：

```python
@property
def id(self) -> int:
    return self.document.id
```

同理：

```python
@property
def source(self) -> str:
    return self.document.source

@property
def content(self) -> str:
    return self.document.content
```

外部就可以：

```python
result.id
result.source
result.content
result.score
```

内部依然保持组合关系。

`@property` 可以理解为：

> 让一个方法以属性访问的形式对外暴露。

---

## 12. 为什么 property 比复制字段更合理

如果直接：

```python
self.content = document.content
```

可能形成：

```text
document.content
result.content
```

两套状态。

property：

```python
@property
def content(self):
    return self.document.content
```

每次都从真正的 `Document` 中读取，保持：

```text
single source of truth
单一数据源
```

---

## 13. Python 与 C++ getter/setter 的差异

Python 通常不会一开始就机械写：

```text
get_id()
set_id()
get_source()
set_source()
```

通常直接：

```python
doc.id
doc.source
doc.content
```

当某个属性确实需要：

```text
校验
只读
计算
转换
转发
```

时，再考虑 `@property`。

---

## 14. 今日项目演进

Day 3：

```text
documents.json
↓
list[dict]
↓
retriever
↓
list[dict]
```

Day 4：

```text
documents.json
↓
list[dict]
↓
data_loader
↓
list[Document]
↓
retriever
↓
list[SearchResult]
↓
main
```

项目开始拥有明确的数据模型。

---

## 15. 今日需要记住

- `self` 可以粗略类比 C++ 的 `this`
- `__init__` 用于初始化实例
- 实例属性属于具体对象
- 类属性属于类本身
- 实例方法描述对象行为
- `__repr__()` 用于提供更有价值的调试表示
- `!r` 更适合调试字符串和嵌套对象
- `A is a B` 时考虑继承
- `A has a B` 时考虑组合
- 不要只为了复用几个字段而使用继承
- `SearchResult` 更适合组合 `Document`
- `sorted()` 可以直接排序自定义对象，只需提供合适的 `key`
- dict 访问 `x["score"]` 迁移为对象访问 `x.score`
- `super()` 用于调用父类实现
- 子类可以继承和重写父类方法
- `isinstance()` 可以验证继承关系
- 多态允许父类接口处理不同子类对象
- `@property` 可以在保持组合关系的同时提供更短的访问接口
- 避免多个字段副本造成多套状态来源
