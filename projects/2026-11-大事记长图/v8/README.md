# 2026 大事记长图 · v8（简约清爽版）

设计思路见 `plan.md`。成品 `out/long_v8.jpg`（1080 × 20640，无字）；参考线版 `out/long_v8_guide.jpg`（蓝框 = 用户写字的区域）；公众号分段 `out/long_v8_slices/`（每段 2400 高）。

## 做法
- **即梦画布**「丽尚国潮 2026 大事记长图」：https://jimeng.jianying.com/ai-tool/ai-canvas/ea9c4282-a3c1-4459-b511-0f054c7b1e59 ，状态文件 `jimeng-state.json`（节点 ID、积分账本；做图预算 1500，本轮用了 104）。
- 资产节点：`cover`（封面）、`photo_huanjie` `photo_qianyue` `photo_qiaoqian` `photo_nanjing`（docx 照片）、`poster_ai`（AI 大赛主视觉）、`logo_new` `logo_mark_new`、`ref_layout_a/b`（版式参考）。
- 模型：**Seedream 5.0 Pro**（8 积分/张）。账号对 Image 2.5 Pro、Image 2、N-Pro 等外部模型无权限（报价返回 Permission denied），ImageMax 报价失败。
- 每块画面用「真实照片 + 封面」两张参考生成：照片定人物站位、动作、服装，封面定画风；色调天蓝、白、浅青为主，金色只点缀。提示词共用 `style.txt`。
- `prep_v8.py`：新 logo 用原图正片叠底贴进换届横匾、乔迁大屏（不让模型画 logo）；换届、签约、秀场三块裁切放大核心；白云 / 红绸 / 燕子抠图。
- `build_v8.py`：每块上下羽化融进一条连续的淡蓝底色（底色按各块上下沿颜色插值）；块间是写字区；过渡元素只在 4 个接缝出现：封面下的云带、第二块后的燕子、第五块后唯一一条红绸、第七块后漫进观光厅的云。
- 渲染：本目录 `python3 -m http.server 8767 &`，`node ../layout/render_long.js http://localhost:8767/long_v8.html out/long_v8.png`。

| 块 | 即梦节点 | 来源 |
|---|---|---|
| 一 换届 | `e1` | photo_huanjie + cover，横匾贴新 logo 组合 |
| 二 签约 | `e2` | photo_qianyue + cover |
| 三 乔迁 | `e3` | photo_qiaoqian + cover，大屏贴新 logo 文字标 |
| 四 AI 大赛 | `e4` | poster_ai + cover |
| 五 采批节 | `e5` | 文字描述；宣传画上「环北采批节」由模型写、已逐字核对 |
| 六 南京 | `e6` | photo_nanjing + cover |
| 七 亚欧商厦 | `e7` | 文字描述 |
| 八 观光厅 | `e8` | 文字描述 |
| 结尾 | `end` | cover（金羊） |
| 过渡素材 | `t_cloud` `t_silk` `t_birds` | 黑底云 / 绿幕红绸 / 白底燕子 |
