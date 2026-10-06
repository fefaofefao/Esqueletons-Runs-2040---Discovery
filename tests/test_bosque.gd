extends "res://tests/test_case.gd"
## Fase 4b: Rota 1 com 3 caminhos (Domadores, Selvagem, Túnel) que se
## reencontram; raízes fecham o atalho central até o Guardião perder.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


## Busca em largura sobre células livres; "allow" filtra as células permitidas.
func _reach(m: MapView, from: Vector2i, to: Vector2i, allow: Callable = Callable()) -> bool:
	var seen := {from: true}
	var q: Array[Vector2i] = [from]
	while not q.is_empty():
		var c: Vector2i = q.pop_front()
		if c == to:
			return true
		for d in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
			var n: Vector2i = c + d
			if seen.has(n) or not m.in_bounds(n):
				continue
			if m.is_blocked(n) and m.npc_at(n) == null:
				continue
			if allow.is_valid() and not allow.call(n):
				continue
			seen[n] = true
			q.append(n)
	return false


func _map(id: String) -> MapView:
	var m := MapView.new()
	host.add_child(m)
	check(m.build(id), "%s monta" % id)
	return m


func test_route1_paths() -> void:
	SaveGame.start_new("Téo")
	var m := _map("rota_1")
	var start := Vector2i(19, 47)
	var goal := Vector2i(19, 1)
	check(_reach(m, start, goal), "Rota 1 leva a Raizal")
	check(_reach(m, start, goal, func(c: Vector2i) -> bool: return c.x <= 18 or c.y <= 13 or c.y >= 36),
		"Caminho dos Domadores (oeste) sozinho chega")
	check(_reach(m, start, goal, func(c: Vector2i) -> bool: return c.x >= 21 or c.y <= 13 or c.y >= 36),
		"Campo das Flores (leste) sozinho chega")
	check(not _reach(m, start, Vector2i(19, 25)), "estrada central fechada pelas raízes")
	var warps: Array = m.data.warps.filter(func(w: Dictionary) -> bool: return w.to == "tunel_raizes")
	check_eq(warps.size(), 2, "duas bocas do Túnel")
	check(m.spawns.size() >= 4, "selvagens nos caminhos")
	m.queue_free()
	var t := _map("tunel_raizes")
	check(_reach(t, Vector2i(3, 12), Vector2i(27, 1)), "o Túnel atravessa de ponta a ponta")
	t.queue_free()
	SaveGame.set_flag("ramalho_beaten")
	var m2 := _map("rota_1")
	check(_reach(m2, Vector2i(19, 47), Vector2i(19, 25)), "depois do Ramalho as raízes somem")
	m2.queue_free()
	await tree.process_frame


func test_raizal_city() -> void:
	SaveGame.start_new("Téo")
	var r := _map("raizal")
	var tos: Array = r.data.warps.map(func(w: Dictionary) -> String: return str(w.to))
	for id in ["raizal_rancho", "raizal_loja", "raizal_casa_galho", "raizal_casa_musgo", "raizal_casa_salvia", "bosque_velho", "rota_1"]:
		check(id in tos, "Raizal tem porta para %s" % id)
	var ram := r.npc_at(Vector2i(19, 3))
	check(ram != null and ram.is_tamer_active(), "Ramalho espera na Clareira")
	check(_reach(r, Vector2i(19, 29), Vector2i(19, 4)), "dá para chegar ao Guardião")
	r.queue_free()
	var bv := _map("bosque_velho")
	check(not bv.interaction_at(Vector2i(11, 6)).is_empty(), "Raizerno interativo (brasão)")
	bv.queue_free()
	await tree.process_frame
	# casas de domadores e cidade completa (seção 6): Rancho, Loja e 2 casas
	var tamers := 0
	for id in ["raizal_casa_galho", "raizal_casa_musgo"]:
		var h := _map(id)
		for n in h.all_npcs():
			if not n.info.get("tamer", {}).is_empty():
				tamers += 1
		h.queue_free()
	check_eq(tamers, 2, "2 casas de domadores")
	check(not (Data.load_json("res://data/shops.json").shops.raizal as Array).is_empty(), "Loja de Raizal")
	await tree.process_frame


func test_guardian_team_coherent() -> void:
	var d = Data.dialog("bosque/ramalho")
	var b := {}
	for n in d:
		if str(n.get("action", "")) == "battle":
			b = n
	check(not b.is_empty(), "Ramalho tem batalha")
	var total := 0
	for e in b.enemies:
		var info := Data.species(str(e[0]))
		var gl: Array = info.get("growth_levels", [])
		var st := int(info.get("stage", 1))
		total += int(e[1])
		if gl.size() == 2 and st >= 2:
			check(int(e[1]) >= int(gl[st - 2]), "%s com idade coerente" % e[0])
	# o ás (Troncudo, único) vem mais novo porque tem atributos de único; a média fica perto de 22
	check(abs(total / float(b.enemies.size()) - 22.0) <= 2.0, "idade média do Guardião ~22")
	check_eq(str(b.kind), "boss", "batalha de chefe")
