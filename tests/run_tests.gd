extends Node
## Executa todos os tests/test_*.gd em modo headless e sai com código 1 se algo falhar.
## Uso: godot --headless res://tests/run_tests.tscn

const TestCase := preload("res://tests/test_case.gd")


func _ready() -> void:
	# isola configurações e save dos testes
	Settings.path = "user://test_settings.json"
	SaveGame.save_path = "user://test_save.json"
	SaveGame.backup_path = "user://test_save.bak.json"
	SaveGame.tmp_path = "user://test_save.tmp"
	var files := []
	for f in DirAccess.get_files_at("res://tests"):
		if f.begins_with("test_") and f.ends_with(".gd") and f != "test_case.gd":
			files.append(f)
	files.sort()
	# --only=parte_do_nome roda só os arquivos que contêm o texto
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--only="):
			var only := a.substr(7)
			files = files.filter(func(f: String) -> bool: return f.contains(only))
	var total_fail := 0
	var total_checks := 0
	for f in files:
		var script: GDScript = load("res://tests/" + f)
		if script == null or not script.can_instantiate():
			printerr("FALHOU  ", f, ": não compila")
			total_fail += 1
			continue
		var t = script.new()
		if t.has_method("set_tree"):
			t.set_tree(get_tree(), self)
		for m in script.get_script_method_list():
			var mname: String = m["name"]
			if not mname.begins_with("test_"):
				continue
			t.current = "%s::%s" % [f, mname]
			await t.call(mname)
		total_checks += t.checks
		for fail in t.failures:
			printerr("FALHOU  ", fail)
		total_fail += t.failures.size()
		print("%-28s %3d verificações, %d falhas" % [f, t.checks, t.failures.size()])
	print("TOTAL: %d verificações, %d falhas" % [total_checks, total_fail])
	for p in ["user://test_settings.json", "user://test_save.json", "user://test_save.bak.json"]:
		if FileAccess.file_exists(p):
			DirAccess.remove_absolute(p)
	get_tree().quit(1 if total_fail > 0 else 0)
