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
