#!/usr/bin/env python3
"""Vídeos de anúncio (10 s) a partir de uma gravação real do jogo.

1. Grave as cenas (gameplay de verdade, 30 fps fixos):
   xvfb-run -a -s "-screen 0 1280x720x24" godot --rendering-driver opengl3 --resolution 1280x720 \\
     --write-movie DIR/raw.avi --fixed-fps 30 res://tools/screenshots/capture.tscn -- --ad --out=DIR
2. Extraia os quadros: ffmpeg -i DIR/raw.avi -start_number 0 DIR/frames/%05d.png
3. python3 tools/video/make_ads.py DIR/frames OUT_DIR

Gera, para cada roteiro, a versão vertical 9:16 (1080×1920) e a horizontal 16:9 (1920×1080),
em MP4 H.264 + AAC, prontas para subir no YouTube e usar no Google Ads.
Os números de quadro abaixo correspondem à gravação do modo --ad (seeds fixas).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FPS = 30
FONT = ROOT / "assets/fonts/nunito/Nunito.ttf"
WHITE = (255, 255, 255)
YELLOW = (255, 214, 64)
INK = (34, 16, 52)
CTA = (255, 92, 56)

# (quadros de origem, recorte em coords 320×180 ou None = tela toda, duração em quadros, título)
SCRIPTS = {
    "A_aniversario": {
        "music": "aniversario.ogg+batalha.ogg",
        "shots": [
            (range(1012, 1062), (120, 30, 280, 120), 60, ["SEU ESQUELETO", "FAZ ANIVERSÁRIO!"]),
            (range(1062, 1150), (120, 30, 280, 120), 48, ["...E CRESCE", "DE VERDADE!"]),
            (range(436, 500), None, 48, ["ACHE OS RAROS", "DOURADOS"]),
            (range(568, 640), None, 72, ["BATALHAS", "EM DUPLA"]),
        ],
        "end": ["JOGUE GRÁTIS"],
    },
    "B_rei": {
        "music": "chefe.ogg",
        "shots": [
            (range(1595, 1660), (168, 55, 312, 136), 66, ["O REI ESQUELETO", "DOMINOU O MUNDO"]),
            (range(436, 502), None, 54, ["RECRUTE", "95 ESQUELETOS"]),
            (list(range(1794, 1828)) + list(range(1916, 1975)), None, 108, ["SÓ VOCÊ", "PODE DETÊ-LO"]),
        ],
        "end": ["SALVE O MUNDO", "JOGUE GRÁTIS"],
    },
}
END_FRAMES = 72
TAG = "GRÁTIS NA GOOGLE PLAY"


def font(size: int, weight: int = 950) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([weight])
    return f


def ease_pop(t: float) -> float:
    """0→1 com um leve exagero (0,7 → 1,08 → 1,0)."""
    if t >= 1:
        return 1.0
    if t < 0.6:
        return 0.7 + (1.08 - 0.7) * (t / 0.6)
    return 1.08 - 0.08 * ((t - 0.6) / 0.4)


def text_img(lines, size, colors, stroke=10) -> Image.Image:
    f = font(size)
    boxes = [f.getbbox(l, stroke_width=stroke) for l in lines]
    w = max(b[2] - b[0] for b in boxes)
    lh = int(size * 1.12)
    im = Image.new("RGBA", (w + 20, lh * len(lines) + stroke * 2 + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        b = boxes[i]
        x = (im.width - (b[2] - b[0])) // 2 - b[0]
        d.text((x, i * lh + stroke), l, font=f, fill=colors[i % len(colors)], stroke_width=stroke, stroke_fill=INK)
    return im


def fit_text(lines, max_w, size, colors) -> Image.Image:
    im = text_img(lines, size, colors)
    while im.width > max_w and size > 30:
        size -= 6
        im = text_img(lines, size, colors)
    return im


def paste_scaled(dst, im, cx, cy, scale):
    if scale != 1:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    dst.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def pill(text, size, pad=(46, 22)) -> Image.Image:
    f = font(size)
    b = f.getbbox(text)
    w, h = b[2] - b[0] + pad[0] * 2, b[3] - b[1] + pad[1] * 2
    im = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 10, w + 6, h + 10), radius=h // 2, fill=(120, 30, 20, 255))
    d.rounded_rectangle((6, 4, w + 6, h + 4), radius=h // 2, fill=CTA + (255,), outline=WHITE, width=4)
    d.text((6 + pad[0] - b[0], 4 + pad[1] - b[1]), text, font=f, fill=WHITE)
    return im


def cover(im: Image.Image, size) -> Image.Image:
    W, H = size
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.BILINEAR)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def title_art() -> Image.Image:
    t = ROOT / "assets/title"
    scene = Image.open(t / "bg.png").convert("RGBA")
    for layer in ("clouds.png", "castle.png", "fore.png"):
        scene.alpha_composite(Image.open(t / layer).convert("RGBA"))
    return scene


def resample(frames, n):
    frames = list(frames)
    return [frames[min(len(frames) - 1, int(i * len(frames) / n))] for i in range(n)]


def game_frame(src: Path, crop):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    return im


def render(name, spec, frames_dir: Path, out: Path, vertical: bool):
    W, H = (1080, 1920) if vertical else (1920, 1080)
    tmp = Path(tempfile.mkdtemp(prefix=f"ad_{name}_"))
    tag = pill(TAG, 46 if vertical else 40)
    n = 0
    for frames, crop, dur, headline in spec["shots"]:
        head = fit_text(headline if vertical else [" ".join(headline)], W - 120 if vertical else 1700, 104 if vertical else 96, [WHITE, YELLOW])
        for k, f in enumerate(resample(frames, dur)):
            g = game_frame(frames_dir / f"{f:05d}.png", crop)
            if vertical:
                canvas = cover(g, (W, H)).filter(ImageFilter.GaussianBlur(28)).convert("RGBA")
                canvas.alpha_composite(Image.new("RGBA", (W, H), (20, 8, 34, 150)))
                gw = W - 40
                gh = int(gw * g.height / g.width)
                big = g.resize((gw, gh), Image.NEAREST).convert("RGBA")
                y0 = 700
                d = ImageDraw.Draw(canvas)
                d.rounded_rectangle((14, y0 - 6, W - 14, y0 + gh + 6), radius=18, fill=WHITE)
                canvas.alpha_composite(big, (20, y0))
                paste_scaled(canvas, head, W / 2, 400, ease_pop(k / 8))
                canvas.alpha_composite(tag, ((W - tag.width) // 2, y0 + gh + 70))
            else:
                canvas = cover(g, (W, H)).filter(ImageFilter.GaussianBlur(28)).convert("RGBA")
                canvas.alpha_composite(Image.new("RGBA", (W, H), (20, 8, 34, 150)))
                gw, gh = 1344, 756
                big = g.resize((gw, gh), Image.NEAREST).convert("RGBA")
                x0, y0 = (W - gw) // 2, 290
                d = ImageDraw.Draw(canvas)
                d.rounded_rectangle((x0 - 6, y0 - 6, x0 + gw + 6, y0 + gh + 6), radius=16, fill=WHITE)
                canvas.alpha_composite(big, (x0, y0))
                paste_scaled(canvas, head, W / 2, 145, ease_pop(k / 8))
            canvas.convert("RGB").save(tmp / f"{n:05d}.png")
            n += 1
    # cartão final: arte HD da abertura, logo, ícone e botão
    art = cover(title_art(), (W, H)).convert("RGBA")
    art.alpha_composite(Image.new("RGBA", (W, H), (20, 8, 34, 90)))
    logo = Image.open(ROOT / "assets/title/logo.png").convert("RGBA")
    logo = logo.resize((int(W * (0.9 if vertical else 0.55)), int(W * (0.9 if vertical else 0.55) * logo.height / logo.width)), Image.LANCZOS)
    icon = Image.open(ROOT / "store/graphics/icon_512.png").convert("RGBA").resize((220, 220) if vertical else (170, 170), Image.LANCZOS)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, icon.width, icon.height), radius=icon.width // 5, fill=255)
    icon.putalpha(mask)
    extra = spec["end"][:-1]
    sub = fit_text(extra, W - 120, 84 if vertical else 70, [YELLOW]) if extra else None
    btn = pill(spec["end"][-1], 84 if vertical else 66, pad=(70, 30))
    store = text_img(["Disponível na Google Play"], 46 if vertical else 40, [WHITE], stroke=6)
    for k in range(END_FRAMES):
        c = art.copy()
        if vertical:
            paste_scaled(c, logo, W / 2, 560, ease_pop(k / 10))
            c.alpha_composite(icon, ((W - icon.width) // 2, 860))
            if sub:
                paste_scaled(c, sub, W / 2, 1190, ease_pop(max(0, k - 6) / 8))
            pulse = 1 + 0.06 * abs(((k / 15) % 2) - 1)
            paste_scaled(c, btn, W / 2, 1400, ease_pop(max(0, k - 10) / 8) * pulse)
            c.alpha_composite(store, ((W - store.width) // 2, 1520))
        else:
            paste_scaled(c, logo, W / 2, 300, ease_pop(k / 10))
            c.alpha_composite(icon, ((W - icon.width) // 2, 520))
            if sub:
                paste_scaled(c, sub, W / 2, 760, ease_pop(max(0, k - 6) / 8))
            pulse = 1 + 0.06 * abs(((k / 15) % 2) - 1)
            paste_scaled(c, btn, W / 2, 890 if sub else 800, ease_pop(max(0, k - 10) / 8) * pulse)
            c.alpha_composite(store, ((W - store.width) // 2, 985 if sub else 900))
        c.convert("RGB").save(tmp / f"{n:05d}.png")
        n += 1
    dur = n / FPS
    music = spec["music"].split("+")
    mdir = ROOT / "assets/music"
    if len(music) == 2:
        # vinheta de aniversário nos 3,6 s iniciais, depois o tema de batalha
        afilter = (f"[1:a]atrim=0:3.6,afade=t=out:st=3.3:d=0.3[a1];[2:a]atrim=0:{dur - 3.6:.2f},asetpts=PTS-STARTPTS,"
                   f"afade=t=in:d=0.2,afade=t=out:st={dur - 3.6 - 0.6:.2f}:d=0.6[a2];[a1][a2]concat=n=2:v=0:a=1[a]")
        inputs = ["-i", str(mdir / music[0]), "-i", str(mdir / music[1])]
    else:
        afilter = f"[1:a]atrim=0:{dur:.2f},afade=t=out:st={dur - 0.6:.2f}:d=0.6[a]"
        inputs = ["-i", str(mdir / music[0])]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(tmp / "%05d.png"), *inputs,
                    "-filter_complex", afilter, "-map", "0:v", "-map", "[a]",
                    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{dur:.2f}", str(out)], check=True)
    print(f"{out.name}: {dur:.1f} s, {W}×{H}")


def main() -> int:
    frames_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, spec in SCRIPTS.items():
        for vertical in (True, False):
            render(name, spec, frames_dir, out_dir / f"esqueletons_{name}_{'9x16' if vertical else '16x9'}.mp4", vertical)
    return 0


if __name__ == "__main__":
    sys.exit(main())
