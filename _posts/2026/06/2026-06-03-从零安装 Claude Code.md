---
title: "从零安装 Claude Code"
date: "2026-06-03"
categories:
  - "AI"
---


# 从零安装 Claude Code

#### 1. 安装 Claude Code

- 安装 [Node.js](https://nodejs.org/zh-cn/download/) 18+。
- Windows 用户需安装 [Git for Windows](https://git-scm.com/download/win)。
- 在命令行界面，执行以下命令安装 Claude Code：

```bash
npm install -g @anthropic-ai/claude-code
```

- 安装结束后，执行以下命令，若显示版本号则安装成功：

```bash
claude --version
```





## Windows 的一键配置脚本（PowerShell）

Windows 的一键配置脚本（PowerShell）：

```powershell
# 替换为你的 MiniMax API Key
$apiKey = "你的_MINIMAX_API_KEY"

# 创建目录
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude" | Out-Null

# 写入 settings.json
@"
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "$apiKey",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3"
  }
}
"@ | Set-Content "$env:USERPROFILE\.claude\settings.json" -Encoding UTF8

# 写入 .claude.json
@"
{
  "hasCompletedOnboarding": true
}
"@ | Set-Content "$env:USERPROFILE\.claude.json" -Encoding UTF8

Write-Host "配置完成！" -ForegroundColor Green
```

**使用方法：**

1. 把 `你的_MINIMAX_API_KEY` 替换为真实 Key
2. 右键 → 用 PowerShell 运行，或在终端粘贴执行

如果提示权限不够，先运行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```



---



## Linux/macOS 一键配置脚本

Linux/macOS 一键配置脚本：

```bash
#!/bin/bash
# 替换为你的 MiniMax API Key
API_KEY="你的_MINIMAX_API_KEY"

mkdir -p ~/.claude

cat > ~/.claude/settings.json << EOF
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "$API_KEY",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3"
  }
}
EOF

cat > ~/.claude.json << EOF
{
  "hasCompletedOnboarding": true
}
EOF

echo "配置完成！"
```

**使用方法：**

1. 把 `你的_MINIMAX_API_KEY` 替换为真实 Key
2. 运行：

```bash
bash setup.sh
```

或者不保存文件，直接改好 Key 后整段粘贴进终端执行即可。



---



## 问题

> Q："hasCompletedOnboarding": true 这是干啥

> A：跳过 Claude Code 首次启动的新手引导页面（就是那个让你点"下一步"的欢迎流程）。
>
> 设置成 `true` 后直接进入正常使用，省去每次配置都要手动点完引导的麻烦。



---



## 测试



``` bash
PS D:\base-temlate\xframe> claude
╭─── Claude Code v2.1.161 ───────────────────────────────────────────────────────────────────────────────╮
│                                    │ Tips for getting started                                          │
│            Welcome back!           │ Run /init to create a CLAUDE.md file with instructions for Claude │
│                                    │ ───────────────────────────────────────────────────────────────── │
│               ▐▛███▜▌             │ What's new                                                        │
╭─── Claude Code v2.1.161 ───────────────────────────────────────────────────────────────────────────────╮
│                                    │ Tips for getting started                                          │
│            Welcome back!           │ Run /init to create a CLAUDE.md file with instructions for Claude │
│                                    │ ───────────────────────────────────────────────────────────────── │
│               ▐▛███▜▌             │ What's new                                                        │
│              ▝▜█████▛▘           │ Check the Claude Code changelog for updates                       │
│                ▘▘ ▝▝             │                                                                   │
│                                    │                                                                   │
│   MiniMax-M3 · API Usage Billing   │                                                                   │
│       D:\base-temlate\xframe       │                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯

   Opus 4.8 is now available! · /model to switch

❯ 你用的是什么模型？                                                                                                                                         

  Thought for 4s (ctrl+o to expand)

● 我使用的是 MiniMax-M3 模型,由 MiniMax 开发。MiniMax 是一家成立于 2022 年初的全球 AI 基础模型公司,致力于推动人工智能向通用人工智能(AGI)的前沿发展。
   
  我的知识截止日期是 2026 年 1 月。

  有什么我可以帮你的吗?

✻ Churned for 6s

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────❯  
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ? for shortcuts · ← for agents

```

