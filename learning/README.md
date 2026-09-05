# Learning Log

记录 Agent 开发学习过程中每天掌握的知识点、项目演进和问题解决过程。

## 学习目录

| Day | 主题 | 核心知识点 | 项目进度 | 状态 |
|---|---|---|---|---|
| [Day 0](./day-00.md) | Git 与项目初始化 | Git 基本流程、仓库结构、分支、remote、push | 创建学习仓库并完成第一次提交 | ✅ |
| [Day 1](./day-01.md) | Python 容器与简单文档检索 | list、dict、set、tuple、sorted、lambda、mutable/reference、dict 展开 | 实现关键词文档检索 V0.1 | ✅ |

## 每天的知识点

### Day 0

- Git 工作区、暂存区、本地仓库、远程仓库之间的关系
- `git status`
- `git add .`
- `git commit -m "..."`
- `git push`
- `git push -u origin main`
- `git remote -v`
- `git ls-remote origin`
- `master` 与 `main`
- `.gitignore`
- 项目目录整理
- GitHub 连接失败时区分 Git 配置问题与网络问题

### Day 1

- `list`
- `dict`
- `set`
- `tuple`
- `for` / `if` / `in`
- `append()`
- `dict["key"]` 与 `dict.get()`
- `sorted(..., key=..., reverse=True)`
- `lambda`
- list 负索引 `[-1]`
- mutable / immutable
- Python 名字绑定与引用
- 遍历 list 时不要同时删除元素
- `dict.copy()`
- `**doc` 构造新 dict
- 保留原始输入、生成新的结果集合

## 项目演进

```text
Day 0
项目初始化
    ↓
Day 1
内存文档
→ 关键词匹配
→ score
→ 过滤
→ 排序
→ 输出结果
```

以后每天完成学习后：

1. 新增 `day-XX.md`
2. 在本文件学习目录中增加一行
3. 补充当天核心知识点
4. 提交代码与学习记录
