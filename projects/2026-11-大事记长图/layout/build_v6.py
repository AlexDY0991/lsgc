# 2026 大事记长图 v6：白金色调，只保留大标题（开篇「大事记」+ 各章标题），其余文字位置留空给用户自己填。
# 过渡每段换一种传统形制：卷轴、折扇、月洞窗、海棠窗、长卷、团扇、城门拱券、宝瓶门、八角窗、挂轴。
# 用法：python3 build_v6.py  -> long_v6.html（成品）和 long_v6_guide.html（带留白区标注的参考线版）
import html
esc = html.escape

def zone(h, label, w=840, extra=''):
    """留白区：半透明白卡 + 金色细线 + 回纹角花；参考线版会显示 label。"""
    return f'''<div class="zone" style="width:{w}px; height:{h}px; {extra}" data-label="{esc(label)}">
      <img class="corner tl" src="img/v5/orn_04.png"><img class="corner tr" src="img/v5/orn_03.png"></div>'''

def head(no, t1, t2, align='center', slot='篇名 · 日期', sep='，'):
    # sep：标题两半之间原文用的分隔符（docx 里第五章是空格）
    t = f'「{esc(t1)}{sep}<br>{esc(t2)}」' if t2 else f'「{esc(t1)}」'
    return f'''<div class="head {align}">
      <div class="badge"><img class="cloud" src="img/v5/orn_10.png"><div class="seal">{no}</div></div>
      <div class="ttl">{t}</div>
      <div class="slot" data-label="{esc(slot)}"></div>
    </div>'''

def win(frame, scene, w, extra='', pos='50% 50%'):
    return f'''<div class="win" style="width:{w}px; {extra}">
      <img class="frame-sizer" src="img/v6/{frame}.png">
      <div class="scene" style="-webkit-mask-image:url(img/v6/{frame}_in.png)"><img src="img/v6/{scene}" style="object-position:{pos}"></div>
      <img class="frame" src="img/v6/{frame}.png"></div>'''

def L(src, style, cls=''):
    return f'<img class="L {cls}" src="{src}" style="{style}">'

CSS = '''
@font-face { font-family:"NotoSerifSC"; src:url("fonts/NotoSerifSC.ttf"); font-weight:200 900; }
:root { --gold:#B8955A; --ink:#4A3B2E; --ink2:#8A7660; --red:#A8332B; }
* { box-sizing:border-box; margin:0; padding:0; }
body { width:1080px; position:relative; overflow-x:hidden; font-family:"NotoSerifSC",serif; color:var(--ink);
  background:#F6F0E4 url(img/v5/tex_ab.jpg) 0 0/1080px 3840px repeat-y; }
.L { position:absolute; pointer-events:none; }
.mul { mix-blend-mode:multiply; }
.fade-y { -webkit-mask-image:linear-gradient(to bottom, transparent, #000 25%, #000 75%, transparent); }
.fade-x { -webkit-mask-image:linear-gradient(to right, transparent, #000 20%, #000 80%, transparent); }
section { position:relative; }
/* 标题块 */
.head { position:relative; text-align:center; }
.head.left { text-align:left; padding-left:96px; }
.head.left .badge .cloud, .head.left .badge .seal { left:84px; transform:none; }
.head.left .badge .seal { left:170px; }
.badge { position:relative; height:180px; }
.badge .cloud { position:absolute; left:50%; top:0; width:420px; transform:translateX(-50%); }
.badge .seal { position:absolute; left:50%; top:60px; transform:translateX(-50%); width:84px; height:84px; line-height:80px; text-align:center;
  background:var(--red); color:#F8E9D2; font-size:50px; font-weight:800; border-radius:10px; box-shadow:inset 0 0 0 3px var(--red), inset 0 0 0 5px #EBC9A0; }
.ttl { margin-top:22px; color:var(--red); font-weight:700; font-size:54px; line-height:1.45; letter-spacing:6px; }
.slot { height:64px; margin-top:14px; }
/* 窗、扇、门：场景在下、框在上 */
.win { position:relative; margin:0 auto; }
.win .frame-sizer { display:block; width:100%; visibility:hidden; }
.win .scene { position:absolute; inset:0; -webkit-mask-size:100% 100%; -webkit-mask-repeat:no-repeat; }
.win .scene img { width:100%; height:100%; object-fit:cover; }
.win .frame { position:absolute; inset:0; width:100%; }
/* 卷轴（代码画轴杆） */
.hscroll { position:relative; margin:0 auto; }
.hscroll .paper { position:absolute; inset:0 28px; background:linear-gradient(#FBF7EE, #F7F0E2); box-shadow:0 0 0 1px rgba(184,149,90,.35), 0 18px 40px -26px rgba(120,90,40,.45); }
.hscroll .paper img { width:100%; height:100%; object-fit:cover; display:block; }
.hscroll .rod { position:absolute; top:-26px; bottom:-26px; width:30px; border-radius:15px;
  background:linear-gradient(90deg, #4A2E1E, #8A5A3A 45%, #3C2416); }
.hscroll .rod::before, .hscroll .rod::after { content:""; position:absolute; left:-4px; width:38px; height:30px; border-radius:8px;
  background:linear-gradient(90deg, #9C7A3C, #F1D48E 50%, #8C6A2E); }
.hscroll .rod::before { top:-14px; } .hscroll .rod::after { bottom:-14px; }
.hscroll .rod.l { left:0; } .hscroll .rod.r { right:0; }
/* 留白区 */
.zone { position:relative; margin:0 auto; background:rgba(255,253,248,.66); border-radius:6px;
  box-shadow:0 0 0 1px rgba(184,149,90,.35), 0 0 0 10px rgba(255,253,248,.3), 0 0 0 11px rgba(184,149,90,.2); }
.zone .corner { position:absolute; width:92px; } .zone .tl { left:-8px; top:-8px; } .zone .tr { right:-8px; top:-8px; }
/* 参考线版 */
body.guide .zone, body.guide .slot, body.guide .blank { outline:3px dashed #3C7BD9; outline-offset:-3px; }
body.guide [data-label]::after { content:attr(data-label); position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
  background:#3C7BD9; color:#fff; font-size:24px; padding:6px 16px; border-radius:6px; white-space:nowrap; font-weight:600; }
body.guide .slot { position:relative; width:560px; margin-left:auto; margin-right:auto; }
body.guide .head.left .slot { margin-left:0; }
'''

parts = []
# ---------- 开篇 ----------
parts.append('''
<section style="height:1920px;">
  <img src="img/v5/open.jpg" style="display:block; width:1080px; height:1920px; -webkit-mask-image:linear-gradient(to bottom, #000 82%, transparent);">
  <img class="L" src="img/logo_wordmark.png" style="left:72px; top:80px; width:270px;">
  <div class="L blank" style="left:66px; top:150px; width:360px; height:150px;" data-label="年份 / 副标题"></div>
</section>''')
# ---------- 导语：横向展开的卷轴 ----------
parts.append(f'''
<section style="margin-top:-260px; padding-bottom:40px;">
  {L("img/v5/orn_01.png", "left:470px; top:-40px; width:140px;")}
  <div class="hscroll" style="width:940px; height:640px; margin-top:110px;">
    <div class="paper blank" data-label="导语 · 约 8 行（每行 18 字内）"></div><div class="rod l"></div><div class="rod r"></div>
  </div>
</section>''')
# ---------- 过渡：千里江山 + 仙鹤 ----------
parts.append(f'''<section style="height:330px;">
  {L("img/v5/shan_1c.jpg", "left:-300px; top:-40px; width:1700px; opacity:.5;", "mul fade-y")}
  {L("img/v5/orn_08.png", "left:660px; top:30px; width:280px;")}
</section>''')
# ---------- 第一章：折扇 ----------
parts.append(f'''
<section>
  {head("一", "换届接力稳舵", "党建引领")}
  {win("f1_2", "s1_wenduo.png", 960, "margin-top:10px; transform:rotate(-2deg);", "50% 40%")}
  {L("img/v5/orn_00.png", "left:-40px; top:520px; width:330px; opacity:.9;")}
  <div style="margin-top:-70px;">{zone(1000, "正文区 · 换届 约 160 字 + 党建引领（待补）", extra="margin-top:0;")}</div>
</section>''')
# ---------- 第二章：月洞窗（图在前，压住上一章留白区下沿） ----------
parts.append(f'''
<section style="margin-top:-90px;">
  {L("img/v5/orn_06.png", "right:-30px; top:120px; width:300px;")}
  {L("img/v5/bamboo.jpg", "right:-300px; top:700px; width:560px; opacity:.28;", "mul fade-y")}
  {win("f2_0", "s2_gongsheng.jpg", 700, "margin-left:70px;")}
  {head("二", "校企双向奔赴", "产学四维共生")}
  {zone(1460, "正文区 · 两段 约 580 字")}
</section>''')
# ---------- 过渡：太阳 + 梅枝 + 雾 ----------
parts.append(f'''<section style="height:300px;">
  {L("img/v5/orn_07.png", "left:60px; top:20px; width:300px; opacity:.9;")}
  {L("img/v5/orn_02.png", "left:520px; top:150px; width:460px; opacity:.85;")}
</section>''')
# ---------- 第三章：海棠窗 ----------
parts.append(f'''
<section>
  {head("三", "乔迁筑巢引凤", "焕新铸魂扬帆")}
  <div style="position:relative; width:760px; height:912px; margin:10px auto 0;">
    <div style="position:absolute; inset:0; -webkit-mask-image:url(img/v5/mask_haitang.png); -webkit-mask-size:100% 100%;"><img src="img/v5/ch3_scene.jpg" style="width:100%; height:100%; object-fit:cover;"></div>
    <img src="img/v5/line_haitang.png" style="position:absolute; left:-14px; top:-14px; width:788px; height:940px;">
    {L("img/v5/orn_05.png", "right:-170px; top:-50px; width:330px;")}
    {L("img/v5/orn_09.png", "left:-210px; top:360px; width:300px; transform:scaleX(-1);")}
  </div>
  <div style="margin-top:-40px;">{zone(1040, "正文区 · 两段 约 380 字")}</div>
</section>''')
# ---------- 第四章：横向长卷（图在前，跨在两章交界上） ----------
parts.append(f'''
<section style="margin-top:-60px;">
  <div class="hscroll" style="width:1000px; height:560px;">
    <div class="paper"><img src="img/v6/s4_zhibi.jpg"></div><div class="rod l"></div><div class="rod r"></div>
  </div>
  {L("img/v5/orn_01.png", "left:40px; top:470px; width:150px;")}
  <div style="height:60px"></div>
  {head("四", "AI 执笔绘视界", "全员共创燃国潮")}
  {zone(900, "正文区 · 约 330 字")}
</section>''')
# ---------- 第五章：团扇（右侧斜挂，标题靠左） ----------
parts.append(f'''
<section style="padding-top:80px;">
  {L("img/v5/shan_1e.jpg", "left:-500px; top:-20px; width:1900px; opacity:.42;", "mul fade-y")}
  <div style="position:absolute; right:40px; top:40px; width:400px; transform:rotate(8deg);">{win("f1_3", "s5_hangzhou.jpg", 400)}</div>
  <div style="height:260px"></div>
  {head("五", "采批节", "双平台", align="left", sep="")}
  <div style="height:300px"></div>
  {zone(860, "正文区 · 采批节 · 双平台（待补，约 300 字）")}
</section>''')
# ---------- 第六章：城门拱券 ----------
parts.append(f'''
<section style="padding-top:120px;">
  {L("img/v5/bamboo.jpg", "left:-280px; top:100px; width:560px; opacity:.3;", "mul fade-y")}
  {L("img/v5/orn_02.png", "right:20px; top:40px; width:400px; opacity:.85;")}
  {head("六", "青春设计聚金陵", "国潮大秀映城墙")}
  {win("f2_3", "s6_jinling.jpg", 720, "margin-top:10px;", "50% 45%")}
  <div style="margin-top:-30px;">{zone(1000, "正文区 · 约 370 字")}</div>
</section>''')
# ---------- 过渡：千里江山 + 双鹤 ----------
parts.append(f'''<section style="height:360px;">
  {L("img/v5/shan_1c.jpg", "left:-900px; top:-20px; width:2100px; opacity:.45;", "mul fade-y")}
  {L("img/v5/orn_09.png", "left:120px; top:40px; width:260px;")}
  {L("img/v5/orn_08.png", "left:600px; top:110px; width:220px;")}
</section>''')
# ---------- 第七章：宝瓶门（左图右题，留白区压在瓶底） ----------
parts.append(f'''
<section>
  <div style="display:flex; align-items:center; gap:0; padding:0 40px 0 50px;">
    <div style="width:520px; flex:none;">{win("f2_2", "s7_jincheng.jpg", 520)}</div>
    <div style="flex:1; text-align:center;">
      <div class="badge" style="width:420px; margin:0 auto;"><img class="cloud" src="img/v5/orn_10.png" style="width:360px;"><div class="seal">七</div></div>
      <div class="ttl" style="font-size:44px; letter-spacing:4px;">「三十二载融金城</div>
      <div class="ttl" style="font-size:30px; letter-spacing:1px; margin-top:6px; white-space:nowrap;">MINSON LAND甘青宁首店开业」</div>
      <div class="slot" style="position:relative;" data-label="篇名 · 日期"></div>
    </div>
  </div>
  {L("img/v5/orn_05.png", "left:430px; top:-40px; width:260px;")}
  <div style="margin-top:-30px;">{zone(1060, "正文区 · 店庆 约 390 字 + MINISO LAND")}</div>
</section>''')
# ---------- 过渡：八角窗 ----------
parts.append(f'''<section style="height:520px;">
  <div style="position:absolute; left:80px; top:60px; width:420px;">{win("f2_1", "s8_guanguang.jpg", 420, "", "50% 70%")}</div>
  {L("img/v5/orn_06.png", "right:40px; top:120px; width:280px;")}
  {L("img/v5/orn_00.png", "right:80px; top:380px; width:340px; opacity:.85;")}
</section>''')
# ---------- 第八章：挂轴 ----------
parts.append(f'''
<section>
  {head("八", "观光厅招商成功", "")}
  <div style="position:relative; width:560px; margin:30px auto 0;">
    <img src="img/v6/f1_0.png" style="display:block; width:620px; margin-left:-30px;">
    <div style="position:relative; width:500px; height:880px; margin:-60px auto 0; box-shadow:0 0 0 10px #F3E7CF, 0 0 0 11px rgba(184,149,90,.5);"><img src="img/v6/s8_guanguang.jpg" style="width:100%; height:100%; object-fit:cover;"></div>
    <img src="img/v6/f1_1.png" style="display:block; width:620px; margin:-50px 0 0 -30px;">
  </div>
  {L("img/v5/orn_09.png", "left:40px; top:600px; width:260px; transform:scaleX(-1);")}
  <div style="margin-top:20px;">{zone(760, "正文区 · 观光厅招商（待补，约 250 字）")}</div>
</section>''')
# ---------- 结尾：金色收束 ----------
parts.append('''
<section style="margin-top:80px; height:1920px;">
  <img src="img/v6/end.jpg" style="display:block; width:1080px; height:1920px; -webkit-mask-image:linear-gradient(to bottom, transparent, #000 12%);">
  <div class="L blank" style="left:140px; top:300px; width:800px; height:520px;" data-label="结尾展望 · 约 4–6 行"></div>
  <img class="L" src="img/logo_wordmark.png" style="left:390px; top:1750px; width:300px;">
</section>''')

for name, cls in (('long_v6.html', ''), ('long_v6_guide.html', 'guide')):
    open(name, 'w').write(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>2026 大事记长图 v6</title><style>{CSS}</style></head>'
                          f'<body class="{cls}">{"".join(parts)}</body></html>')
print('ok')
