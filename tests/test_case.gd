extends RefCounted
## Base mínima dos testes headless (sem dependências externas).

var failures: Array[String] = []
var checks := 0
var current := ""


func check(cond: bool, msg: String) -> void:
	checks += 1
	if not cond:
		failures.append("%s: %s" % [current, msg])


func check_eq(actual: Variant, expected: Variant, msg: String = "") -> void:
	check(actual == expected, "%s (esperado %s, obtido %s)" % [msg, str(expected), str(actual)])


## Lê um CSV de tradução: {chave: {"pt_BR": ..., "en": ..., "es": ...}}
static func read_csv(path: String) -> Dictionary:
	var out := {}
	var f := FileAccess.open(path, FileAccess.READ)
	var header := f.get_csv_line()
	while not f.eof_reached():
		var row := f.get_csv_line()
		if row.size() < header.size() or row[0] == "":
			continue
		var entry := {}
		for i in range(1, header.size()):
			entry[header[i]] = row[i]
		out[row[0]] = entry
	return out


static func all_translations() -> Dictionary:
	var out := {}
	for f in DirAccess.get_files_at("res://i18n"):
		if f.ends_with(".csv"):
			out.merge(read_csv("res://i18n/" + f))
	return out
