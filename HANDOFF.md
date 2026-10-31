# 交接文档 · 丽尚国潮素材工作室（2026-10-31 建立）

## 下一个窗口（第二个窗口）先做这些
1. 检查 `LOVART_ACCESS_KEY`、`LOVART_SECRET_KEY` 有没有读到。读不到就请用户核对环境设置（变量名、保存后要新开会话），不要让用户把密钥贴进聊天。
2. 读到了：读 Lovart 官方 SKILL.md，用 `projects --json`、`threads --all --json` 看用户 Lovart 账号里有哪些项目。**用户说 Lovart 里有丽尚国潮的 IP 素材**，找到后列给用户看，逐个确认能不能用，再登记进 ASSETS.md。只查看、不生成，不花积分。
3. 即梦登录可能已过期（第一个窗口的登录到 UTC 18:19），要用即梦时按 jimeng-canvas skill 重新登录。
4. 用户会上传品牌信息文档：放进 `brand/`，整理进 BRAND.md 给用户确认（只写文档里有的，不编造）。
5. 问第一批需求和预算，按 skill 流程开始。

## 用户定的工具分工（2026-10-31）
- **做图、海报、设计稿：主要用 Lovart。** 丽尚国潮的 IP 素材在 Lovart 里，Lovart 的工具也更多。
- **做视频：用即梦**（样片模式，先报价再运行）。
- 写实画面需要时也可以用即梦 Seedream，但默认先用 Lovart。

## 新窗口的第一步（通用）
1. 通读 `CLAUDE.md`、`BRAND.md`、`ASSETS.md`，以及 skill：`brand-video`（重点）、`brand-visuals`、`jimeng-canvas`、`lovart`、`higgsfield-timed-prompts`、`higgsfield-motion`。
2. `bash tools/setup.sh`：装工具环境，克隆 Lovart 客户端，检查 Lovart 密钥是否已设置。
3. 即梦：按 `jimeng-canvas` skill 安装 CLI（安装脚本先读再运行），登录，把授权链接用中文发给用户。
4. Lovart：读官方 `SKILL.md`。如果密钥没设置，请用户在云端环境设置里加 `LOVART_ACCESS_KEY` 和 `LOVART_SECRET_KEY`，新会话才会生效。**不要让用户把密钥贴进聊天。**
5. 向用户收集品牌信息，填 BRAND.md（见表格），并请用户上传品牌资料到 `brand/`。
6. 问用户第一批要做什么（海报？视频？），以及预算，然后按对应 skill 的流程开始。

## 目录约定
- `brand/`：品牌资料（logo、VI、产品图、参考）
- `projects/<日期-项目名>/`：每个项目一个目录，含 brief、prompts、状态文件、交付物
- `tools/`：脚本工具
- `docs/`：方法笔记。`higgsfield-realism-workflow-notes.md` 必读；`coolfly-case-study.md` 是上一个项目的完整规则，作参考

## 来源
skill 和工具从 CoolFly 品牌片项目（仓库 alexdy0991/productvideo）迁移过来，已通用化。CoolFly 项目的经验教训都写进了 brand-video skill 的第六节。

## 当前进度
- 仓库初始化完成，还没开始任何项目。
- 2026-10-31 第一个窗口：
  - `tools/setup.sh` 已跑通（修了一处：Playwright 的 Chromium 目录改名为 `chrome-linux64`，原通配符匹配不到导致脚本中途退出）。
  - 即梦 CLI 1.2.1 已安装（安装脚本先读后运行，用户批准），已登录。账号 VIP，可用约 29,807 积分（分批在 11 月 22–27 日过期）。模型列表里有 `seedream_5.0_pro`、`seedance_2.5_draft`，和 skill 一致。
  - **注意：这次登录约 6 小时就过期（不是一天）。** 过期后按 jimeng-canvas skill 重新登录；必须用 `auth wait --device-code`，不能用 `auth status` 轮询代替。
  - Lovart 密钥未设置，已请用户在环境设置里加 `LOVART_ACCESS_KEY`、`LOVART_SECRET_KEY`（新会话生效）。**新会话第一件事：检查这两个变量。**
  - 已建 `brand/` 目录，等用户上传品牌资料、提供品牌信息（BRAND.md 仍待填写）。
- 2026-10-31 第二个窗口（工作分支 `claude/lsgc-studio-setup`，main 只放用户上传的文件）：
  - `tools/setup.sh` 跑通，Lovart 客户端已克隆。两个 Lovart 变量都读到了（只检查有没有，不打印）。
  - **Lovart 官方客户端的限制（读源码确认）：** `config`、`projects`、`threads` 只读本机 `~/.lovart/state.json`，不连服务器，新容器里是空的，**既不能验证密钥，也列不出账号里的项目**；`threads` 没有 `--all` 参数（会报错）。客户端没有任何"列出账号项目 / 素材库"的命令。
  - 密钥用 `query-mode` 验证有效（只读、不花积分）。账号当前是 **fast 模式（消耗积分）**；unlimited 可用（`unlimited_enable: true`），无限模型：GPT Image 1.5、GPT Image 2（low 2K）、Midjourney、Nano Banana 2（2K）、Nano Banana Pro（2K）、Seedream 4 / 4.5、Seedream 5.0 Pro（1K，剩 19 天）。要不要切 unlimited 由用户决定（`set-mode` 是持久的服务器设置）。
  - 找 Lovart 里的 IP 素材：需要用户提供项目链接（`canvas?projectId=…`）或在网页上导出图片传到仓库；拿到素材库图片地址和 asset_id 后可以用 `chat --subjects` 引用。
  - 用户把品牌文档 `（已压缩）丽尚国潮集团简介2026.pdf` 放在 main，已复制到 `brand/`。BRAND.md 已按文档整理成草稿（🟡 待用户逐项确认）。从 PDF 截了文字标、圆形标、IP 人偶参考图，登记在 ASSETS.md（🟡）。
  - **小丽画布已接通：** 用户给的分享链接 https://www.lovart.ai/r/eogm9ih 是画布「小丽」（项目 `ot6jDEQsAo`，对话 `f6a2e811-c1de-423c-8a64-96ed18691fad`）。新容器里：`project-add --project-id ot6jDEQsAo`（**不要加 `--name`**，会改服务器上的画布名），然后 `chat --project-id ot6jDEQsAo --thread-id f6a2e811-…` 就能接着原对话做，Lovart Agent 记得之前所有小丽的图。已用一条纯文字消息测试成功（Agent 回答标准形象以「小丽LILY角色设定板」为准）。注意：`chat` 返回整条对话历史，`failures` 里有历史上被拒的记录，判断本次结果要看最后一条。用户说 Lovart 模式可以自由切换。
  - 第一批需求：**丽尚国潮 2026 年度总结视频**，2027 年 1 月发，以小丽为核心，呈现由 Claude 构思。下一步：brand-video 第 0 步（创意方向，等用户选）。
