# 2026 大事记 · v9（照「两会新观察｜人工智能+」形式）

参考研究见 `../refs/v9/study.md`。

## 成品（`out9/`）
- `long_v9.jpg`：长图 1080 × 25740，含 docx 原文摘句；`long_v9_notext.jpg`：同一张图不排正文；`long_v9_slices/`：公众号分段（每段 2400 高）。
- `poster_1.jpg` … `poster_8.jpg`：单张海报 1080 × 3240（1:3），插画 + 白色毛笔大字 + 竖排「丽尚国潮」和章节标题。

## 做法
- 即梦画布 `ea9c4282-a3c1-4459-b511-0f054c7b1e59`，Seedream 5.0 Pro。画风参考节点 `style_a/b/c`（参考海报上半部分），人物参考 docx 照片节点。
- 插画节点 `i1`–`i8`（9:21，提示词共用 `style9.txt`），毛笔字节点 `c1`–`c8`（黑底白字，`c3` 重画过一次，第一版「迁」字形含糊）。
- `text_v9.py`：长图正文 = docx 原句摘录（每条都核对过在 docx 里）。排版只做：数字/英文与汉字间空格去掉、直引号换中文引号、在逗号分号处断行（行尾逗号顿号分号和句末句号去掉，同参考）、长句在词与词之间断开（jieba 分词）。
- `prep_v9.py`：新 logo 原图正片叠底贴进换届横匾、乔迁大屏；毛笔字抠成透明底。
- `build_v9.py`（用 `/tmp/studio-tools/venv/bin/python`，需要 jieba）：生成长图、无字版、8 张海报的 HTML。渲染：在上一级目录 `python3 -m http.server 8768 &`，`node ../layout/render_long.js http://localhost:8768/v8/long_v9.html out9/long_v9.png`；海报用 `../layout/render.js`。
- 积分：这一版插画两轮 + 毛笔字 + 重画共 200 积分，项目累计 304 / 1500。
