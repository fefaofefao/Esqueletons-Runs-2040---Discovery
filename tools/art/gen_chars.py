#!/usr/bin/env python3
"""Gera as folhas de sprite dos personagens humanos (16x24 por quadro).

Folha: colunas = quadros, linhas = direções (baixo, esquerda, direita, cima).
A direita é o espelho da esquerda. Pixel art original desenhada em ASCII.
"""
from pathlib import Path
from draw import from_ascii, mirror, new

ROOT = Path(__file__).resolve().parents[2]
FW, FH = 16, 24

# ------------------------------------------------------------------ Protagonista (2040)
P_PAL = {
    "o": (36, 28, 44), "h": (88, 56, 44), "H": (128, 86, 60),
    "v": (70, 222, 232), "V": (32, 150, 176), "L": (220, 255, 255),
    "s": (244, 202, 166), "S": (212, 160, 126), "e": (36, 28, 44), "m": (190, 110, 100),
    "c": (66, 86, 128), "C": (44, 58, 92), "l": (80, 236, 236),
    "b": (226, 120, 60), "B": (176, 82, 44),
    "p": (54, 56, 76), "P": (38, 38, 54), "k": (236, 236, 244), "K": (166, 170, 190),
}

P_DOWN_TOP = [
    "................",
    "....oooooooo....",
    "...ohhhhhhhho...",
    "..ohhhHHHhhhho..",
    "..ohvvvvvvvvho..",
    "..oVvLvvvvvvVo..",
    "..ohssssssssho..",
    "..ohsessssesho..",
    "..oSsessssesSo..",
    "...oSssmmssSo...",
    "....oSssssSo....",
    ".....oooooo.....",
    "...occcllccco...",
    "..oCcccLlcccCo..",
    "..oCcCcLlcCcCo..",
    "..oCcCcllcCcCo..",
    "..osCcclLccCso..",
    "...oCCCCCCCCo...",
]
P_DOWN_LEGS = {
    "stand": [
        "...oppppppppo...",
        "...opppoopppo...",
        "...oPpo..oPpo...",
        "...oPpo..oPpo...",
        "..okkKo..okkKo..",
        "..ooooo..ooooo..",
    ],
    "step": [
        "...oppppppppo...",
        "...opppoopppo...",
        "...oPpo..oPpo...",
        "..okkKo..oPpo...",
        "..ooooo.okkKo...",
        "........ooooo...",
    ],
}

P_UP_TOP = [
    "................",
    "....oooooooo....",
    "...ohhhhhhhho...",
    "..ohhhHHHhhhho..",
    "..ohhhhhhhhhho..",
    "..oVvvvvvvvvVo..",
    "..ohhhhHHhhhho..",
    "..ohhhhhhhhhho..",
    "..oHhhhhhhhhHo..",
    "...oHhhhhhhHo...",
    "....oSssssSo....",
    ".....oooooo.....",
    "...occcccccco...",
    "..oCobbbbbbocCo.",
    "..oCobBbbBbocCo.",
    "..oCobbbbbbocCo.",
    "..osobBBBBbocso.",
    "...oCooooooCo...",
]

P_LEFT_TOP = [
    "................",
    ".....ooooooo....",
    "....ohhhhhhho...",
    "...ohhhhHHhhho..",
    "..ovvvvvvvhhho..",
    "..oLvvvvVVhhho..",
    "..osssssshhhho..",
    "..oesssssShhho..",
    "..oesssssShho...",
    ".ossssssSSho....",
    "..omsssSSo......",
    "...ooooooo......",
    "....occccco.....",
    "...occllcCbo....",
    "...occcLcCbbo...",
    "...ocscccCbbo...",
    "...oCssccCbBo...",
    "....oCCCCCBo....",
]
P_LEFT_LEGS = {
    "stand": [
        "....oppppppo....",
        "....oppPppo.....",
        ".....opPpo......",
        ".....oPPpo......",
        "....okkkKo......",
        "....oooooo......",
    ],
    "step": [
        "....oppppppo....",
        "...opppoPppo....",
        "..oppo..oPpo....",
        "..oPo...oPPo....",
        ".okkKo..okkKo...",
        ".ooooo..ooooo...",
    ],
    "step2": [
        "....oppppppo....",
        "....oppPPpo.....",
        "....opPPpo......",
        "...oPPpo........",
        "..okkkKo........",
        "..oooooo........",
    ],
}

# ------------------------------------------------------------------ Bento (pescador idoso)
B_PAL = {
    "o": (36, 28, 44), "y": (228, 196, 116), "Y": (184, 146, 74), "r": (178, 64, 50),
    "s": (214, 154, 110), "S": (176, 116, 80), "e": (36, 28, 44),
    "w": (238, 238, 242), "W": (188, 190, 206),
    "c": (78, 122, 170), "C": (54, 90, 132), "t": (232, 232, 238),
    "v": (128, 88, 58), "V": (96, 64, 42),
    "p": (98, 86, 74), "P": (72, 62, 54), "k": (76, 54, 42), "K": (52, 38, 30),
    "n": (156, 108, 62),
}

B_DOWN = [
    "................",
    "......oooo......",
    "....ooyyyyoo....",
    "...oyyyYYyyyo...",
    "..oyrrrrrrrryo..",
    "ooyyyyyyyyyyyyoo",
    ".oYYYYYYYYYYYYo.",
    "..oSSSSSSSSSSo..",
    "..osseesseesso..",
    "..oswwssssswso..",
    "..owwwwsswwwwo..",
    "..oWwwwwwwwwWo..",
    "..ovoWwwwwWovo..",
    "..ovvcotocvvvo..",
    ".osvvctctcvvsno.",
    ".osVvcctccvVsno.",
    "..oVvctctcvVon..",
    "...oVVVVVVVVon..",
    "...opppppppppn..",
    "...opppoopppon..",
    "...oPpo..oPpo.n.",
    "...oPpo..oPpo.n.",
    "..okkKo..okkKon.",
    "..ooooo..ooooo..",
]
B_UP = [
    "................",
    "......oooo......",
    "....ooyyyyoo....",
    "...oyyyYYyyyo...",
    "..oyrrrrrrrryo..",
    "ooyyyyyyyyyyyyoo",
    ".oYYYYYYYYYYYYo.",
    "..owWWWWWWWWwo..",
    "..owwwwwwwwwwo..",
    "..oSwwwwwwwwSo..",
    "...oSSSSSSSSo...",
    "...owwwwwwwwo...",
    "..ovvvvvvvvvvo..",
    "..ovvvvVVvvvvo..",
    ".osvvvvvvvvvvso.",
    ".osVvvvvvvvvVso.",
    "..oVvvvvvvvvVo..",
    "...oVVVVVVVVo...",
    "...oppppppppo...",
    "...opppoopppo...",
    "...oPpo..oPpo...",
    "...oPpo..oPpo...",
    "..okkKo..okkKo..",
    "..ooooo..ooooo..",
]
B_LEFT = [
    "................",
    "......oooo......",
    ".....oyyyyoo....",
    "....oyyyYYyyo...",
    "....orrrrrrro...",
    "ooyyyyyyyyyyyo..",
    ".oYYYYYYYYYYYo..",
    "...oSSSSSSwwo...",
    "...oesssswwwo...",
    "..ossssswwwo....",
    "..owwwwswwwo....",
    "...owwwwwwo.....",
    "....oWwwWo......",
    "....ocvvvvo.....",
    "...otcvvvVvo....",
    "...oscvvvVvo....",
    "..nosvvvvVo.....",
    "..n.oVVVVVo.....",
    "..n.opppppo.....",
    "..n.oppPpo......",
    "..n..opPpo......",
    "..n..oPPpo......",
    "..n.okkkKo......",
    "....oooooo......",
]


def build_frame(top, legs):
    return from_ascii(top + legs, P_PAL)


def bob(img, dy):
    """Desloca o quadro dy px para cima (balanço do passo)."""
    out = new(img.width, img.height)
    out.alpha_composite(img.crop((0, dy, img.width, img.height)), (0, 0))
    # mantém os pés no chão: recompõe as 4 últimas linhas originais
    out.alpha_composite(img.crop((0, img.height - 4, img.width, img.height)), (0, img.height - 4))
    return out


def player_sheet():
    down = [build_frame(P_DOWN_TOP, P_DOWN_LEGS["stand"]),
            bob(build_frame(P_DOWN_TOP, P_DOWN_LEGS["step"]), 1),
            bob(mirror(build_frame(P_DOWN_TOP, P_DOWN_LEGS["step"])), 1)]
    # a cabeça no espelho fica idêntica (simétrica); o espelho só inverte a perna
    up = [from_ascii(P_UP_TOP + P_DOWN_LEGS["stand"], P_PAL),
          bob(from_ascii(P_UP_TOP + P_DOWN_LEGS["step"], P_PAL), 1),
          bob(mirror(from_ascii(P_UP_TOP + P_DOWN_LEGS["step"], P_PAL)), 1)]
    left = [build_frame(P_LEFT_TOP, P_LEFT_LEGS["stand"]),
            bob(build_frame(P_LEFT_TOP, P_LEFT_LEGS["step"]), 1),
            bob(build_frame(P_LEFT_TOP, P_LEFT_LEGS["step2"]), 1)]
    right = [mirror(f) for f in left]
    return [down, left, right, up]


def bento_sheet():
    down0 = from_ascii(B_DOWN, B_PAL)
    up0 = from_ascii(B_UP, B_PAL)
    left0 = from_ascii(B_LEFT, B_PAL)
    # segundo quadro: respiração (corpo desce 1 px, cabeça junto)
    def breathe(img):
        out = new(img.width, img.height)
        out.alpha_composite(img.crop((0, 0, img.width, img.height - 5)), (0, 1))
        out.alpha_composite(img.crop((0, img.height - 5, img.width, img.height)), (0, img.height - 5))
        return out
    rows = []
    for base in (down0, left0, mirror(left0), up0):
        rows.append([base, breathe(base)])
    return rows


def save_sheet(rows, path):
    cols = max(len(r) for r in rows)
    img = new(cols * FW, len(rows) * FH)
    for r, frames in enumerate(rows):
        for c, fr in enumerate(frames):
            img.alpha_composite(fr, (c * FW, r * FH))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def shadow():
    img = new(16, 6)
    for y in range(6):
        for x in range(16):
            dx = (x + 0.5 - 8) / 7.0
            dy = (y + 0.5 - 3) / 2.6
            if dx * dx + dy * dy <= 1:
                img.putpixel((x, y), (20, 16, 30, 80))
    return img


def main():
    out = ROOT / "assets" / "sprites"
    save_sheet(player_sheet(), out / "player.png")
    save_sheet(bento_sheet(), out / "bento.png")
    shadow().save(out / "shadow.png")
    print("personagens gerados em", out)


if __name__ == "__main__":
    main()
