# 生成 2026 大事记长图 v4 的排版页。正文逐字取自 ../content_2026_raw.md（用户 docx）。
import re, html
raw = open('../content_2026_raw.md').read().replace('\\', '')
L = [l.strip() for l in raw.split('\n') if l.strip()]
esc = html.escape

INTRO = ["回望 2026，", "丽尚国潮以换届接力稳舵治理，", "以乔迁自持总部、品牌焕新开启新篇；",
         "校企合作从东海之滨延伸至陇原大地，", "首届 AI 视频创作大赛点燃全员共创热情；",
         "杭州、南京、兰州三地业务各展新貌。", "以宋韵为根，以竹魂为志，", "把国潮写进城市，写进生活。"]
OUTRO = ["展望 2027，", "丽尚国潮将继续以「引领时尚消费　传播国潮文化」为使命，",
         "向着「中国领先的美丽时尚消费产业平台", "和国潮文化传播平台」坚定前行。"]

CH = [  # 编号, 篇, 标题第1行, 第2行, 日期, 画面, 正文段落（docx 行号）, 待补说明
  ("一", "集团", "换届接力稳舵", "党建引领", "3月", "c1_wenduo", [2], "党建引领 · 内容待补"),
  ("二", "集团", "校企双向奔赴", "产学四维共生", "", "c2_gongsheng", [5, 6], None),
  ("三", "集团", "乔迁筑巢引凤", "焕新铸魂扬帆", "6月5日", "c3_qiaoqian", [8, 9], None),
  ("四", "集团", "AI 执笔绘视界", "全员共创燃国潮", "3月30日", "c4_zhibi", [11], None),
  ("五", "杭州环北", "采批节", "双平台", "", "c5_hangzhou", [], "采批节 · 双平台 · 内容待补"),
  ("六", "南京环北", "青春设计聚金陵", "国潮大秀映城墙", "7月29日", "c6_jinling", [16], None),
  ("七", "亚欧商厦", "三十二载融金城", "MINSON LAND甘青宁首店开业", "", "c7_jincheng", [19, 20], None),
  ("八", "亚欧国际", "观光厅招商成功", "", "", "c8_guanguang", [], "观光厅招商成功 · 内容待补"),
]
# 核对：标题拼起来必须和 docx 标题一致
for no, grp, t1, t2, *_ in CH:
    src = next(l for l in L if l.startswith(no + '、'))
    norm = lambda x: x.replace('，', '').replace(' ', '')
    assert norm(src[2:]) == norm(t1 + t2), (src, t1, t2)

def fit(t):
    # 长标题缩字号，保证一行放下（可用宽度约 900px，字距 8px）
    w = sum(0.55 if ord(c) < 128 else 1.0 for c in t)
    return '' if w <= 11 else f' style="font-size:{int(860 / w) - 8}px"'

def chapter(no, grp, t1, t2, date, img, paras, todo):
    body = ''.join(f'<p>{esc(L[i])}</p>' for i in paras)
    if todo: body += f'<div class="todo">{esc(todo)}</div>'
    return f'''
<section class="chap">
  <div class="orn"><span></span><i>{esc(grp)}</i><span></span></div>
  <header class="head">
    <div class="seal">{no}</div>
    <h2><span class="t1"{fit(t1)}>{esc(t1)}</span>{f'<span class="t2"{fit(t2)}>{esc(t2)}</span>' if t2 else ''}</h2>
    {f'<div class="date">{esc(date)}</div>' if date else ''}
  </header>
  <img class="panel" src="img/v4/{img}.jpg" alt="">
  <div class="body">{body}</div>
</section>'''

page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>2026 大事记长图 v4</title>
<style>
@font-face {{ font-family:"NotoSerifSC"; src:url("fonts/NotoSerifSC.ttf"); font-weight:200 900; }}
:root {{ --paper:#F8F3E9; --zhu:#B3261E; --ink:#2A201A; --ink2:#6A5A4C; --gold:#B8924A; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ width:1080px; background:var(--paper); color:var(--ink); font-family:"NotoSerifSC",serif; position:relative; }}
.grain {{ position:absolute; inset:0; pointer-events:none; mix-blend-mode:multiply; opacity:.22; z-index:5;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='360' height='360'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .45  0 0 0 0 .38  0 0 0 0 .3  0 0 0 .5 0'/></filter><rect width='360' height='360' filter='url(%23n)'/></svg>"); }}
.panel {{ display:block; width:1080px; height:1920px;
  -webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 150px, #000 calc(100% - 200px), transparent 100%); }}
/* 开篇 */
.open {{ position:relative; }}
.open .logo {{ position:absolute; left:70px; top:76px; width:290px; }}
.open .yr {{ position:absolute; left:70px; top:150px; font-size:120px; font-weight:800; color:var(--zhu); letter-spacing:2px; line-height:1; }}
.open .yr small {{ display:block; font-size:30px; font-weight:500; letter-spacing:22px; color:var(--ink2); margin:16px 0 0 4px; }}
.verse {{ text-align:center; font-size:32px; line-height:2.1; letter-spacing:2px; color:var(--ink); }}
.verse.intro {{ margin:-180px 0 0; padding:0 80px 60px; position:relative; }}
/* 章节 */
.chap {{ padding-top:180px; }}
.orn {{ display:flex; align-items:center; justify-content:center; gap:26px; color:var(--gold); }}
.orn span {{ width:180px; height:1px; background:linear-gradient(90deg, transparent, var(--gold)); }}
.orn span:last-child {{ background:linear-gradient(270deg, transparent, var(--gold)); }}
.orn i {{ font-style:normal; font-size:28px; letter-spacing:16px; font-weight:600; }}
.head {{ text-align:center; margin-top:46px; }}
.seal {{ display:inline-block; width:104px; height:104px; line-height:100px; background:var(--zhu); color:#FBEBD5; font-size:64px; font-weight:900; border-radius:8px;
  box-shadow: inset 0 0 0 4px #B3261E, inset 0 0 0 7px #F2C9A0; }}
.head h2 {{ margin-top:34px; font-weight:900; line-height:1.28; }}
.head .t1 {{ display:block; font-size:68px; letter-spacing:8px; color:var(--ink); }}
.head .t2 {{ display:block; font-size:68px; letter-spacing:8px; color:var(--zhu); }}
.head .date {{ display:inline-block; margin-top:26px; padding:6px 30px; font-size:30px; font-weight:700; letter-spacing:4px; color:var(--zhu);
  border-top:1px solid var(--gold); border-bottom:1px solid var(--gold); }}
.chap .panel {{ margin-top:-40px; }}
.body {{ margin:-150px 110px 0; position:relative; }}
.body p {{ font-size:31px; line-height:1.95; text-align:justify; text-indent:2em; margin-bottom:28px; }}
.todo {{ margin:30px auto 0; width:640px; padding:44px 0; text-align:center; border:2px dashed var(--gold); border-radius:16px; color:var(--ink2); font-size:28px; letter-spacing:6px; }}
/* 结尾 */
.end {{ position:relative; padding-top:200px; }}
.end .verse {{ position:absolute; left:0; right:0; top:330px; z-index:2; }}
.end .logo {{ display:block; width:320px; margin:40px auto 140px; position:relative; }}
</style></head><body><div class="grain"></div>
<section class="open">
  <img class="panel" src="img/v4/p0_kaipian.jpg" alt="">
  <img class="logo" src="img/logo_wordmark.png" alt="丽尚国潮">
  <div class="yr">2026<small>年度大事记</small></div>
</section>
<div class="verse intro">{"<br>".join(esc(x) for x in INTRO)}</div>
{''.join(chapter(*c) for c in CH)}
<section class="end">
  <img class="panel" src="img/v4/c9_guochao.jpg" alt="">
  <div class="verse">{"<br>".join(esc(x) for x in OUTRO)}</div>
  <img class="logo" src="img/logo_wordmark.png" alt="丽尚国潮">
</section>
</body></html>'''
open('long_v4.html', 'w').write(page)
print('ok', len(page))
