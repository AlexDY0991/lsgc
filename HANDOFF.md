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
