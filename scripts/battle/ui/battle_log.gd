class_name BattleLog
extends PanelContainer
## Faixa de mensagens da batalha (2 linhas): máquina de escrever que respeita
## o 2x e a velocidade do texto; segue sozinha após uma pausa curta. A (ou
## toque) acelera.

signal advanced

const HOLD := 0.55
## Largura útil do texto e linhas (o teste de overflow usa as mesmas medidas).
const TEXT_WIDTH := 226.0
const LINES := 2

var _label: Label
var _shown := 0.0
var _typing := false
var _hold := 0.0
var _waiting := false


func _init() -> void:
	theme = UiTheme.build()
	mouse_filter = Control.MOUSE_FILTER_STOP
	add_theme_stylebox_override("panel", UiTheme.frame("light"))
	_label = UiTheme.label("")
	_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_label.custom_minimum_size = Vector2(TEXT_WIDTH, 24)
	add_child(_label)
	gui_input.connect(func(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed:
			accept_event()
			skip())


func say(text: String) -> void:
	visible = true
	_label.text = "\n".join(TextFit.wrap_lines(text, TEXT_WIDTH).slice(0, LINES))
	_label.visible_characters = 0
	_shown = 0.0
	_typing = true
	_hold = HOLD
	_waiting = true
	await advanced


func _process(delta: float) -> void:
	if not _waiting:
		return
	if _typing:
		_shown += delta * Settings.text_cps() * 1.6
		_label.visible_characters = mini(int(_shown), _label.get_total_character_count())
		if _label.visible_characters >= _label.get_total_character_count():
			_typing = false
		return
	_hold -= delta
	if _hold <= 0.0:
		_finish()


func skip() -> void:
	if not _waiting:
		return
	if _typing:
		_typing = false
		_label.visible_characters = -1
		_hold = 0.15
	else:
		_finish()


func _finish() -> void:
	_waiting = false
	advanced.emit()


func clear() -> void:
	_label.text = ""
