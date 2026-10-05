class_name Player
extends Node2D
## Protagonista: movimento em grade nas 4 direções. Um toque rápido numa
## direção nova só vira o personagem; segurar anda. Segurar B corre.

const WALK_TIME := 0.26
const RUN_TIME := 0.13
const TURN_DELAY := 0.09
const BUMP_INTERVAL_MS := 380

var cell := Vector2i.ZERO
var facing := "down"
var world: World
var map: MapView
var sprite: CharacterSprite
var moving := false
var frozen := false
var running := false

var _from := Vector2.ZERO
var _to := Vector2.ZERO
var _prev_cell := Vector2i.ZERO
var _t := 0.0
var _dur := WALK_TIME
var _turn_wait := 0.0
var _last_dir := Vector2i.ZERO
var _dust: CPUParticles2D


func setup(owner_world: World, owner_map: MapView) -> void:
	world = owner_world
	map = owner_map
	name = "Player"
	sprite = CharacterSprite.new()
	add_child(sprite)
	sprite.setup("res://assets/sprites/player.png", 3, 2.0 / WALK_TIME)
	_dust = _make_dust()
	add_child(_dust)


func place(c: Vector2i, dir: String) -> void:
	cell = c
	_prev_cell = c
	moving = false
	position = MapView.cell_to_pos(c)
	facing = dir
	sprite.face(dir)
	sprite.idle()


func _process(delta: float) -> void:
	if moving:
		_t += delta / _dur
		if _t < 1.0:
			position = _from.lerp(_to, _t)
			return
		position = _to
		moving = false
		world.on_player_arrived(cell)
		# andar contínuo: sem atraso de virar se a direção continuar pressionada
		_handle_input(delta, true)
		return
	_handle_input(delta, false)


func _handle_input(delta: float, continuing: bool) -> void:
	if frozen or not Game.world_input_enabled():
		if not moving:
			sprite.idle()
		_last_dir = Vector2i.ZERO
		return
	var dir := Controls.current_direction()
	if dir == Vector2i.ZERO:
		_turn_wait = 0.0
		_last_dir = Vector2i.ZERO
		sprite.idle()
		return
	var dname := Controls.dir_name(dir)
	if not continuing and dir != _last_dir and dname != facing:
		facing = dname
		sprite.face(dname)
		sprite.idle()
		_turn_wait = TURN_DELAY
		_last_dir = dir
		return
	_last_dir = dir
	if _turn_wait > 0.0:
		_turn_wait -= delta
		return
	try_move(dir)


func try_move(dir: Vector2i) -> bool:
	facing = Controls.dir_name(dir)
	sprite.face(facing)
	var target := cell + dir
	if map.is_blocked(target):
		sprite.walk(0.5)
		Audio.sfx("bump", BUMP_INTERVAL_MS)
		return false
	running = Input.is_action_pressed("btn_b")
	_start_move(target, RUN_TIME if running else WALK_TIME)
	sprite.walk(2.0 if running else 1.0)
	if running:
		_dust.restart()
	return true


func _start_move(target: Vector2i, duration: float) -> void:
	_prev_cell = cell
	_from = position
	_to = MapView.cell_to_pos(target)
	_t = 0.0
	_dur = duration
	cell = target
	moving = true


## Volta à célula anterior (usado quando uma saída está bloqueada).
func step_back() -> void:
	if _prev_cell == cell:
		return
	var back := _prev_cell
	_start_move(back, WALK_TIME)
	sprite.walk(1.0)


func facing_cell() -> Vector2i:
	return cell + Controls.dir_from_name(facing)


func _unhandled_input(event: InputEvent) -> void:
	if moving or frozen or not Game.world_input_enabled():
		return
	if event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		world.interact(facing_cell(), Controls.dir_from_name(facing))


func _make_dust() -> CPUParticles2D:
	var p := CPUParticles2D.new()
	p.texture = load("res://assets/ui/particle_dust.png")
	p.emitting = false
	p.one_shot = true
	p.amount = 5
	p.lifetime = 0.45
	p.explosiveness = 1.0
	p.local_coords = false
	p.direction = Vector2(0, -1)
	p.spread = 70.0
	p.initial_velocity_min = 6.0
	p.initial_velocity_max = 14.0
	p.gravity = Vector2(0, 18)
	p.position = Vector2(0, -2)
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0.9))
	ramp.set_color(1, Color(1, 1, 1, 0.0))
	p.color_ramp = ramp
	p.z_index = -1
	return p
