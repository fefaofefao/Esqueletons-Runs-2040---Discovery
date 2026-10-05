extends "res://tests/test_case.gd"
## Mapas e diálogos: integridade dos dados e regras de colisão/portas.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


func _all_maps() -> Array[String]:
	var out: Array[String] = []
	for f in DirAccess.get_files_at("res://data/maps"):
		if f.ends_with(".json"):
			out.append(f.get_basename())
	return out


func test_maps_build_and_spawn_free() -> void:
	for id in _all_maps():
		var m := MapView.new()
		host.add_child(m)
		check(m.build(id), "%s monta" % id)
		check(m.size.x > 0 and m.size.y > 0, "%s tem tamanho" % id)
		check(not m.is_blocked(m.spawn_cell), "%s: spawn livre" % id)
		for w in m.data.get("warps", []):
			var cell := Vector2i(int(w.x), int(w.y))
			check(not m.is_blocked(cell), "%s: porta em %s acessível" % [id, cell])
			var to := str(w.to)
			if Data.has_map(to):
				var target := Data.map(to)
				var tm := MapView.new()
				host.add_child(tm)
				tm.build(to)
				var tc := Vector2i(int(w.get("tx", -1)), int(w.get("ty", -1)))
				if tc.x >= 0:
					check(not tm.is_blocked(tc), "%s -> %s: chegada %s livre" % [id, to, tc])
					check(tm.warp_at(tc).is_empty(), "%s -> %s: chegada não cai noutra porta" % [id, to])
				check(target.has("region"), "%s tem região" % to)
				tm.free()
			else:
				var known := false
				for r in Data.regions().values():
					if to in r.get("maps", []):
						known = true
				check(known, "%s: porta para '%s', que não é mapa nem mapa planejado" % [id, to])
		m.free()


func test_collision_rules() -> void:
	var m := MapView.new()
	host.add_child(m)
	m.build("praia_despertar")
	check(m.is_blocked(Vector2i(-1, 0)), "fora do mapa bloqueia")
	check(m.is_blocked(Vector2i(10, 28)), "água funda bloqueia")
	check(not m.is_blocked(Vector2i(8, 22)), "píer sobre a água é caminhável")
	check(m.is_blocked(Vector2i(33, 14)), "NPC ocupa a célula")
	check(m.is_blocked(Vector2i(34, 10)), "parede da cabana bloqueia")
	check(not m.is_blocked(Vector2i(35, 10)), "porta da cabana é passável")
	check(not m.interaction_at(Vector2i(22, 3)).is_empty(), "placa interativa")
	m.free()


func test_canonical_mask() -> void:
	check_eq(MapView.canonical_mask(1 | 16), 1, "canto NE some quando há borda N")
	check_eq(MapView.canonical_mask(16), 16, "canto NE sozinho permanece")
	check_eq(MapView.canonical_mask(1 | 2 | 4 | 8 | 255), 15, "todas as bordas")
	var desc := Data.tileset("overworld")
	for ov in desc.overlays:
		for m in range(256):
			var c := MapView.canonical_mask(m)
			if c != 0:
				check(ov.masks.has(str(c)), "overlay %s tem a máscara %d" % [ov.id, c])
				if not ov.masks.has(str(c)):
					return


func test_dialog_references() -> void:
	var keys := all_translations()
	for file in DirAccess.get_files_at("res://data/dialogs"):
		if not file.ends_with(".json"):
			continue
		var d = Data.load_json("res://data/dialogs/" + file)
		for id in d.dialogs.keys():
			for n in d.dialogs[id]:
				for k in ["say", "speaker"]:
					if n.has(k):
						check(keys.has(str(n[k])), "%s/%s: chave %s inexistente" % [file, id, n[k]])
				if n.has("goto"):
					check(not Data.dialog(str(n["goto"])).is_empty(), "%s/%s: goto quebrado" % [file, id])
				for opt in n.get("choice", []):
					check(keys.has(str(opt.text)), "%s/%s: opção sem tradução" % [file, id])
					if opt.has("goto"):
						check(not Data.dialog(str(opt["goto"])).is_empty(), "%s/%s: goto de opção quebrado" % [file, id])
	for id in _all_maps():
		var m := Data.map(id)
		for p in m.get("props", []):
			if p.has("dialog"):
				check(not Data.dialog(str(p.dialog)).is_empty(), "%s: diálogo do objeto %s" % [id, p.type])
		for n in m.get("npcs", []):
			var info := Data.npc(str(n.id))
			check(not info.is_empty(), "%s: NPC %s existe" % [id, n.id])
			for entry in info.get("dialog", []):
				check(not Data.dialog(str(entry.dialog)).is_empty(), "NPC %s: diálogo %s" % [n.id, entry.dialog])


func test_dialog_box_runs_script() -> void:
	SaveGame.start_new("Téo")
	var box := DialogBox.new()
	box.setup(Data.dialog("prologo/bento_rei"))
	Game.open_overlay(box)
	check(Game.top_overlay() == box, "diálogo vira o overlay do topo")
	check(not Game.world_input_enabled(), "diálogo bloqueia o mapa")
	# avança até o fim: A completa a caixa e depois passa para a próxima
	for i in 12:
		if not is_instance_valid(box) or Game.top_overlay() != box:
			break
		box._press()
	check(Game.top_overlay() == null, "diálogo fecha ao terminar")
	check(SaveGame.get_flag("bento_met"), "set_flag do roteiro aplicado")
	var txt := DialogBox.format_text("DLG_P_BENTO_4")
	check(txt.contains("Téo"), "{player} substituído pelo nome")
