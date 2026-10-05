extends Node
## Revisão de mapas: renderiza cada mapa inteiro (com NPCs, objetos, portas e as
## zonas dos selvagens marcadas) num PNG em escala 1:1. Não entra no jogo.
## Uso: xvfb-run godot --rendering-driver opengl3 res://tools/screenshots/map_sheet.tscn -- --out=/caminho [--maps=a,b]

var out_dir := "user://maps"


func _ready() -> void:
	var only := []
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--out="):
			out_dir = a.substr(6)
		elif a.begins_with("--maps="):
			only = a.substr(7).split(",")
	DirAccess.make_dir_recursive_absolute(out_dir)
	SaveGame.start_new("Téo")
	var ids := []
	for f in DirAccess.get_files_at("res://data/maps"):
		if f.ends_with(".json"):
			ids.append(f.get_basename())
	ids.sort()
	for id in ids:
		if not only.is_empty() and not only.has(id):
			continue
		await _render(id)
	get_tree().quit()


func _render(id: String) -> void:
	var vp := SubViewport.new()
	vp.transparent_bg = false
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(vp)
	var map := MapView.new()
	vp.add_child(map)
	if not map.build(id):
		vp.queue_free()
		return
	vp.size = Vector2i(map.pixel_size())
	# zonas de selvagens: círculo com o raio de patrulha e a faixa de idade
	var enc: Dictionary = Data.load_json("res://data/encounters.json").get("tables", {})
	for sp in map.spawns:
		var c := Vector2(int(sp.get("x", 0)) * 16 + 8, int(sp.get("y", 0)) * 16 + 8)
		var mark := _Zone.new()
		mark.position = c
		mark.radius = float(sp.get("radius", 2)) * 16.0 + 8.0
		var lv := []
		for e in enc.get(str(sp.get("table", "")), []):
			lv.append_array([int(e.min_level), int(e.max_level)])
		mark.label = "%s %d-%d" % [str(sp.get("table", "")), lv.min() if lv else 0, lv.max() if lv else 0]
		map.add_child(mark)
	for i in 4:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	img.save_png("%s/%s.png" % [out_dir, id])
	print("mapa: %s %dx%d" % [id, vp.size.x, vp.size.y])
	vp.queue_free()


class _Zone extends Node2D:
	var radius := 32.0
	var label := ""

	func _ready() -> void:
		z_index = 50

	func _draw() -> void:
		draw_circle(Vector2.ZERO, radius, Color(1, 0.2, 0.2, 0.18))
		draw_arc(Vector2.ZERO, radius, 0, TAU, 32, Color(1, 0.2, 0.2, 0.8), 1.0)
		draw_string(ThemeDB.fallback_font, Vector2(-radius, -radius - 2), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 8, Color.WHITE)
