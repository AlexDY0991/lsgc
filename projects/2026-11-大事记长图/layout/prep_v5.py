# v5 素材预处理：抠装饰元素、底纹、古画染色、海棠框。用法：python3 prep_v5.py 生成素材目录 commons目录
import sys, glob, hashlib, json
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
G, C = sys.argv[1], sys.argv[2]
OUT = 'img/v5'
def lov(a):
    u = f'https://a.lovart.ai/artifacts/agent/{a}.png'
    return glob.glob(f"{G}/g_{hashlib.sha1(u.encode()).hexdigest()[:12]}*")[0]

# 1) 开篇、插图
Image.open(lov('mMMW9Uc9WOJxQyIq')).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(f'{OUT}/open.jpg', quality=92)
Image.open(lov('hYlGZKS3Fs7ymMfG')).convert('RGB').resize((900, 1200), Image.LANCZOS).save(f'{OUT}/ch3_scene.jpg', quality=92)

# 2) 装饰元素：白底 -> 透明，按连通区域切开
orn = Image.open(lov('cMZDfzinNm9UKzoW')).convert('RGB')
a = np.asarray(orn).astype(np.float32)
dist = 255 - a.min(2)                      # 离纯白的距离
alpha = np.clip((dist - 8) / 40, 0, 1)
mask = Image.fromarray((alpha > 0.05).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(25))
m = np.asarray(mask) > 0
# 连通区域（简单 flood fill）
H, W = m.shape; lab = np.zeros((H, W), np.int32); boxes = []
from collections import deque
for y in range(0, H, 4):
    for x in range(0, W, 4):
        if m[y, x] and not lab[y, x]:
            n = len(boxes) + 1; q = deque([(y, x)]); lab[y, x] = n; y0 = y1 = y; x0 = x1 = x
            while q:
                cy, cx = q.popleft()
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n; q.append((ny, nx)); y0 = min(y0, ny); y1 = max(y1, ny); x0 = min(x0, nx); x1 = max(x1, nx)
            if (y1 - y0) * (x1 - x0) > 3000: boxes.append((x0, y0, x1, y1))
rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
info = []
for i, (x0, y0, x1, y1) in enumerate(sorted(boxes, key=lambda b: (b[1] // 200, b[0]))):
    Image.fromarray(rgba[y0:y1, x0:x1]).save(f'{OUT}/orn_{i:02d}.png'); info.append((i, x0, y0, x1 - x0, y1 - y0))
print('ornaments', info)

# 3) 金箔底纹：上下镜像接成长条（无缝）
tex = Image.open(lov('GShh7Q2bWH6bmWuo')).convert('RGB').resize((1080, 1920), Image.LANCZOS)
tex.save(f'{OUT}/tex_a.jpg', quality=90); tex.transpose(Image.FLIP_TOP_BOTTOM).save(f'{OUT}/tex_b.jpg', quality=90)

# 4) 千里江山图：去饱和、染淡金灰，做成正片叠底用的淡山水带
def tint(src, out, w=1080):
    im = Image.open(src).convert('L')
    im = im.resize((w * 2, int(im.height * w * 2 / im.width)), Image.LANCZOS)
    g = np.asarray(im).astype(np.float32) / 255
    g = 1 - (1 - g) * 0.55                                    # 减淡
    gold = np.array([226, 205, 165]) / 255; paper = np.array([1, 1, 1])
    rgb = paper * g[..., None] + gold * (1 - g[..., None])    # 暗部染淡金灰
    Image.fromarray((rgb * 255).astype(np.uint8)).save(out, quality=88)
tint(f'{C}/qianli_1c.jpg', f'{OUT}/shan_1c.jpg'); tint(f'{C}/qianli_1e.jpg', f'{OUT}/shan_1e.jpg')

# 5) 墨竹：转成淡墨，正片叠底用
b = Image.open(f'{C}/bamboo_kejiusi.jpg').convert('L')
g = np.asarray(b).astype(np.float32)
lo, hi = np.percentile(g, 2), np.percentile(g, 60)
g = np.clip((g - lo) / (hi - lo), 0, 1); g = 1 - (1 - g) * 0.45
ink = np.array([150, 140, 120]) / 255
rgb = g[..., None] * 1 + (1 - g[..., None]) * ink
Image.fromarray((rgb * 255).astype(np.uint8)).resize((900, int(900 * b.height / b.width))).save(f'{OUT}/bamboo.jpg', quality=88)

# 6) 海棠形（四瓣）蒙版和金色描边：r(θ) = 1 + k·cos(4θ)，四个圆润花瓣朝上下左右
def haitang(w, h, k=0.13):
    S = 4; W2, H2 = w * S, h * S
    t = np.linspace(0, 2 * np.pi, 2000)
    r = 1 + k * np.cos(4 * t); r = r / r.max()
    pts = [(W2 / 2 + np.cos(a) * rr * (W2 / 2 - 2), H2 / 2 + np.sin(a) * rr * (H2 / 2 - 2)) for a, rr in zip(t, r)]
    im = Image.new('L', (W2, H2), 0); ImageDraw.Draw(im).polygon(pts, fill=255)
    return im.resize((w, h), Image.LANCZOS)
hm = haitang(900, 1080)
m = Image.new('RGBA', hm.size, (255, 255, 255, 0)); m.putalpha(hm); m.save(f'{OUT}/mask_haitang.png')
# 描边比画面外扩一圈（frame .line 用 inset:-14px）
big = haitang(928, 1108)
edge = np.asarray(big.filter(ImageFilter.MaxFilter(5))).astype(np.int16) - np.asarray(big.filter(ImageFilter.MinFilter(3))).astype(np.int16)
o = np.zeros((big.height, big.width, 4), np.uint8); o[..., 0:3] = (190, 152, 86); o[..., 3] = np.clip(edge * 1.2, 0, 255)
Image.fromarray(o).save(f'{OUT}/line_haitang.png')
print('done')
