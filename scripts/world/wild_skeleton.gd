class_name WildSkeleton
extends Node2D
## Esqueleto selvagem visível no mapa (seção 7): patrulha dentro de um raio em
## torno do ponto de spawn e inicia a batalha ao encostar no jogador.
## Comportamentos: "patrol" (passeia), "circle" (ronda em círculo), "chase"
## (persegue quando vê o jogador), "shy" (foge), "fast" (passeia rápido).
## Golden: brilha, solta faíscas e toca um som ao entrar na tela.

const STEP_TIME := 0.32

var species := ""
var level := 1
var golden := false
var cell := Vector2i.ZERO
var home := Vector2i.ZERO
var radius := 3
var behavior := "patrol"
var map: MapView
var world: World
var stunned := 0.0
var spawn_id := ""

var _sprite: Sprite2D
var _moving := false
var _from := Vector2.ZERO
var _to := Vector2.ZERO
var _t := 0.0
var _wait := 1.0
var _rng := RandomNumberGenerator.new()
var _circle_i := 0
var _announced := false
var _bob := 0.0
var _has_map_sprite := false


func setup(owner_map: MapView, spec: Dictionary, at: Vector2i, center: Vector2i, r: int, beh: String) -> WildSkeleton:
	map = owner_map
	species = str(spec.species)
	level = int(spec.level)
	golden = bool(spec.get("golden", false))
	cell = at
	home = center
	radius = r
	behavior = beh if beh != "" else str(Data.species(species).get("map_behavior", "patrol"))
	_rng.seed = hash(str(at) + species + str(Time.get_ticks_usec()))
	_wait = _rng.randf_range(0.3, 1.5)
	name = "Wild_%s_%d_%d" % [species, at.x, at.y]
	var shadow := Sprite2D.new()
	shadow.texture = load("res://assets/sprites/shadow.png")
	shadow.position = Vector2(0, -2)
	add_child(shadow)
	_sprite = Sprite2D.new()
	var info := Data.species(species)
	if info.has("map_sprite") and ResourceLoader.exists(str(info["map_sprite"])):
		_has_map_sprite = true
		_sprite.texture = load(str(info["map_sprite"]))
		_sprite.region_enabled = true
		_sprite.region_rect = Rect2(0, 0, 16, 16)
		_sprite.offset = Vector2(-8, -16)
	else:
		# sem sprite de mapa: usa o de batalha reduzido
		_sprite.texture = load(str(info.get("sprite", "")))
		_sprite.region_enabled = true
		_sprite.region_rect = Rect2(0, 0, 32, 32)
		_sprite.scale = Vector2(0.5, 0.5)
		_sprite.offset = Vector2(-16, -32)
	_sprite.centered = false
	add_child(_sprite)
	if golden:
		GoldenFX.apply(_sprite, Vector2(8, 8) if _has_map_sprite else Vector2(16, 16), Vector2(8, 8))
	position = MapView.cell_to_pos(cell)
	return self


func _process(delta: float) -> void:
	_bob += delta
	_sprite.position.y = -absf(sin(_bob * 6.0)) * 1.5 if _moving else 0.0
	if _has_map_sprite:
		# 2 quadros: alterna mais rápido andando
		var frame := int(_bob * (6.0 if _moving else 2.0)) % 2
		_sprite.region_rect = Rect2(16 * frame, 0, 16, 16)
	if golden and not _announced and _on_screen():
		_announced = true
		Audio.sfx("golden")
	if stunned > 0.0:
		stunned -= delta
		modulate.a = 0.5 + 0.5 * absf(sin(_bob * 12.0))
		return
	modulate.a = 1.0
	if _moving:
		_t += delta / (STEP_TIME * (0.6 if behavior == "fast" else 1.0))
		if _t >= 1.0:
			position = _to
			_moving = false
		else:
			position = _from.lerp(_to, _t)
		return
	if not Game.world_input_enabled():
		return
	_wait -= delta
	if _wait > 0.0:
		return
	_wait = _rng.randf_range(0.5, 1.4) * (0.5 if behavior == "fast" else 1.0)
	_step()


func _on_screen() -> bool:
	var p := get_global_transform_with_canvas().origin
	var vp := get_viewport_rect().size
	return p.x > -8 and p.y > -8 and p.x < vp.x + 8 and p.y < vp.y + 8


func _player_cell() -> Vector2i:
	return world.player.cell if world and world.player else Vector2i(-999, -999)


func _step() -> void:
	var pc := _player_cell()
	var dist := (pc - cell).abs()
	var near := dist.x + dist.y <= 4
	var dir := Vector2i.ZERO
	match behavior:
		"chase":
			if near:
				dir = _toward(pc)
		"shy":
			if near:
				dir = -_toward(pc)
		"circle":
			var ring := [Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT, Vector2i.UP]
			dir = ring[(_circle_i / 2) % 4]
			_circle_i += 1
	if dir == Vector2i.ZERO:
		var dirs := [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]
		dir = dirs[_rng.randi() % 4]
	var target := cell + dir
	if target == pc:
		# encostou no jogador
		if world:
			world.on_touch_wild(self)
		return
	var off := target - home
	if absi(off.x) + absi(off.y) > radius or map.is_blocked(target) or target == pc:
		return
	map.move_wild(self, cell, target)
	cell = target
	_from = position
	_to = MapView.cell_to_pos(target)
	_t = 0.0
	_moving = true


func _toward(pc: Vector2i) -> Vector2i:
	var d := pc - cell
	if absi(d.x) > absi(d.y):
		return Vector2i(signi(d.x), 0)
	return Vector2i(0, signi(d.y))


func stun(seconds: float) -> void:
	stunned = seconds
