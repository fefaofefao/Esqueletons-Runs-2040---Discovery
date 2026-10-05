#!/usr/bin/env python3
"""Gera a UI: moldura 9-slice, controles de toque, ícones do topo, logo,
ícone do app e texturas de partículas. Tudo original."""
from pathlib import Path
from PIL import Image

from draw import new, put, rect, ellipse, outline, from_ascii, mix, bayer
from pixfont import PixFont

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / "assets" / "ui"
OUTL = (40, 30, 48)


def frame(fill, inner, accent):
    """Moldura 24x24 para StyleBoxTexture (margens de 6 px)."""
    img = new(24, 24)
    for y in range(24):
        for x in range(24):
            edge = min(x, y, 23 - x, 23 - y)
            if edge == 0:
                c = OUTL
            elif edge == 1:
                c = accent
            elif edge == 2:
                c = inner
            else:
                c = fill
            put(img, x, y, c)
    # cantos arredondados
    for (x, y) in [(0, 0), (23, 0), (0, 23), (23, 23)]:
        img.putpixel((x, y), (0, 0, 0, 0))
    for (x, y) in [(1, 1), (22, 1), (1, 22), (22, 22)]:
        img.putpixel((x, y), OUTL + (255,))
    return img


def dpad():
    s = 24
    img = new(s * 3, s * 3)
    base = (236, 236, 244)
    shade = (176, 180, 200)
    for (cx, cy) in [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]:
        rect(img, cx * s + 1, cy * s + 1, s - 2, s - 2, base)
    # preenche as junções
    rect(img, s, s - 1, s, s + 2, base)
    rect(img, s - 1, s, s + 2, s, base)
    # sombra inferior de cada braço
    for (cx, cy) in [(1, 0), (0, 1), (2, 1), (1, 2)]:
        rect(img, cx * s + 1, cy * s + s - 4, s - 2, 3, shade)
    ellipse(img, s * 1.5, s * 1.5, 5, 5, shade)
    # setas
    col = (90, 92, 120)
    for (cx, cy), (dx, dy) in {(1, 0): (0, -1), (1, 2): (0, 1), (0, 1): (-1, 0), (2, 1): (1, 0)}.items():
        mx, my = cx * s + s // 2, cy * s + s // 2 - 1
        for i in range(4):
            for j in range(-i, i + 1):
                if dx == 0:
                    put(img, mx + j, my + dy * (3 - i) - dy, col)
                else:
                    put(img, mx + dx * (3 - i) - dx, my + j, col)
    outline(img, OUTL)
    return img


def dpad_glow():
    img = new(22, 22)
    rect(img, 0, 0, 22, 22, (255, 255, 255, 110))
    return img


def round_button(letter, col, pressed=False):
    img = new(30, 30)
    body = col if not pressed else mix(col, (255, 255, 255), 0.35)
    ellipse(img, 15, 15, 13.5, 13.5, mix(col, (0, 0, 0), 0.35))
    ellipse(img, 15, 14 if not pressed else 15, 13, 12.5, body)
    ellipse(img, 11, 9, 4, 2.5, mix(body, (255, 255, 255), 0.5))
    outline(img, OUTL)
    f = PixFont()
    w = f.width(letter) - 1
    f.draw(img, 15 - w // 2, 7 + (0 if not pressed else 1), letter, (255, 255, 255, 255))
    return img


def pill(w, h, col):
    img = new(w, h)
    rect(img, 1, 0, w - 2, h, col)
    rect(img, 0, 1, w, h - 2, col)
    rect(img, 1, 1, w - 2, 1, mix(col, (255, 255, 255), 0.35))
    rect(img, 1, h - 2, w - 2, 1, mix(col, (0, 0, 0), 0.3))
    outline(img, OUTL)
    return img


def icon_menu():
    img = pill(22, 16, (70, 82, 120))
    for y in (4, 7, 10):
        rect(img, 6, y + 1, 11, 2, (236, 236, 244))
    return img


def icon_speed(on):
    col = (232, 160, 48) if on else (70, 82, 120)
    img = pill(26, 16, col)
    tri = (255, 255, 255) if on else (176, 180, 200)
    for ox in (7, 13):
        for y in range(7):
            for x in range(4 - abs(3 - y)):
                put(img, ox + x, 4 + y, tri)
    return img


def logo():
    f = PixFont()

    def scaled_text(text, scale, top_col, bot_col, spacing=2):
        w = f.width(text) + spacing * len(text)
        tmp = new(w + 2, 14)
        x = 1
        for ch in text:
            x = f.draw(tmp, x, 0, ch, (255, 255, 255, 255)) + spacing
        tmp = tmp.resize((tmp.width * scale, tmp.height * scale), Image.NEAREST)
        for y in range(tmp.height):
            for x in range(tmp.width):
                if tmp.getpixel((x, y))[3]:
                    t = max(0.0, min(1.0, (y - 2 * scale) / (7.0 * scale)))
                    tmp.putpixel((x, y), mix(top_col, bot_col, t))
        pad = new(tmp.width + 4, tmp.height + 4)
        # sombra projetada
        shadow = Image.new("RGBA", tmp.size, OUTL + (255,))
        pad.paste(shadow, (3, 3), tmp)
        pad.alpha_composite(tmp, (1, 1))
        outline(pad, OUTL)
        return pad

    l1 = scaled_text("ESQUELETONS", 2, (255, 252, 240), (200, 190, 168))
    l2 = scaled_text("RUNS", 2, (255, 252, 240), (200, 190, 168))
    l3 = scaled_text("2040", 3, (170, 255, 255), (30, 160, 200), spacing=1)
    W = max(l1.width, l2.width + l3.width + 4) + 4
    img = new(W, l1.height + l3.height)
    img.alpha_composite(l1, ((W - l1.width) // 2, 0))
    x0 = (W - (l2.width + 4 + l3.width)) // 2
    img.alpha_composite(l2, (x0, l1.height - 4 + (l3.height - l2.height) // 2))
    img.alpha_composite(l3, (x0 + l2.width + 4, l1.height - 8))
    return img.crop(img.getbbox())


SKULL = [
    "........oooooooooooooooo........",
    "......oowwwwwwwwwwwwwwwwoo......",
    ".....owwwwwwwwwwwwwwwwwwwwo.....",
    "....owwwwwwwwwwwwwwwwwwwwwwo....",
    "...owwwwwwwwwwwwwwwwwwwwwwwwo...",
    "...owwwwwwwwwwwwwwwwwwwwwwwWo...",
    "..owwwwwwwwwwwwwwwwwwwwwwwwwWo..",
    "..ovvvvvvvvvvvvvvvvvvvvvvvvvvo..",
    "..oVvvLLvvvvvvvvvvvvvvvvvvvvVo..",
    "..oVvLLvvvvvvvvvvvvvvvvvvvvvVo..",
    "..oVvvvvvvvvvvvvvvvvvvvvvvvvVo..",
    "..oVVVVVVVVVVVVVVVVVVVVVVVVVVo..",
    "..owwwwwwwwwwwwwwwwwwwwwwwwwWo..",
    "..owwwwwwwwwwwwwwwwwwwwwwwwwWo..",
    "...owwwwwwwwwwoowwwwwwwwwwwWo...",
    "...oWwwwwwwwwoooowwwwwwwwwWWo...",
    "....oWWwwwwwwoooowwwwwwwWWWo....",
    ".....oWWWwwwwwwwwwwwwwWWWWo.....",
    "......ooWWWWWWWWWWWWWWWWoo......",
    "........owwwwwwwwwwwwwwo........",
    "........owowowowowowowwo........",
    "........owowowowowowowWo........",
    ".........oWWWWWWWWWWWWo.........",
    "..........oooooooooooo..........",
]


SKULL_PAL = {"o": OUTL, "w": (246, 244, 236), "W": (196, 192, 184), "v": (70, 222, 232),
             "V": (32, 150, 176), "L": (230, 255, 255)}


def scene_bg(base):
    """Pôr do sol sobre o mar, em base x base pixels."""
    img = new(base, base)
    horizon = int(base * 0.65)
    for y in range(base):
        for x in range(base):
            if y < horizon:
                t = y / horizon
                c = mix((120, 96, 170), (250, 170, 90), min(1.0, t * 2.2)) if t < 0.45 else \
                    mix((250, 170, 90), (246, 120, 110), (t - 0.45) / 0.55)
            else:
                c = mix((58, 160, 192), (34, 100, 164), (y - horizon) / (base - horizon))
                if (x + y) % 7 == 0 and bayer(x, y) > 0.5:
                    c = mix(c, (138, 222, 226), 0.6)
            put(img, x, y, c)
    ellipse(img, base / 2, horizon, base * 0.22, base * 0.1, (255, 226, 150))
    return img


def app_icon(size):
    skull = from_ascii(SKULL, SKULL_PAL)
    base = 40
    img = scene_bg(base)
    img.alpha_composite(skull, (4, 9))
    scale = max(1, size // base)
    out = img.resize((base * scale, base * scale), Image.NEAREST)
    if out.size[0] != size:
        out = img.resize((size, size), Image.NEAREST)
    return out


def adaptive_fg(size=432):
    skull = from_ascii(SKULL, SKULL_PAL)
    scale = 8  # 32*8 = 256 px, dentro da zona segura de 288 px
    s = skull.resize((skull.width * scale, skull.height * scale), Image.NEAREST)
    img = new(size, size)
    img.alpha_composite(s, ((size - s.width) // 2, (size - s.height) // 2))
    return img


def adaptive_bg(size=432):
    return scene_bg(48).resize((size, size), Image.NEAREST)


def particles():
    out = {}
    leaf = new(4, 3)
    for (x, y, c) in [(0, 1, (70, 164, 84)), (1, 0, (118, 200, 98)), (2, 1, (70, 164, 84)), (1, 1, (118, 200, 98)),
                      (3, 2, (40, 118, 70)), (2, 2, (40, 118, 70))]:
        put(leaf, x, y, c)
    out["leaf"] = leaf
    spark = new(3, 3)
    for (x, y) in [(1, 0), (0, 1), (2, 1), (1, 2)]:
        put(spark, x, y, (255, 255, 230, 200))
    put(spark, 1, 1, (255, 255, 255))
    out["sparkle"] = spark
    dust = new(4, 4)
    ellipse(dust, 2, 2, 2, 2, (238, 222, 186, 220))
    out["dust"] = dust
    dot = new(1, 1)
    put(dot, 0, 0, (255, 255, 255))
    out["dot"] = dot
    return out


def main():
    UI.mkdir(parents=True, exist_ok=True)
    frame((250, 246, 234), (226, 232, 244), (84, 116, 172)).save(UI / "frame_light.png")
    frame((30, 34, 56), (44, 50, 80), (120, 150, 210)).save(UI / "frame_dark.png")
    frame((250, 246, 234), (238, 230, 200), (214, 158, 60)).save(UI / "frame_name.png")
    dpad().save(UI / "dpad.png")
    dpad_glow().save(UI / "dpad_glow.png")
    round_button("A", (210, 70, 80)).save(UI / "btn_a.png")
    round_button("A", (210, 70, 80), True).save(UI / "btn_a_pressed.png")
    round_button("B", (70, 110, 200)).save(UI / "btn_b.png")
    round_button("B", (70, 110, 200), True).save(UI / "btn_b_pressed.png")
    icon_menu().save(UI / "btn_menu.png")
    icon_speed(False).save(UI / "btn_speed_1x.png")
    icon_speed(True).save(UI / "btn_speed_2x.png")
    logo().save(UI / "logo.png")
    for name, img in particles().items():
        img.save(UI / f"particle_{name}.png")
    icons = ROOT / "assets" / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    app_icon(512).save(icons / "icon_512.png")
    app_icon(192).save(icons / "icon_192.png")
    adaptive_fg().save(icons / "icon_fg_432.png")
    adaptive_bg().save(icons / "icon_bg_432.png")
    app_icon(160).save(ROOT / "icon.png")
    print("UI gerada em", UI)


if __name__ == "__main__":
    main()
