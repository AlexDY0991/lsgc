# v8 素材预处理。用法（在 v8 目录）：python3 -I prep_v8.py
# 1) 新 logo 贴进换届横匾（e1）和乔迁大屏（e3），正片叠底继承墙面光影；
# 2) 各块按"放大核心"裁切成 1080×1440；封面、结尾 1080×1920；
# 3) 过渡素材抠图：白云（黑底）、红绸（绿幕）、燕子（白底）。
from collections import deque
import numpy as np
from PIL import Image, ImageFilter, ImageChops

R, OUT = 'out_r1', 'img'
WORD = Image.open('../content_v2/media/image4.png').convert('RGBA')   # 新 logo 文字标
MARK = Image.open('../content_v2/media/image5.png').convert('RGBA')   # 新辅助图形（圆标）

def multiply_paste(base, logo, box):
    """把 logo 按 box（x0,y0,x1,y1）居中缩放，正片叠底贴到 base 上。"""
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / logo.width, (y1 - y0) / logo.height)
    lg = logo.resize((int(logo.width * s), int(logo.height * s)), Image.LANCZOS)
    layer = Image.new('RGB', base.size, 'white')
    white = Image.new('RGB', lg.size, 'white'); white.paste(lg, (0, 0), lg)
    px, py = x0 + ((x1 - x0) - lg.width) // 2, y0 + ((y1 - y0) - lg.height) // 2
    layer.paste(white, (px, py))
    return ImageChops.multiply(base, layer)

def lockup(h):
    """圆标 + 文字标的横向组合（和换届照片背景墙一致）。"""
    m = MARK.resize((h, h), Image.LANCZOS)
    w = WORD.resize((int(WORD.width * h * 0.62 / WORD.height), int(h * 0.62)), Image.LANCZOS)
    out = Image.new('RGBA', (m.width + int(h * 0.25) + w.width, h), (255, 255, 255, 0))
    out.alpha_composite(m, (0, 0)); out.alpha_composite(w, (m.width + int(h * 0.25), (h - w.height) // 2))
    return out

# ---- e1：横匾 (556,659)-(1179,897) ----
e1 = Image.open(f'{R}/e1.png').convert('RGB')
e1 = multiply_paste(e1, lockup(400), (556 + 70, 659 + 60, 1179 - 70, 897 - 60))
# ---- e3：大屏露出部分 x 215–1520，y 850 起，人物头顶约 1050 ----
e3 = Image.open(f'{R}/e3.png').convert('RGB')
e3 = multiply_paste(e3, WORD, (520, 880, 1215, 1010))

def block(img, box, name):
    """box = 原图裁切框（宽:高 = 3:4），输出 1080×1440。"""
    img.crop(box).resize((1080, 1440), Image.LANCZOS).save(f'{OUT}/{name}.jpg', quality=92)
    print(name, box)

W, H = 1728, 2304
block(e1, (170, 120, 170 + 1400, 120 + 1867), 'b1_huanjie')            # 合影拉近
block(Image.open(f'{R}/e2.png').convert('RGB'), (114, 150, 114 + 1500, 150 + 2000), 'b2_qianyue')   # 握手拉近
block(e3, (0, 0, W, H), 'b3_qiaoqian')
block(Image.open(f'{R}/e4.png').convert('RGB'), (0, 0, W, H), 'b4_ai')
block(Image.open(f'{R}/e5.png').convert('RGB'), (0, 0, W, H), 'b5_hangzhou')
block(Image.open(f'{R}/e6.png').convert('RGB'), (0, 120, 1560, 120 + 2080), 'b6_nanjing')         # 领头模特拉近
block(Image.open(f'{R}/e7.png').convert('RGB'), (0, 0, W, H), 'b7_yaou')
block(Image.open(f'{R}/e8.png').convert('RGB'), (0, 0, W, H), 'b8_guanguang')
Image.open('assets/cover.jpg').convert('RGB').resize((1080, 1920), Image.LANCZOS).save(f'{OUT}/b0_cover.jpg', quality=92)
Image.open(f'{R}/end.png').convert('RGB').resize((1080, 1920), Image.LANCZOS).save(f'{OUT}/b9_end.jpg', quality=92)

# ---- 抠图 ----
def components(m, min_area=6000):
    Hh, Ww = m.shape; lab = np.zeros((Hh, Ww), np.int32); boxes = []
    for y in range(0, Hh, 3):
        for x in range(0, Ww, 3):
            if m[y, x] and not lab[y, x]:
                n = len(boxes) + 1; q = deque([(y, x)]); lab[y, x] = n; y0 = y1 = y; x0 = x1 = x
                while q:
                    cy, cx = q.popleft()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < Hh and 0 <= nx < Ww and m[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; q.append((ny, nx)); y0 = min(y0, ny); y1 = max(y1, ny); x0 = min(x0, nx); x1 = max(x1, nx)
                if (y1 - y0) * (x1 - x0) > min_area: boxes.append((x0, y0, x1 + 1, y1 + 1))
    return sorted(boxes, key=lambda b: (b[1] // 300, b[0]))

def save_parts(rgb, al, prefix, grow=21):
    m = np.asarray(Image.fromarray((al > .04).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(grow))) > 0
    for i, (x0, y0, x1, y1) in enumerate(components(m)):
        Image.fromarray(np.dstack([rgb[y0:y1, x0:x1], al[y0:y1, x0:x1] * 255]).astype(np.uint8)).save(f'{OUT}/{prefix}{i}.png')
        print(prefix, i, x1 - x0, y1 - y0)

def soft(al, blur=1.2):
    return np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255

# 白云：黑底，按亮度做 alpha，再反预乘；边缘往冷白收
a = np.asarray(Image.open(f'{R}/t_cloud.png').convert('RGB')).astype(np.float32)
al = np.clip((a.mean(2) - 20) / 150, 0, 1) ** 1.2
rgb = np.clip(a / np.maximum(al[..., None], 1e-3), 0, 255)
w = (1 - al[..., None]) ** 1.5; rgb = rgb * (1 - w) + np.array([240, 246, 252.]) * w
rgb = 255 - (255 - rgb) * 0.55                                   # 提亮，去掉灰重感
save_parts(rgb, soft(al, 1.5), 'cloud_')

# 红绸：绿幕抠像 + 去绿边，色相往朱红略收
a = np.asarray(Image.open(f'{R}/t_silk.png').convert('RGB')).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
al = soft(1 - np.clip((g - np.maximum(r, b) - 25) / 70, 0, 1), .8)
a[..., 1] = np.minimum(g, np.maximum(r, b))                      # 去绿边
hsv = np.asarray(Image.fromarray(a.astype(np.uint8)).convert('HSV')).astype(np.float32)
hsv[..., 0] = 2; hsv[..., 1] *= 0.82; hsv[..., 2] *= 0.86          # 色相收到朱红，降饱和、压亮度
a = np.asarray(Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')).astype(np.float32)
save_parts(a, al, 'silk_')

# 燕子：白底，按离白的距离做 alpha
a = np.asarray(Image.open(f'{R}/t_birds.png').convert('RGB')).astype(np.float32)
al = np.clip((255 - a.min(2) - 12) / 60, 0, 1)
save_parts(a, soft(al, .8), 'bird_', grow=15)
