# 第一集《源启》视频生成计划 v1（2026-10-31，等动态分镜确认后执行）

> 第 4 步预案。一律即梦 Seedance 2.5 **样片模式**（`seedance_2.5_draft`，480p，21:9），约 9 积分/秒。视频预算：用户定 **3,600 积分以内**（不够再追加）。每次运行前单独报价，用户确认后才跑。
> 用户提醒：用即梦的**运镜预设**和**全能参考（m2v）**提高准确度。运镜预设只能在网页上点选：节点由 Claude 建好、提示词写好，用户按下表在网页上选预设并运行。

## 生成单位（一次生成 = 一场戏）
| 场 | 镜头 | 时长 | 模式 | 参考（全能参考挂的图） | 运镜预设建议 | 约积分 |
|---|---|---|---|---|---|---|
| V1 | 1.1–1.2 竹 | 12 s | m2v | sb_1_1、sb_1_2、3 张影调参考 | 镜头左移（慢） | 108 |
| V2 | 2.1–2.3 茧·抽丝 | 12 s | m2v | sb_2_1~2_3、char_neolithic、prop_pot_3v2、lay_neolithic | 无（固定 / 缓推） | 108 |
| V3 | 3.1–3.3 织 | 10 s | m2v | sb_3_1~3_3、char_neolithic、prop_backstrap_loom_3v2、lay_neolithic | 镜头左移 | 90 |
| V4 | 4.1–4.4 丝路 | 20 s | m2v | sb_4_1~4_4、lay_jincheng | FPV 穿越机 / 镜头左移 | 180 |
| V5 | 5.1–5.3 唐·杭州 | 10 s | m2v | sb_5_1、look_tang_ling_v2、sb_5_3、char_tang_weaver、lay_tang_room、prop_tang_loom_3v | 镜头左移 | 90 |
| V6a | 6.1 长卷展开 | 4 s | m2v | sb_6_1、prop_scroll_v1 | 镜头左移 | 36 |
| V6b | 6.2 画 → 真实作坊 | 4 s | 首尾帧 | 首 prop_song_painting_v1，尾 lay_song_workshop | 急速推进 | 36 |
| V7 | 6.3–6.7 南宋工序快切 | 12 s | m2v | sb_6_3~6_7、look_song_reeling_v2、char_song_*（3 张）、prop_hualou_3v2、prop_reel_3v、ref_shears_single | 无 | 108 |
| V8a | 7.1 古渡口 → 今日兰州 | 5 s | 首尾帧 | 首 sb_4_4，尾 sb_7_1 | 无（固定机位时空转场） | 45 |
| V8b | 7.2–7.6 三城 + 设计台 | 13 s | m2v | ref 照片 4 张、sb_7_3~7_6、char_designer、lay_design_studio | 一镜到底 / 镜头右移 | 117 |
| V9 | 8.1 夜·拉高 | 8 s | m2v | ref_lanzhou_yaou_intl_night_aerial | 急速后移 | 72 |
| — | 8.2 logo | 6 s | 代码 | — | — | 0 |
| **合计** | | **110 s** | | | | **约 990 / 轮** |

- 先跑一场测试（建议 V7 南宋工序：人物最多、最难），逐帧检查合格后再跑其余。
- 预算分配：第一轮约 990，返工预留两轮约 2,000，余量约 600。
- 每条提示词按 higgsfield-timed-prompts 的结构写：一句话总述 → REFERENCES（@节点：取什么、忽略什么）→ LOOK（LOOK v2）→ 人物 → 道具规则 → 布局 → 带时间码的 SHOTS → SOUND（不要配乐和人声，只要环境声）→ KEEP CONSISTENT。
- 满意后由用户在网页画布上把定剪用到的片段直出 1080p。
