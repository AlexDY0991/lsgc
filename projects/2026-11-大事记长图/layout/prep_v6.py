# v6 素材预处理：抠框饰、算窗洞内部蒙版、插图白底转透明。用法：python3 -I prep_v6.py 生成素材目录
import sys, glob, hashlib
from collections import deque
import numpy as np
from PIL import Image, ImageFilter
G = sys.argv[1]; OUT = 'img/v6'
def lov(a):
    u = f'https://a.lovart.ai/artifacts/agent/{a}.png'
    return glob.glob(f"{G}/g_{hashlib.sha1(u.encode()).hexdigest()[:12]}*")[0]
def white_alpha(a, lo=8, span=40):
    return np.clip((255 - a.min(2) - lo) / span, 0, 1)
def components(m, step=3, min_area=6000):
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
    return boxes
def interior(alpha_crop):
    # 从中心沿"近白"像素泛洪，碰不到边界的区域 = 窗洞内部
    h, w = alpha_crop.shape; free = alpha_crop < 0.15
    seen = np.zeros_like(free); cy, cx = h // 2, w // 2
    if not free[cy, cx]:
        ys, xs = np.nonzero(free[h//3:2*h//3, w//3:2*w//3]);
        if len(ys) == 0: return None
        cy, cx = ys[len(ys)//2] + h//3, xs[len(xs)//2] + w//3
    q = deque([(cy, cx)]); seen[cy, cx] = True; touches = False
    while q:
        y, x = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                if free[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((ny, nx))
            else: touches = True
    if touches: return None
    m = Image.fromarray(seen.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2))
    return m
def cut_sheet(aid, prefix):
    a = np.asarray(Image.open(lov(aid)).convert('RGB')).astype(np.float32)
    al = white_alpha(a)
    m = np.asarray(Image.fromarray((al > 0.06).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(15))) > 0
    boxes = sorted(components(m), key=lambda b: (b[0]))
    rgba = np.dstack([a, al * 255]).astype(np.uint8)
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        Image.fromarray(rgba[y0:y1, x0:x1]).save(f'{OUT}/{prefix}{i}.png')
        im = interior(al[y0:y1, x0:x1])
        tag = ''
        if im is not None:
            mm = Image.new('RGBA', im.size, (255, 255, 255, 0)); mm.putalpha(im); mm.save(f'{OUT}/{prefix}{i}_in.png'); tag = ' +interior'
        print(prefix, i, (x0, y0, x1 - x0, y1 - y0), tag)
cut_sheet('yTYJSqjCWrDsAKfu', 'f1_')   # 卷轴杆 / 折扇 / 团扇
cut_sheet('9rQoUKf9dOlsugMn', 'f2_')   # 月洞窗 / 宝瓶门 / 八角窗 / 城门拱券
# 插图
sc = {'s1_wenduo': '9mDtIDnrbK3gWCP9', 's2_gongsheng': 'v1ZvRpKD9Q39sZjy', 's4_zhibi': 'Rx3AEOF0bv5Yryze', 's5_hangzhou': 'NZoEZDaCAsL8Fkc5',
      's6_jinling': 'DYHSnzlln76VLHBg', 's7_jincheng': 'AAzV4Vs4TG3oQIGf', 's8_guanguang': 'EdsBFz2fPe1Rppgx', 'end': 'AdV4yxpIoVA5dVXp'}
for n, aid in sc.items():
    im = Image.open(lov(aid)).convert('RGB')
    if n == 's1_wenduo':   # 扇面：白底转透明
        a = np.asarray(im).astype(np.float32); al = white_alpha(a, 6, 30)
        Image.fromarray(np.dstack([a, al * 255]).astype(np.uint8)).save(f'{OUT}/{n}.png')
    elif n == 'end':
        im.resize((1080, 1920), Image.LANCZOS).save(f'{OUT}/{n}.jpg', quality=92)
    else:
        im.save(f'{OUT}/{n}.jpg', quality=92)
    print(n, im.size)
