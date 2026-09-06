# Day 05 - Iterator、Generator、Decorator 与 Context Manager

## 1. 今日目标

Day 05 是 Python 复习阶段中第一次明显偏“Python 特有机制”的一天，内容比前几天更抽象，主要学习：

- iterable 与 iterator 的区别
- `iter()` / `next()`
- generator 与 `yield`
- lazy evaluation（惰性计算）
- `sorted()` 如何消费 generator
- 函数作为对象、参数与返回值
- decorator（装饰器）
- `*args` / `**kwargs`
- closure（闭包）
- `functools.wraps`
- context manager（上下文管理器）
- `__enter__()` / `__exit__()`
- `with ... as ...`
- context manager 中的异常传播与抑制

今天的目标不是“从零手写复杂框架机制”，而是达到：

> 能解释核心机制、能读懂代码、能写简单版本、以后在 FastAPI / LangChain / LangGraph 中遇到时知道它在做什么。

---

# 2. Iterable 与 Iterator

## 2.1 Iterable

例如：

```python
numbers = [10, 20, 30]
```

`list` 是 iterable（可迭代对象），因为：

```python
for x in numbers:
    print(x)
```

可以正常遍历。

但是：

```python
next(numbers)
```

不能直接使用。

因此：

```text
list
→ iterable
→ 可以被遍历
→ 但本身不是 iterator
```

## 2.2 Iterator

通过：

```python
it = iter(numbers)
```

可以得到 iterator。

然后：

```python
print(next(it))
print(next(it))
print(next(it))
```

依次得到：

```text
10
20
30
```

继续：

```python
next(it)
```

会触发：

```text
StopIteration
```

可以粗略类比 C++ 中“记录当前遍历状态的位置对象”。

更准确地说：

```text
iterator
→ 保存遍历状态
→ 每次 next() 产生下一个元素
→ 没有元素后抛出 StopIteration
```

## 2.3 Iterator 也可以被 `for` 遍历

```python
numbers = [10, 20, 30]
it = iter(numbers)

print(next(it))

for x in it:
    print(x)
```

输出：

```text
10
20
30
```

其中 `for` 只会继续消费剩余部分。

如果 iterator 已经被消费完：

```python
for x in it:
    print(x)
```

不会再次输出内容。

而 list 可以重复 `for`，因为每次都可以重新通过 `iter(numbers)` 获得一个新的 iterator。

## 2.4 对 `for` 的粗略理解

可以先把：

```python
for x in iterable:
    ...
```

理解成：

```text
iter(iterable)
↓
不断 next(iterator)
↓
取得一个元素
↓
直到 StopIteration
```

真实实现更底层，但这个思维模型足够用于当前学习。

---

# 3. Generator 与 `yield`

## 3.1 最小 Generator

```python
def generate_numbers():
    yield 1
    yield 2
    yield 3
```

只要函数体中出现 `yield`，它就成为 generator function。

调用：

```python
g = generate_numbers()
```

得到的不是：

```python
[1, 2, 3]
```

而是一个 generator object。

```python
print(type(g))
```

会看到类似：

```text
<class 'generator'>
```

## 3.2 Generator function 调用时不会立即执行完整函数

执行：

```python
g = generate_numbers()
```

并不是：

```text
函数从头执行到尾
↓
return 一个 Iterator
```

而是：

```text
Python 发现函数体里有 yield
↓
创建 generator object
↓
保存函数代码和执行状态
↓
返回 generator object
```

真正开始运行通常是在：

```python
next(g)
```

或者：

```python
for x in g:
```

或者：

```python
sorted(g)
```

有人开始“消费”它时。

## 3.3 `yield` 的核心语义

```python
def generate_numbers():
    print("准备 1")
    yield 1

    print("准备 2")
    yield 2
```

第一次 `next(g)` 执行到 `yield 1`：

```text
产生 1
↓
暂停函数
↓
保存当前执行状态
```

第二次 `next(g)` 不会重新从函数开头执行，而是从上一次 `yield` 后继续。

可以先记：

```text
yield
=
产生一个值
+
暂停函数

下一次 next()
=
从暂停位置继续
```

## 3.4 `yield` 与 `return`

`return`：

```text
返回值
↓
当前函数调用结束
```

`yield`：

```text
产生一个值
↓
函数暂停
↓
当前调用还没有彻底结束
↓
之后可以继续
```

需要特别纠正：

```text
return ≠ 必然需要完整结果占满内存
```

之前普通检索版本占用一个完整结果列表，是因为代码主动写了：

```python
results = []
results.append(...)
return results
```

而不是因为 `return` 本身一定会占满内存。

---

# 4. 在 Retriever 中使用 Generator

原始版本：

```python
results = []

for doc in documents:
    score = calculate_score(doc, keywords)

    if score > 0:
        results.append(SearchResult(doc, score))

return results
```

Generator 版本：

```python
def generate_search_results(documents, keywords):
    for doc in documents:
        score = calculate_score(doc, keywords)

        if score > 0:
            yield SearchResult(doc, score)
```

这里不再需要：

```python
results = []
```

也不再需要：

```python
results.append(...)
```

因为：

```text
append
→ 函数自己收集全部结果

yield
→ 每得到一个结果就交给外部消费者
```

## 4.1 今日踩坑：`append(yield ...)`

曾尝试：

```python
results.append(
    yield SearchResult(doc, score)
)
```

这是错误的思维方式。

当前场景中：

```text
append
和
yield
```

代表两种不同的数据组织策略。

应该从：

```python
results.append(result)
```

直接变成：

```python
yield result
```

而不是把两者叠在一起。

---

# 5. Generator 为什么可以直接交给 `sorted()`

例如：

```python
generator = generate_search_results(
    documents,
    keywords
)

search_results = sorted(
    generator,
    key=lambda x: x.score,
    reverse=True
)
```

关键点：

```text
sorted() 接受 iterable
```

并不要求一定传入 list。

因此可以：

```python
sorted([3, 1, 2])
sorted((3, 1, 2))
sorted({3, 1, 2})
sorted(generator)
```

## 5.1 `sorted(generator)` 不是排序 generator 对象本身

不是：

```text
对 <generator object ...> 排序
```

而是：

```text
sorted 主动消费 generator
↓
generator 不断 yield 元素
↓
sorted 收集这些元素
↓
直到 StopIteration
↓
统一排序
↓
返回新的 list
```

可以粗略理解为：

```python
temp = []

for item in generator:
    temp.append(item)

temp.sort(...)
return temp
```

真实 CPython 实现并不是这段 Python 代码，但思维模型足够准确。

## 5.2 为什么最终是 list

因为 Python 内置：

```python
sorted(iterable)
```

的 API 约定就是返回一个新的 list。

所以：

```python
sorted(tuple)
sorted(set)
sorted(generator)
```

最后都会得到 list。

这与 generator 之前是否来自 list 没有关系。

类型变化：

```text
generate_search_results()
↓
Generator / Iterator[SearchResult]
↓
sorted() 主动消费
↓
list[SearchResult]
```

## 5.3 `sorted()` 会把 generator 消费完

```python
generator = generate_search_results(...)

search_results = sorted(generator)

for result in generator:
    print(result)
```

最后一个 `for` 不会输出内容。

原因：

```text
generator 已经被 sorted 消费完
```

Generator / iterator 通常是一次性向前消费的。

---

# 6. Lazy Evaluation（惰性计算）

Generator 的惰性不是因为“它叫 iterator”，而是因为：

> 不需要时不计算，需要下一个值时才继续计算。

例如：

```python
g = generate_search_results(...)
```

此时可能还没有真正完成任何检索计算。

直到：

```python
next(g)
```

或：

```python
sorted(g)
```

才开始逐步执行。

可以记：

```text
lazy
=
don't compute until needed
=
需要时才计算
```

当前项目中 generator 不是为了性能优化。当前数据只有几条，而且最终 `sorted(generator)` 仍然需要拿到全部搜索结果后才能排序。

更典型的场景包括：

```text
大文件逐行处理
数据库流式结果
LLM streaming
日志流
批处理
FastAPI StreamingResponse
LangChain / LangGraph stream
```

---

# 7. 今日踩坑：`# type:` 不是普通注释

曾写：

```python
# type:generator
```

VS Code / Pylance 提示语法异常。

原因：

```python
# type:
```

可能被工具识别为 Python 的 type comment，而不是普通注释。

旧式示例：

```python
x = 10  # type: int
```

现代 Python 更推荐：

```python
x: int = 10
```

如果只是学习笔记，建议写：

```python
# generator object
```

或：

```python
# generator 对象，逐个产生 SearchResult
```

---

# 8. Decorator：函数也是对象

```python
def hello():
    print("hello")
```

不带括号：

```python
x = hello
```

表示把函数对象赋给 `x`。

然后：

```python
x()
```

同样可以调用。

区别：

```text
hello
→ 函数对象本身

hello()
→ 调用函数，并取得返回结果
```

---

# 9. 函数可以作为参数和返回值

函数作为参数：

```python
def execute(func):
    func()
```

调用：

```python
execute(hello)
```

传递的是函数对象。

函数也可以返回函数：

```python
def outer():
    def inner():
        print("inner")

    return inner
```

调用：

```python
x = outer()
x()
```

Decorator 建立在：

```text
函数可以作为参数
函数可以作为返回值
```

这两个基础之上。

---

# 10. 最小 Decorator

```python
def decorator(func):
    def wrapper():
        print("before")
        func()
        print("after")

    return wrapper
```

然后：

```python
@decorator
def hello():
    print("hello")
```

基本等价于：

```python
def hello():
    print("hello")

hello = decorator(hello)
```

因此：

```text
@decorator
def f():
```

可以先翻译成：

```python
f = decorator(f)
```

---

# 11. 为什么 `return wrapper` 而不是 `return wrapper()`

正确：

```python
return wrapper
```

返回的是：

```text
wrapper 函数对象
```

这样以后调用原函数名时才真正执行 wrapper。

如果写：

```python
return wrapper()
```

意思是：

```text
现在立刻执行 wrapper
↓
把 wrapper 的执行结果返回
```

因此：

```text
return wrapper
→ 返回包装后的函数

return wrapper()
→ 立即执行包装函数
```

---

# 12. `*args` / `**kwargs`

最初：

```python
def wrapper():
```

只能包装没有参数的函数。

如果原函数：

```python
def add(a, b):
    return a + b
```

装饰后调用：

```python
add(1, 2)
```

实际上会调用：

```python
wrapper(1, 2)
```

因此 wrapper 需要接收并转发参数。

## 12.1 `*args`

```python
def f(*args):
    print(args)
```

调用：

```python
f(1, 2, 3)
```

得到：

```python
(1, 2, 3)
```

因此：

```text
*args
→ 收集位置参数
→ tuple
```

调用时：

```python
func(*args)
```

又会把 tuple 拆开。

## 12.2 `**kwargs`

```python
def f(**kwargs):
    print(kwargs)
```

调用：

```python
f(name="Alice", age=20)
```

得到：

```python
{
    "name": "Alice",
    "age": 20
}
```

因此：

```text
**kwargs
→ 收集关键字参数
→ dict
```

调用：

```python
func(**kwargs)
```

又会把 dict 解包成关键字参数。

这与：

```python
Document(**raw_doc)
```

属于同一种函数调用解包机制。

---

# 13. 通用 Decorator 模板

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper
```

为什么需要：

```python
return result
```

因为原函数可能有返回值。

如果 wrapper 不把结果继续 return 出去，装饰后的函数可能从原本有返回值变成返回 `None`。

---

# 14. 今日项目产出：`@timer`

新增：

```text
src/utils.py
```

示例：

```python
import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(
            f"{func.__name__} took "
            f"{end - start:.6f}s"
        )

        return result

    return wrapper
```

接入：

```python
@timer
def load_documents(...):
    ...
```

以及：

```python
@timer
def retrieve_documents(...):
    ...
```

业务函数内部无需重复加入计时代码，却拥有统一的计时能力。

---

# 15. 为什么使用 Decorator

Decorator 的价值是：

> 把重复出现在很多函数周围的外围逻辑抽离出来。

典型横切逻辑：

```text
日志
计时
缓存
重试
权限检查
事务
监控
trace
```

以后 FastAPI 中：

```python
@app.get("/documents")
def get_documents():
    ...
```

`@app.get(...)` 就是 decorator。

Agent 开发里也常见：

```python
@tool
def search_database(query: str):
    ...
```

因此当前手写 decorator 的意义主要是：

```text
以后看到 @xxx
不再把它当黑魔法
```

---

# 16. Closure（闭包）

Decorator 中：

```python
def timer(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

执行：

```python
add = timer(add)
```

以后 `timer()` 已经执行结束。

但 wrapper 仍然能够访问：

```python
func
```

也就是原始 `add`。

这就是这里的 closure 核心现象：

> 内层函数使用了外层函数的变量，并且外层函数结束后，内层函数仍然能够继续访问这个变量。

---

# 17. `__name__` 与 `functools.wraps`

函数对象有：

```python
func.__name__
```

例如：

```python
def add(a, b):
    return a + b

print(add.__name__)
```

输出：

```text
add
```

但是：

```python
@timer
def add(...):
    ...
```

本质上：

```python
add = timer(add)
```

而 `timer()` 返回的是 wrapper。

因此如果不处理：

```python
add.__name__
```

可能变成：

```text
wrapper
```

标准写法：

```python
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

`@wraps(func)` 会尽可能保留原函数的重要元信息，例如：

```text
__name__
__doc__
__annotations__
```

---

# 18. Context Manager

之前已经使用：

```python
with open(
    file_path,
    "r",
    encoding="utf-8"
) as file:
    documents = json.load(file)
```

Context Manager 的核心：

```text
__enter__()
__exit__()
```

---

# 19. 不使用 `with` 的资源管理

```python
file = open(...)

documents = json.load(file)

file.close()
```

如果中间 `json.load(file)` 发生异常，后面的 `file.close()` 可能无法执行。

可以使用：

```python
file = open(...)

try:
    ...
finally:
    file.close()
```

保证清理。

Context Manager 就是把这种“进入 / 退出生命周期管理”抽象成统一机制。

---

# 20. `__enter__()` / `__exit__()`

```python
class DemoContext:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        print("exit")
```

使用：

```python
with DemoContext() as ctx:
    print("working")
```

执行顺序：

```text
__enter__()
↓
with 内部代码
↓
__exit__()
```

---

# 21. `as ctx` 到底是什么

```python
with DemoContext() as ctx:
    ...
```

其中 `ctx` 就是：

```python
__enter__()
```

的返回值。

如果：

```python
def __enter__(self):
    return self
```

那么 `ctx` 就是 `DemoContext` 对象本身。

但 `__enter__()` 不一定必须 return self。

例如：

```python
def __enter__(self):
    return "hello"
```

那么：

```python
with DemoContext() as ctx:
    print(ctx)
```

会打印：

```text
hello
```

所以：

```text
as xxx
=
接住 __enter__() 的返回值
```

如果不需要这个返回值，可以不写 `as`。

---

# 22. `__exit__()` 的三个异常参数

```python
def __exit__(
    self,
    exc_type,
    exc_value,
    traceback
):
```

如果 with 内部正常结束：

```text
exc_type = None
exc_value = None
traceback = None
```

如果：

```python
with DemoContext():
    1 / 0
```

则大致会收到：

```text
exc_type
→ ZeroDivisionError

exc_value
→ division by zero

traceback
→ traceback 对象
```

这些是 Python 传给 `__exit__()` 的输入参数，不是 `__exit__()` 的返回值。

---

# 23. `__exit__()` 返回 True / False / None

如果没有显式 return：

```python
def __exit__(...):
    print("exit")
```

Python 默认：

```python
return None
```

## 23.1 返回 `False` / `None`

表示：

```text
如果 with 内发生异常
→ 不抑制异常
→ 异常继续向外传播
```

## 23.2 返回 `True`

表示：

```text
context manager 表示异常已经被处理
→ 抑制异常
→ 不继续向外传播
```

例如：

```python
with DemoContext():
    print("A")
    1 / 0
    print("B")

print("C")
```

如果 `__exit__()`：

```python
return True
```

输出中不会有 `B`，但可以继续输出 `C`。

原因：

```text
1 / 0 发生异常
↓
with 内部剩余代码立刻终止
↓
调用 __exit__()
↓
__exit__ 返回 True
↓
异常不继续向外传播
↓
执行 with 后面的代码
```

因此：

```text
return True
不是“with 内部继续运行”
而是“异常不再向外传播”
```

---

# 24. Context Manager 与 C++ RAII

可以粗略建立联系：

C++ RAII：

```text
构造 / 获取资源
↓
使用
↓
析构 / 释放资源
```

Python Context Manager：

```text
__enter__()
↓
使用资源
↓
__exit__()
```

机制并不完全相同，但解决的问题很相似：

> 让资源的获取与释放形成明确、可靠的生命周期边界。

---

# 25. Day 05 今日项目变化

项目主链路进一步演进为：

```text
documents.json
↓
data_loader
↓
Document
↓
generate_search_results()
↓
yield SearchResult
↓
generator
↓
sorted()
↓
list[SearchResult]
↓
main
```

新增通用工具：

```text
src/
├── main.py
├── models.py
├── data_loader.py
├── retriever.py
└── utils.py
```

其中：

```text
utils.py
→ timer decorator
```

---

# 26. Day 05 问答检查

## Q1：为什么 list 是 iterable，但不是 iterator？

因为 list 保存元素，并能够通过 `iter(list)` 创建 iterator，但 list 本身不负责记录当前迭代状态，也不能直接使用 `next(list)`。

## Q2：`iter()` 做了什么？

从一个 iterable 中获得 iterator。

## Q3：`next()` 做了什么？

让 iterator 产生下一个元素，并更新内部遍历状态。没有元素时抛出 `StopIteration`。

## Q4：`yield` 和 `return` 有什么区别？

`return` 返回后函数结束；`yield` 产生一个值后暂停函数、保存状态，下次继续。

## Q5：为什么 generator 叫惰性？

因为 generator function 被调用时通常不会立刻执行所有计算，而是在调用者真正需要下一个元素时才继续执行。

## Q6：为什么 `sorted()` 可以接 generator？

因为 `sorted()` 接收 iterable。Generator 是 iterable / iterator，因此可以被主动消费。

## Q7：为什么 `sorted(generator)` 最后返回 list？

因为 `sorted()` 的 API 设计就是接收 iterable、消费元素、排序并返回新的 list。

## Q8：为什么 decorator 能接收函数？

因为 Python 中函数也是对象，可以作为参数传递。

## Q9：为什么 wrapper 使用 `*args / **kwargs`？

为了让 wrapper 能够接收并转发原函数的任意位置参数和关键字参数。

## Q10：为什么 wrapper 要 `return result`？

为了保留原函数的返回值语义。

## Q11：为什么 decorator `return wrapper`，不是 `return wrapper()`？

因为 decorator 需要返回包装后的函数对象；`wrapper()` 表示立刻执行 wrapper。

## Q12：`@timer` 基本等价于什么？

```python
@timer
def func():
    ...
```

基本等价于：

```python
def func():
    ...

func = timer(func)
```

## Q13：Closure 在 timer 中体现在哪里？

`wrapper` 使用了外层 `timer` 的局部变量 `func`，并且在 `timer()` 结束后仍然能够访问它。

## Q14：`@wraps(func)` 解决什么问题？

让 wrapper 尽可能保留原函数的 `__name__`、`__doc__`、`__annotations__` 等元信息。

## Q15：`with ... as ctx` 中 ctx 是什么？

`ctx` 是 `__enter__()` 的返回值。

## Q16：`__exit__()` 的异常参数来自哪里？

由 Python 在退出 with 块时传入；正常时一般是 None，异常时包含异常类型、异常实例和 traceback。

## Q17：`__exit__()` 返回 True 有什么效果？

with 内异常处之后的语句仍然不执行，但异常不会继续向外传播，因此 with 后面的外部代码可以继续执行。

---

# 27. 今日最重要的坑

```text
1. list 是 iterable，不是 iterator。

2. iterator 会记录遍历状态，消费后不能自动重新开始。

3. generator function 调用时得到 generator object，
   不是函数执行完以后 return 一个 Iterator。

4. yield 不是 append 的附加语法。
   append = 自己收集结果
   yield = 一个一个向外产生结果

5. sorted(generator) 是 sorted 主动消费 generator，
   不是 generator 先自己执行完再交给 sorted。

6. sorted() 最终返回 list，
   是 sorted 自身的 API 行为。

7. `# type:` 可能被类型检查器当成特殊 type comment。

8. `return wrapper` 返回函数对象；
   `return wrapper()` 是立即执行函数。

9. `@timer` 本质上可以理解为：
   func = timer(func)

10. wrapper 能在 timer 结束后继续访问 func，
    是 closure 的体现。

11. `@wraps(func)` 用于保留原函数元信息。

12. `as ctx` 接收的是 `__enter__()` 的返回值。

13. `__exit__()` 的异常信息是输入参数，不是返回值。

14. `__exit__()` 返回 True：
    with 内异常处之后的代码仍然不会执行，
    但异常不会继续传播到 with 外部。

15. `__exit__()` 返回 False / None：
    异常继续向外传播。
```

---

# 28. 实验文件整理建议

目前单个 `playground.py` 已经混入很多不同知识点，继续全部堆在一个文件里不利于回顾。

从现在开始建议：

```text
playground/
├── day-05.py
├── day-06.py
├── day-07.py
└── ...
```

每天形成三类内容：

```text
src/
→ 正式项目代码

playground/day-XX.py
→ 当天可以随意修改、测试、制造异常的概念实验

learning/day-XX.md
→ 当天知识、踩坑、问答与总结
```

一天内部实验较多时，不必再拆成大量小文件，在当天文件内分区即可：

```python
# ====================
# 1. Iterator
# ====================

...

# ====================
# 2. Generator
# ====================

...

# ====================
# 3. Decorator
# ====================

...

# ====================
# 4. Context Manager
# ====================

...
```

这样既能归类，也不会产生过多零碎文件。

如果当前 `playground.py` 已经比较乱，不必花大量时间重构旧实验。可以把它保留为历史草稿，从 Day 05 或 Day 06 开始按天整理。

---

# 29. Day 05 完成状态

```text
Iterable / Iterator        ✅
iter() / next()            ✅
StopIteration              ✅
Generator                  ✅
yield                      ✅
Lazy Evaluation            ✅
sorted(generator)          ✅

函数对象                   ✅
Decorator                  ✅
*args / **kwargs           ✅
Closure 初步               ✅
functools.wraps            ✅
@timer 项目接入            ✅

Context Manager            ✅
__enter__ / __exit__       ✅
with ... as ...            ✅
异常传播 / 抑制            ✅
```

Day 05 完成。
