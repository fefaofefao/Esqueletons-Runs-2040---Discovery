#!/usr/bin/env python3
"""NPCs humanos (16×24 por quadro, 4 direções × 2 quadros de respiração).

Mesmo formato do Bento (assets/sprites/bento.png): linhas = baixo, esquerda,
direita, cima. Cada NPC é uma receita de partes (pele, cabelo, roupa, avental,
óculos, barba, chapéu, bengala). Arte original gerada por código.
"""
from pathlib import Path

from PIL import Image, ImageDraw

from draw import mirror, new

ROOT = Path(__file__).resolve().parents[2]
FW, FH = 16, 24
O = (36, 28, 44)


def dk(c, f=0.25):
    return tuple(int(v * (1 - f)) for v in c[:3])


def lt(c, f=0.2):
    return tuple(int(v + (255 - v) * f) for v in c[:3])


NPCS = {
    # id: receita
    "marola": dict(skin=(214, 160, 120), hair=(70, 50, 40), style="bun", shirt=(220, 90, 100), legs=(90, 70, 110), skirt=True, apron=(246, 240, 226)),
    "anzol": dict(skin=(232, 186, 150), hair=(150, 150, 160), style="short", shirt=(70, 120, 170), legs=(70, 60, 50), apron=(196, 150, 90), beard=(170, 170, 176), hat=("cap", (196, 72, 64))),
    "pipa": dict(skin=(244, 202, 166), hair=(210, 120, 60), style="pigtails", shirt=(250, 200, 70), legs=(80, 140, 200), skirt=True, small=True),
    "cascalho": dict(skin=(226, 180, 140), hair=(230, 230, 236), style="bald", shirt=(110, 90, 140), legs=(70, 60, 80), glasses=True, beard=(230, 230, 236), cane=True),
    "jurema": dict(skin=(170, 112, 80), hair=(40, 30, 30), style="long", shirt=(80, 160, 150), legs=(60, 80, 110), hat=("straw", (226, 196, 120))),
    "bras": dict(skin=(232, 186, 150), hair=(60, 40, 30), style="short", shirt=(110, 140, 70), legs=(60, 60, 70), hat=("cap", (110, 140, 70)), badge=True),
    "seu_remo": dict(skin=(200, 150, 110), hair=(90, 60, 40), style="short", shirt=(214, 120, 60), legs=(70, 70, 90), beard=(90, 60, 40)),
    "lenhador_velho": dict(skin=(214, 160, 120), hair=(200, 200, 206), style="bald", shirt=(170, 60, 50), legs=(70, 60, 50), beard=(200, 200, 206), hat=("cap", (90, 70, 50))),
    "rufo": dict(skin=(232, 186, 150), hair=(150, 80, 40), style="short", shirt=(200, 140, 60), legs=(60, 70, 90)),
    "iris": dict(skin=(200, 150, 110), hair=(60, 40, 70), style="long", shirt=(140, 90, 170), legs=(60, 60, 80)),
    "cipo": dict(skin=(244, 202, 166), hair=(40, 90, 40), style="short", shirt=(70, 120, 70), legs=(70, 60, 50), hat=("cap", (60, 110, 60)), badge=True),
    "tilia": dict(skin=(226, 176, 136), hair=(170, 100, 60), style="bun", shirt=(240, 160, 170), legs=(110, 90, 120), skirt=True, apron=(246, 240, 226)),
    "toco": dict(skin=(200, 150, 110), hair=(110, 80, 50), style="short", shirt=(120, 90, 60), legs=(60, 50, 40), apron=(170, 130, 80), beard=(110, 80, 50)),
    "salvia": dict(skin=(232, 190, 160), hair=(220, 220, 200), style="long", shirt=(90, 150, 120), legs=(70, 100, 90), skirt=True, glasses=True),
    "graveto": dict(skin=(244, 202, 166), hair=(60, 40, 30), style="short", shirt=(90, 150, 210), legs=(70, 60, 50), small=True),
    "hera": dict(skin=(214, 160, 120), hair=(90, 60, 40), style="bun", shirt=(110, 140, 90), legs=(80, 70, 60), skirt=True),
    "guarda_raiz": dict(skin=(232, 186, 150), hair=(60, 40, 30), style="short", shirt=(110, 140, 70), legs=(60, 60, 70), hat=("cap", (110, 140, 70)), badge=True),
    "irmao_galho": dict(skin=(214, 160, 120), hair=(140, 90, 50), style="short", shirt=(150, 110, 70), legs=(70, 60, 50), hat=("cap", (150, 110, 70))),
    "pai_musgo": dict(skin=(200, 150, 110), hair=(60, 90, 50), style="short", shirt=(90, 120, 80), legs=(60, 70, 60), beard=(60, 90, 50)),
    "vigia_lasca": dict(skin=(214, 160, 120), hair=(60, 40, 30), style="short", shirt=(110, 140, 70), legs=(60, 60, 70), hat=("cap", (110, 140, 70)), badge=True),
    "seixo": dict(skin=(200, 150, 110), hair=(150, 150, 150), style="short", shirt=(150, 120, 80), legs=(80, 70, 60), beard=(150, 150, 150), hat=("straw", (190, 160, 100))),
    "brita": dict(skin=(232, 186, 150), hair=(70, 50, 40), style="short", shirt=(90, 100, 120), legs=(60, 60, 70), hat=("cap", (230, 190, 60))),
    "rubi": dict(skin=(214, 160, 120), hair=(160, 40, 50), style="long", shirt=(140, 70, 60), legs=(70, 60, 60), apron=(120, 90, 60)),
    "graxa": dict(skin=(200, 150, 110), hair=(40, 30, 30), style="short", shirt=(70, 70, 80), legs=(50, 50, 60), hat=("cap", (180, 70, 50)), badge=True),
    "pirita": dict(skin=(226, 176, 136), hair=(200, 160, 60), style="bun", shirt=(220, 120, 110), legs=(110, 90, 100), skirt=True, apron=(246, 240, 226)),
    "cobre": dict(skin=(214, 160, 120), hair=(170, 90, 50), style="short", shirt=(180, 110, 60), legs=(70, 60, 50), apron=(140, 100, 70), beard=(170, 90, 50)),
    "carvao": dict(skin=(170, 112, 80), hair=(40, 40, 40), style="bald", shirt=(70, 70, 70), legs=(50, 50, 50), beard=(60, 60, 60), glasses=True),
    "fagulha": dict(skin=(244, 202, 166), hair=(230, 120, 40), style="pigtails", shirt=(230, 180, 60), legs=(90, 80, 110), small=True),
    "turmalina": dict(skin=(214, 160, 120), hair=(220, 210, 220), style="bun", shirt=(120, 80, 140), legs=(80, 70, 90), skirt=True, cane=True),
    "agata": dict(skin=(200, 150, 110), hair=(50, 40, 40), style="long", shirt=(100, 120, 140), legs=(60, 60, 70), hat=("cap", (230, 190, 60))),
    "bigorna": dict(skin=(232, 186, 150), hair=(90, 60, 40), style="short", shirt=(130, 130, 140), legs=(60, 60, 70), apron=(90, 70, 50)),
    "fuligem": dict(skin=(190, 140, 100), hair=(50, 50, 50), style="short", shirt=(100, 110, 80), legs=(60, 60, 50), glasses=True),
    "cascudo": dict(skin=(200, 150, 110), hair=(40, 30, 30), style="short", shirt=(90, 130, 170), legs=(70, 60, 50), small=True, hat=("cap", (200, 90, 60))),
    "bloqueio": dict(skin=(214, 160, 120), hair=(60, 40, 30), style="short", shirt=(90, 90, 100), legs=(60, 60, 70), hat=("cap", (230, 190, 60)), badge=True),
    # pântano (4d)
    "garca": dict(skin=(214, 160, 120), hair=(236, 236, 240), style="bun", shirt=(220, 230, 236), legs=(110, 130, 150), skirt=True, apron=(150, 200, 170)),
    "junco": dict(skin=(190, 140, 100), hair=(70, 60, 40), style="short", shirt=(120, 140, 80), legs=(80, 70, 50), hat=("straw", (200, 180, 110)), beard=(70, 60, 40)),
    "taboa": dict(skin=(232, 186, 150), hair=(130, 80, 50), style="pigtails", shirt=(150, 110, 70), legs=(90, 110, 70), skirt=True),
    "bagre": dict(skin=(170, 112, 80), hair=(40, 40, 40), style="bald", shirt=(70, 110, 130), legs=(60, 70, 60), beard=(80, 80, 80), hat=("cap", (90, 120, 90))),
    "neblina": dict(skin=(226, 190, 170), hair=(220, 226, 230), style="long", shirt=(170, 190, 200), legs=(120, 130, 150), skirt=True, cane=True),
    "girino": dict(skin=(200, 150, 110), hair=(50, 40, 30), style="short", shirt=(120, 190, 110), legs=(70, 90, 120), small=True),
    "sape": dict(skin=(190, 140, 100), hair=(200, 200, 190), style="bald", shirt=(140, 120, 90), legs=(90, 80, 60), beard=(200, 200, 190), cane=True),
    "lodo": dict(skin=(214, 160, 120), hair=(90, 70, 50), style="short", shirt=(100, 90, 70), legs=(70, 60, 50), glasses=True, apron=(150, 130, 90)),
    "pena": dict(skin=(232, 186, 150), hair=(60, 40, 40), style="bun", shirt=(70, 90, 160), legs=(60, 70, 110), hat=("cap", (70, 90, 160)), badge=True),
    "traira": dict(skin=(200, 150, 110), hair=(30, 30, 40), style="long", shirt=(90, 130, 110), legs=(60, 70, 60), hat=("straw", (190, 170, 110))),
    "canico": dict(skin=(232, 186, 150), hair=(170, 120, 60), style="short", shirt=(160, 160, 90), legs=(80, 80, 60)),
    "marreco": dict(skin=(214, 160, 120), hair=(60, 40, 30), style="short", shirt=(70, 120, 90), legs=(70, 60, 50), hat=("cap", (60, 110, 70)), beard=(60, 40, 30)),
    "remanso": dict(skin=(170, 112, 80), hair=(220, 220, 220), style="short", shirt=(120, 100, 80), legs=(70, 60, 50), hat=("straw", (210, 190, 120)), beard=(220, 220, 220)),
    "fel": dict(skin=(200, 170, 140), hair=(100, 140, 80), style="short", shirt=(80, 110, 70), legs=(50, 60, 50), glasses=True, badge=True),
    # Ossório (4e)
    "trote": dict(skin=(232, 186, 150), hair=(150, 100, 50), style="short", shirt=(60, 80, 150), legs=(220, 210, 190), hat=("cap", (60, 80, 150)), badge=True),
    "elmo": dict(skin=(214, 160, 120), hair=(60, 40, 30), style="short", shirt=(150, 156, 170), legs=(60, 70, 110), hat=("helm", (170, 176, 190))),
    "malva": dict(skin=(200, 150, 110), hair=(140, 60, 120), style="long", shirt=(150, 156, 170), legs=(60, 70, 110), hat=("helm", (170, 176, 190))),
    "bigode": dict(skin=(232, 186, 150), hair=(90, 60, 30), style="short", shirt=(70, 90, 150), legs=(60, 60, 80), beard=(90, 60, 30), hat=("helm", (150, 156, 170))),
    "ameia": dict(skin=(226, 176, 136), hair=(200, 200, 200), style="bun", shirt=(240, 236, 226), legs=(60, 80, 150), skirt=True, apron=(200, 70, 70)),
    "dobrao": dict(skin=(190, 140, 100), hair=(40, 30, 30), style="short", shirt=(120, 60, 120), legs=(60, 50, 60), apron=(220, 190, 90), beard=(40, 30, 30)),
    "viseira": dict(skin=(214, 160, 120), hair=(220, 180, 90), style="bun", shirt=(60, 80, 150), legs=(60, 60, 80), badge=True, hat=("helm", (220, 190, 90))),
    "elo": dict(skin=(232, 186, 150), hair=(30, 30, 40), style="short", shirt=(170, 60, 60), legs=(60, 60, 80), small=True),
    "clarim": dict(skin=(200, 150, 110), hair=(110, 70, 40), style="short", shirt=(200, 60, 60), legs=(220, 200, 160), hat=("cap", (60, 80, 150)), beard=(110, 70, 40)),
    "fivela": dict(skin=(244, 202, 166), hair=(240, 200, 90), style="pigtails", shirt=(90, 150, 210), legs=(70, 70, 120), small=True, skirt=True),
    "selo": dict(skin=(232, 190, 160), hair=(230, 230, 230), style="bald", shirt=(90, 70, 110), legs=(60, 50, 70), glasses=True, beard=(230, 230, 230)),
    "brasao": dict(skin=(190, 140, 100), hair=(200, 200, 200), style="short", shirt=(60, 80, 150), legs=(80, 70, 60), cane=True, beard=(200, 200, 200)),
    "grade": dict(skin=(170, 112, 80), hair=(40, 40, 40), style="bald", shirt=(150, 156, 170), legs=(60, 70, 110), hat=("helm", (130, 136, 150)), beard=(40, 40, 40)),
    # picos (4f)
    "treno": dict(skin=(214, 160, 120), hair=(90, 60, 40), style="short", shirt=(200, 80, 60), legs=(70, 70, 90), hat=("hood", (200, 80, 60)), beard=(90, 60, 40)),
    "grampo": dict(skin=(232, 186, 150), hair=(60, 40, 30), style="short", shirt=(230, 170, 50), legs=(60, 70, 110), hat=("hood", (230, 170, 50))),
    "rajada": dict(skin=(200, 150, 110), hair=(220, 220, 240), style="long", shirt=(90, 160, 220), legs=(60, 60, 90), hat=("hood", (90, 160, 220))),
    "brisa": dict(skin=(232, 190, 160), hair=(40, 40, 40), style="bald", shirt=(200, 120, 60), legs=(200, 120, 60), skirt=True),
    "lareira": dict(skin=(214, 160, 120), hair=(170, 80, 50), style="bun", shirt=(200, 60, 60), legs=(110, 80, 70), skirt=True, apron=(240, 236, 226)),
    "cachecol": dict(skin=(190, 140, 100), hair=(40, 30, 30), style="short", shirt=(70, 120, 90), legs=(70, 60, 50), hat=("hood", (200, 60, 60))),
    "lamina": dict(skin=(244, 202, 166), hair=(240, 220, 140), style="pigtails", shirt=(150, 200, 240), legs=(70, 90, 150), skirt=True),
    "granizo": dict(skin=(214, 160, 120), hair=(230, 230, 240), style="short", shirt=(110, 130, 170), legs=(60, 60, 80), small=True, hat=("hood", (110, 130, 170))),
    "floquinho": dict(skin=(244, 202, 166), hair=(90, 60, 40), style="short", shirt=(240, 240, 250), legs=(90, 120, 200), small=True, hat=("hood", (240, 240, 250))),
    "camelia": dict(skin=(200, 150, 110), hair=(60, 40, 40), style="long", shirt=(110, 170, 110), legs=(80, 70, 60), apron=(230, 210, 170), hat=("straw", (200, 180, 110))),
    "pinhao": dict(skin=(214, 160, 120), hair=(220, 220, 220), style="short", shirt=(120, 90, 70), legs=(70, 60, 50), beard=(220, 220, 220), cane=True, hat=("hood", (120, 90, 70))),
    "degelo": dict(skin=(232, 186, 150), hair=(110, 80, 50), style="short", shirt=(90, 140, 200), legs=(60, 60, 80), glasses=True),
    "pingente": dict(skin=(170, 112, 80), hair=(40, 40, 40), style="short", shirt=(170, 210, 236), legs=(80, 100, 140), hat=("helm", (200, 230, 245)), badge=True),
    # deserto (4g)
    "cantil": dict(skin=(170, 112, 80), hair=(220, 220, 220), style="short", shirt=(220, 200, 160), legs=(150, 120, 90), hat=("wrap", (240, 236, 220)), beard=(220, 220, 220), cane=True),
    "corcova": dict(skin=(190, 140, 100), hair=(40, 30, 30), style="short", shirt=(200, 140, 80), legs=(120, 90, 60), hat=("wrap", (200, 70, 60)), beard=(40, 30, 30)),
    "veu": dict(skin=(214, 160, 120), hair=(40, 30, 40), style="long", shirt=(170, 70, 140), legs=(220, 180, 90), skirt=True, hat=("wrap", (240, 200, 90))),
    "pa": dict(skin=(232, 186, 150), hair=(150, 100, 60), style="short", shirt=(190, 170, 120), legs=(110, 90, 70), glasses=True, hat=("straw", (210, 190, 130))),
    "moringa": dict(skin=(170, 112, 80), hair=(60, 40, 40), style="bun", shirt=(80, 140, 170), legs=(200, 170, 120), skirt=True, apron=(240, 230, 200)),
    "canela": dict(skin=(200, 150, 110), hair=(110, 60, 40), style="long", shirt=(190, 100, 60), legs=(120, 80, 60), apron=(230, 200, 140), hat=("wrap", (230, 170, 60))),
    "tamara": dict(skin=(190, 140, 100), hair=(30, 30, 30), style="pigtails", shirt=(220, 170, 70), legs=(140, 90, 60), hat=("wrap", (150, 60, 50))),
    "batuque": dict(skin=(170, 112, 80), hair=(30, 30, 30), style="short", shirt=(200, 60, 60), legs=(240, 200, 90), small=True),
    "rosa": dict(skin=(232, 186, 150), hair=(200, 120, 60), style="bun", shirt=(80, 120, 160), legs=(160, 130, 90), glasses=True, hat=("wrap", (240, 236, 220))),
    "alforje": dict(skin=(190, 140, 100), hair=(90, 70, 50), style="short", shirt=(160, 120, 80), legs=(110, 80, 60), beard=(90, 70, 50), hat=("wrap", (200, 180, 140))),
    "grao": dict(skin=(200, 150, 110), hair=(50, 30, 20), style="short", shirt=(240, 210, 120), legs=(140, 100, 70), small=True, hat=("wrap", (240, 240, 230))),
    "miragem": dict(skin=(214, 160, 120), hair=(240, 240, 240), style="long", shirt=(150, 120, 190), legs=(110, 90, 140), skirt=True, cane=True),
    "sandalo": dict(skin=(170, 112, 80), hair=(40, 30, 30), style="bald", shirt=(110, 70, 140), legs=(230, 200, 120), badge=True, beard=(40, 30, 30)),
    "vo_concha": dict(skin=(232, 190, 160), hair=(236, 236, 240), style="bun", shirt=(150, 110, 180), legs=(120, 90, 140), skirt=True, glasses=True, cane=True),
}


def draw_npc(r, view, breath=0):
    img = new(FW, FH)
    d = ImageDraw.Draw(img)
    skin, hair, shirt, legs = r["skin"], r["hair"], r["shirt"], r["legs"]
    small = r.get("small", False)
    top = 4 if small else 1
    hy = top + 5 + breath  # centro da cabeça
    # pernas / saia
    ly = 17 if not small else 18
    if r.get("skirt"):
        d.polygon([(4, ly - 1 + breath), (11, ly - 1 + breath), (12, 21), (3, 21)], fill=legs)
        d.rectangle([5, 21, 6, 22], fill=skin)
        d.rectangle([9, 21, 10, 22], fill=skin)
    else:
        d.rectangle([4, ly + breath, 7, 22], fill=legs)
        d.rectangle([8, ly + breath, 11, 22], fill=dk(legs, 0.1))
    d.rectangle([4, 22, 7, 23], fill=(60, 44, 40))
    d.rectangle([8, 22, 11, 23], fill=(60, 44, 40))
    # tronco
    ty = top + 10 + breath
    d.rectangle([3, ty, 12, ly + breath], fill=shirt)
    d.rectangle([3, ty, 12, ty], fill=lt(shirt))
    if view in ("down", "up"):
        d.rectangle([2, ty + 1, 2, ty + 5], fill=skin if view == "down" else shirt)
        d.rectangle([13, ty + 1, 13, ty + 5], fill=skin if view == "down" else shirt)
    else:
        d.rectangle([7, ty + 1, 8, ty + 6], fill=dk(shirt, 0.15))
        d.rectangle([7, ty + 6, 8, ty + 7], fill=skin)
    if r.get("apron") and view != "up":
        x0, x1 = (5, 10) if view == "down" else ((4, 8) if view == "left" else (7, 11))
        d.rectangle([x0, ty + 2, x1, ly + 1 + breath], fill=r["apron"])
    if r.get("badge") and view == "down":
        d.point((10, ty + 2), fill=(250, 220, 90))
    # cabeça
    d.ellipse([3, hy - 5, 12, hy + 4], fill=skin)
    # cabelo
    st = r["style"]
    if view == "up":
        if st != "bald":
            d.ellipse([3, hy - 5, 12, hy + 4], fill=hair)
        else:
            d.ellipse([3, hy - 5, 12, hy + 4], fill=skin)
            d.rectangle([3, hy, 12, hy + 2], fill=hair)
    else:
        if st in ("short", "bun", "pigtails", "long"):
            d.chord([3, hy - 5, 12, hy + 3], 180, 360, fill=hair)
            d.rectangle([3, hy - 2, 4 if view != "left" else 3, hy + 1], fill=hair)
            d.rectangle([11 if view != "right" else 12, hy - 2, 12, hy + 1], fill=hair)
        if st == "bald":
            d.rectangle([3, hy - 1, 3, hy + 1], fill=hair)
            d.rectangle([12, hy - 1, 12, hy + 1], fill=hair)
        if st == "long":
            d.rectangle([3, hy - 2, 4, hy + 6], fill=hair)
            d.rectangle([11, hy - 2, 12, hy + 6], fill=hair)
    if st == "bun":
        d.ellipse([6, hy - 8, 9, hy - 5], fill=hair)
    if st == "pigtails":
        d.ellipse([0, hy - 2, 3, hy + 2], fill=hair)
        d.ellipse([12, hy - 2, 15, hy + 2], fill=hair)
    # rosto
    if view == "down":
        d.point((5, hy), fill=O)
        d.point((10, hy), fill=O)
        d.point((7, hy + 2), fill=dk(skin, 0.3))
        d.point((8, hy + 2), fill=dk(skin, 0.3))
        if r.get("glasses"):
            d.rectangle([4, hy - 1, 6, hy + 1], outline=(60, 60, 80))
            d.rectangle([9, hy - 1, 11, hy + 1], outline=(60, 60, 80))
        if r.get("beard"):
            d.chord([4, hy, 11, hy + 5], 0, 180, fill=r["beard"])
    elif view in ("left", "right"):
        ex = 4 if view == "left" else 11
        d.point((ex, hy), fill=O)
        if r.get("glasses"):
            d.rectangle([ex - 1, hy - 1, ex + 1, hy + 1], outline=(60, 60, 80))
        if r.get("beard"):
            bx = (3, 8) if view == "left" else (7, 12)
            d.chord([bx[0], hy, bx[1], hy + 5], 0, 180, fill=r["beard"])
    # chapéu
    if r.get("hat"):
        kind, c = r["hat"]
        if kind == "cap":
            d.chord([3, hy - 6, 12, hy + 1], 180, 360, fill=c)
            if view == "down":
                d.rectangle([4, hy - 2, 11, hy - 1], fill=dk(c))
            elif view == "left":
                d.rectangle([1, hy - 2, 6, hy - 1], fill=dk(c))
            elif view == "right":
                d.rectangle([9, hy - 2, 14, hy - 1], fill=dk(c))
        elif kind == "hood":
            d.chord([2, hy - 6, 13, hy + 4], 180, 360, fill=c)
            d.rectangle([2, hy - 1, 3, hy + 5], fill=c)
            d.rectangle([12, hy - 1, 13, hy + 5], fill=c)
            d.rectangle([3, hy - 2, 12, hy - 2], fill=(240, 240, 240))
        elif kind == "wrap":
            d.chord([3, hy - 7, 12, hy], 180, 360, fill=c)
            d.rectangle([3, hy - 3, 12, hy - 2], fill=dk(c))
            if view in ("left", "right"):
                tx = 12 if view == "left" else 2
                d.rectangle([tx, hy - 2, tx + 1, hy + 4], fill=c)
        elif kind == "helm":
            d.chord([3, hy - 6, 12, hy + 1], 180, 360, fill=c)
            d.rectangle([7, hy - 8, 8, hy - 6], fill=(200, 60, 60))
            if view == "down":
                d.rectangle([7, hy - 2, 8, hy + 1], fill=dk(c))
        elif kind == "straw":
            d.ellipse([0, hy - 4, 15, hy - 1], fill=c)
            d.chord([4, hy - 8, 11, hy - 1], 180, 360, fill=lt(c, 0.1))
            d.rectangle([4, hy - 3, 11, hy - 3], fill=(200, 80, 70))
    # bengala
    if r.get("cane") and view != "up":
        cx = 14 if view in ("down", "right") else 1
        d.line([(cx, ty + 4), (cx, 23)], fill=(130, 90, 56))
        d.point((cx - 1 if cx == 14 else cx + 1, ty + 4), fill=(130, 90, 56))
    # contorno
    src = img.copy()
    for y in range(FH):
        for x in range(FW):
            if src.getpixel((x, y))[3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < FW and 0 <= ny < FH and src.getpixel((nx, ny))[3] > 128:
                    img.putpixel((x, y), O + (255,))
                    break
    return img


def sheet(r):
    rows = []
    for view in ("down", "left", "right", "up"):
        v = "left" if view == "right" else view
        frames = [draw_npc(r, v, 0), draw_npc(r, v, 1)]
        if view == "right":
            frames = [mirror(f) for f in frames]
        rows.append(frames)
    img = new(2 * FW, 4 * FH)
    for ri, frames in enumerate(rows):
        for ci, fr in enumerate(frames):
            img.alpha_composite(fr, (ci * FW, ri * FH))
    return img


def skeleton_sheet(species):
    """Esqueleto como NPC (Lia, Taro): usa o sprite de mapa da espécie (2 quadros)."""
    src = Image.open(ROOT / "assets" / "skeletons" / "map" / f"{species}.png").convert("RGBA")
    img = new(2 * FW, 4 * FH)
    for row in range(4):
        for col in range(2):
            fr = src.crop((col * 16, 0, col * 16 + 16, 16))
            if row == 2:
                fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(fr, (col * FW, row * FH + 8))
    return img


def main():
    out = ROOT / "assets" / "sprites" / "npc"
    out.mkdir(parents=True, exist_ok=True)
    skeleton_sheet("faroleira_1").save(out / "skel_lia.png")
    skeleton_sheet("grumete_1").save(out / "skel_taro.png")
    skeleton_sheet("lenhador_3").save(out / "skel_ramalho.png")
    skeleton_sheet("ferreiro_3").save(out / "skel_fornalha.png")
    skeleton_sheet("lavadeira_3").save(out / "skel_musga.png")
    skeleton_sheet("sentinela_3").save(out / "skel_calico.png")
    skeleton_sheet("escultor_3").save(out / "skel_alva.png")
    skeleton_sheet("tamborileiro_3").save(out / "skel_duna.png")
    skeleton_sheet("rei_esqueleto").save(out / "skel_rei.png")
    skeleton_sheet("degustor").save(out / "skel_degustor.png")
    skeleton_sheet("mineiro_2").save(out / "skel_mineiro.png")
    for sp in ("faroleira_2", "faroleira_3", "grumete_2", "grumete_3"):
        skeleton_sheet(sp).save(out / f"skel_{sp}.png")
    for sp in ("vagonauta", "brumaga", "bufardo", "nevasco", "ampulhor"):
        skeleton_sheet(sp).save(out / f"skel_{sp}.png")
    preview = new(len(NPCS) * 2 * FW, 4 * FH)
    for i, (nid, r) in enumerate(NPCS.items()):
        s = sheet(r)
        s.save(out / f"{nid}.png")
        preview.alpha_composite(s, (i * 2 * FW, 0))
    preview.resize((preview.width * 4, preview.height * 4), Image.NEAREST).save("/tmp/npcs_preview.png")
    print("npcs:", len(NPCS), "->", out)


if __name__ == "__main__":
    main()
