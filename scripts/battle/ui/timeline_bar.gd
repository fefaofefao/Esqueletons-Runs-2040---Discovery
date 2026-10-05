class_name TimelineBar
extends Control
## Timeline das próximas ações (turnos por tempo). O 1º é quem age agora.
## Azul = aliado, vermelho = inimigo. Um elo ciano liga dois aliados (ou dois
## inimigos) seguidos: é a Sintonia. Durante a escolha de golpe, a timeline
## já mostra onde o próximo turno de quem age vai cair (fantasma tracejado).

const CHIP := Vector2(18, 16)
const GAP := 4.0

var _order: Array = []
var _views: Dictionary = {}
var _ghost_uid := -1
var _ghost_index := -1


func _init() -> void:
	theme = UiTheme.build()


func set_order(order: Array, views: Dictionary, ghost_uid: int = -1) -> void:
	_order = order
	_views = views
	_ghost_uid = ghost_uid
	_ghost_index = -1
	if ghost_uid >= 0:
		for i in range(1, order.size()):
			if order[i].uid == ghost_uid:
				_ghost_index = i
				break
	var w := order.size() * CHIP.x + maxf(0, order.size() - 1) * GAP + 10
	custom_minimum_size = Vector2(w, CHIP.y + 6)
	size = custom_minimum_size
	queue_redraw()


func _draw() -> void:
	if _order.is_empty():
		return
	draw_style_box(UiTheme.frame("dark"), Rect2(Vector2.ZERO, size))
	for i in _order.size():
		var m: Monster = _order[i]
		var x := 5.0 + i * (CHIP.x + GAP)
		var r := Rect2(Vector2(x, 3), CHIP)
		var ally := m.side == BattleEngine.PLAYER
		var border := Color8(90, 170, 255) if ally else Color8(240, 90, 90)
		# elo de Sintonia com o anterior
		if i > 0 and _order[i - 1].side == m.side and _order[i - 1].uid != m.uid:
			draw_line(Vector2(x - GAP - 1, 11), Vector2(x + 1, 11), Color8(90, 240, 255), 2.0)
		if i == 0:
			draw_rect(r.grow(2), Color(1, 0.86, 0.35, 0.6))
			border = Color8(255, 220, 90)
		draw_rect(r, Color8(28, 24, 44))
		var v: UnitView = _views.get(m.uid)
		if v:
			draw_texture_rect_region(v.sprite.texture, Rect2(r.position + Vector2(1, 1), Vector2(16, 14)), v.head_region(), Color.WHITE)
		draw_rect(r, border, false, 1.0)
		if i == _ghost_index:
			# fantasma: próximo turno de quem está escolhendo
			for k in range(0, 18, 4):
				draw_line(Vector2(x + k, 1), Vector2(x + minf(k + 2, 18), 1), Color8(255, 240, 160), 1.0)
				draw_line(Vector2(x + k, 20), Vector2(x + minf(k + 2, 18), 20), Color8(255, 240, 160), 1.0)
