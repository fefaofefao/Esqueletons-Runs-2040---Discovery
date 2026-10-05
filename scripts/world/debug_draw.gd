class_name DebugDraw
extends Node2D
## Desenhos de depuração no mapa (só em build de debug): raios de patrulha
## dos NPCs/esqueletos e, a partir da fase 3, áreas das tabelas de encontro.

static var show_radii := false
static var show_encounters := false
## Todos os selvagens que nascerem a partir de agora serão Golden (debug).
static var force_golden := false

var world: World


func _ready() -> void:
	z_index = 50


func _process(_delta: float) -> void:
	if show_radii or show_encounters:
		queue_redraw()


func _draw() -> void:
	if not OS.is_debug_build() or world == null or world.map == null:
		return
	if show_radii:
		for child in world.map.entities.get_children():
			if child is WildSkeleton:
				var w := child as WildSkeleton
				var c := MapView.cell_to_pos(w.home) + Vector2(0, -8)
				draw_arc(c, (w.radius + 0.5) * MapView.T, 0, TAU, 40, Color(1, 0.8, 0.2, 0.9), 1.0)
			if child is Npc:
				var npc := child as Npc
				var r := maxf(npc.patrol_radius(), 0.5) * MapView.T
				draw_arc(npc.position + Vector2(0, -8), r, 0, TAU, 32, Color(1, 0.3, 0.3, 0.8), 1.0)
		if world.player:
			draw_rect(Rect2(Vector2(world.player.cell * MapView.T), Vector2(16, 16)), Color(0.3, 1, 0.3, 0.6), false, 1.0)
	if show_encounters:
		var font := UiTheme.font()
		for sp in world.map.spawns:
			var c := MapView.cell_to_pos(Vector2i(int(sp.get("x", 0)), int(sp.get("y", 0)))) + Vector2(0, -8)
			draw_circle(c, 3, Color(0.3, 0.6, 1, 0.9))
			var y := 0.0
			for e in Data.encounter_table(str(sp.get("table", ""))):
				var line := "%s %d-%d" % [str(e.species), int(e.get("min_level", 0)), int(e.get("max_level", 0))]
				draw_string(font, c + Vector2(6, y), line, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.8, 0.9, 1))
				y += 10
