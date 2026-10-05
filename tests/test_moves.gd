extends "res://tests/test_case.gd"
## Fase 3c: golpes reais (2 acertos, dreno, efeito em si mesmo), learnsets das
## 80 espécies e batalhas completas entre espécies reais.

var R: Dictionary


func _engine(p: Array, e: Array, seed := 3) -> BattleEngine:
	var b := BattleEngine.new()
	b.setup(p, e, "tamer", seed)
	return b


func _use(b: BattleEngine, user: Monster, move_id: String, target: Monster) -> Array:
	b.events = []
	b._use_move(user, move_id, target.uid, 1.0)
	return b.events


func test_two_hits() -> void:
	var a := Monster.create("grumete_2", 30)
	var d := Monster.create("mineiro_2", 40)
	var b := _engine([a], [d])
	var evs := _use(b, a, "remada_dupla", d)
	var hits := evs.filter(func(e: Dictionary) -> bool: return e.t == "damage" or e.t == "miss")
	check(hits.size() == 2 or evs.any(func(e: Dictionary) -> bool: return e.t == "miss"), "Remada Dupla acerta 2 vezes (%d)" % hits.size())


func test_drain_heals_user() -> void:
	var a := Monster.create("gasista_3", 60)
	var d := Monster.create("mineiro_3", 60)
	var b := _engine([a], [d])
	a.hp = a.max_hp() / 3
	var before := a.hp
	_use(b, a, "dreno_toxico", d)
	check(a.hp > before, "Dreno Tóxico recupera PV de quem usa")


func test_self_effect_on_attack() -> void:
	var a := Monster.create("cartografo_2", 55)
	var d := Monster.create("mineiro_2", 40)
	var b := _engine([a], [d])
	_use(b, a, "rota_dos_ecos", d)
	check_eq(int(a.stages.get("spd", 0)), 1, "Rota dos Ecos sobe a VEL de quem usa")
	check_eq(int(d.stages.get("spd", 0)), 0, "e não a do alvo")
	var c := Monster.create("carregador_3", 70)
	var e := Monster.create("sentinela_3", 70)
	var b2 := _engine([c], [e])
	_use(b2, c, "avalanche_de_carga", e)
	check_eq(int(c.stages.get("spd", 0)), -1, "Avalanche de Carga baixa a VEL de quem usa")


func test_every_species_has_moves() -> void:
	R = Data.battle_rules()
	for id in Data.all_species_ids(false):
		var info := Data.species(id)
		var age := 5
		var gl: Array = info.get("growth_levels", [])
		if gl.size() == 2 and int(info.get("stage", 1)) > 1:
			age = int(gl[int(info.stage) - 2]) + 2
		if id == "rei_esqueleto":
			age = 120
		var m := Monster.create(id, age)
		check(m.moves.size() >= 2, "%s (%d anos) sabe ao menos 2 golpes (%d)" % [id, age, m.moves.size()])
		var attacks := m.moves.filter(func(mv: Dictionary) -> bool: return int(Data.move(str(mv.id)).get("power", 0)) > 0)
		check(not attacks.is_empty(), "%s tem golpe de dano" % id)
		if gl.size() == 2 and int(info.get("stage", 1)) == 2:
			check(info.get("growth_move", "") == info.get("signature_move", ""), "%s aprende a assinatura ao crescer" % id)


func test_signature_only_own_line() -> void:
	var d = Data.load_json("res://data/species.json")
	var owner := {}
	for ln in d.lines:
		owner[ln.signature_move] = ln.id
	for ln in d.lines:
		for st in ln.stages:
			for e in st.learnset:
				if owner.has(e[1]):
					check_eq(owner[e[1]], ln.id, "%s aprende assinatura alheia %s" % [st.id, e[1]])


func test_real_battles_finish() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 80
	var ids := Data.all_species_ids(false)
	for k in 12:
		var age := rng.randi_range(10, 90)
		var p := []
		var e := []
		for i in 2:
			p.append(Monster.create(ids[rng.randi() % ids.size()], age))
			e.append(Monster.create(ids[rng.randi() % ids.size()], age))
		var b := _engine(p, e, k)
		for step in 600:
			var actor := b.next_actor()
			if actor == null:
				break
			b.act(BattleAI.choose(b, actor, false))
			if b.result != "":
				break
		check(b.result in ["win", "lose"], "batalha real %d termina (%s)" % [k, b.result])
