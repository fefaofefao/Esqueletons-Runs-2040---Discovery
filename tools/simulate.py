#!/usr/bin/env python3
"""Roda o simulador de balanceamento (tools/sim/simulate.gd, motor real em
Godot headless), confere os critérios da seção 11 do AGENTS.md e gera
docs/BALANCEAMENTO.md.

Uso: python3 tools/simulate.py [--runs 40] [--trials 10] [--check]
  --check  sai com código 1 se algum critério falhar
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAMES = {"prologo": "Prólogo", "bosque": "Bosque", "minas": "Minas", "pantano": "Pântano", "ossorio": "Ossório",
         "picos": "Picos", "deserto": "Deserto", "castelo": "Castelo"}
TYPES = {"fisico": "Físico", "magico": "Mágico", "cura": "Cura/Suporte", "veneno": "Veneno"}

# Histórico dos ajustes feitos com o simulador (fase 3c). Acrescente a cada rodada.
ADJUSTMENTS = [
    ("XP por inimigo", "base_xp por estágio 50/110/180 e divisor 5 faziam a idade disparar (Bosque aos 44 anos).",
     "base_xp achatado (60/68/68) e `xp.reward_div` = 18: a recompensa cresce na mesma proporção da curva (n−1)^2,2."),
    ("Faixa de idade dos selvagens", "Selvagens de até 18 anos no Bosque (já adolescentes) derrotavam o time de 10 anos.",
     "Selvagens começam na idade de chegada e vão até +5; domadores +2 acima disso."),
    ("Golpes de veneno", "Todos eram mágicos: Veneno batia na RES alta dos magos e ainda tinha desvantagem de tipo (Mágico vencia 97%).",
     "Picada, Cuspe Ácido, Chuva de Espinhos e Ferrão das Dunas passaram a ser físicos."),
    ("Ordem de aprendizado", "A rotação dos golpes deixava o Físico com golpes fracos nas idades em que o Mágico já tinha os médios.",
     "Escadas de poder iguais entre os tipos; a variedade vem do tipo secundário e da assinatura."),
    ("Perfis de atributo", "3 das 6 linhas físicas são tanques lentos; as duas linhas velozes eram mágicas.",
     "Tanque: ATQ 1,25 e VEL 0,85; mago: MAG 1,15; veloz: VEL 1,25; Escultor passou a astuto."),
    ("Vantagem de tipo", "×1,5 / ×0,75 criava duelos decididos só pelo tipo.", "×1,35 / ×0,8."),
    ("Cura/Suporte", "Sem dano próprio, as linhas de cura só perdiam duelos.",
     "Jato Fresco (drena) e Badalada Serena (atinge todos) viraram golpes de dano; as linhas de cura aprendem ataques do tipo secundário."),
    ("Taro × Lia", "Com a mesma equipe, Lia vencia ~100% dos Guardiões e Taro 0–50%.",
     "Taro (Grumete) virou perfil tanque e ganhou Cura como secundário (como Lia); Remada Dupla 2×50, Facho do Farol 60."),
    ("Guardiões (protótipos)", "Bosque e Minas cheios de Veneno anulavam times físicos; os últimos Guardiões ficavam fáceis.",
     "Bosque com um de cada tipo (o Pântano continua temático de Veneno); Ossório +4 anos, Deserto +5, Pântano +2; Rei com uma escolta de suporte."),
]


def find_godot():
    for c in [os.environ.get("GODOT"), shutil.which("godot"), str(Path.home() / ".local/bin/godot")]:
        if c and Path(c).exists():
            return c
    sys.exit("godot não encontrado (defina GODOT)")


def run_sim(runs, trials):
    out = Path(tempfile.gettempdir()) / "esq_sim.json"
    godot = find_godot()
    subprocess.run([godot, "--headless", "--import"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    r = subprocess.run([godot, "--headless", "res://tools/sim/simulate.tscn", "--", f"--runs={runs}", f"--trials={trials}", f"--out={out}"],
                       cwd=ROOT, capture_output=True, text=True, timeout=1800)
    if "SCRIPT ERROR" in r.stdout + r.stderr or not out.exists():
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit("simulação falhou")
    return json.loads(out.read_text())


def check(d, bal):
    t = bal["targets"]
    lo, hi = t["guardian_winrate"]
    fails = []
    for r in d["regions"]:
        if r["guardian_target"] and not lo <= r["winrate"] <= hi:
            fails.append(f"{NAMES[r['id']]}: vitória contra o Guardião {r['winrate']:.0%} fora de {lo:.0%}–{hi:.0%}")
        if r["boss_winrate"] >= 0 and not lo <= r["boss_winrate"] <= hi:
            fails.append(f"Rei: vitória {r['boss_winrate']:.0%} fora de {lo:.0%}–{hi:.0%}")
    total = sum(r["minutes"] for r in d["regions"])
    if not t["total_minutes"][0] <= total <= t["total_minutes"][1]:
        fails.append(f"tempo total {total:.0f} min fora de {t['total_minutes']}")
    top = max(d["move_usage"].items(), key=lambda x: x[1])
    if top[1] > t["max_move_usage"]:
        fails.append(f"golpe dominante: {top[0]} com {top[1]:.0%} de uso")
    ty = d["types"]
    for k, v in ty.items():
        others = [x for kk, x in ty.items() if kk != k]
        if v - sum(others) / len(others) > t["max_type_gap"]:
            fails.append(f"tipo {TYPES[k]} {v - sum(others) / len(others):+.0%} acima da média dos outros")
    # sem grind: a idade esperada no Guardião é atingida só seguindo a rota (tolerância de 3 anos)
    for r in d["regions"]:
        if r["guardian_target"] and r["guardian_age"] < r["guardian_target"] - 3:
            fails.append(f"{NAMES[r['id']]}: idade {r['guardian_age']:.1f} abaixo da meta {r['guardian_target']} (exigiria grind)")
    return fails, total


def write_doc(d, bal, fails, total):
    moves = {m["id"]: m for m in json.loads((ROOT / "data/moves.json").read_text())["moves"]}
    L = ["# Balanceamento", "",
         "Gerado por `tools/simulate.py` (simulador `tools/sim/simulate.gd`, que usa o motor e a IA reais da batalha e os dados reais). "
         "Metas em `data/balance.json`; regras em `data/battle.json`. Repita a simulação ao fim de cada tarefa das fases 3c e 4.", "",
         f"**{d['runs']} jogadas simuladas** (metade com Taro, metade com Lia), {d['trials']} tentativas por Guardião em cada jogada.", ""]
    L.append("## Critérios de aceite")
    L.append("")
    if fails:
        L += [f"- ❌ {f}" for f in fails]
    else:
        L.append("- ✅ Todos os critérios da seção 11 foram atendidos.")
    L.append("")
    L.append("## Por região")
    L.append("")
    L.append("| Região | Chegada (meta) | Idade no Guardião (meta) | Vitória contra o Guardião | Taro / Lia | Batalhas | Derrotas | Tempo (min) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in d["regions"]:
        bs = r.get("by_starter", {})
        def pct(k):
            v = bs.get(k)
            return f"{v[0] / v[1]:.0%}" if v and v[1] else "—"
        win = f"{r['winrate']:.0%}" if r["guardian_target"] else "—"
        if r["boss_winrate"] >= 0:
            win += f" · Rei {r['boss_winrate']:.0%}"
        tgt = r["arrive_target"]
        L.append(f"| {NAMES[r['id']]} | {r['arrive_age']:.1f} ({tgt[0]:.0f}–{tgt[1]:.0f}) | "
                 f"{r['guardian_age']:.1f} ({r['guardian_target'] or '—'}) | {win} | {pct('grumete')} / {pct('faroleira')} | "
                 f"{r['battles']:.0f} | {r['lost']:.1f} | {r['minutes']:.1f} |")
    L.append(f"| **Total** | | | | | | | **{total:.0f} min ({int(total // 60)}h{int(total % 60):02d})** |")
    L.append("")
    tm = bal["time"]
    L.append(f"Tempo = batalhas × duração simulada (ação do jogador {tm['seconds_per_player_action']} s, do inimigo {tm['seconds_per_enemy_action']} s, "
             f"+{tm['battle_overhead_seconds']} s de abertura/fim) + caminhada + leitura a {tm['reading_wpm']} palavras/min. "
             "Caminhada e leitura são o **orçamento** de cada região para a fase 4 (mapas e roteiro ainda não existem); "
             "a fase 4 deve medir os valores reais e repetir a simulação.")
    L.append("")
    L.append("## Tipos (duelos 2×2 na mesma idade: 20, 50 e 80 anos)")
    L.append("")
    L.append("| Tipo | Vitória geral | vs Físico | vs Mágico | vs Cura | vs Veneno |")
    L.append("|---|---|---|---|---|---|")
    for t in ["fisico", "magico", "cura", "veneno"]:
        row = [f"{d['type_pairs'].get(f'{t}>{o}', 0):.0%}" if o != t else "—" for o in ["fisico", "magico", "cura", "veneno"]]
        L.append(f"| {TYPES[t]} | {d['types'][t]:.0%} | " + " | ".join(row) + " |")
    L.append("")
    L.append("Ciclo de vantagem: Físico > Mágico > Veneno > Físico; Cura é neutra (vale ×1,35 / ×0,8). "
             "Cura perde duelos de dano por definição: é tipo de suporte e brilha em equipe mista.")
    L.append("")
    L.append("## Golpes mais usados pelo jogador")
    L.append("")
    L.append("| Golpe | Uso |")
    L.append("|---|---|")
    for k, v in sorted(d["move_usage"].items(), key=lambda x: -x[1])[:10]:
        L.append(f"| {k} ({moves[k]['type']}, {moves[k]['weight']}) | {v:.1%} |")
    L.append("")
    L.append(f"Limite: nenhum golpe acima de {bal['targets']['max_move_usage']:.0%}.")
    L.append("")
    L.append("## Modelo da jogada típica")
    L.append("- Enfrenta ~70% dos selvagens que cruzam a rota (`wild_crossings`) e todos os domadores (`tamers`); 30% dos encontros têm 2 selvagens.")
    L.append("- Equipe recrutada mais provável por região (`team` em `balance.json`); quem entra no time chega com a idade dos selvagens da região.")
    L.append("- IA do jogador: melhor dano esperado, cura abaixo de 35% de PV, valor por tempo (peso do golpe). Selvagens erram 25% das vezes.")
    L.append("- Após cada batalha a equipe é curada (poções/Rancho), os crescimentos acontecem e golpes novos substituem o de menor poder.")
    L.append("- Guardiões: protótipos com linhas da região na idade-meta, até a fase 4 definir as equipes do roteiro.")
    L.append("")
    L.append("## O que foi ajustado")
    L.append("")
    L.append("| Assunto | Problema encontrado | Ajuste |")
    L.append("|---|---|---|")
    for a, b, c in ADJUSTMENTS:
        L.append(f"| {a} | {b} | {c} |")
    L.append("")
    (ROOT / "docs/BALANCEAMENTO.md").write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=40)
    ap.add_argument("--trials", type=int, default=10)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    bal = json.loads((ROOT / "data/balance.json").read_text())
    d = run_sim(a.runs, a.trials)
    fails, total = check(d, bal)
    write_doc(d, bal, fails, total)
    print(f"simulate: {total:.0f} min; {len(fails)} critério(s) falhando -> docs/BALANCEAMENTO.md")
    for f in fails:
        print("  -", f)
    if a.check and fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
