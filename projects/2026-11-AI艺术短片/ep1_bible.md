# 第一集《源启》连贯性设定 + 资产记录（v1，2026-10-31）

方向：A「一根丝」（用户 2026-10-31 选定），借南宋《蚕织图》做章节画卷。旁白草稿用户同意先这么做（`ep1_treatment.md`）。结尾落到杭州环北丝绸服装城 → 丽尚国潮集团 logo（用户提供了 logo 和环北航拍）。

## 连贯性设定（每条视频提示词都原样附上）
- **主角道具：一缕生丝。** 几十根极细蚕丝并成的一缕，约 1 毫米，淡金色、半透明、有丝光。它是画面里唯一的暖金亮点。以 `prop_silk` 为准。不发光、不像霓虹、不变成金属丝。
- **运动方向：** 丝线和镜头运动全片从画面右往左（和中国长卷的展开方向一致）。
- **主光：** 古代段为画面左上方的窄硬光（窗格光 / 斜射光），《一代宗师》式；暗部青灰、石绿。现代段转为明亮的中性白光。
- **景别：** 手、器物、材质的特写为主，人物只露侧脸、背影、手。不出现完整正脸。
- **色调（方案「宋韵青金」）：** 青灰、石绿暗部 + 生丝淡金 + 木头赭石；偶尔一点炉火暖光。
- **禁忌：** 不让模型写字（字幕、logo 用代码叠加）；logo 不让 AI 画；不出现灯笼等俗套元素；不出现其他品牌。

## 资产（第 1 步）
| 资产 | 文件 | 即梦节点 | 状态 | 自查 |
|---|---|---|---|---|
| 环北航拍（白天，用户提供） | `brand/photos/huanbei_aerial_day.jpg` | `ref_huanbei` node_77xj6qxq59 | ✅ 用户提供 | — |
| 道具·生丝 v1 | `assets/v1/prop_silk_v1.png` | node_txdtfwapb4 | 🟡 待确认 | 三格：煮茧抽丝 / 暗场里绷直发亮 / 微距多根细丝并合。丝线走向右下 → 左上，符合设定 |
| 开场·竹林暗场 v1 | `assets/v1/loc_bamboo_v1.png` | node_ncy1thggdk | 🟡 待确认 | 留白、左上硬光、青绿都对；**竹身上的淡金经纬细纹没有出来**，打算在视频里用丝线从竹节"抽出"来表现，不一定要在静帧里有 |
| 场景·南宋丝织作坊 v1 | `assets/v1/loc_song_workshop_v1.png` | node_jrpq773eck | 🟡 待确认 | 花楼机上下两人（拉花 + 织工）、左侧直棂窗硬光、蚕茧筐、丝绸匹料、络丝架都有；前景右侧留了空地。花楼机结构是模型理解的样子，需要学校老师看一眼是否像宋代 |
| 场景·环北黄昏 v1 | `assets/v1/loc_huanbei_dusk_v1.png` | node_z72ph9bxzm | 🟡 待确认 | 建筑外形、倒锥玻璃体、天际线和电视塔对；主招牌「杭州环北丝绸服装城」和圆标正确。**左下「杭州银行」招牌字变形了**；构图比原照片稍微拉远。可以在后期用原照片的招牌区域替换，或重生成 |
| 南京环北（白天，用户提供） | `brand/photos/nanjing_huanbei_day.jpg` | `ref_nanjing_huanbei_day` node_gkw12x9npe | ✅ 用户提供 | — |
| 兰州亚欧商厦（白天，用户提供） | `brand/photos/lanzhou_yaou_shangsha_day.jpg` | `ref_lanzhou_yaou_shangsha_day` node_7016nfyk4w | ✅ 用户提供 | — |
| 兰州亚欧国际大厦（日出航拍，用户提供） | `brand/photos/lanzhou_yaou_intl_sunrise.jpg` | `ref_lanzhou_yaou_intl_sunrise` node_zcyztjngz1 | ✅ 用户提供 | 光线已经很好，可直接做首帧参考 |
| 兰州亚欧国际大厦（夜景俯拍，用户提供） | `brand/photos/lanzhou_yaou_intl_night_aerial.jpg` | `ref_lanzhou_yaou_intl_night_aerial` node_m26azea0sk | ✅ 用户提供 | 适合第 8 段大地俯瞰的起点 |
| 江南水乡晨雾 v1 | `assets/v1/loc_jiangnan_v1.png` | node_jxwg9wx042 | 🟡 待确认 | 留白、晨雾、左上光对；**丝线画成了一团烟雾状**，比 `prop_silk` 蓬松，视频里要强调"一缕" |
| 原始腰机和手 v1 | `assets/v1/prop_backstrap_loom_v1.png` | node_bet2frsenb | 🟡 待确认 | 席地而坐、经线向左绷直、骨质打纬刀、五指正常；织物像麻布，偏粗；经线下面多了一个陶罐，位置有点怪 |
| 丝路·绸成沙丘 v1 | `assets/v1/loc_silk_dunes_v1.png` | node_crn8ngh6g5 | 🟡 待确认 | 绸缎化沙丘的意境很好；**驼队朝右走，和"向西＝向左"相反**，视频里要改方向；丝线偏蓬松 |
| 金城黄河古渡口 v1 | `assets/v1/loc_jincheng_river_v1.png` | node_1nj13wzaa9 | 🟡 待确认 | 黄土山、羊皮筏子、驼队、无现代建筑，都对。注意：黄河在兰州是自西向东流，按"右＝东"应从左往右流，视频提示词要按这个写 |
| 唐代红袖织绫 v1 | `assets/v1/prop_tang_ling_v1.png` | node_ed3sm4ddnk | 🟡 待确认 | 红袖、四瓣柿蒂纹、窗外西湖晨雾都对；织机的经线方向和织物的关系不太符合真实织机（特写里不明显） |
| 南京环北黄昏 v1 | `assets/v1/loc_nj_huanbei_dusk_v1.png` | node_qv8jgrb97w | 🟡 待确认 | 建筑、招牌「环北 服装批发市场」都对，圆柱玻璃裙楼亮灯 |
| 兰州亚欧商厦黄昏 v1 | `assets/v1/loc_lz_shangsha_dusk_v1.png` | node_jsgtdt985v | 🟡 待确认 | 建筑、金色「亚欧商厦」字和标志都对；小招牌字模糊不影响 |
| logo 文字标 | `brand/logo_wordmark.png`（2000×445） | — | ✅ 用户提供 | 高清位图，可描成矢量做走针动画 |
| logo 圆标 | `brand/logo_mark.png`（2000×1995） | — | ✅ 用户提供 | 同上 |

## 下一批资产（等第一批确认后做）
- 道具：陶釜和茧（并入生丝定妆）、原始腰机、驼队货包、唐代织机和柿蒂纹绫、运河船、现代设计台和剪刀。
- 人物（只出手和侧脸）：新石器织者、唐代红袖织绫女子、南宋织工两人、现代设计师。
- 场景：新石器作坊、大漠驼队、海港、唐代杭州窗边（西湖晨雾）、运河拱桥、现代设计工作室、环北室内、杭州夜景俯瞰（结尾经纬网）。
- 画卷：《蚕织图》风格的长卷（参考公开馆藏图像重绘）。
