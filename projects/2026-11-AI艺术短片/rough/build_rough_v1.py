#!/usr/bin/env python3
"""第一集《源启》粗剪 v1：即梦样片（480p）按动态分镜 v2 的时间线剪成 118 秒，配动态分镜 v2 的临时旁白和配乐。

用法（仓库根目录）：/tmp/studio-tools/venv/bin/python -I projects/2026-11-AI艺术短片/rough/build_rough_v1.py OUTDIR
需要：video/r1/*.mp4、video/test/V10_climax_t1.mp4（原始片段，可用 tools/jm.py wait 重新下载）、
     动态分镜 v2 的输出目录（mix.wav 和 l*.wav），默认在 scratchpad，可用 ANIM_V2 环境变量指定。
"""
import importlib.util, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path.cwd(); P = REPO / 'projects/2026-11-AI艺术短片'
sys.path.insert(0, str(REPO / 'tools')); from edl_check import check   # noqa: E402
OUT = Path(sys.argv[1]); SEG = OUT / 'seg'; SEG.mkdir(parents=True, exist_ok=True)
ANIM = Path(os.environ.get('ANIM_V2', '/tmp/claude-0/-home-user-lsgc/5b7e00bb-f735-5086-b5d0-e4456ca7130d/scratchpad/anim_v2'))
R1, T = P / 'video/r1', P / 'video/test'
W, H, FPS = 1920, 1080, 24
PH = 804; PY = (H - PH) // 2
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
END = 'END'

def v(n): return R1 / f'{n}.mp4'

# (片中开始, 片中结束, 素材, 入点, 速度, 内容标签)
SHOTS = [
 # 序
 (0.0, 7.0, v('V1_bamboo'), 0.5, 1, 'bamboo-grove'),
 (7.0, 10.0, v('V1_bamboo'), 8.5, 1, 'bamboo-node'),
 # 起
 (10.0, 13.0, v('V2_cocoon'), 0.0, 1, 'pot'),
 (13.0, 18.0, v('V2_cocoon'), 3.0, 1, 'cocoon-lift'),
 (18.0, 21.0, v('V3_backstrap'), 0.3, 1, 'backstrap-wide'),
 (21.0, 23.0, v('V3_backstrap'), 5.0, 1, 'woven-edge'),
 (23.0, 25.0, v('V3_backstrap'), 7.0, 1, 'neo-lookup-setup'),
 (25.0, 30.0, v('V4_silkroad'), 0.0, 1, 'mountains'),
 (30.0, 32.5, v('V4_silkroad'), 5.5, 1, 'camel-silk'),
 (32.5, 35.0, v('V4_silkroad'), 10.3, 1, 'caravan'),
 (35.0, 38.0, v('V4_silkroad'), 14.5, 1, 'ferry'),
 # 承
 (38.0, 41.0, v('V5_tang'), 0.0, 1, 'west-lake'),
 (41.0, 45.0, v('V5_tang'), 3.0, 1, 'tang-weave'),
 (45.0, 47.0, v('V6a_scroll'), 0.0, 1, 'scroll'),
 (47.0, 52.0, v('V6b_painting'), 0.0, 1, 'painting-to-real'),
 (52.0, 55.0, v('V7a_drawloom'), 0.0, 1, 'drawboy'),
 (55.0, 58.0, v('V7a_drawloom'), 3.0, 1, 'song-weave'),
 (58.0, 60.0, v('V7b_silkwoman'), 0.5, 1, 'feed'),
 # 高潮：千年一梭（越切越快）
 (60.0, 62.0, v('V7b_silkwoman'), 3.2, 1, 'reel'),
 (62.0, 63.6, v('V3_backstrap'), 3.4, 1, 'backstrap-beat'),
 (63.6, 65.0, v('V5_tang'), 7.2, 1, 'damask'),
 (65.0, 66.2, v('V13_merchants'), 0.3, 1, 'fold'),
 (66.2, 67.3, T / 'V10_climax_t1.mp4', 6.2, 1, 'drawboy-echo'),
 (67.3, 68.3, v('V13_merchants'), 3.8, 1, 'porter'),
 (68.3, 69.2, T / 'V10_climax_t1.mp4', 4.4, 1, 'tang-echo'),
 (69.2, 70.0, v('V4_silkroad'), 8.1, 1, 'camel-silk-2'),
 (70.0, 70.7, T / 'V10_climax_t1.mp4', 8.6, 1, 'fold-echo'),
 (70.7, 71.4, v('V5_tang'), 8.7, 1, 'damask-2'),
 (71.4, 72.0, T / 'V10_climax_t1.mp4', 12.4, 1, 'porter-echo'),
 (72.0, 72.6, v('V13_merchants'), 1.6, 1, 'fold-2'),
 (72.6, 73.2, T / 'V10_climax_t1.mp4', 0.4, 1, 'reel-echo'),
 (73.2, 73.8, v('V7b_silkwoman'), 5.3, 1, 'reel-2'),
 (73.8, 74.4, T / 'V10_climax_t1.mp4', 7.4, 1, 'drawboy-echo2'),
 (74.4, 75.0, v('V5_tang'), 9.4, 1, 'damask-3'),
 (75.0, 76.5, v('V7b_silkwoman'), 6.0, 1, 'song-cut'),
 (76.5, 80.0, v('V11b_cut_lookup'), 0.0, 1, 'designer-cut'),
 # 真空
 (80.0, 83.5, v('V11b_cut_lookup'), 3.6, 1, 'designer-lookup'),
 (83.5, 84.5, v('V3_backstrap'), 9.0, 1, 'neo-lookup-echo'),
 # 释放
 (84.5, 87.5, v('V12c_people'), 0.0, 1, 'window-city'),
 (87.5, 92.5, v('V8a_ferry'), 0.0, 1, 'ferry-to-today'),
 (92.5, 95.0, v('V12c_people'), 3.2, 1, 'river-people'),
 (95.0, 97.0, v('V8b_cities'), 0.6, 1, 'yaou-shangsha'),
 (97.0, 99.5, v('V12c_people'), 6.3, 1, 'family'),
 (99.5, 101.0, v('V8b_cities'), 3.6, 1, 'nanjing-huanbei'),
 (101.0, 102.5, v('V8b_cities'), 6.6, 1, 'hangzhou-huanbei'),
 (102.5, 104.0, v('V12c_people'), 9.6, 1, 'merchant-shutter'),
 # 收
 (104.0, 111.0, v('V9_night'), 0.0, 1, 'night-pullup'),
 (111.0, 118.0, END, 0.0, 1, 'logo'),
]
DUR = 118.0
# 同一条生成里本来就是连续的多镜头，允许相邻
ADJ = {i for i in range(1, len(SHOTS)) if Path(str(SHOTS[i][2])).name == Path(str(SHOTS[i - 1][2])).name}


def seg(i, a, b, src, sin, speed):
    out = SEG / f'{i:02d}.mp4'
    vf = (f"fps={FPS},scale={W}:-2:flags=lanczos,crop={W}:{PH},"
          f"pad={W}:{H}:0:{PY}:black,setsar=1")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{sin:.3f}', '-i', str(src), '-t', f'{(b - a) * speed:.3f}',
                    '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), str(out)], check=True)
    return out


def endcard_seg(i, a, b):
    spec = importlib.util.spec_from_file_location('a1', P / 'animatic/animatic_v1.py')
    saved = sys.argv[:]; sys.argv = [sys.argv[0], str(OUT / 'a1tmp')]
    a1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a1); sys.argv = saved
    wm = a1.logo_assets()
    fb, fs = ImageFont.truetype(FONT, 44), ImageFont.truetype(FONT, 22)
    out = SEG / f'{i:02d}.mp4'
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    for n in range(int(round((b - a) * FPS))):
        pic = a1.endcard(0.0, n / FPS, wm, fb, fs).resize((W, PH))
        fr = Image.new('RGB', (W, H)); fr.paste(pic, (0, PY)); ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    return out


def subtitles():
    import soundfile as sf
    spec = importlib.util.spec_from_file_location('a2', P / 'animatic/animatic_v2.py')
    src = (P / 'animatic/animatic_v2.py').read_text()
    lines = eval(src[src.index('LINES = [') + 8: src.index(']', src.index('LINES = [')) + 1])
    subs = []
    for t, key, text in lines:
        info = sf.info(str(ANIM / f'{key}.wav'))
        if key != 'l8':   # 结尾句在标题卡上，不再出字幕
            subs.append((t, t + info.duration + 0.4, text))
    return subs


if __name__ == '__main__':
    print(check([s for s in SHOTS if s[2] != END] + [(111.0, 118.0, 'END.png', 0.0, 1, 'logo')], DUR,
                max_uses=8, allow_adjacent=ADJ))
    segs = [endcard_seg(i, a, b) if src == END else seg(i, a, b, src, sin, sp) for i, (a, b, src, sin, sp, tag) in enumerate(SHOTS)]
    (OUT / 'list.txt').write_text(''.join(f"file '{s}'\n" for s in segs))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(OUT / 'list.txt'), '-c', 'copy', str(OUT / 'picture.mp4')], check=True)
    # 字幕 + 角标
    filt = []
    for k, (a, b, text) in enumerate(subtitles()):
        tf = OUT / f'sub{k}.txt'; tf.write_text(text)
        filt.append(f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=40:fontcolor=white:borderw=2:bordercolor=black@0.8:"
                    f"x=(w-text_w)/2:y={PY + PH - 80}:enable='between(t,{a:.2f},{b:.2f})'")
    filt.append(f"drawtext=fontfile={FONT}:text='粗剪 v1 · 样片 480p · 临时旁白和配乐':fontsize=22:fontcolor=gray:x=w-tw-30:y=30")
    final = OUT / 'yuanqi_rough_v1.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'picture.mp4'), '-i', str(ANIM / 'mix.wav'), '-vf', ','.join(filt),
                    '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), '-shortest', str(final)], check=True)
    print(final)
