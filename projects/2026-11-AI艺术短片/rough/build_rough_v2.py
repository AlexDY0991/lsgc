#!/usr/bin/env python3
"""第一集《源启》粗剪 v2：按配乐 M2（即梦 Seed Music，111.7 BPM）的真实节拍重剪；即梦配音（沉稳解说Pro）；新的高潮快切；精做 logo。

用法（仓库根目录）：/tmp/studio-tools/venv/bin/python -I projects/2026-11-AI艺术短片/rough/build_rough_v2.py OUTDIR
需要：video/r1/*.mp4（原始片段，tools/jm.py wait 可重新下载）、audio/*.wav、rough/logo/logo_v1.py 渲染出的 logo_v1.mp4（LOGO 环境变量指定）。
音乐结构（music_window.py 实测）：M2 在 57.2 / 66.6 / 84.6 / 109.6 s 有台阶式抬升，68–100 s 最响。片子时间 = 音乐时间：
  音乐整体延后 0.15 s 让拍点对上剪点（实测剪点比拍点晚约 150 ms）。高潮 60.17–76.30（30 拍，4→3→2→1 拍越切越快），76.54 爆点（实测强拍）；67.58/73.98/75.53/84.57 按实测起音微调，79.88 起真空（音乐静音），84.57 释放（音乐抬升点），109.57 logo。
"""
import os, subprocess, sys
from pathlib import Path

REPO = Path.cwd(); P = REPO / 'projects/2026-11-AI艺术短片'
sys.path.insert(0, str(REPO / 'tools')); from edl_check import check   # noqa: E402
OUT = Path(sys.argv[1]); SEG = OUT / 'seg'; SEG.mkdir(parents=True, exist_ok=True)
LOGO = Path(os.environ.get('LOGO', '/tmp/claude-0/-home-user-lsgc/5b7e00bb-f735-5086-b5d0-e4456ca7130d/scratchpad/logo/logo_v1.mp4'))
AU = P / 'audio'
W, H, FPS, PH = 1920, 1080, 24, 804
PY = (H - PH) // 2
FONT = '/tmp/studio-tools/fonts/NotoSerifSC-300.ttf'
R = lambda n: P / f'video/r1/{n}.mp4'
T10 = P / 'video/test/V10_climax_t1.mp4'
B = 0.5371   # 一拍

# (开始, 结束, 素材, 入点, 速度, 内容标签)
SHOTS = [
 (0.00, 7.00, R('V1_bamboo'), 0.5, 1, 'bamboo-grove'),
 (7.00, 10.00, R('V1_bamboo'), 8.5, 1, 'bamboo-node'),
 (10.00, 13.00, R('V2_cocoon'), 0.0, 1, 'pot'),
 (13.00, 18.00, R('V2_cocoon'), 3.0, 1, 'cocoon-lift'),
 (18.00, 21.00, R('V3_backstrap'), 0.3, 1, 'backstrap-wide'),
 (21.00, 23.00, R('V3_backstrap'), 5.0, 1, 'woven-edge'),
 (23.00, 25.00, R('V3_backstrap'), 7.0, 0.95, 'neo-lookup-setup'),
 (25.00, 30.00, R('V4_silkroad'), 0.0, 1, 'mountains'),
 (30.00, 32.50, R('V4_silkroad'), 5.5, 1, 'camel-silk'),
 (32.50, 35.00, R('V4_silkroad'), 10.3, 1, 'caravan'),
 (35.00, 38.00, R('V4_silkroad'), 14.5, 1, 'ferry'),
 (38.00, 41.00, R('V5_tang'), 0.0, 1, 'west-lake'),
 (41.00, 45.00, R('V17_tang_redo'), 0.0, 1, 'tang-weave'),
 (45.00, 47.00, R('V18_scroll_redo'), 0.0, 1, 'scroll'),
 (47.00, 52.00, R('V6b_painting'), 0.0, 1, 'painting-to-real'),
 (52.00, 55.00, R('V7a_drawloom'), 0.0, 1, 'drawboy'),
 (55.00, 58.00, R('V7a_drawloom'), 3.0, 1, 'song-weave'),
 (58.00, 60.17, R('V7b_silkwoman'), 0.5, 1, 'feed'),
 # 高潮「千年一梭」：4,4,3,3,2,2,2,2,1×8 拍；相邻两刀靠旋转 / 方向 / 上提 / 下压匹配
 (60.17, 62.32, R('V7b_silkwoman'), 3.2, 1, 'reel'),                 # 转轮
 (62.32, 64.47, R('V16_climax_modern'), 0.0, 0.907, 'handwheel'),     # 转轮 → 缝纫机手轮
 (64.47, 66.09, R('V3_backstrap'), 3.35, 1, 'backstrap-beat'),
 (66.09, 67.58, R('V14_climax_ancient'), 0.0, 1, 'tang-shuttle'),     # 右→左
 (67.58, 68.77, R('V14_climax_ancient'), 2.0, 1, 'song-reed'),        # 右→左
 (68.77, 69.85, R('V13_merchants'), 0.3, 1, 'fold'),
 (69.85, 70.92, R('V14_climax_ancient'), 4.0, 1, 'drawboy-pull'),     # 上提
 (70.92, 72.00, R('V13_merchants'), 3.8, 1, 'porter'),                # 上提 → 扛起
 (72.00, 72.54, R('V14_climax_ancient'), 6.0, 1, 'treadle'),          # 下压
 (72.54, 73.07, R('V5_tang'), 7.2, 1, 'reed-knock'),                  # 下压
 (73.07, 73.61, R('V16_climax_modern'), 2.05, 1, 'needle'),           # 下压
 (73.61, 74.02, R('V15_climax_silk'), 0.2, 1, 'cocoon-fingers'),
 (74.02, 74.69, R('V15_climax_silk'), 2.2, 1, 'reel-guide'),
 (74.69, 75.12, R('V16_climax_modern'), 4.1, 1, 'chalk'),             # 右→左
 (75.12, 75.53, R('V15_climax_silk'), 4.1, 1, 'silk-unroll'),         # 右→左
 (75.53, 76.54, R('V7b_silkwoman'), 5.77, 1, 'song-shears'),           # 南宋一剪
 (76.54, 78.36, R('V16_climax_modern'), 6.0, 1, 'modern-shears'),     # 爆点：同构图的今天一剪
 (78.36, 79.88, R('V11b_cut_lookup'), 1.95, 1, 'designer-cut'),
 # 真空
 (79.88, 83.60, R('V11b_cut_lookup'), 3.6, 1, 'designer-lookup'),
 (83.60, 84.57, R('V3_backstrap'), 8.93, 1, 'neo-lookup-echo'),
 # 释放
 (84.57, 87.10, R('V12c_people'), 0.0, 1, 'window-city'),
 (87.10, 91.60, R('V8a_ferry'), 0.0, 1, 'ferry-to-today'),
 (91.60, 94.10, R('V12c_people'), 3.2, 1, 'river-people'),
 (94.10, 96.10, R('V8b_cities'), 0.6, 1, 'yaou-shangsha'),
 (96.10, 98.50, R('V12c_people'), 6.3, 1, 'family'),
 (98.50, 100.00, R('V8b_cities'), 3.6, 1, 'nanjing-huanbei'),
 (100.00, 101.50, R('V8b_cities'), 6.6, 1, 'hangzhou-huanbei'),
 (101.50, 102.57, R('V12c_people'), 9.6, 1, 'merchant-shutter'),
 (102.57, 109.57, R('V9_night'), 0.0, 1, 'night-pullup'),
 (109.57, 118.00, LOGO, 0.0, 1, 'logo'),
]
DUR = 118.0
VO = [(1.5, 'A_l1', '天地有经纬，文明有脉络。'), (11.0, 'A_l2', '五千多年前，先民从一枚茧里，抽出了丝。'),
      (18.5, 'A_l3', '一经一纬，织成了绢；织机声里，一代传给一代。'), (28.0, 'A_l4', '大汉凿空，丝绸西出。过黄河，出河西，连起了东方与西方。'),
      (39.8, 'A_l5', '唐时杭州，红袖织绫，柿蒂花者尤佳。'), (47.6, 'A_l6', '南宋临安，从浴蚕到剪帛，二十四道工序，被画进了长卷。'),
      (80.4, 'A_lv', '五千年，这双手，从没有停下。'), (88.0, 'A_l7', '千年之后，经纬仍在。兰州、南京、杭州，城与城之间，人与人之间。'),
      (111.4, 'A_l8', '以天地经纬，织人间脉络。丽尚国潮。')]
ADJ = {i for i in range(1, len(SHOTS)) if Path(str(SHOTS[i][2])).name == Path(str(SHOTS[i - 1][2])).name}


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


def seg(i, a, b, src, sin, sp):
    out = SEG / f'{i:02d}.mp4'; d = b - a
    vf = (f"setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:-2:flags=lanczos,crop={W}:{PH},pad={W}:{H}:0:{PY}:black,setsar=1")
    af = f"atempo={sp},afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.15):.3f}:d=0.15" if sp != 1 else f"afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.15):.3f}:d=0.15"
    has_a = 'audio' in subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', str(src)], capture_output=True, text=True).stdout
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{sin:.3f}', '-t', f'{d * sp + 0.05:.3f}', '-i', str(src)]
    if not has_a:
        cmd += ['-f', 'lavfi', '-t', f'{d:.3f}', '-i', 'anullsrc=r=48000:cl=stereo']
    cmd += ['-vf', vf, '-t', f'{d:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p']
    cmd += (['-af', af] if has_a else ['-map', '0:v', '-map', '1:a']) + ['-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', str(out.with_suffix('.mov'))]
    subprocess.run(cmd, check=True)
    return out.with_suffix('.mov')


def main():
    print(check(SHOTS, DUR, max_uses=8, allow_adjacent=ADJ))
    for a, b, src, sin, sp, tag in SHOTS:
        need = sin + (b - a) * sp
        assert need <= dur(src) + 0.02, f'{tag}: needs {need:.2f}s of {Path(src).name} ({dur(src):.2f}s)'
    segs = [seg(i, *s[:5]) for i, s in enumerate(SHOTS)]
    (OUT / 'list.txt').write_text(''.join(f"file '{s}'\n" for s in segs))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(OUT / 'list.txt'), '-c', 'copy', str(OUT / 'cut.mov')], check=True)
    # ---- 声音：配乐（增益曲线）+ 配音 + 片段环境声 ----
    inputs = ['-i', str(OUT / 'cut.mov'), '-i', str(AU / 'M2_piano.wav')]
    chains = []
    duck = '+'.join(f'between(t,{t - 0.2:.2f},{t + dur(AU / (k + ".wav")) + 0.3:.2f})' for t, k, _ in VO if k not in ('A_lv', 'A_l8'))
    mvol = (f"if(lt(t,60.17),if({duck},0.32,0.55),"
            f"if(lt(t,76.54),0.62+0.5*(t-60.17)/16.37,"
            f"if(lt(t,79.88),1.15,"
            f"if(lt(t,84.57),0.0,"
            f"if(lt(t,109.57),if({duck},0.55,0.95),0.8)))))")
    chains.append(f"[1]aresample=48000,adelay=150|150,volume='{mvol}':eval=frame,afade=t=out:st={DUR - 1.2}:d=1.2[mus]")
    chains.append("[0:a]volume='if(between(t,79.88,84.57),0.25,0.38)':eval=frame[amb]")
    labs = []
    for i, (t, k, _) in enumerate(VO, 2):
        inputs += ['-i', str(AU / f'{k}.wav')]
        chains.append(f"[{i}]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=1.6,adelay={int(t * 1000)}|{int(t * 1000)}[v{i}]"); labs.append(f'[v{i}]')
    chains.append(f"[mus][amb]{''.join(labs)}amix=inputs={2 + len(labs)}:normalize=0:duration=first[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(chains), '-map', '[mx]', '-t', str(DUR), '-ar', '48000', str(OUT / 'mix_raw.wav')], check=True)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(OUT / 'mix_raw.wav'), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    lufs = float(r[r.rindex('I:'):].split()[1])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'mix_raw.wav'), '-af',
                    f'volume={-14 - lufs:.2f}dB,aresample=192000,alimiter=limit=0.82:attack=1:release=60:level=false,aresample=48000', str(OUT / 'mix.wav')], check=True)
    # ---- 字幕 + 角标 ----
    filt = []
    for n, (t, k, text) in enumerate(VO):
        if k == 'A_l8':
            continue   # 结尾句由 logo 标题卡承担
        tf = OUT / f'sub{n}.txt'; tf.write_text(text)
        e = t + dur(AU / f'{k}.wav') + 0.3
        filt.append(f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=38:fontcolor=white@0.92:borderw=1.5:bordercolor=black@0.7:"
                    f"x=(w-text_w)/2:y={PY + PH - 76}:enable='between(t,{t:.2f},{e:.2f})'")
    filt.append(f"drawtext=fontfile=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc:text='粗剪 v2 · 样片 480p · 配乐和配音为即梦生成的草稿':fontsize=20:fontcolor=gray:x=w-tw-30:y=30")
    final = OUT / 'yuanqi_rough_v2.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'cut.mov'), '-i', str(OUT / 'mix.wav'), '-map', '0:v', '-map', '1:a', '-vf', ','.join(filt),
                    '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), str(final)], check=True)
    print(final)


if __name__ == '__main__':
    main()
