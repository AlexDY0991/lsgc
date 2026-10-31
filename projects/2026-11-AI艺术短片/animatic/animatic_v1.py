#!/usr/bin/env python3
"""第一集《源启》动态分镜 v1：分镜图 + 推拉摇移 + 临时旁白和字幕 + 代码合成的临时配乐。

用法（仓库根目录，用工具 venv 的 python）：
  /tmp/studio-tools/venv/bin/python -I projects/2026-11-AI艺术短片/animatic/animatic_v1.py OUTDIR
镜头表来自 prompts/storyboard_v1.py。画幅 2.39:1，输出 1920×1080（上下黑边）。临时旁白是 Kokoro 合成（只供内部判断节奏），
配乐是 higgsfield-motion 的 score.html 代码合成（organic 预设）。不花即梦积分。
"""
import importlib.util, json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO = Path.cwd()
P = REPO / 'projects/2026-11-AI艺术短片'
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
TOOLS = Path(os.environ.get('STUDIO_TOOLS', '/tmp/studio-tools'))
SK = REPO / '.claude/skills/higgsfield-motion'
W, H, FPS = 1920, 1080, 24
PH = int(W / 2.39)            # picture height inside the letterbox
PY = (H - PH) // 2
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
GOLD = (219, 190, 104)

spec = importlib.util.spec_from_file_location('sb', P / 'prompts/storyboard_v1.py'); sb = importlib.util.module_from_spec(spec); spec.loader.exec_module(sb)
SRC = {'6.2': P / 'assets/v1/prop_song_painting_v1.png', '5.2': P / 'assets/look_v2/look_tang_ling_v2.png', '6.6': P / 'assets/look_v2/look_song_reeling_v2.png',
       '7.2': REPO / 'brand/photos/lanzhou_yaou_intl_sunrise.jpg', '8.1': REPO / 'brand/photos/lanzhou_yaou_intl_night_aerial.jpg'}

# 每镜的运镜：(zoom 起, zoom 止, 中心x 起, 中心x 止, 中心y 起, 中心y 止)；镜头向左移 = 中心 x 变小
MOVES = {
    '1.1': (1.25, 1.12, .62, .50, .50, .50), '1.2': (1.10, 1.25, .50, .46, .50, .50),
    '2.1': (1.05, 1.10, .50, .50, .52, .48), '2.2': (1.10, 1.22, .50, .50, .50, .50), '2.3': (1.08, 1.28, .50, .40, .50, .45),
    '3.1': (1.18, 1.18, .58, .44, .50, .50), '3.2': (1.10, 1.18, .50, .48, .50, .50), '3.3': (1.05, 1.15, .50, .48, .45, .42),
    '4.1': (1.20, 1.20, .62, .38, .50, .50), '4.2': (1.15, 1.15, .60, .44, .50, .50), '4.3': (1.15, 1.15, .58, .42, .50, .50),
    '4.4': (1.05, 1.08, .50, .50, .50, .50),
    '5.1': (1.15, 1.15, .58, .44, .50, .50), '5.2': (1.05, 1.15, .52, .50, .50, .48), '5.3': (1.10, 1.20, .50, .46, .50, .50),
    '6.1': (1.20, 1.20, .62, .40, .50, .50), '6.2': (1.00, 1.18, .50, .50, .50, .50), '6.3': (1.10, 1.18, .50, .50, .56, .48),
    '6.4': (1.08, 1.16, .52, .50, .50, .50), '6.5': (1.06, 1.14, .50, .50, .50, .50), '6.6': (1.06, 1.14, .50, .52, .50, .50),
    '6.7': (1.10, 1.20, .50, .46, .50, .50),
    '7.1': (1.05, 1.08, .50, .50, .50, .50), '7.2': (1.05, 1.20, .48, .48, .45, .42), '7.3': (1.05, 1.12, .50, .50, .50, .50),
    '7.4': (1.05, 1.12, .50, .50, .50, .50), '7.5': (1.05, 1.12, .50, .50, .50, .50), '7.6': (1.08, 1.18, .52, .46, .50, .50),
    '8.1': (1.60, 1.00, .42, .50, .45, .50),
}

# 旁白草稿（ep1_script_v3.md）：(开始秒, key, 文本)
LINES = [(1.5, 'l1', '天地有经纬，文明有脉络。'),
         (14.0, 'l2', '五千多年前，先民从一枚茧里，抽出了丝。'),
         (25.0, 'l3', '一经一纬，织成了绢；织机声里，一代传给一代。'),
         (37.5, 'l4', '大汉凿空，丝绸西出。过黄河，出河西，连起了东方与西方。'),
         (56.0, 'l5', '唐时杭州，红袖织绫，柿蒂花者尤佳。'),
         (67.5, 'l6', '南宋临安，从浴蚕到剪帛，二十四道工序，被画进了长卷。'),
         (87.5, 'l7', '千年之后，经纬仍在。兰州、南京、杭州，城与城之间，丝绸仍在流动。'),
         (107.5, 'l8', '以天地经纬，织人间脉络。丽尚国潮。')]
VOICE = 'zm_yunjian'


def times():
    out = []
    for sid, t, seg, desc, prompt, reuse in sb.SHOTS:
        a, b = t.replace('–', '-').split('-'); out.append((sid, float(a), float(b), seg))
    return out


SH = times(); DUR = SH[-1][2]


def ease(u):
    return u * u * (3 - 2 * u)


def load(sid):
    p = SRC.get(sid) or P / f'storyboard/v1/{sb.key(sid)}.png'
    im = Image.open(p).convert('RGB')
    w, h = im.size; th = int(w / 2.39)
    im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th)) if th <= h else im
    return im.resize((2880, int(2880 / 2.39)), Image.LANCZOS)


def view(img, z, cx, cy):
    sw, sh = img.size; bw, bh = sw / z, sh / z
    x0 = min(max(cx * sw - bw / 2, 0), sw - bw); y0 = min(max(cy * sh - bh / 2, 0), sh - bh)
    return img.crop((int(x0), int(y0), int(x0 + bw), int(y0 + bh))).resize((W, PH), Image.BICUBIC)


def grid_overlay(fr, alpha, spacing=96, phase=0.0):
    """极淡的淡金经纬线（代码动效占位）"""
    ov = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    a = int(70 * alpha)
    for x in np.arange(-spacing + (phase * spacing) % spacing, W + spacing, spacing):
        d.line([(x, 0), (x, PH)], fill=GOLD + (a,), width=1)
    for y in np.arange(spacing / 2, PH, spacing):
        d.line([(0, y), (W, y)], fill=GOLD + (int(a * .7),), width=1)
    return Image.alpha_composite(fr.convert('RGBA'), ov).convert('RGB')


def logo_assets():
    wm = Image.open(REPO / 'brand/logo_wordmark.png').convert('RGBA')
    arr = np.array(wm).astype(np.int16)
    dark = (arr[..., 0] < 100) & (arr[..., 1] < 100) & (arr[..., 2] < 100)
    arr[dark, 0:3] = (236, 230, 218)   # 黑字在深色背景上改成米白，红色叶片保持
    wm = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    wm = wm.resize((760, int(760 * wm.height / wm.width)), Image.LANCZOS)
    return wm


def endcard(t0, t, wm, f_big, f_small):
    """8.2：经纬线从四周收拢 → logo 显现 → 标题卡（代码动效的占位版，正式版用 higgsfield-motion 精做）"""
    fr = Image.new('RGB', (W, PH), (10, 12, 14)); d = ImageDraw.Draw(fr, 'RGBA')
    u = min(1, (t - t0) / 2.5); e = ease(u)
    cx, cy = W / 2, PH / 2 - 30
    for i in range(-9, 10):
        x = cx + i * 90 * (1 - e) + i * 6 * e
        d.line([(x, 0), (x, PH)], fill=GOLD + (int(80 * (1 - .6 * e)),), width=1)
    for j in range(-4, 5):
        y = cy + j * 80 * (1 - e) + j * 4 * e
        d.line([(0, y), (W, y)], fill=GOLD + (int(60 * (1 - .6 * e)),), width=1)
    la = max(0, min(1, (t - t0 - 1.8) / 1.0))
    if la > 0:
        lg = wm.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * la)))
        fr.paste(lg, (int(cx - lg.width / 2), int(cy - lg.height / 2)), lg)
    ta = max(0, min(1, (t - t0 - 3.0) / 0.8))
    if ta > 0:
        c = int(225 * ta)
        s1 = '以天地经纬　织人间脉络'; s2 = 'LONGITUDE  AND  LATITUDE'
        d.text((cx - d.textlength(s1, font=f_big) / 2, cy + 120), s1, font=f_big, fill=(c, c, c))
        d.text((cx - d.textlength(s2, font=f_small) / 2, cy + 178), s2, font=f_small, fill=(int(c * .8),) * 3)
    return fr


def picture(subs):
    cache = {}
    f_sub = ImageFont.truetype(FONT, 40); f_tag = ImageFont.truetype(FONT, 26)
    f_big = ImageFont.truetype(FONT, 44); f_small = ImageFont.truetype(FONT, 22)
    wm = logo_assets()
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', str(OUT / 'picture.mp4')], stdin=subprocess.PIPE)
    for n in range(int(round(DUR * FPS))):
        t = n / FPS
        sid, a, b, seg = next(s for s in SH if s[1] <= t < s[2]) if t < DUR else SH[-1]
        if sid == '8.2':
            pic = endcard(a, t, wm, f_big, f_small)
        else:
            if sid not in cache:
                cache[sid] = load(sid)
                if sid == '6.2':
                    cache['6.2b'] = load_path(P / 'assets/sheets/lay_song_workshop.png')
            z0, z1, x0, x1, y0, y1 = MOVES[sid]
            u = ease((t - a) / (b - a))
            pic = view(cache[sid], z0 + (z1 - z0) * u, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u)
            if sid == '6.2':   # 画 → 真实作坊：同构图叠化（视频里用首尾帧做）
                k = max(0, min(1, (t - a - 1.2) / 1.8))
                real = view(cache['6.2b'], z0 + (z1 - z0) * u, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u)
                pic = Image.blend(pic, real, ease(k))
            if sid == '1.2':
                pic = grid_overlay(pic, ease(min(1, (t - a) / 2.5)) * (1 - max(0, (t - b + .8) / .8)), phase=(t - a) * .15)
            if sid == '8.1':
                pic = grid_overlay(pic, ease(max(0, min(1, (t - a - 3) / 4))), spacing=72)
            for edge in (a, b):   # 2 帧淡入淡出只是为了让动态分镜好看，正式剪辑按镜头表处理转场
                pass
        fr = Image.new('RGB', (W, H), (0, 0, 0)); fr.paste(pic, (0, PY))
        d = ImageDraw.Draw(fr)
        for st, en, text in subs:
            if st <= t < en and not (sid == '8.2' and text.startswith('以天地')):
                al = min(1, (t - st) / .25, (en - t) / .25); c = int(235 * al)
                tw = d.textlength(text, font=f_sub)
                d.text(((W - tw) / 2, PY + PH - 78), text, font=f_sub, fill=(c, c, c), stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((30, 26), f'{sid}  {seg}   {t:06.2f}s', font=f_tag, fill=(255, 205, 60))
        d.text((W - 360, 26), '动态分镜 v1 · 临时旁白/配乐', font=f_tag, fill=(160, 160, 160))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()


def load_path(p):
    im = Image.open(p).convert('RGB'); w, h = im.size; th = int(w / 2.39)
    im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th)) if th <= h else im
    return im.resize((2880, int(2880 / 2.39)), Image.LANCZOS)


def voice():
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(str(TOOLS / 'kokoro-model/kokoro-v1.0.onnx'), str(TOOLS / 'kokoro-model/voices-v1.0.bin'))
    subs = []
    for t, key, text in LINES:
        audio, sr = k.create(text, voice=VOICE, speed=0.82, lang='cmn')
        sf.write(OUT / f'{key}.wav', audio, sr)
        d = len(audio) / sr
        subs.append((t, t + d + 0.4, text)); print(f'{key} {t:6.1f}s +{d:4.1f}s  {text}')
    return subs


def score():
    ev = {'fps': FPS, 'bpm': 75, 'dur': DUR, 'events': [
        {'t': 12.0, 'k': 'drop'}, {'t': 100.8, 'k': 'vac'}, {'t': 102.4, 'k': 'lift'}, {'t': 110.4, 'k': 'end'},
        {'t': 34.0, 'k': 'swell', 'dur': 1.5, 'w': 0.6}, {'t': 64.0, 'k': 'swell', 'dur': 1.5, 'w': 0.6},
        {'t': 84.0, 'k': 'impact', 'w': 0.7}, {'t': 112.4, 'k': 'impact', 'w': 0.6}]}
    (OUT / 'events.json').write_text(json.dumps(ev))
    env = dict(os.environ, HFT_BROWSER=str(TOOLS / 'chrome'))
    subprocess.run(['node', 'scripts/render_audio.mjs', 'assets/templates/audio/score.html', str(OUT / 'score.wav'),
                    '--query', f'preset=organic&bpm=75&dur={DUR}', '--events', str(OUT / 'events.json'), '--timeout', '1500'], cwd=SK, env=env, check=True)


def mix():
    inputs, chains, labels = ['-i', str(OUT / 'score.wav')], [], []
    for i, (t, key, _) in enumerate(LINES, 1):
        inputs += ['-i', str(OUT / f'{key}.wav')]
        chains.append(f'[{i}]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=2.0,adelay={int(t*1000)}|{int(t*1000)}[v{i}]'); labels.append(f'[v{i}]')
    graph = ';'.join(chains) + f";[0]volume=0.55[m];[m]{''.join(labels)}amix=inputs={1+len(labels)}:normalize=0:duration=first[a]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', graph, '-map', '[a]', '-t', str(DUR), '-ar', '48000', str(OUT / 'mix_raw.wav')], check=True)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(OUT / 'mix_raw.wav'), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    lufs = float(r[r.rindex('I:'):].split()[1])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'mix_raw.wav'), '-af',
                    f'volume={-14 - lufs:.2f}dB,aresample=192000,alimiter=limit=0.82:attack=1:release=60:level=false,aresample=48000',
                    str(OUT / 'mix.wav')], check=True)


if __name__ == '__main__':
    assert all(abs(SH[i][2] - SH[i + 1][1]) < 1e-6 for i in range(len(SH) - 1))
    subs = voice()
    if not (OUT / 'score.wav').exists(): score()
    mix(); picture(subs)
    final = OUT / 'yuanqi_animatic_v1.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'picture.mp4'), '-i', str(OUT / 'mix.wav'), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', str(final)], check=True)
    print(final)
