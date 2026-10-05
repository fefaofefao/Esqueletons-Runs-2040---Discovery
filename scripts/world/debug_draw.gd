class_name DebugDraw
extends Node2D
## Desenhos de depuração no mapa (só em build de debug): raios de patrulha
## dos NPCs/esqueletos e, a partir da fase 3, áreas das tabelas de encontro.

static var show_radii := false
static var show_encounters := false

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
			if child is Npc:
				var npc := child as Npc
				var r := maxf(npc.patrol_radius(), 0.5) * MapView.T
				draw_arc(npc.position + Vector2(0, -8), r, 0, TAU, 32, Color(1, 0.3, 0.3, 0.8), 1.0)
		if world.player:
			draw_rect(Rect2(Vector2(world.player.cell * MapView.T), Vector2(16, 16)), Color(0.3, 1, 0.3, 0.6), false, 1.0)
	if show_encounters:
		for z in world.map.data.get("encounters", []):
			var r: Array = z.get("rect", [0, 0, 0, 0])
			draw_rect(Rect2(float(r[0]) * 16, float(r[1]) * 16, float(r[2]) * 16, float(r[3]) * 16), Color(0.3, 0.6, 1, 0.8), false, 1.0)
