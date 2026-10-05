extends "res://tests/test_case.gd"
## Movimento em grade com frames reais: virar, andar, correr, colidir e porta.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


## Espera em tempo real (não escala com o 2x).
func _wait(s: float) -> void:
	await tree.create_timer(s, true, false, true).timeout


func _press(action: String, pressed: bool) -> void:
	Controls.emit_action(action, pressed)
	Input.flush_buffered_events()


func test_walk_turn_bump_and_door() -> void:
	SaveGame.start_new("Téo")
	Speed.set_fast(false)
	var w := World.new()
	host.add_child(w)
	Game.world = w
	w.load_map("praia_despertar", Vector2i(22, 18), "up")
	var p := w.player
	# toque rápido só vira
	_press("move_right", true)
	await _wait(0.04)
	_press("move_right", false)
	await _wait(0.1)
	check_eq(p.facing, "right", "toque rápido vira")
	check_eq(p.cell, Vector2i(22, 18), "toque rápido não anda")
	# segurar anda
	_press("move_right", true)
	await _wait(0.75)
	_press("move_right", false)
	await _wait(0.35)
	check(p.cell.x >= 24, "segurar anda pelo menos 2 casas (x=%d)" % p.cell.x)
	check_eq(p.position, MapView.cell_to_pos(p.cell), "termina alinhado à grade")
	# correr com B é mais rápido
	var start := p.cell.x
	_press("btn_b", true)
	_press("move_left", true)
	await _wait(0.5)
	_press("move_left", false)
	_press("btn_b", false)
	await _wait(0.3)
	check(start - p.cell.x >= 3, "correndo anda ~2x mais (andou %d)" % (start - p.cell.x))
	# colisão com a água
	p.place(Vector2i(20, 20), "down")
	_press("move_down", true)
	await _wait(0.5)
	_press("move_down", false)
	await _wait(0.1)
	check_eq(p.cell, Vector2i(20, 20), "água bloqueia")
	# 2x acelera o movimento
	p.place(Vector2i(14, 15), "right")
	Speed.set_fast(true)
	_press("move_right", true)
	await _wait(0.75)
	_press("move_right", false)
	await _wait(0.2)
	Speed.set_fast(false)
	check(p.cell.x - 14 >= 5, "no 2x anda o dobro (andou %d)" % (p.cell.x - 14))
	# porta da cabana
	p.place(Vector2i(35, 11), "up")
	_press("move_up", true)
	await _wait(0.5)
	_press("move_up", false)
	await _wait(0.3)
	check_eq(w.map_id, "cabana_bento", "porta leva para dentro da cabana")
	# segurando "cima" ele continua andando depois da porta, como esperado
	check(w.player.cell.x == 6 and w.player.cell.y <= 8, "chega pela célula de destino (%s)" % w.player.cell)
	check_eq(str(SaveGame.data.player.map), "cabana_bento", "posição salva no save")
	Game.world = null
	w.queue_free()
	await _wait(0.05)


## Bug relatado no celular: ao fechar uma conversa, ela começava de novo
## sozinha. O mesmo toque no A chegava duas vezes (clique emulado no diálogo +
## ação btn_a no mapa). Aqui: fecha a conversa com A e manda outro A logo em
## seguida — a conversa não pode reabrir. Depois do intervalo, A fala de novo.
func test_dialog_does_not_reopen_after_closing() -> void:
	SaveGame.start_new("Téo")
	for f in ["intro_done", "bento_met", "has_partner", "partner_lia"]:
		SaveGame.set_flag(f)
	Speed.set_fast(false)
	var w := World.new()
	host.add_child(w)
	Game.world = w
	w.load_map("vila_mare", Vector2i(17, 17), "up")   # Pipa está em (17, 16)
	await _wait(0.2)
	var p := w.player
	check(w.map.npc_at(Vector2i(17, 16)) != null, "há um NPC na frente")
	_press("btn_a", true)
	_press("btn_a", false)
	await _wait(0.3)
	check(Game.top_overlay() is DialogBox, "A abre a conversa")
	# fecha a conversa (pode ter mais de uma caixa)
	for i in 12:
		if not (Game.top_overlay() is DialogBox):
			break
		var box := Game.top_overlay() as DialogBox
		if box._typing:
			box._press()
		box._press()
		await tree.process_frame
	check(Game.top_overlay() == null, "conversa fechada")
	# o "segundo" A do mesmo toque, logo depois de fechar
	_press("btn_a", true)
	_press("btn_a", false)
	await _wait(0.1)
	check(Game.top_overlay() == null, "a conversa NÃO reabre sozinha")
	await _wait(0.4)
	_press("btn_a", true)
	_press("btn_a", false)
	await _wait(0.2)
	check(Game.top_overlay() is DialogBox, "depois do intervalo, A fala de novo normalmente")
	Game.close_all_overlays()
	check(p != null, "jogador existe")
	Game.world = null
	w.queue_free()
	await tree.process_frame
