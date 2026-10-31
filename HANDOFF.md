# 交接文档 · 丽尚国潮素材工作室（2026-10-31 建立）

## 工具分工（用户 2026-10-31 最新决定，替代之前的版本）
- **Lovart 暂不使用**：用户试过，不好用。之后用户主动提起才再用。
- **全部用即梦**：
  - 图片、海报画面、人物 / 产品 / 场景资产：即梦 Seedream 5.0 Pro（`jm.py img`），做图可以直接做；
  - 视频：即梦 Seedance 2.5 样片模式（先报价，在预算内运行）；
  - 海报上的精确文字（品牌名、文案、参数）：用代码排版叠上去（见 brand-visuals skill），不靠模型写字。
- 动态设计、代码渲染的片头片尾、字幕动画、配乐：用 higgsfield-motion / higgsfield-motion-saas skill；视频提示词用 higgsfield-timed-prompts skill。

## 下一个窗口先做这些
1. 确认在 `claude/lsgc-studio-setup` 分支（main 分支是空的）。
2. 通读 CLAUDE.md、BRAND.md、ASSETS.md 和全部 skill（见下面「新窗口的第一步」第 1 条）。
3. `bash tools/setup.sh`。
4. 安装即梦 CLI（安装脚本先下载、读一遍再运行），`auth login --force`，把授权链接用中文发给用户，然后 `auth wait --device-code`。登录后 `auth account` 看积分，`model list` 核对模型。
5. 请用户上传品牌信息文档：放进 `brand/`，整理进 BRAND.md 给用户确认，只写文档里有的内容。丽尚国潮的 IP 素材原来在 Lovart 里，请用户把 IP 形象图导出后上传到 `brand/`。
6. 问第一批要做什么、预算多少，然后按 skill 流程和确认关口开始。

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
  - 用户（2026-10-31）：下周给完整的 2026 大事件（时间、地点、事件）；小丽样子固定、打扮可变；发视频号等多个官方媒体；预算先不考虑。已完成整体设计和脚本框架：`projects/2027-01-2026年度片/design.md`（核心创意、三种风格 S1/S2/S3、90 秒结构和事件占位 E1–E12、转场库、连贯性设定草案和用户在画布里的审美偏好、画幅、声音、参考、流程关口）。三张风格样张在 `style_frames/`，也在小丽画布里。**等用户选风格、确认"金色圆标做贯穿道具"，然后收到事件清单后进入第 1 步（资产）。**
  - 注意：在小丽对话里 `chat --download` 会把整条对话的 70 多张历史图全部下载下来；只需要新图时不要加 `--download`，用最后几个 artifact 的 URL 单独 `download`。
  - **2026-10-31 更正：用户说旧画布 `ot6jDEQsAo` 里有很多错误的小丽，Claude 出的第一版样张也不对。** 用户新建画布 `2ujk8uexd7gg`（https://www.lovart.ai/canvas?projectId=2ujk8uexd7gg），只放了一张原型参考图（用户上传 `https://a.lovart.ai/artifacts/user/2wEl70ukql2RfHJ6.png`，副本 `brand/xiaoli_prototype_sheet.png`）。**以后所有小丽的图都在新画布里做。** 外形锁定写在 `brand/xiaoli_identity.md`，每次生成都附原型图并带锁定段。
  - 新画布里 Lovart Agent 看不到画布上的图（试过），所以参考图必须用 `--attachments` 传。新画布对话：`5dea0f52-092a-401c-9f62-52c2b180b73a`（thinking 模式）。画布是公开可看的，必要时可用无头浏览器打开页面找到图片地址，再用客户端 `download` 下载单张。
