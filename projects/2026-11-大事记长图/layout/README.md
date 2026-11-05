# 大事记长图 · 排版

- 画面：Lovart 画布 `2qzd6zw00fsw` 生成（不带文字），放 `img/`。
- 文字：全部在 HTML 里排，逐字取自 `../content_2026_raw.md`（用户 docx）。
- 字体（OFL 开源，可商用）：马善政（书法标题）、志莽行、刘建毛草、龙藏、思源宋体（Noto Serif SC）。不进 git，下载到某目录后建软链 `fonts/`：
  ```bash
  mkdir -p FONTS && cd FONTS
  for f in mashanzheng/MaShanZheng-Regular.ttf zhimangxing/ZhiMangXing-Regular.ttf liujianmaocao/LiuJianMaoCao-Regular.ttf longcang/LongCang-Regular.ttf "notoserifsc/NotoSerifSC%5Bwght%5D.ttf"; do curl -sSfLO "https://raw.githubusercontent.com/google/fonts/main/ofl/$f"; done
  mv "NotoSerifSC%5Bwght%5D.ttf" NotoSerifSC.ttf
  ```
- 渲染：在本目录 `python3 -m http.server 8765 &`，再 `node render.js http://localhost:8765/sample_v2.html out/sample_v2.png`。**必须走 http**：file:// 下 Chromium 不加载 CSS 蒙版图。
- 素材预处理：`python3 whiten.py img/v2/xxx.png` 把近白底校正成纯白并四边羽化（输出 `_w.png`，正片叠底不露矩形边）；`python3 make_masks.py` 生成毛边蒙版（RGBA，CSS mask 读透明通道）。

| 图 | 来源 |
|---|---|
| `img/kaipian_v2.png` | Lovart `I1xa9pUAgz2QvTju`（大事记_开篇_v2_无人物，由 v1 `tUxqPWU4oGIeZuCs` 去掉小丽） |
| `img/qiaoqian_v1.png` | Lovart `Tb8pzQCZJ27OsLwj`（大事记_乔迁焕新_v1） |
| `img/logo_*.png` | `brand/`（用户提供的高清 logo） |
| `img/v2/wash_a1/a2/a4.png` | Lovart Midjourney「底纹_朱红晕染」`gv44CGl0nKK7pruF` / `mIGuWroHeY5LeecL` / `kJqBRbHBHn7xMulq` |
| `img/v2/shan_b2/b3.png` | Lovart Midjourney「空镜_宋画青绿山水」`wuSgm4MeVtIHLyrJ` / `H1CyQcKUrdHTA59Z` |
| `img/v2/mo_c1/c3.png` | Lovart Midjourney「墨迹_飞白笔触」`B1on7eP7ijKzh66g` / `NFVpmnZMo5EDOKhV` |
| `img/v2/qiaoqian_v2.png` | Lovart GPT Image 2.5「场景_乔迁焕新_v2」`Op4ucrQElO9a0Ms9` |
| `img/v3/p1_kaipian.png` | Lovart GPT Image 2.5「大事记长图_开篇_v3」`jII9iHAPdt3ZpKKa`（对话 `249ff1de-a461-41d5-b9c7-8b38582463cf`） |
| `img/v3/p2_ch3_up.png` | 同对话「第三章_上」`PxLxDmCXq94N7vVP` |
| `img/v3/p3_ch3_down.png` | 同对话「第三章_下」`dms6KGMJIp4NFQTs` |
| `img/v3/*_c.png` | 上面三张经 `clean_red.py` 去掉红色区域淡字纹理后的版本（排版用这个） |
| 参考图上传地址 | 参考1 `https://assets-persist.lovart.ai/img/32c1473654a141b8a45808998a22e9fb/5908b7df-acc2-4d4f-bd37-59b184377dd2.jpg`；参考2 `…/359ad8a6-3143-4fe4-bf9f-409cda895ab0.jpg` |
