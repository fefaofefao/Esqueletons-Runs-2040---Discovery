class_name CharacterSprite
extends Node2D
## Sprite de personagem em folha 16x24: colunas = quadros, linhas = direções
## (baixo, esquerda, direita, cima). Inclui sombra suave sob os pés.

const FW := 16
const FH := 24
const ROWS := {"down": 0, "left": 1, "right": 2, "up": 3}

var anim: AnimatedSprite2D
var facing := "down"


func setup(sheet_path: String, frames: int, walk_fps: float, idle_fps: float = 0.0) -> void:
	var tex: Texture2D = load(sheet_path)
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for dir: String in ROWS.keys():
		var row: int = ROWS[dir]
		var idle_name: String = "idle_" + dir
		var walk_name: String = "walk_" + dir
		sf.add_animation(idle_name)
		sf.add_animation(walk_name)
		sf.set_animation_speed(idle_name, maxf(idle_fps, 0.1))
		sf.set_animation_speed(walk_name, walk_fps)
		sf.add_frame(idle_name, _frame(tex, 0, row))
		if idle_fps > 0.0 and frames > 1:
			sf.add_frame(idle_name, _frame(tex, 1, row))
		if frames >= 3:
			# passo A, parado, passo B, parado
			for c in [1, 0, 2, 0]:
				sf.add_frame(walk_name, _frame(tex, c, row))
		else:
			sf.add_frame(walk_name, _frame(tex, 0, row))
	var shadow := Sprite2D.new()
	shadow.texture = load("res://assets/sprites/shadow.png")
	shadow.position = Vector2(0, -2)
	add_child(shadow)
	anim = AnimatedSprite2D.new()
	anim.sprite_frames = sf
	anim.centered = false
	anim.offset = Vector2(-FW / 2.0, -FH)
	add_child(anim)
	idle()


func _frame(tex: Texture2D, col: int, row: int) -> AtlasTexture:
	var at := AtlasTexture.new()
	at.atlas = tex
	at.region = Rect2(col * FW, row * FH, FW, FH)
	return at


func face(dir: String) -> void:
	facing = dir
	var anim_name := ("walk_" if anim.animation.begins_with("walk") and anim.is_playing() else "idle_") + dir
	if anim.animation != anim_name:
		anim.play(anim_name)


func walk(speed_scale: float = 1.0) -> void:
	var anim_name := "walk_" + facing
	anim.speed_scale = speed_scale
	if anim.animation != anim_name or not anim.is_playing():
		anim.play(anim_name)


func idle() -> void:
	anim.speed_scale = 1.0
	anim.play("idle_" + facing)
