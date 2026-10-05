#!/usr/bin/env python3
"""Gera os mapas do Prólogo (Vila Maré e interiores) a partir de um desenho em
grade. Rodar de novo sobrescreve data/maps/vila_mare.json e os interiores.
Fonte do conteúdo: docs/roteiro/01_prologo.md."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W, H = 40, 32

# terreno base
g = [["g"] * W for _ in range(H)]
def fill(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < W and 0 <= y < H:
                g[y][x] = c
# bordas de arbustos
fill(0, 0, W - 1, 1, "B"); fill(0, 0, 1, H - 1, "B"); fill(0, H - 2, W - 1, H - 1, "B")
# mar a leste com cais
fill(33, 2, W - 1, H - 3, "~"); fill(36, 2, W - 1, H - 3, "W")
fill(31, 9, 32, 26, ".")  # areia da orla
fill(33, 15, 38, 16, "=")  # cais
# caminhos: estrada norte-sul (x 19-20), praça, ruas para as casas e o cais
fill(19, 0, 20, H - 1, "p")
fill(14, 12, 25, 18, "p")   # praça
fill(9, 11, 30, 11, "p")    # rua das lojas
fill(6, 21, 33, 21, "p")    # rua das casas
fill(26, 15, 32, 16, "p")   # rua do cais
fill(9, 11, 9, 21, "p"); fill(30, 11, 30, 21, "p")
# canteiros de flores
for (x, y) in [(15, 13), (24, 13), (15, 17), (24, 17), (5, 26), (6, 27), (34, 4), (12, 28), (27, 28)]:
    g[y][x] = "f"
# estrada norte: 1 célula de largura na altura do Brás (o arbusto força passar por ele)
fill(20, 3, 20, 5, "B")
# saída sul (para a Praia)
fill(19, H - 2, 20, H - 1, "p")

ground = ["".join(r) for r in g]
props = [
    {"type": "house_ranch", "x": 12, "y": 10},
    {"type": "house_shop", "x": 27, "y": 10},
    {"type": "house_a", "x": 8, "y": 20},
    {"type": "house_b", "x": 30, "y": 20},
    {"type": "well", "x": 20, "y": 15, "dialog": "vila_mare/poco"},
    {"type": "stall", "x": 16, "y": 19},
    {"type": "lamp_post", "x": 13, "y": 13}, {"type": "lamp_post", "x": 26, "y": 13},
    {"type": "lamp_post", "x": 18, "y": 25}, {"type": "lamp_post", "x": 21, "y": 6},
    {"type": "flower_box", "x": 10, "y": 11}, {"type": "flower_box", "x": 25, "y": 11},
    {"type": "sign", "x": 18, "y": 28, "dialog": "vila_mare/placa_entrada"},
    {"type": "sign", "x": 14, "y": 11, "dialog": "vila_mare/placa_rancho"},
    {"type": "sign", "x": 29, "y": 11, "dialog": "vila_mare/placa_loja"},
    {"type": "sign", "x": 32, "y": 14, "dialog": "vila_mare/placa_cais"},
    {"type": "sign", "x": 18, "y": 2, "dialog": "vila_mare/placa_norte"},
    {"type": "boat", "x": 35, "y": 18}, {"type": "boat", "x": 36, "y": 13},
    {"type": "net_rack", "x": 32, "y": 23}, {"type": "barrel", "x": 31, "y": 17}, {"type": "crate", "x": 32, "y": 18},
    {"type": "palm", "x": 4, "y": 6}, {"type": "palm", "x": 30, "y": 5}, {"type": "palm", "x": 5, "y": 15},
    {"type": "palm", "x": 26, "y": 26}, {"type": "palm", "x": 13, "y": 27},
]
for x in range(3, 9):
    props.append({"type": "fence", "x": x, "y": 24})
for x in range(23, 29):
    props.append({"type": "fence", "x": x, "y": 6})
npcs = [
    {"id": "pipa", "x": 17, "y": 16, "facing": "right"},
    {"id": "cascalho", "x": 22, "y": 13, "facing": "down"},
    {"id": "jurema", "x": 31, "y": 13, "facing": "left"},
    {"id": "bras", "x": 19, "y": 4, "facing": "down", "if_not": "bras_beaten"},
    {"id": "bras_depois", "x": 22, "y": 3, "facing": "left", "if": "bras_beaten"},
    {"id": "rival_lia", "x": 20, "y": 2, "facing": "left", "if": "partner_taro", "if_not": "rival_vila_done"},
    {"id": "rival_taro", "x": 20, "y": 2, "facing": "left", "if": "partner_lia", "if_not": "rival_vila_done"},
]
warps = [
    {"x": 12, "y": 10, "to": "vila_rancho", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
    {"x": 27, "y": 10, "to": "vila_loja", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
    {"x": 8, "y": 20, "to": "vila_casa_remo", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
    {"x": 30, "y": 20, "to": "vila_casa_concha", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
    {"x": 19, "y": H - 1, "to": "praia_despertar", "tx": 23, "ty": 1, "facing": "down", "sfx": ""},
    {"x": 20, "y": H - 1, "to": "praia_despertar", "tx": 24, "ty": 1, "facing": "down", "sfx": ""},
    {"x": 19, "y": 0, "to": "rota_1", "tx": 19, "ty": 48, "facing": "up", "sfx": ""},
    {"x": 20, "y": 0, "to": "rota_1", "tx": 20, "ty": 48, "facing": "up", "sfx": ""},
]
vila = {"id": "vila_mare", "region": "vila_mare", "name_key": "MAP_VILA_MARE", "tileset": "overworld",
        "legend": {"g": "grass", "f": "flowers", "B": "bush", "p": "path", "~": "water", "W": "deep", "=": "dock", ".": "sand"},
        "ground": ground, "spawn": {"x": 19, "y": H - 3, "facing": "up"}, "props": props, "npcs": npcs, "warps": warps,
        "ambient": ["sea_sparkle", "leaves"]}


def room(mid, name_key, back_x, back_y, props, npcs, region="vila_mare"):
    rows = ["TTTTTTTTTTTT", "TwwnwwwwwnwT"] + ["T..........T"] * 7 + ["TTTTTTmTTTTT"]
    return {"id": mid, "region": region, "name_key": name_key, "tileset": "overworld",
            "legend": {"T": "wall_top", "w": "wall", "n": "wall_window", ".": "floor", "m": "mat"},
            "ground": rows, "spawn": {"x": 6, "y": 8, "facing": "up"}, "props": props, "npcs": npcs,
            "warps": [{"x": 6, "y": 9, "to": "vila_mare", "tx": back_x, "ty": back_y + 1, "facing": "down", "sfx": "door"}]}


maps = {
    "vila_mare": vila,
    "vila_rancho": room("vila_rancho", "MAP_VILA_RANCHO", 12, 10,
                        [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "plant", "x": 10, "y": 2},
                         {"type": "rug", "x": 6, "y": 6}, {"type": "lamp", "x": 1, "y": 7}, {"type": "shelf", "x": 9, "y": 7}],
                        [{"id": "marola", "x": 7, "y": 3, "facing": "down"}]),
    "vila_loja": room("vila_loja", "MAP_VILA_LOJA", 27, 10,
                      [{"type": "shelf", "x": 3, "y": 2}, {"type": "shelf", "x": 10, "y": 2}, {"type": "table", "x": 7, "y": 4},
                       {"type": "barrel", "x": 1, "y": 7}, {"type": "crate", "x": 10, "y": 7}, {"type": "rod_rack", "x": 5, "y": 2}],
                      [{"id": "anzol", "x": 6, "y": 3, "facing": "down"}]),
    "vila_casa_remo": room("vila_casa_remo", "MAP_VILA_CASA_REMO", 8, 20,
                           [{"type": "table", "x": 7, "y": 5}, {"type": "stool", "x": 5, "y": 5}, {"type": "bed", "x": 2, "y": 3},
                            {"type": "rod_rack", "x": 9, "y": 2}, {"type": "rug", "x": 6, "y": 7}],
                           [{"id": "seu_remo", "x": 6, "y": 3, "facing": "down"}]),
    "vila_casa_concha": room("vila_casa_concha", "MAP_VILA_CASA_CONCHA", 30, 20,
                             [{"type": "table", "x": 7, "y": 4}, {"type": "plant", "x": 1, "y": 2}, {"type": "plant", "x": 10, "y": 2},
                              {"type": "lamp", "x": 10, "y": 6}, {"type": "rug", "x": 6, "y": 6}],
                             [{"id": "vo_concha", "x": 5, "y": 3, "facing": "down"}]),
}
for mid, m in maps.items():
    for r in m["ground"]:
        assert len(r) == len(m["ground"][0]), mid
    (ROOT / "data/maps" / f"{mid}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("mapas:", ", ".join(maps))
