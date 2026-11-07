# v7（3D 金色版）素材预处理。用法：python3 -I prep_v7.py 生成素材目录 第一页图片
import sys, glob, hashlib
from collections import deque
import numpy as np
from PIL import Image, ImageFilter
G, P0 = sys.argv[1], sys.argv[2]
OUT = 'img'
def lov(a):
    u = f'https://a.lovart.ai/artifacts/agent/{a}.png'
    return glob.glob(f"{G}/g_{hashlib.sha1(u.encode()).hexdigest()[:12]}*")[0]
PANELS = [('p00_page1', None), ('p01_wenduo', 'LT3Fiv2rbEER4YxU'), ('p02_xiaoqi', 'DuVDbYQ0CO74735X'), ('p03_qiaoqian', 'd5EbaBUeQD7uzXxf'),
          ('p04_ai', 'YhQO8nY9O4GttWZL'), ('p05_hangzhou', '1vFgDlIgRv3JXxk3'), ('p06_nanjing', 'VSHX9RjEbWKK3Nvw'),
          ('p07_yaou', 'gQjo8KG9UkIFMIL9'), ('p08_guanguang', 'x7zvYCOVpg9MXuYi'), ('p09_end', '2lIZuVzswz7b8Uca')]
for n, a in PANELS:
    im = Image.open(P0 if a is None else lov(a)).convert('RGB').resize((1080, 1920), Image.LANCZOS)
    im.save(f'{OUT}/{n}.jpg', quality=92); print(n)

def components(m, step=3, min_area=8000):
    H, W = m.shape; lab = np.zeros((H, W), np.int32); boxes = []
    for y in range(0, H, step):
        for x in range(0, W, step):
            if m[y, x] and not lab[y, x]:
                n = len(boxes) + 1; q = deque([(y, x)]); lab[y, x] = n; y0 = y1 = y; x0 = x1 = x
                while q:
                    cy, cx = q.popleft()
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; q.append((ny, nx)); y0 = min(y0, ny); y1 = max(y1, ny); x0 = min(x0, nx); x1 = max(x1, nx)
                if (y1 - y0) * (x1 - x0) > min_area: boxes.append((x0, y0, x1 + 1, y1 + 1))
    return sorted(boxes, key=lambda b: (b[1] // 300, b[0]))
def save_parts(rgb, alpha, prefix):
    m = np.asarray(Image.fromarray((alpha > .04).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(21))) > 0
    for i, (x0, y0, x1, y1) in enumerate(components(m)):
        Image.fromarray(np.dstack([rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1] * 255]).astype(np.uint8)).save(f'{OUT}/{prefix}{i}.png')
        print(prefix, i, x1 - x0, y1 - y0)

# 云：黑底 -> 透明（按亮度做 alpha，再反预乘）
a = np.asarray(Image.open(lov('VKqyemkpli2byDBe')).convert('RGB')).astype(np.float32)
lum = a.mean(2)
al = np.clip((lum - 30) / 140, 0, 1) ** 1.3                      # 边缘更柔、去掉暗晕
rgb = np.clip(a / np.maximum(al[..., None], 1e-3), 0, 255)
cream = np.array([252, 244, 228.])
w = (1 - al[..., None]) ** 1.5                                    # 越靠边越往奶白收
rgb = rgb * (1 - w) + cream * w
al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
save_parts(rgb, al, 'cloud_')

# 飘带：绿幕抠像 + 去绿边
a = np.asarray(Image.open(lov('u7gw42t0Uj8G11vl')).convert('RGB')).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
key = g - np.maximum(r, b)
al = 1 - np.clip((key - 25) / 70, 0, 1)
al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8))).astype(np.float32) / 255
a[..., 1] = np.minimum(g, np.maximum(r, b) * 1.02)
save_parts(a, al, 'ribbon_')
