extends "res://tests/test_case.gd"
## Save versionado: gravação, leitura, backup, arquivo corrompido e migração.


func test_round_trip() -> void:
	SaveGame.delete_save()
	SaveGame.start_new("Téo")
	SaveGame.set_position("praia_despertar", "praia", Vector2i(7, 9), "left")
	SaveGame.set_flag("bento_met")
	check(SaveGame.save_game(), "save_game retorna true")
	SaveGame.data = {}
	check(SaveGame.load_game(), "load_game retorna true")
	check_eq(SaveGame.player_name(), "Téo", "nome com acento preservado")
	check_eq(int(SaveGame.data.player.x), 7, "posição x")
	check_eq(int(SaveGame.data.player.y), 9, "posição y")
	check_eq(str(SaveGame.data.player.facing), "left", "direção")
	check(SaveGame.get_flag("bento_met"), "flag preservada")
	check_eq(int(SaveGame.data.version), SaveGame.VERSION, "versão atual gravada")


func test_backup_and_corruption() -> void:
	SaveGame.delete_save()
	SaveGame.start_new("Ana")
	SaveGame.save_game()
	SaveGame.data.player.name = "Bia"
	SaveGame.save_game()
	check(FileAccess.file_exists(SaveGame.backup_path), "o save anterior vira backup")
	# corrompe o principal: deve cair no backup ("Ana")
	var f := FileAccess.open(SaveGame.save_path, FileAccess.WRITE)
	f.store_string("{ isso não é json")
	f.close()
	SaveGame.data = {}
	check(SaveGame.load_game(), "carrega mesmo com o principal corrompido")
	check_eq(SaveGame.player_name(), "Ana", "usa o backup")
	SaveGame.delete_save()
	check(not SaveGame.has_save(), "delete_save apaga tudo")


func test_migration_from_v0() -> void:
	var old := {"name": "Rui", "map": "cabana_bento", "x": 3, "y": 4, "flags": {"x": true}}
	var d := SaveGame.migrate(old)
	check_eq(int(d.version), SaveGame.VERSION, "migra até a versão atual")
	check_eq(str(d.player.name), "Rui", "nome migrado")
	check_eq(str(d.player.map), "cabana_bento", "mapa migrado")
	check_eq(int(d.player.x), 3, "x migrado")
	check(d.has("party") and d.has("ossuary") and d.has("play_time"), "chaves novas criadas")
	check(bool(d.flags.get("x", false)), "flags migradas")


func test_play_time_by_region() -> void:
	SaveGame.start_new("Téo")
	SaveGame.set_position("praia_despertar", "praia", Vector2i(1, 1), "down")
	SaveGame.tracking = true
	var old_scale := Engine.time_scale
	Engine.time_scale = 2.0
	SaveGame._process(1.0)
	Engine.time_scale = old_scale
	SaveGame.tracking = false
	var t: Dictionary = SaveGame.region_times()["praia"]
	check(is_equal_approx(float(t.game), 1.0), "tempo de jogo (equivalente a 1x) conta o delta escalado")
	check(is_equal_approx(float(t.real), 0.5), "tempo real desconta o 2x")


func test_migration_single_partner_to_list() -> void:
	var old := {"version": 1, "player": {"name": "Rui"}, "partner_uid": 7,
		"party": [{"uid": 7, "species": "faroleira_2", "nickname": "Lia", "level": 30}, {"uid": 9, "species": "lenhador_1", "level": 20}]}
	var d := SaveGame.migrate(old)
	check_eq(int(d.version), SaveGame.VERSION, "migra até a versão atual")
	check(not d.has("partner_uid"), "parceiro único sai")
	check_eq(d.partner_uids, [7], "vira lista de parceiros")
	check(bool(d.party[0].get("starter", false)), "parceiro antigo ganha o bônus de inicial")
	check(not bool(d.party[1].get("starter", false)), "os outros não")
