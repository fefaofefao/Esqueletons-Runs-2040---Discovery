class_name Ambient
extends RefCounted
## Partículas de ambiente por mapa (lista "ambient" no JSON do mapa):
##   sea_sparkle  brilhos na água
##   leaves       folhas soltas dos coqueiros, levadas pelo vento
##   dust_motes   poeira flutuando na luz (interiores)


static func add_to_map(map: MapView) -> void:
	for kind in map.data.get("ambient", []):
		match str(kind):
			"sea_sparkle":
				_sea_sparkle(map)
			"leaves":
				_leaves(map)
			"dust_motes":
				_dust_motes(map)


static func _base(tex: String, amount: int, lifetime: float) -> CPUParticles2D:
	var p := CPUParticles2D.new()
	p.texture = load("res://assets/ui/particle_%s.png" % tex)
	p.amount = maxi(amount, 1)
	p.lifetime = lifetime
	p.randomness = 1.0
	p.lifetime_randomness = 0.4
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_POINTS
	p.gravity = Vector2.ZERO
	p.initial_velocity_min = 0.0
	p.initial_velocity_max = 0.0
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0))
	ramp.set_color(1, Color(1, 1, 1, 0))
	ramp.add_point(0.35, Color(1, 1, 1, 1))
	p.color_ramp = ramp
	return p


static func _points(cells: Array, per_cell: int, rng: RandomNumberGenerator, offset: Vector2, jitter: float) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for c in cells:
		for i in per_cell:
			var base := Vector2(c) * MapView.T + Vector2(8, 8) + offset
			pts.append(base + Vector2(rng.randf_range(-jitter, jitter), rng.randf_range(-jitter, jitter)))
	return pts


static func _sea_sparkle(map: MapView) -> void:
	var cells := map.cells_of(["water", "deep"])
	if cells.is_empty():
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = hash(map.id)
	var p := _base("sparkle", clampi(cells.size() / 10, 6, 40), 1.1)
	p.emission_points = _points(cells, 1, rng, Vector2.ZERO, 7.0)
	map.add_child(p)
	map.move_child(p, map.ground_props.get_index())


static func _leaves(map: MapView) -> void:
	var palms := map.props_of("palm")
	if palms.is_empty():
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = hash(map.id) + 1
	var p := _base("leaf", clampi(palms.size() * 2, 2, 16), 4.0)
	p.emission_points = _points(palms, 3, rng, Vector2(2, -42), 9.0)
	p.direction = Vector2(1, 0.3)
	p.spread = 25.0
	p.initial_velocity_min = 6.0
	p.initial_velocity_max = 14.0
	p.gravity = Vector2(3, 9)
	p.angular_velocity_min = -160.0
	p.angular_velocity_max = 160.0
	p.angle_min = -180.0
	p.angle_max = 180.0
	p.z_index = 20
	map.add_child(p)


static func _dust_motes(map: MapView) -> void:
	var cells := map.cells_of(["floor", "mat"])
	if cells.is_empty():
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = hash(map.id) + 2
	var p := _base("dot", clampi(cells.size() / 4, 4, 20), 5.0)
	p.emission_points = _points(cells, 1, rng, Vector2.ZERO, 8.0)
	p.direction = Vector2(0.3, -1)
	p.spread = 40.0
	p.initial_velocity_min = 1.0
	p.initial_velocity_max = 3.0
	p.color = Color(1, 0.95, 0.8, 0.5)
	p.z_index = 20
	map.add_child(p)
