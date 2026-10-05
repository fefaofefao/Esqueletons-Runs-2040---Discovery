class_name Overlay
extends Control
## Base de toda tela sobreposta (menus, diálogos, caixas). O Game mantém a pilha;
## só a do topo recebe entrada. Funciona com o jogo pausado.

signal closed

## Pausa a árvore enquanto aberto (menu de pausa, configurações no mapa...).
var pauses_game := false
var _opened_frame := -1


func _init() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	# o tema não atravessa CanvasLayer: cada raiz de UI recebe o tema do jogo
	theme = UiTheme.build()


func mark_opened() -> void:
	_opened_frame = Engine.get_process_frames()


## Verdadeiro se este overlay está no topo e já passou o quadro em que abriu
## (evita que o mesmo toque/tecla que o abriu também o acione).
func accepts_input() -> bool:
	return Game.top_overlay() == self and Engine.get_process_frames() > _opened_frame


func close() -> void:
	Game.close_overlay(self)


## Chamado pelo botão voltar do Android. Padrão: equivale a apertar B.
func on_back() -> void:
	Controls.tap_action("btn_b")


func centered_panel(min_width: float) -> PanelContainer:
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)
	var panel := PanelContainer.new()
	panel.custom_minimum_size.x = min_width
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	center.add_child(panel)
	return panel


func dim_background(alpha: float = 0.45) -> void:
	var bg := ColorRect.new()
	bg.color = Color(0.05, 0.04, 0.08, alpha)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(bg)
