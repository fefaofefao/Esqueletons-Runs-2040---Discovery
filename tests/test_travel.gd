extends "res://tests/test_case.gd"
## Viagem rápida (pedido do Fernando): só cidades já visitadas, chegada na porta
## do Rancho, disponível desde o começo e sem pular a história.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


func _wait(s: float) -> void:
	await tree.create_timer(s, true, false, true).timeout


func test_only_visited_cities() -> void:
	SaveGame.start_new("Téo")
	check_eq(Travel.destinations(), [], "começo do jogo: nenhuma cidade")
	Travel.mark_visited("praia_despertar")
	check_eq(Travel.destinations(), [], "a praia não é cidade")
	Travel.mark_visited("vila_mare")
	check_eq(Travel.destinations(), ["vila_mare"], "Vila Maré depois da visita")
	Travel.mark_visited("vila_mare")
	check_eq(SaveGame.data["visited_cities"].size(), 1, "sem repetir")
	check(not Travel.destinations().has("palmeiral"), "nunca uma cidade à frente na história")


func test_old_saves_by_progress() -> void:
	SaveGame.start_new("Téo")
	SaveGame.set_flag("ramalho_beaten")
	check(Travel.destinations().has("raizal"), "venceu o Ramalho: Raizal liberada mesmo sem registro de visita")
	check(not Travel.destinations().has("brasal"), "Brasal ainda não")
	SaveGame.start_new("Téo")


func test_every_city_has_a_free_arrival() -> void:
	for cid in ["vila_mare", "raizal", "brasal", "brejo", "ossorio", "geada", "palmeiral"]:
		var a := Travel.arrival(cid)
		check_eq(str(a.get("map", "")), cid, "chegada de %s é na própria cidade" % cid)
		var w := World.new()
		host.add_child(w)
		w.load_map(str(a.map), a.cell, "down")
		check_eq(w.player.cell, a.cell, "%s: chega na porta do Rancho (célula livre)" % cid)
		w.queue_free()
	await tree.process_frame


func test_travel_from_pause() -> void:
	SaveGame.start_new("Téo")
	for f in ["intro_done", "bento_met", "has_partner", "partner_lia", "partner_taro", "x_raizal_visto"]:
		SaveGame.set_flag(f)
	var w := World.new()
	host.add_child(w)
	Game.world = w
	w.load_map("vila_mare", Vector2i(19, 26), "up")
	check(Travel.destinations().has("vila_mare"), "entrar na cidade registra a visita")
	var menu := TravelMenu.new()
	Game.open_overlay(menu)
	await tree.process_frame
	var ids: Array = menu._menu.items.map(func(i: Dictionary) -> String: return str(i.id))
	check_eq(ids, ["vila_mare", "_back"], "o menu lista só a Vila Maré (e Voltar)")
	check(not bool(menu._menu.items[0].get("enabled", true)), "a cidade atual aparece apagada")
	Game.close_all_overlays()
	Game.travel_to("palmeiral")
	await _wait(0.1)
	check_eq(w.map_id, "vila_mare", "não viaja para cidade não visitada")
	Travel.mark_visited("raizal")
	Game.travel_to("raizal")
	for i in 60:
		if w.map_id == "raizal" and not Game.transitioning:
			break
		await _wait(0.05)
	Game.close_all_overlays()
	check_eq(w.map_id, "raizal", "viajou para Raizal")
	check_eq(w.player.cell, Vector2i(12, 11), "na porta do Rancho")
	check(not Travel.allowed_here("museu_2040"), "bloqueado nas cenas finais")
	Game.world = null
	w.queue_free()
	SaveGame.start_new("Téo")  # não deixa flags para os próximos testes
	await _wait(0.05)
