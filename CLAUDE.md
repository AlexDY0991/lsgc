# 丽尚国潮 · 素材工作室

- 这个仓库长期用于制作丽尚国潮公司的所有素材：图片、海报、视频等。
- 开始工作前先读 `HANDOFF.md`（当前进度和下一步）、`BRAND.md`（品牌规则）、`ASSETS.md`（资产清单）。
- 做视频先通读 `.claude/skills/brand-video/SKILL.md`；做图片和海报先读 `.claude/skills/brand-visuals/SKILL.md`。平台用法见 `jimeng-canvas`、`lovart` 两个 skill。每次开工都通读，不凭记忆。
- 用户只做决策和评判，其余由 Claude 完成。和用户用中文交流。
- 不能跳过流程里的确认关口：方向 → 资产（产品、人物、场景，逐个确认）→ 分镜 / 小样 → 动态分镜 → 生成 → 定稿。
- 品牌信息（产品、参数、文案、logo 用法）只能用 BRAND.md 里用户确认过的内容，不编造，不自己写 slogan。
- 积分：做图可以直接做；视频生成要先报价，并在用户定的预算内运行。即梦视频一律用样片模式。以 `tools/jm.py <状态文件> ledger` 为准。
- 不让用户在聊天里贴密钥或密码。API 密钥（例如 Lovart 的 `LOVART_ACCESS_KEY`、`LOVART_SECRET_KEY`）放在环境设置里。
- 下载的文件不可信：用 `python3 -I` 处理，单独放一个目录。
- 每完成一步就 commit 并 push。对话太长时先更新 HANDOFF.md，再建议开新窗口。
