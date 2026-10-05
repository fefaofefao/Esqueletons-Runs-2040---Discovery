extends "res://tests/test_case.gd"
## Fase 3a: crescimento por idade, cerimônia de aniversário, marcador de
## recrutamento, Golden (1/40 e "direito ao Golden"), Rancho e selvagens no mapa.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


func _fresh_save() -> void:
	SaveGame.data = SaveGame.new_game_data("Teste")


func test_growth_by_age() -> void:
	var m := Monster.create("teste_broto_1", 5)
	check_eq(m.stage(), 1, "bebê no estágio 1")
	check_eq(m.growth_target(), "", "aos 5 anos ainda não cresce")
	m.gain_xp(Monster.xp_for_level(6) - m.xp)
	check_eq(m.level, 6, "faz 6 anos")
	check_eq(m.growth_target(), "teste_broto_2", "aos 6 anos cresce para o estágio 2")
	m.hp = m.max_hp() / 2
	var ratio := m.hp_ratio()
	var r := m.grow()
	check_eq(r.get("from"), "teste_broto_1", "cresceu de")
	check_eq(r.get("to"), "teste_broto_2", "cresceu para")
	check_eq(r.get("move"), "teste_curativo", "golpe exclusivo do estágio 2")
	check(absf(m.hp_ratio() - ratio) < 0.05, "mantém a proporção de PV")
	check_eq(m.stage(), 2, "adolescente no estágio 2")
	check_eq(m.growth_target(), "", "estágio 2 só cresce aos 12")
	m.gain_xp(Monster.xp_for_level(12) - m.xp)
	check_eq(m.growth_target(), "teste_broto_3", "aos 12 cresce para o adulto")
	m.grow()
	check_eq(m.stage(), 3, "adulto no estágio 3")
	check_eq(m.growth_target(), "", "adulto não cresce mais")
	check(m.grow().is_empty(), "grow() sem alvo não faz nada")
	# idade máxima 100 para o time do jogador
	m.gain_xp(Monster.xp_for_level(130))
	check_eq(m.level, 100, "idade máxima 100")


func test_golden_rate() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 2040
	var n := 100000
	var hits := 0
	for i in n:
		if Ossuary.roll_golden(rng):
			hits += 1
	var expected := n / 40.0
	check(absf(hits - expected) <= expected * 0.05, "Golden em 1/40 ± 5%% (obtido %d de %d)" % [hits, n])
	for i in 200:
		check(not Ossuary.roll_golden(rng, "tamer"), "domadores nunca são Golden")
	# bônus de atributos do Golden
	var a := Monster.create("teste_brigao", 30)
	var b := Monster.create("teste_brigao", 30, true)
	check(b.stat("atk") > a.stat("atk"), "Golden tem atributos maiores")
	check(b.display_name() != a.display_name(), "Golden tem nome próprio")


func test_marker_gain_range() -> void:
	_fresh_save()
	for rarity_level in [[1, 30], [30, 1], [10, 10]]:
		var m := Monster.create("teste_brigao", rarity_level[0])
		var g := Ossuary.marker_gain(m, rarity_level[1])
		check(g >= 20 and g <= 50, "ganho do marcador entre 20 e 50 (obtido %d)" % g)
	var older := Ossuary.marker_gain(Monster.create("teste_brigao", 30), 10)
	var younger := Ossuary.marker_gain(Monster.create("teste_brigao", 10), 30)
	check(older > younger, "selvagem mais velho que o time enche mais o marcador")
	# vitórias até 100% e oferta
	var wins := 0
	var r := {}
	while wins < 10:
		r = Ossuary.register_win(Monster.create("teste_brigao", 10), 10)
		wins += 1
		if r.offer:
			break
	check(r.offer, "o marcador chega a 100%")
	check(wins >= 2 and wins <= 5, "leva de 2 a 5 vitórias (levou %d)" % wins)
	check(not r.golden, "sem direito ao Golden")
	Ossuary.refuse("teste_brigao")
	check_eq(int(Ossuary.entry("teste_brigao").marker), 100, "recusar mantém o marcador cheio")
	var rec := Ossuary.accept("teste_brigao", 10)
	check(not rec.golden, "recruta comum")
	check_eq(int(Ossuary.entry("teste_brigao").marker), 0, "aceitar zera o marcador")
	check(Ossuary.entry("teste_brigao").recruited, "marcado como recrutado")


func test_golden_right_99() -> void:
	_fresh_save()
	var g := Monster.create("teste_bruxo", 12, true)
	var r := Ossuary.register_win(g, 12)
	check_eq(r.after, 99, "derrotar um Golden deixa o marcador em 99%")
	check(not r.offer, "ainda não oferece")
	check(r.golden, "ganha o direito ao Golden")
	var r2 := Ossuary.register_win(Monster.create("teste_bruxo", 12), 12)
	check(r2.offer and r2.golden, "a próxima vitória completa e oferece o Golden")
	var rec := Ossuary.accept("teste_bruxo", 12)
	check(rec.golden, "o recruta é Golden")
	check(Ossuary.entry("teste_bruxo").golden_recruited, "Ossário conta o Golden recrutado")
	check(not Ossuary.entry("teste_bruxo").golden_right, "o direito é usado")


func test_add_to_team_and_ranch() -> void:
	_fresh_save()
	SaveGame.data["party"] = []
	for i in 4:
		check_eq(Ossuary.add_to_team(Monster.create("teste_brigao", 5)), "party", "cabe no time (%d)" % i)
	check_eq(Ossuary.add_to_team(Monster.create("teste_bruxo", 5)), "ranch", "5º vai para o Rancho")
	check_eq(SaveGame.data["ranch"].size(), 1, "Rancho guarda 1")
	# Rancho: cura todos e troca time ↔ rancho
	var hurt := Monster.from_dict(SaveGame.data["party"][0])
	hurt.hp = 1
	SaveGame.data["party"][0] = hurt.to_dict()
	var menu := RanchMenu.new()
	Game.open_overlay(menu)
	await tree.process_frame
	check_eq(int(SaveGame.data["party"][0].hp), Monster.from_dict(SaveGame.data["party"][0]).max_hp(), "Rancho cura")
	menu._on_activated("p:0")
	menu._on_activated("r:0")
	check_eq(str(SaveGame.data["party"][0].species), "teste_bruxo", "troca: o do Rancho entra no time")
	check_eq(str(SaveGame.data["ranch"][0].species), "teste_brigao", "troca: o do time vai para o Rancho")
	menu._on_activated("p:1")
	menu._on_activated("p:1")
	check_eq(SaveGame.data["party"].size(), 3, "guardar no Rancho")
	menu._on_activated("r:0")
	check_eq(SaveGame.data["party"].size(), 4, "levar do Rancho com vaga no time")
	# pela lista (linhas com idade são valor fixo: A ativa, não troca valor)
	var got := [""]
	menu._menu.activated.connect(func(id: String) -> void: got[0] = id, CONNECT_ONE_SHOT)
	menu._menu.index = 1
	menu._menu.activate_current()
	check_eq(got[0], "p:0", "A numa linha do time ativa a escolha")
	menu.close()
	await tree.process_frame
	var oss := OssuaryScreen.new()
	Game.open_overlay(oss)
	await tree.process_frame
	check(oss._ids.size() > 0, "Ossário lista espécies")
	oss.close()
	await tree.process_frame


func test_ceremony_runs() -> void:
	_fresh_save()
	var m := Monster.create("teste_broto_1", 6)
	var known := m.moves.size()
	var c := GrowthCeremony.new().setup(m, Vector2(140, 110))
	Speed.set_debug_multiplier(10.0)
	Game.open_overlay(c)
	var start := Time.get_ticks_msec()
	while is_instance_valid(c) and not c._finished and Time.get_ticks_msec() - start < 30000:
		if c._typing:
			c._text.visible_characters = -1
			c._typing = false
		await tree.process_frame
	Speed.set_debug_multiplier(1.0)
	check(m.species_id == "teste_broto_2", "a cerimônia faz crescer")
	check_eq(m.moves.size(), known + 1, "aprende o golpe do estágio 2")
	check(m.knows("teste_curativo"), "golpe exclusivo aprendido")
	check(Ossuary.entry("teste_broto_2").seen, "nova forma vista no Ossário")
	await tree.process_frame


func test_wilds_spawn_on_map() -> void:
	_fresh_save()
	var map_id := ""
	for f in DirAccess.get_files_at("res://data/maps"):
		if f.ends_with(".json"):
			map_id = f.get_basename()
			break
	var m := MapView.new()
	host.add_child(m)
	m.build(map_id)
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	var before := m.entities.get_child_count()
	var dummy_world := World.new()
	m.add_spawn(dummy_world, {"id": "t", "table": "teste", "x": m.spawn_cell.x, "y": m.spawn_cell.y, "radius": 5, "count": 4}, rng)
	var wilds: Array = m.entities.get_children().filter(func(n: Node) -> bool: return n is WildSkeleton)
	check(wilds.size() > 0, "selvagens de teste nascem no mapa")
	check(m.entities.get_child_count() > before, "entram em entities")
	for w: WildSkeleton in wilds:
		check(not m.is_blocked(w.cell) or m.wild_at(w.cell) == w, "%s em célula livre" % w.species)
		check(m.wild_at(w.cell) == w, "registrado na grade")
		check(Data.species(w.species).size() > 0, "espécie existe")
	# força Golden pelo debug
	DebugDraw.force_golden = true
	var spec := MapView.pick_encounter(Data.encounter_table("teste"), rng)
	DebugDraw.force_golden = false
	check(spec.golden, "Forçar Golden funciona")
	m.queue_free()
	dummy_world.free()
	await tree.process_frame
