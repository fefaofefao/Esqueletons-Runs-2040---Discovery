"""Kit para montar uma região (fase 4c em diante) a partir de uma fonte única.

Uma região define: textos (PT/EN/ES), roteiros (diálogos com ações), NPCs,
tabelas de encontro, loja, itens, mapas e o documento de roteiro. Region.write()
grava tudo nos arquivos do jogo e gera docs/roteiro/<nn>_<id>.md com todas as
falas — o roteiro e o jogo saem da mesma fonte, então nunca divergem.
"""
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


# ------------------------------------------------------------------ grade
class Grid:
    def __init__(self, w, h, base):
        self.w, self.h = w, h
        self.g = [[base] * w for _ in range(h)]

    def fill(self, x0, y0, x1, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    self.g[y][x] = c

    def path(self, pts, c, width=2):
        """Caminho em L entre pontos (largura 'width')."""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 == x1:
                self.fill(x0, y0, x0 + width - 1, y1, c)
            else:
                self.fill(x0, y0, x1, y0 + width - 1, c)

    def at(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return None

    def rows(self):
        return ["".join(r) for r in self.g]


def scatter(grid, props, area, n, seed, kinds, ok="gf", avoid=(), spacing=2):
    r = random.Random(seed)
    x0, y0, x1, y1 = area
    taken = []
    tries = 0
    while len(taken) < n and tries < 3000:
        tries += 1
        x, y = r.randint(x0, x1), r.randint(y0, y1)
        if grid.at(x, y) not in ok or grid.at(x - 1, y) not in ok:
            continue
        if any(abs(x - ax) <= spacing and abs(y - ay) <= spacing for ax, ay in taken + list(avoid)):
            continue
        taken.append((x, y))
        props.append({"type": r.choice(kinds), "x": x, "y": y})


def room(mid, region, name_key, back_map, back_xy, props, npcs, floor="floor", wall="wall", top="wall_top"):
    rows = ["TTTTTTTTTTTT", "TwwnwwwwwnwT"] + ["T..........T"] * 7 + ["TTTTTTmTTTTT"]
    return {"id": mid, "region": region, "name_key": name_key, "tileset": "overworld",
            "legend": {"T": top, "w": wall, "n": "wall_window" if wall == "wall" else wall, ".": floor, "m": "mat"},
            "ground": rows, "spawn": {"x": 6, "y": 8, "facing": "up"}, "props": props, "npcs": npcs,
            "warps": [{"x": 6, "y": 9, "to": back_map, "tx": back_xy[0], "ty": back_xy[1] + 1, "facing": "down", "sfx": "door"}]}


# ------------------------------------------------------------------ roteiro
def say(k, spk=None):
    n = {"say": k}
    if spk:
        n["speaker"] = spk
    return n


def ask(k, spk, options):
    """options: [(texto_key, goto_ou_None)]"""
    ch = []
    for t, g in options:
        o = {"text": t}
        if g:
            o["goto"] = g
        ch.append(o)
    n = {"say": k, "choice": ch}
    if spk:
        n["speaker"] = spk
    return n


def battle(tamer, enemies, reward, flag=None, items=None, kind="tamer", marker=None):
    a = {"action": "battle", "kind": kind, "tamer_key": tamer, "enemies": enemies, "reward": reward}
    if flag:
        a["win_flag"] = flag
    if items:
        a["items"] = items
    if marker:
        a["marker"] = marker
    return a


def act(name, **kw):
    a = {"action": name}
    a.update(kw)
    return a


def flag(name, value=True):
    return {"set_flag": name, "value": value}


def goto(ref):
    return {"goto": ref}


def human(sid, name, dialog, behavior="look_around", tamer=None, role="hint"):
    e = {"name_key": name, "role": role, "sprite": f"res://assets/sprites/npc/{sid}.png", "frames": 2, "idle_fps": 1.2,
         "behavior": behavior, "look_dirs": ["down", "left", "right"], "dialog": dialog}
    if tamer:
        e["tamer"] = tamer
    return e


def skel(sprite, name, dialog, tamer=None, role="story"):
    e = {"name_key": name, "role": role, "sprite": f"res://assets/sprites/npc/{sprite}.png", "frames": 2, "idle_fps": 2.0,
         "behavior": "stand", "dialog": dialog}
    if tamer:
        e["tamer"] = tamer
    return e


# ------------------------------------------------------------------ região
class Region:
    def __init__(self, rid, number, dialog_file, region_ids):
        self.id = rid
        self.number = number
        self.dialog_file = dialog_file
        self.region_ids = region_ids
        self.T = {}
        self.D = {}
        self.NPCS = {}
        self.TABLES = {}
        self.SHOPS = {}
        self.ITEMS = {}
        self.MAPS = {}
        self.ALLOW = []
        self.DOC = {}
        self.NPC_DOC = []      # (nome, função, motivo)
        self.CHOICES = []      # (escolha, opções, consequência)
        self.HOUSES = []       # (dono, tema, recompensa)
        self.BATTLE_BG = {}
        self.CITIES = []       # cities.json: {id, map, ranch, shop, tamer_houses, npcs, quests}
        self.ROUTES = []       # routes.json: {id, map, paths: [{kind, required}]}
        self.order = []        # ordem dos diálogos no documento

    def t(self, key, pt, en, es):
        self.T[key] = (pt, en, es)
        if pt == en or pt == es:
            self.ALLOW.append(key)
        return key

    def d(self, ref, nodes):
        self.D[ref] = nodes
        self.order.append(ref)
        return f"{self.dialog_file}/{ref}"

    def ref(self, name):
        return f"{self.dialog_file}/{name}"

    # -------------------------------------------------------------- gravação
    def write(self):
        (ROOT / f"data/dialogs/{self.dialog_file}.json").write_text(json.dumps(
            {"_comment": f"Gerado por tools/maps/{self.id}.py (fonte única do roteiro).", "dialogs": self.D},
            ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        self._merge("data/npcs.json", "npcs", self.NPCS)
        self._merge("data/encounters.json", "tables", self.TABLES)
        self._merge("data/shops.json", "shops", self.SHOPS)
        self._merge("data/items.json", "items", self.ITEMS)
        self._merge_list("data/cities.json", "cities", self.CITIES)
        self._merge_list("data/routes.json", "routes", self.ROUTES)
        for mid, m in self.MAPS.items():
            for r in m["ground"]:
                assert len(r) == len(m["ground"][0]), mid
            (ROOT / "data/maps" / f"{mid}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        regions = json.loads((ROOT / "data/regions.json").read_text())
        for mid, m in self.MAPS.items():
            reg = regions["regions"][m["region"]]
            if mid not in reg["maps"]:
                reg["maps"].append(mid)
        for rid, bg in self.BATTLE_BG.items():
            regions["regions"][rid]["battle_bg"] = bg
        (ROOT / "data/regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        self._write_csv()
        self._write_allow()
        self._write_doc()
        print(f"{self.id}: {len(self.T)} textos, ~{self.words()} palavras PT-BR, {len(self.MAPS)} mapas")

    def _merge(self, path, key, values):
        if not values:
            return
        p = ROOT / path
        d = json.loads(p.read_text())
        d.setdefault(key, {}).update(values)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def _merge_list(self, path, key, items):
        if not items:
            return
        p = ROOT / path
        d = json.loads(p.read_text()) if p.exists() else {"_comment": "Gerado pelos scripts de região (tools/maps). Conferido por tools/validate_data.py.", key: []}
        ids = {i["id"] for i in items}
        d[key] = [x for x in d.get(key, []) if x["id"] not in ids] + list(items)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def tamer(self, nid, sprite, name, ref, flag, vision=4, if_=None):
        """NPC domador: luta uma vez (flag) e depois repete a fala final."""
        self.NPCS[nid] = human(sprite, name, [{"if": flag, "dialog": self.ref(ref + "_depois")}, {"dialog": self.ref(ref)}], "stand",
                               {"vision": vision, "flag": flag}, "tamer")
        return nid

    def _write_csv(self):
        path = ROOT / "i18n/dialogue.csv"
        rows = list(csv.reader(open(path, encoding="utf-8")))
        header, body = rows[0], [r for r in rows[1:] if r and r[0] not in self.T]
        body += [[k, *v] for k, v in self.T.items()]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(body)

    def _write_allow(self):
        p = ROOT / "i18n/allow_identical.txt"
        text = p.read_text(encoding="utf-8")
        start = f"# --- região {self.id} (nomes próprios iguais nos idiomas) ---"
        end = f"# --- fim {self.id} ---"
        if start in text:
            a = text.index(start)
            b = text.index(end) + len(end)
            text = text[:a].rstrip("\n") + "\n" + text[b:].lstrip("\n")
        block = "\n".join([start] + self.ALLOW + [end]) + "\n"
        marker = "# --- gerado por tools/bestiary/build.py"
        if marker in text:
            i = text.index(marker)
            text = text[:i] + block + text[i:]
        else:
            text = text.rstrip("\n") + "\n" + block
        p.write_text(text, encoding="utf-8")

    def words(self):
        return sum(len(v[0].split()) for k, v in self.T.items() if k.startswith(("DLG_", "SIGN_", "OBJ_")))

    def _speaker(self, key):
        return self.T.get(key, (key,))[0] if key else ""

    def _text(self, key):
        if key in self.T:
            return self.T[key][0]
        return f"`{key}`"

    def _write_doc(self):
        D = self.DOC
        L = [f"# Roteiro — {D['title']}", "",
             f"Fase {D['phase']}. **Gerado por `tools/maps/{self.id}.py`**, a mesma fonte que grava os mapas, NPCs e diálogos do jogo, "
             f"portanto o jogo implementa exatamente o que está aqui. Diálogos em `data/dialogs/{self.dialog_file}.json`.", "",
             f"**Duração alvo:** {D['duration']}. **Idades:** {D['ages']}.", "",
             "## 1. Problema local", D["problem"], "",
             f"## 2. Pista de 2040 (nº {D['clue_n']})", D["clue"], "",
             "## 3. Momento de Lia e Taro", *[f"- {x}" for x in D["moment"]], ""]
        g = D["guardian"]
        L += ["## 4. Guardião: " + g["name"],
              f"- **Parentesco:** {g['kin']}",
              f"- **Personalidade:** {g['personality']}",
              f"- **Motivo para servir ao Rei:** {g['motive']}",
              f"- **Mecânica-tema:** {g['mechanic']}",
              f"- **Equipe:** {g['team']}",
              f"- **Recompensa:** {g['reward']}", ""]
        L += ["## 5. Mapas", "| Mapa | Conteúdo |", "|---|---|"]
        L += [f"| {a} | {b} |" for a, b in D["maps"]]
        L += ["", "## 6. NPCs e motivo de existir", "| NPC | Função | Por que existe |", "|---|---|---|"]
        L += [f"| {a} | {b} | {c} |" for a, b, c in self.NPC_DOC]
        L += ["", "## 7. Casas de domadores", "| Dono | Tema da equipe | Recompensa |", "|---|---|---|"]
        L += [f"| {a} | {b} | {c} |" for a, b, c in self.HOUSES]
        L += ["", "## 8. Escolhas e consequências", "| Escolha | Opções | Consequência |", "|---|---|---|"]
        L += [f"| {a} | {b} | {c} |" for a, b, c in self.CHOICES]
        L += ["", "## 9. Falas (PT-BR, na ordem dos roteiros)", ""]
        for ref in self.order:
            L.append(f"### `{self.dialog_file}/{ref}`")
            for n in self.D[ref]:
                L.append(self._node_line(n))
            L.append("")
        L += ["## 10. Contagem", f"Cerca de **{self.words()} palavras** de texto de jogo em PT-BR nesta região."]
        (ROOT / f"docs/roteiro/{self.number:02d}_{self.id}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    def _node_line(self, n):
        cond = []
        for k in ("if", "if_not"):
            if k in n:
                cond.append(f"{k} {n[k]}")
        for k in ("if_all", "if_any"):
            if k in n:
                cond.append(f"{k} {', '.join(n[k])}")
        if "if_count" in n:
            cond.append(f"pelo menos {n['if_count']['min']} de {', '.join(n['if_count']['flags'])}")
        c = f" *({'; '.join(cond)})*" if cond else ""
        if "say" in n or "choice" in n:
            spk = self._speaker(n.get("speaker", ""))
            line = f"- {'**' + spk + ':** ' if spk else '*(narração)* '}{self._text(n['say']) if 'say' in n else ''}{c}"
            if "choice" in n:
                opts = " / ".join(f"\"{self._text(o['text'])}\"" + (f" → `{o['goto']}`" if o.get("goto") else "") for o in n["choice"])
                line += f"\n  - (escolha) {opts}"
            return line
        if "action" in n:
            a = dict(n)
            name = a.pop("action")
            if name == "battle":
                team = ", ".join(f"{self._sp(e[0])} {e[1]}" for e in a["enemies"])
                extra = f" · {a.get('reward', 0)} moedas" if a.get("reward") else ""
                if a.get("items"):
                    extra += " + " + ", ".join(f"{i[1]}× {i[0]}" for i in a["items"])
                return f"- *[batalha {a.get('kind')}: {team}{extra}]*{c}"
            return f"- *[ação {name}: {json.dumps(a, ensure_ascii=False)}]*{c}"
        if "set_flag" in n:
            return f"- *[flag {n['set_flag']} = {n.get('value', True)}]*{c}"
        if "goto" in n:
            return f"- *[vai para `{n['goto']}`]*{c}"
        return f"- {json.dumps(n, ensure_ascii=False)}"

    def _sp(self, sid):
        p = ROOT / "i18n/species.csv"
        for r in csv.reader(open(p, encoding="utf-8")):
            if r and r[0] == "SPECIES_" + sid.upper():
                return r[1]
        return sid


# ------------------------------------------------------------------ espécies
_SPECIES = None


def stage_id(line, age):
    """Id da espécie coerente com a idade (estágio pela idade de crescimento)."""
    global _SPECIES
    if _SPECIES is None:
        _SPECIES = json.loads((ROOT / "data/species.json").read_text())
    for ln in _SPECIES["lines"]:
        if ln["id"] == line:
            g1, g2 = ln["growth_levels"]
            st = 1 if age < g1 else (2 if age < g2 else 3)
            return f"{line}_{st}"
    return line  # único / Rei


def team(spec):
    """[(linha, idade)] -> [[espécie, idade]] com estágio coerente."""
    return [[stage_id(l, a), a] for l, a in spec]


# ------------------------------------------------------------------ rota com 3 caminhos
def make_route(rid, region, name_key, legend, south, north, *, gate=None, tamers=(), hint=None, sign=None,
               spawns=(), extra_npcs=(), extra_props=(), deco=("rock_small",), deco_ok="g", tint=None, seed=1):
    """Rota padrão 40×50 (seção 7): Caminho dos Domadores a oeste, Caminho
    Selvagem (campo 'f') a leste e Atalho central fechado por 'gate' (objeto
    com flag). Os 3 se reencontram na zona norte, antes da cidade.
    south/north: (mapa, tx, ty)."""
    W, H = 40, 50
    g = Grid(W, H, "B")
    g.fill(2, 36, 37, 48, "g")
    g.fill(19, 36, 20, 49, "p")
    g.fill(19, 14, 20, 35, "p")                       # atalho central
    g.fill(3, 39, 18, 41, "g"); g.fill(3, 40, 18, 40, "p")
    g.fill(2, 9, 8, 41, "g"); g.fill(4, 10, 5, 40, "p")
    g.fill(4, 9, 18, 12, "g"); g.fill(4, 10, 18, 11, "p")
    g.fill(21, 39, 35, 41, "g"); g.fill(21, 40, 34, 40, "p")
    g.fill(25, 9, 38, 39, "f")
    g.fill(33, 10, 34, 40, "p")
    g.fill(21, 9, 34, 12, "g"); g.fill(21, 10, 34, 11, "p")
    r = random.Random(seed)
    for _ in range(6):
        x, y = r.randint(26, 36), r.randint(14, 36)
        g.fill(x, y, x + 1, y + 1, "g")
    g.fill(2, 2, 37, 13, "g")
    g.fill(19, 0, 20, 13, "p")
    props = list(extra_props)
    if gate:
        for y in (35, 15):
            gp = dict(gate)
            gp.update({"x": 20, "y": y})
            props.append(gp)
    if sign:
        props.append({"type": "sign", "x": 18, "y": 42, "dialog": sign})
    scatter(g, props, (3, 43, 36, 47), 8, seed + 1, list(deco), ok=deco_ok, avoid=[(19, 44), (20, 44), (22, 42), (18, 42)])
    scatter(g, props, (3, 2, 36, 8), 9, seed + 2, list(deco), ok=deco_ok, avoid=[(19, 4), (20, 4), (26, 13), (10, 6)])
    scatter(g, props, (2, 12, 8, 38), 5, seed + 3, list(deco), ok=deco_ok, avoid=[(6, 30), (3, 20)])
    npcs = []
    spots = [(6, 30, "left"), (3, 20, "right"), (12, 9, "down")]
    for (nid, cond), (x, y, f) in zip(tamers, spots):
        e = {"id": nid, "x": x, "y": y, "facing": f}
        e.update(cond)
        npcs.append(e)
    if hint:
        npcs.append({"id": hint, "x": 22, "y": 42, "facing": "left"})
    npcs += list(extra_npcs)
    m = {"id": rid, "region": region, "name_key": name_key, "tileset": "overworld", "legend": legend,
         "ground": g.rows(), "spawn": {"x": 19, "y": 47, "facing": "up"}, "props": props, "npcs": npcs,
         "warps": [{"x": 19, "y": 49, "to": south[0], "tx": south[1], "ty": south[2], "facing": "down", "sfx": ""},
                   {"x": 20, "y": 49, "to": south[0], "tx": south[1] + 1, "ty": south[2], "facing": "down", "sfx": ""},
                   {"x": 19, "y": 0, "to": north[0], "tx": north[1], "ty": north[2], "facing": "up", "sfx": ""},
                   {"x": 20, "y": 0, "to": north[0], "tx": north[1] + 1, "ty": north[2], "facing": "up", "sfx": ""}],
         "spawns": list(spawns), "ambient": []}
    if tint:
        m["tint"] = tint
    return m


# ------------------------------------------------------------------ cidade padrão
def make_town(tid, region, name_key, legend, *, south, north, west, houses, npcs, props=(), deco=(), deco_ok="g",
              north_guard=None, tint=None, seed=10, plaza="p"):
    """Cidade 40×32 (seção 6): Rancho (12,10), Loja (27,10), casas em (8,20),
    (31,20) e (14,27); praça; saída sul (rota anterior), norte (próxima rota,
    vigiada por 'north_guard' até o Guardião perder) e oeste (área especial)."""
    W, H = 40, 32
    g = Grid(W, H, "g")
    g.fill(0, 0, W - 1, 0, "B"); g.fill(0, 0, 0, H - 1, "B"); g.fill(W - 1, 0, W - 1, H - 1, "B"); g.fill(0, H - 1, W - 1, H - 1, "B")
    g.fill(19, 0, 20, H - 1, "p")
    g.fill(14, 12, 25, 18, plaza); g.fill(9, 11, 30, 11, "p"); g.fill(6, 21, 33, 21, "p")
    g.fill(9, 11, 9, 21, "p"); g.fill(30, 11, 30, 21, "p")
    g.fill(0, 15, 14, 16, "p")
    g.fill(14, 21, 14, 27, "p")
    pr = [{"type": houses[0], "x": 12, "y": 10}, {"type": houses[1], "x": 27, "y": 10},
          {"type": houses[2], "x": 8, "y": 20}, {"type": houses[3], "x": 31, "y": 20}, {"type": houses[4], "x": 14, "y": 27}]
    pr += list(props)
    if deco:
        scatter(g, pr, (2, 1, 11, 8), 4, seed, list(deco), ok=deco_ok)
        scatter(g, pr, (28, 1, 37, 8), 4, seed + 1, list(deco), ok=deco_ok)
        scatter(g, pr, (2, 23, 11, 29), 3, seed + 2, list(deco), ok=deco_ok, avoid=[(8, 20)])
        scatter(g, pr, (25, 23, 37, 29), 3, seed + 3, list(deco), ok=deco_ok, avoid=[(31, 20)])
    nl = list(npcs)
    if north_guard:
        nl.append(north_guard)
    m = {"id": tid, "region": region, "name_key": name_key, "tileset": "overworld", "legend": legend,
         "ground": g.rows(), "spawn": {"x": 19, "y": 29, "facing": "up"}, "props": pr, "npcs": nl,
         "warps": [{"x": 19, "y": H - 1, "to": south[0], "tx": south[1], "ty": south[2], "facing": "down", "sfx": ""},
                   {"x": 20, "y": H - 1, "to": south[0], "tx": south[1] + 1, "ty": south[2], "facing": "down", "sfx": ""},
                   {"x": 19, "y": 0, "to": north[0], "tx": north[1], "ty": north[2], "facing": "up", "sfx": ""},
                   {"x": 20, "y": 0, "to": north[0], "tx": north[1] + 1, "ty": north[2], "facing": "up", "sfx": ""},
                   {"x": 0, "y": 15, "to": west[0], "tx": west[1], "ty": west[2], "facing": "left", "sfx": ""},
                   {"x": 0, "y": 16, "to": west[0], "tx": west[1], "ty": west[2] + 1, "facing": "left", "sfx": ""}],
         "ambient": []}
    if tint:
        m["tint"] = tint
    return m


TOWN_DOORS = {"rancho": (12, 10), "loja": (27, 10), "a": (8, 20), "b": (31, 20), "c": (14, 27)}


def town_doors(m, tid, rooms):
    """rooms: {'rancho': mapa, 'loja': mapa, 'a': mapa, 'b': mapa, 'c': mapa}"""
    for k, mid in rooms.items():
        x, y = TOWN_DOORS[k]
        m["warps"].append({"x": x, "y": y, "to": mid, "tx": 6, "ty": 8, "facing": "up", "sfx": "door"})


# ------------------------------------------------------------------ área especial (caverna/arena)
def make_lair(lid, region, name_key, legend, *, east, guardian_npc, extra_npcs=(), props=(), spawns=(), tint=None, on_enter=()):
    """Área especial 34×22: entrada a leste (volta à cidade), corredor com
    salão de selvagens, câmara do segredo (sul) e arena do Guardião (norte)."""
    W, H = 34, 22
    g = Grid(W, H, "B")
    g.fill(28, 9, 33, 12, "p")                 # entrada
    g.fill(18, 8, 29, 13, "g")                 # salão 1
    g.fill(13, 10, 18, 11, "p")
    g.fill(3, 12, 13, 19, "g")                 # câmara sul (segredo/único)
    g.fill(6, 3, 13, 11, "p")
    g.fill(3, 1, 17, 6, "f")                   # arena do Guardião
    m = {"id": lid, "region": region, "name_key": name_key, "tileset": "overworld", "legend": legend,
         "ground": g.rows(), "spawn": {"x": 31, "y": 10, "facing": "left"}, "props": list(props),
         "npcs": [guardian_npc] + list(extra_npcs),
         "warps": [{"x": 33, "y": 10, "to": east[0], "tx": east[1], "ty": east[2], "facing": "right", "sfx": ""},
                   {"x": 33, "y": 11, "to": east[0], "tx": east[1], "ty": east[2] + 1, "facing": "right", "sfx": ""}],
         "spawns": list(spawns), "ambient": []}
    if tint:
        m["tint"] = tint
    if on_enter:
        m["on_enter"] = list(on_enter)
    return m
