# 大事记长图 · 排版

- 画面：Lovart 画布 `2qzd6zw00fsw` 生成（不带文字），放 `img/`。
- 文字：全部在 HTML 里排，逐字取自 `../content_2026_raw.md`（用户 docx）。
- 字体（OFL 开源，可商用）：马善政（书法标题）、志莽行、刘建毛草、龙藏、思源宋体（Noto Serif SC）。不进 git，下载到某目录后建软链 `fonts/`：
  ```bash
  mkdir -p FONTS && cd FONTS
  for f in mashanzheng/MaShanZheng-Regular.ttf zhimangxing/ZhiMangXing-Regular.ttf liujianmaocao/LiuJianMaoCao-Regular.ttf longcang/LongCang-Regular.ttf "notoserifsc/NotoSerifSC%5Bwght%5D.ttf"; do curl -sSfLO "https://raw.githubusercontent.com/google/fonts/main/ofl/$f"; done
  mv "NotoSerifSC%5Bwght%5D.ttf" NotoSerifSC.ttf
  ```
- 渲染：`node render.js sample_v1.html out/sample_v1.png`（宽 1080，整页长图）。

| 图 | 来源 |
|---|---|
| `img/kaipian_v2.png` | Lovart `I1xa9pUAgz2QvTju`（大事记_开篇_v2_无人物，由 v1 `tUxqPWU4oGIeZuCs` 去掉小丽） |
| `img/qiaoqian_v1.png` | Lovart `Tb8pzQCZJ27OsLwj`（大事记_乔迁焕新_v1） |
| `img/logo_*.png` | `brand/`（用户提供的高清 logo） |
