# Day 2 - 函数、类型注解与模块化

## 1. 今日目标

- 将 Day 1 的单文件脚本拆成职责清晰的函数
- 理解参数、返回值和局部变量
- 学习 Python 类型注解
- 将检索逻辑从 `main.py` 拆到独立模块 `retriever.py`
- 开始建立“脚本 → 模块化项目”的工程化思维

---

## 2. 知识点学习过程

### 2.1 从一大段 `main()` 拆成多个函数

Day 1 的检索逻辑最初全部写在 `main()` 中：

```text
main()
├── 初始化 documents
├── 初始化 keywords
├── 计算 score
├── 过滤
├── 排序
└── 输出
```

Day 2 将职责拆分为：

```text
main()
│
├── retrieve_documents()
│       └── calculate_score()
│
└── print_search_results()
```

当前每个函数的职责：

```text
calculate_score()
→ 计算一篇文档的关键词命中分数

retrieve_documents()
→ 遍历文档、过滤无关文档、排序并返回结果

print_search_results()
→ 负责展示检索结果

main()
→ 初始化数据并组织整个程序执行流程
```

---

### 2.2 参数与返回值

评分函数：

```python
def calculate_score(doc, keywords):
    score = 0

    for keyword in keywords:
        if keyword in doc["content"]:
            score += 1

    return score
```

这里：

```text
doc
keywords
```

是函数参数。

```python
return score
```

表示把计算结果返回给调用方。

调用：

```python
score = calculate_score(doc, keywords)
```

需要区分：

```python
print(score)
```

只是把数据输出给人看，

而：

```python
return score
```

是把结果交回程序继续使用。

---

### 2.3 单一职责

函数不是为了单纯减少代码行数，而是为了让每一部分逻辑只负责一件事。

例如：

```python
calculate_score()
```

只负责：

```text
doc + keywords
        ↓
      score
```

它不负责排序、打印，也不直接修改整个文档列表。

这样以后可以单独检查：

```text
评分逻辑是否正确？
检索逻辑是否正确？
展示逻辑是否正确？
```

---

### 2.4 `print_search_results()` 是否应该做成通用函数

最开始觉得显式打印：

```python
doc["id"]
doc["source"]
doc["content"]
doc["score"]
```

只能适用于当前 document 结构，不够“自适应”。

确实可以写成：

```python
for result in results:
    for key, value in result.items():
        print(f"{key}: {value}")
```

这样可以自动打印任意字段。

但后来理解：

> 能做成通用函数，不代表现在一定应该做成通用函数。

如果未来 document 增加：

```text
embedding
metadata
internal_debug
```

通用打印函数会把内部字段也全部输出。

因此当前更适合保留：

```python
print_search_results()
```

作为专门的“搜索结果展示函数”。

学习到：

```text
显式字段输出
→ 控制更强，适合业务展示

遍历 dict.items()
→ 更通用，适合调试工具
```

先围绕当前职责设计，等真正出现重复需求后再抽象。

---

### 2.5 类型注解 Type Hints

给函数增加了类型信息。

例如：

```python
def calculate_score(
    doc: dict,
    keywords: set[str]
) -> int:
```

含义：

```text
doc: dict
→ 参数预期是 dict

keywords: set[str]
→ 参数预期是由 str 组成的 set

-> int
→ 函数预期返回 int
```

检索函数：

```python
def retrieve_documents(
    documents: list[dict],
    keywords: set[str]
) -> list[dict]:
```

表示：

```text
输入：
list[dict]
set[str]

输出：
list[dict]
```

展示函数：

```python
def print_search_results(
    results: list[dict]
) -> None:
```

其中：

```python
-> None
```

表示函数不返回有意义的数据。

---

### 2.6 Type Hint 不等于运行时强制检查

Python 类型注解主要服务于：

```text
程序员
IDE
静态类型检查器
代码审查
项目维护
```

例如：

```python
def add(a: int, b: int) -> int:
    return a + b
```

类型注解表达了设计意图，但 Python 本身通常不会像 C++ 一样仅凭类型注解就在运行时强制阻止错误类型调用。

因此：

```text
Type Hint
≠
Runtime Type Check
```

---

### 2.7 `list[dict]` 仍然比较宽泛

虽然：

```python
list[dict]
```

比完全没有类型信息更清晰，

但它仍然只能说明：

> 这是一个由 dict 组成的 list。

它没有规定 dict 一定包含：

```text
id
source
content
score
```

后续会逐渐学习更明确的数据模型，例如：

```text
TypedDict
dataclass
Pydantic Model
```

当前阶段先掌握基础 Type Hint。

---

### 2.8 第一次拆模块

项目结构从：

```text
src/
└── main.py
```

变成：

```text
src/
├── main.py
└── retriever.py
```

职责划分：

```text
main.py
→ 程序入口、初始化数据、组织流程、输出结果

retriever.py
→ 文档评分与检索逻辑
```

---

### 2.9 Python module

一个 `.py` 文件可以作为一个 Python module。

因此：

```text
retriever.py
```

就是 `retriever` 模块。

在 `main.py` 中使用：

```python
from retriever import retrieve_documents
```

表示：

> 从 `retriever.py` 模块中导入 `retrieve_documents` 函数。

当前不使用：

```python
from retriever import *
```

而是显式导入需要的对象，让依赖关系更清楚。

---

### 2.10 为什么 `calculate_score()` 不需要暴露给 `main.py`

`main.py` 只需要知道：

```text
给 retrieve_documents：
documents + keywords

得到：
results
```

至于检索函数内部如何计算 score，是 `retriever.py` 自己的职责。

形成：

```text
main
只关心“我要检索”

retriever
负责“具体怎么检索”
```

---

### 2.11 不把 documents 做成全局变量

没有把：

```python
documents
keywords
```

直接写成 `retriever.py` 中的全局变量。

继续保持：

```python
results = retrieve_documents(documents, keywords)
```

原因：

- 输入来源清晰
- 函数依赖更少
- 后续测试更容易
- 同一个函数可以处理不同 documents 和 keywords

---

### 2.12 默认参数、关键字参数与作用域

认识默认参数：

```python
def retrieve_documents(
    documents: list[dict],
    keywords: set[str],
    reverse: bool = True
) -> list[dict]:
```

调用时可以使用默认值：

```python
retrieve_documents(documents, keywords)
```

也可以使用关键字参数：

```python
retrieve_documents(
    documents=documents,
    keywords=keywords,
    reverse=False
)
```

关键字参数可以让调用含义更加清晰。

函数内部：

```python
score = 0
```

属于局部变量。

它主要在当前函数作用域中使用，不应该依赖函数外部的隐式状态。

---

## 3. 遇到的问题并解决

### 问题 1：VS Code / Codex 自动补全太积极

在编写函数时，VS Code 会直接给出大段代码补全。

问题：

当前阶段正在学习：

```text
函数怎么拆
参数是什么
return 什么
模块如何组织
```

如果直接使用整段 Tab 补全，代码虽然能完成，但可能跳过自己的思考过程。

解决：

建立当前学习阶段的使用规则：

```text
AI 帮忙打字
→ 可以

AI 替代正在学习的核心思考
→ 不使用
```

判断标准：

> 如果关掉补全，自己仍然能写出来，只是速度更慢，可以使用补全。

如果完全不知道怎么写，只能依赖补全，则先自己思考和实现。

---

### 问题 2：`print_search_results()` 是否应该自动打印所有 key

一开始认为手动写：

```python
doc["id"]
doc["source"]
doc["content"]
doc["score"]
```

不够通用。

后来理解：

> 业务展示函数不需要追求“万能”。

当前函数专门负责展示搜索结果，所以显式指定需要展示的字段反而更安全、更清楚。

如果未来确实需要通用调试工具，可以另写：

```python
print_records()
```

而不是把业务函数改成万能工具。

---

### 问题 3：函数拆分与面向对象的关系

开始时把：

```text
main.py
retriever.py
```

理解为 C++ 面向对象项目的起点。

进一步区分：

当前做的主要是：

```text
模块化
+
职责分离
```

还没有真正进入 OOP。

真正的面向对象后续可能出现：

```text
Document
Retriever
SearchResult
```

等类和对象。

当前演进路径可以理解为：

```text
脚本
↓
函数拆分
↓
模块拆分
↓
数据模型
↓
类 / 服务
↓
完整工程结构
```

---

## 4. 今日项目结构变化

Day 1：

```text
src/
└── main.py
```

Day 2：

```text
src/
├── main.py
└── retriever.py
```

其中：

```text
main.py
→ 初始化 documents
→ 初始化 keywords
→ 调用 retrieve_documents()
→ 调用 print_search_results()

retriever.py
→ calculate_score()
→ retrieve_documents()
```

---

## 5. 今日项目结果

项目从：

```text
V0.1
单文件简单文档检索器
```

演进为：

```text
V0.2
具有函数职责划分和模块边界的文档检索器
```

程序行为基本不变，但代码组织发生变化。

这是一次典型的：

```text
refactor
```

即：

> 在尽量不改变外部行为的情况下改善代码结构。

---

## 6. 今日需要记住

- 函数需要有清晰职责
- `return` 和 `print` 的作用不同
- 参数应该显式表达函数依赖
- 尽量避免依赖全局变量
- `list[dict]`、`set[str]`、`-> int`、`-> None` 是基础类型注解
- Type Hint 不等于运行时强制类型检查
- 一个 `.py` 文件可以是一个 module
- `from retriever import retrieve_documents` 是显式导入模块中的函数
- `main.py` 负责组织流程，`retriever.py` 负责检索逻辑
- 不要为了“通用”而过早抽象
- AI 自动补全应该帮助输入，而不是替代正在训练的思考过程
- 模块化和职责分离是后续工程化、数据模型和面向对象设计的基础
