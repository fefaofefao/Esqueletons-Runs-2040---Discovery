class_name CreditsScreen
extends Overlay
## Créditos rolando (fim de jogo e tela Sobre). Dados da produtora vêm de
## config/publisher.json; A acelera, B pula.

var _box: VBoxContainer
var _speed := 14.0
var _fast := false


func _init() -> void:
	super._init()
	pauses_game = true
	mouse_filter = Control.MOUSE_FILTER_STOP


func _ready() -> void:
	var bg := ColorRect.new()
	bg.color = Color(0.05, 0.04, 0.08, 1.0)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)
	_box = VBoxContainer.new()
	_box.add_theme_constant_override("separation", 6)
	_box.custom_minimum_size = Vector2(get_viewport_rect().size.x, 0)
	add_child(_box)
	var pub := Data.publisher()
	var lines := [
		["CREDITS_TITLE", UiTheme.TEXT_ACCENT, {}],
		["CREDITS_PRODUCER", UiTheme.TEXT_LIGHT, {"name": str(pub.get("producer", ""))}],
		["CREDITS_DIRECTOR", UiTheme.TEXT_LIGHT, {"name": str(pub.get("responsible", ""))}],
		["CREDITS_ORIGINAL", UiTheme.TEXT_LIGHT, {}],
		["CREDITS_ENGINE", UiTheme.TEXT_LIGHT, {}],
		["CREDITS_FONTS", UiTheme.TEXT_LIGHT, {}],
		["CREDITS_THANKS", UiTheme.TEXT_ACCENT, {}],
	]
	for l in lines:
		var lab := UiTheme.label(tr(l[0]).format(l[2]), l[1])
		lab.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lab.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		lab.custom_minimum_size = Vector2(get_viewport_rect().size.x - 40, 0)
		_box.add_child(lab)
		_box.add_child(Control.new())
	_box.position = Vector2(20, get_viewport_rect().size.y + 4)


func _process(delta: float) -> void:
	_box.position.y -= delta * _speed * (4.0 if _fast else 1.0)
	if _box.position.y + _box.size.y < -8:
		close()


func _unhandled_input(event: InputEvent) -> void:
	if not accepts_input():
		return
	if event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		close()
	elif event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		_fast = not _fast
