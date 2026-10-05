class_name UnitCard
extends Control
## Carta do esqueleto na base da tela: nome, tipo, idade, PV (barra animada;
## números para os aliados), veneno, destaque de quem age e de Sintonia.

const W := 79.0
const H := 40.0
## Espaço do nome (o teste de overflow confere os nomes das espécies).
const NAME_WIDTH := W - 14.0

var monster: Monster
var ally := true
var shown_hp := 0.0
var acting := false
var synced := false
## Marcador de recrutamento (0–100) mostrado nos inimigos selvagens; -1 = esconder.
var marker := -1
var _name: Label
var _age: Label
var _hp_text: Label
var _type: TextureRect
var _poison: TextureRect
var _t := 0.0


func setup(m: Monster, is_ally: bool) -> UnitCard:
	theme = UiTheme.build()
	ally = is_ally
	size = Vector2(W, H)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_name = UiTheme.label("", UiTheme.TEXT_LIGHT if not ally else UiTheme.TEXT_DARK)
	_name.position = Vector2(7, 2)
	_name.size = Vector2(NAME_WIDTH, 12)
	_name.clip_text = true
	add_child(_name)
	_type = TextureRect.new()
	_type.position = Vector2(7, 16)
	add_child(_type)
	_age = UiTheme.label("", UiTheme.TEXT_VALUE if ally else Color8(255, 214, 140))
	_age.position = Vector2(18, 13)
	add_child(_age)
	_poison = TextureRect.new()
	_poison.texture = load("res://assets/battle/status_poison.png")
	_poison.position = Vector2(W - 15, 14)
	add_child(_poison)
	_hp_text = UiTheme.label("", UiTheme.TEXT_DARK)
	_hp_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_hp_text.position = Vector2(W - 44, 25)
	_hp_text.size = Vector2(38, 12)
	add_child(_hp_text)
	bind(m)
	return self


func bind(m: Monster) -> void:
	monster = m
	shown_hp = float(m.hp)
	refresh()


static func age_text(n: int) -> String:
	return TranslationServer.translate("BTL_AGE_ONE") if n == 1 else TranslationServer.translate("BTL_AGE").format({"n": n})


func refresh() -> void:
	if monster == null:
		return
	_name.text = ("★" if monster.golden else "") + monster.display_name()
	_name.add_theme_color_override("font_color", Color8(255, 210, 90) if monster.golden else (UiTheme.TEXT_DARK if ally else UiTheme.TEXT_LIGHT))
	_age.text = age_text(monster.level)
	_type.texture = load("res://assets/battle/type_%s.png" % monster.type())
	_poison.visible = monster.is_poisoned()
	_hp_text.visible = ally
	_hp_text.text = "%d/%d" % [roundi(shown_hp), monster.max_hp()]
	queue_redraw()


func set_acting(on: bool, sintonia: bool = false) -> void:
	acting = on
	synced = sintonia
	queue_redraw()


func animate_hp(target_hp: int, seconds: float = 0.45) -> void:
	var tw := create_tween()
	tw.tween_method(func(v: float) -> void:
		shown_hp = v
		_hp_text.text = "%d/%d" % [roundi(v), monster.max_hp()]
		queue_redraw(), shown_hp, float(target_hp), seconds)
	await tw.finished
	refresh()


func _process(delta: float) -> void:
	_t += delta
	if acting:
		queue_redraw()


func _draw() -> void:
	var r := Rect2(Vector2.ZERO, size)
	draw_style_box(UiTheme.frame("light" if ally else "dark"), r)
	if acting:
		var a := 0.55 + 0.35 * sin(_t * 7.0)
		var col := Color(0.35, 0.95, 1.0, a) if synced else Color(1.0, 0.82, 0.3, a)
		draw_rect(r.grow(-1), col, false, 2.0)
	var bw := (W - 54.0) if ally else (W - 14.0)
	var bar := Rect2(7, 29, bw, 4)
	if marker >= 0:
		var mr := Rect2(7, 35, W - 14.0, 2)
		draw_rect(mr, Color8(60, 40, 80))
		draw_rect(Rect2(mr.position, Vector2(mr.size.x * marker / 100.0, 2)), Color8(230, 220, 255))
	draw_rect(bar.grow(1), Color8(40, 30, 48))
	draw_rect(bar, Color8(70, 60, 80))
	var ratio := clampf(shown_hp / maxf(1.0, float(monster.max_hp())), 0.0, 1.0)
	var col2 := Color8(72, 200, 96) if ratio > 0.5 else (Color8(240, 200, 60) if ratio > 0.2 else Color8(226, 70, 70))
	draw_rect(Rect2(bar.position, Vector2(bw * ratio, 4)), col2)
	draw_rect(Rect2(bar.position, Vector2(bw * ratio, 1)), col2.lightened(0.35))
