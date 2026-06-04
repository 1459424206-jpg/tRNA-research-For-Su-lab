param(
    [string]$RepoUrl = "https://github.com/1459424206-jpg/tRNA-research-For-Su-lab.git",
    [string]$Branch = "main",
    [string]$CommitMessage = "Organize tRNA research materials"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git was not found in PATH. Install Git for Windows, reopen PowerShell, then rerun this script."
}

if (-not (Test-Path -LiteralPath ".git")) {
    git init
}

git branch -M $Branch

$remote = git remote 2>$null
if ($remote -contains "origin") {
    git remote set-url origin $RepoUrl
} else {
    git remote add origin $RepoUrl
}

git add .
git status --short

git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "No staged changes to commit."
} else {
    git commit -m $CommitMessage
}

git push -u origin $Branch
