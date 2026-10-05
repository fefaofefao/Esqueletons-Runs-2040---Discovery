extends "res://tests/test_case.gd"
## Regras da batalha (seção 9): fórmula, tipos, ordem, veneno, estágios, itens,
## troca, fuga, XP (100%/50%), níveis e fim da batalha.

var R: Dictionary


func _team(specs: Array) -> Array:
	var out := []
	for s in specs:
		out.append(Monster.create(s[0], s[1]))
	return out


func _engine(p: Array, e: Array, kind := "wild", seed := 7) -> BattleEngine:
	var b := BattleEngine.new()
	b.setup(_team(p), _team(e), kind, seed)
	return b


func test_damage_formula_matches_spec() -> void:
	R = Data.battle_rules()
	var a := Monster.create("teste_fisico", 20)
	var d := Monster.create("teste_magico", 20)
	var mv := Data.move("teste_soco")
	var r := BattleEngine.calc_damage(R, a, d, mv, null, {"variance": 1.0, "crit": false})
	var expected := ((2.0 * 20 / 5 + 2) * 40 * a.stat("atk") / float(d.stat("def"))) / 50.0 + 2
	expected *= 1.5 * 1.25  # físico vence mágico + mesmo tipo
	check_eq(r["damage"], int(expected), "dano = fórmula da seção 9")
	var crit := BattleEngine.calc_damage(R, a, d, mv, null, {"variance": 1.0, "crit": true})
	check_eq(crit["damage"], int(expected * 1.5), "crítico ×1,5")
	var low := BattleEngine.calc_damage(R, a, d, mv, null, {"variance": 0.85, "crit": false})
	check_eq(low["damage"], int(expected * 0.85), "variação mínima 0,85")


func test_type_chart() -> void:
	R = Data.battle_rules()
	check(is_equal_approx(BattleEngine.type_multiplier(R, "fisico", "magico"), 1.5), "Físico > Mágico")
	check(is_equal_approx(BattleEngine.type_multiplier(R, "magico", "veneno"), 1.5), "Mágico > Veneno")
	check(is_equal_approx(BattleEngine.type_multiplier(R, "veneno", "fisico"), 1.5), "Veneno > Físico")
	check(is_equal_approx(BattleEngine.type_multiplier(R, "magico", "fisico"), 0.75), "contra: ×0,75")
	for t in ["fisico", "magico", "veneno", "cura"]:
		check(is_equal_approx(BattleEngine.type_multiplier(R, "cura", t), 1.0), "Cura neutro atacando %s" % t)
		check(is_equal_approx(BattleEngine.type_multiplier(R, t, "cura"), 1.0), "Cura neutro defendendo de %s" % t)
	check_eq(BattleEngine.effectiveness_label(1.5), "BTL_EFF_STRONG", "rótulo Forte")
	check_eq(BattleEngine.effectiveness_label(0.75), "BTL_EFF_WEAK", "rótulo Fraco")


func test_turn_order_speed_and_priority() -> void:
	var b := _engine([["teste_cura", 20], ["teste_veneno", 20]], [["teste_fisico", 20], ["teste_magico", 20]])
	var order := b.predicted_order()
	for i in order.size() - 1:
		check(order[i].battle_stat("spd") >= order[i + 1].battle_stat("spd"), "ordem por VEL")
	var slow: Monster = b.active_units(0)[0]  # cura, o mais lento
	var acts := {slow.uid: {"kind": "move", "move": "teste_golpe_rapido", "target": b.active_units(1)[0].uid}}
	check(b.predicted_order(acts)[0] == slow, "golpe com prioridade passa na frente")
	acts = {slow.uid: {"kind": "switch", "to": 0}}
	check(b.predicted_order(acts)[0] == slow, "troca age antes dos golpes")


func test_round_events_and_pp() -> void:
	var b := _engine([["teste_fisico", 15], ["teste_magico", 15]], [["teste_magico", 12], ["teste_fisico", 12]])
	var p0: Monster = b.active_units(0)[0]
	var target: Monster = b.active_units(1)[0]
	var pp_before: int = p0.moves.filter(func(x): return x.id == "teste_soco")[0].pp
	var ev := b.run_round({p0.uid: {"kind": "move", "move": "teste_soco", "target": target.uid}})
	check(ev.any(func(e): return e.t == "move" and e.user == p0.uid), "evento do golpe")
	check(ev.any(func(e): return e.t == "damage" or e.t == "miss"), "evento de dano")
	var pp_after: int = p0.moves.filter(func(x): return x.id == "teste_soco")[0].pp
	check_eq(pp_after, pp_before - 1, "gasta 1 PP")


func test_poison_lasts_3_to_5_turns() -> void:
	var durations := {}
	for seed in 40:
		var b := _engine([["teste_veneno", 20]], [["teste_cura", 20]], "wild", seed)
		var v: Monster = b.active_units(0)[0]
		var t: Monster = b.active_units(1)[0]
		b._apply_effect(v, t, {"kind": "poison"})
		durations[t.poison_turns] = true
		check(t.poison_turns >= 3 and t.poison_turns <= 5, "veneno entre 3 e 5 turnos")
		var hp := t.hp
		b._end_of_round()
		check(t.hp < hp, "veneno tira PV no fim da rodada")
	check(durations.size() >= 2, "duração do veneno varia")


func test_stat_stages() -> void:
	var b := _engine([["teste_cura", 20]], [["teste_fisico", 20]])
	var m: Monster = b.active_units(0)[0]
	var base := m.battle_stat("atk")
	for i in 5:
		b._apply_effect(m, m, {"kind": "stat", "stat": "atk", "stages": 1})
	check_eq(int(m.stages["atk"]), 3, "estágio máximo +3")
	check(is_equal_approx(m.battle_stat("atk"), base * 2.5), "+3 = ×2,5")
	check(is_equal_approx(Monster.stage_multiplier(-3), 0.4), "-3 = ×0,4")


func test_heal_items_and_revive() -> void:
	var b := _engine([["teste_fisico", 20], ["teste_magico", 20]], [["teste_cura", 5]])
	b.bag = {"pocao_p": 1, "reviver": 1, "antidoto": 1}
	var a: Monster = b.active_units(0)[0]
	var c: Monster = b.active_units(0)[1]
	a.hp = 10
	b._use_item(a, "pocao_p", a.uid)
	check_eq(a.hp, mini(40, a.max_hp()), "Poção P cura 30")
	check(not b.bag.has("pocao_p"), "item consumido")
	c.hp = 0
	b._use_item(a, "reviver", c.uid)
	check(c.hp == int(c.max_hp() * 0.5), "Reviver volta com 50%")
	a.poison_turns = 3
	b._use_item(a, "antidoto", a.uid)
	check(not a.is_poisoned(), "antídoto cura veneno")


func test_switch_costs_turn() -> void:
	var b := _engine([["teste_fisico", 20], ["teste_magico", 20], ["teste_cura", 20]], [["teste_veneno", 5]])
	var a: Monster = b.active_units(0)[0]
	var ev := b.run_round({a.uid: {"kind": "switch", "to": 2}})
	check(ev.any(func(e): return e.t == "switch_in"), "troca acontece")
	check(not ev.any(func(e): return e.t == "move" and e.user == a.uid), "quem sai não ataca na rodada")
	check(b.active_units(0).any(func(m): return m.species_id == "teste_cura"), "reserva entrou")


func test_flee_rules() -> void:
	var b := _engine([["teste_veneno", 30]], [["teste_cura", 5]], "tamer")
	var a: Monster = b.active_units(0)[0]
	var ev := b.run_round({a.uid: {"kind": "flee"}})
	check(ev.any(func(e): return e.t == "cant_flee"), "não foge de domador")
	var fled := 0
	for seed in 200:
		var w := _engine([["teste_veneno", 30]], [["teste_cura", 30]], "wild", seed)
		var p := w.flee_chance()
		check(p >= 0.15 and p <= 0.95, "chance de fuga dentro dos limites")
		w.run_round({w.active_units(0)[0].uid: {"kind": "flee"}})
		if w.result == "fled":
			fled += 1
	check(fled > 60 and fled < 199, "fuga depende de sorte e VEL (%d/200)" % fled)
	var fast := _engine([["teste_veneno", 30]], [["teste_cura", 10]])
	var slow := _engine([["teste_cura", 10]], [["teste_veneno", 30]])
	check(fast.flee_chance() > slow.flee_chance(), "mais VEL = mais chance")


func test_xp_participants_and_reserves() -> void:
	var b := _engine([["teste_fisico", 10], ["teste_magico", 10], ["teste_cura", 10]], [["teste_veneno", 10]])
	var foe: Monster = b.active_units(1)[0]
	foe.hp = 1
	var reward := b.xp_reward(foe)
	var p: Array = b.teams[0]
	var xp_before := p.map(func(m): return m.xp)
	b._damage(foe, 1, {})
	b._on_faint(foe)
	check_eq(p[0].xp - xp_before[0], reward, "participante recebe 100%")
	check_eq(p[2].xp - xp_before[2], int(reward * 0.5), "reserva recebe 50%")
	b._check_end()
	check_eq(b.result, "win", "vence quando todos os inimigos caem")


func test_level_up_learns_moves() -> void:
	var m := Monster.create("teste_fisico", 7)
	var before := m.moves.size()
	var hp_before := m.max_hp()
	var levels := m.gain_xp(Monster.xp_for_level(8) - m.xp)
	check_eq(levels, [8], "sobe para o nível 8")
	check(m.max_hp() > hp_before, "atributos sobem com o nível")
	check(Monster.moves_learned_at("teste_fisico", 8).has("teste_fortalecer"), "learnset no nível 8")
	check(before <= 4, "no máximo 4 golpes")
	var full := Monster.create("teste_fisico", 20)
	check_eq(full.moves.size(), 4, "nasce com os 4 golpes mais recentes")
	check(BattleEngine.learn_move(full, "teste_soco", 0), "aprende trocando um golpe")
	var top := Monster.create("teste_fisico", 50)
	top.gain_xp(999999)
	check_eq(top.level, 50, "nível máximo 50")


func test_defeat() -> void:
	var b := _engine([["teste_cura", 2]], [["teste_fisico", 40]], "wild", 3)
	for i in 20:
		if b.result != "":
			break
		var a: Monster = b.active_units(0)[0]
		b.run_round({a.uid: {"kind": "move", "move": "teste_faisca", "target": b.active_units(1)[0].uid}})
	check_eq(b.result, "lose", "perde quando a equipe toda cai")


func test_serialization() -> void:
	var m := Monster.create("teste_veneno", 17, true)
	m.hp -= 5
	m.poison_turns = 2
	var copy := Monster.from_dict(JSON.parse_string(JSON.stringify(m.to_dict())))
	check_eq(copy.to_dict(), m.to_dict(), "ida e volta pelo JSON do save")
	check(copy.stat("atk") > Monster.create("teste_veneno", 17).stat("atk"), "Golden tem +10%")


func test_ai_heals_when_low() -> void:
	var b := _engine([["teste_fisico", 20]], [["teste_cura", 20]], "tamer")
	var foe: Monster = b.active_units(1)[0]
	foe.hp = int(foe.max_hp() * 0.2)
	var a := BattleAI.choose(b, foe)
	var heals := func(id: String) -> bool:
		return Data.move(id).get("effects", []).any(func(e): return e.kind == "heal")
	check(heals.call(a.move) and a.target == foe.uid, "IA se cura abaixo de 35%% (%s)" % a.move)
	foe.hp = foe.max_hp()
	a = BattleAI.choose(b, foe)
	check(not heals.call(a.move), "IA ataca com PV cheio")
