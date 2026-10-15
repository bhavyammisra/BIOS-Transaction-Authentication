# Promo video

- **`Pramaan_Promo_60s.mp4`**: the 60 s promo (1080p, 60 fps, H.264, no audio).
- **`SCRIPT.md`**: timed voiceover script and on-screen beats, plus how to add the VO.
- **`src/`**: source. `pramaan_promo.html` is the whole animation (`render(t)` draws time `t`); open it in a browser with `#24.5` on the URL to see one frame.

Re-render after editing the HTML:
```
pip install playwright imageio-ffmpeg
python promo/src/render.py                    # full video, ~10 min
python promo/src/render.py --stills 5 24 38   # PNG previews in promo/src/stills/
```
Uses the installed Microsoft Edge, so no browser download is needed.
