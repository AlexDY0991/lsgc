# 把素材的近白底校正成纯白（正片叠底后不露矩形边）。用法：python3 whiten.py img/v2/wash_a2.png ...
import sys, numpy as np
from PIL import Image
for f in sys.argv[1:]:
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
    h, w, _ = a.shape
    k = max(8, min(h, w) // 40)
    corners = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    # 取四角里最亮的那些像素当纸色（避开角上本身有颜料的情况）
    lum = corners.mean(1); bg = np.percentile(corners[lum > np.percentile(lum, 60)], 50, axis=0)
    out = np.clip(a / bg * 255.0, 0, 255)
    # 很接近白的地方直接推成纯白
    near = (out.min(2) > 242)[..., None]
    out = np.where(near, 255, out)
    # 四边羽化成白（素材画到边上时不留硬边）
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.minimum.reduce([xx / (w * .14), (w - 1 - xx) / (w * .14), yy / (h * .12), (h - 1 - yy) / (h * .12)])
    m = np.clip(m, 0, 1)[..., None] ** 1.5
    out = out * m + 255 * (1 - m)
    g = f.replace('.png', '_w.png')
    Image.fromarray(out.astype(np.uint8)).save(g); print(g, 'bg', bg.round(1))
