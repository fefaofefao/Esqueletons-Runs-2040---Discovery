extends Node
## Roteiro de capturas de tela para revisão visual (não entra no jogo).
## Uso: xvfb-run godot --rendering-driver opengl3 res://tools/screenshots/capture.tscn -- --out=/caminho

var out_dir := "user://screens"


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--out="):
			out_dir = a.substr(6)
	DirAccess.make_dir_recursive_absolute(out_dir)
	Settings.path = "user://capture_settings.json"
	SaveGame.save_path = "user://capture_save.json"
	SaveGame.backup_path = "user://capture_save.bak.json"
	SaveGame.delete_save()
	if "--with-save" in OS.get_cmdline_user_args():
		SaveGame.start_new("Téo")
		SaveGame.save_game()
	Settings.set_value("language", "pt_BR")
	Settings.set_value("touch_controls", "off")
	Game.boot(self)
	await _wait(0.75)
	await _shot("00_titulo_intro")
	await _wait(1.6)
	await _shot("01_titulo")
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--region="):
			await _region_shots(a.substr(9))
			get_tree().quit()
			return
	if "--bosque" in OS.get_cmdline_user_args():
		await _bosque_shots()
		get_tree().quit()
		return
	if "--prologo" in OS.get_cmdline_user_args():
		await _prologo_shots()
		get_tree().quit()
		return
	if "--bestiary" in OS.get_cmdline_user_args():
		await _bestiary_shots()
		get_tree().quit()
		return
	if "--phase3" in OS.get_cmdline_user_args():
		await _phase3_shots()
		get_tree().quit()
		return
	if "--battle" in OS.get_cmdline_user_args():
		await _battle_shots()
		get_tree().quit()
		return
	if "--only-title" in OS.get_cmdline_user_args():
		Controls.tap_action("move_down")
		await _wait(0.4)
		await _shot("01b_titulo_selecao")
		Settings.set_value("language", "es")
		await _wait(0.3)
		await _shot("01c_titulo_es")
		Settings.set_value("language", "pt_BR")
		Game.open_overlay(SettingsMenu.new())
		await _wait(0.3)
		await _shot("01d_titulo_config")
		get_tree().quit()
		return
	var entry := NameEntry.new()
	Game.open_overlay(entry)
	await _wait(0.3)
	await _shot("02_nome")
	entry.close()
	Game.start_new_game("Téo")
	await _wait(1.0)
	await _shot("03_praia_spawn")
	await _hold("move_right", 1.6)
	await _hold("move_up", 0.9)
	await _shot("04_praia_andando")
	Game.show_dialog("prologo/bento_primeira")
	await _wait(2.5)
	await _shot("05_dialogo")
	Controls.tap_action("btn_a")
	await _wait(0.2)
	Game.close_all_overlays()
	Settings.set_value("touch_controls", "on")
	await _wait(0.3)
	Game.show_dialog("prologo/bento_repete")
	await _wait(2.0)
	await _shot("06_toque_dialogo")
	Game.close_all_overlays()
	Speed.set_fast(true)
	await _wait(0.2)
	await _shot("07_toque_2x")
	Speed.set_fast(false)
	Settings.set_value("touch_controls", "off")
	Game.open_pause()
	await _wait(0.3)
	await _shot("08_pausa")
	Game.open_overlay(SettingsMenu.new())
	await _wait(0.3)
	await _shot("09_config_pt")
	Settings.set_value("language", "es")
	await _wait(0.3)
	await _shot("10_config_es")
	Settings.set_value("language", "en")
	await _wait(0.3)
	await _shot("11_config_en")
	Settings.set_value("language", "pt_BR")
	Game.close_all_overlays()
	Game.open_debug()
	await _wait(0.3)
	await _shot("12_debug")
	Game.close_all_overlays()
	Game.warp("cabana_bento", Vector2i(6, 8), "up")
	await _wait(1.2)
	await _shot("13_cabana")
	Game.show_dialog("prologo/estante_bento")
	await _wait(3.0)
	await _shot("14_cabana_dialogo")
	Game.close_all_overlays()
	Game.warp("praia_despertar", Vector2i(35, 11), "down")
	await _wait(1.0)
	await _shot("15_praia_cabana")
	Game.open_overlay(AboutScreen.new())
	await _wait(0.3)
	await _shot("16_sobre")
	get_tree().quit()


func _wait(seconds: float) -> void:
	await get_tree().create_timer(seconds, true, false, true).timeout


func _hold(action: String, seconds: float) -> void:
	Controls.emit_action(action, true)
	await _wait(seconds)
	Controls.emit_action(action, false)
	await _wait(0.35)


func _shot(shot_name: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(out_dir.path_join(shot_name + ".png"))
	print("captura: ", shot_name, " ", img.get_size())


func _battle_shots() -> void:
	Game.start_new_game("Téo")
	await _wait(1.0)
	var party := []
	for sp in ["teste_fisico", "teste_magico", "teste_cura", "teste_veneno"]:
		party.append(Monster.create(sp, 12).to_dict())
	SaveGame.data["party"] = party
	SaveGame.data["bag"] = {"pocao_p": 3, "antidoto": 2, "reviver": 1}
	if "--touch" in OS.get_cmdline_user_args():
		Settings.set_value("touch_controls", "on")
	Game.start_battle({"kind": "wild", "seed": 5, "enemies": [["teste_magico", 11], ["teste_veneno", 12]]})
	await _wait(1.0)
	await _shot("b1_intro")
	await _wait(4.0)
	await _shot("b2_anel")
	Controls.tap_action("move_right")
	await _wait(0.3)
	await _shot("b3_anel_itens")
	Controls.tap_action("move_up")
	await _wait(0.2)
	Controls.tap_action("btn_a")
	await _wait(0.4)
	await _shot("b4_golpes")
	Controls.tap_action("move_right")
	await _wait(0.2)
	Controls.tap_action("btn_a")
	await _wait(0.4)
	await _shot("b5_alvo")
	Controls.tap_action("btn_a")
	await _wait(0.5)
	Controls.tap_action("btn_a")
	await _wait(0.3)
	Controls.tap_action("btn_a")
	await _wait(0.3)
	Controls.tap_action("btn_a")
	await _wait(1.3)
	await _shot("b6_rodada")
	await _wait(2.5)
	await _shot("b7_rodada2")
	await _wait(10.0)
	await _shot("b8_depois")
	Game.battle.debug_win()
	await _wait(4.0)
	await _shot("b9_fim")


## Fase 3a: Golden, marcador e recrutamento, aniversário/crescimento, selvagens, Ossário e Rancho.
func _phase3_shots() -> void:
	Game.start_new_game("Téo")
	await _wait(1.0)
	SaveGame.data["party"] = [Monster.create("teste_broto_1", 5).to_dict(), Monster.create("teste_fisico", 12).to_dict()]
	Ossuary.entry("teste_veneno")["marker"] = 75
	Game.start_battle({"kind": "wild", "seed": 3, "enemies": [["teste_magico", 11, true], ["teste_veneno", 6]]})
	await _wait(1.2)
	await _shot("c1_golden_intro")
	await _wait(3.0)
	await _shot("c2_golden_batalha")
	# a vitória dá XP: o Brotinho faz 6 anos e cresce ao voltar ao mapa
	for m in Game.battle.engine.teams[BattleEngine.PLAYER]:
		if m.species_id == "teste_broto_1":
			m.gain_xp(Monster.xp_for_level(6) - m.xp - 2)
	Game.battle.debug_win()
	for i in 14:
		await _wait(0.9)
		if Game.top_overlay() is ChoiceBox:
			await _shot("c3_recrutar")
			Controls.tap_action("btn_a")
			break
		Controls.tap_action("btn_a")
	await _wait(1.5)
	await _shot("c4_recrutou")
	for i in 30:
		await _wait(0.25)
		if Game.top_overlay() is GrowthCeremony:
			break
		Controls.tap_action("btn_a")
	await _wait(2.2)
	await _shot("c5_aniversario")
	await _wait(3.2)
	await _shot("c6_silhuetas")
	await _wait(2.4)
	await _shot("c7_cresceu")
	for i in 20:
		await _wait(0.5)
		if not (Game.top_overlay() is GrowthCeremony):
			break
	var w := Game.world
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	DebugDraw.force_golden = false
	w.map.add_spawn(w, {"id": "cap", "table": "teste", "x": w.player.cell.x, "y": w.player.cell.y, "radius": 5, "count": 5}, rng)
	DebugDraw.show_radii = true
	await _wait(1.5)
	await _shot("c8_selvagens")
	DebugDraw.show_radii = false
	Game.open_overlay(OssuaryScreen.new())
	await _wait(0.4)
	await _shot("c9_ossario")
	Game.close_all_overlays()
	Game.open_overlay(RanchMenu.new())
	await _wait(0.4)
	await _shot("c10_rancho")


## Fase 3b: Ossário com espécies reais, fichas e selvagens reais no mapa.
func _bestiary_shots() -> void:
	Game.start_new_game("Téo")
	await _wait(1.0)
	var ids := Data.all_species_ids(false)
	for i in ids.size():
		var e := Ossuary.entry(ids[i])
		e["seen"] = i % 5 != 4
		e["defeated"] = i % 3 == 0
		e["recruited"] = i % 4 == 0
		e["marker"] = (i * 37) % 100
	Ossuary.entry("faroleira_3")["golden_recruited"] = true
	var oss := OssuaryScreen.new()
	Game.open_overlay(oss)
	await _wait(0.4)
	await _shot("d1_ossario")
	for id in ["grumete_1", "faroleira_3", "palafiteiro_3", "rei_esqueleto"]:
		Ossuary.entry(id)["seen"] = true
		var en := OssuaryEntry.new().setup(id, int(Data.species(id).get("number", 0)))
		Game.open_overlay(en)
		await _wait(0.5)
		await _shot("d2_ficha_" + id)
		en.close()
		await _wait(0.2)
	Game.close_all_overlays()
	var w := Game.world
	var rng := RandomNumberGenerator.new()
	rng.seed = 4
	var table := []
	for id in ["grumete_1", "faroleira_1", "marisqueiro_1", "rendeira_1", "lenhador_2", "mineiro_3", "domador_escorpioes_3"]:
		table.append({"species": id, "min_level": 5, "max_level": 5})
	Data.encounter_overrides["_cap"] = table
	w.map.add_spawn(w, {"id": "cap", "table": "_cap", "x": w.player.cell.x, "y": w.player.cell.y, "radius": 5, "count": 7}, rng)
	await _wait(1.2)
	await _shot("d3_selvagens_reais")
	var taro := Monster.create("grumete_2", 24)
	taro.nickname = "Taro"
	var lia := Monster.create("faroleira_2", 24)
	lia.nickname = "Lia"
	SaveGame.data["party"] = [taro.to_dict(), lia.to_dict(), Monster.create("lenhador_2", 22).to_dict()]
	Game.start_battle({"kind": "wild", "seed": 9, "enemies": [["mineiro_2", 25], ["gasista_1", 22, true]]})
	await _wait(5.5)
	await _shot("d4_batalha_real")
	Controls.tap_action("btn_a")
	await _wait(0.4)
	Controls.tap_action("move_right")
	await _wait(0.3)
	await _shot("d5_golpes_reais")


## Avança diálogos (A) até não haver overlay; escolhe as opções na ordem dada.
## Tira uma foto no passo "shot_at" (contando caixas de fala).
func _advance(choices: Array = [], shot_name: String = "", shot_at: int = -1, max_steps: int = 60) -> void:
	var n := 0
	for i in max_steps:
		await _wait(0.25)
		var top := Game.top_overlay()
		if top == null:
			if Game.battle == null and not Game.transitioning:
				return
			continue
		if top is DialogBox:
			var box := top as DialogBox
			if box._typing:
				box._press()
				await _wait(0.1)
			if n == shot_at and shot_name != "":
				await _shot(shot_name)
			if box._waiting_choice and box._choice:
				box._choice.index = int(choices.pop_front()) if not choices.is_empty() else 0
				box._choice.refresh()
				await _wait(0.3)
				box._choice.activate_current()
			else:
				box._press()
			n += 1


func _goto(map_id: String, cell: Vector2i, facing: String) -> void:
	await Game.warp(map_id, cell, facing)
	await _wait(0.6)


func _prologo_shots() -> void:
	Game.start_new_game("Téo")
	await _wait(1.6)
	await _shot("p1_despertar")
	await _advance()
	await _goto("praia_despertar", Vector2i(32, 14), "right")
	Game.world.interact(Vector2i(33, 14), Vector2i.RIGHT)
	await _advance([1], "p2_bento", 2)
	Game.warp("cabana_bento", Vector2i(6, 8), "up")  # a cena de entrada espera o diálogo
	await _wait(1.6)
	await _advance([0], "p3_escolha", 6)
	await _shot("p4_depois_escolha")
	await _goto("praia_despertar", Vector2i(14, 13), "down")
	await _wait(1.0)
	await _shot("p5_praia_selvagens")
	var w := Game.world
	var wild: WildSkeleton = null
	for c in w.map.entities.get_children():
		if c is WildSkeleton:
			wild = c
	if wild:
		w.on_touch_wild(wild)
		await _wait(5.0)
		await _shot("p6_dica_batalha")
		Game.battle.debug_win()
		await _advance([], "p7_marcador", 6, 120)
	await _goto("vila_mare", Vector2i(19, 26), "up")
	await _wait(1.2)
	await _shot("p8_vila")
	await _goto("vila_mare", Vector2i(19, 14), "up")
	await _shot("p9_praca")
	await _goto("vila_rancho", Vector2i(7, 4), "up")
	Game.world.interact(Vector2i(7, 3), Vector2i.UP)
	await _advance([1], "p10_marola", 1)
	await _goto("vila_loja", Vector2i(6, 4), "up")
	SaveGame.data["money"] = 500
	Game.world.interact(Vector2i(6, 3), Vector2i.UP)
	await _wait(1.0)
	Controls.tap_action("btn_a")
	await _wait(0.8)
	await _shot("p11_loja")
	Game.close_all_overlays()
	await _wait(0.4)
	await _goto("vila_mare", Vector2i(19, 9), "up")
	await _wait(2.5)
	await _shot("p12_bras")
	Game.open_overlay(TeamMenu.new())
	await _wait(0.4)
	await _shot("p13_equipe")


func _bosque_shots() -> void:
	Game.start_new_game("Téo")
	await _wait(1.0)
	await _advance()
	for f in ["intro_done", "bento_met", "has_partner", "partner_lia", "tut_battle", "tut_marker", "bras_beaten"]:
		SaveGame.set_flag(f)
	var lia := Monster.create("faroleira_2", 20)
	lia.nickname = "Lia"
	SaveGame.data["party"] = [lia.to_dict(), Monster.create("lenhador_2", 20).to_dict(), Monster.create("rendeira_2", 19).to_dict()]
	await _goto("rota_1", Vector2i(19, 43), "up")
	await _wait(1.0)
	await _shot("b1_rota_bifurcacao")
	await _goto("rota_1", Vector2i(31, 28), "up")
	await _shot("b2_campo_flores")
	Game.warp("tunel_raizes", Vector2i(3, 12), "up")
	await _wait(1.6)
	await _advance([], "b3_tunel_lia", 1)
	await _goto("tunel_raizes", Vector2i(12, 10), "up")
	await _shot("b4_tunel_dentro")
	await _goto("raizal", Vector2i(19, 22), "up")
	await _wait(0.8)
	await _shot("b5_raizal")
	await _goto("raizal", Vector2i(19, 7), "up")
	await _wait(0.3)
	Game.world.player.try_move(Vector2i.UP)
	await _wait(2.5)
	await _shot("b6_ramalho_ve")
	await _advance([], "b7_ramalho_fala", 1)
	await _wait(1.0)
	if Game.battle:
		await _wait(4.0)
		await _shot("b8_ramalho_batalha")
		Game.battle.debug_win()
		await _advance([], "", -1, 160)
	await _goto("bosque_velho", Vector2i(12, 7), "up")
	await _wait(0.6)
	Game.world.interact(Vector2i(12, 6), Vector2i.UP)
	await _advance([1], "b9_raizerno_brasao", 1)


## Capturas por região, descritas em tools/screenshots/regions.json:
## {"<região>": {"flags": [...], "party": [[espécie, idade, apelido?]], "steps": [
##    {"map", "x", "y", "f", "shot", "interact": [x, y]?, "choices": [...]?, "shot_at": n?,
##     "step": "up"?, "battle": true?, "wait": s?}]}}
func _region_shots(rid: String) -> void:
	var all = Data.load_json("res://tools/screenshots/regions.json")
	var cfg: Dictionary = all.get(rid, {})
	Game.start_new_game("Téo")
	await _wait(1.0)
	await _advance()
	for f in cfg.get("flags", []):
		SaveGame.set_flag(str(f))
	var party := []
	for e in cfg.get("party", []):
		var m := Monster.create(str(e[0]), int(e[1]))
		if e.size() > 2:
			m.nickname = str(e[2])
		party.append(m.to_dict())
	if not party.is_empty():
		SaveGame.data["party"] = party
	for st in cfg.get("steps", []):
		for f in st.get("flags", []):
			SaveGame.set_flag(str(f))
		if st.get("no_wait_warp", false):
			Game.warp(str(st.map), Vector2i(int(st.x), int(st.y)), str(st.get("f", "up")))
			await _wait(1.6)
		else:
			await _goto(str(st.map), Vector2i(int(st.x), int(st.y)), str(st.get("f", "up")))
		await _wait(float(st.get("wait", 0.4)))
		if st.has("step"):
			Game.world.player.try_move({"up": Vector2i.UP, "down": Vector2i.DOWN, "left": Vector2i.LEFT, "right": Vector2i.RIGHT}[str(st.step)])
			await _wait(2.5)
		if st.has("interact"):
			var c := Vector2i(int(st.interact[0]), int(st.interact[1]))
			Game.world.interact(c, c - Game.world.player.cell)
		if st.has("interact") or st.has("step") or st.get("no_wait_warp", false):
			await _advance(st.get("choices", []).duplicate(), str(st.get("shot", "")), int(st.get("shot_at", 0)), 40)
			if st.get("battle", false) and Game.battle:
				await _wait(4.0)
				await _shot(str(st.shot) + "_batalha")
				Game.battle.debug_win()
				await _advance(st.get("after_choices", []).duplicate(), str(st.get("after_shot", "")), int(st.get("after_shot_at", 0)), 160)
		else:
			await _shot(str(st.shot))
