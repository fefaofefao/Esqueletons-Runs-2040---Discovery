class_name TimelineBar
extends Control
## Timeline de turnos no topo: rostinhos de quem age, na ordem prevista da rodada.
## Azul = aliado, vermelho = inimigo; quem está agindo fica destacado.

const CHIP := Vector2(18, 16)
const GAP := 7.0

var _entries: Array = []  # [{monster, view}]
var _current := -1
var _done := {}


func set_order(order: Array, views: Dictionary) -> void:
	_entries = []
	for m in order:
		_entries.append({"m": m, "view": views.get(m.uid)})
	_current = -1
	_done = {}
	var w := _entries.size() * CHIP.x + maxf(0, _entries.size() - 1) * GAP
	custom_minimum_size = Vector2(w + 8, CHIP.y + 6)
	size = custom_minimum_size
	queue_redraw()


func set_current(uid: int) -> void:
	for i in _entries.size():
		if _entries[i].m.uid == uid:
			if _current >= 0:
				_done[_current] = true
			_current = i
	queue_redraw()


func _draw() -> void:
	if _entries.is_empty():
		return
	draw_style_box(UiTheme.frame("dark"), Rect2(Vector2.ZERO, size))
	for i in _entries.size():
		var e: Dictionary = _entries[i]
		var m: Monster = e.m
		var x := 4.0 + i * (CHIP.x + GAP)
		var r := Rect2(Vector2(x, 3), CHIP)
		var ally := m.side == BattleEngine.PLAYER
		var border := Color8(90, 170, 255) if ally else Color8(240, 90, 90)
		if i == _current:
			border = Color8(255, 220, 90)
			draw_rect(r.grow(2), Color(1, 0.86, 0.35, 0.45))
		draw_rect(r, Color8(28, 24, 44))
		var v: UnitView = e.view
		if v:
			draw_texture_rect_region(v.sprite.texture, Rect2(r.position + Vector2(1, 1), Vector2(16, 14)), v.head_region(),
				Color(1, 1, 1, 0.45) if (_done.has(i) or m.is_fainted()) else Color.WHITE)
		draw_rect(r, border, false, 1.0)
		if i < _entries.size() - 1:
			var ax := x + CHIP.x + 1.5
			draw_colored_polygon(PackedVector2Array([Vector2(ax, 8), Vector2(ax + 3, 11), Vector2(ax, 14)]), Color8(200, 200, 220))
