class_name BattleAI
extends RefCounted
## IA simples (a mesma do simulador da fase 3c): cura abaixo de 35% de PV,
## senão o golpe com melhor dano esperado. Selvagens erram de propósito às vezes.


static func choose(engine: BattleEngine, m: Monster) -> Dictionary:
	var ai: Dictionary = engine.rules.get("ai", {})
	var moves := engine.usable_moves(m)
	if engine.is_wild() and engine.rng.randf() < float(ai.get("wild_random", 0.25)):
		var mid: String = moves[engine.rng.randi() % moves.size()]
		var tg := engine.legal_targets(m, str(engine.move_data(mid).get("target", "enemy")))
		return {"kind": "move", "move": mid, "target": tg[engine.rng.randi() % tg.size()].uid if not tg.is_empty() else 0}
	var best := {"kind": "move", "move": moves[0], "target": 0}
	var best_score := -1.0
	for mid in moves:
		var mv := engine.move_data(mid)
		var target_kind := str(mv.get("target", "enemy"))
		for t in engine.legal_targets(m, target_kind):
			var s := score(engine, m, mv, t, target_kind)
			if s > best_score:
				best_score = s
				best = {"kind": "move", "move": mid, "target": t.uid}
	return best


## Valor esperado de usar o golpe no alvo (em "PV equivalentes").
static func score(engine: BattleEngine, user: Monster, mv: Dictionary, target: Monster, target_kind: String) -> float:
	var ai: Dictionary = engine.rules.get("ai", {})
	var acc := float(mv.get("accuracy", 100)) / 100.0
	var value := 0.0
	var foes := target.side != user.side
	if foes and str(mv.get("category", "")) != "status" and int(mv.get("power", 0)) > 0:
		var r := BattleEngine.calc_damage(engine.rules, user, target, mv, null, {"crit": false})
		var dmg := float(r["damage"])
		if target_kind == "all_enemies":
			dmg *= 0.75 * maxf(1.0, engine.active_units(target.side).size())
		value += minf(dmg, target.hp) * acc
		if dmg >= target.hp:
			value *= 1.3
	for eff in mv.get("effects", []):
		var chance := float(eff.get("chance", 100)) / 100.0 * acc
		match str(eff.get("kind", "")):
			"poison":
				if foes and not target.is_poisoned():
					value += target.max_hp() * float(engine.rules.get("poison", {}).get("fraction", 0.08)) * 4.0 * chance
			"heal":
				if not foes and target.hp_ratio() < float(ai.get("heal_below", 0.35)):
					value += target.max_hp() * float(eff.get("percent", 30)) / 100.0 * 1.6
			"cure":
				if not foes and target.is_poisoned():
					value += target.max_hp() * 0.25
			"stat":
				var stage := int(target.stages.get(str(eff.get("stat", "")), 0))
				var helps := (int(eff.get("stages", 1)) > 0) != foes
				if helps and abs(stage) < 2:
					value += user.max_hp() * 0.12 * chance
	return value
