# 第一集《源启》连贯性设定 + 资产记录（v1，2026-10-31）

方向：A「一根丝」（用户 2026-10-31 选定；后改为「经纬是感觉，不是一根真实的丝线」），借南宋《蚕织图》做章节画卷。旁白草稿用户同意先这么做（`ep1_treatment.md`）。结尾落到杭州环北丝绸服装城 → 丽尚国潮集团 logo（用户提供了 logo 和环北航拍）。

## 连贯性设定 v2（2026-10-31 用户反馈后修订，每条提示词都原样附上）
- **不再有一根真实的丝线贯穿全片**（用户：太土气）。「经纬」只是全片的感觉：画面里本来就有的线条承担这个意象 —— 经线、织机的纵横结构、窗格、竹节、河流、街道、城市灯光的网格。另外在少数关键处（开场、结尾 logo）用代码做克制的淡金色经纬线动效，不让 AI 画发光的线。
- **转场靠动作和形状的匹配**：投梭 → 投梭、窗格 → 窗格、河面 → 河面（古今同机位）、剪帛的一刀 → 切到下一场。
- **运动方向：** 镜头运动以从右往左为主（手卷方向，也是东 → 西）。
- **人物：** 允许出现人，以侧脸、低头、背光、局部为主，普通人长相（不是模特），每个人以定妆照为准，同一个人在不同镜头里服装一致。
- **画幅：** 2.39:1 宽银幕（即梦按 21:9 生成）。
- **禁忌：** 不让模型写字；logo 不让 AI 画；不出现灯笼等俗套元素；不出现其他品牌；不出现敦煌壁画飞天（第二集）、大海帆船（第四集）。

## 影调配方（LOOK v2，2026-10-31 校准；对比图 `assets/look_compare.jpg`）
v1 的 AI 感来自：处处是夕阳金色和丁达尔光柱、HDR 一样的通透和锐利、构图居中干净、材质光滑像产品图、只有手没有人（像图库素材）。东方树叶的画面是：低调偏暗、冷青灰橄榄绿、低饱和、柔和高光、真实的人和旧衣服、前景遮挡、不居中构图、浅景深、胶片颗粒。
每条场景 / 镜头提示词都附上这一段（风格参考图：即梦节点 `style_dfsy_41_6`、`style_dfsy_59_6`、`style_dfsy_80_2`，取自东方树叶参考片，只参考影调，不参考内容）：
```
影调参考 @style_dfsy_41_6 @style_dfsy_59_6 @style_dfsy_80_2 这三张图（只参考它们的色调、光线、影调和颗粒质感，不参考其中的内容、人物和服装）：整体低调偏暗，中间调压暗，高光柔和不过曝；冷青灰、橄榄绿为主调，低饱和；暖色只来自少量窗光或火光，没有夕阳金色。阴天漫射光为底，加一个方向的窗光，不要成束的丁达尔光柱。ARRI Alexa 35 配老式球面定焦镜头拍摄，焦段 50–85mm，浅景深，前景有虚化的遮挡物，构图不居中、可以裁切头部。轻微胶片颗粒，不锐化、不HDR、不磨皮。人物是普通人长相、不是模特，皮肤有毛孔、晒痕和细纹，衣服是洗旧、起皱、褪色的粗布，环境有灰尘和使用痕迹。像真实拍摄的电影剧照，不要CG感、不要插画感。画面无文字。
```
- 提示词里不用：电影级、史诗、梦幻、金色光芒、丁达尔、完美、8K、高清细节。
- 现代段（今天三城、设计台）同样低饱和、柔和，但换成冷白的日光和城市的蓝调，不做广告片式的高光亮白。

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
| 挑丝的手 v1 | `assets/v1/prop_reeling_hands_v1.png` | node_e6m6gajxay | 🟡 待确认 | 陶釜、茧、竹箸挑丝、丝线向左上，光对 |
| 原始腰机 v2 | `assets/v1/prop_backstrap_loom_v2.png` | node_d8s3yyrwch | 🟡 待确认 | 陶罐已去掉，经线和绢更细，有丝光（替代 v1） |
| 丝线越群山 v1 | `assets/v1/loc_mountains_v1.png` | node_fcqr1b4ygx | 🟡 待确认 | 雪山、晨雾、丝线从右往左 |
| 绸成沙丘 v2 | `assets/v1/loc_silk_dunes_v2.png` | node_78ztjr7gq6 | 🟡 待确认 | 丝线变细了；驼队剪影太小，朝向仍不明确，视频里写死"向左" |
| 江南水乡 v2 | `assets/v1/loc_jiangnan_v2.png` | node_fazfs4gh9g | 🟡 待确认 | 丝线比 v1 清楚，但仍是几股波浪线 |
| 《蚕织图》风格长卷 v1 | `assets/v1/prop_scroll_v1_flip.png`（原图 `prop_scroll_v1.png` 镜像） | node_226nngw0wt（未镜像） | 🟡 待确认 | 工序连环画面、绢本质感好、无文字。原图卷轴在右侧，像从左往右展开；**已水平镜像**成从右往左（中国手卷方向）。做视频时要上传镜像版 |
| 画中作坊（工笔版） v1 | `assets/v1/prop_song_painting_v1.png` | node_xrtr8wr0v5 | 🟡 待确认 | 和 `loc_song_workshop` 构图、人物位置一致 → 可以做「画变成真实作坊」的首尾帧转场 |
| 南宋喂蚕 v1 | `assets/v1/loc_song_feeding_v1.png` | node_zsrkdjqhrr | 🟡 待确认 | 竹匾、蚕、桑叶、窗格光 |
| 南宋缫丝 v1 | `assets/v1/loc_song_reeling_v1.png` | node_cmrm4najb4 | 🟡 待确认 | 缫车丝軖、煮茧锅、蒸汽、侧背影；露了一点侧脸（规则允许） |
| 南宋剪帛 v1 | `assets/v1/loc_song_cutting_v1.png` | node_z9fsepzasz | 🟡 待确认 | 构图光线好；**剪刀是现代带指环的样式**，宋代应是交股剪（U 形弹簧剪），可以重做 |
| 今日兰州黄河 v1 | `assets/v1/loc_lz_river_today_v1.png` | node_49w7wm0388 | 🟡 待确认 | 河谷、黄土山和古渡口相似，远处超高层是亚欧国际大厦的外形，河边留了一只羊皮筏子呼应。可以和 `loc_jincheng_river` 做首尾帧时空转场 |
| 今日设计台 v1 | `assets/v1/loc_design_studio_v1.png` | node_fdb1gfrbr1 | 🟡 待确认 | 明亮中性光、真丝面料、划粉、直尺、剪刀、牛皮纸样板 |
| 大地经纬 v1 | `assets/v1/loc_earth_night_v1.png` | node_pjw2wzzef0 | ⚠️ 慎用 | 画面好，三个光点连成纬线。**但 AI 画的海岸线和陆地轮廓不准确，公开发布的画面如果能被认成中国地图，需要符合地图规范**。建议改成看不出地图轮廓的写法（云层之上只见城市光点和经纬线），或用正规底图 |
| logo 文字标 | `brand/logo_wordmark.png`（2000×445） | — | ✅ 用户提供 | 高清位图，可描成矢量做走针动画 |
| logo 圆标 | `brand/logo_mark.png`（2000×1995） | — | ✅ 用户提供 | 同上 |

## 原「下一批资产」清单（2026-10-31 已全部做完，见上表）
- 道具：陶釜和茧（并入生丝定妆）、原始腰机、驼队货包、唐代织机和柿蒂纹绫、运河船、现代设计台和剪刀。
- 人物（只出手和侧脸）：新石器织者、唐代红袖织绫女子、南宋织工两人、现代设计师。
- 场景：新石器作坊、大漠驼队、海港、唐代杭州窗边（西湖晨雾）、运河拱桥、现代设计工作室、环北室内、杭州夜景俯瞰（结尾经纬网）。
- 画卷：《蚕织图》风格的长卷（参考公开馆藏图像重绘）。

## 规范资产（Higgsfield 第一步，2026-10-31 补做，LOOK v2）
旧的 24 张 v1 电影画面降级为**风格 / 分镜参考**，不再作为身份依据。以下为正式资产，全部 🟡 待用户确认。文件在 `assets/sheets/`，拼图：`assets/sheets_characters.jpg`、`assets/sheets_props.jpg`、`assets/sheets_props_v2.jpg`、`assets/sheets_layouts.jpg`。影调校准：`assets/look_v2/`，对比 `assets/look_compare.jpg`。

| 编号 | 资产 | 节点键（状态文件） | 自查 |
|---|---|---|---|
| C1 | 新石器织者 | `char_neolithic` | 三联格式对；粗麻贯头衣、骨簪、赤脚、皮腰带 |
| C2 | 唐代织绫女子 | `char_tang_weaver` | 脸取自 `look_tang_ling_v2`；暗红宽袖短襦、灰褐长裙 |
| C3 | 南宋织工（投梭） | `char_song_weaver` | 脸取自 `look_song_workshop_v2`；灰蓝头巾和衣裤、围裙 |
| C4 | 南宋拉花工 | `char_song_drawboy` | 脸取自 `look_song_workshop_v2`；本色交领短衣、绑腿草鞋 |
| C5 | 南宋蚕娘（喂蚕、缫丝、剪帛同一人） | `char_song_silkwoman` | 脸取自 `look_song_reeling_v2`；深灰头巾、交领衫、围裙 |
| C6 | 现代设计师 | `char_designer` | 齐肩短发、藏青衬衫、软尺、白帆布鞋 |
| P1 | 原始腰机 | `prop_backstrap_loom_3v2` | v2：无框架的软结构、兽皮编织腰带无金属扣（v1 是框架 + 皮带扣，作废） |
| P2 | 唐代斜织机 | `prop_tang_loom_3v` | 四视图一致；结构是模型理解的斜织机，请学校老师看 |
| P3 | 南宋花楼机 | `prop_hualou_3v2` | v2 有人形比例，花楼高于人；体量仍比真实花楼机小一些 |
| P4 | 宋代脚踏缫车 | `prop_reel_3v` | 煮茧锅、导丝钩、六角丝軖、踏板，四视图一致 |
| P5 | 宋代交股剪 | `prop_shears_3v2` | v2：U 形弹簧、无指环无转轴，四视图一致（v1 混了两种剪刀，作废） |
| P6 | 陶釜和竹箸 | `prop_pot_3v2` | v2：架在三块石头上（v1 有奇怪的吊石，作废） |
| L1 | 新石器作坊 | `lay_neolithic` | 干栏木屋、门口天光、火塘陶釜、中间空地留给腰机 |
| L2 | 唐代窗边织室 | `lay_tang_room` | 左侧临湖木窗是主光，斜织机和空坐凳，络丝籰子 |
| L3 | 南宋作坊 | `lay_song_workshop` + 俯视图 `lay_song_workshop_top` | 布局与 v1 一致；地面仍有窗格光斑（比 v1 克制）；俯视图：橙点＝拉花工 C4，蓝点＝织工 C3，三角＝主机位 |
| L4 | 金城古渡口 | `lay_jincheng` | 阴天、风沙、羊皮筏子和货包，无现代建筑；河流方向视频里写死"自左向右" |
| L5 | 今日设计工作室 | `lay_design_studio` | 大窗冷白光、打板台、面料、剪刀、衣架；偏干净，视频里压暗一点 |

还用 v1 画面、暂不重做的：竹林暗场、群山、沙丘、江南、长卷、工笔作坊、今日兰州黄河、三城黄昏（建筑类以用户照片为准）。进入分镜时，凡是 v1 里出现金色夕阳和丝线的，都按 LOOK v2 重画。
