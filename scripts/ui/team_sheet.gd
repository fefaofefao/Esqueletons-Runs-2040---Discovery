class_name TeamSheet
extends Overlay
## Ficha de um esqueleto da equipe: sprite, nome, espécie, tipo, idade,
## crescimento, atributos e golpes. A = tornar o 1º do time; B = voltar.

signal done(make_lead: bool)

var monster: Monster
var team_index := 0


func setup(m: Monster, i: int) -> TeamSheet:
	monster = m
	team_index = i
	return self


func _init() -> void:
	super._init()
	pauses_game = true
	mouse_filter = Control.MOUSE_FILTER_STOP


func _ready() -> void:
	dim_background(0.6)
	var panel := centered_panel(300)
	var col := VBoxContainer.new()
	panel.add_child(col)
	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 6)
	col.add_child(top)
	var frame := Control.new()
	frame.custom_minimum_size = Vector2(64, 64)
	top.add_child(frame)
	var spr := Sprite2D.new()
	spr.texture = load(str(monster.info().get("sprite", "")))
	spr.region_enabled = true
	spr.region_rect = Rect2(0, 0, 32, 32)
	spr.centered = false
	spr.scale = Vector2(2, 2)
	frame.add_child(spr)
	if monster.golden:
		GoldenFX.apply(spr, Vector2(16, 16), Vector2(10, 12))
	var right := VBoxContainer.new()
	top.add_child(right)
	right.add_child(UiTheme.label(("★" if monster.golden else "") + monster.display_name(), UiTheme.TEXT_ACCENT))
	var sp_name := tr(str(monster.info().get("name_key", "")))
	right.add_child(UiTheme.label("%s · %s" % [sp_name, tr("TYPE_" + monster.type().to_upper())]))
	right.add_child(UiTheme.label("%s · %s %d/%d" % [UnitCard.age_text(monster.level), tr("STAT_HP"), monster.hp, monster.max_hp()], UiTheme.TEXT_VALUE))
	var gl: Array = monster.info().get("growth_levels", [])
	var st := monster.stage()
	if gl.size() == 2 and st < 3:
		right.add_child(UiTheme.label(tr("TEAM_GROWS_AT").format({"n": int(gl[st - 1])}), UiTheme.TEXT_VALUE))
	var stats := ""
	for s in ["atk", "mag", "def", "res", "spd"]:
		stats += "%s %d  " % [tr("STAT_" + s.to_upper()), monster.stat(s)]
	col.add_child(UiTheme.label(stats.strip_edges()))
	var moves := []
	for mv in monster.moves:
		moves.append(tr(str(Data.move(str(mv.id)).get("name_key", ""))))
	col.add_child(UiTheme.label(" · ".join(moves), UiTheme.TEXT_VALUE))
	if team_index > 0:
		col.add_child(UiTheme.label(tr("TEAM_MAKE_LEAD"), UiTheme.TEXT_DISABLED))


func _finish(lead: bool) -> void:
	done.emit(lead)
	close()


func _unhandled_input(event: InputEvent) -> void:
	if not accepts_input():
		return
	if event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		Audio.sfx("confirm")
		_finish(team_index > 0)
	elif event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		Audio.sfx("cancel")
		_finish(false)


func _gui_input(event: InputEvent) -> void:
	if accepts_input() and event is InputEventMouseButton and event.pressed:
		_finish(false)
