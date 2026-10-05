class_name UnitPanel
extends Control
## Caixa de informação: nome, nível, ícone de tipo, barra de PV animada,
## PV em números (aliados) e selo de veneno.

const W := 116.0
## Espaço do nome (o teste de overflow confere os nomes das espécies).
const NAME_WIDTH := W - 15.0 - 30.0

var monster: Monster
var show_numbers := false
var shown_hp := 0.0
var _name: Label
var _level: Label
var _hp_text: Label
var _type: TextureRect
var _poison: TextureRect


func setup(m: Monster, numbers: bool) -> UnitPanel:
	theme = UiTheme.build()
	show_numbers = numbers
	custom_minimum_size = Vector2(W, 25 if numbers else 21)
	size = custom_minimum_size
	_type = TextureRect.new()
	_type.position = Vector2(4, 4)
	add_child(_type)
	_name = UiTheme.label("")
	_name.position = Vector2(15, 0)
	_name.size = Vector2(NAME_WIDTH, 12)
	_name.clip_text = true
	add_child(_name)
	_level = UiTheme.label("", UiTheme.TEXT_VALUE)
	_level.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_level.position = Vector2(W - 30, 0)
	_level.size = Vector2(27, 12)
	add_child(_level)
	_poison = TextureRect.new()
	_poison.texture = load("res://assets/battle/status_poison.png")
	_poison.position = Vector2(6, 13)
	add_child(_poison)
	_hp_text = UiTheme.label("")
	_hp_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_hp_text.position = Vector2(W - 60, 12)
	_hp_text.size = Vector2(56, 12)
	add_child(_hp_text)
	bind(m)
	return self


func bind(m: Monster) -> void:
	monster = m
	shown_hp = float(m.hp)
	refresh()


func refresh() -> void:
	if monster == null:
		return
	_name.text = monster.display_name()
	_level.text = tr("BTL_LEVEL_SHORT").format({"n": monster.level})
	_type.texture = load("res://assets/battle/type_%s.png" % monster.type())
	_poison.visible = monster.is_poisoned()
	_hp_text.visible = show_numbers
	_hp_text.text = "%d/%d" % [roundi(shown_hp), monster.max_hp()]
	queue_redraw()


func animate_hp(target_hp: int, seconds: float = 0.45) -> void:
	var tw := create_tween()
	tw.tween_method(func(v: float) -> void:
		shown_hp = v
		_hp_text.text = "%d/%d" % [roundi(v), monster.max_hp()]
		queue_redraw(), shown_hp, float(target_hp), seconds)
	await tw.finished
	refresh()


func _draw() -> void:
	var sb := UiTheme.frame("light")
	draw_style_box(sb, Rect2(Vector2.ZERO, size))
	# barra de PV
	var bx := 22.0 if show_numbers else 26.0
	var by := 15.0 if not show_numbers else 15.0
	var bw := (W - 66.0) if show_numbers else (W - 32.0)
	var r := Rect2(bx, by, bw, 4)
	draw_rect(r.grow(1), Color8(40, 30, 48))
	draw_rect(r, Color8(70, 60, 80))
	var ratio := clampf(shown_hp / maxf(1.0, float(monster.max_hp())), 0.0, 1.0)
	var col := Color8(72, 200, 96) if ratio > 0.5 else (Color8(240, 200, 60) if ratio > 0.2 else Color8(226, 70, 70))
	draw_rect(Rect2(r.position, Vector2(bw * ratio, 4)), col)
	draw_rect(Rect2(r.position, Vector2(bw * ratio, 1)), col.lightened(0.35))
