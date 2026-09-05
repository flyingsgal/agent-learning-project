# Day 0 - Git 与项目初始化

## 1. 今日目标

- 创建 Agent 学习仓库
- 建立最小 Python 项目
- 熟悉 Git 最基本的提交与推送流程
- 理解本地项目与 GitHub 远程仓库之间的关系

---

## 2. 知识点学习过程

### 2.1 建立最小项目结构

最终整理为：

```text
agent-learning-project/
├── README.md
├── LEARNING.md
├── .gitignore
└── src/
    └── main.py
```

`src/main.py` 保留最小启动代码：

```python
def main():
    print("Agent learning project started.")

if __name__ == "__main__":
    main()
```

这一阶段重点不是功能，而是先建立一个可以持续演进的项目。

### 2.2 Git 的基本工作流

逐步理解：

```text
工作区
  ↓ git add
暂存区
  ↓ git commit
本地仓库
  ↓ git push
GitHub 远程仓库
```

常用命令：

```bash
git status
git add .
git commit -m "xxx"
git push
```

第一次建立上游关系：

```bash
git push -u origin main
```

之后正常推送：

```bash
git push
```

### 2.3 `git add .`

`git add .` 不只是添加新文件，它会把当前目录范围内的新增、修改、删除、重命名等变化加入暂存区。

### 2.4 commit 与 push

`commit`：在本地创建一个版本记录。

`push`：把本地已有 commit 推送到远程 GitHub。

因此，即使暂时无法连接 GitHub，只要 commit 成功，本地版本仍然已经保存。

### 2.5 `main` 分支

最开始本地分支为 `master`，后来统一改成 `main`。

当前项目规模很小，先直接在 `main` 上学习和提交，不急着引入 branch / merge / rebase / PR。

### 2.6 `.gitignore`

当前主要忽略：

```gitignore
__pycache__/
*.pyc
.venv/
venv/
.env
.idea/
.vscode/
.DS_Store
*.db
*.sqlite
*.sqlite3
```

需要注意：已经被 Git 跟踪的文件，不会因为后来加入 `.gitignore` 就自动停止跟踪。

---

## 3. 遇到的问题并解决

### 问题 1：项目文件一开始都放进了 `src/`

最初 README、LEARNING、`.gitignore` 等文件也在 `src/` 中。

解决：把项目说明和配置文件移动到根目录，只把源码留在 `src/`。

### 问题 2：第一次 push 与后续 push 的区别不清楚

第一次：

```bash
git push -u origin main
```

`-u` 建立本地 `main` 与远程 `origin/main` 的跟踪关系。

之后：

```bash
git push
```

即可。

### 问题 3：push 时出现网络错误

出现：

```text
Recv failure: Connection was reset
Failed to connect to github.com port 443
```

先用：

```bash
git remote -v
```

确认 remote 正确。

再用：

```bash
git ls-remote origin
```

测试是否能访问远程。

当 `git ls-remote origin` 也失败时，可以判断不是 commit、branch 或 push 权限问题，而是当前网络无法连接 GitHub。

网络恢复后重新 `git push` 即可。

---

## 4. 今日项目结果

完成：

```text
创建仓库
→ 建立最小 Python 项目
→ 修正项目目录
→ 建立 main 分支
→ 完成 commit
→ 完成 push
```

---

## 5. 今日需要记住

- `git status`：查看状态
- `git add .`：加入暂存区
- `git commit`：保存本地版本
- `git push`：推送 commit
- `git remote -v`：检查远程地址
- `git ls-remote origin`：测试远程访问
- `.gitignore` 主要作用于未跟踪文件
- 本地 commit 成功后，即使暂时 push 失败，版本也不会丢
