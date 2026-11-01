#!/usr/bin/env python3
"""第一集《源启》结尾 logo 动画 v1（代码渲染，逐帧是 t 的纯函数，3 个子帧做运动模糊）。

用法：/tmp/studio-tools/venv/bin/python -I projects/2026-11-AI艺术短片/rough/logo/logo_v1.py OUTDIR [--stills]
时间线（本地秒，总长 DUR）：
  0.0–2.4  淡金经纬线从四周向中心收拢（经＝纵线、纬＝横线），先亮后隐
  1.0–2.8  圆形标用"走针"方式（顺时针一圈）以淡金色绣出
  2.8–3.3  圆形标由金转为品牌红；3.5–4.0 缩小淡出
  4.05–5.6 文字标「丽尚国潮」按 8 条横带依次从右往左织出，每条带前端有一根淡金纬线
  5.7–6.5  标题「以天地经纬　织人间脉络」/ LONGITUDE AND LATITUDE 淡入，之后静止
logo 用用户提供的 brand/logo_mark.png、brand/logo_wordmark.png，不重画、不变形；文字标的黑色在深色底上换成米白，红色叶形保持。
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path.cwd(); OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
STILLS = '--stills' in sys.argv
W, H, PH, FPS = 1920, 1080, 804, 24
PY = (H - PH) // 2
DUR = 8.43
GOLD = np.array([219, 190, 104], np.float32)
RED = np.array([200, 16, 26], np.float32)
IVORY = (236, 230, 218)
BG = np.array([10, 12, 14], np.float32)
F_CN = '/tmp/studio-tools/fonts/NotoSerifSC-300.ttf'
F_EN = '/tmp/studio-tools/fonts/NotoSerifSC-300.ttf'
CX, CY = W / 2, PH / 2 - 30


def ease(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def eout(u):
    u = min(1.0, max(0.0, u)); return 1 - (1 - u) ** 3


# ---------- 资产 ----------
mk = Image.open(REPO / 'brand/logo_mark.png').convert('RGBA')
MK_SIZE = 260
mk = mk.resize((MK_SIZE, int(MK_SIZE * mk.height / mk.width)), Image.LANCZOS)
MK_A = np.asarray(mk.getchannel('A'), np.float32) / 255
mh, mw = MK_A.shape
yy, xx = np.mgrid[0:mh, 0:mw]
THETA = (np.arctan2(xx - mw / 2, -(yy - mh / 2)) / (2 * np.pi)) % 1.0     # 0 在正上方，顺时针增加

wm = Image.open(REPO / 'brand/logo_wordmark.png').convert('RGBA')
arr = np.asarray(wm).astype(np.int16)
dark = (arr[..., 0] < 110) & (arr[..., 1] < 110) & (arr[..., 2] < 110)
arr[dark, :3] = IVORY
wm = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
WM_W = 820
wm = wm.resize((WM_W, int(WM_W * wm.height / wm.width)), Image.LANCZOS)
WM = np.asarray(wm, np.float32) / 255
wh, ww = WM.shape[:2]
BANDS = 8

f_cn = ImageFont.truetype(F_CN, 54); f_en = ImageFont.truetype(F_EN, 22)
T1, T2 = '以天地经纬　织人间脉络', 'L O N G I T U D E   A N D   L A T I T U D E'
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 1, (PH, W)).astype(np.float32) for _ in range(6)]
vy, vx = np.mgrid[0:PH, 0:W]
VIGN = (1 - 0.35 * (((vx - W / 2) / (W / 2)) ** 2 + ((vy - PH / 2) / (PH / 2)) ** 2)).clip(0.55, 1).astype(np.float32)


def comp(dst, rgb, alpha, x0, y0):
    h, w = alpha.shape
    x0, y0 = int(round(x0)), int(round(y0))
    sl = dst[y0:y0 + h, x0:x0 + w]
    a = alpha[..., None]
    sl[:] = sl * (1 - a) + rgb * a


def text_layer(text, font, fill, alpha, blur):
    tw = int(font.getlength(text)) + 40; th = font.size * 2
    im = Image.new('L', (tw, th), 0); ImageDraw.Draw(im).text((20, font.size // 3), text, font=font, fill=255)
    if blur > 0.05: im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, np.float32) / 255 * alpha
    return np.broadcast_to(np.array(fill, np.float32), a.shape + (3,)), a


def render(t):
    img = np.broadcast_to(BG, (PH, W, 3)).copy()
    # 1) 经纬线收拢
    if t < 2.6:
        s = 150 - 140 * ease(t / 2.4)
        ga = min(1, t / 0.6) * (1 - ease((t - 1.4) / 1.0)) * 0.42
        if ga > 0.003:
            lay = Image.new('L', (W, PH), 0); d = ImageDraw.Draw(lay)
            n = int(W / 2 / max(s, 1)) + 2
            for i in range(-n, n + 1):
                x = CX + i * s
                if -2 < x < W + 2: d.line([(x, 0), (x, PH)], fill=255, width=1)
            m = int(PH / 2 / max(s, 1)) + 2
            for j in range(-m, m + 1):
                y = CY + j * s
                if -2 < y < PH + 2: d.line([(0, y), (W, y)], fill=200, width=1)
            a = np.asarray(lay, np.float32) / 255 * ga
            img = img * (1 - a[..., None]) + GOLD * a[..., None]
    # 2) 圆形标：走针绣出 → 转红 → 淡出
    if 1.0 <= t < 4.1:
        p = eout((t - 1.0) / 1.8)
        alpha = MK_A * (THETA <= p)
        col = GOLD + (RED - GOLD) * ease((t - 2.8) / 0.5)
        fade = 1 - ease((t - 3.5) / 0.5)
        sc = 1 - 0.08 * ease((t - 3.5) / 0.5)
        if sc < 0.999:
            ah = Image.fromarray((alpha * 255).astype(np.uint8)).resize((int(mw * sc), int(mh * sc)), Image.LANCZOS)
            alpha = np.asarray(ah, np.float32) / 255
        h, w = alpha.shape
        comp(img, col, alpha * fade, CX - w / 2, CY - h / 2)
        if p < 0.999:   # 针尖的亮点
            ang = p * 2 * np.pi; r = mw * 0.48
            px, py = CX + r * np.sin(ang), CY - r * np.cos(ang)
            dot = Image.new('L', (40, 40), 0); ImageDraw.Draw(dot).ellipse((14, 14, 26, 26), fill=255)
            da = np.asarray(dot.filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
            comp(img, np.array([255, 240, 200], np.float32), da, px - 20, py - 20)
    # 3) 文字标逐带织出（从右往左），带前端一根纬线
    if t >= 4.05:
        rev = np.zeros((wh, ww), np.float32); bh = wh / BANDS
        thread = []
        for k in range(BANDS):
            pk = eout((t - 4.05 - k * 0.13) / 0.55)
            y0, y1 = int(k * bh), int((k + 1) * bh)
            edge = ww * (1 - pk)
            rev[y0:y1, int(edge):] = 1.0
            if 0 < pk < 1: thread.append((edge, (y0 + y1) / 2, pk))
        a = WM[..., 3] * rev
        comp(img, WM[..., :3] * 255, a, CX - ww / 2, CY - wh / 2)
        for edge, yc, pk in thread:
            lay = Image.new('L', (W, 6), 0); d = ImageDraw.Draw(lay)
            x0 = CX - ww / 2 + edge
            d.line([(x0, 3), (min(W - 1, x0 + 260), 3)], fill=255, width=2)
            la = np.asarray(lay.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
            ramp = np.clip(1 - (np.arange(W) - x0) / 260, 0, 1)[None, :]
            comp(img, GOLD * 1.15, la * ramp * (1 - pk) * 1.2, 0, CY - wh / 2 + yc - 3)
    # 4) 标题
    if t >= 5.7:
        u = ease((t - 5.7) / 0.8)
        rgb, a = text_layer(T1, f_cn, IVORY, u, 6 * (1 - u))
        comp(img, rgb, a, CX - a.shape[1] / 2, CY + wh / 2 + 70 + 8 * (1 - u))
        u2 = ease((t - 6.0) / 0.8)
        rgb, a = text_layer(T2, f_en, (190, 170, 120), u2 * 0.9, 4 * (1 - u2))
        comp(img, rgb, a, CX - a.shape[1] / 2, CY + wh / 2 + 160 + 6 * (1 - u2))
    return img


def frame(n):
    t = n / FPS
    acc = sum(render(t + k / (3 * FPS) * 0.5) for k in range(3)) / 3
    acc = acc * VIGN[..., None] + GRAIN[n % 6][..., None] * 3.0
    pic = Image.fromarray(acc.clip(0, 255).astype(np.uint8))
    fr = Image.new('RGB', (W, H)); fr.paste(pic, (0, PY)); return fr


if __name__ == '__main__':
    if STILLS:
        for t in (0.6, 1.5, 2.3, 3.3, 4.3, 4.9, 6.2, 8.0):
            frame(int(t * FPS)).save(OUT / f'logo_{t:.1f}.png')
    else:
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', str(OUT / 'logo_v1.mp4')], stdin=subprocess.PIPE)
        for n in range(int(round(DUR * FPS))):
            ff.stdin.write(frame(n).tobytes())
        ff.stdin.close(); ff.wait(); print(OUT / 'logo_v1.mp4')
