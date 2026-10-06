#!/usr/bin/env python3
"""Refinamento dos mapas externos (pedido do Fernando: "o mapa tem que ser refinado").

Roda depois de todos os geradores (tools/maps/build_all.py chama no fim) e, para
cada mapa externo:
  1. quebra as bordas retas da mata/rocha com reentrâncias irregulares;
  2. espalha manchas de flores e detalhes da região (pedras, tocos, cogumelos,
     conchas, juncos, cactos...) nas áreas vazias.

Segurança: nada é colocado em trilhas (nem ao lado delas), perto de portas, NPCs,
objetos interativos, zonas de selvagens ou do ponto de chegada. Cada mudança que
bloqueia passagem só é aceita se todos os destinos que eram alcançáveis continuam
alcançáveis e nenhum bolsão de chão fica isolado. Determinístico (semente = id do
mapa) e marcado com "refined": true para não rodar duas vezes.

Uso: python3 tools/maps/refine.py [mapa ...]
"""
import json
import random
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TILES = json.loads((ROOT / "data/tilesets/overworld.json").read_text(encoding="utf-8"))["terrains"]
PROPS = json.loads((ROOT / "data/props.json").read_text(encoding="utf-8"))
PROPS = PROPS.get("props", PROPS)

WALLS = {"bush", "rock", "snow_rock", "sandstone"}          # bordas que ganham reentrâncias
OPEN = {"grass", "flowers", "sand", "ash", "mud", "snow", "dune"}  # chão natural que recebe detalhes
PATHS = {"path", "dock", "stone", "ice", "castle_floor", "carpet", "floor", "mat"}

# detalhes por região: (tipo de objeto, terrenos onde pode ir, peso)
DECOR = {
    "praia": [("starfish", {"sand"}, 3), ("driftwood", {"sand"}, 2), ("rock_small", {"sand", "grass"}, 2), ("plant", {"grass"}, 1)],
    "vila_mare": [("rock_small", {"grass"}, 2), ("plant", {"grass"}, 2), ("starfish", {"sand"}, 1), ("stump", {"grass"}, 1)],
    "bosque": [("mushrooms", {"grass", "flowers"}, 3), ("stump", {"grass"}, 2), ("rock_small", {"grass"}, 2), ("log", {"grass"}, 1),
               ("tree_pine", {"grass"}, 1), ("tree_oak2", {"grass"}, 1)],
    "minas": [("rock_small", {"ash"}, 4), ("rubble", {"ash"}, 2), ("dead_tree", {"ash"}, 1)],
    "pantano": [("reeds", {"mud", "grass"}, 3), ("mushrooms", {"mud", "grass"}, 2), ("glow_shroom", {"mud", "grass"}, 1), ("dead_tree", {"mud"}, 1)],
    "ossorio": [("rock_small", {"grass"}, 2), ("plant", {"grass"}, 2), ("broken_column", {"grass"}, 1), ("stump", {"grass"}, 1)],
    "picos": [("rock_small", {"snow"}, 3), ("snow_pine", {"snow"}, 2)],
    "deserto": [("cactus", {"dune", "sand"}, 3), ("rock_small", {"dune", "sand"}, 2), ("dead_tree", {"dune"}, 1)],
    "castelo": [("rubble", {"grass", "ash", "stone"}, 2), ("broken_column", {"grass", "ash"}, 1)],
}
FLOWER_REGIONS = {"praia", "vila_mare", "bosque", "ossorio"}
# copas sobre a mata (e pedras sobre a rocha): dão volume sem mudar a passagem
CANOPY = {
    "bush": {"bosque": ["tree_oak", "tree_oak2", "tree_pine", "tree_pine"], "vila_mare": ["tree_oak", "tree_oak2", "palm"],
             "praia": ["palm", "tree_oak2"], "ossorio": ["tree_oak", "tree_oak2", "tree_pine"], "pantano": ["willow", "dead_tree"],
             "castelo": ["dead_tree", "tree_pine"], "minas": ["dead_tree"], "picos": ["snow_pine"], "deserto": ["palm"]},
    "rock": {"minas": ["rock_big", "rock_small", "dead_tree"]},
    "snow_rock": {"picos": ["snow_pine", "snow_pine", "rock_big"]},
    "sandstone": {"deserto": ["rock_big", "cactus"]},
}


def solid_terrain(t):
    return bool(TILES.get(t, {}).get("solid", True))


class MapGrid:
    def __init__(self, m):
        self.m = m
        legend = m["legend"]
        self.rows = [list(r) for r in m["ground"]]
        self.h = len(self.rows)
        self.w = max(len(r) for r in self.rows)
        self.legend = legend
        self.char_of = {}
        for ch, t in legend.items():
            self.char_of.setdefault(t, ch)
        self.prop_cells = {}   # célula -> objeto (colisão)
        self.near_props = set()
        self.soft = []         # decoração simples que pode dar lugar a lagos, ruínas e riachos
        for p in m.get("props", []):
            info = PROPS.get(p["type"], {})
            cond = any(k in p for k in ("if", "if_not", "if_all", "if_any", "if_none"))
            if p["type"] in REMOVABLE and not cond and not p.get("dialog"):
                self.soft.append(p)
                for dx, dy in info.get("collision", []):
                    self.prop_cells[(p["x"] + dx, p["y"] + dy)] = p
                continue
            for dx, dy in info.get("collision", []):
                c = (p["x"] + dx, p["y"] + dy)
                if not cond:
                    self.prop_cells[c] = p
                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        self.near_props.add((c[0] + ox, c[1] + oy))
            self.near_props.add((p["x"], p["y"]))

    def terrain(self, x, y):
        if 0 <= y < self.h and 0 <= x < len(self.rows[y]):
            return self.legend.get(self.rows[y][x], "void")
        return "void"

    def set_terrain(self, x, y, t):
        if t not in self.char_of:
            used = set(self.legend) | {c for r in self.rows for c in r}
            ch = next(c for c in "fFkKqQzZjJ0123456789" if c not in used)
            self.legend[ch] = t
            self.char_of[t] = ch
        self.rows[y][x] = self.char_of[t]

    def walkable(self, c):
        x, y = c
        return not solid_terrain(self.terrain(x, y)) and c not in self.prop_cells

    def reach(self, start):
        if not self.walkable(start):
            return set()
        seen = {start}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n not in seen and 0 <= n[0] < self.w and 0 <= n[1] < self.h and self.walkable(n):
                    seen.add(n)
                    q.append(n)
        return seen


TRAILS = {"path", "stone"}
# decoração simples que um ponto de interesse ou riacho pode substituir
REMOVABLE = {"tree_oak", "tree_oak2", "tree_pine", "snow_pine", "palm", "stump", "log", "mushrooms", "rock_small", "rock_big",
             "plant", "dead_tree", "cactus", "starfish", "driftwood", "reeds", "glow_shroom"}
MEANDER_MAPS = ("rota_", "praia_despertar", "bosque_velho")


def _base_open(g, cells):
    """Chão natural mais comum em volta (o que fica no lugar da trilha que saiu)."""
    from collections import Counter
    cnt = Counter()
    for (x, y) in cells:
        for dx in (-3, -2, 2, 3):
            for t in (g.terrain(x + dx, y), g.terrain(x, y + dx)):
                if t in OPEN:
                    cnt[t] += 1
    return cnt.most_common(1)[0][0] if cnt else None


def meander(m, g, rng):
    """Trilhas retas viram curvas suaves. Trilha e chão são ambos passáveis, então a
    passagem não muda; as pontas (portas, cruzamentos, portões) ficam no lugar."""
    if not m["id"].startswith(MEANDER_MAPS):
        return 0
    fixed = set()
    for p in m.get("props", []):
        hard = p["type"] not in REMOVABLE or any(k.startswith("if") for k in p) or p.get("dialog")
        for dx, dy in PROPS.get(p["type"], {}).get("collision", []) or [(0, 0)]:
            for ox in ((-1, 0, 1) if hard else (0,)):
                for oy in ((-1, 0, 1) if hard else (0,)):
                    fixed.add((p["x"] + dx + ox, p["y"] + dy + oy))
    for n in m.get("npcs", []) + m.get("warps", []):
        for ox in range(-2, 3):
            for oy in range(-2, 3):
                fixed.add((n["x"] + ox, n["y"] + oy))
    changed = 0
    for horizontal in (False, True):
        # vista "transposta" para tratar trilhas horizontais com o mesmo código
        W, H = (g.h, g.w) if horizontal else (g.w, g.h)
        at = (lambda a, b: g.terrain(b, a)) if horizontal else (lambda a, b: g.terrain(a, b))
        cell = (lambda a, b: (b, a)) if horizontal else (lambda a, b: (a, b))
        runs = []  # (início, fim, a0, a1, terreno)
        prev = None
        for b in range(H):
            segs = []
            a = 0
            while a < W:
                t = at(a, b)
                if t in TRAILS:
                    a0 = a
                    while a < W and at(a, b) == t:
                        a += 1
                    segs.append((a0, a - 1, t))
                else:
                    a += 1
            narrow = [s for s in segs if s[1] - s[0] <= 2]
            for s in narrow:
                if prev and any(r[1] == b - 1 and r[2] == s[0] and r[3] == s[1] and r[4] == s[2] for r in prev):
                    r = next(r for r in prev if r[1] == b - 1 and r[2] == s[0] and r[3] == s[1] and r[4] == s[2])
                    r[1] = b
                else:
                    runs.append([b, b, s[0], s[1], s[2]])
            prev = [r for r in runs if r[1] == b]
        import math
        subruns = []
        for b0, b1, a0, a1, terr in runs:
            amp_need = 2
            cur = None
            for b in range(b0, b1 + 1):
                room = all((at(a, b) in OPEN or at(a, b) == terr) and cell(a, b) not in fixed and cell(a, b) not in g.prop_cells
                           for a in range(a0 - amp_need, a1 + amp_need + 1))
                if room:
                    if cur and cur[1] == b - 1:
                        cur[1] = b
                    else:
                        cur = [b, b, a0, a1, terr]
                        subruns.append(cur)
        for b0, b1, a0, a1, terr in subruns:
            L = b1 - b0 + 1
            if L < 10:
                continue
            amp = 2 if L >= 18 else 1
            cycles = max(1, round(L / 16))
            phase = rng.choice([0.0, math.pi])
            offs = []
            for b in range(b0, b1 + 1):
                taper = min(1.0, (b - b0) / 3.0, (b1 - b) / 3.0)
                offs.append(round(amp * taper * math.sin(phase + 2 * math.pi * cycles * (b - b0) / (L - 1))))
            new = set()
            for i, b in enumerate(range(b0, b1 + 1)):
                lo, hi = a0 + offs[i], a1 + offs[i]
                if i > 0:  # continuidade nas viradas
                    lo, hi = min(lo, a0 + offs[i - 1]), max(hi, a1 + offs[i - 1])
                for a in range(lo, hi + 1):
                    new.add(cell(a, b))
            old = {cell(a, b) for b in range(b0, b1 + 1) for a in range(a0, a1 + 1)}
            touched = new ^ old
            if any(c in fixed or c in g.prop_cells or (g.terrain(*c) not in OPEN and c not in old) for c in touched):
                continue
            base = _base_open(g, old)
            if base is None:
                continue
            for c in old - new:
                g.set_terrain(c[0], c[1], base)
            for c in new - old:
                g.set_terrain(c[0], c[1], terr)
            changed += len(touched)
    return changed


# pontos de interesse por região: lago, ruína, bosquinho, fogueira, oásis, lago gelado...
POI = {
    "praia": ["grove_palm", "campfire"],
    "vila_mare": ["pond", "grove"],
    "bosque": ["pond", "grove", "ruin", "campfire"],
    "minas": ["crystals", "cart", "ruin"],
    "pantano": ["pond", "deadwood"],
    "ossorio": ["ruin", "pond", "grove"],
    "picos": ["ice_pond", "snowman"],
    "deserto": ["oasis", "ruin"],
    "castelo": ["ruin"],
}


def _soft_in(g, area):
    """Decoração simples que ocupa (ou está ancorada em) alguma célula da área."""
    out = []
    for p in g.soft:
        cs = {(p["x"] + dx, p["y"] + dy) for dx, dy in PROPS.get(p["type"], {}).get("collision", [])} | {(p["x"], p["y"])}
        if cs & area:
            out.append(p)
    return out


def _remove_soft(m, g, props):
    for p in props:
        if p in g.soft:
            g.soft.remove(p)
        for c in [c for c, q in g.prop_cells.items() if q is p]:
            del g.prop_cells[c]
        if p in m.get("props", []):
            m["props"].remove(p)


def _blocked(g, c):
    q = g.prop_cells.get(c)
    return q is not None and q not in g.soft


def _empty_spots(g, prot, radius):
    """Centros de áreas vazias: tudo num raio é chão natural livre e não protegido."""
    spots = []
    for y in range(radius + 1, g.h - radius - 1):
        for x in range(radius + 1, g.w - radius - 1):
            ok = True
            for oy in range(-radius, radius + 1):
                for ox in range(-radius, radius + 1):
                    c = (x + ox, y + oy)
                    if g.terrain(*c) not in OPEN or c in prot or _blocked(g, c):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                spots.append((x, y))
    return spots


def stream(m, g, rng, prot, safe, accept, path_band=frozenset()):
    """Riacho de 2 células atravessando a rota, com ponte de tábuas onde cruza a trilha."""
    if not m["id"].startswith("rota_") or m.get("region") not in ("bosque", "vila_mare", "ossorio", "pantano"):
        return 0
    import math
    ys = list(range(8, g.h - 8))
    rng.shuffle(ys)
    for y0 in ys:
        water, bridge = set(), set()
        ok = True
        for x in range(g.w):
            yy = y0 + round(1.4 * math.sin(x / 4.5))
            for y in (yy, yy + 1):
                c = (x, y)
                t = g.terrain(*c)
                if t in TRAILS:
                    bridge.add(c)
                elif t in OPEN:
                    if (c in prot and c not in path_band) or _blocked(g, c):
                        ok = False
                        break
                    water.add(c)
                elif solid_terrain(t):
                    continue
                else:
                    ok = False
                    break
            if not ok:
                break
        if not ok or len(water) < 12 or not bridge:
            continue
        # a trilha precisa atravessar a água (senão a ponte fica solta)
        area = set()
        for (wx, wy) in water | bridge:
            area |= {(wx + ox, wy + oy) for ox in (-1, 0, 1) for oy in (-1, 0, 1)}
        gone = _soft_in(g, area)
        saved = {c: q for c, q in g.prop_cells.items() if q in gone}
        for c in saved:
            del g.prop_cells[c]
        old = {c: g.terrain(*c) for c in water | bridge}
        for c in water:
            g.set_terrain(c[0], c[1], "water")
        for c in bridge:
            g.set_terrain(c[0], c[1], "dock")
        if safe(water):
            accept()
            _remove_soft(m, g, gone)
            for c in water | bridge:
                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        prot.add((c[0] + ox, c[1] + oy))
            return len(water) + len(bridge)
        for c, t in old.items():
            g.set_terrain(c[0], c[1], t)
        g.prop_cells.update(saved)
    return 0


def place_pois(m, g, rng, prot, safe, accept):
    region = m.get("region", "")
    kinds = POI.get(region)
    if not kinds:
        return 0
    spots = _empty_spots(g, prot, 3)
    rng.shuffle(spots)
    used = []
    changed = 0
    budget = max(1, (g.w * g.h) // 520)
    for (x, y) in spots:
        if budget <= 0:
            break
        if any(abs(x - ux) < 9 and abs(y - uy) < 9 for ux, uy in used):
            continue
        kind = kinds[len(used) % len(kinds)]
        props, water, deep, ice = [], set(), set(), set()
        if kind in ("pond", "ice_pond"):
            for oy in range(-2, 3):
                for ox in range(-3, 4):
                    if (ox / 3.2) ** 2 + (oy / 2.2) ** 2 <= 1.0:
                        (water if kind == "pond" else ice).add((x + ox, y + oy))
            if kind == "pond":
                deep = {(x + ox, y) for ox in (-1, 0, 1)}
                props += [{"type": "lilypad", "x": x - 2, "y": y - 1}, {"type": "lilypad", "x": x + 1, "y": y + 1}]
                props += [{"type": "reeds", "x": x + 4, "y": y}, {"type": "reeds", "x": x - 4, "y": y + 1}]
            else:
                props += [{"type": "snowman", "x": x + 4, "y": y - 1}, {"type": "rock_small", "x": x - 4, "y": y + 1}]
        elif kind == "grove":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("tree_oak", 0, -2), ("tree_oak2", -2, 1), ("tree_pine", 2, 1), ("mushrooms", 0, 1), ("stump", 2, -2)]]
        elif kind == "grove_palm":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("palm", 0, -1), ("palm", -2, 1), ("palm", 2, 1), ("rock_small", 0, 2)]]
        elif kind == "ruin":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("broken_column", -2, -2), ("broken_column", 2, -2), ("broken_column", -2, 2), ("rubble", 1, 2), ("rock_small", 0, 0)]]
        elif kind == "campfire":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("campfire", 0, 0), ("log", 0, -2), ("stump", -2, 1), ("stump", 2, 1)]]
        elif kind == "crystals":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("crystal", 0, 0), ("crystal", -2, 1), ("crystal", 2, -1), ("rock_small", 1, 2)]]
        elif kind == "cart":
            props += [{"type": "rails", "x": x + dx, "y": y} for dx in (-2, -1, 0, 1, 2)]
            props += [{"type": "mine_cart", "x": x + 1, "y": y}, {"type": "rubble", "x": x - 1, "y": y + 2}]
        elif kind == "deadwood":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("willow", 0, -1), ("dead_tree", -2, 1), ("glow_shroom", 2, 1), ("mushrooms", 0, 2)]]
        elif kind == "oasis":
            props += [{"type": t, "x": x + dx, "y": y + dy} for t, dx, dy in
                      [("oasis_pool", 0, 0), ("palm", -3, -1), ("palm", 3, 0), ("reeds", 2, 1)]]
        elif kind == "snowman":
            props += [{"type": "snowman", "x": x, "y": y}, {"type": "snow_pine", "x": x - 2, "y": y - 1}, {"type": "snow_pine", "x": x + 2, "y": y - 1}]
        props = [p for p in props if p["type"] in PROPS]
        block = set(water) | set(deep)
        coll = []
        for p in props:
            for dx, dy in PROPS[p["type"]].get("collision", []):
                coll.append((p["x"] + dx, p["y"] + dy))
        if any(g.terrain(*c) not in OPEN or c in prot or _blocked(g, c) for c in coll + list(block | ice)):
            continue
        area = {(x + ox, y + oy) for ox in range(-4, 5) for oy in range(-3, 4)}
        gone = _soft_in(g, area)
        saved = {c: q for c, q in g.prop_cells.items() if q in gone}
        for c in saved:
            del g.prop_cells[c]
        old = {c: g.terrain(*c) for c in block | ice}
        for c in water:
            g.set_terrain(c[0], c[1], "water")
        for c in deep:
            g.set_terrain(c[0], c[1], "deep")
        for c in ice:
            g.set_terrain(c[0], c[1], "ice")
        for p in props:
            for dx, dy in PROPS[p["type"]].get("collision", []):
                g.prop_cells[(p["x"] + dx, p["y"] + dy)] = p
        if safe(block | set(coll)):
            accept()
            _remove_soft(m, g, gone)
            m.setdefault("props", []).extend(props)
            used.append((x, y))
            budget -= 1
            changed += len(props) + len(block | ice)
            for ox in range(-5, 6):
                for oy in range(-4, 5):
                    prot.add((x + ox, y + oy))
        else:
            for c, t in old.items():
                g.set_terrain(c[0], c[1], t)
            for c in coll:
                g.prop_cells.pop(c, None)
            g.prop_cells.update(saved)
    return changed


def refine(m):
    if m.get("refined") or m.get("tileset", "overworld") != "overworld":
        return False
    g = MapGrid(m)
    cells = [(x, y) for y in range(g.h) for x in range(g.w)]
    open_cells = [c for c in cells if g.terrain(*c) in OPEN]
    if g.w * g.h < 300 or len(open_cells) < 0.2 * len(cells):
        return False  # interiores e salões
    region = m.get("region", "")
    rng = random.Random("refine:" + m["id"])
    meandered = meander(m, g, rng)
    open_cells = [c for c in cells if g.terrain(*c) in OPEN]

    # células protegidas
    prot = set(g.near_props)

    def protect(cx, cy, r):
        for ox in range(-r, r + 1):
            for oy in range(-r, r + 1):
                prot.add((cx + ox, cy + oy))

    for w in m.get("warps", []):
        protect(w["x"], w["y"], 2)
    for n in m.get("npcs", []):
        protect(n["x"], n["y"], 2)
    for sp in m.get("spawns", []):
        protect(int(sp["x"]), int(sp["y"]), 1)
    sp0 = m.get("spawn", {})
    start = (int(sp0.get("x", 0)), int(sp0.get("y", 0)))
    protect(start[0], start[1], 2)
    for p in m.get("props", []):
        if p.get("dialog") or PROPS.get(p["type"], {}).get("interactive"):
            protect(p["x"], p["y"], 2)

    hard = set(prot)
    for c in cells:
        if g.terrain(*c) in PATHS or g.terrain(*c) in {"water", "deep", "swamp"}:
            protect(c[0], c[1], 1)
    path_band = prot - hard

    # NPCs e conteúdo condicional contam como passagem livre no teste de alcance
    if not g.walkable(start):
        for w in m.get("warps", []):
            if g.walkable((w["x"], w["y"])):
                start = (w["x"], w["y"])
                break
    targets = {(w["x"], w["y"]) for w in m.get("warps", [])}
    for n in m.get("npcs", []) + [p for p in m.get("props", []) if p.get("dialog")]:
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            targets.add((n["x"] + d[0], n["y"] + d[1]))
    targets |= {(int(s["x"]), int(s["y"])) for s in m.get("spawns", [])}
    base = g.reach(start)
    goal = targets & base

    def safe(block):
        """block: células que deixam de ser passáveis. Aceita se não corta nada."""
        after = g.reach(start)
        return goal <= after and len(after) >= len(base) - len(block)

    changed = meandered

    def accept():
        nonlocal base
        base = g.reach(start)

    # 0. riacho com ponte e pontos de interesse nas áreas vazias
    changed += stream(m, g, rng, prot, safe, accept, path_band)
    changed += place_pois(m, g, rng, prot, safe, accept)
    open_cells = [c for c in cells if g.terrain(*c) in OPEN]

    # 1. reentrâncias nas bordas da mata/rocha
    edge = []
    for (x, y) in open_cells:
        if (x, y) in prot:
            continue
        walls = [g.terrain(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if g.terrain(x + dx, y + dy) in WALLS]
        if walls:
            edge.append(((x, y), walls[0]))
    rng.shuffle(edge)
    grown = []
    for (x, y), wall in edge[: int(len(edge) * 0.45)]:
        old = g.terrain(x, y)
        g.set_terrain(x, y, wall)
        if safe({(x, y)}):
            base = g.reach(start)
            changed += 1
            grown.append(((x, y), wall))
        else:
            g.set_terrain(x, y, old)
    # segunda camada: algumas reentrâncias viram "dentes" mais fundos
    for (x, y), wall in grown[: len(grown) // 3]:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if g.terrain(*n) in OPEN and n not in prot and rng.random() < 0.5:
                old = g.terrain(*n)
                g.set_terrain(n[0], n[1], wall)
                if safe({n}):
                    base = g.reach(start)
                    changed += 1
                else:
                    g.set_terrain(n[0], n[1], old)
                break

    # copas: árvores e pedras por cima da mata/rocha (só onde tudo em volta já é parede)
    taken = [(p["x"], p["y"]) for p in m.get("props", [])]
    for (x, y) in cells:
        t = g.terrain(x, y)
        kinds = CANOPY.get(t, {}).get(region)
        if not kinds or rng.random() > 0.22:
            continue
        if any(g.terrain(x + dx, y + dy) != t for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            continue
        if any(abs(x - px) < 2 and abs(y - py) < 2 for px, py in taken):
            continue
        kind = rng.choice(kinds)
        if kind not in PROPS:
            continue
        m.setdefault("props", []).append({"type": kind, "x": x, "y": y})
        taken.append((x, y))
        changed += 1

    # 2. manchas de flores
    if region in FLOWER_REGIONS:
        grass = [c for c in open_cells if g.terrain(*c) == "grass" and c not in prot]
        for _ in range(max(1, len(grass) // 140)):
            if not grass:
                break
            cx, cy = rng.choice(grass)
            for ox in range(-1, 2):
                for oy in range(-1, 2):
                    if rng.random() < 0.6 and g.terrain(cx + ox, cy + oy) == "grass" and (cx + ox, cy + oy) not in prot:
                        g.set_terrain(cx + ox, cy + oy, "flowers")
                        changed += 1

    # 3. detalhes da região
    palette = DECOR.get(region, [])
    if palette:
        free = [c for c in cells if g.terrain(*c) in OPEN and c not in prot and c not in g.prop_cells]
        rng.shuffle(free)
        want = len(free) // 26
        placed = []
        for (x, y) in free:
            if want <= 0:
                break
            if any(abs(x - px) <= 2 and abs(y - py) <= 2 for px, py in placed):
                continue
            opts = [(t, w) for t, terr, w in palette if g.terrain(x, y) in terr and t in PROPS]
            if not opts:
                continue
            t = rng.choices([o[0] for o in opts], weights=[o[1] for o in opts])[0]
            coll = [(x + dx, y + dy) for dx, dy in PROPS[t].get("collision", [])]
            if any(c in prot or c in g.prop_cells or g.terrain(*c) not in OPEN for c in coll):
                continue
            prop = {"type": t, "x": x, "y": y}
            for c in coll:
                g.prop_cells[c] = prop
            if coll and not safe(set(coll)):
                for c in coll:
                    del g.prop_cells[c]
                continue
            if coll:
                base = g.reach(start)
            m.setdefault("props", []).append(prop)
            placed.append((x, y))
            want -= 1
            changed += 1

    m["ground"] = ["".join(r) for r in g.rows]
    m["legend"] = g.legend
    m["refined"] = True
    return changed


def main(ids):
    total = 0
    for f in sorted((ROOT / "data/maps").glob("*.json")):
        if ids and f.stem not in ids:
            continue
        m = json.loads(f.read_text(encoding="utf-8"))
        n = refine(m)
        if n is False:
            continue
        f.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        total += 1
        print(f"refine: {f.stem} ({n} mudanças)")
    print(f"refine: {total} mapas refinados")


if __name__ == "__main__":
    main(sys.argv[1:])
