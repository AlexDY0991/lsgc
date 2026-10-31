# 交接文档 · 丽尚国潮素材工作室（2026-10-31 建立）

## 新窗口的第一步
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
