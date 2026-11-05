# 只把亮部（纸面）往更淡的米白推，红色、墨色基本不动。用法：python3 lighten_paper.py in.jpg out.jpg
import sys, numpy as np
from PIL import Image
PAPER = np.array([243, 231, 215.]); TARGET = np.array([249, 243, 233.])
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)
lum = a.mean(2, keepdims=True)
sat = (a.max(2, keepdims=True) - a.min(2, keepdims=True))
w = np.clip((lum - 170) / 60, 0, 1) * np.clip(1 - (sat - 30) / 50, 0, 1)   # 亮且不饱和 = 纸
out = a + (TARGET - PAPER) * w
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(sys.argv[2], quality=92)
