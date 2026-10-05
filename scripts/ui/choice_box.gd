class_name ChoiceBox
extends Overlay
## Pergunta com opções (ex.: confirmar sobrescrever o save). B escolhe a última opção.

signal answered(index: int)

var question_key := ""
var option_keys: Array = []
var _menu: MenuList


func setup(question: String, options: Array) -> ChoiceBox:
	question_key = question
	option_keys = options
	return self


func _ready() -> void:
	dim_background()
	var panel := centered_panel(220)
	var box := VBoxContainer.new()
	panel.add_child(box)
	for line in TextFit.wrap_lines(tr(question_key), 206):
		box.add_child(UiTheme.label(line))
	box.add_child(Control.new())
	_menu = MenuList.new()
	_menu.overlay = self
	var items := []
	for i in option_keys.size():
		items.append({"id": str(i), "key": str(option_keys[i])})
	box.add_child(_menu)
	_menu.set_items(items)
	_menu.activated.connect(func(id: String) -> void: _answer(int(id)))
	_menu.cancelled.connect(func() -> void: _answer(option_keys.size() - 1))


func _answer(i: int) -> void:
	answered.emit(i)
	close()


static func ask(question: String, options: Array) -> int:
	var box := ChoiceBox.new().setup(question, options)
	Game.open_overlay(box)
	var result: int = await box.answered
	return result
