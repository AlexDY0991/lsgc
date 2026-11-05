# 只在朱红区域抹掉细小的淡字/水印纹理（中值滤波 + 羽化蒙版），其他区域不动。
# 用法：python3 clean_red.py 输入.png 输出.png
import sys, numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 110) & (r - g > 55) & (r - b > 45)          # 朱红像素
m = Image.fromarray((red * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(4))
m = np.asarray(m).astype(np.float32)[..., None] / 255.0
smooth = np.asarray(im.filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)
# 把纸纹细节以低强度加回，避免红色变得像塑料
detail = a - np.asarray(im.filter(ImageFilter.GaussianBlur(2))).astype(np.float32)
out = a * (1 - m) + (smooth + detail * 0.25) * m
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(dst)
print(dst, 'red area %.1f%%' % (red.mean() * 100))
