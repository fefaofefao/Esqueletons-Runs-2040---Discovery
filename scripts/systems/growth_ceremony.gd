class_name GrowthCeremony
extends Overlay
## Animação "Aniversário e Crescimento" (seção 8), feita no mapa:
##   1. o controle congela e o esqueleto sai do chão ao lado do jogador;
##   2. bolo com velas, confete e o balão "Feliz aniversário, [nome]!", com música
##      curta; ele sopra as velas;
##   3. brilho pulsante, com a silhueta alternando entre o estágio atual e o novo,
##      acelerando até um flash;
##   4. revelação: "[nome] cresceu e virou [espécie]!";
##   5. golpe novo: abre a escolha de qual esquecer (se já sabe 4).
## Dura ~7 s em 1x e respeita o 2x (tweens no tempo do jogo). A acelera o texto,
## mas não pula a revelação.

signal done

var monster: Monster
var anchor := Vector2.ZERO
var _old_tex: Texture2D
var _new_tex: Texture2D
var _sprite: Sprite2D
var _clip: Control
var _cake: Sprite2D
var _balloon: PanelContainer
var _flash: ColorRect
var _text_box: PanelContainer
var _text: Label
var _typing := false
var _shown := 0.0
var _finished := false


func setup(m: Monster, screen_pos: Vector2) -> GrowthCeremony:
	monster = m
	anchor = screen_pos
	return self


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	_old_tex = load(str(monster.info().get("sprite", "")))
	var target := monster.growth_target()
	_new_tex = load(str(Data.species(target).get("sprite", "")))
	_clip = Control.new()
	_clip.clip_contents = true
	_clip.size = Vector2(40, 40)
	_clip.position = anchor + Vector2(10, -38)
	add_child(_clip)
	_sprite = Sprite2D.new()
	_sprite.texture = _old_tex
	_sprite.region_enabled = true
	_sprite.region_rect = Rect2(0, 0, 32, 32)
	_sprite.centered = false
	_sprite.position = Vector2(4, 40)
	_clip.add_child(_sprite)
	if monster.golden:
		GoldenFX.apply(_sprite, Vector2(16, 16), Vector2(10, 12))
	_cake = Sprite2D.new()
	_cake.texture = load("res://assets/battle/cake.png")
	_cake.region_enabled = true
	_cake.region_rect = Rect2(0, 0, 28, 26)
	_cake.position = anchor + Vector2(62, -14)
	_cake.scale = Vector2.ZERO
	add_child(_cake)
	_balloon = PanelContainer.new()
	var bl := UiTheme.label(tr("GROW_BIRTHDAY").format({"name": monster.display_name()}), UiTheme.TEXT_ACCENT)
	_balloon.add_child(bl)
	_balloon.visible = false
	add_child(_balloon)
	_flash = ColorRect.new()
	_flash.set_anchors_preset(Control.PRESET_FULL_RECT)
	_flash.color = Color(1, 1, 1, 0)
	_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_flash)
	_text_box = PanelContainer.new()
	_text = UiTheme.label("")
	_text.custom_minimum_size = Vector2(UiTheme.DIALOG_TEXT_WIDTH, 24)
	_text_box.add_child(_text)
	_text_box.visible = false
	add_child(_text_box)
	_play()


func _wait(s: float) -> void:
	await get_tree().create_timer(s, true).timeout


func _play() -> void:
	# 1. sai do chão
	Audio.sfx("door")
	_dust(_clip.position + Vector2(20, 38))
	var tw := create_tween()
	tw.tween_property(_sprite, "position:y", 6.0, 0.8).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	await tw.finished
	# 2. bolo, confete, balão e música
	Audio.sfx("birthday")
	var tc := create_tween()
	tc.tween_property(_cake, "scale", Vector2.ONE, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_confetti(anchor + Vector2(40, -40))
	_balloon.visible = true
	_balloon.reset_size()
	_balloon.position = Vector2(clampf(anchor.x - _balloon.size.x / 2.0 + 30, 4, get_viewport_rect().size.x - _balloon.size.x - 4), anchor.y - 74)
	var flick := 0
	for i in 8:
		flick = 1 - flick
		_cake.region_rect = Rect2(28 * flick, 0, 28, 26)
		await _wait(0.15)
	# sopra as velas
	Audio.sfx("blow")
	var blow := create_tween()
	blow.tween_property(_sprite, "position:x", 8.0, 0.12)
	blow.tween_property(_sprite, "position:x", 4.0, 0.12)
	_cake.region_rect = Rect2(56, 0, 28, 26)
	_smoke(_cake.position + Vector2(0, -12))
	await _wait(0.6)
	_balloon.visible = false
	var tcake := create_tween()
	tcake.tween_property(_cake, "modulate:a", 0.0, 0.3)
	# 3. brilho e silhuetas alternando, acelerando
	var interval := 0.36
	var use_new := false
	while interval > 0.045:
		use_new = not use_new
		_sprite.texture = _new_tex if use_new else _old_tex
		_sprite.modulate = Color(0, 0, 0, 1) if use_new else Color(2.2, 2.2, 2.2, 1)
		await _wait(interval)
		interval *= 0.78
	# flash
	Audio.sfx("grow_flash")
	var tf := create_tween()
	tf.tween_property(_flash, "color:a", 1.0, 0.12)
	await tf.finished
	var result := monster.grow()
	_sprite.texture = _new_tex
	_sprite.modulate = Color.WHITE
	var tf2 := create_tween()
	tf2.tween_property(_flash, "color:a", 0.0, 0.45)
	_sparkles(_clip.position + Vector2(20, 20))
	await tf2.finished
	# 4. revelação
	var species_name := tr(str(Data.species(result.get("to", "")).get("name_key", "")))
	await _say(tr("GROW_DONE").format({"name": _base_name(result.get("from", "")), "species": species_name}))
	Ossuary.mark_seen(monster)
	Ossuary.entry(monster.species_id)["recruited"] = true
	# 5. golpe exclusivo do novo estágio
	var mv := str(result.get("move", ""))
	if mv != "" and not monster.knows(mv):
		await _learn(mv)
	_finished = true
	done.emit()
	close()


func _base_name(species: String) -> String:
	if monster.nickname != "":
		return monster.nickname
	return tr(str(Data.species(species).get("name_key", "")))


func _say(text: String) -> void:
	_text_box.visible = true
	_text_box.reset_size()
	var vp := get_viewport_rect().size
	_text_box.position = Vector2(floorf((vp.x - _text_box.size.x) / 2.0), vp.y - _text_box.size.y - 4)
	_text.text = "\n".join(TextFit.wrap_lines(text, UiTheme.DIALOG_TEXT_WIDTH).slice(0, 2))
	_text.visible_characters = 0
	_shown = 0.0
	_typing = true
	while _typing:
		await get_tree().process_frame
	# segura a mensagem um pouco (A não pula a revelação, só o texto)
	await _wait(0.9)


func _process(delta: float) -> void:
	if _typing:
		_shown += delta * Settings.text_cps()
		_text.visible_characters = int(_shown)
		if _text.visible_characters >= _text.get_total_character_count():
			_typing = false


func _unhandled_input(event: InputEvent) -> void:
	if not accepts_input():
		return
	if event.is_action_pressed("btn_a", false) or event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		if _typing:
			_text.visible_characters = -1
			_typing = false


## Sem botão voltar durante a cerimônia (não pode ser pulada).
func on_back() -> void:
	pass


func _learn(move_id: String) -> void:
	var mv_name := tr(str(Data.move(move_id).get("name_key", "")))
	if monster.moves.size() < 4:
		monster.moves.append({"id": move_id, "pp": int(Data.move(move_id).get("pp", 10))})
		await _say(tr("BTL_LEARNED").format({"name": monster.display_name(), "move": mv_name}))
		return
	await _say(tr("BTL_LEARN_PROMPT").format({"name": monster.display_name(), "move": mv_name}))
	var options := []
	for m in monster.moves:
		options.append(str(Data.move(str(m["id"])).get("name_key", "")))
	options.append("BTL_LEARN_GIVE_UP")
	var answer := await ChoiceBox.ask("BTL_LEARN_TITLE", options)
	if answer >= 0 and answer < monster.moves.size():
		BattleEngine.learn_move(monster, move_id, answer)
		await _say(tr("BTL_LEARNED").format({"name": monster.display_name(), "move": mv_name}))
	else:
		await _say(tr("BTL_DID_NOT_LEARN").format({"name": monster.display_name(), "move": mv_name}))


# ------------------------------------------------------------------ partículas
func _burst(at: Vector2, color: Color, amount: int, speed: float, gravity: Vector2, tex: String = "dot", life: float = 0.9) -> void:
	var p := CPUParticles2D.new()
	p.texture = load("res://assets/ui/particle_%s.png" % tex)
	p.one_shot = true
	p.explosiveness = 0.85
	p.amount = amount
	p.lifetime = life
	p.spread = 180.0
	p.initial_velocity_min = speed * 0.4
	p.initial_velocity_max = speed
	p.gravity = gravity
	p.scale_amount_min = 1.0
	p.scale_amount_max = 2.0
	p.color = color
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 1))
	ramp.set_color(1, Color(1, 1, 1, 0))
	p.color_ramp = ramp
	p.position = at
	add_child(p)
	p.emitting = true


func _confetti(at: Vector2) -> void:
	for c in [Color8(255, 120, 140), Color8(255, 220, 90), Color8(120, 200, 255), Color8(150, 240, 140), Color8(200, 140, 255)]:
		_burst(at, c, 10, 90.0, Vector2(0, 120), "dot", 1.4)


func _dust(at: Vector2) -> void:
	_burst(at, Color8(238, 222, 186), 12, 30.0, Vector2(0, 30), "dust", 0.7)


func _smoke(at: Vector2) -> void:
	_burst(at, Color8(200, 200, 210), 8, 14.0, Vector2(0, -30), "dust", 1.0)


func _sparkles(at: Vector2) -> void:
	_burst(at, Color8(255, 250, 200), 18, 60.0, Vector2(0, -20), "sparkle", 1.0)
