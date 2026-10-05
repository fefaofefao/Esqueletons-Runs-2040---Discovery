class_name UnitView
extends Node2D
## Esqueleto em campo (arena lateral): sprite 32x32 em escala 2, aliados virados
## para a direita e inimigos espelhados; sombra e animações (entrada, ataque, dano,
## queda, seleção).

const SCALE := 2.0

var monster: Monster
var is_enemy := false
var home := Vector2.ZERO
var sprite: Sprite2D
var _marker: Label
var _shadow: Sprite2D
var _bob := 0.0


func setup(m: Monster, enemy: bool) -> UnitView:
	monster = m
	is_enemy = enemy
	_shadow = Sprite2D.new()
	_shadow.texture = load("res://assets/sprites/shadow.png")
	_shadow.scale = Vector2(2.4, 1.6)
	_shadow.position = Vector2(0, -2)
	add_child(_shadow)
	sprite = Sprite2D.new()
	var tex: Texture2D = load(str(m.info().get("sprite", "res://assets/battle/dummy_fisico.png")))
	sprite.texture = tex
	sprite.region_enabled = true
	# folha: quadro de batalha virado para a direita; o inimigo é espelhado
	sprite.region_rect = Rect2(0, 0, 32, 32)
	sprite.flip_h = enemy
	sprite.centered = false
	sprite.scale = Vector2(SCALE, SCALE)
	sprite.offset = Vector2(-16, -32)
	add_child(sprite)
	if m.golden:
		GoldenFX.apply(sprite, Vector2(16, 16), Vector2(12, 14))
	_marker = UiTheme.label("▼", UiTheme.TEXT_ACCENT)
	_marker.add_theme_color_override("font_outline_color", Color(1, 1, 1))
	_marker.position = Vector2(-3, -76)
	_marker.visible = false
	add_child(_marker)
	return self


func set_selected(on: bool) -> void:
	_marker.visible = on
	if not on:
		sprite.modulate = Color.WHITE


func _process(delta: float) -> void:
	_bob += delta
	if _marker.visible:
		_marker.position.y = -76 + round(sin(_bob * 8.0) * 2.0)
		sprite.modulate = Color(1, 1, 1).lerp(Color(1.25, 1.25, 1.25), 0.5 + 0.5 * sin(_bob * 10.0))
	elif monster and not monster.is_fainted() and sprite.position == Vector2.ZERO:
		# respiração leve
		sprite.scale.y = SCALE * (1.0 + 0.012 * sin(_bob * 2.4 + float(monster.uid)))


func head_region() -> Rect2:
	return Rect2(8, 1, 16, 14)


func enter(from_left: bool) -> void:
	modulate.a = 1.0
	visible = true
	sprite.position = Vector2(-140 if from_left else 140, 0)
	var tw := create_tween()
	tw.tween_property(sprite, "position", Vector2.ZERO, 0.35).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	await tw.finished


func leave(to_left: bool) -> void:
	var tw := create_tween()
	tw.tween_property(sprite, "position", Vector2(-140 if to_left else 140, 0), 0.25).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN)
	await tw.finished
	visible = false
	sprite.position = Vector2.ZERO


func lunge(toward: Vector2) -> void:
	var dir := (toward - global_position).normalized() * 12.0
	var tw := create_tween()
	tw.tween_property(sprite, "position", dir, 0.09).set_ease(Tween.EASE_OUT)
	tw.tween_property(sprite, "position", Vector2.ZERO, 0.14)
	await tw.finished


func hurt() -> void:
	var tw := create_tween()
	for i in 3:
		tw.tween_property(sprite, "modulate", Color(3, 3, 3), 0.04)
		tw.tween_property(sprite, "modulate", Color(1, 1, 1), 0.05)
	var sh := create_tween()
	for i in 4:
		sh.tween_property(sprite, "position:x", 3.0 if i % 2 == 0 else -3.0, 0.035)
	sh.tween_property(sprite, "position:x", 0.0, 0.035)
	await tw.finished


func faint() -> void:
	var tw := create_tween().set_parallel(true)
	tw.tween_property(sprite, "position:y", 30.0, 0.45).set_ease(Tween.EASE_IN)
	tw.tween_property(self, "modulate:a", 0.0, 0.45)
	await tw.finished
	visible = false
	sprite.position = Vector2.ZERO


func center() -> Vector2:
	return global_position + Vector2(0, -30)
