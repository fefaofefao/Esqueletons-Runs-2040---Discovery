class_name PropSprite
extends Node2D
## Objeto de cenário com origem nos "pés" (para o y-sort), animação opcional
## e brilho de luz opcional (lamparinas, fogueiras).


static func create(def: Dictionary, tex: Texture2D, prop_id: String) -> PropSprite:
	var node := PropSprite.new()
	node.name = prop_id
	var r: Array = def["rect"]
	var frames := int(def.get("frames", 1))
	var sf := SpriteFrames.new()
	sf.set_animation_speed("default", maxf(float(def.get("fps", 1.0)), 0.1))
	for i in frames:
		var at := AtlasTexture.new()
		at.atlas = tex
		at.region = Rect2(float(r[0]) + i * float(r[2]), float(r[1]), float(r[2]), float(r[3]))
		sf.add_frame("default", at)
	var spr := AnimatedSprite2D.new()
	spr.sprite_frames = sf
	spr.centered = false
	var origin: Array = def["origin"]
	spr.offset = Vector2(-float(origin[0]), -float(origin[1]))
	node.add_child(spr)
	if frames > 1:
		spr.play("default")
		# começa em um quadro diferente para não balançarem todos juntos
		spr.frame = absi(hash(prop_id + str(Time.get_ticks_usec()))) % frames
	if def.has("light"):
		node.add_child(_glow(def["light"]))
	return node


static func _glow(light: Dictionary) -> Sprite2D:
	var radius := float(light.get("radius", 32))
	var col: Array = light.get("color", [1.0, 0.8, 0.5])
	var grad := Gradient.new()
	grad.set_color(0, Color(col[0], col[1], col[2], float(light.get("intensity", 0.35))))
	grad.set_color(1, Color(col[0], col[1], col[2], 0.0))
	var gt := GradientTexture2D.new()
	gt.gradient = grad
	gt.fill = GradientTexture2D.FILL_RADIAL
	gt.fill_from = Vector2(0.5, 0.5)
	gt.fill_to = Vector2(1.0, 0.5)
	gt.width = int(radius * 2)
	gt.height = int(radius * 2)
	var s := Sprite2D.new()
	s.texture = gt
	var off: Array = light.get("offset", [0, -8])
	s.position = Vector2(float(off[0]), float(off[1]))
	var mat := CanvasItemMaterial.new()
	mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	s.material = mat
	s.z_index = 5
	return s
