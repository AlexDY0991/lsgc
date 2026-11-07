# 2026 大事记长图 v8：简约清爽版。封面（用户图）→ 八件大事各一块 → 结尾。
# 每块画面上下羽化，融进一条连续的淡蓝底色；块与块之间是留给用户写字的安静区域（参考线版标出）。
# 过渡元素只在少数接缝出现、各不相同：云带、燕子、一次红绸、云海；其余接缝只靠颜色渐变。
# 用法：python3 -I build_v8.py && python3 -m http.server 8767 & node ../layout/render_long.js http://localhost:8767/long_v8.html out/long_v8.png
import numpy as np
from PIL import Image

PAPER = (238, 246, 251)          # 全图最淡的底色（淡蓝白）
BLOCKS = [  # (文件, 高, 上羽化, 下羽化, 标签)
    ('b0_cover', 1920, 0, 620, '封面'),
    ('b1_huanjie', 1440, 220, 260, '大事一 · 换届 / 党建'),
    ('b2_qianyue', 1440, 220, 260, '大事二 · 校企合作'),
    ('b3_qiaoqian', 1440, 220, 260, '大事三 · 乔迁焕新'),
    ('b4_ai', 1440, 220, 260, '大事四 · AI 创作大赛'),
    ('b5_hangzhou', 1440, 220, 260, '大事五 · 杭州环北 采批节'),
    ('b6_nanjing', 1440, 220, 260, '大事六 · 南京环北 设计大赛'),
    ('b7_yaou', 1440, 220, 260, '大事七 · 亚欧商厦 店庆 / MINISO LAND'),
    ('b8_guanguang', 1440, 220, 260, '大事八 · 亚欧国际 观光厅'),
    ('b9_end', 1920, 260, 0, '结尾'),
]
GAPS = [640, 600, 640, 600, 640, 600, 640, 600, 320]      # 块与块之间的写字区高度
DECO = ['cloudband', None, 'birds', None, None, 'silk', None, 'cloudsea', None]

def edge_color(path, top):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    band = a[:24] if top else a[-24:]
    return band.reshape(-1, 3).mean(0)

def mix(c, t=0.55):   # 往最淡的底色收一点，留白更"空"
    return np.array(c) * (1 - t) + np.array(PAPER) * t

# ---- 计算每块位置和底色关键点 ----
y, layout, stops = 0, [], []
for i, (name, h, ft, fb, label) in enumerate(BLOCKS):
    f = f'img/{name}.jpg'
    ct = mix(edge_color(f, True)) if i else edge_color(f, True)
    cb = mix(edge_color(f, False)) if name != 'b0_cover' else np.array(PAPER)
    layout.append((name, y, h, ft, fb, label)); stops += [(y, ct), (y + h, cb)]
    y += h
    if i < len(GAPS):
        y += GAPS[i]
TOTAL = y
# 底色条：1 像素宽的纵向渐变，按关键点插值
ys = np.arange(TOTAL)
sy = np.array([s[0] for s in stops]); sc = np.array([s[1] for s in stops])
col = np.stack([np.interp(ys, sy, sc[:, k]) for k in range(3)], 1)
Image.fromarray(np.repeat(col[:, None, :], 4, 1).astype(np.uint8)).save('img/bg_strip.png')

def img(src, x, y, w, extra=''):
    return f'<img class="L" src="img/{src}.png" style="left:{x}px; top:{y}px; width:{w}px; {extra}">'

def deco(kind, g0, g1):
    """g0/g1 = 写字区的上下沿（绝对 y）。"""
    if kind == 'cloudband':   # 封面底部 → 第一块：一条云带托住封面的山丘
        return (img('cloud_2', -200, g0 - 420, 640) + img('cloud_3', 300, g0 - 250, 380)
                + img('cloud_1', 560, g0 - 470, 620) + img('cloud_0', 860, g0 - 300, 420))
    if kind == 'birds':       # 两只燕子从写字区右上飞过
        return img('bird_0', 760, g0 + 60, 200, 'transform:rotate(-6deg);') + img('bird_2', 900, g0 + 170, 130)
    if kind == 'silk':        # 全图唯一的一条红绸，从写字区下沿斜穿进下一块
        return img('silk_0', -120, g1 + 10, 1300, 'transform:rotate(-12deg); opacity:.92; -webkit-mask-image:linear-gradient(90deg, transparent 0, #000 22%, #000 100%);')
    if kind == 'cloudsea':    # 下一块是云上的观光厅：云从写字区两侧漫进去
        return (img('cloud_3', -120, g1 - 160, 420, 'opacity:.9;') + img('cloud_1', 640, g1 - 200, 560, 'opacity:.9;'))
    return ''

CSS = f'''
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ width:1080px; height:{TOTAL}px; position:relative; overflow:hidden; background:url(img/bg_strip.png) 0 0/1080px {TOTAL}px no-repeat; }}
.b {{ position:absolute; left:0; width:1080px; }}
.b img {{ width:100%; height:100%; display:block; }}
.L {{ position:absolute; pointer-events:none; z-index:20; }}
.zone {{ position:absolute; display:none; z-index:30; }}
body.guide .zone {{ display:block; outline:3px dashed #2F6FD6; outline-offset:-3px; background:rgba(47,111,214,.07); }}
body.guide .zone span {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); background:#2F6FD6; color:#fff;
  font:600 26px/1.4 "Noto Sans CJK SC","WenQuanYi Zen Hei",sans-serif; padding:6px 18px; border-radius:6px; white-space:nowrap; }}
'''
parts, decos, zones = [], [], []
for i, (name, y0, h, ft, fb, label) in enumerate(layout):
    m = f'linear-gradient(to bottom, {"transparent 0, #000 %dpx" % ft if ft else "#000 0"}, {"#000 calc(100%% - %dpx), transparent 100%%" % fb if fb else "#000 100%"})'
    parts.append(f'<div class="b" style="top:{y0}px; height:{h}px; -webkit-mask-image:{m};"><img src="img/{name}.jpg"></div>')
    if i < len(GAPS):
        g0 = y0 + h; g1 = g0 + GAPS[i]
        decos.append(deco(DECO[i], g0, g1))
        nxt = layout[i + 1][5]
        zx, zw = (90, 640) if DECO[i] == 'birds' else (90, 900)
        if i == len(GAPS) - 1:      # 结尾前这段空白只做过渡，结尾文字写在结尾页的天空里
            continue
        zones.append(f'<div class="zone" style="left:{zx}px; top:{g0 + 40}px; width:{zw}px; height:{GAPS[i] - 80}px;"><span>{nxt} · 文字区</span></div>')
# 封面大标题区、结尾文字区
zones.append('<div class="zone" style="left:80px; top:70px; width:920px; height:620px;"><span>封面 · 大标题区</span></div>')
ey = layout[-1][1]
zones.append(f'<div class="zone" style="left:90px; top:{ey + 300}px; width:900px; height:560px;"><span>结尾 · 展望文字区</span></div>')

body = ''.join(parts) + ''.join(decos) + ''.join(zones)
for fn, cls in (('long_v8.html', ''), ('long_v8_guide.html', 'guide')):
    open(fn, 'w').write(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>2026 大事记长图 v8</title><style>{CSS}</style></head><body class="{cls}">{body}</body></html>')
print('total', TOTAL, [(l[0], l[1]) for l in layout])
