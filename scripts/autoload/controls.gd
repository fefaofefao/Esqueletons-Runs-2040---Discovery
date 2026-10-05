extends Node
## Registra as ações de entrada (teclado, gamepad e controles virtuais) e
## acompanha a direção pressionada mais recente.

signal input_mode_changed(touch: bool)

const DIRS := {
	"move_up": Vector2i.UP,
	"move_down": Vector2i.DOWN,
	"move_left": Vector2i.LEFT,
	"move_right": Vector2i.RIGHT,
}

const KEYS := {
	"move_up": [KEY_UP, KEY_W],
	"move_down": [KEY_DOWN, KEY_S],
	"move_left": [KEY_LEFT, KEY_A],
	"move_right": [KEY_RIGHT, KEY_D],
	"btn_a": [KEY_Z, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER],
	"btn_b": [KEY_X, KEY_BACKSPACE, KEY_SHIFT],
	"btn_menu": [KEY_ESCAPE, KEY_C],
	"btn_speed": [KEY_F, KEY_TAB],
	"dbg_menu": [KEY_F1],
}

const JOY_BUTTONS := {
	"move_up": [JOY_BUTTON_DPAD_UP],
	"move_down": [JOY_BUTTON_DPAD_DOWN],
	"move_left": [JOY_BUTTON_DPAD_LEFT],
	"move_right": [JOY_BUTTON_DPAD_RIGHT],
	"btn_a": [JOY_BUTTON_A],
	"btn_b": [JOY_BUTTON_B],
	"btn_menu": [JOY_BUTTON_START],
	"btn_speed": [JOY_BUTTON_RIGHT_SHOULDER],
	"dbg_menu": [JOY_BUTTON_BACK],
}

const JOY_AXES := {
	"move_up": [JOY_AXIS_LEFT_Y, -1.0],
	"move_down": [JOY_AXIS_LEFT_Y, 1.0],
	"move_left": [JOY_AXIS_LEFT_X, -1.0],
	"move_right": [JOY_AXIS_LEFT_X, 1.0],
}

## Pilha de direções na ordem em que foram pressionadas (a última vence).
var _dir_stack: Array[String] = []
var touch_mode := false


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	register_actions()
	touch_mode = DisplayServer.is_touchscreen_available()


static func register_actions() -> void:
	for action in KEYS.keys():
		if not InputMap.has_action(action):
			InputMap.add_action(action, 0.45)
		InputMap.action_erase_events(action)
		for k in KEYS[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)
		for b in JOY_BUTTONS.get(action, []):
			var jb := InputEventJoypadButton.new()
			jb.button_index = b
			InputMap.action_add_event(action, jb)
		if JOY_AXES.has(action):
			var jm := InputEventJoypadMotion.new()
			jm.axis = JOY_AXES[action][0]
			jm.axis_value = JOY_AXES[action][1]
			InputMap.action_add_event(action, jm)


func _input(event: InputEvent) -> void:
	for action in DIRS.keys():
		if event.is_action_pressed(action, false):
			_dir_stack.erase(action)
			_dir_stack.append(action)
		elif event.is_action_released(action):
			_dir_stack.erase(action)
	if event is InputEventScreenTouch:
		_set_touch_mode(true)
	elif (event is InputEventKey and event.pressed) or event is InputEventJoypadButton:
		_set_touch_mode(false)


func _set_touch_mode(value: bool) -> void:
	if touch_mode != value:
		touch_mode = value
		input_mode_changed.emit(value)


## Direção atual (a mais recente ainda pressionada) ou Vector2i.ZERO.
func current_direction() -> Vector2i:
	for i in range(_dir_stack.size() - 1, -1, -1):
		var action := _dir_stack[i]
		if Input.is_action_pressed(action):
			return DIRS[action]
	# Fallback: alguma direção pressionada que não passou pelo _input (ex.: ao voltar de pausa)
	for action in DIRS.keys():
		if Input.is_action_pressed(action):
			return DIRS[action]
	return Vector2i.ZERO


func clear() -> void:
	_dir_stack.clear()


## Injeta uma ação como se viesse de um botão físico (controles virtuais, botão voltar).
static func emit_action(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	ev.strength = 1.0 if pressed else 0.0
	Input.parse_input_event(ev)


static func tap_action(action: String) -> void:
	emit_action(action, true)
	emit_action(action, false)


static func dir_name(dir: Vector2i) -> String:
	match dir:
		Vector2i.UP:
			return "up"
		Vector2i.LEFT:
			return "left"
		Vector2i.RIGHT:
			return "right"
	return "down"


static func dir_from_name(name: String) -> Vector2i:
	match name:
		"up":
			return Vector2i.UP
		"left":
			return Vector2i.LEFT
		"right":
			return Vector2i.RIGHT
	return Vector2i.DOWN
