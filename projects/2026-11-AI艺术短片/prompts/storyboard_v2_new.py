#!/usr/bin/env python3
"""第一集《源启》分镜 v2 新增镜头（高潮「千年一梭」、真空的眼神、释放段的人）。
其余镜头沿用 storyboard_v1.py。用法：python3 projects/2026-11-AI艺术短片/prompts/storyboard_v2_new.py save [key ...]
"""
import importlib.util, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('sb1', HERE / 'storyboard_v1.py'); sb1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(sb1)
W, LOOK_NOW = sb1.W, sb1.LOOK_NOW.replace('招牌文字保持照片原样，不生成新文字。', '画面里不出现任何招牌文字和品牌标志。')
S = sb1.S

NEW = {
 'sb2_c6_cut': ("设计师剪开丝绸（与南宋剪帛匹配切）",
   W + "以 @lay_design_studio 的空间为准：@char_designer 这位设计师（脸和衣服以定妆照为准，藏青衬衫袖子挽起）俯身在打板台上，双手用一把裁缝剪刀从右向左剪开一块浅米色真丝面料，剪口的丝头微微翘起。构图和 @sb_6_7 相同：面料横铺在画面里，台面占画面下半部，她的手从画面右侧进入，左侧大窗的冷白光照在丝绸上。中近景。" + LOOK_NOW),
 'sb2_c6_lookup': ("设计师停下，抬头望向窗外（与新石器织女抬头匹配）",
   W + "@char_designer 这位设计师（脸和衣服以定妆照为准）剪完后停下手，抬起头望向画面左侧的大窗外，侧脸被冷白的窗光照亮，眼神平静，有一点动容。近景，构图和 @sb_3_3 完全相同：人物在画面右侧三分之一、脸朝左，背景是虚化的工作室。" + LOOK_NOW),
 'sb2_hb_fold': ("环北商户叠丝绸",
   W + "今天杭州一家丝绸服装批发商铺里，一位五十岁上下的女商户（普通人长相，短发，深色针织开衫）在柜台上熟练地叠一件浅色真丝衬衫，身后货架上是成排的丝绸成衣，清晨冷白的灯光。近景，焦点在手和丝绸上，她的脸在焦外、侧面。" + LOOK_NOW),
 'sb2_hb_pack': ("清晨，商户扛起货包",
   W + "清晨，今天杭州的服装批发市场门口，一位三十多岁的男商户（普通人长相，旧夹克）把一大包用编织袋捆好的货扛上肩，旁边是成堆的货包和推车，天刚亮的蓝灰色光，路灯还亮着。中景，背面和侧脸。" + LOOK_NOW),
 'sb2_mall_family': ("兰州商场门口，一家三口走进灯光",
   W + "黄昏，兰州一座百货商场的入口，一家三口（年轻的父母和六七岁的女儿）牵着手走进温暖的灯光里，女儿穿一件浅色连衣裙，回头笑。中景，商场里的暖光和门外的蓝调天色对比，背景虚化。" + LOOK_NOW),
 'sb2_river_people': ("今日兰州黄河边的人",
   W + "今天兰州黄河边的滨河步道，傍晚，几位老人坐在河边长椅上聊天，一个孩子沿着栏杆跑过，背景是浑黄的黄河和对岸亮起灯的楼群。中景，普通人长相，自然、真实，不摆拍。" + LOOK_NOW),
 'sb2_hb_smile': ("傍晚收摊，商户回头笑着打招呼",
   W + "傍晚，今天杭州服装批发市场的一个商铺，一位四十多岁的男商户（普通人长相）一边拉下半截卷帘门，一边回头和邻铺的人笑着打招呼，铺子里的灯还亮着，暖光从门里透出来。近景，真实、温暖。" + LOOK_NOW),
 'sb2_window_rise': ("从工作室窗口望出去，城市亮灯",
   W + "黄昏，从一间设计工作室的大窗向外看：窗外是今天杭州的城市屋顶和远处的楼群，城里的灯一盏一盏亮起，天空是深蓝灰，天边一抹很淡的暖色。窗框在画面边缘虚化，玻璃上有一点室内的倒影。" + LOOK_NOW),
}

if __name__ == '__main__':
    if sys.argv[1:2] == ['save']:
        only = sys.argv[2:]
        for k, (title, prompt) in NEW.items():
            if only and k not in only:
                continue
            subprocess.run(['python3', 'tools/jm.py', S, 'img', k, '--ratio', '21:9', '--title', '分镜v2 ' + title, '--prompt', prompt], check=True)
    else:
        for k, (t, _) in NEW.items():
            print(k, t)
