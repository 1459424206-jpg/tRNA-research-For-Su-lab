# 复刻与上传流程

本文记录本仓库从本地研究材料整理到 GitHub 上传的完整流程，方便在另一台电脑上继续维护或复刻同样的上传方式。

目标仓库：

```text
https://github.com/1459424206-jpg/tRNA-research-For-Su-lab
```

## 1. 新电脑准备

### 安装 Git

1. 安装 Git for Windows。
2. 安装后打开 Git Bash。
3. 检查 Git 是否可用：

```bash
git --version
```

### 设置 Git 用户信息

第一次提交前设置用户名和邮箱：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

### 网络与代理

如果 GitHub 访问不稳定，先确保浏览器能打开 GitHub。

本次使用 v2rayN 时，截图中端口为：

- HTTP 代理：`127.0.0.1:10809`
- SOCKS 代理：`127.0.0.1:10808`

Git Bash 中优先使用 HTTP 代理：

```bash
git config --global http.proxy http://127.0.0.1:10809
git config --global https.proxy http://127.0.0.1:10809
git config --global http.sslBackend schannel
git config --global http.version HTTP/1.1
```

测试能否连接 GitHub：

```bash
git ls-remote https://github.com/1459424206-jpg/tRNA-research-For-Su-lab.git main
```

如果 HTTP 代理不通，可改用 SOCKS：

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
git config --global http.proxy socks5h://127.0.0.1:10808
git config --global https.proxy socks5h://127.0.0.1:10808
```

如果需要清除代理配置：

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 2. 在新电脑下载本仓库

选择一个工作目录，例如 `D:/Project`，然后运行：

```bash
cd /d/Project
git clone https://github.com/1459424206-jpg/tRNA-research-For-Su-lab.git
cd tRNA-research-For-Su-lab
```

如果仓库较大，下载需要等待一段时间。

## 3. 从零上传一个本地材料文件夹

如果是在另一台电脑上把新的本地文件夹整理并上传到 GitHub，可参考本节。

进入本地材料目录：

```bash
cd "/d/Project/tRNA research"
```

初始化仓库并绑定远程：

```bash
git init
git branch -M main
git remote add origin https://github.com/1459424206-jpg/tRNA-research-For-Su-lab.git
```

如果提示 `remote origin already exists`，改用：

```bash
git remote set-url origin https://github.com/1459424206-jpg/tRNA-research-For-Su-lab.git
```

建议先配置长路径和换行符：

```bash
git config core.longpaths true
git config core.autocrlf false
```

## 4. 推荐的 `.gitignore`

本仓库不上传本地虚拟环境、依赖目录和临时文件。建议保留以下 `.gitignore`：

```gitignore
.venv/
.venv_paper2ppt/
node_modules/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
~$*
*.tmp
*.temp
*.log
.env
.env.*
.DS_Store
Thumbs.db
```

## 5. 分批上传策略

本仓库包含大量 PPT、PDF、图片和第三方工具快照，一次性 `git add .` 后推送可能生成数百 MB 的 Git pack，容易出现网络中断。

推荐先创建一个分批上传分支：

```bash
git checkout --orphan upload-batches
git rm -r --cached .
```

第一批先上传说明文件和脚本：

```bash
git add .gitignore README.md UPLOAD_NOTES.md scripts
git commit -m "Add repository overview and scripts"
git push -u origin upload-batches:main
```

之后每批成功后再继续下一批。由于本地分支叫 `upload-batches`，远程分支叫 `main`，后续推送建议统一使用：

```bash
git push origin HEAD:main
```

示例分批顺序：

```bash
git add "new study" "tRNA_embryo_sperm_cryo_literature_20260604" "analysis_induro_modification_fingerprints_20260602"
git commit -m "Add focused tRNA literature and fingerprint analyses"
git push origin HEAD:main
```

```bash
git add artifact-build-manifest.json make_trna_embryo_ppt.py *.pptx *.png *.svg *.pdf
git commit -m "Add integrated reports and figures"
git push origin HEAD:main
```

```bash
git add "tRNA analysis tools and algorithms"
git commit -m "Add tRNA analysis tools and algorithms materials"
git push origin HEAD:main
```

```bash
git add "tRNA-related wet-lab experiments"
git commit -m "Add tRNA wet-lab experiment materials"
git push origin HEAD:main
```

```bash
git add output outputs
git commit -m "Add generated outputs"
git push origin HEAD:main
```

```bash
git add "tRNA mod-fingerprint database"
git commit -m "Add tRNA modification fingerprint database materials"
git push origin HEAD:main
```

```bash
git add "biological functions and structural characteristics of tRNA"
git commit -m "Add tRNA biology and structure materials"
git push origin HEAD:main
```

## 6. 常见问题处理

### `nothing added to commit but untracked files present`

原因：还没有执行 `git add`。

处理：

```bash
git add .
git commit -m "Commit message"
```

对于本仓库这种大目录，不推荐直接 `git add .`，建议按第 5 节分批添加。

### `Filename too long`

原因：Windows 路径长度限制。

处理：

```bash
git config core.longpaths true
git add .
```

### `LF will be replaced by CRLF`

这是换行符警告，不是失败原因。科研脚本和配置文件建议尽量保持原样：

```bash
git config core.autocrlf false
```

### `RPC failed; curl 55 Send failure: Connection was reset`

原因：一次推送包太大或网络连接被重置。

处理：

1. 确认 Git 走代理。
2. 避免一次推送所有大文件。
3. 按目录分批提交和推送。

可使用：

```bash
git config --global http.version HTTP/1.1
git config --global http.postBuffer 1048576000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
```

### `Failed to connect to github.com port 443`

原因：Git 无法连接 GitHub。

处理：

1. 先确认浏览器能打开 GitHub。
2. 开启 v2rayN 或其他代理。
3. 按第 1 节配置 Git 代理。
4. 用 `git ls-remote origin main` 测试。

### `The upstream branch of your current branch does not match`

原因：本地分支名是 `upload-batches`，远程分支名是 `main`。

处理：

```bash
git push origin HEAD:main
```

或者设置：

```bash
git config push.default upstream
```

## 7. 日常更新流程

以后只修改少量文件时，按下面流程即可：

```bash
git status --short
git add README.md
git commit -m "Update README"
git push origin HEAD:main
```

如果新增了一个大目录，仍建议单独分批：

```bash
git add "目录名"
git commit -m "Add new research materials"
git push origin HEAD:main
```

## 8. 版权与大文件提醒

仓库是 public 时，要特别注意论文 PDF、网页 HTML、第三方代码仓库快照和示例数据的版权/许可证。若某些材料不适合公开分发，建议只保留引用信息、DOI、下载链接、阅读笔记和索引表。

如果未来出现超过 GitHub 100 MB 的单个文件，不要直接提交到普通 Git 历史中。优先考虑 Git LFS、云盘、数据仓库或只保存文件索引。
