extends "res://tests/test_case.gd"
## Fase 6: música (seção 15) — tema por região, temas de batalha, chefe, Rei,
## aniversário e Golden, e a volta da música do mapa depois da batalha.


func test_every_theme_exists() -> void:
	for key in ["title", "credits", "battle", "boss", "king", "birthday", "golden"]:
		var p := Audio.theme(key)
		check(p != "" and ResourceLoader.exists(p), "tema %s existe (%s)" % [key, p])
	var regions: Dictionary = Data.load_json("res://data/regions.json")["regions"]
	for rid in regions:
		var p := str(regions[rid].get("music", ""))
		check(p != "" and ResourceLoader.exists(p), "região %s tem música" % rid)


func test_battle_theme_choice() -> void:
	check_eq(Audio.battle_theme({"kind": "wild", "enemies": [["lenhador_1", 5]]}), Audio.theme("battle"), "selvagem: tema de batalha")
	check_eq(Audio.battle_theme({"kind": "tamer", "enemies": [["lenhador_1", 5]]}), Audio.theme("battle"), "domador: tema de batalha")
	check_eq(Audio.battle_theme({"kind": "boss", "enemies": [["lenhador_2", 22]]}), Audio.theme("boss"), "Guardião: tema de chefe")
	check_eq(Audio.battle_theme({"kind": "boss", "enemies": [["rei_esqueleto", 120]]}), Audio.theme("king"), "Rei: tema próprio")


func test_map_music_loops_and_returns_after_battle() -> void:
	var praia := Audio.theme("title").replace("titulo", "praia")
	Audio.play_music(praia)
	check_eq(Audio.current_music(), praia, "música do mapa")
	check(Audio._music.stream is AudioStreamOggVorbis and Audio._music.stream.loop, "música do mapa em laço")
	Audio.push_music(Audio.theme("battle"))
	check_eq(Audio.current_music(), Audio.theme("battle"), "batalha troca o tema")
	Audio.pop_music()
	check_eq(Audio.current_music(), praia, "depois da batalha, volta a do mapa")
	Audio.stop_music()
