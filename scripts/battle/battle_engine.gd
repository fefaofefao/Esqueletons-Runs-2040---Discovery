class_name BattleEngine
extends RefCounted
## Regras da batalha em dupla (2×2) com TURNOS POR TEMPO (timeline):
## cada esqueleto em campo tem um "relógio". Quem chega primeiro age; depois
## volta para a fila com uma espera = base / VEL × PESO da ação.
##   - golpes LEVES voltam logo, PESADOS demoram (o jogador vê isso na timeline);
##   - alguns golpes ATRASAM o alvo (empurram o próximo turno dele);
##   - SINTONIA: se dois aliados agem em sequência, o segundo ganha +25%.
## Sem nenhuma interface: a tela e o simulador (fase 3c) usam o mesmo motor.
##
## Uso: next_actor() diz quem age; act(ação) resolve e devolve eventos.
## Ações: {"kind": "move", "move": id, "target": uid} | {"kind": "switch", "to": índice}
##        {"kind": "item", "item": id, "target": uid}    | {"kind": "flee"}

const PLAYER := 0
const ENEMY := 1

var rules: Dictionary
var rng := RandomNumberGenerator.new()
var kind := "wild"  # wild | tamer | boss
var teams: Array = [[], []]
var active: Array = [[-1, -1], [-1, -1]]
var bag: Dictionary = {}
var now := 0.0
var turn_no := 0
var flee_attempts := 0
var result := ""  # "" | win | lose | fled
var events: Array = []
## Próximo instante de ação de cada esqueleto em campo (uid -> tempo).
var next_at: Dictionary = {}
## Última ação de cada esqueleto do jogador (para "Repetir").
var last_actions: Dictionary = {}
var _last_side := -1
var _last_uid := -1
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
	next_at = {}
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
	var init: Array = rules.get("timing", {}).get("initial", [0.3, 0.65])
	for side in 2:
		for m in active_units(side):
			next_at[m.uid] = base_delay(m) * rng.randf_range(float(init[0]), float(init[1]))
	result = ""
	now = 0.0
	turn_no = 0
	flee_attempts = 0
	_last_side = -1
	_last_uid = -1
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
	var dmg := base * eff * stab * variance * (float(d.get("crit_mul", 1.5)) if crit else 1.0) * float(opts.get("bonus", 1.0))
	return {"damage": maxi(1, int(dmg)), "crit": crit, "eff": eff}


# ------------------------------------------------------------------ tempo
## Espera até a próxima ação: base / VEL efetiva.
func base_delay(m: Monster) -> float:
	return float(rules.get("timing", {}).get("base", 1000)) / maxf(1.0, m.battle_stat("spd"))


func move_weight(move_id: String) -> float:
	var w: Dictionary = rules.get("timing", {}).get("weights", {})
	return float(w.get(str(move_data(move_id).get("weight", "normal")), 1.0))


func action_weight(a: Dictionary) -> float:
	var t: Dictionary = rules.get("timing", {})
	match str(a.get("kind", "")):
		"move":
			return move_weight(str(a.get("move", "")))
		"switch":
			return float(t.get("switch", 1.0))
		"item":
			return float(t.get("item", 1.0))
		"flee":
			return float(t.get("flee", 1.0))
	return 1.0


func _order_key(m: Monster) -> Array:
	return [float(next_at.get(m.uid, INF)), -m.battle_stat("spd"), m.side, m.uid]


static func _key_less(a: Array, b: Array) -> bool:
	for i in a.size():
		if a[i] != b[i]:
			return a[i] < b[i]
	return false


## Quem age agora (o menor relógio entre os que estão em campo).
func next_actor() -> Monster:
	var best: Monster = null
	for side in 2:
		for m in active_units(side):
			if not next_at.has(m.uid):
				next_at[m.uid] = now + base_delay(m)
			if best == null or _key_less(_order_key(m), _order_key(best)):
				best = m
	return best


## Próximas n ações previstas (para a timeline). override: {uid: peso} da ação
## que esse esqueleto está escolhendo agora (mostra onde o próximo turno dele cai).
func predict(n: int = 8, override: Dictionary = {}) -> Array:
	var sim := next_at.duplicate()
	var units := active_units(PLAYER) + active_units(ENEMY)
	var out := []
	var used := {}
	for i in n:
		var best: Monster = null
		var best_t := INF
		for m in units:
			var t: float = sim.get(m.uid, now + base_delay(m))
			if best == null or t < best_t or (is_equal_approx(t, best_t) and m.battle_stat("spd") > best.battle_stat("spd")):
				best = m
				best_t = t
		if best == null:
			break
		out.append(best)
		var w := 1.0
		if override.has(best.uid) and not used.has(best.uid):
			w = float(override[best.uid])
			used[best.uid] = true
		sim[best.uid] = best_t + base_delay(best) * w
	return out


## Sintonia: o esqueleto age logo depois de um aliado (sem inimigo no meio).
func sintonia_for(m: Monster) -> bool:
	return _last_side == m.side and _last_uid != m.uid and _last_uid != -1


# ------------------------------------------------------------------ ação
func act(action: Dictionary) -> Array:
	events = []
	if result != "":
		return events
	var actor := next_actor()
	if actor == null:
		return events
	now = float(next_at[actor.uid])
	turn_no += 1
	_mark_participation()
	# veneno conta nos turnos do próprio envenenado
	if actor.is_poisoned():
		_poison_tick(actor)
		_check_end()
		if actor.is_fainted() or result != "":
			_last_side = -1
			_last_uid = -1
			return events
	var sync := sintonia_for(actor)
	_ev("turn", {"user": actor.uid, "sintonia": sync})
	if actor.side == PLAYER:
		last_actions[actor.uid] = action.duplicate()
	var bonus := float(rules.get("sintonia", {}).get("bonus", 1.25)) if sync else 1.0
	match str(action.get("kind", "")):
		"move":
			_use_move(actor, str(action.get("move", "struggle")), int(action.get("target", 0)), bonus)
		"switch":
			switch_in(actor.side, slot_of(actor), int(action.get("to", -1)))
		"item":
			_use_item(actor, str(action.get("item", "")), int(action.get("target", 0)))
		"flee":
			_try_flee(actor)
	if not actor.is_fainted() and slot_of(actor) >= 0:
		next_at[actor.uid] = now + base_delay(actor) * action_weight(action)
	_last_side = actor.side
	_last_uid = actor.uid
	_check_end()
	return events


## Turno do inimigo (IA).
func act_enemy() -> Array:
	var actor := next_actor()
	return act(BattleAI.choose(self, actor))


func _ev(t: String, data: Dictionary = {}) -> void:
	var e := data.duplicate()
	e["t"] = t
	events.append(e)


func _use_move(user: Monster, move_id: String, target_uid: int, bonus: float) -> void:
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
		var dealt := 0
		if str(mv.get("category", "physical")) != "status" and int(mv.get("power", 0)) > 0:
			for h in int(mv.get("hits", 1)):
				if target.is_fainted():
					break
				var r := calc_damage(rules, user, target, mv, rng, {"bonus": bonus})
				if target_kind == "all_enemies" and targets.size() > 1:
					r["damage"] = maxi(1, int(r["damage"] * 0.75))
				var before: int = target.hp
				_damage(target, int(r["damage"]), {"crit": r["crit"], "eff": r["eff"], "user": user.uid})
				dealt += before - target.hp
		for eff in mv.get("effects", []):
			var on_self: bool = str(eff.get("on", "target")) == "self"
			if target.is_fainted() and not on_self:
				continue
			if rng.randf() * 100.0 >= float(eff.get("chance", 100)):
				continue
			if str(eff.get("kind", "")) == "drain":
				if dealt > 0 and not user.is_fainted():
					_heal(user, maxi(1, int(dealt * float(eff.get("percent", 50)) / 100.0)))
				continue
			_apply_effect(user, user if on_self else target, eff, bonus)
		if target.is_fainted():
			_on_faint(target)


func _damage(target: Monster, amount: int, extra: Dictionary) -> void:
	var dealt := mini(amount, target.hp)
	target.hp -= dealt
	var e := {"target": target.uid, "amount": dealt, "hp": target.hp}
	e.merge(extra)
	_ev("damage", e)


func _apply_effect(user: Monster, target: Monster, eff: Dictionary, bonus: float = 1.0) -> void:
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
			var amount := int(ceil(target.max_hp() * float(eff.get("percent", 30)) / 100.0 * bonus))
			_heal(target, amount)
		"cure":
			if target.is_poisoned():
				target.poison_turns = 0
				_ev("cured", {"target": target.uid})
		"delay":
			if next_at.has(target.uid):
				var push := base_delay(target) * float(eff.get("amount", 0.3))
				next_at[target.uid] = float(next_at[target.uid]) + push
				_ev("delayed", {"target": target.uid})


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


## Troca o esqueleto de um slot (ação "switch" ou reposição de quem caiu).
## Quem entra espera um turno inteiro para agir.
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
		next_at.erase(outgoing.uid)
		if not outgoing.is_fainted():
			_ev("switch_out", {"target": outgoing.uid, "slot": slot, "side": side})
	active[side][slot] = team_index
	incoming.stages = {}
	next_at[incoming.uid] = now + base_delay(incoming) * float(rules.get("timing", {}).get("enter", 0.8))
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
	next_at.erase(m.uid)
	_ev("faint", {"target": m.uid})
	var slot := slot_of(m)
	if slot >= 0:
		active[m.side][slot] = -1
	if m.side == ENEMY:
		_award_xp(m)
		var res := reserves(ENEMY)
		if slot >= 0 and not res.is_empty():
			switch_in(ENEMY, slot, res[0])


func _poison_tick(m: Monster) -> void:
	var p: Dictionary = rules.get("poison", {})
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
	return maxi(1, int(base * enemy.level / float(x.get("reward_div", 5.0)) * mul))


func _award_xp(enemy: Monster) -> void:
	var x: Dictionary = rules.get("xp", {})
	var total := xp_reward(enemy)
	var parts: Dictionary = _participants.get(enemy.uid, {})
	for m in teams[PLAYER]:
		if m.is_fainted():
			continue
		var share := float(x.get("participant_share", 1.0)) if parts.has(m.uid) else float(x.get("reserve_share", 0.5))
		give_xp(m, maxi(1, int(total * share)))


## Dá XP a um aliado (vitória ou o premiado "dobrar a XP"), com subida de idade
## e golpes novos como eventos para a tela.
func give_xp(m: Monster, amount: int) -> void:
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
