extends "res://tests/test_case.gd"
## Fumaça da tela de batalha: joga batalhas completas pela interface (escolhendo
## sempre a 1ª opção) e confere que terminam, que a equipe volta atualizada e
## que trocas forçadas e aprendizado de golpes não travam.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


func _play(info: Dictionary, team: Array, by_tap: bool = false) -> String:
	var bag := {"pocao_p": 2}
	var screen := BattleScreen.new().setup(info, team, bag)
	host.add_child(screen)
	var result := [""]
	screen.finished.connect(func(r: String) -> void: result[0] = r)
	Speed.set_debug_multiplier(10.0)
	var start := Time.get_ticks_msec()
	while result[0] == "" and Time.get_ticks_msec() - start < 60000:
		await tree.process_frame
		match screen.state:
			"ring":
				screen._on_ring_chosen("moves")
			"moves":
				screen._choose_move()
			"target":
				screen._confirm_target()
			"list":
				# pelo mesmo caminho do botão A / toque (MenuList), não direto no callback:
				# assim pega listas em que o A muda um valor em vez de escolher (bug do celular)
				for i in screen._list.items.size():
					if screen._list.items[i].get("enabled", true) and screen._list.items[i].id != "_back":
						if by_tap:
							# toque na linha, como no celular (na batalha não há botões A/B na tela)
							var ev := InputEventMouseButton.new()
							ev.button_index = MOUSE_BUTTON_LEFT
							ev.pressed = true
							screen._list._on_row_input(ev, i)
						else:
							screen._list.index = i
							screen._list.activate_current()
						break
			_:
				screen._log.skip()
	Speed.set_debug_multiplier(1.0)
	screen.queue_free()
	await tree.process_frame
	return result[0]


func test_wild_battle_completes() -> void:
	var team := [Monster.create("teste_fisico", 20), Monster.create("teste_magico", 20)]
	var r := await _play({"kind": "wild", "seed": 3, "enemies": [["teste_veneno", 8], ["teste_cura", 8]]}, team)
	check_eq(r, "win", "vence selvagens fracos")
	check(team[0].xp > Monster.xp_for_level(20) or team[1].xp > Monster.xp_for_level(20), "XP aplicado à equipe")


func test_tamer_with_reserves_and_replacement() -> void:
	var team := [Monster.create("teste_cura", 6), Monster.create("teste_veneno", 6), Monster.create("teste_fisico", 14)]
	var r := await _play({"kind": "tamer", "seed": 9, "tamer_key": "DBG_TAMER_NAME", "reward": 0,
		"enemies": [["teste_fisico", 13], ["teste_magico", 13], ["teste_veneno", 12]]}, team)
	check(r in ["win", "lose"], "batalha de domador termina (%s)" % r)


func test_forced_replacement_is_selectable() -> void:
	# o primeiro desmaia logo: a lista "Quem entra no lugar?" precisa aceitar o A
	var team := [Monster.create("teste_cura", 2), Monster.create("teste_fisico", 30), Monster.create("teste_magico", 30)]
	var r := await _play({"kind": "tamer", "seed": 4, "tamer_key": "DBG_TAMER_NAME", "reward": 0,
		"enemies": [["teste_fisico", 25], ["teste_magico", 25]]}, team)
	check(r in ["win", "lose"], "a troca forçada é escolhida e a batalha termina (%s)" % r)
	check(team[0].is_fainted(), "o fraco desmaiou (houve troca forçada)")


func test_forced_replacement_by_tap() -> void:
	# a mesma troca forçada, escolhendo com um toque na linha (sem botão A na tela)
	var team := [Monster.create("teste_cura", 2), Monster.create("teste_fisico", 30), Monster.create("teste_magico", 30)]
	var r := await _play({"kind": "tamer", "seed": 4, "tamer_key": "DBG_TAMER_NAME", "reward": 0,
		"enemies": [["teste_fisico", 25], ["teste_magico", 25]]}, team, true)
	check(r in ["win", "lose"], "um toque escolhe quem entra e a batalha termina (%s)" % r)
	check(team[0].is_fainted(), "houve troca forçada")


func test_defeat_ends() -> void:
	var team := [Monster.create("teste_cura", 2)]
	var r := await _play({"kind": "boss", "seed": 1, "enemies": [["teste_fisico", 30], ["teste_magico", 30]]}, team)
	check_eq(r, "lose", "derrota termina a batalha")


func test_level_up_learn_prompt_does_not_block() -> void:
	# nível 13 -> 14 aprende "Pancada" com 4 golpes já conhecidos: abre a escolha
	var m := Monster.create("teste_fisico", 13)
	while m.moves.size() < 4:
		m.moves.append({"id": "teste_faisca", "pp": 30})
	m.xp = Monster.xp_for_level(14) - 1
	var r := await _play({"kind": "wild", "seed": 2, "enemies": [["teste_cura", 5]]}, [m])
	check_eq(r, "win", "vence")
	check(m.level >= 14, "subiu de nível")
