"""Render pramaan_promo.html to MP4 (silent, 1080p).
Usage:
  python promo/src/render.py                      -> promo/Pramaan_Promo_60s.mp4 (60 fps)
  python promo/src/render.py --stills 3 22.5 38   -> PNG stills in promo/src/stills/
Needs: pip install playwright imageio-ffmpeg  (uses the installed Microsoft Edge; no browser download)
"""
import argparse, pathlib, subprocess, sys, time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
HTML = (HERE / "pramaan_promo.html").as_uri()
DUR = 60.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--out", default=str(HERE.parent / "Pramaan_Promo_60s.mp4"))
    ap.add_argument("--stills", type=float, nargs="*")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=DUR)
    a = ap.parse_args()
    with sync_playwright() as p:
        br = p.chromium.launch(channel="msedge", args=["--force-color-profile=srgb", "--hide-scrollbars"])
        page = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto(HTML)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        if a.stills is not None:
            d = HERE / "stills"; d.mkdir(exist_ok=True)
            for t in a.stills:
                page.evaluate(f"render({t})")
                page.screenshot(path=str(d / f"t{t:05.2f}.png"))
            print("stills ->", d); return
        n0, n1 = round(a.start * a.fps), round(a.end * a.fps)
        cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps),
               "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
               "-profile:v", "high", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
               "-movflags", "+faststart", a.out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(n0, n1):
            page.evaluate(f"render({i / a.fps})")
            ff.stdin.write(page.screenshot(type="png"))
            if i % 300 == 0:
                print(f"frame {i}/{n1}  {time.time() - t0:.0f}s", flush=True)
        ff.stdin.close(); ff.wait(); br.close()
        print("done ->", a.out, f"{time.time() - t0:.0f}s")

if __name__ == "__main__":
    sys.exit(main())
