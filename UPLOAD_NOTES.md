# Upload notes

目标仓库：<https://github.com/1459424206-jpg/tRNA-research-For-Su-lab>

## 当前整理状态

- 已加入 `.gitignore`，排除本地虚拟环境、`node_modules`、缓存、Office 临时文件和本地环境变量。
- 已加入根目录 `README.md`，说明主要目录和上传范围。
- 计划保留研究文献、流程说明、脚本、报告、PPT、图片和已整理材料。

## 当前阻塞

本机 PowerShell 当前找不到 `git` 或 `gh` 命令，也没有检测到可用的 GitHub token。GitHub 连接器已确认当前账号对目标仓库有 push/admin 权限，但连接器的文件级 API 不适合批量上传约 901 MB、1,851 个本地文件。因此还不能直接从这里完成整仓库远程推送。

## 安装并登录后可执行的命令

在安装 Git for Windows 并完成 GitHub 认证后，可在本目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\push_to_github.ps1
```

或手动执行：

```powershell
git init
git branch -M main
git remote add origin https://github.com/1459424206-jpg/tRNA-research-For-Su-lab.git
git add .
git status --short
git commit -m "Organize tRNA research materials"
git push -u origin main
```

如果远程仓库已经有提交，需要先执行：

```powershell
git pull --rebase origin main
git push -u origin main
```
