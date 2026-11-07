# 2026 大事记 v9：完全照「两会新观察｜人工智能+」的形式做。
#   long_v9.html          一条长图：开头标题块 → 八段（插画 + 过渡渐变区里的标题和文字）→ 结尾
#   long_v9_notext.html   同上，不排正文（只留 logo 和插画），给用户自己写字
#   poster_v9_1..8.html   单张海报 1080×3240：插画 + 白色毛笔大字 + 竖排标题
# 文字全部来自 text_v9.py（docx 原句），这里只做版式处理：数字/英文与汉字间的空格去掉、直引号换中文引号、
# 在逗号/顿号/分号处断行并去掉行尾的这些标点和句末句号（参考图的排法）。断行后逐条核对仍是 docx 原文。
# 用法（v8 目录）：/tmp/studio-tools/venv/bin/python -I build_v9.py（需要 jieba、pillow、numpy），然后 http.server 8768，node ../layout/render_long.js …
import re, html
import jieba
jieba.setLogLevel(60)
for _w in ['兰州财经大学', '浙江理工大学', '华润杭曜置地中心', '亚欧商厦', '杭州环北', '南京环北', '老门东', '治理基因', '品牌焕新', '空间即平台', '丽尚国潮', '媒体代表', '合作伙伴', '政府领导', '链接智力']:
    jieba.add_word(_w)
import numpy as np
from PIL import Image

exec(open('text_v9.py').read())
RAW = re.sub(r'\s+', ' ', open('../content_v2/content_1107.md').read().replace('\\"', '"').replace('\\', ''))
W = 1080
IH = 2520                      # 每段插画高（1080 宽）
GAP = 560                      # 段与段之间的渐变过渡区
FADE = 260                     # 插画上下羽化

def norm(t):
    t = re.sub(r'(?<=[一-鿿])\s+(?=[0-9A-Za-z"“])|(?<=[0-9A-Za-z"”])\s+(?=[一-鿿])', '', t)
    out, q = [], 0
    for ch in t:
        if ch == '"': out.append('“' if q % 2 == 0 else '”'); q += 1
        else: out.append(ch)
    return ''.join(out)

def lines(t, maxc=19):
    t = norm(t)
    parts = re.split(r'(?<=[，；：])', t)
    res = []
    for p in parts:
        p = p.strip()
        if not p: continue
        p = re.sub(r'[，、；。]$', '', p)
        while len(p) > maxc:                      # 太长：在词与词之间（jieba 分词）断开，优先顿号后，不切开引号和书名号
            n = -(-len(p) // maxc); target = len(p) / n
            bounds, pos = [], 0
            for tok in jieba.cut(p):
                pos += len(tok); bounds.append(pos)
            def ok(i):
                return (0 < i < len(p) and p[:i].count('《') == p[:i].count('》') and p[:i].count('“') == p[:i].count('”')
                        and not re.match(r'[0-9.]', p[i - 1]) and p[i] != '、' and len(p) - i >= 3
                        and not (p[i - 1] == '、' and len(re.split(r'[、]', p[i:])[0]) <= 2))   # 不拆短词并列（潮启、潮力…）
            cands = [b for b in bounds if ok(b) and b <= maxc + 5]
            cut = min(cands, key=lambda b: (abs(b - target) + (4 if b > maxc else 0), -b)) if cands else maxc
            res.append(re.sub(r'、$', '', p[:cut])); p = p[cut:]
        res.append(p)
    return res

def check(src, ls):   # 断行后的文字去掉标点、空格、引号后，必须和 docx 原句一致，且原句在 docx 里
    strip = lambda x: re.sub(r'[\s，、；。“”"]', '', x)
    assert src in RAW, src[:30]
    assert strip(''.join(ls)) == strip(src), (src[:30], ls)
    print('  ' + ' / '.join(ls))

def edge_rgb(path, top):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    return a[:30].reshape(-1, 3).mean(0) if top else a[-30:].reshape(-1, 3).mean(0)

def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
def hexc(c): return '#%02x%02x%02x' % tuple(int(max(0, min(255, v))) for v in c)
def ink(c): return '#ffffff' if lum(c) < 165 else '#1d3557'

CSS = '''
@font-face { font-family:"NotoSerifSC"; src:url("../layout/fonts/NotoSerifSC.ttf"); font-weight:200 900; }
@font-face { font-family:"KingHwa"; src:url("../layout/fonts/KingHwa_OldSong.ttf"); }
* { box-sizing:border-box; margin:0; padding:0; }
body { width:1080px; position:relative; overflow:hidden; font-family:"NotoSerifSC",serif; }
.L { position:absolute; left:0; width:1080px; }
.txt { position:absolute; left:0; width:1080px; text-align:center; font-weight:800; letter-spacing:1px; }
.txt p { font-size:31px; line-height:1.62; }
.txt .gap { height:28px; }
.ttl { font-family:"KingHwa","NotoSerifSC",serif; font-weight:normal; font-size:56px; line-height:1.3; letter-spacing:4px; }
.grp { font-size:24px; letter-spacing:12px; font-weight:600; opacity:.85; margin-bottom:14px; }
.panel { display:inline-block; padding:30px 46px; border-radius:10px; background:rgba(255,255,255,.62); box-shadow:0 0 0 1px rgba(255,255,255,.75) inset; }
.dots { position:absolute; inset:0; pointer-events:none;
  background-image:radial-gradient(circle, rgba(255,255,255,.95) 0 3px, rgba(255,255,255,.35) 4px, transparent 9px);
  background-size:260px 330px; background-position:40px 60px; opacity:.55; }
'''

def text_block(top_y, items, color, panel=False, size=None):
    body = ''.join('<div class="gap"></div>' if x is None else f'<p>{html.escape(x)}</p>' for x in items)
    if panel:
        body = f'<div class="panel">{body}</div>'
    st = f'font-size:{size}px;' if size else ''
    return f'<div class="txt" style="top:{top_y}px; color:{color}; {st}">{body}</div>'

def build_long(with_text):
    parts, y = [], 0
    imgs = [f'img9/i{i}.jpg' for i in range(1, 9)]
    tops = [edge_rgb(f, True) for f in imgs]; bots = [edge_rgb(f, False) for f in imgs]
    stops = []
    # 开头：标题块（logo + 年度大事记）
    intro_h = 760
    stops += [(0, tops[0] * .78 + np.array([30, 60, 120]) * .22), (intro_h + FADE, tops[0])]
    parts.append(f'<img src="../content_v2/media/image4.png" style="position:absolute; left:{(W - 520) // 2}px; top:250px; width:520px; filter:brightness(0) invert(1);">')
    parts.append(f'<div class="txt" style="top:410px; color:#fff;"><div class="ttl" style="font-size:96px; letter-spacing:10px;">2026</div><div class="ttl" style="font-size:64px; letter-spacing:22px; margin-top:6px;">年度大事记</div></div>')
    y = intro_h
    for i, s in enumerate(SECTIONS):
        if i > 0:
            g0 = y; y += GAP
            stops += [(g0 - FADE, bots[i - 1]), (y + FADE, tops[i])]
        # 插画
        m = f'linear-gradient(to bottom, transparent 0, #000 {FADE}px, #000 calc(100% - {FADE}px), transparent 100%)'
        parts.append(f'<div class="L" style="top:{y}px; height:{IH}px; -webkit-mask-image:{m};"><img src="{imgs[i]}" style="width:100%; height:100%; display:block;"></div>')
        if with_text:
            # 标题 + 上段文字：放在本段插画上方的过渡区（底色 = 本段顶部主色）
            items_top = []
            for t in s['top']:
                ls = lines(t); check(t, ls); items_top += ls + [None]
            col = ink(tops[i])
            ty = y - (GAP if i > 0 else 0) + 60 if i > 0 else y - 40
            tt = norm(s['title'])
            tt_html = html.escape(tt).replace('MINSON', '<br><span style="font-size:42px">MINSON') + ('</span>' if 'MINSON' in tt else '')
            head = f'<div class="txt" style="top:{ty}px; color:{col};"><div class="grp">{html.escape(s["group"])}</div><div class="ttl">{tt_html}</div></div>'
            parts.append(head)
            if items_top:
                parts.append(text_block(ty + (250 if 'MINSON' in s['title'] else 190), items_top[:-1], col))
            # 下段文字：插画下部的浅色留白区，压在半透明白色面板上（参考图的做法）
            items_b = []
            for t in s['bottom']:
                ls = lines(t); check(t, ls); items_b += ls + [None]
            if items_b:
                parts.append(text_block(y + int(IH * 0.70), items_b[:-1], '#1d3557', panel=True))
        y += IH
    # 结尾
    end_h = 900
    stops += [(y - FADE, bots[-1]), (y + end_h, tops[-1] * .6 + np.array([40, 120, 150]) * .4)]
    parts.append(f'<img src="../content_v2/media/image5.png" style="position:absolute; left:{(W - 150) // 2}px; top:{y + 330}px; width:150px; filter:brightness(0) invert(1);">')
    parts.append(f'<img src="../content_v2/media/image4.png" style="position:absolute; left:{(W - 420) // 2}px; top:{y + 520}px; width:420px; filter:brightness(0) invert(1);">')
    y += end_h
    # 底色条
    ys = np.arange(y); sy = np.array([s_[0] for s_ in stops]); sc = np.array([s_[1] for s_ in stops])
    order = np.argsort(sy, kind='stable'); sy, sc = sy[order], sc[order]
    col = np.stack([np.interp(ys, sy, sc[:, k]) for k in range(3)], 1)
    Image.fromarray(np.repeat(col[:, None, :], 4, 1).astype(np.uint8)).save('img9/bg_long.png')
    return y, ''.join(parts)

for fn, wt in (('long_v9.html', True), ('long_v9_notext.html', False)):
    H, body = build_long(wt)
    open(fn, 'w').write(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>2026 大事记 v9</title><style>{CSS}'
                        f'body{{height:{H}px; background:url(img9/bg_long.png) 0 0/1080px {H}px no-repeat;}}</style></head>'
                        f'<body><div class="dots" style="height:{H}px"></div>{body}</body></html>')
    print(fn, H)

# ---------- 单张海报 1080×3240 ----------
PH = 3240
def deepen(c, k=.72):   # 海报下部用更饱和、更深的主色，让白色毛笔字看得清
    c = np.array(c, float); g = c.mean()
    return np.clip((c - g) * 1.35 + g * k, 0, 255)
for i, s in enumerate(SECTIONS, 1):
    f = f'img9/i{i}.jpg'; top = edge_rgb(f, True); deep = deepen(top)
    t = norm(s['title']); halves = [x for x in re.split(r'，', t) if x]
    if len(halves) == 1 and 'MINSON' in t: halves = ['三十二载融金城', 'MINSON LAND甘青宁首店开业']
    vt = ''.join(f'<div style="font-size:{34 if len(h) < 12 else 26}px; letter-spacing:4px; margin-top:150px; margin-left:6px;">「{html.escape(h)}」</div>' for h in halves)
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>海报 {i}</title><style>{CSS}
body {{ height:{PH}px; background:linear-gradient(to bottom, {hexc(top)} 0, {hexc(top)} 40%, {hexc(deep)} 100%); }}
.calli {{ position:absolute; left:20px; top:1880px; width:1040px; height:1330px; object-fit:contain; filter:drop-shadow(0 6px 24px rgba(0,0,0,.18)); }}
.vt {{ position:absolute; left:70px; top:2560px; writing-mode:vertical-rl; color:#fff; font-weight:900; text-shadow:0 2px 10px rgba(0,0,0,.18); }}
.vt .big {{ font-size:76px; margin-left:10px; letter-spacing:8px; font-weight:900; }}
</style></head><body>
<div class="L" style="top:0; height:{IH}px; -webkit-mask-image:linear-gradient(to bottom, #000 0, #000 62%, transparent 100%);"><img src="{f}" style="width:100%; height:100%; display:block;"></div>
<div class="L" style="top:1500px; height:{PH - 1500}px; background:linear-gradient(to bottom, transparent 0, {hexc(deep)}cc 45%, {hexc(deep)} 100%);"></div>
<div class="dots" style="height:{PH}px; opacity:.4"></div>
<img class="calli" src="img9/calli_{i}.png">
<div class="vt"><div class="big">丽尚国潮</div>{vt}</div>
<img src="../content_v2/media/image4.png" style="position:absolute; right:60px; top:{PH - 110}px; width:220px; filter:brightness(0) invert(1); opacity:.9;">
</body></html>'''
    open(f'poster_v9_{i}.html', 'w').write(page)
print('posters ok')
