# Agent 开发工程师 7 周加速学习计划（每天 4 小时）

> 适用背景：已有一定 Python 基础和 C++ 项目基础，希望尽快补齐 Python 工程化、Python Web 后端、LangChain、LangGraph，并最终具备独立实现 Agent 后端项目的能力。  
> 计划强度：**49 天 × 4 小时/天 ≈ 196 小时**。  
> 核心原则：**不追求把课程刷完，而追求每个阶段都有可运行代码和项目产出。**

---

## 0. 总体路线

```text
Python 查漏补缺
    ↓
Python 工程化
    ↓
HTTP / REST / 数据库基础
    ↓
FastAPI（主学） + Django（了解）
    ↓
LangChain 核心能力
    ↓
LangGraph 状态化 Agent
    ↓
FastAPI + LangGraph + RAG + Checkpoint + Trace 综合项目
```

### 时间分配

| 阶段 | 天数 | 约用时 | 优先级 |
|---|---:|---:|---|
| Python 复习 | 7 天 | 28h | 高 |
| Python 工程化 | 7 天 | 28h | 高 |
| FastAPI + 后端基础 | 10 天 | 40h | 极高 |
| Django | 3 天 | 12h | 低/次要 |
| 后端阶段整合 | 1 天 | 4h | 高 |
| LangChain | 7 天 | 28h | 极高 |
| LangGraph | 10 天 | 40h | 极高 |
| 综合 Agent 项目 | 4 天 | 16h | 极高 |
| **合计** | **49 天** | **196h** | |

> 对 Agent 求职而言，建议时间权重约为：  
> **FastAPI 80% : Django 20%**。  
> Django 的目标是“看得懂、知道体系”，不是现阶段深入成为 Django 后端工程师。

---

# 1. 每天 4 小时应该怎么分配

建议固定成一个模板，减少每天重新规划的成本：

| 时间 | 内容 |
|---|---|
| 60 min | 学当天 3～5 个核心知识点 |
| 90 min | 跟课程 / 官方文档敲代码 |
| 60 min | 脱离教程自己实现一遍 |
| 30 min | 总结 + 问答回忆 + Git Commit |

每天新增知识点控制在 **3～5 个**。  
如果一天接触 10～20 个新概念，大概率只是“看过”，而不是掌握。

每天结束前必须回答：

- [ ] 今天最重要的 3 个概念是什么？
- [ ] 不看教程能不能写出核心代码？
- [ ] 今天代码是否提交到 Git？
- [ ] 有没有一个可运行结果？
- [ ] 哪个知识点明天需要再复习 15 分钟？

---

# 2. 各阶段：最重要与次重要知识点

## 阶段 A：Python 复习

### P0：最重要

1. 函数、参数、作用域、闭包
2. `list / dict / set / tuple` 与推导式
3. 面向对象：class、继承、组合、`__init__`
4. 异常处理：`try / except / finally / raise`
5. 模块、包、import
6. 类型注解 `typing`
7. `async / await`
8. 文件、JSON、`pathlib`

### P1：次重要

1. decorator
2. iterator / generator
3. context manager
4. `lambda / map / filter`
5. threading / multiprocessing 基础区别
6. Python 魔术方法

### 当前不用深挖

- 元类 metaclass
- 描述符 descriptor
- CPython 源码
- GIL 底层实现细节
- 高级并发优化

---

## 阶段 B：Python 工程化

### P0：最重要

1. 项目目录设计与模块拆分
2. 虚拟环境与依赖管理
3. `pyproject.toml`
4. `uv` / pip 基本工作流
5. `dataclass`
6. Pydantic
7. `.env` 与配置管理
8. logging
9. pytest
10. Git 基础工作流
11. 异常分类与业务错误设计
12. Docker 基础

### P1：次重要

1. Ruff
2. mypy / pyright
3. pre-commit
4. pytest mock
5. CI/CD 基础
6. packaging / build
7. `__init__.py` 与包发布机制

### 这一阶段的目标

你应该从：

```text
main.py
```

一个文件，进化到：

```text
project/
├── pyproject.toml
├── .env.example
├── src/
│   └── app/
│       ├── core/
│       ├── models/
│       ├── services/
│       └── utils/
└── tests/
```

并能解释：

> 为什么代码要这样拆，而不是所有逻辑都塞到一个文件中。

---

## 阶段 C：FastAPI / Python 后端

### P0：最重要

1. HTTP 请求 / 响应
2. REST API
3. GET / POST / PUT / PATCH / DELETE
4. HTTP Status Code
5. FastAPI Router
6. Path / Query / Body 参数
7. Pydantic Request / Response Schema
8. Dependency Injection
9. Service / Repository 分层思想
10. async endpoint
11. SQL 基础
12. SQLAlchemy / SQLModel 基本 CRUD
13. SQLite → PostgreSQL 的基本迁移意识
14. Alembic migration
15. 全局异常处理
16. API 测试
17. 文件上传
18. Docker / Docker Compose

### P1：次重要

1. JWT / OAuth2 基础
2. Middleware
3. CORS
4. BackgroundTasks
5. StreamingResponse
6. SSE / WebSocket
7. Redis
8. Rate Limit
9. Nginx
10. Celery / MQ

### 对 Agent 项目尤其重要

```text
POST /documents
POST /chat
GET  /tasks/{id}
GET  /traces/{trace_id}
```

这种 API 如何设计，以及：

```text
FastAPI
   ↓
Service
   ↓
LangGraph Agent
   ↓
Database / LLM / Retriever
```

如何分层。

---

## 阶段 D：Django

### P0：只要求理解

1. Project / App
2. URL → View
3. Model / ORM
4. Migration
5. Admin
6. Authentication 基本概念
7. Django REST Framework 是什么

### P1：有余力再看

1. Serializer
2. ViewSet
3. Middleware
4. Permissions
5. Celery 集成
6. Django Channels

### 当前目标

能够回答：

> FastAPI 和 Django 有什么区别？为什么 AI / Agent API 服务通常更倾向 FastAPI？

不要求你现阶段用 Django 写一个大型项目。

---

## 阶段 E：LangChain

### P0：最重要

1. Chat Model
2. Message
3. Prompt Template
4. `invoke / stream / ainvoke`
5. Tools
6. Tool Calling
7. Pydantic Structured Output
8. Agent 基础
9. Context / Message History
10. RAG 基本链路
11. Document / Chunk / Metadata
12. Embedding
13. Vector Store
14. Retriever

### P1：次重要

1. Middleware
2. LangSmith
3. Reranker
4. Multi-query
5. Hybrid Retrieval
6. Advanced RAG

### 学完标准

不看教程能实现：

```text
User
 ↓
LLM
 ↓
Tool Calling
 ↓
Tool
 ↓
LLM
 ↓
Structured Answer
```

以及最简单的：

```text
Document
 ↓
Split
 ↓
Embedding
 ↓
Vector Store
 ↓
Retriever
 ↓
LLM
```

---

## 阶段 F：LangGraph

### P0：最重要

1. State
2. Node
3. Edge
4. START / END
5. Reducer
6. Conditional Edge
7. Agent Loop
8. ToolNode
9. Command
10. Checkpointer
11. Thread
12. Persistence
13. Short-term Memory
14. Interrupt / Human-in-the-loop
15. Retry / Error Handling
16. Subgraph

### P1：次重要

1. Streaming
2. Send
3. Long-term Memory / Store
4. Supervisor
5. Handoff
6. Multi-Agent
7. Durable Execution 深入
8. LangGraph Deployment

### 必须搞清楚的概念区别

```text
Node != Agent

多个 Node != Multi-Agent

Checkpoint != 用户长期 Memory

State != 数据库

Workflow Agent != Autonomous Agent
```

---

# 3. 49 天详细时间表

## Week 1：Python 快速复习

### Day 1：核心语法与容器

- [ ] list / tuple / dict / set
- [ ] 切片
- [ ] 推导式
- [ ] mutable vs immutable
- [ ] 常见容器操作复杂度有基本概念

**产出：** 写一个读取 JSON 数据并完成过滤、分组、排序的小程序。

---

### Day 2：函数

- [ ] 参数传递
- [ ] `*args / **kwargs`
- [ ] scope / LEGB
- [ ] closure
- [ ] lambda

**产出：** 写 10 个小函数，不使用全局变量。

---

### Day 3：面向对象

- [ ] class / instance
- [ ] `__init__`
- [ ] instance/class attribute
- [ ] inheritance
- [ ] composition

**产出：**

```text
Question
Evidence
Answer
Citation
```

分别建成 Python 类。

---

### Day 4：函数进阶

- [ ] decorator
- [ ] iterator
- [ ] generator
- [ ] `yield`
- [ ] context manager

**产出：** 写一个统计函数运行时间的 decorator。

---

### Day 5：异常 + 文件

- [ ] try / except / finally
- [ ] raise
- [ ] 自定义 Exception
- [ ] pathlib
- [ ] JSON / text file

**产出：** 一个读取配置文件并带异常处理的小工具。

---

### Day 6：typing

- [ ] 基础 type hints
- [ ] Optional / Union
- [ ] list / dict 泛型
- [ ] Protocol / TypedDict 了解
- [ ] dataclass 初步

**产出：** 给前 5 天代码补完整类型注解。

---

### Day 7：async / await + 周复盘

- [ ] coroutine
- [ ] async / await
- [ ] event loop
- [ ] I/O bound vs CPU bound
- [ ] thread / process / coroutine 区别

**产出：** 并发调用 5 个模拟 API。

**通关标准：**

- [ ] 能解释为什么 LLM API 特别适合异步 I/O
- [ ] 能看懂普通 Agent 项目中的 `async def`
- [ ] 能自己设计一个简单 class

---

# Week 2：Python 工程化

## Day 8：项目结构

- [ ] module / package
- [ ] `__init__.py`
- [ ] absolute / relative import
- [ ] src layout
- [ ] 分层思想

**产出：** 把 Week 1 的零散代码整理成一个项目。

---

## Day 9：环境与依赖管理

- [ ] virtualenv 概念
- [ ] uv
- [ ] pyproject.toml
- [ ] lock file
- [ ] dependency / dev dependency

**产出：**

```bash
uv init
uv add ...
uv run ...
```

完成一个可复现环境。

---

## Day 10：配置管理

- [ ] environment variables
- [ ] `.env`
- [ ] `.env.example`
- [ ] Settings
- [ ] secret 不进 Git

**产出：** 把 LLM API Key 从源码移到环境变量。

---

## Day 11：数据模型

- [ ] dataclass
- [ ] Pydantic BaseModel
- [ ] validation
- [ ] Enum
- [ ] serialization

**产出：**

```python
Question
Evidence
Answer
Citation
```

全部改成清晰的数据模型。

---

## Day 12：异常与日志

- [ ] business error
- [ ] system error
- [ ] logging level
- [ ] structured log 思想
- [ ] request / trace id 概念

**产出：**

```text
Answered
Refused
Failed
```

三类状态和对应异常。

---

## Day 13：测试

- [ ] pytest
- [ ] fixture
- [ ] parametrize
- [ ] mock
- [ ] unit vs integration test

**产出：** 至少写 10 个 pytest test cases。

---

## Day 14：代码质量 + Docker

- [ ] Ruff
- [ ] type checker 基础
- [ ] Git branch / commit
- [ ] Dockerfile
- [ ] `.dockerignore`

**产出：** 把本周项目 Docker 化。

**通关标准：**

```bash
git clone ...
uv sync
pytest
docker build ...
```

都可以正常完成。

---

# Week 3：HTTP + FastAPI 核心

## Day 15：HTTP / REST

- [ ] Request / Response
- [ ] URL / Header / Body
- [ ] HTTP Method
- [ ] Status Code
- [ ] REST

**产出：** 手写一份 Agent API 设计文档。

---

## Day 16：FastAPI 入门

- [ ] FastAPI app
- [ ] Router
- [ ] Path parameter
- [ ] Query parameter
- [ ] Request Body

**产出：**

```text
GET  /health
POST /questions
GET  /questions/{id}
```

---

## Day 17：Pydantic + API Schema

- [ ] Request Model
- [ ] Response Model
- [ ] validation
- [ ] optional fields
- [ ] OpenAPI / Swagger

**产出：** 给 Day 16 所有 API 添加严格 Schema。

---

## Day 18：Dependency Injection

- [ ] Depends
- [ ] dependency
- [ ] router/service 分离
- [ ] service layer
- [ ] repository 概念

**产出：**

```text
router
 ↓
service
 ↓
repository
```

三层小项目。

---

## Day 19：FastAPI async

- [ ] async endpoint
- [ ] sync vs async
- [ ] blocking call
- [ ] async HTTP client
- [ ] timeout

**产出：** FastAPI endpoint 并发调用多个模拟 LLM。

---

## Day 20：SQL 基础

- [ ] table
- [ ] primary key
- [ ] foreign key
- [ ] SELECT / INSERT / UPDATE / DELETE
- [ ] transaction 基本概念

**产出：** SQLite 创建 question / conversation 表。

---

## Day 21：ORM

- [ ] SQLAlchemy / SQLModel
- [ ] model
- [ ] session
- [ ] CRUD
- [ ] relationship 基本概念

**产出：** FastAPI + SQLite CRUD。

---

# Week 4：FastAPI 工程实践 + Django 快速了解

## Day 22：数据库 migration

- [ ] PostgreSQL 基本认识
- [ ] SQLite vs PostgreSQL
- [ ] Alembic
- [ ] migration
- [ ] schema change

**产出：** 新增一个字段并通过 migration 更新数据库。

---

## Day 23：异常处理与 Middleware

- [ ] HTTPException
- [ ] custom exception handler
- [ ] middleware
- [ ] CORS
- [ ] lifespan

**产出：** 统一 API Error Response。

---

## Day 24：Agent 常用 API 能力

- [ ] UploadFile
- [ ] StreamingResponse
- [ ] BackgroundTasks
- [ ] SSE 概念
- [ ] WebSocket 概念

**产出：**

```text
POST /documents
POST /chat
```

支持文件与流式响应中的至少一个。

---

## Day 25：测试 FastAPI

- [ ] TestClient / httpx
- [ ] dependency override
- [ ] API integration test
- [ ] DB test isolation
- [ ] mock external API

**产出：** 10 个 API tests。

---

## Day 26：Docker Compose

- [ ] Docker Compose
- [ ] service
- [ ] volume
- [ ] network
- [ ] FastAPI + PostgreSQL

**产出：**

```bash
docker compose up
```

可以启动 API + DB。

---

## Day 27：Django 核心

- [ ] project / app
- [ ] urls
- [ ] views
- [ ] models
- [ ] ORM

**产出：** Django 最小 CRUD demo。

---

## Day 28：Django + 阶段总结

- [ ] migration
- [ ] admin
- [ ] auth
- [ ] DRF 是什么
- [ ] FastAPI vs Django

**产出：** 写一页对比：

```text
什么时候选 FastAPI？
什么时候选 Django？
Agent 后端为什么优先 FastAPI？
```

> 如果进度落后，Django 可以压缩到 1 天，把时间留给 LangGraph。

---

# Week 5：LangChain

建议配合 `xbsheng/atguigu-note` 的 LangChain 课程，优先顺序：

```text
模型 → Message/Prompt → Tools → Structured Output → Agent → Memory → RAG
```

不要强制按课程 1～10 章完整顺序刷。

---

## Day 29：Model

- [ ] Chat Model
- [ ] invoke
- [ ] stream
- [ ] batch
- [ ] ainvoke

**产出：** 用统一封装调用一个 LLM Provider。

---

## Day 30：Message + Prompt

- [ ] System / Human / AI Message
- [ ] Prompt Template
- [ ] MessagesPlaceholder
- [ ] conversation context
- [ ] token/context 基本概念

**产出：** 多轮聊天 demo。

---

## Day 31：Tools

- [ ] `@tool`
- [ ] tool schema
- [ ] tool description
- [ ] tool calling
- [ ] 多工具选择

**产出：** Calculator + Search 两个 Tools。

---

## Day 32：Structured Output

- [ ] Pydantic schema
- [ ] structured response
- [ ] validation
- [ ] parser failure
- [ ] retry / fallback 思想

**产出：**

```python
class AgentAnswer(BaseModel):
    answer: str
    confidence: float
    evidence_ids: list[str]
```

---

## Day 33：Agent

- [ ] agent loop
- [ ] model
- [ ] tools
- [ ] observation
- [ ] final answer

**产出：** 一个 Tool-Calling Agent。

---

## Day 34：RAG 基础

- [ ] Document Loader
- [ ] Chunk
- [ ] Metadata
- [ ] Embedding
- [ ] Vector Store

**产出：** 本地文档入库。

---

## Day 35：Retriever + RAG QA

- [ ] Retriever
- [ ] Top-K
- [ ] prompt grounding
- [ ] citation / metadata
- [ ] LangSmith 基本了解

**产出：** 一个带来源信息的最小 RAG QA。

**通关标准：**

可以从零写出：

```text
Load
→ Split
→ Embed
→ Store
→ Retrieve
→ Generate
```

---

# Week 6：LangGraph 核心

## Day 36：State / Node / Edge

- [ ] State
- [ ] Node
- [ ] Edge
- [ ] START / END
- [ ] graph compile

**产出：** 三节点 Graph。

---

## Day 37：State 类型与 Reducer

- [ ] TypedDict
- [ ] dataclass
- [ ] Pydantic State
- [ ] Reducer
- [ ] MessagesState

**产出：** 一个带 messages 的 State。

---

## Day 38：Conditional Routing

- [ ] conditional edge
- [ ] router
- [ ] branch
- [ ] loop
- [ ] termination

**产出：**

```text
Question
 ↓
Router
 ├→ Search
 └→ Calculator
```

---

## Day 39：Tool Agent

- [ ] ToolNode
- [ ] tool loop
- [ ] model tool call
- [ ] observation
- [ ] recursion limit

**产出：** 不使用高级封装，手写一个 LangGraph Tool Agent。

---

## Day 40：Command / Control Flow

- [ ] Command
- [ ] goto
- [ ] state update
- [ ] dynamic routing
- [ ] parallel 基础

**产出：** 根据执行结果动态改变路径。

---

## Day 41：Checkpoint

- [ ] checkpointer
- [ ] thread_id
- [ ] checkpoint
- [ ] persistence
- [ ] resume

**产出：** SQLite / 可持久化 Checkpoint demo。

---

## Day 42：Memory

- [ ] short-term memory
- [ ] conversation state
- [ ] checkpoint vs memory
- [ ] long-term memory 概念
- [ ] Store 概念

**产出：** 多轮有状态对话。

---

# Week 7：LangGraph 高级 + 综合项目

## Day 43：Interrupt / HITL

- [ ] interrupt
- [ ] resume
- [ ] human approval
- [ ] state modification
- [ ] sensitive tool approval

**产出：** “执行操作前等待人工确认”的 Agent。

---

## Day 44：Reliability

- [ ] retry
- [ ] timeout
- [ ] business refusal
- [ ] system failure
- [ ] trace / logging

**产出：**

```text
Answered
Refused
Failed
```

状态化 Agent。

---

## Day 45：Subgraph + Multi-Agent 概念

- [ ] subgraph
- [ ] supervisor
- [ ] handoff
- [ ] multi-agent communication
- [ ] workflow vs multi-agent

**产出：** 最小 Supervisor + 2 Worker demo。

> Multi-Agent 此时只做入门，不要成为当前主线。

---

## Day 46：综合项目①——架构

目标项目：

# Evidence-driven Document Agent

```text
FastAPI
  ↓
LangGraph
  ↓
Source Router
  ├─ RAG
  └─ Tool
  ↓
Evidence
  ↓
Answer
  ↓
Citation
```

当天完成：

- [ ] 项目目录
- [ ] State
- [ ] API Schema
- [ ] Graph Node 设计
- [ ] 数据库 Schema

---

## Day 47：综合项目②——核心功能

- [ ] `/documents`
- [ ] `/chat`
- [ ] Retriever
- [ ] Evidence
- [ ] Citation

目标：

```text
问题 → 检索 → Evidence → Answer → Citation
```

跑通。

---

## Day 48：综合项目③——可靠性

- [ ] Checkpoint
- [ ] Refused / Failed
- [ ] Retry
- [ ] Trace ID
- [ ] pytest

目标：故意制造 LLM timeout，能够定位异常。

---

## Day 49：综合项目④——部署与复盘

- [ ] Dockerfile
- [ ] Docker Compose
- [ ] README
- [ ] architecture diagram
- [ ] 面试项目介绍

README 至少包含：

```text
1. 项目背景
2. 系统架构
3. 技术选型
4. Agent 工作流
5. State 设计
6. RAG 设计
7. Checkpoint
8. 错误处理
9. 如何运行
10. 测试结果
```

---

# 4. 推荐 GitHub 仓库：按阶段使用

> 仓库在 2026-09-04 进行了检索/核验。  
> 不建议把所有仓库都从头看一遍，每个阶段只选 1 个主仓库 + 1 个辅助仓库。

---

## A. Python / LangChain / LangGraph 中文主线

### 1. xbsheng/atguigu-note

https://github.com/xbsheng/atguigu-note

**用途：主课程。**

覆盖：

- Python
- LangChain 1.2
- LangGraph
- 配套课件
- Notebook / 代码

推荐使用方式：

```text
Python：查漏补缺
LangChain：作为主要中文教程
LangGraph：作为主要中文教程
```

不要把全部视频刷完。

---

## B. Python 工程化

### 2. astral-sh/uv

https://github.com/astral-sh/uv

**用途：现代 Python 项目与依赖管理。**

重点学习：

```text
uv init
uv add
uv sync
uv run
pyproject.toml
lock file
```

不需要读 uv 源码。

---

### 3. wemake-services/wemake-python-styleguide

https://github.com/wemake-services/wemake-python-styleguide

**用途：理解 Python 工程代码质量和规范。**

重点：

- 命名
- 函数复杂度
- import
- 可维护性
- lint

使用方法：作为“代码审查清单”，不要背所有规则。

---

### 4. cjolowicz/cookiecutter-hypermodern-python

https://github.com/cjolowicz/cookiecutter-hypermodern-python

**用途：观察成熟 Python 项目结构。**

注意：它更适合作为工程结构参考，不作为最新工具版本的唯一依据。

重点看：

```text
项目目录
tests
配置
lint
typing
CI
package
```

---

# C. FastAPI

### 5. zhanymkanov/fastapi-best-practices

https://github.com/zhanymkanov/fastapi-best-practices

**强烈推荐。**

用途：

> 学完 FastAPI 基础后，看“真实项目应该怎么组织”。

重点关注：

- project structure
- router
- dependencies
- async
- database
- validation
- configuration
- testing

这是“FastAPI 会用”到“FastAPI 会工程化”的桥梁。

---

### 6. fastapi/full-stack-fastapi-template

https://github.com/fastapi/full-stack-fastapi-template

**用途：学习完整生产项目结构。**

该模板包含的方向包括：

- FastAPI
- SQLModel
- PostgreSQL
- Docker Compose
- JWT
- pytest
- OpenAPI

你的学习顺序：

```text
先自己写小项目
      ↓
再看这个模板
      ↓
比较自己的目录与它有什么区别
```

不要一开始直接复制模板，否则很多东西会“能跑但不懂”。

---

# D. Django

### 7. cookiecutter/cookiecutter-django

https://github.com/cookiecutter/cookiecutter-django

用途：

> 了解生产级 Django 项目通常包含哪些组件。

只看架构：

```text
settings
apps
models
auth
Docker
Celery
deployment
```

现阶段不要投入大量时间研究其全部代码。

---

# E. LangChain / RAG

### 8. langchain-ai/langchain

https://github.com/langchain-ai/langchain

官方仓库。

用途：

- API 变化时查最新实现
- 看 examples / tests
- 确认教程有没有过时

不建议初学阶段阅读整个源码。

---

### 9. langchain-ai/rag-from-scratch

https://github.com/langchain-ai/rag-from-scratch

**推荐作为 RAG 加速材料。**

适合建立：

```text
Indexing
Retrieval
Generation
```

的底层认知。

建议在 LangChain Week 的 Day 34～35 使用。

---

# F. LangGraph

### 10. langchain-ai/langgraph

https://github.com/langchain-ai/langgraph

官方仓库。

用途：

- State
- persistence
- agent
- multi-agent
- 源码 / tests 查询

学习时：

```text
中文课程学概念
      +
官方 repo / docs 校验 API
```

因为 LangGraph 更新较快，不要只依赖旧博客。

---

# G. Agent 综合教程

### 11. datawhalechina/hello-agents

https://github.com/datawhalechina/hello-agents

**非常适合补 Agent 原理和完整知识体系。**

定位：

> 《从零开始构建智能体》的原理与实践教程。

建议：

- Week 5 开始穿插
- 不作为 Python / FastAPI 教材
- 重点理解 Agent 原理、RAG、Tool、Memory 等概念

---

### 12. adongwanai/AgentGuide

https://github.com/adongwanai/AgentGuide

**更偏求职、进阶 Agent、RAG。**

包含方向：

- LangGraph 实战
- Advanced RAG
- Multi-Agent
- Agent 求职
- 面试内容

建议：

> Week 6 以后再使用。

前期直接看高级 RAG / Multi-Agent，容易知识堆积但项目能力跟不上。

---

# 5. 仓库使用优先级

不要同时开十几个 GitHub 仓库。

建议固定：

## Python 阶段

```text
主：xbsheng/atguigu-note
辅：astral-sh/uv
参考：wemake-python-styleguide
```

## FastAPI 阶段

```text
基础：FastAPI 官方教程
工程：fastapi-best-practices
项目结构：full-stack-fastapi-template
```

## LangChain 阶段

```text
主：xbsheng/atguigu-note
RAG：rag-from-scratch
校验：langchain-ai/langchain
```

## LangGraph 阶段

```text
主：xbsheng/atguigu-note
校验：langchain-ai/langgraph
原理：hello-agents
进阶：AgentGuide
```

---

# 6. 每周必须有的项目产出

| 周 | 必须产出 |
|---|---|
| W1 | Python CLI / async 小程序 |
| W2 | 工程化 Python 项目 + pytest + Docker |
| W3 | FastAPI CRUD API |
| W4 | FastAPI + DB + Docker Compose |
| W5 | Tool Agent + RAG |
| W6 | Stateful LangGraph Agent + Checkpoint |
| W7 | FastAPI + LangGraph + RAG 综合项目 |

如果某一周：

> “视频看完了，但是没有代码产出”

这一周视为 **没有完成**。

---

# 7. 面试导向：必须能回答的问题

## Python

- [ ] list 与 tuple 的区别？
- [ ] generator 有什么意义？
- [ ] decorator 是什么？
- [ ] async / await 为什么适合 LLM API？
- [ ] thread / process / coroutine 区别？
- [ ] Python 异常如何设计？

## 工程化

- [ ] `pyproject.toml` 做什么？
- [ ] 为什么需要虚拟环境？
- [ ] Pydantic 和 dataclass 有什么区别？
- [ ] logging 和 print 有什么区别？
- [ ] unit test / integration test 区别？

## FastAPI

- [ ] FastAPI 为什么性能和异步支持较好？
- [ ] Depends 是什么？
- [ ] Pydantic 在 API 中起什么作用？
- [ ] Router / Service / Repository 怎么分？
- [ ] async endpoint 里为什么不能随便调用阻塞代码？
- [ ] 如何统一异常返回？
- [ ] 如何测试 API？
- [ ] FastAPI 和 Django 如何选择？

## LangChain

- [ ] Message 有哪些类型？
- [ ] Tool Calling 流程是什么？
- [ ] Structured Output 怎么保证格式？
- [ ] RAG 的完整流程？
- [ ] Retriever 和 Vector Store 的区别？
- [ ] Chunk Size 为什么影响 RAG？

## LangGraph

- [ ] State / Node / Edge 分别是什么？
- [ ] Reducer 解决什么问题？
- [ ] Conditional Edge 如何实现？
- [ ] Checkpoint 做什么？
- [ ] Thread 是什么？
- [ ] Checkpoint 和 Memory 有什么区别？
- [ ] Node 和 Agent 有什么区别？
- [ ] Workflow 和 Multi-Agent 有什么区别？
- [ ] Interrupt 解决什么问题？
- [ ] Agent 如何处理中断恢复？

---

# 8. 如果时间进一步变紧，怎么砍

按这个顺序砍：

### 第一批可以压缩

1. Django：3 天 → 1 天
2. Python multiprocessing：只理解
3. Django DRF：只知道是什么
4. LangChain Middleware：只看
5. WebSocket：只理解
6. Multi-Agent：只做最小 demo

### 绝对不要砍

```text
Python async
typing / Pydantic
异常处理
pytest
HTTP
FastAPI
SQL
Docker
Tool Calling
Structured Output
RAG
LangGraph State
Conditional Routing
Checkpoint
Memory 基础
Retry / Error Handling
综合项目
```

---

# 9. 最终目标

49 天结束时，你至少应该独立拥有一个类似：

```text
                       FastAPI
                          ↓
                    LangGraph Agent
                          ↓
            ┌─────────────┴────────────┐
            ↓                          ↓
        RAG Retriever                Tools
            ↓                          ↓
        Evidence                    Result
            └─────────────┬────────────┘
                          ↓
                       Answer
                          ↓
                      Citation
                          ↓
                 Checkpoint / Trace
                          ↓
                 SQLite/PostgreSQL
```

的项目。

API 至少包含：

```text
POST /documents
POST /chat
GET  /sessions/{thread_id}
GET  /traces/{trace_id}
```

项目至少包含：

```text
FastAPI
Pydantic
SQL
LangChain
LangGraph
RAG
Tool Calling
Checkpoint
Logging
pytest
Docker
```

做到这里之后，再进入：

```text
Advanced RAG
Long-term Memory
Multi-Agent
MCP
Agent Evaluation
Observability
```

会更加顺畅。

---

# 10. 学习纪律

最后给这个计划加三个硬约束：

### 规则 1：每天至少 50% 时间写代码

```text
看 2h
写 2h
```

是最低要求。

更推荐：

```text
看 1～1.5h
写 2～2.5h
```

---

### 规则 2：每周必须有 GitHub Commit

目标：

```text
7 周
→ 7 个 milestone
→ 至少 40 次有效 commit
```

不要为了 commit 数量拆无意义提交。

---

### 规则 3：框架 API 不要背

需要掌握的是：

```text
为什么需要 State？
为什么需要 Tool？
为什么需要 Retriever？
为什么需要 Checkpoint？
为什么 Agent Backend 需要 async？
```

API 忘了可以查。

架构思想不知道，才是真正的问题。
