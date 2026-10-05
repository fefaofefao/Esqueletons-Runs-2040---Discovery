class_name TextFit
extends RefCounted
## Quebra de linha e paginação com a fonte real. Usado pela caixa de diálogo e
## pelo teste de overflow, para que os dois concordem sempre.


static func wrap_lines(text: String, width: float, font: Font = null, size: int = UiTheme.FONT_SIZE) -> PackedStringArray:
	if font == null:
		font = UiTheme.font()
	var lines := PackedStringArray()
	for paragraph in text.split("\n"):
		var current := ""
		for word in paragraph.split(" ", false):
			var candidate: String = word if current == "" else current + " " + word
			if _w(candidate, font, size) <= width:
				current = candidate
				continue
			if current != "":
				lines.append(current)
			current = word
			# palavra sozinha mais larga que a linha: quebra por caractere
			while _w(current, font, size) > width and current.length() > 1:
				var cut := current.length() - 1
				while cut > 1 and _w(current.substr(0, cut), font, size) > width:
					cut -= 1
				lines.append(current.substr(0, cut))
				current = current.substr(cut)
		lines.append(current)
	return lines


static func paginate(text: String, width: float, lines_per_page: int) -> PackedStringArray:
	var lines := wrap_lines(text, width)
	var pages := PackedStringArray()
	var i := 0
	while i < lines.size():
		pages.append("\n".join(lines.slice(i, i + lines_per_page)))
		i += lines_per_page
	if pages.is_empty():
		pages.append("")
	return pages


static func _w(s: String, font: Font, size: int) -> float:
	return font.get_string_size(s, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
