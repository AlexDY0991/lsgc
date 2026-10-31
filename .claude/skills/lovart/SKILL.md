---
name: lovart
description: 用 Lovart（lovart.ai 设计 Agent）做海报、主视觉、KV、社媒图、包装和品牌设计稿，也能出视频和音频。用 Lovart 生成或修改设计之前先读。
---

# Lovart

调用的是官方客户端 `lovartai/lovart-skill`（MIT，只用 Python 标准库）。它把需求发给 Lovart 托管的设计 Agent，由 Agent 选模型并在 Lovart 画布上出图。

## 准备
1. `bash tools/setup.sh` 会把客户端克隆到 `/tmp/studio-tools/lovart-skill`，并显示密钥有没有设置好。
2. **第一次使用前，读一遍 `/tmp/studio-tools/lovart-skill/skills/lovart-skill/SKILL.md`**（官方规则），以它为准。
3. 密钥：需要环境变量 `LOVART_ACCESS_KEY` 和 `LOVART_SECRET_KEY`。
   - 在 Lovart 网页的头像菜单 →「AK/SK Management」里获取；
   - **由用户加到云端环境设置里**（新会话才会生效）。**绝不能让用户把密钥贴到聊天里**；
   - 默认接口是 `https://lgw.lovart.ai`。不要设置 `LOVART_INSECURE_SSL`。

## 用法
```bash
L="python3 /tmp/studio-tools/lovart-skill/skills/lovart-skill/scripts/agent_skill.py"
$L chat --prompt "…设计需求…" --json --download       # 发需求、等结果、下载
$L upload 文件.png                                     # 上传参考图（logo、产品图），返回 CDN 地址
$L projects / threads / status / result / download   # 项目、对话、状态、结果、下载
$L query-mode / set-mode                             # 查看 / 切换模式（fast 模式消耗积分）
```
- 下载的文件默认放在 `/tmp/lovart`，交付前复制到项目目录。状态记录在 `~/.lovart/state.json`。
- **`projects`、`threads`、`config` 只读本机的 `~/.lovart/state.json`，不连 Lovart 服务器**（2026-10-31 读源码确认）。新容器里它们是空的，**查不到用户账号里已有的项目和素材**。`threads` 也没有 `--all` 参数。客户端没有列出远程项目、画布内容或素材库的命令。
  - 要用账号里已有的项目：请用户给画布链接（`https://www.lovart.ai/canvas?projectId=…`，projectId 不是密钥），用 `project-add --project-id … --name …` 登记（会远程校验并取项目名）。
  - 要看、要确认已有素材（例如 IP 形象）：请用户从 Lovart 下载原图传给我们，放进 `brand/`，逐个确认后登记 ASSETS.md；生成时用 `upload` 传回作参考。用户素材库里的图也可以用 `--subjects` 引用（要素材库 URL，可沿用已有审核）。
  - 项目里设了品牌套件（brand kit）会自动带上；引用别的套件用 `--kits`。
  - 新容器里 `~/.lovart/state.json` 不在了；项目 ID 和对话 ID 要记在 ASSETS.md 第 6 节，开工时用 `project-add` 恢复。
- **官方规则：** 只用客户端的命令，不直接调接口；遇到需要确认的高消耗步骤（`confirm`）要先问用户，不能自动确认。第一次 `chat` 之前先跑 `config --json` 和 `threads --json`，相关话题沿用已有的对话（`--thread-id`）。
- 结果里的 `failures` 数组即使有图返回也要检查。

## 适合用来做什么
- 海报、主视觉（KV）、活动物料、社媒图、包装、品牌延展稿。这类设计稿 Lovart 的版式能力比单纯做图强。
- 写需求时要写清楚：品牌（附 BRAND.md 的要点和 logo）、用途和尺寸、文案（按 BRAND.md 的语言规定，不自己编 slogan）、风格参考、必须避免的东西。
- 出稿后先自查：文字有没有错字、logo 有没有变形、品牌色对不对，然后再交给用户确认。
