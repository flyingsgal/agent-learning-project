# Day 3 - JSON 文件读取、异常处理与数据加载模块

## 1. 今日目标

- 将 `documents` 从 `main.py` 中移出，保存到独立 JSON 文件
- 学会使用 `open()` 和 `with open(...)`
- 理解 `json.load()` 与 `json.loads()` 的区别
- 学会处理常见文件读取异常
- 理解 `try / except`
- 理解异常传播（exception propagation）
- 将数据读取逻辑拆到 `data_loader.py`
- 进一步明确模块职责边界

---

## 2. 知识点学习过程

### 2.1 将数据和代码分离

Day 2 时，文档数据仍然直接写在 `main.py` 中。Day 3 将数据移到：

```text
data/
└── documents.json
```

程序开始变为：

```text
JSON 数据文件
    ↓
Python 加载
    ↓
documents
    ↓
retriever
```

实现：

```text
代码 → src/
数据 → data/
```

---

### 2.2 JSON 与 Python 数据结构的对应

常见对应关系：

```text
JSON array  → Python list
JSON object → Python dict
JSON string → Python str
```

JSON 与 Python 语法并不完全相同，例如 JSON 的字符串和 key 使用双引号。

---

### 2.3 使用 `with open(...)` 读取文件

```python
with open(
    "data/documents.json",
    "r",
    encoding="utf-8"
) as file:
    documents = json.load(file)
```

其中：

```text
"r" → read，只读模式
encoding="utf-8" → 使用 UTF-8 解码
```

`with open(...)` 可以理解为：

```text
打开文件
↓
在代码块中使用
↓
离开代码块后自动关闭资源
```

当前项目路径统一使用：

```python
"data/documents.json"
```

---

### 2.4 `json.load()` 与 `json.loads()`

文件对象：

```python
with open("data/documents.json", "r", encoding="utf-8") as file:
    documents = json.load(file)
```

可以记：

```text
load → file
```

JSON 字符串：

```python
text = '[{"id": 1}]'
documents = json.loads(text)
```

可以记：

```text
loads → string
```

---

### 2.5 验证 JSON 到 Python 的转换

读取后打印：

```python
print(type(documents))
print(type(documents[0]))
print(documents[0])
```

观察到：

```text
<class 'list'>
<class 'dict'>
...
```

说明：

```text
JSON array
↓ json.load()
Python list

JSON object
↓
Python dict
```

---

## 3. 异常处理

### 3.1 文件不存在

将路径临时改成：

```python
"data/not_exist.json"
```

得到：

```text
FileNotFoundError
```

说明：

```text
文件路径错误 / 文件不存在
→ FileNotFoundError
```

---

### 3.2 JSON 格式错误

故意删除 JSON 中必要的逗号后，得到：

```text
json.decoder.JSONDecodeError
```

说明：

```text
文件存在，但 JSON 格式非法
→ JSONDecodeError
```

---

### 3.3 `try / except`

在 `main.py` 中：

```python
try:
    documents = load_documents("data/documents.json")

except FileNotFoundError as e:
    print(f"文件不存在，请检查文件路径：{e}")
    return

except json.JSONDecodeError as e:
    print(f"JSON 解码错误，请检查文件内容是否为有效 JSON：{e}")
    return

except UnicodeDecodeError as e:
    print(f"文件编码错误，请检查文件编码格式：{e}")
    return
```

执行逻辑：

```text
正常
→ try 完成
→ 跳过 except
→ 继续程序

异常
→ 跳到匹配的 except
→ 处理错误
```

---

### 3.4 为什么不使用裸 `except`

不推荐：

```python
except:
    print("出错了")
```

因为可能把：

```text
IndexError
KeyError
TypeError
逻辑 bug
```

等完全不同的问题一起吞掉。

当前只捕获明确知道如何处理的异常：

```text
FileNotFoundError
JSONDecodeError
UnicodeDecodeError
```

---

### 3.5 `as e`

例如：

```python
except FileNotFoundError as e:
```

`e` 保存异常对象，可以输出具体错误：

```python
print(f"文件读取失败：{e}")
```

---

### 3.6 为什么异常后 `return`

如果文档没有成功读取：

```text
documents 不可用
↓
后续检索没有意义
```

因此：

```text
加载失败
→ 打印错误
→ return
→ 结束 main
```

---

## 4. 数据加载模块

### 4.1 创建 `data_loader.py`

项目增加：

```text
src/
├── main.py
├── retriever.py
└── data_loader.py
```

`data_loader.py`：

```python
import json

def load_documents(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return documents
```

职责：

```text
file_path
↓
open
↓
json.load
↓
return documents
```

---

### 4.2 为什么 `data_loader.py` 不处理异常

最终职责：

```text
data_loader.py
→ 负责“怎么加载数据”

main.py
→ 负责“加载失败以后怎么办”
```

原因是同一个 `load_documents()` 后续可能被不同调用方使用：

```text
命令行程序
FastAPI
测试代码
LangGraph Node
```

不同调用方对错误的处理方式可能不同。

例如：

```text
命令行 → print 错误
FastAPI → 返回 HTTP 错误
测试 → 让异常直接暴露
LangGraph → 写入 state.error
```

因此当前理解为：

> 底层函数负责做事，上层调用者决定错误怎么处理。

---

### 4.3 异常传播 Exception Propagation

如果 `data_loader.py` 中：

```python
def load_documents(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
```

`open()` 抛出 `FileNotFoundError`，而当前函数没有捕获，则异常会继续向调用方传播：

```text
open()
↓
load_documents()
↓
main()
```

然后由 `main()` 中的 `try / except` 捕获。

这叫：

```text
exception propagation
异常传播
```

---

## 5. 今日项目结构

```text
agent-learning-project/
├── data/
│   └── documents.json
├── learning/
│   ├── README.md
│   ├── Agent 7-Week Study Plan.md
│   ├── day-00.md
│   ├── day-01.md
│   ├── day-02.md
│   └── day-03.md
└── src/
    ├── main.py
    ├── retriever.py
    └── data_loader.py
```

职责：

```text
main.py
→ orchestration / 流程编排
→ 处理上层异常
→ 调用各模块

data_loader.py
→ I/O / 数据输入
→ 加载 JSON

retriever.py
→ business logic / 检索逻辑
→ 评分、过滤、排序
```

---

## 6. 项目演进

```text
Day 1
main.py
├── 数据
├── 检索
└── 输出

        ↓

Day 2
main.py
→ 流程

retriever.py
→ 检索逻辑

        ↓

Day 3
data/documents.json
→ 数据

data_loader.py
→ 数据加载

retriever.py
→ 检索逻辑

main.py
→ 流程编排 + 异常处理
```

项目继续从“能运行的 Python 脚本”向“有明确职责边界的小型工程”演进。

---

## 7. 今日遇到的问题并解决

### 问题 1：`load()` 和 `loads()` 容易混淆

修正为：

```text
json.load(file)
→ 文件对象

json.loads(text)
→ JSON 字符串
```

### 问题 2：文件路径不存在

错误：

```text
FileNotFoundError
```

解决：

在上层 `main()` 捕获并输出具体错误信息。

### 问题 3：JSON 内容写错

错误：

```text
JSONDecodeError
```

解决：

在 `main()` 捕获并提示检查 JSON 格式。

### 问题 4：编码错误

加入：

```text
UnicodeDecodeError
```

处理文件编码不符合预期的情况。

### 问题 5：异常处理放在哪里

拆模块后明确：

```text
data_loader → 只负责加载
main → 决定加载失败后怎么办
```

通过异常传播实现职责分离。

---

## 8. 今日需要记住

- JSON 数据应该和 Python 业务代码分离
- `with open(...)` 用于管理文件资源
- `"r"` 表示只读模式
- 中文文件显式使用 `encoding="utf-8"`
- `json.load()` 读取文件对象
- `json.loads()` 解析 JSON 字符串
- JSON array 会转换为 Python list
- JSON object 会转换为 Python dict
- `try / except` 用于处理预期异常
- `as e` 可以获得异常对象
- 不要轻易使用裸 `except`
- 文件不存在常见为 `FileNotFoundError`
- JSON 格式错误常见为 `JSONDecodeError`
- 编码错误可能是 `UnicodeDecodeError`
- 读取失败后如果程序无法继续，应及时 `return`
- 异常可以从底层函数向上层调用者传播
- 底层模块负责做事，上层模块决定错误处理策略
- `main.py`、`data_loader.py`、`retriever.py` 已形成初步职责分层
