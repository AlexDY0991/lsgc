# 生成不规则毛边羽化蒙版（白=显示）。用法：python3 make_masks.py
import numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
def noise(w, h, scale, octaves=4):
    out = np.zeros((h, w))
    amp, tot = 1.0, 0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        g = rng.random((h // s + 2, w // s + 2))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * (np.asarray(im) / 255.0); tot += amp; amp *= 0.5
    return out / tot
def brush_mask(w, h, inset=0.12, rough=0.10, feather=18, shape='ellipse', name='m'):
    y, x = np.mgrid[0:h, 0:w]
    nx, ny = (x / w - .5) * 2, (y / h - .5) * 2
    if shape == 'ellipse':
        d = np.sqrt(nx ** 2 + ny ** 2)
    else:  # 圆角矩形
        d = np.maximum(np.abs(nx), np.abs(ny)) ** 4 + 0 * nx
        d = (np.abs(nx) ** 6 + np.abs(ny) ** 6) ** (1 / 6)
    n = noise(w, h, 120) - .5
    d = d + n * rough * 2 + (noise(w, h, 18, 2) - .5) * rough * .6
    a = np.clip((1 - inset - d) / 0.06, 0, 1)
    al = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))
    im = Image.new('RGBA', (w, h), (255, 255, 255, 0)); im.putalpha(al)  # CSS mask 读透明通道
    im.save(f'img/v2/{name}.png'); print(name, w, h)
brush_mask(1000, 1300, inset=.05, rough=.12, feather=14, shape='rect', name='mask_scene')
brush_mask(1000, 760, inset=.02, rough=.14, feather=10, shape='rect', name='mask_scroll')
brush_mask(1000, 1400, inset=.0, rough=.16, feather=26, shape='ellipse', name='mask_shan')
# 撕纸边：高频噪声 + 很小的羽化，边缘利落
def torn_mask(w, h, name, inset=.035, rough=.035, feather=1.2):
    y, x = np.mgrid[0:h, 0:w]
    nx, ny = (x / w - .5) * 2, (y / h - .5) * 2
    d = (np.abs(nx) ** 8 + np.abs(ny) ** 8) ** (1 / 8)
    n = (noise(w, h, 60, 3) - .5) * rough * 2 + (noise(w, h, 6, 2) - .5) * rough * .9
    a = np.clip((1 - inset - d - n) / 0.004, 0, 1)
    al = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))
    im = Image.new('RGBA', (w, h), (255, 255, 255, 0)); im.putalpha(al); im.save(f'img/v2/{name}.png'); print(name, w, h)
torn_mask(900, 820, 'mask_panel')
