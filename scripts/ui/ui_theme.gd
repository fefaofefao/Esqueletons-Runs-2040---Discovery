class_name UiTheme
extends RefCounted
## Tema da interface (fonte pixel, molduras 9-slice e cores) e medidas de layout
## usadas também pelo teste de overflow de texto.

const FONT_PATH := "res://assets/fonts/pixel.fnt"
const FONT_SIZE := 12
const LINE_HEIGHT := 12

const TEXT_DARK := Color8(48, 40, 56)
const TEXT_LIGHT := Color8(246, 242, 232)
const TEXT_DISABLED := Color8(150, 146, 162)
const TEXT_ACCENT := Color8(196, 96, 40)
const TEXT_VALUE := Color8(54, 96, 160)

## Diálogo: até 3 linhas de até 288 px.
const DIALOG_TEXT_WIDTH := 288.0
const DIALOG_LINES := 3
## Menus: largura útil de um rótulo e de um valor (configurações).
const MENU_LABEL_WIDTH := 160.0
const MENU_VALUE_WIDTH := 90.0
## Folga exigida para traduções mais longas (PT-BR é a origem).
const TEXT_GROWTH := 1.3

static var _font: Font
static var _theme: Theme


static func font() -> Font:
	if _font == null:
		var f: FontFile = load(FONT_PATH)
		f.fixed_size_scale_mode = TextServer.FIXED_SIZE_SCALE_INTEGER_ONLY
		_font = f
	return _font


static func frame(kind: String = "light") -> StyleBoxTexture:
	var sb := StyleBoxTexture.new()
	sb.texture = load("res://assets/ui/frame_%s.png" % kind)
	for side in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]:
		sb.set_texture_margin(side, 6)
	sb.content_margin_left = 7
	sb.content_margin_right = 7
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	return sb


static func build() -> Theme:
	if _theme:
		return _theme
	var t := Theme.new()
	t.default_font = font()
	t.default_font_size = FONT_SIZE
	t.set_color("font_color", "Label", TEXT_DARK)
	t.set_constant("line_spacing", "Label", 0)
	t.set_stylebox("panel", "PanelContainer", frame("light"))
	t.set_stylebox("panel", "Panel", frame("light"))
	t.set_constant("separation", "VBoxContainer", 1)
	t.set_constant("separation", "HBoxContainer", 2)
	_theme = t
	return t


static func label(text: String = "", color: Color = TEXT_DARK) -> Label:
	var l := Label.new()
	l.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	l.text = text
	l.add_theme_color_override("font_color", color)
	return l


static func text_width(text: String) -> float:
	return font().get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, FONT_SIZE).x
