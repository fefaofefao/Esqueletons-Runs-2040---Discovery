class_name BattleEngine
extends RefCounted
## Regras da batalha em dupla (2×2), sem nenhuma interface: a tela de batalha
## e o simulador (fase 3c) usam a mesma lógica. Cada rodada devolve uma lista
## de eventos que a tela anima em ordem.
##
## Ações (uma por esqueleto ativo do jogador):
##   {"kind": "move", "move": id, "target": uid}
##   {"kind": "switch", "to": índice no time}
##   {"kind": "item", "item": id, "target": uid}
##   {"kind": "flee"}
##
## Eventos: ver _ev(); cada um tem "t" (tipo) e uids dos envolvidos.

const PLAYER := 0
const ENEMY := 1

var rules: Dictionary
var rng := RandomNumberGenerator.new()
var kind := "wild"  # wild | tamer | boss
var teams: Array = [[], []]
var active: Array = [[-1, -1], [-1, -1]]
var bag: Dictionary = {}
var round_no := 0
var flee_attempts := 0
var result := ""  # "" | win | lose | fled
var events: Array = []
var last_player_actions: Dictionary = {}
var _participants := {}


func setup(player_team: Array, enemy_team: Array, battle_kind: String = "wild", seed: int = -1) -> void:
	rules = Data.battle_rules()
	if seed >= 0:
		rng.seed = seed
	else:
		rng.randomize()
	kind = battle_kind
	teams = [player_team, enemy_team]
	var per := int(rules.get("active_per_side", 2))
	for side in 2:
		active[side] = []
		for i in per:
			active[side].append(-1)
		for m in teams[side]:
			m.reset_battle_state()
			m.side = side
		var slot := 0
		for i in teams[side].size():
			if slot >= per:
				break
			if not teams[side][i].is_fainted():
				active[side][slot] = i
				slot += 1
	result = ""
	round_no = 0
	flee_attempts = 0
	_participants = {}
	_mark_participation()


func is_wild() -> bool:
	return kind == "wild"


# ------------------------------------------------------------------ consultas
func active_units(side: int) -> Array:
	var out := []
	for idx in active[side]:
		if idx >= 0 and not teams[side][idx].is_fainted():
			out.append(teams[side][idx])
	return out


func slot_of(m: Monster) -> int:
	var idx: int = teams[m.side].find(m)
	return active[m.side].find(idx) if idx >= 0 else -1


func find(uid: int) -> Monster:
	for side in 2:
		for m in teams[side]:
			if m.uid == uid:
				return m
	return null


func alive_count(side: int) -> int:
	var n := 0
	for m in teams[side]:
		if not m.is_fainted():
			n += 1
	return n


func reserves(side: int) -> Array:
	var out := []
	for i in teams[side].size():
		if not active[side].has(i) and not teams[side][i].is_fainted():
			out.append(i)
	return out


func legal_targets(user: Monster, target_kind: String) -> Array:
	match target_kind:
		"enemy", "all_enemies":
			return active_units(1 - user.side)
		"self":
			return [user]
		"ally", "all_allies":
			return active_units(user.side)
		"party":
			return teams[user.side].filter(func(m: Monster) -> bool: return not m.is_fainted())
		"fainted_ally":
			return teams[user.side].filter(func(m: Monster) -> bool: return m.is_fainted())
	return []


static func target_needs_choice(target_kind: String) -> bool:
	return target_kind in ["enemy", "ally", "party", "fainted_ally"]


func move_data(id: String) -> Dictionary:
	if id == "struggle":
		var s: Dictionary = rules.get("struggle", {}).duplicate()
		s["id"] = "struggle"
		return s
	return Data.move(id)


func usable_moves(m: Monster) -> Array:
	var out := []
	for mv in m.moves:
		if int(mv["pp"]) > 0:
			out.append(str(mv["id"]))
	return out if not out.is_empty() else ["struggle"]


func effectiveness(move_type: String, defender_type: String) -> float:
	return BattleEngine.type_multiplier(rules, move_type, defender_type)


static func type_multiplier(r: Dictionary, move_type: String, defender_type: String) -> float:
	var chart: Dictionary = r.get("type_chart", {})
	var beats: Dictionary = chart.get("beats", {})
	if beats.get(move_type, "") == defender_type:
		return float(chart.get("strong", 1.5))
	if beats.get(defender_type, "") == move_type:
		return float(chart.get("weak", 0.75))
	return 1.0


static func effectiveness_label(mult: float) -> String:
	if mult > 1.01:
		return "BTL_EFF_STRONG"
	if mult < 0.99:
		return "BTL_EFF_WEAK"
	return "BTL_EFF_NORMAL"


## Fórmula da seção 9:
## ((2×Nível/5+2) × Poder × Ataque/Defesa)/50 + 2
## × vantagem de tipo × mesmo tipo (1,25) × variação (0,85–1,0) × crítico (1,5; 6,25%).
static func calc_damage(r: Dictionary, attacker: Monster, defender: Monster, mv: Dictionary,
		random: RandomNumberGenerator, opts: Dictionary = {}) -> Dictionary:
	var d: Dictionary = r.get("damage", {})
	var physical: bool = str(mv.get("category", "physical")) == "physical"
	var atk := attacker.battle_stat("atk" if physical else "mag")
	var def := maxf(1.0, defender.battle_stat("def" if physical else "res"))
	var lvl := float(attacker.level)
	var power := float(mv.get("power", 0))
	var base := ((float(d.get("level_mul", 2)) * lvl / float(d.get("level_div", 5)) + float(d.get("level_add", 2)))
		* power * atk / def) / float(d.get("div", 50)) + float(d.get("add", 2))
	var eff := type_multiplier(r, str(mv.get("type", "")), defender.type())
	var stab := float(d.get("stab", 1.25)) if str(mv.get("type", "")) == attacker.type() else 1.0
	var vr: Array = d.get("variance", [0.85, 1.0])
	var variance: float = opts.get("variance", random.randf_range(float(vr[0]), float(vr[1])) if random else (float(vr[0]) + float(vr[1])) / 2.0)
	var crit: bool = opts.get("crit", random.randf() < float(d.get("crit_chance", 0.0625)) if random else false)
	var dmg := base * eff * stab * variance * (float(d.get("crit_mul", 1.5)) if crit else 1.0)
	return {"damage": maxi(1, int(dmg)), "crit": crit, "eff": eff}


# ------------------------------------------------------------------ ordem
func action_priority(a: Dictionary) -> int:
	var pr: Dictionary = rules.get("priority", {})
	match str(a.get("kind", "")):
		"switch":
			return int(pr.get("switch", 6))
		"item":
			return int(pr.get("item", 5))
		"flee":
			return int(pr.get("flee", 7))
		"move":
			return int(move_data(str(a.get("move", ""))).get("priority", 0))
	return 0


func order_actions(acts: Array) -> Array:
	for a in acts:
		a["_tie"] = rng.randf()
	acts.sort_custom(func(x: Dictionary, y: Dictionary) -> bool:
		var px := action_priority(x)
		var py := action_priority(y)
		if px != py:
			return px > py
		var sx: float = (x["user"] as Monster).battle_stat("spd")
		var sy: float = (y["user"] as Monster).battle_stat("spd")
		if not is_equal_approx(sx, sy):
			return sx > sy
		return x["_tie"] > y["_tie"])
	return acts


## Ordem prevista para a timeline (prioridade das ações escolhidas, se houver, e VEL).
func predicted_order(player_actions: Dictionary = {}) -> Array:
	var acts := []
	for side in 2:
		for m in active_units(side):
			var a: Dictionary = player_actions.get(m.uid, {"kind": "move", "move": ""}).duplicate()
			a["user"] = m
			acts.append(a)
	var saved := rng.state
	var ordered := order_actions(acts)
	rng.state = saved
	return ordered.map(func(a: Dictionary) -> Monster: return a["user"])


# ------------------------------------------------------------------ rodada
func run_round(player_actions: Dictionary) -> Array:
	events = []
	if result != "":
		return events
	round_no += 1
	last_player_actions = player_actions.duplicate(true)
	_mark_participation()
	var acts := []
	for m in active_units(PLAYER):
		if player_actions.has(m.uid):
			var a: Dictionary = player_actions[m.uid].duplicate()
			a["user"] = m
			acts.append(a)
	for m in active_units(ENEMY):
		var a := BattleAI.choose(self, m)
		a["user"] = m
		acts.append(a)
	for a in order_actions(acts):
		if result != "":
			break
		var user: Monster = a["user"]
		if user.is_fainted() or slot_of(user) < 0:
			continue
		_execute(a)
		_check_end()
	if result == "":
		_end_of_round()
		_check_end()
	return events


func _ev(t: String, data: Dictionary = {}) -> void:
	var e := data.duplicate()
	e["t"] = t
	events.append(e)


func _execute(a: Dictionary) -> void:
	var user: Monster = a["user"]
	match str(a.get("kind", "")):
		"move":
			_use_move(user, str(a.get("move", "struggle")), int(a.get("target", 0)))
		"switch":
			switch_in(user.side, slot_of(user), int(a.get("to", -1)))
		"item":
			_use_item(user, str(a.get("item", "")), int(a.get("target", 0)))
		"flee":
			_try_flee(user)


func _use_move(user: Monster, move_id: String, target_uid: int) -> void:
	var mv := move_data(move_id)
	if mv.is_empty():
		return
	if move_id != "struggle":
		for entry in user.moves:
			if entry["id"] == move_id:
				if int(entry["pp"]) <= 0:
					move_id = "struggle"
					mv = move_data(move_id)
				else:
					entry["pp"] = int(entry["pp"]) - 1
				break
	_ev("move", {"user": user.uid, "move": move_id})
	var target_kind := str(mv.get("target", "enemy"))
	var targets := legal_targets(user, target_kind)
	if target_kind in ["enemy", "ally"]:
		var chosen := find(target_uid)
		if chosen == null or not targets.has(chosen):
			# alvo caiu ou saiu: passa para outro válido do mesmo lado
			chosen = targets[0] if not targets.is_empty() else null
		targets = [chosen] if chosen else []
	if targets.is_empty():
		_ev("no_target", {"user": user.uid})
		return
	for target in targets:
		if target.is_fainted():
			continue
		var acc := float(mv.get("accuracy", 100))
		if acc < 100.0 and rng.randf() * 100.0 >= acc:
			_ev("miss", {"user": user.uid, "target": target.uid})
			continue
		if str(mv.get("category", "physical")) != "status" and int(mv.get("power", 0)) > 0:
			var r := calc_damage(rules, user, target, mv, rng)
			if target_kind == "all_enemies" and targets.size() > 1:
				r["damage"] = maxi(1, int(r["damage"] * 0.75))
			_damage(target, int(r["damage"]), {"crit": r["crit"], "eff": r["eff"], "user": user.uid})
		for eff in mv.get("effects", []):
			if target.is_fainted():
				break
			if rng.randf() * 100.0 >= float(eff.get("chance", 100)):
				continue
			_apply_effect(user, target, eff)
		if target.is_fainted():
			_on_faint(target)


func _damage(target: Monster, amount: int, extra: Dictionary) -> void:
	var dealt := mini(amount, target.hp)
	target.hp -= dealt
	var e := {"target": target.uid, "amount": dealt, "hp": target.hp}
	e.merge(extra)
	_ev("damage", e)


func _apply_effect(user: Monster, target: Monster, eff: Dictionary) -> void:
	match str(eff.get("kind", "")):
		"poison":
			if target.is_poisoned():
				_ev("already_poisoned", {"target": target.uid})
				return
			var turns: Array = rules.get("poison", {}).get("turns", [3, 5])
			target.poison_turns = rng.randi_range(int(turns[0]), int(turns[1]))
			_ev("poisoned", {"target": target.uid, "turns": target.poison_turns})
		"stat":
			var s := str(eff.get("stat", "atk"))
			var st: Dictionary = rules.get("stages", {})
			var before := int(target.stages.get(s, 0))
			var after := clampi(before + int(eff.get("stages", 1)), int(st.get("min", -3)), int(st.get("max", 3)))
			target.stages[s] = after
			_ev("stat", {"target": target.uid, "stat": s, "delta": after - before, "requested": int(eff.get("stages", 1))})
		"heal":
			var amount := int(ceil(target.max_hp() * float(eff.get("percent", 30)) / 100.0))
			_heal(target, amount)
		"cure":
			if target.is_poisoned():
				target.poison_turns = 0
				_ev("cured", {"target": target.uid})


func _heal(target: Monster, amount: int) -> void:
	var healed := mini(amount, target.max_hp() - target.hp)
	target.hp += healed
	_ev("heal", {"target": target.uid, "amount": healed, "hp": target.hp})


func _use_item(user: Monster, item_id: String, target_uid: int) -> void:
	var it := Data.item(item_id)
	var target := find(target_uid)
	if it.is_empty() or target == null or int(bag.get(item_id, 0)) <= 0:
		_ev("item_fail", {"user": user.uid, "item": item_id})
		return
	bag[item_id] = int(bag[item_id]) - 1
	if int(bag[item_id]) <= 0:
		bag.erase(item_id)
	_ev("item", {"user": user.uid, "item": item_id, "target": target.uid})
	match str(it.get("kind", "")):
		"heal":
			if not target.is_fainted():
				_heal(target, int(it.get("amount", 30)))
		"cure":
			if target.is_poisoned():
				target.poison_turns = 0
				_ev("cured", {"target": target.uid})
		"revive":
			if target.is_fainted():
				target.hp = maxi(1, int(target.max_hp() * float(it.get("fraction", 0.5))))
				target.poison_turns = 0
				_ev("revived", {"target": target.uid, "hp": target.hp})


func flee_chance() -> float:
	var f: Dictionary = rules.get("flee", {})
	var mine := 0.0
	var theirs := 1.0
	for m in active_units(PLAYER):
		mine = maxf(mine, m.battle_stat("spd"))
	for m in active_units(ENEMY):
		theirs = maxf(theirs, m.battle_stat("spd"))
	var p := float(f.get("base", 0.5)) + float(f.get("speed_k", 0.4)) * (mine - theirs) / theirs + float(f.get("attempt_bonus", 0.12)) * flee_attempts
	return clampf(p, float(f.get("min", 0.15)), float(f.get("max", 0.95)))


func _try_flee(user: Monster) -> void:
	if not is_wild():
		_ev("cant_flee", {"user": user.uid})
		return
	var p := flee_chance()
	flee_attempts += 1
	if rng.randf() < p:
		result = "fled"
		_ev("fled", {"user": user.uid})
	else:
		_ev("flee_failed", {"user": user.uid})


## Troca o esqueleto de um slot. Usado pela ação "switch" e para repor quem caiu.
func switch_in(side: int, slot: int, team_index: int) -> bool:
	if slot < 0 or team_index < 0 or team_index >= teams[side].size():
		return false
	var incoming: Monster = teams[side][team_index]
	if incoming.is_fainted() or active[side].has(team_index):
		return false
	var out_idx: int = active[side][slot]
	if out_idx >= 0:
		var outgoing: Monster = teams[side][out_idx]
		outgoing.stages = {}
		_ev("switch_out", {"target": outgoing.uid, "slot": slot, "side": side})
	active[side][slot] = team_index
	incoming.stages = {}
	_ev("switch_in", {"target": incoming.uid, "slot": slot, "side": side})
	_mark_participation()
	return true


## Slots do jogador vazios (alguém caiu) que podem ser preenchidos por reservas.
func pending_replacements() -> Array:
	var out := []
	if reserves(PLAYER).is_empty():
		return out
	for slot in active[PLAYER].size():
		var idx: int = active[PLAYER][slot]
		if idx < 0 or teams[PLAYER][idx].is_fainted():
			out.append(slot)
	return out.slice(0, reserves(PLAYER).size())


func _on_faint(m: Monster) -> void:
	m.poison_turns = 0
	_ev("faint", {"target": m.uid})
	if m.side == ENEMY:
		_award_xp(m)
		var slot := slot_of(m)
		var res := reserves(ENEMY)
		if slot >= 0:
			active[ENEMY][slot] = -1
			if not res.is_empty():
				switch_in(ENEMY, slot, res[0])
	else:
		var slot := slot_of(m)
		if slot >= 0:
			active[PLAYER][slot] = -1


func _end_of_round() -> void:
	var p: Dictionary = rules.get("poison", {})
	for side in 2:
		for m in active_units(side):
			if not m.is_poisoned():
				continue
			var dmg := maxi(int(p.get("min_damage", 1)), int(m.max_hp() * float(p.get("fraction", 0.0834))))
			m.poison_turns -= 1
			var dealt := mini(dmg, m.hp)
			m.hp -= dealt
			_ev("poison_tick", {"target": m.uid, "amount": dealt, "hp": m.hp})
			if m.is_fainted():
				_on_faint(m)
			elif m.poison_turns == 0:
				_ev("poison_end", {"target": m.uid})


func _check_end() -> void:
	if result != "":
		return
	if alive_count(ENEMY) == 0:
		result = "win"
		_ev("win")
	elif alive_count(PLAYER) == 0:
		result = "lose"
		_ev("lose")


# ------------------------------------------------------------------ XP
func _mark_participation() -> void:
	for e in active_units(ENEMY):
		if not _participants.has(e.uid):
			_participants[e.uid] = {}
		for p in active_units(PLAYER):
			_participants[e.uid][p.uid] = true
			p.participated = true


func xp_reward(enemy: Monster) -> int:
	var x: Dictionary = rules.get("xp", {})
	var base := float(enemy.info().get("base_xp", 60))
	var mul := 1.0 if is_wild() else float(x.get("trainer_mul", 1.5))
	return maxi(1, int(base * enemy.level / 5.0 * mul))


func _award_xp(enemy: Monster) -> void:
	var x: Dictionary = rules.get("xp", {})
	var total := xp_reward(enemy)
	var parts: Dictionary = _participants.get(enemy.uid, {})
	for m in teams[PLAYER]:
		if m.is_fainted():
			continue
		var share := float(x.get("participant_share", 1.0)) if parts.has(m.uid) else float(x.get("reserve_share", 0.5))
		var amount := maxi(1, int(total * share))
		var old_level: int = m.level
		var levels: Array = m.gain_xp(amount)
		_ev("xp", {"target": m.uid, "amount": amount, "levels": levels, "from_level": old_level})
		for lvl in levels:
			for mid in Monster.moves_learned_at(m.species_id, lvl):
				if m.knows(mid):
					continue
				if m.moves.size() < 4:
					m.moves.append({"id": mid, "pp": int(Data.move(mid).get("pp", 10))})
					_ev("learned", {"target": m.uid, "move": mid})
				else:
					_ev("learn_prompt", {"target": m.uid, "move": mid})


## Resolve o pedido de aprender golpe (replace_index -1 = não aprender).
static func learn_move(m: Monster, move_id: String, replace_index: int) -> bool:
	if replace_index < 0 or replace_index >= m.moves.size():
		return false
	m.moves[replace_index] = {"id": move_id, "pp": int(Data.move(move_id).get("pp", 10))}
	return true
