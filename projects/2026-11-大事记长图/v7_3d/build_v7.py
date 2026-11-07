# 2026 大事记长图 v7（3D 金色版）：第一页 = 用户定稿图；之后每件大事一页，结尾一页。
# 页与页上下叠接，每个接缝换一种过渡（云海、飘带、阳光、斜向渐变、云边蒙版、同城延续）。
# 文字全部留给用户自己写：参考线版（long_v7_guide.html）标出每页的文字区。
# 用法：python3 build_v7.py && python3 -m http.server 8766 & node ../layout/render_long.js http://localhost:8766/long_v7.html out/long_v7.png
import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1920
PANELS = ['p00_page1', 'p01_wenduo', 'p02_xiaoqi', 'p03_qiaoqian', 'p04_ai', 'p05_hangzhou',
          'p06_nanjing', 'p07_yaou', 'p08_guanguang', 'p09_end']
LABELS = ['封面 · 大标题区', '大事一 · 换届 / 党建', '大事二 · 校企合作', '大事三 · 乔迁焕新', '大事四 · AI 创作大赛',
          '大事五 · 杭州环北 采批节 / 双平台', '大事六 · 南京环北 设计大赛', '大事七 · 亚欧商厦 店庆', '大事八 · 亚欧国际 观光厅', '结尾 · 展望']
# 每页的文字区（页内坐标 x, y, w, h），都落在天空里
TEXT = [(80, 70, 920, 640)] + [(90, 300, 900, 380)] * 8 + [(90, 300, 900, 420)]

# 接缝：(与上一页的重叠高度, 蒙版类型, 装饰)
SEAMS = [
    (380, 'linear', 'cloudbank'),     # 封面 → 一：封面底部山丘没有云，用一排云海托住
    (300, 'linear', 'ribbon_s'),      # 一 → 二：一条金色 S 形飘带穿过接缝
    (300, 'linear', 'sunglow'),       # 二 → 三：阳光渐变
    (340, 'diag', 'spiral'),          # 三 → 四：斜向渐变 + 螺旋飘带
    (360, 'cloudedge', 'cloudline'),  # 四 → 五：云朵形状的蒙版边缘 + 沿边一排小云
    (300, 'linear', 'cloudbank2'),    # 五 → 六：云海 + 金色光点
    (300, 'linear', 'ribbon_long'),   # 六 → 七：横穿整幅的长飘带
    (460, 'linear', 'none'),          # 七 → 八：同为兰州黄河，长渐变让城市直接延续
    (360, 'linear', 'cloudsea'),      # 八 → 结尾：大片云海 + 阳光
]

# 云边蒙版（白 = 显示下一页）
def cloud_edge_mask(h, path):
    rng = np.random.default_rng(3)
    xs = np.arange(W)
    edge = np.zeros(W)
    for k, amp in ((3, 70), (7, 40), (15, 18), (31, 8)):
        ph = rng.random() * 6.28
        edge += amp * np.abs(np.sin(xs / W * np.pi * k + ph))      # 鼓包状，像云朵轮廓
    edge = h * 0.62 - edge
    y = np.arange(h)[:, None]
    a = np.clip((y - edge[None, :]) / 120 + 0.5, 0, 1)
    im = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))
    out = Image.new('RGBA', (W, h), (255, 255, 255, 0)); out.putalpha(im); out.save(path)

def img(src, x, y, w, extra=''):
    return f'<img class="L" src="{src}" style="left:{x}px; top:{y}px; width:{w}px; {extra}">'

def deco(kind, s):
    """s = 接缝中线的绝对 y。"""
    c = 'img/cloud_{}.png'.format
    r = 'img/ribbon_{}.png'.format
    if kind == 'cloudbank':
        return (img(c(1), -160, s - 250, 640) + img(c(4), 330, s - 190, 620) + img(c(0), 700, s - 320, 560)
                + img(r(1), -80, s - 420, 1240, 'transform:rotate(-6deg);'))
    if kind == 'ribbon_s':
        return img(r(0), 40, s - 560, 1000, 'transform:rotate(12deg);') + img(c(2), 760, s - 200, 380)
    if kind == 'sunglow':
        return (f'<div class="L glow" style="left:-200px; top:{s - 420}px; width:1480px; height:840px;"></div>'
                + img(c(4), -120, s - 180, 460) + img(c(2), 820, s - 230, 360))
    if kind == 'spiral':
        return img(r(2), 40, s - 420, 380, 'transform:rotate(-14deg);') + img(c(3), 640, s - 360, 520)
    if kind == 'cloudbank2':
        return (img(c(0), -120, s - 250, 520) + img(c(3), 360, s - 330, 480) + img(c(1), 700, s - 220, 520)
                + f'<div class="L sparkle" style="left:0; top:{s - 300}px; width:1080px; height:600px;"></div>')
    if kind == 'ribbon_long':
        return img(r(1), -140, s - 500, 1380, 'transform:rotate(8deg);') + img(c(2), -60, s - 170, 380)
    if kind == 'cloudline':
        return (img(c(1), -200, s - 210, 560) + img(c(2), 250, s - 190, 420) + img(c(4), 560, s - 200, 560)
                + img(c(0), 860, s - 240, 420))
    if kind == 'cloudsea':
        return (f'<div class="L glow" style="left:-100px; top:{s - 380}px; width:1280px; height:760px;"></div>'
                + img(c(4), -180, s - 240, 700) + img(c(0), 360, s - 330, 600) + img(c(1), 640, s - 210, 640))
    return ''

cloud_edge_mask(360, 'img/mask_cloudedge.png')

CSS = '''
* { box-sizing:border-box; margin:0; padding:0; }
body { width:1080px; position:relative; overflow-x:hidden; background:#EAF4FB; }
.p { position:absolute; left:0; width:1080px; height:1920px; }
.p img.bg { width:100%; height:100%; display:block; }
.L { position:absolute; pointer-events:none; }
.glow { background:radial-gradient(ellipse at center, rgba(255,236,180,.85) 0%, rgba(255,230,170,.45) 35%, rgba(255,230,170,0) 70%); mix-blend-mode:screen; }
.sparkle { background-image:radial-gradient(circle, rgba(255,240,190,.95) 0 2px, transparent 3px), radial-gradient(circle, rgba(255,220,140,.8) 0 1.5px, transparent 2.5px);
  background-size:140px 120px, 90px 110px; background-position:20px 30px, 60px 70px; mix-blend-mode:screen;
  -webkit-mask-image:radial-gradient(ellipse at center, #000 30%, transparent 70%); }
.zone { position:absolute; display:none; }
body.guide .zone { display:block; outline:3px dashed #2F6FD6; outline-offset:-3px; background:rgba(47,111,214,.08); }
body.guide .zone span { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); background:#2F6FD6; color:#fff;
  font:600 26px/1.4 "Noto Sans CJK SC","WenQuanYi Zen Hei",sans-serif; padding:6px 18px; border-radius:6px; white-space:nowrap; }
'''

parts, decos, y = [], [], 0
tops = []
for i, name in enumerate(PANELS):
    if i == 0:
        style = ''
    else:
        ov, mtype, kind = SEAMS[i - 1]
        y -= ov
        if mtype == 'linear':
            style = f'-webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 {ov}px);'
        elif mtype == 'diag':
            style = (f'-webkit-mask-image:linear-gradient(172deg, transparent 0, transparent {int(ov*0.15)}px, #000 {int(ov*1.15)}px);')
        else:  # cloudedge
            style = ('-webkit-mask-image:url(img/mask_cloudedge.png), linear-gradient(#000, #000);'
                     f'-webkit-mask-size:1080px {ov}px, 1080px {H - ov}px; -webkit-mask-position:0 0, 0 {ov}px; -webkit-mask-repeat:no-repeat;')
        decos.append(deco(kind, y + ov // 2))
    tops.append(y)
    tx, ty, tw, th = TEXT[i]
    parts.append(f'<div class="p" style="top:{y}px; z-index:{i + 1}; {style}"><img class="bg" src="img/{name}.jpg">'
                 f'<div class="zone" style="left:{tx}px; top:{ty}px; width:{tw}px; height:{th}px;"><span>{LABELS[i]} · 文字区</span></div></div>')
    y += H
total = y
body = ''.join(parts) + f'<div style="position:absolute; left:0; top:0; width:1080px; height:{total}px; z-index:50; pointer-events:none;">{"".join(decos)}</div>'
for fn, cls in (('long_v7.html', ''), ('long_v7_guide.html', 'guide')):
    open(fn, 'w').write(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>2026 大事记长图 v7</title><style>{CSS}</style></head>'
                        f'<body class="{cls}" style="height:{total}px">{body}</body></html>')
print('total height', total, 'panel tops', tops)
