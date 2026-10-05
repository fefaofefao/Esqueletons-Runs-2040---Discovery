"""Golpes (fase 3c) — fonte única de data/moves.json, i18n/moves.csv e learnsets.

56 golpes: 16 Físicos, 16 Mágicos, 12 de Cura/Suporte e 12 de Veneno. As 24
assinaturas de linha estão entre eles (a linha aprende a sua ao crescer para o
estágio 2). Cada golpe tem peso (leve/normal/pesado): golpes leves devolvem o
turno mais cedo, pesados batem mais forte, mas demoram a voltar (timeline).

Efeitos suportados pelo motor:
  poison {chance}            envenena o alvo
  stat   {stat, stages, on}  muda atributo (on: "target" ou "self")
  heal   {percent}           cura % do PV do alvo
  cure                       tira o veneno
  delay  {amount}            empurra o próximo turno do alvo (fração de um turno)
  drain  {percent}           o usuário recupera % do dano causado
Campo "hits": golpes de 2 acertos (cada um com o poder indicado).

A descrição (3 idiomas) é montada a partir dos efeitos, então sempre bate com
o que o golpe faz. Golpes sem efeito têm uma frase curta própria ("flavor").
"""

P, M, S = "physical", "magical", "status"
E, AE, SELF, AL, AA = "enemy", "all_enemies", "self", "ally", "all_allies"
LIGHT, NORMAL, HEAVY = "light", "normal", "heavy"


def mv(id, pt, en, es, type, cat, power, acc, pp, target, weight, effects=(), hits=1, flavor=None, sig=None):
    return {"id": id, "names": {"pt": pt, "en": en, "es": es}, "type": type, "category": cat, "power": power,
            "accuracy": acc, "pp": pp, "target": target, "weight": weight, "effects": list(effects), "hits": hits,
            "flavor": flavor, "signature_of": sig}


def poison(ch):
    return {"kind": "poison", "chance": ch}


def stat(s, n, ch=100, on="target"):
    return {"kind": "stat", "stat": s, "stages": n, "chance": ch, "on": on}


def heal(p):
    return {"kind": "heal", "percent": p}


def delay(a, ch=100):
    return {"kind": "delay", "amount": a, "chance": ch}


def drain(p):
    return {"kind": "drain", "percent": p}


CURE = {"kind": "cure"}

F, Mg, C, V = "fisico", "magico", "cura", "veneno"

MOVES = [
    # ---------------------------------------------------------------- FÍSICOS (16)
    mv("empurrao", "Empurrão", "Shove", "Empujón", F, P, 30, 100, 30, E, LIGHT,
       flavor=("Rápido e simples.", "Quick and simple.", "Rápido y simple.")),
    mv("cabecada", "Cabeçada", "Headbutt", "Cabezazo", F, P, 45, 100, 25, E, NORMAL,
       flavor=("Crânio contra crânio.", "Skull against skull.", "Cráneo contra cráneo.")),
    mv("chute_na_canela", "Chute na Canela", "Shin Kick", "Patada al Tobillo", F, P, 40, 100, 25, E, NORMAL, [stat("spd", -1, 30)]),
    mv("passo_ligeiro", "Passo Ligeiro", "Nimble Step", "Paso Veloz", F, P, 35, 100, 20, E, LIGHT, [stat("spd", 1, 100, "self")]),
    mv("osso_bumerangue", "Osso Bumerangue", "Bone Boomerang", "Hueso Bumerán", F, P, 30, 95, 20, E, NORMAL, hits=2),
    mv("ranger_os_dentes", "Ranger os Dentes", "Grit Teeth", "Apretar Dientes", F, S, 0, 100, 15, SELF, LIGHT,
       [stat("atk", 1), stat("def", 1)]),
    mv("quebra_costela", "Quebra-Costela", "Rib Cracker", "Rompecostillas", F, P, 60, 90, 15, E, NORMAL, [stat("def", -1, 40)]),
    mv("rodopio", "Rodopio", "Whirl", "Remolino", F, P, 45, 95, 15, AE, NORMAL,
       flavor=("Gira e acerta todos.", "Spins into everyone.", "Gira y golpea a todos.")),
    mv("investida", "Investida", "Charge", "Embestida", F, P, 75, 95, 15, E, HEAVY, [delay(0.25)]),
    mv("soco_seco", "Soco Seco", "Dry Punch", "Puño Seco", F, P, 95, 90, 10, E, HEAVY,
       flavor=("Lento e brutal.", "Slow and brutal.", "Lento y brutal.")),
    mv("remada_dupla", "Remada Dupla", "Double Stroke", "Remada Doble", F, P, 50, 95, 15, E, NORMAL, hits=2, sig="grumete"),
    mv("golpe_de_tora", "Golpe de Tora", "Log Slam", "Golpe de Tronco", F, P, 100, 90, 10, E, HEAVY, [delay(0.3)], sig="lenhador"),
    mv("desmoronar", "Desmoronar", "Cave-In", "Derrumbe", F, P, 65, 95, 10, AE, HEAVY, [stat("spd", -1, 30)], sig="mineiro"),
    mv("estaca_firme", "Estaca Firme", "Pile Driver", "Estaca Certera", F, P, 75, 95, 15, E, NORMAL, [stat("def", 1, 50, "self")], sig="palafiteiro"),
    mv("muralha_viva", "Muralha Viva", "Living Wall", "Muralla Viva", F, S, 0, 100, 10, SELF, NORMAL,
       [stat("def", 2), stat("res", 1)], sig="sentinela"),
    mv("avalanche_de_carga", "Avalanche de Carga", "Cargo Avalanche", "Alud de Carga", F, P, 110, 90, 5, E, HEAVY,
       [delay(0.4), stat("spd", -1, 100, "self")], sig="carregador"),
    # ---------------------------------------------------------------- MÁGICOS (16)
    mv("faisca_ossea", "Faísca Óssea", "Bone Spark", "Chispa Ósea", Mg, M, 35, 100, 30, E, LIGHT,
       flavor=("Um estalo de magia.", "A snap of magic.", "Un chasquido mágico.")),
    mv("clarao", "Clarão", "Flare", "Destello", Mg, M, 45, 100, 25, E, NORMAL, [stat("res", -1, 30)]),
    mv("eco_sombrio", "Eco Sombrio", "Dark Echo", "Eco Sombrío", Mg, M, 55, 100, 20, E, NORMAL,
       flavor=("Ressoa nos ossos.", "Rattles the bones.", "Resuena en los huesos.")),
    mv("concentrar", "Concentrar", "Focus", "Concentrarse", Mg, S, 0, 100, 15, SELF, LIGHT, [stat("mag", 2)]),
    mv("ventania", "Ventania", "Gale", "Vendaval", Mg, M, 35, 95, 15, AE, LIGHT, [delay(0.15)]),
    mv("chama_fria", "Chama Fria", "Cold Flame", "Llama Fría", Mg, M, 60, 95, 15, E, NORMAL, [stat("atk", -1, 30)]),
    mv("chuva_de_brasas", "Chuva de Brasas", "Ember Rain", "Lluvia de Brasas", Mg, M, 50, 90, 10, AE, NORMAL,
       flavor=("Brasas em todos.", "Embers on all foes.", "Brasas sobre todos.")),
    mv("ancora_do_tempo", "Âncora do Tempo", "Time Anchor", "Ancla del Tiempo", Mg, S, 0, 90, 10, E, LIGHT, [delay(0.6)]),
    mv("raio_lunar", "Raio Lunar", "Moonbeam", "Rayo Lunar", Mg, M, 85, 90, 10, E, HEAVY,
       flavor=("Luz fria e pesada.", "Cold, heavy light.", "Luz fría y pesada.")),
    mv("explosao_arcana", "Explosão Arcana", "Arcane Burst", "Estallido Arcano", Mg, M, 115, 85, 5, E, HEAVY,
       [stat("mag", -1, 100, "self")]),
    mv("facho_do_farol", "Facho do Farol", "Beacon Beam", "Haz del Faro", Mg, M, 60, 100, 15, E, NORMAL, [stat("res", -1, 30)], sig="faroleira"),
    mv("melodia_vagalume", "Melodia Vaga-lume", "Firefly Tune", "Melodía Luciérnaga", Mg, M, 45, 100, 15, AE, LIGHT, sig="flautista",
       flavor=("Luz dançante.", "Dancing light.", "Luz danzante.")),
    mv("martelo_de_brasa", "Martelo de Brasa", "Ember Hammer", "Martillo de Brasa", Mg, M, 90, 90, 10, E, HEAVY, [stat("def", -1, 30)], sig="ferreiro"),
    mv("decreto_selado", "Decreto Selado", "Sealed Decree", "Decreto Sellado", Mg, M, 60, 95, 10, E, NORMAL, [delay(0.35)], sig="escriba"),
    mv("estatua_de_gelo", "Estátua de Gelo", "Ice Statue", "Estatua de Hielo", Mg, M, 75, 90, 10, E, NORMAL, [stat("spd", -1, 50)], sig="escultor"),
    mv("rota_dos_ecos", "Rota dos Ecos", "Echo Route", "Ruta de Ecos", Mg, M, 55, 100, 15, E, LIGHT, [stat("spd", 1, 100, "self")], sig="cartografo"),
    # ---------------------------------------------------------------- CURA / SUPORTE (12)
    mv("remendo", "Remendo", "Patch Up", "Parche", C, S, 0, 100, 15, SELF, NORMAL, [heal(35)]),
    mv("curativo", "Curativo", "Bandage", "Vendaje", C, S, 0, 100, 10, AL, NORMAL, [heal(40)]),
    mv("balsamo", "Bálsamo", "Balm", "Ungüento", C, S, 0, 100, 8, AA, HEAVY, [heal(25)]),
    mv("limpeza", "Limpeza", "Cleanse", "Purga", C, S, 0, 100, 10, AA, LIGHT, [CURE]),
    mv("encorajar", "Encorajar", "Cheer", "Animar", C, S, 0, 100, 15, AL, LIGHT, [stat("atk", 1), stat("mag", 1)]),
    mv("remendo_de_rede", "Remendo de Rede", "Net Mend", "Remiendo de Red", C, S, 0, 100, 10, AL, NORMAL, [heal(40), stat("def", 1)], sig="rendeira"),
    mv("seiva_viva", "Seiva Viva", "Living Sap", "Savia Viva", C, S, 0, 100, 10, AA, NORMAL, [heal(25)], sig="herborista"),
    mv("jato_fresco", "Jato Fresco", "Cool Spray", "Chorro Fresco", C, M, 55, 100, 15, E, NORMAL, [drain(50)], sig="aguadeiro"),
    mv("orvalho_de_lirio", "Orvalho de Lírio", "Lily Dew", "Rocío de Lirio", C, S, 0, 100, 10, SELF, NORMAL, [heal(45), stat("res", 1)], sig="jardineiro_lirios"),
    mv("badalada_serena", "Badalada Serena", "Serene Toll", "Campanada Serena", C, M, 45, 100, 10, AE, NORMAL, [delay(0.15)], sig="sineiro"),
    mv("cha_de_abrigo", "Chá de Abrigo", "Shelter Tea", "Té de Refugio", C, S, 0, 100, 8, AA, HEAVY, [heal(35)], sig="chazeiro"),
    mv("ritmo_da_caravana", "Ritmo da Caravana", "Caravan Rhythm", "Ritmo de Caravana", C, S, 0, 100, 10, AA, NORMAL, [stat("spd", 1)], sig="tamborileiro"),
    # ---------------------------------------------------------------- VENENO (12)
    mv("picada", "Picada", "Prick", "Pinchazo", V, P, 30, 100, 30, E, LIGHT, [poison(30)]),
    mv("lodo", "Lodo", "Sludge", "Lodo", V, M, 45, 100, 20, E, NORMAL, [poison(30)]),
    mv("bafo_azedo", "Bafo Azedo", "Sour Breath", "Aliento Agrio", V, S, 0, 90, 15, E, NORMAL, [poison(100)]),
    mv("neblina_verde", "Neblina Verde", "Green Mist", "Neblina Verde", V, M, 30, 95, 15, AE, NORMAL, [poison(20)]),
    mv("cuspe_acido", "Cuspe Ácido", "Acid Spit", "Escupitajo Ácido", V, P, 55, 95, 15, E, NORMAL, [stat("res", -1, 40)]),
    mv("dreno_toxico", "Dreno Tóxico", "Toxic Drain", "Drenaje Tóxico", V, M, 55, 100, 10, E, NORMAL, [drain(50)]),
    mv("toxina_lenta", "Toxina Lenta", "Slow Toxin", "Toxina Lenta", V, S, 0, 85, 10, E, NORMAL, [poison(100), delay(0.3)]),
    mv("chuva_de_espinhos", "Chuva de Espinhos", "Spine Shower", "Lluvia de Púas", V, P, 40, 95, 10, AE, NORMAL, [poison(25)], sig="marisqueiro"),
    mv("nuvem_de_esporos", "Nuvem de Esporos", "Spore Cloud", "Nube de Esporas", V, S, 0, 85, 10, AE, HEAVY, [poison(70)], sig="cogumeleiro"),
    mv("vazamento", "Vazamento", "Gas Leak", "Fuga de Gas", V, M, 65, 95, 10, E, NORMAL, [poison(40)], sig="gasista"),
    mv("anil_toxico", "Anil Tóxico", "Toxic Bluing", "Añil Tóxico", V, M, 70, 95, 10, E, NORMAL, [poison(35), stat("res", -1)], sig="lavadeira"),
    mv("ferrao_das_dunas", "Ferrão das Dunas", "Dune Sting", "Aguijón de Dunas", V, P, 60, 100, 15, E, LIGHT, [poison(50)], sig="domador_escorpioes"),
]

BY_ID = {m["id"]: m for m in MOVES}

# ------------------------------------------------------------------ descrições
STAT_NAMES = {"pt": {"atk": "ATQ", "mag": "MAG", "def": "DEF", "res": "RES", "spd": "VEL"},
              "en": {"atk": "ATK", "mag": "MAG", "def": "DEF", "res": "RES", "spd": "SPD"},
              "es": {"atk": "ATQ", "mag": "MAG", "def": "DEF", "res": "RES", "spd": "VEL"}}
TXT = {
    "pt": {"poison": "envenena", "delay": "atrasa", "delay_big": "atrasa muito", "heal": "cura {p}%",
           "cure": "tira veneno", "drain": "drena {p}% do dano", "hits": "acerta 2 vezes", "self": "sua ", "and_poison": " e o veneno"},
    "en": {"poison": "poisons", "delay": "delays", "delay_big": "big delay", "heal": "heals {p}%",
           "cure": "cures poison", "drain": "drains {p}% dealt", "hits": "hits twice", "self": "your ", "and_poison": ", cures poison"},
    "es": {"poison": "envenena", "delay": "retrasa", "delay_big": "retrasa mucho", "heal": "cura {p}%",
           "cure": "quita veneno", "drain": "drena {p}% del daño", "hits": "golpea 2 veces", "self": "tu ", "and_poison": " y el veneno"},
}


def describe(m, lang):
    t = TXT[lang]
    parts = []
    if m["hits"] > 1:
        parts.append(t["hits"])
    stats = {}
    for e in m["effects"]:
        k = e["kind"]
        ch = e.get("chance", 100)
        tail = f" ({ch}%)" if ch < 100 else ""
        if k == "poison":
            parts.append(t["poison"] + tail)
        elif k == "delay":
            parts.append((t["delay_big"] if e["amount"] >= 0.5 else t["delay"]) + tail)
        elif k == "heal":
            parts.append(t["heal"].format(p=e["percent"]))
        elif k == "cure":
            parts.append(t["cure"])
        elif k == "drain":
            parts.append(t["drain"].format(p=e["percent"]))
        elif k == "stat":
            stats.setdefault((e["stages"], ch, e.get("on", "target")), []).append(STAT_NAMES[lang][e["stat"]])
    for (n, ch, on), names in stats.items():
        arrows = ("↑" if n > 0 else "↓") * min(2, abs(n))
        own_target = m["target"] in (SELF, AL, AA)
        pre = t["self"] if on == "self" and not own_target else ""
        parts.append(pre + " ".join(nm + arrows for nm in names) + (f" ({ch}%)" if ch < 100 else ""))
    # "cura 25%" + "tira veneno" -> "cura 25% e o veneno" (cabe na faixa)
    heals = [p for p in parts if p.startswith(t["heal"].split(" ")[0] + " ")]
    if heals and t["cure"] in parts:
        parts.remove(t["cure"])
        parts[parts.index(heals[0])] = heals[0] + t["and_poison"]
    if not parts:
        i = {"pt": 0, "en": 1, "es": 2}[lang]
        return m["flavor"][i]
    out = ", ".join(parts)
    return out[0].upper() + out[1:] + "."


def key(mid):
    return "MOVE_" + mid.upper()


def to_json():
    out = []
    for m in MOVES:
        d = {"id": m["id"], "name_key": key(m["id"]), "desc_key": key(m["id"]) + "_DESC", "type": m["type"],
             "category": m["category"], "power": m["power"], "accuracy": m["accuracy"], "pp": m["pp"],
             "target": m["target"], "weight": m["weight"], "effects": m["effects"]}
        if m["hits"] > 1:
            d["hits"] = m["hits"]
        if m["signature_of"]:
            d["signature_of"] = m["signature_of"]
        out.append(d)
    return {"moves": out}


def csv_rows():
    rows = []
    for m in MOVES:
        rows.append([key(m["id"]), m["names"]["pt"], m["names"]["en"], m["names"]["es"]])
        rows.append([key(m["id"]) + "_DESC", describe(m, "pt"), describe(m, "en"), describe(m, "es")])
    return rows


# ------------------------------------------------------------------ learnsets
# Ordem de aprendizado por tipo (do mais fraco ao mais forte).
POOL = {
    "fisico": ["empurrao", "cabecada", "osso_bumerangue", "chute_na_canela", "ranger_os_dentes", "quebra_costela",
               "investida", "rodopio", "passo_ligeiro", "soco_seco"],
    "magico": ["faisca_ossea", "clarao", "eco_sombrio", "ventania", "concentrar", "chama_fria",
               "raio_lunar", "chuva_de_brasas", "ancora_do_tempo", "explosao_arcana"],
    "cura": ["remendo", "curativo", "limpeza", "encorajar", "balsamo"],
    "veneno": ["picada", "lodo", "cuspe_acido", "neblina_verde", "bafo_azedo", "dreno_toxico", "toxina_lenta"],
}
# Tipo secundário de cada linha (cobertura) — dá variedade dentro do mesmo tipo.
SECONDARY = {
    "grumete": "cura", "faroleira": "cura", "marisqueiro": "fisico", "rendeira": "magico",
    "lenhador": "veneno", "herborista": "veneno", "cogumeleiro": "magico", "flautista": "fisico",
    "mineiro": "magico", "ferreiro": "fisico", "gasista": "fisico", "aguadeiro": "fisico",
    "lavadeira": "cura", "palafiteiro": "veneno", "jardineiro_lirios": "magico",
    "sentinela": "cura", "escriba": "veneno", "sineiro": "fisico",
    "carregador": "magico", "escultor": "cura", "chazeiro": "magico",
    "domador_escorpioes": "fisico", "cartografo": "veneno", "tamborileiro": "fisico",
}


def _rot(lst, n):
    n %= max(1, len(lst))
    return lst[n:] + lst[:n]


def line_moves(ln, index):
    """Lista ordenada de (idade, golpe) da linha inteira (os 3 estágios)."""
    t, sec = ln["type"], SECONDARY[ln["id"]]
    own = POOL[t][:]
    # variação entre linhas do mesmo tipo: os golpes do meio mudam de ordem
    # escadas de poder iguais entre os tipos (a variedade vem do secundário e da assinatura)
    atk = sorted([m for m in POOL[sec] if BY_ID[m]["power"] > 0], key=lambda m: BY_ID[m]["power"] * BY_ID[m]["hits"])
    if not atk:  # secundário de suporte: cura e reforço em vez de ataque
        atk = POOL[sec][:]
    other = [atk[0], atk[min(len(atk) - 1, 1 + index % 2)], atk[min(len(atk) - 1, 3 + index % 2)], atk[-1]]
    g1, g2 = ln["growth"]
    if t == "cura":
        # suporte: precisa de um golpe de dano cedo (do tipo secundário)
        seq = [(1, other[0]), (1, own[0]), (5, own[1]), (9, other[1]), (g1 - 4, own[2]),
               (g1 + 6, other[2]), (g1 + 14, own[3]), (g2 + 4, other[3]), (g2 + 10, own[4])]
    else:
        o = lambda i: own[i] if i < len(own) else None  # noqa: E731
        seq = [(1, own[0]), (1, other[0]), (5, own[1]), (9, own[2]), (g1 - 3, own[3]), (g1 + 5, other[1]),
               (g1 + 12, own[4]), (g2 - 4, o(5)), (g2 + 4, o(6)), (g2 + 12, o(7)), (g2 + 20, own[-1])]
    seen = set()
    out = []
    for age, mid in seq:
        if mid is None or mid in seen:
            continue
        seen.add(mid)
        out.append([max(1, min(100, age)), mid])
    out.append([g1, ln["signature"]["id"]])
    out.sort(key=lambda x: x[0])
    return out


def _index(ln):
    import bestiary as B
    same = [x["id"] for x in B.LINES if x["type"] == ln["type"]]
    return same.index(ln["id"])


def learnset(ln, stage):
    full = line_moves(ln, _index(ln))
    if stage == 1:
        # o bebê não aprende a assinatura (ela vem ao crescer)
        return [e for e in full if e[1] != ln["signature"]["id"]]
    return full


def growth_move(ln, stage):
    if stage == 2:
        return ln["signature"]["id"]
    if stage == 3:
        return POOL[ln["type"]][-1]
    return ""


UNIQUE_SETS = {
    "raizerno": ["remendo", "investida", "balsamo", "quebra_costela", "encorajar"],
    "vagonauta": ["passo_ligeiro", "investida", "rodopio", "soco_seco", "osso_bumerangue"],
    "brumaga": ["neblina_verde", "toxina_lenta", "dreno_toxico", "eco_sombrio", "cuspe_acido"],
    "bufardo": ["ancora_do_tempo", "chuva_de_brasas", "cuspe_acido", "raio_lunar", "ventania"],
    "nevasco": ["balsamo", "limpeza", "chama_fria", "curativo", "encorajar"],
    "ampulhor": ["ancora_do_tempo", "raio_lunar", "eco_sombrio", "explosao_arcana", "concentrar"],
    "degustor": ["bafo_azedo", "toxina_lenta", "dreno_toxico", "soco_seco", "lodo"],
    "rei_esqueleto": ["explosao_arcana", "ancora_do_tempo", "chuva_de_brasas", "dreno_toxico", "raio_lunar", "concentrar"],
}


def learnset_unique(u):
    return [[1, m] for m in UNIQUE_SETS[u["id"]]]
