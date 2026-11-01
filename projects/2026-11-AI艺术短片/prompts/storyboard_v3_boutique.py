"""粗剪 v2 意见：1:37 / 1:42 的沿街店铺太土 → 改为商场里有设计感的高级丝绸店。先出 3 张小样给用户确认，再做视频。"""
LOOK = ("Cinematic still, 2.39:1, old spherical 50 mm prime, shallow depth of field, out-of-focus foreground, off-centre framing. "
        "Low-key and restrained like a quiet art-house film: dark warm-grey mid-tones, soft rolled-off highlights, low saturation, "
        "warm-neutral light from concealed architectural fixtures plus soft daylight from the mall atrium; light film grain, no HDR, no sharpening. "
        "No text, no logos, no readable signs, no mannequin faces.")
SHOP = ("A high-end contemporary Chinese silk boutique inside a quiet, upscale shopping mall: designed interior with travertine stone, "
        "dark walnut and brushed bronze, a low plinth with folded silk, a few silk garments hung far apart on a slim bronze rail, "
        "a long length of ivory silk damask draped from the ceiling, generous empty space, glass shopfront facing the mall corridor.")
PEOPLE = ("Real people, documentary feel: ordinary Chinese faces with real skin texture, natural unposed gestures, never looking at the camera, "
          "dressed in simple good-quality everyday clothes (not models, not advertising).")
FRAMES = {
 'sb3_boutique_open': f"{SHOP} Morning before the mall opens, the corridor outside still dim. A woman about forty, the shop owner, in a plain dark wool coat over a black top, "
                      f"slides the tall glass door open with one hand; behind her the boutique lights are coming on. Medium shot from the corridor, slightly behind her shoulder. {PEOPLE} {LOOK}",
 'sb3_boutique_family': f"{SHOP} Afternoon. A young woman in her late twenties and her mother in her fifties step through the glass door into the boutique, "
                        f"the mother reaching out to touch a silk scarf on the plinth. Wide shot from inside the shop, out-of-focus silk in the foreground. {PEOPLE} {LOOK}",
 'sb3_boutique_touch': f"{SHOP} Close-up: an older woman's hand with real wrinkles lifts the edge of an ivory silk damask with a subtle woven floral pattern; "
                       f"the silk catches the soft light; behind, out of focus, the shop assistant folds a scarf. {PEOPLE} {LOOK}",
}
