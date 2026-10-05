class_name GoldenFX
extends Node
## Aplica o visual Golden a um Sprite2D: shader de paleta dourada, brilho a
## cada 2 s (tempo escalado, respeita o 2x) e faíscas douradas.

const SHADER := preload("res://assets/shaders/golden.gdshader")

var _mat: ShaderMaterial
var _t := 0.0


static func apply(sprite: Sprite2D, sparkle_offset: Vector2 = Vector2(0, -16), sparkle_extent: Vector2 = Vector2(10, 12)) -> GoldenFX:
	var fx := GoldenFX.new()
	fx.name = "GoldenFX"
	var mat := ShaderMaterial.new()
	mat.shader = SHADER
	var ts := sprite.texture.get_size()
	var r := sprite.region_rect if sprite.region_enabled else Rect2(Vector2.ZERO, ts)
	mat.set_shader_parameter("region", Vector4(r.position.x / ts.x, r.position.y / ts.y, r.size.x / ts.x, r.size.y / ts.y))
	sprite.material = mat
	fx._mat = mat
	sprite.add_child(fx)
	var p := CPUParticles2D.new()
	p.texture = load("res://assets/ui/particle_sparkle.png")
	p.amount = 6
	p.lifetime = 0.9
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	p.emission_rect_extents = sparkle_extent
	p.position = sparkle_offset
	p.gravity = Vector2(0, -12)
	p.color = Color(1.0, 0.86, 0.35)
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0))
	ramp.set_color(1, Color(1, 1, 1, 0))
	ramp.add_point(0.4, Color(1, 1, 1, 1))
	p.color_ramp = ramp
	p.local_coords = true
	sprite.add_child(p)
	return fx


func _process(delta: float) -> void:
	_t += delta
	if _mat:
		_mat.set_shader_parameter("t", _t)
