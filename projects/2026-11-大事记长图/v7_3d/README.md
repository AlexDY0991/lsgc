# 2026 大事记长图 · v7（3D 金色未来城市版）

用户 2026-11-07 要求**推翻之前所有版本重做**：第一页用用户自己的「金羊 + 白马」图（`refs/page1_user.jpg`），之后每件大事一页，保留第一页的画风（3D 电影感、C4D、超大广角俯视、中国未来世界、以金为主、夏日炫酷）；**文字全部由用户自己写**；页与页之间用云、丝带、渐变、建筑等自然过渡、不要生硬。

## 结构（1080 × 16100）
封面（用户图）→ 一 换届/党建（金色巨轮、舵轮）→ 二 校企合作（湖畔金色校园 + 跨越两地的光桥）→ 三 乔迁焕新（金色总部大楼 + 朱红丝巾）→ 四 AI 大赛（全息胶片、AI 山水）→ 五 杭州环北（金色商城、布匹、数字光流、物流车队）→ 六 南京环北（城墙、鸡鸣寺塔、玄武湖、城墙下的国潮秀）→ 七 亚欧商厦（黄河、中山桥、白塔山、大鹅气球）→ 八 亚欧国际（313 米金色大厦、观光厅）→ 结尾（金羊奔向旭日、白马远去、三城云海）

## 接缝（每个都不一样）
| 接缝 | 方式 |
|---|---|
| 封面 → 一 | 一排 3D 云海托住封面底部的山丘 + 金色飘带 |
| 一 → 二 | 金色 S 形飘带穿过接缝 |
| 二 → 三 | 阳光渐变（暖光晕） |
| 三 → 四 | 斜向渐变 + 螺旋飘带 |
| 四 → 五 | 云朵轮廓的蒙版边缘 + 沿边一排小云 |
| 五 → 六 | 云海 + 金色光点 |
| 六 → 七 | 横穿整幅的长飘带 |
| 七 → 八 | 同为兰州黄河，长渐变让城市直接延续 |
| 八 → 结尾 | 大片云海 + 阳光 |

## 文件
- `out/long_v7.jpg`：成品（无字）；`out/long_v7_guide.jpg`：蓝色虚线标出每页的文字区（都在天空里）；`out/long_v7_slices/`：公众号分段（每段 2400 高）。
- `build_v7.py`：合成脚本（接缝参数 `SEAMS`、文字区 `TEXT`）；`prep_v7.py`：各页缩放、云和飘带抠图。
- 渲染：本目录 `python3 -m http.server 8766 &`，然后 `node ../layout/render_long.js http://localhost:8766/long_v7.html out/long_v7.png`。

## 素材来源（Lovart 画布 `2qzd6zw00fsw`，GPT Image 2.5，每次附第一页做风格参考）
| 文件 | Lovart artifact |
|---|---|
| `img/p00_page1.jpg` | 用户提供（上传地址见 HANDOFF） |
| `img/p01_wenduo.jpg` | `LT3Fiv2rbEER4YxU`（同题 Nano Banana Pro 版 `G6shUQuDyCHhN6Or` 未用：只有 768 宽、画风偏模型感） |
| `img/p02_xiaoqi.jpg` … `p08_guanguang.jpg` | `DuVDbYQ0CO74735X` `d5EbaBUeQD7uzXxf` `YhQO8nY9O4GttWZL` `1vFgDlIgRv3JXxk3` `VSHX9RjEbWKK3Nvw` `gQjo8KG9UkIFMIL9` `x7zvYCOVpg9MXuYi` |
| `img/p09_end.jpg` | `2lIZuVzswz7b8Uca` |
| `img/cloud_*.png` | `VKqyemkpli2byDBe`（黑底云朵，抠图） |
| `img/ribbon_*.png` | `u7gw42t0Uj8G11vl`（绿幕飘带，抠图） |
