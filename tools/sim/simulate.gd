extends Node
## Simulador de balanceamento (seção 11 do AGENTS.md), headless, com o motor e a
## IA reais da batalha e os dados reais (species.json, moves.json, battle.json,
## balance.json).
##
## Jogada típica por região: o jogador enfrenta ~70% dos selvagens que cruzam a
## rota e todos os domadores do caminho, com a equipe recrutada mais provável
## (balance.json "team"; "@starter" alterna Grumete/Faroleira entre as rodadas).
## A IA do jogador é a simples (melhor dano esperado, cura abaixo de 35% de PV),
## sem erros aleatórios; os selvagens erram 25% das vezes, como no jogo. Após
## cada batalha a equipe é curada (poções/Rancho) e os crescimentos acontecem.
## Ao chegar ao Guardião, a equipe daquele momento enfrenta-o N vezes (taxa de
## vitória) e segue em frente.
##
## Uso: godot --headless res://tools/sim/simulate.tscn -- --runs=40 --out=/caminho/sim.json

var rules: Dictionary
var bal: Dictionary
var rng := RandomNumberGenerator.new()
var move_usage := {}
var move_total := 0


func _ready() -> void:
	var runs := 40
	var trials := 10
	var out := "user://sim.json"
	var seed := 2040
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--runs="):
			runs = int(a.substr(7))
		elif a.begins_with("--trials="):
			trials = int(a.substr(9))
		elif a.begins_with("--out="):
			out = a.substr(6)
		elif a.begins_with("--seed="):
			seed = int(a.substr(7))
	rng.seed = seed
	rules = Data.battle_rules()
	bal = Data.load_json("res://data/balance.json")
	var regions: Array = bal["regions"]
	var acc := []
	for r in regions:
		acc.append({"id": r.id, "arrive_age": 0.0, "guardian_age": 0.0, "wins": 0, "trials": 0, "boss_wins": 0, "boss_trials": 0,
			"battles": 0, "lost": 0, "battle_seconds": 0.0, "guardian_seconds": 0.0, "by_starter": {}})
	for run in runs:
		var starter := "grumete" if run % 2 == 0 else "faroleira"
		_playthrough(starter, regions, acc, trials)
	var report := {"runs": runs, "trials": trials, "regions": [], "move_usage": {}, "types": _type_duels(), "time": bal["time"]}
	report["type_pairs"] = pair_rates
	for i in regions.size():
		var a: Dictionary = acc[i]
		var r: Dictionary = regions[i]
		var words := float(r.get("read_words", 0))
		var minutes: float = float(r.get("walk_minutes", 0)) + words / float(bal["time"]["reading_wpm"]) \
			+ (a.battle_seconds + a.guardian_seconds) / runs / 60.0
		report.regions.append({"id": r.id, "arrive_target": r.arrive, "guardian_target": r.guardian_age,
			"arrive_age": a.arrive_age / runs, "guardian_age": a.guardian_age / runs,
			"winrate": float(a.wins) / maxf(1, a.trials), "boss_winrate": float(a.boss_wins) / maxf(1, a.boss_trials) if a.boss_trials > 0 else -1.0,
			"battles": float(a.battles) / runs, "lost": float(a.lost) / runs, "minutes": minutes,
			"battle_minutes": a.battle_seconds / runs / 60.0, "by_starter": a.by_starter})
	for k in move_usage.keys():
		report.move_usage[k] = float(move_usage[k]) / maxf(1, move_total)
	var f := FileAccess.open(out, FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("simulação: ", runs, " jogadas -> ", out)
	get_tree().quit()


# ------------------------------------------------------------------ espécies
func species_at(line: String, age: int) -> String:
	if Data.species(line).size() > 0:
		return line  # único ou Rei
	var stages: Array = Data.line_stages(line)
	var gl: Array = Data.species(stages[0]).get("growth_levels", [100, 100])
	var st := 1 if age < int(gl[0]) else (2 if age < int(gl[1]) else 3)
	return stages[st - 1]


func make(line: String, age: int) -> Monster:
	return Monster.create(species_at(line, age), age)


# ------------------------------------------------------------------ jogada
func _playthrough(starter: String, regions: Array, acc: Array, trials: int) -> void:
	var owned := {}
	for i in regions.size():
		var r: Dictionary = regions[i]
		var a: Dictionary = acc[i]
		var party: Array = []
		for ln in r.team:
			var line := starter if ln == "@starter" else str(ln)
			if not owned.has(line):
				owned[line] = make(line, int(r.wild_age[0]) if i > 0 else int(r.arrive[0]))
			party.append(owned[line])
		a.arrive_age += _avg_age(party)
		var fights := int(round(float(r.wild_crossings) * 0.7))
		var plan := []
		for k in fights:
			plan.append("wild")
		for k in int(r.tamers):
			plan.insert(int(round(float(k + 1) * plan.size() / (int(r.tamers) + 1))), "tamer")
		for kind in plan:
			var enemies := []
			if kind == "wild":
				var n := 2 if rng.randf() < 0.3 else 1
				for k in n:
					enemies.append(make(_pick(r.wild_lines), rng.randi_range(int(r.wild_age[0]), int(r.wild_age[1]))))
			else:
				var n := rng.randi_range(2, 3)
				for k in n:
					enemies.append(make(_pick(r.wild_lines), rng.randi_range(int(r.tamer_age) - 2, int(r.tamer_age))))
			var res := _battle(party, enemies, kind, true)
			a.battles += 1
			a.battle_seconds += res.seconds
			if res.result != "win":
				a.lost += 1
			_after_battle(party)
		a.guardian_age += _avg_age(party)
		for key in ["guardian", "final_boss"]:
			var g: Array = r.get(key, [])
			if g.is_empty():
				continue
			var wins := 0
			for t in trials:
				var copy := party.map(func(m: Monster) -> Monster: return Monster.from_dict(m.to_dict()))
				var foes := []
				for e in g:
					foes.append(make(str(e[0]), int(e[1])))
				var res := _battle(copy, foes, "boss", t == 0)
				if res.result == "win":
					wins += 1
				if t == 0:
					a.guardian_seconds += res.seconds
			if key == "guardian":
				a.wins += wins
				a.trials += trials
				var bs: Dictionary = a.by_starter
				if not bs.has(starter):
					bs[starter] = [0, 0]
				bs[starter][0] += wins
				bs[starter][1] += trials
			else:
				a.boss_wins += wins
				a.boss_trials += trials
			# a vitória "de verdade" também dá XP (uma batalha completa)
			var foes2 := []
			for e in g:
				foes2.append(make(str(e[0]), int(e[1])))
			_battle(party, foes2, "boss", false)
			_after_battle(party)


func _pick(lines: Array) -> String:
	return str(lines[rng.randi() % lines.size()])


func _avg_age(party: Array) -> float:
	var t := 0.0
	for m in party:
		t += m.level
	return t / maxf(1, party.size())


func _after_battle(party: Array) -> void:
	for m in party:
		m.heal_full()
		while m.growth_target() != "":
			var r: Dictionary = m.grow()
			var gm := str(r.get("move", ""))
			if gm != "" and not m.knows(gm):
				_learn(m, gm)


## Golpe novo com 4 golpes: troca o de menor poder (golpes de status contam 40).
func _learn(m: Monster, move_id: String) -> void:
	if m.moves.size() < 4:
		m.moves.append({"id": move_id, "pp": int(Data.move(move_id).get("pp", 10))})
		return
	var worst := 0
	var worst_p := 9999.0
	for i in m.moves.size():
		var mv := Data.move(str(m.moves[i]["id"]))
		var p := float(mv.get("power", 0)) * int(mv.get("hits", 1)) if str(mv.get("category", "")) != "status" else 40.0
		if p < worst_p:
			worst_p = p
			worst = i
	BattleEngine.learn_move(m, move_id, worst)


func _battle(party: Array, enemies: Array, kind: String, count_usage: bool) -> Dictionary:
	var e := BattleEngine.new()
	e.setup(party, enemies, kind, rng.randi())
	e.bag = {}
	var player_actions := 0
	var enemy_actions := 0
	for step in 600:
		var actor := e.next_actor()
		if actor == null:
			break
		var action := BattleAI.choose(e, actor, actor.side == BattleEngine.ENEMY)
		if actor.side == BattleEngine.PLAYER:
			player_actions += 1
			if count_usage and str(action.get("kind", "")) == "move":
				var mid := str(action.move)
				move_usage[mid] = int(move_usage.get(mid, 0)) + 1
				move_total += 1
		else:
			enemy_actions += 1
		var evs := e.act(action)
		for ev in evs:
			if str(ev.get("t", "")) == "learn_prompt":
				var who := e.find(int(ev.target))
				if who:
					_learn(who, str(ev.move))
		for slot in e.pending_replacements():
			var res := e.reserves(BattleEngine.PLAYER)
			if not res.is_empty():
				e.switch_in(BattleEngine.PLAYER, slot, res[0])
		if e.result != "":
			break
	var t: Dictionary = bal["time"]
	var secs := player_actions * float(t.seconds_per_player_action) + enemy_actions * float(t.seconds_per_enemy_action) \
		+ float(t.battle_overhead_seconds)
	return {"result": e.result, "seconds": secs, "actions": player_actions + enemy_actions}


# ------------------------------------------------------------------ tipos
## Duelos 2×2 entre linhas de tipos diferentes, na mesma idade (20, 50 e 80
## anos): taxa de vitória de cada tipo contra os outros.
var pair_rates := {}


func _type_duels() -> Dictionary:
	var pairs := {}
	var by_type := {}
	var lines_by_type := {}
	var d = Data.load_json("res://data/species.json")
	for ln in d["lines"]:
		if not lines_by_type.has(ln.type):
			lines_by_type[ln.type] = []
		lines_by_type[ln.type].append(ln.id)
	var types: Array = lines_by_type.keys()
	for t in types:
		by_type[t] = [0, 0]
	for age in [20, 50, 80]:
		for a in types:
			for b in types:
				if a == b:
					continue
				for k in 60:
					var p := [make(_pick(lines_by_type[a]), age), make(_pick(lines_by_type[a]), age)]
					var q := [make(_pick(lines_by_type[b]), age), make(_pick(lines_by_type[b]), age)]
					var res := _battle(p, q, "tamer", false)
					by_type[a][1] += 1
					var pk: String = "%s>%s" % [a, b]
					pairs[pk] = int(pairs.get(pk, 0)) + (1 if res.result == "win" else 0)
					if res.result == "win":
						by_type[a][0] += 1
	var out := {}
	for t in types:
		out[t] = float(by_type[t][0]) / maxf(1, by_type[t][1])
	for k in pairs.keys():
		pair_rates[k] = float(pairs[k]) / 180.0
	return out
