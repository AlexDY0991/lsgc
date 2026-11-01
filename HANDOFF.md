# 交接文档 · 丽尚国潮素材工作室（2026-10-31 建立）

## 工具分工（用户 2026-10-31 最新决定，替代下面进度记录里的旧分工）
- **Lovart 暂停使用**：用户觉得不好用。用户主动提起才再用。Lovart 里已有的东西（小丽原型图、风格样张）都已下载到仓库，可以当参考图。
- **全部改用即梦**：
  - 图片、海报画面、小丽和场景资产：即梦 Seedream 5.0 Pro（`jm.py img`），参考图用 `jm.py upload` 上传后在提示词里 `@KEY` 引用。做图可以直接做；
  - 视频：即梦 Seedance 2.5 样片模式（每次先报价，在预算内运行）；
  - 精确文字（品牌名、文案、年份、数据）：代码排版叠上去（brand-visuals skill），不靠模型写字。
- 动态设计、代码渲染的片头片尾、字幕和数字动画、临时配乐：higgsfield-motion / higgsfield-motion-saas skill；视频提示词：higgsfield-timed-prompts skill。

## 下一个窗口（第三个窗口）先做这些
1. 确认在 `claude/lsgc-studio-setup` 分支（main 只放用户上传的原始文件）。
2. 通读 CLAUDE.md、BRAND.md、ASSETS.md、`brand/xiaoli_identity.md`、`projects/2027-01-2026年度片/design.md`，以及全部 skill：brand-video（重点）、brand-visuals、jimeng-canvas、higgsfield-timed-prompts、higgsfield-motion、higgsfield-motion-saas；和 `docs/higgsfield-realism-workflow-notes.md`。
3. `bash tools/setup.sh`。
4. 安装即梦 CLI（安装脚本先下载、读一遍再运行），`auth login --force`，把授权链接用中文发给用户，然后 `auth wait --device-code`（不能用 auth status 轮询代替）。登录后 `auth account` 看积分，`model list` 核对模型。
5. 新建即梦画布「丽尚国潮 2026 年度片」和状态文件 `projects/2027-01-2026年度片/jimeng-state.json`；上传 `brand/xiaoli_prototype_sheet.png`（大 PNG 先转 JPEG）登记为节点 `xiaoli_ref`，登记进 ASSETS.md 第 6 节。
6. 用即梦按 `brand/xiaoli_identity.md` 的锁定段重做小丽：先出一张标准打扮的三视图定妆（正面、侧面、背面），逐条对「之前出过的错」自查，再给用户确认（brand-video 第 1 步）。Lovart 版风格样张只当参考，风格方向仍等用户选（design.md 第 9 节 S1/S2/S3）。
7. 等待中的用户决定：选风格；确认「金色圆标做贯穿道具」；BRAND.md 草稿逐项确认；下周提供 2026 大事件清单。

## 新窗口的第一步（通用）
1. 通读 `CLAUDE.md`、`BRAND.md`、`ASSETS.md`，以及 skill：`brand-video`（重点）、`brand-visuals`、`jimeng-canvas`、`lovart`（暂停使用）、`higgsfield-timed-prompts`、`higgsfield-motion`。
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
- 2026-10-31 第三个窗口：
  - `tools/setup.sh` 跑通；即梦 CLI 1.2.1 重装（安装脚本先读，用户批准后运行；下载时连接被重置几次，重试成功）。登录成功，有效期到 2026-10-31 20:07 UTC（约 6 小时）。`auth wait` 第一次报 `auth_dependency_failed`（可重试），用同一个 device code 重试就成功了。
  - 账号 maestro 会员，可用 29,475 积分（11-22 到期 13,455；11-26 到期 3,700；11-27 到期 12,320）。模型里有 `seedream_5.0_pro`、`seedance_2.5_draft`、`seed_music_1.0`。
  - 写好了小丽三视图定妆提示词 `projects/2027-01-2026年度片/prompts/xiaoli_turnaround_v1.md`（没生成）。**用户：小丽和年度片暂停，改做一个新片子**（内容等用户说明）。年度片画布、状态文件都还没建。
  - **新项目：丽尚国潮 AI 艺术短片（校企合作，四集《源启》《流韵》《汇影》《潮鸣》）**，目录 `projects/2026-11-AI艺术短片/`：方案 PDF 和全文 `plan_text.txt`、参考片 `refs/东方树叶十周年.mp4`（拉片在 `refs/dfsy_analysis/`）。先做第一集《源启》（丝绸）。研究结论在 `ep1_study.md`。用户（10-31）：思路由 Claude 研究、史实由 Claude 整理、品牌最后点到集团、可以有旁白、时长不固定。史实表 `ep1_facts.md`，三个方向和推荐结构（含旁白草稿）`ep1_treatment.md`，等用户选方向。
  - 用户选方向 A「一根丝」，旁白草稿同意先用；提供 logo 高清位图（`brand/logo_wordmark.png`、`brand/logo_mark.png`）和环北航拍（`brand/photos/huanbei_aerial_day.jpg`）。用户提醒：即梦视频用运镜预设和全能参考（m2v）提高准确度。
  - 即梦画布「丽尚国潮 AI艺术短片 第一集 源启」已建，状态文件 `projects/2026-11-AI艺术短片/jimeng-state.json`（资产阶段做图上限 800 积分，视频预算未定）。`tools/jm.py` 加了 `--ratio`。
  - 第一批资产 4 张（32 积分）：生丝道具、竹林暗场、南宋丝织作坊、环北黄昏。连贯性设定和资产表在 `ep1_bible.md`，等用户确认。
  - 用户（10-31）：要丝绸之路画面（兰州亚欧商厦、亚欧国际是丝路要点），第一集可以务虚；结尾三城都出现（加南京）。脚本 v2 `ep1_script_v3.md`（v2 在 git 历史里）：经＝古今、纬＝东西；丝路段放汉唐（南宋陆上丝路已衰落）。提供南京环北、亚欧商厦、亚欧国际两张照片（`brand/photos/`，已上传即梦）。第二批资产 7 张（56 积分）在 `ep1_bible.md`，等用户确认两批资产、选结尾句、定视频预算。
  - 用户：先做所有资产。第三批 13 张（104 积分）已做完并自查（见 `ep1_bible.md`），共花 192 积分。待用户确认全部资产；注意「大地经纬」涉及地图规范，建议改写法。下一步：分镜 → 动态分镜。
  - 用户（10-31）：①要按 Higgsfield 先做规范资产；②**不要一根真实丝线贯穿**（土气），经纬只是感觉 + 少量代码动效；③v1 AI 感重，不如东方树叶。已做：LOOK v2 影调配方（东方树叶 3 帧作影调参考，2.39:1），校准对比 `assets/look_compare.jpg`；人物定妆 6、道具三视图 6（4 张重做）、场景布局 5 + 俯视图 1，见 `ep1_bible.md`「规范资产」。脚本改为 v3。累计 392 积分。等用户确认规范资产和新影调。
  - 用户（10-31）：新影调方向对；资产先不改继续做；**视频预算 3600 以内**（不够再追加）。已做：分镜 v1（32 镜，`storyboard/storyboard_v1.md`，提示词源 `prompts/storyboard_v1.py`）；动态分镜 v1 `animatic/out/源启_动态分镜_v1.mp4`（116 秒，脚本 `animatic/animatic_v1.py`，临时旁白 Kokoro 中文 zm_yunjian、临时配乐 score.html organic 75BPM）；视频生成计划和报价 `ep1_video_plan.md`（约 990 积分/轮）。累计做图 632 积分。等用户确认动态分镜的节奏和叙事，再报价跑第一场测试（建议 V7 南宋工序）。
  - 注意：render_audio.mjs 渲染 116 秒的配乐要 20 分钟以上，需加 `--timeout 1500`；Kokoro 中文发音有误（"经纬"读不准），只当临时。
  - 用户看完动态分镜 v1：画面可以，但没有高潮，结尾没有情绪。同意新方向：伏笔（新石器织女抬头）→ 高潮「千年一梭」越切越快、南宋一剪匹配今天一剪 → 真空（设计师抬头 ↔ 织女抬头）→ 释放（三城亮灯、有人）→ logo。脚本 v4 `ep1_script_v4.md`；新增分镜 8 张 `storyboard/v2/`（64 积分，累计做图 696）；动态分镜 v2 `animatic/animatic_v2.py`；视频计划 v2 约 1,310 积分/轮。
  - 11-01：第一轮视频跑完（非手艺 9 场 + 手艺 5 场 + 纪实重做今天的人），视频累计 1,620 / 3,600。粗剪 v1 `rough/out/源启_粗剪_v1.mp4`（118 秒，`rough/build_rough_v1.py`，问题清单 `rough/rough_v1_notes.md`）。原始视频片段不进 git，状态文件里有 submitId 可重新下载；粗剪要用动态分镜 v2 的 mix.wav（在 scratchpad，丢了就重跑 `animatic/animatic_v2.py`，配乐要 20 分钟）。等用户看粗剪。
  - 11-01：用户要求：音乐由 Claude 找或做，可以用即梦配音；高潮按匹配剪辑重做；唐代投梭和长卷重做；重新粗剪，精做 logo；**高清先不做**。已完成粗剪 v2 `rough/out/源启_粗剪_v2.mp4`（`rough/build_rough_v2.py`，说明见 `rough/rough_v2_notes.md`），logo `rough/logo/logo_v1.py`。配乐 M2，配音「沉稳解说Pro」。`tools/jm.py` 新增 `tts` 命令。音频在 `audio/`（扩展名是 .wav，内容是 mp3）。积分：视频 1,908 / 3,600，总计 2,754。等用户看 v2、选配音声音。
