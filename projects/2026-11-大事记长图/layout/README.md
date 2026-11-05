# 大事记长图 · 排版

- 画面：Lovart 画布 `2qzd6zw00fsw` 生成（不带文字），放 `img/`。
- 文字：全部在 HTML 里排，逐字取自 `../content_2026_raw.md`（用户 docx）。
- **标题和章号用京華老宋体（KingHwa_OldSong）**，用户 2026-11-05 指定。作者特里王（TerryWang），声明免费商用；不可单独售卖字体文件、不可修改字形；字形不合现行规范，作者建议不用于教育等正式用字场合。文件 32MB 不进 git：从 fonthubs 直链下载（1.007 版，2023-07-28；作者原帖只给网盘）：`curl -L -o fonts/KingHwa_OldSong.ttf https://bucket.fonthubs.com/0d31888c-5dfc-431d-aaf7-3487e411146c.ttf`，下载后用 fontTools 核对 name 表是 KingHwa_OldSong。
- 其他字体（OFL 开源，可商用）：马善政（书法标题）、志莽行、刘建毛草、龙藏、思源宋体（Noto Serif SC）。不进 git，下载到某目录后建软链 `fonts/`：
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
| `img/v4/*.jpg` | Lovart GPT Image 2.5 整幅画面（1152×2048 → 1080×1920，经 clean_red + lighten_paper）。开篇 `76kFkouDV4G23CYy`（对话 249ff1de…）；一 `zJlZ9W80aeBNXnXC`；二 `mnYs2bQ5YED3jr4e`；三 `yTXbQeUapnJcsmOv`；四 `qixSP9a295AVQA25`；五 `rPRr34LzFd2B4iCR`；六 `CTLEUu2lUVRs2a2e`；七 `ThYHLnCt1X47bJ9V`；八 `DBFJ2MnNypApmzPU`；结尾 `N4wkK5fyF11sYSBZ` |
| `img/v5/open.jpg` | Lovart GPT Image 2.5「大事记v5_开篇」`mMMW9Uc9WOJxQyIq` |
| `img/v5/ch3_scene.jpg` | 「大事记v5_乔迁插图」`hYlGZKS3Fs7ymMfG` |
| `img/v5/tex_*.jpg` | 「大事记v5_金箔底纹」`GShh7Q2bWH6bmWuo`（tex_ab = 原图 + 上下翻转拼接，可无缝循环） |
| `img/v5/orn_00–10.png` | 「大事记v5_装饰元素」`cMZDfzinNm9UKzoW` 抠图：00/02/10 祥云，01 卷云，03/04 回纹角花，05 桂花，06 梅花，07 太阳，08/09 仙鹤 |
| `img/v5/shan_*`、`bamboo.jpg` | Commons 公有领域古画，见 CREDITS.md；预处理 `prep_v5.py` |
| `img/v6/f1_*.png` | Lovart GPT Image 2.5「大事记v6_卷轴扇框」`yTYJSqjCWrDsAKfu` 抠图：0/1 卷轴天杆地杆，2 折扇，3 团扇；`*_in.png` 是框内部蒙版 |
| `img/v6/f2_*.png` | 「大事记v6_花窗门洞」`9rQoUKf9dOlsugMn`：0 月洞窗，1 八角窗，2 宝瓶门，3 城门拱券 |
| `img/v6/s*.jpg/png`、`end.jpg` | 稳舵 `9mDtIDnrbK3gWCP9`、共生 `v1ZvRpKD9Q39sZjy`、执笔 `Rx3AEOF0bv5Yryze`、杭州 `NZoEZDaCAsL8Fkc5`、金陵 `DYHSnzlln76VLHBg`、金城 `AAzV4Vs4TG3oQIGf`、观光 `EdsBFz2fPe1Rppgx`、结尾 `AdV4yxpIoVA5dVXp` |
