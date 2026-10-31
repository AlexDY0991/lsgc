#!/usr/bin/env python3
"""第一集《源启》动态分镜 v2：加入高潮「千年一梭」、真空的眼神、释放段的人（用户 2026-10-31：没有高潮、结尾没有情绪）。

用法（仓库根目录）：/tmp/studio-tools/venv/bin/python -I projects/2026-11-AI艺术短片/animatic/animatic_v2.py OUTDIR
情绪曲线：序（静）→ 起（慢）→ 承（渐浓）→ 高潮 60–80s（越切越快，织机声变鼓点，76.5s 剪刀匹配切 = 爆点）
        → 真空 80–84.5s（近乎无声，两个时代的眼神）→ 释放 84.5–104s（三城亮灯、有人）→ 收 104–118s（logo）。
高潮段的画面在动态分镜里重复用了几张分镜图（不同的裁切），正式视频里是一场单独生成的快切戏，不重复素材。
"""
import importlib.util, json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path.cwd()
P = REPO / 'projects/2026-11-AI艺术短片'
spec = importlib.util.spec_from_file_location('a1', P / 'animatic/animatic_v1.py')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0], str(OUT)]
a1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a1)   # 复用 v1 的 view / grid_overlay / endcard / logo
W, H, FPS, PH, PY, FONT, TOOLS, SK = a1.W, a1.H, a1.FPS, a1.PH, a1.PY, a1.FONT, a1.TOOLS, a1.SK

V1 = P / 'storyboard/v1'; V2 = P / 'storyboard/v2'
IMG = {k: V1 / f'sb_{k.replace(".", "_")}.png' for k in
       ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3', '4.4', '5.1', '5.3', '6.1', '6.3', '6.4', '6.5', '6.7',
        '7.1', '7.3', '7.4', '7.5', '7.6']}
IMG.update({'5.2': P / 'assets/look_v2/look_tang_ling_v2.png', '6.6': P / 'assets/look_v2/look_song_reeling_v2.png',
            '6.2': P / 'assets/v1/prop_song_painting_v1.png', '7.2': REPO / 'brand/photos/lanzhou_yaou_intl_sunrise.jpg',
            '8.1': REPO / 'brand/photos/lanzhou_yaou_intl_night_aerial.jpg'})
for k in ['c6_cut', 'c6_lookup', 'hb_fold', 'hb_pack', 'mall_family', 'river_people', 'hb_smile', 'window_rise']:
    IMG[k] = V2 / f'sb2_{k}.png'

# (开始, 结束, 图, 段落, (zoom0, zoom1, x0, x1, y0, y1))
SHOTS = [
 (0.0, 7.0, '1.1', '序·竹', (1.25, 1.12, .62, .50, .5, .5)),
 (7.0, 10.0, '1.2', '序·竹', (1.10, 1.25, .50, .46, .5, .5)),
 (10.0, 13.0, '2.2', '起·茧', (1.10, 1.22, .5, .5, .5, .5)),
 (13.0, 18.0, '2.3', '起·茧', (1.08, 1.28, .50, .40, .50, .45)),
 (18.0, 21.0, '3.1', '起·织', (1.18, 1.18, .58, .46, .5, .5)),
 (21.0, 23.0, '3.2', '起·织', (1.10, 1.18, .50, .48, .5, .5)),
 (23.0, 27.0, '3.3', '起·伏笔：她抬头', (1.04, 1.16, .50, .47, .45, .42)),
 (27.0, 30.0, '4.1', '起·向西', (1.20, 1.20, .62, .40, .5, .5)),
 (30.0, 32.5, '4.2', '起·向西', (1.15, 1.15, .60, .46, .5, .5)),
 (32.5, 35.0, '4.3', '起·向西', (1.15, 1.15, .58, .44, .5, .5)),
 (35.0, 38.0, '4.4', '起·金城', (1.05, 1.09, .5, .5, .5, .5)),
 (38.0, 41.0, '5.1', '承·唐', (1.15, 1.15, .58, .46, .5, .5)),
 (41.0, 45.0, '5.2', '承·唐', (1.05, 1.15, .52, .50, .50, .48)),
 (45.0, 49.0, '6.1', '承·南宋', (1.20, 1.20, .62, .42, .5, .5)),
 (49.0, 54.0, '6.2', '承·南宋', (1.00, 1.18, .5, .5, .5, .5)),
 (54.0, 57.0, '6.3', '承·南宋', (1.10, 1.18, .5, .5, .56, .48)),
 (57.0, 60.0, '6.5', '承·南宋', (1.06, 1.14, .5, .5, .5, .5)),
 # 高潮：千年一梭（越切越快）
 (60.0, 62.0, '6.6', '高潮·千年一梭', (1.10, 1.25, .52, .56, .5, .5)),
 (62.0, 63.6, '3.2', '高潮·千年一梭', (1.35, 1.50, .45, .40, .55, .55)),
 (63.6, 65.0, '5.3', '高潮·千年一梭', (1.30, 1.45, .55, .50, .5, .5)),
 (65.0, 66.2, '6.4', '高潮·千年一梭', (1.40, 1.55, .40, .36, .5, .5)),
 (66.2, 67.3, 'hb_fold', '高潮·千年一梭', (1.10, 1.25, .45, .42, .55, .55)),
 (67.3, 68.3, '6.3', '高潮·千年一梭', (1.45, 1.60, .55, .55, .40, .36)),
 (68.3, 69.2, 'hb_pack', '高潮·千年一梭', (1.15, 1.30, .60, .62, .45, .45)),
 (69.2, 70.0, '2.3', '高潮·千年一梭', (1.60, 1.80, .42, .40, .40, .38)),
 (70.0, 70.8, '7.6', '高潮·千年一梭', (1.30, 1.50, .55, .52, .60, .60)),
 (70.8, 71.5, '3.1', '高潮·千年一梭', (1.50, 1.70, .45, .42, .55, .55)),
 (71.5, 72.2, '5.2', '高潮·千年一梭', (1.50, 1.70, .40, .38, .55, .55)),
 (72.2, 72.8, '4.2', '高潮·千年一梭', (1.50, 1.70, .45, .42, .45, .45)),
 (72.8, 73.4, '6.5', '高潮·千年一梭', (1.50, 1.70, .55, .55, .45, .45)),
 (73.4, 74.0, 'hb_fold', '高潮·千年一梭', (1.60, 1.85, .40, .38, .62, .62)),
 (74.0, 74.5, '6.4', '高潮·千年一梭', (1.70, 1.90, .35, .32, .50, .50)),
 (74.5, 75.0, '5.3', '高潮·千年一梭', (1.70, 1.90, .45, .42, .50, .50)),
 (75.0, 76.5, '6.7', '高潮·南宋一剪', (1.15, 1.35, .45, .42, .45, .45)),
 (76.5, 80.0, 'c6_cut', '爆点·今天一剪', (1.15, 1.25, .62, .60, .55, .52)),
 # 真空：两个时代的眼神
 (80.0, 82.2, 'c6_lookup', '真空·她抬头', (1.06, 1.10, .50, .49, .45, .44)),
 (82.2, 84.5, '3.3', '真空·五千年前', (1.10, 1.14, .50, .49, .45, .44)),
 # 释放：三城亮灯，有人
 (84.5, 88.0, 'window_rise', '释放', (1.00, 1.15, .50, .50, .55, .45)),
 (88.0, 92.0, '7.1', '释放·兰州', (1.05, 1.10, .5, .5, .5, .5)),
 (92.0, 94.0, 'river_people', '释放·兰州', (1.05, 1.12, .5, .5, .5, .5)),
 (94.0, 96.0, '7.3', '释放·兰州', (1.05, 1.12, .5, .5, .5, .5)),
 (96.0, 98.0, 'mall_family', '释放·兰州', (1.05, 1.14, .5, .5, .5, .5)),
 (98.0, 100.0, '7.4', '释放·南京', (1.05, 1.12, .5, .5, .5, .5)),
 (100.0, 102.0, '7.5', '释放·杭州', (1.05, 1.12, .5, .5, .5, .5)),
 (102.0, 104.0, 'hb_smile', '释放·杭州', (1.05, 1.12, .52, .50, .5, .5)),
 (104.0, 111.0, '8.1', '收·经纬', (1.60, 1.00, .42, .50, .45, .50)),
 (111.0, 118.0, 'END', '收·丽尚国潮', None),
]
DUR = SHOTS[-1][1]

LINES = [(1.5, 'l1', '天地有经纬，文明有脉络。'),
         (11.0, 'l2', '五千多年前，先民从一枚茧里，抽出了丝。'),
         (18.5, 'l3', '一经一纬，织成了绢；织机声里，一代传给一代。'),
         (28.0, 'l4', '大汉凿空，丝绸西出。过黄河，出河西，连起了东方与西方。'),
         (40.5, 'l5', '唐时杭州，红袖织绫，柿蒂花者尤佳。'),
         (48.5, 'l6', '南宋临安，从浴蚕到剪帛，二十四道工序，被画进了长卷。'),
         (80.6, 'lv', '五千年，这双手，从没有停下。'),
         (89.0, 'l7', '千年之后，经纬仍在。兰州、南京、杭州，城与城之间，人与人之间。'),
         (111.5, 'l8', '以天地经纬，织人间脉络。丽尚国潮。')]


def load(k):
    im = Image.open(IMG[k]).convert('RGB'); w, h = im.size; th = int(w / 2.39)
    im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th)) if th <= h else im
    return im.resize((2880, int(2880 / 2.39)), Image.LANCZOS)


def voice():
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(str(TOOLS / 'kokoro-model/kokoro-v1.0.onnx'), str(TOOLS / 'kokoro-model/voices-v1.0.bin'))
    subs = []
    for t, key, text in LINES:
        audio, sr = k.create(text, voice=a1.VOICE, speed=0.78 if key in ('lv', 'l8') else 0.82, lang='cmn')
        sf.write(OUT / f'{key}.wav', audio, sr); d = len(audio) / sr
        subs.append((t, t + d + 0.4, text)); print(f'{key} {t:6.1f}s +{d:4.1f}s  {text}')
    return subs


def score():
    cuts = [s[0] for s in SHOTS if 60.0 <= s[0] < 76.5]
    ev = {'fps': FPS, 'bpm': 80, 'dur': DUR, 'events':
          [{'t': 38.0, 'k': 'drop'}, {'t': 80.0, 'k': 'vac'}, {'t': 84.5, 'k': 'lift'}, {'t': 111.5, 'k': 'end'},
           {'t': 76.5, 'k': 'riser', 'dur': 6.0, 'w': 1.0}, {'t': 76.5, 'k': 'impact', 'w': 1.3},
           {'t': 84.5, 'k': 'swell', 'dur': 2.0, 'w': 0.8}, {'t': 111.5, 'k': 'impact', 'w': 1.0}]
          + [{'t': c, 'k': 'tick', 'w': 0.6 + 0.6 * (c - 60) / 16.5, 'note': 'shuttle'} for c in cuts]}
    (OUT / 'events.json').write_text(json.dumps(ev))
    env = dict(os.environ, HFT_BROWSER=str(TOOLS / 'chrome'))
    subprocess.run(['node', 'scripts/render_audio.mjs', 'assets/templates/audio/score.html', str(OUT / 'score.wav'),
                    '--query', f'preset=arrival&bpm=80&dur={DUR}', '--events', str(OUT / 'events.json'), '--timeout', '2400'],
                   cwd=SK, env=env, check=True)


def mix():
    inputs, chains, labels = ['-i', str(OUT / 'score.wav')], [], []
    for i, (t, key, _) in enumerate(LINES, 1):
        inputs += ['-i', str(OUT / f'{key}.wav')]
        chains.append(f'[{i}]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=2.0,adelay={int(t*1000)}|{int(t*1000)}[v{i}]'); labels.append(f'[v{i}]')
    # 旁白时把配乐压低；真空段（80–84.5）配乐几乎静音
    duck = '+'.join(f'between(t,{t-0.2:.2f},{t+5.5:.2f})' for t, k, _ in LINES if k not in ('lv',))
    vol = f"if(between(t,80.0,84.5),0.08,if({duck},0.45,0.8))"
    graph = ';'.join(chains) + f";[0]volume='{vol}':eval=frame[m];[m]{''.join(labels)}amix=inputs={1+len(labels)}:normalize=0:duration=first[a]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', graph, '-map', '[a]', '-t', str(DUR), '-ar', '48000', str(OUT / 'mix_raw.wav')], check=True)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(OUT / 'mix_raw.wav'), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    lufs = float(r[r.rindex('I:'):].split()[1])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'mix_raw.wav'), '-af',
                    f'volume={-14 - lufs:.2f}dB,aresample=192000,alimiter=limit=0.82:attack=1:release=60:level=false,aresample=48000',
                    str(OUT / 'mix.wav')], check=True)


def picture(subs):
    cache = {}
    f_sub = ImageFont.truetype(FONT, 40); f_tag = ImageFont.truetype(FONT, 26)
    f_big = ImageFont.truetype(FONT, 44); f_small = ImageFont.truetype(FONT, 22)
    wm = a1.logo_assets()
    real62 = None
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', str(OUT / 'picture.mp4')], stdin=subprocess.PIPE)
    for n in range(int(round(DUR * FPS))):
        t = n / FPS
        a, b, k, seg, mv = next(s for s in SHOTS if s[0] <= t < s[1]) if t < DUR else SHOTS[-1]
        if k == 'END':
            pic = a1.endcard(a, t, wm, f_big, f_small)
        else:
            if k not in cache: cache[k] = load(k)
            z0, z1, x0, x1, y0, y1 = mv; u = a1.ease((t - a) / (b - a))
            args = (z0 + (z1 - z0) * u, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u)
            pic = a1.view(cache[k], *args)
            if k == '6.2':
                if real62 is None: real62 = a1.load_path(P / 'assets/sheets/lay_song_workshop.png')
                pic = Image.blend(pic, a1.view(real62, *args), a1.ease(max(0, min(1, (t - a - 1.2) / 1.8))))
            if k == '1.2':
                pic = a1.grid_overlay(pic, a1.ease(min(1, (t - a) / 2.5)) * (1 - max(0, (t - b + .8) / .8)), phase=(t - a) * .15)
            if k == '8.1':
                pic = a1.grid_overlay(pic, a1.ease(max(0, min(1, (t - a - 3) / 4))), spacing=72)
            if 80.0 <= t < 84.5:   # 真空：画面微微压暗、去色
                g = pic.convert('L').convert('RGB'); pic = Image.blend(pic, g, 0.25)
        fr = Image.new('RGB', (W, H), (0, 0, 0)); fr.paste(pic, (0, PY)); d = ImageDraw.Draw(fr)
        for st, en, text in subs:
            if st <= t < en and not (k == 'END' and text.startswith('以天地')):
                al = min(1, (t - st) / .25, (en - t) / .25); c = int(235 * al); tw = d.textlength(text, font=f_sub)
                d.text(((W - tw) / 2, PY + PH - 78), text, font=f_sub, fill=(c, c, c), stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((30, 26), f'{seg}   {t:06.2f}s', font=f_tag, fill=(255, 205, 60))
        d.text((W - 360, 26), '动态分镜 v2 · 临时旁白/配乐', font=f_tag, fill=(160, 160, 160))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()


if __name__ == '__main__':
    assert all(abs(SHOTS[i][1] - SHOTS[i + 1][0]) < 1e-6 for i in range(len(SHOTS) - 1))
    subs = voice()
    if not (OUT / 'score.wav').exists(): score()
    mix(); picture(subs)
    final = OUT / 'yuanqi_animatic_v2.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'picture.mp4'), '-i', str(OUT / 'mix.wav'), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', str(final)], check=True)
    print(final)
