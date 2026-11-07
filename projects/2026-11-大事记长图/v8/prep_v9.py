# v9（仿「两会新观察」插画版）素材预处理。用法（v8 目录）：python3 -I prep_v9.py
from collections import deque
import numpy as np
from PIL import Image, ImageFilter, ImageChops

R, OUT = 'out_r3', 'img9'
WORD = Image.open('../content_v2/media/image4.png').convert('RGBA')
MARK = Image.open('../content_v2/media/image5.png').convert('RGBA')

def biggest_white(img, area):
    """在 area 里找最大的一块近白、低饱和的连通区域，返回外框。"""
    x0, y0, x1, y1 = area
    a = np.asarray(img.convert('RGB')).astype(int)[y0:y1, x0:x1]
    m = (a.min(2) > 228) & ((a.max(2) - a.min(2)) < 22)
    H, W = m.shape; lab = np.zeros((H, W), np.int32); best = (0, None)
    for y in range(0, H, 4):
        for x in range(0, W, 4):
            if m[y, x] and not lab[y, x]:
                q = deque([(y, x)]); lab[y, x] = 1; n = 0; bx0 = bx1 = x; by0 = by1 = y
                while q:
                    cy, cx = q.popleft(); n += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = 1; q.append((ny, nx)); bx0 = min(bx0, nx); bx1 = max(bx1, nx); by0 = min(by0, ny); by1 = max(by1, ny)
                if n > best[0]: best = (n, (x0 + bx0, y0 + by0, x0 + bx1, y0 + by1))
    return best[1]

def multiply_paste(base, logo, box):
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / logo.width, (y1 - y0) / logo.height)
    lg = logo.resize((max(1, int(logo.width * s)), max(1, int(logo.height * s))), Image.LANCZOS)
    layer = Image.new('RGB', base.size, 'white')
    white = Image.new('RGB', lg.size, 'white'); white.paste(lg, (0, 0), lg)
    layer.paste(white, (x0 + ((x1 - x0) - lg.width) // 2, y0 + ((y1 - y0) - lg.height) // 2))
    return ImageChops.multiply(base.convert('RGB'), layer)

def lockup(h):
    m = MARK.resize((h, h), Image.LANCZOS)
    w = WORD.resize((int(WORD.width * h * 0.62 / WORD.height), int(h * 0.62)), Image.LANCZOS)
    out = Image.new('RGBA', (m.width + int(h * 0.25) + w.width, h), (255, 255, 255, 0))
    out.alpha_composite(m, (0, 0)); out.alpha_composite(w, (m.width + int(h * 0.25), (h - w.height) // 2))
    return out

imgs = {k: Image.open(f'{R}/{k}.png').convert('RGB') for k in ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8']}
W0, H0 = imgs['i1'].size
# 换届：横匾
b = biggest_white(imgs['i1'], (int(W0 * .15), int(H0 * .18), int(W0 * .85), int(H0 * .32)))
print('i1 plaque', b)
x0, y0, x1, y1 = b; pw, ph = x1 - x0, y1 - y0
imgs['i1'] = multiply_paste(imgs['i1'], lockup(400), (x0 + int(pw * .12), y0 + int(ph * .22), x1 - int(pw * .12), y1 - int(ph * .22)))
# 乔迁：大屏（自动识别只找到上沿，按画面手动定框：大屏 x≈266–1034，上沿 y≈1300，人物头顶 y≈1400，原图坐标）
imgs['i3'] = multiply_paste(imgs['i3'], WORD, (360, 1318, 940, 1412))
for k, im in imgs.items():
    im.resize((1080, int(1080 * H0 / W0)), Image.LANCZOS).save(f'{OUT}/{k}.jpg', quality=92)

# 毛笔字：黑底白字 -> 透明底白字
for i in range(1, 9):
    a = np.asarray(Image.open(f'{R}/c{i}.png').convert('L')).astype(np.float32)
    al = np.clip((a - 40) / 170, 0, 1)
    m = (al > .05)
    ys, xs = np.nonzero(m); bx = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    rgba = np.zeros(a.shape + (4,), np.uint8); rgba[..., :3] = 255; rgba[..., 3] = (al * 255).astype(np.uint8)
    Image.fromarray(rgba).crop(bx).save(f'{OUT}/calli_{i}.png'); print('calli', i, bx)
