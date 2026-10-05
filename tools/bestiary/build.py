#!/usr/bin/env python3
"""Gera, a partir de tools/bestiary/bestiary.py:
  - i18n/species.csv  (SPECIES_<ID> nomes e OSS_<ID> entradas do Ossário)
  - data/species.json (linhas, únicos e Rei; atributos dentro das bandas)
  - docs/BESTIARIO.md (a bíblia de criaturas legível)

Atributos: perfil do papel (role) × total do estágio. Os totais ficam dentro
das bandas da seção 11 (Bebê 250–320, Adolescente 360–430, Adulto 470–540,
únicos 450–520, Rei ≈600); a raridade puxa para o alto da banda.
Os golpes (learnset) são definidos na fase 3c em tools/bestiary/moves.py; se o
arquivo existir, este script também os aplica.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import bestiary as B  # noqa: E402

STATS = ["hp", "atk", "mag", "def", "res", "spd"]
ROLE = {
    "tanque":      {"hp": 1.25, "atk": 0.95, "mag": 0.70, "def": 1.30, "res": 1.10, "spd": 0.70},
    "bruto":       {"hp": 1.10, "atk": 1.40, "mag": 0.60, "def": 1.05, "res": 0.80, "spd": 1.05},
    "veloz":       {"hp": 0.90, "atk": 1.15, "mag": 0.95, "def": 0.80, "res": 0.85, "spd": 1.35},
    "equilibrado": {"hp": 1.05, "atk": 1.00, "mag": 1.00, "def": 1.00, "res": 1.00, "spd": 0.95},
    "mago":        {"hp": 0.95, "atk": 0.60, "mag": 1.40, "def": 0.80, "res": 1.15, "spd": 1.10},
    "suporte":     {"hp": 1.15, "atk": 0.65, "mag": 1.10, "def": 1.00, "res": 1.20, "spd": 0.90},
    "astuto":      {"hp": 0.95, "atk": 1.05, "mag": 1.05, "def": 0.90, "res": 0.95, "spd": 1.10},
    "rei":         {"hp": 1.10, "atk": 1.00, "mag": 1.15, "def": 0.95, "res": 1.00, "spd": 0.80},
}
STAGE_TOTAL = {1: (262, 300), 2: (372, 412), 3: (482, 522)}  # (comum, raro)
RARITY_T = {"comum": 0.0, "incomum": 0.5, "raro": 1.0, "unico": 1.0}
UNIQUE_TOTAL = 490
KING_TOTAL = 600
BASE_XP = {1: 50, 2: 110, 3: 180}


def stats_for(role, typ, total):
    w = dict(ROLE[role])
    # quem ataca com magia (mágico, cura) usa MAG como atributo principal
    if typ in ("magico", "cura") and w["atk"] > w["mag"]:
        w["atk"], w["mag"] = w["mag"], w["atk"]
    if typ == "fisico" and w["mag"] > w["atk"]:
        w["atk"], w["mag"] = w["mag"], w["atk"]
    s = sum(w.values())
    out = {k: int(round(total * w[k] / s)) for k in STATS}
    out["hp"] += total - sum(out.values())
    return out


def key(sid):
    return "SPECIES_" + sid.upper()


def okey(sid):
    return "OSS_" + sid.upper()


def load_moves():
    p = Path(__file__).parent / "moves.py"
    if not p.exists():
        return None
    import moves as M  # noqa: E402
    return M


def build():
    rows = []
    lines_out = []
    M = load_moves()
    for ln in B.LINES:
        stages = []
        lo, hi = 0, 0
        for i, st in enumerate(ln["stages"], start=1):
            sid = f"{ln['id']}_{i}"
            rows.append([key(sid), st["pt"], st["en"], st["es"]])
            rows.append([okey(sid), st["entry"]["pt"], st["entry"]["en"], st["entry"]["es"]])
            lo, hi = STAGE_TOTAL[i]
            total = int(round(lo + (hi - lo) * RARITY_T[ln["rarity"]]))
            entry = {"id": sid, "name_key": key(sid), "entry_key": okey(sid),
                     "stats": stats_for(ln["role"], ln["type"], total), "base_xp": BASE_XP[i] + (10 if ln["rarity"] == "raro" else 0),
                     "sprite": f"res://assets/skeletons/{sid}.png", "map_sprite": f"res://assets/skeletons/map/{sid}.png"}
            if M:
                entry["learnset"] = M.learnset(ln, i)
                gm = M.growth_move(ln, i)
                if gm:
                    entry["growth_move"] = gm
            stages.append(entry)
        lines_out.append({"id": ln["id"], "type": ln["type"], "region": ln["region"], "rarity": ln["rarity"],
                          "growth_levels": ln["growth"], "signature_move": ln["signature"]["id"],
                          "gender": ln["gender"], "map_behavior": ln["behavior"], "starter": ln.get("starter", ""),
                          "stages": stages})
    uniques = []
    for u in B.UNIQUES:
        rows.append([key(u["id"]), u["names"]["pt"], u["names"]["en"], u["names"]["es"]])
        rows.append([okey(u["id"]), u["entry"]["pt"], u["entry"]["en"], u["entry"]["es"]])
        e = {"id": u["id"], "name_key": key(u["id"]), "entry_key": okey(u["id"]), "type": u["type"],
             "region": u["region"], "rarity": "unico", "gender": u["gender"], "map_behavior": u["behavior"],
             "stats": stats_for(u["role"], u["type"], UNIQUE_TOTAL), "base_xp": 170,
             "sprite": f"res://assets/skeletons/{u['id']}.png", "map_sprite": f"res://assets/skeletons/map/{u['id']}.png"}
        if M:
            e["learnset"] = M.learnset_unique(u)
        uniques.append(e)
    k = B.KING
    rows.append([key(k["id"]), k["names"]["pt"], k["names"]["en"], k["names"]["es"]])
    rows.append([okey(k["id"]), k["entry"]["pt"], k["entry"]["en"], k["entry"]["es"]])
    king = {"id": k["id"], "name_key": key(k["id"]), "entry_key": okey(k["id"]), "type": k["type"],
            "region": k["region"], "rarity": "unico", "gender": k["gender"], "map_behavior": k["behavior"],
            "stats": stats_for("rei", k["type"], KING_TOTAL), "base_xp": 400,
            "sprite": f"res://assets/skeletons/{k['id']}.png", "map_sprite": f"res://assets/skeletons/map/{k['id']}.png"}
    if M:
        king["learnset"] = M.learnset_unique(k)
    # número do Ossário: ordem das regiões, linhas antes dos únicos da região
    n = 0
    for reg in B.REGION_ORDER:
        for ln in lines_out:
            if ln["region"] == reg:
                for st in ln["stages"]:
                    n += 1
                    st["number"] = n
        for u in uniques:
            if u["region"] == reg:
                n += 1
                u["number"] = n
    king["number"] = 80
    data = {"lines": lines_out, "uniques": uniques, "king": king}
    (ROOT / "data/species.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with open(ROOT / "i18n/species.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["keys", "pt_BR", "en", "es"])
        w.writerows(rows)
    write_doc(data)
    print(f"bestiário: {len(lines_out)} linhas, {len(uniques)} únicos, rei; {len(rows)} textos")


def write_doc(data):
    num = {}
    for ln in data["lines"]:
        for st in ln["stages"]:
            num[st["id"]] = st["number"]
    for u in data["uniques"]:
        num[u["id"]] = u["number"]
    out = ["# Bestiário — Esqueletons Runs 2040: Edição Discovery", "",
           "A bíblia de criaturas (seção 8 do AGENTS.md). **Fonte única:** `tools/bestiary/bestiary.py`; "
           "este arquivo, `data/species.json` e `i18n/species.csv` são gerados por `tools/bestiary/build.py`. "
           "Sprites: `tools/art/gen_skeletons.py`. Folha de revisão visual: `docs/bestiario_sheet.png`.", "",
           "**80 espécies no Ossário:** 24 linhas × 3 estágios (Bebê → Adolescente → Adulto), 7 únicos e o Rei.", ""]
    # resumo
    from collections import Counter
    tc = Counter(ln["type"] for ln in B.LINES)
    out.append("| Tipo | Linhas |")
    out.append("|---|---|")
    for t in ["fisico", "magico", "cura", "veneno"]:
        out.append(f"| {B.TYPE_PT[t]} | {tc[t]} |")
    out.append("")
    out.append("| Região | Linhas novas | Único |")
    out.append("|---|---|---|")
    for reg in B.REGION_ORDER:
        ls = [ln["stages"][0]["pt"] + "/" + ln["stages"][2]["pt"] for ln in B.LINES if ln["region"] == reg]
        us = [u["names"]["pt"] for u in B.UNIQUES if u["region"] == reg]
        if reg == "castelo":
            us.append(B.KING["names"]["pt"] + " (Rei)")
        out.append(f"| {B.REGION_NAMES[reg]} | {len(ls)}: {', '.join(ls) or '—'} | {', '.join(us) or '—'} |")
    out.append("")
    stats_by_id = {st["id"]: st["stats"] for ln in data["lines"] for st in ln["stages"]}
    for reg in B.REGION_ORDER:
        regl = [ln for ln in B.LINES if ln["region"] == reg]
        if not regl:
            continue
        out.append(f"## {B.REGION_NAMES[reg]}")
        out.append("")
        for ln in regl:
            names = " → ".join(st["pt"] for st in ln["stages"])
            out.append(f"### {names}")
            if ln.get("starter"):
                out.append(f"*Linha de **{ln['starter']}**, parceiro inicial.*")
            out.append("")
            out.append(f"- **Conceito:** {ln['concept']}")
            out.append(f"- **Silhueta:** {ln['silhouette']}")
            out.append(f"- **Arco de crescimento:** {ln['arc']}")
            out.append(f"- **Personalidade:** {ln['personality']}. **No mapa:** {B.BEHAVIOR_PT[ln['behavior']]}.")
            out.append(f"- **Tipo:** {B.TYPE_PT[ln['type']]} · **Raridade:** {ln['rarity']} · "
                       f"**Cresce aos** {ln['growth'][0]} e {ln['growth'][1]} anos")
            sg = ln["signature"]
            out.append(f"- **Golpe assinatura:** {sg['pt']} / {sg['en']} / {sg['es']}")
            out.append("")
            out.append("| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |")
            out.append("|---|---|---|---|---|---|---|")
            for i, st in enumerate(ln["stages"], start=1):
                sid = f"{ln['id']}_{i}"
                tot = sum(stats_by_id[sid].values())
                label = ["Bebê", "Adolescente", "Adulto"][i - 1]
                out.append(f"| {num[sid]:03d} | {label} | {st['pt']} | {st['en']} | {st['es']} | {tot} | {st['entry']['pt']} |")
            out.append("")
    out.append("## Únicos e Rei")
    out.append("")
    out.append("Não crescem. Aparecem uma vez por região (a partir do Bosque) e no Castelo.")
    out.append("")
    for u in B.UNIQUES + [B.KING]:
        n = 80 if u is B.KING else num[u["id"]]
        out.append(f"### {n:03d} · {u['names']['pt']} / {u['names']['en']} / {u['names']['es']}")
        out.append(f"- **Conceito:** {u['concept']}")
        out.append(f"- **Silhueta:** {u['silhouette']}")
        out.append(f"- **Personalidade:** {u['personality']}. **No mapa:** {B.BEHAVIOR_PT[u['behavior']]}.")
        out.append(f"- **Tipo:** {B.TYPE_PT[u['type']]} · **Região:** {B.REGION_NAMES[u['region']]}")
        out.append(f"- **Ossário:** {u['entry']['pt']}")
        out.append("")
    (ROOT / "docs/BESTIARIO.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    build()
