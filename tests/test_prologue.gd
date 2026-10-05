extends "res://tests/test_case.gd"
## Fase 4a: roteiros do Prólogo rodando de verdade (diálogo + ações), com um
## "jogador automático" que avança as falas e escolhe opções.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


## Roda um roteiro até o fim, escolhendo as opções na ordem dada.
func _play(ref: String, choices: Array = []) -> void:
	var done := [false]
	var runner := func() -> void:
		await Game.play_script(Data.dialog(ref))
		done[0] = true
	runner.call()
	var start := Time.get_ticks_msec()
	while not done[0] and Time.get_ticks_msec() - start < 8000:
		await tree.process_frame
		var top := Game.top_overlay()
		if top is DialogBox:
			var box := top as DialogBox
			if box._waiting_choice and box._choice:
				box._choice.index = int(choices.pop_front()) if not choices.is_empty() else 0
				box._choice.activate_current()
			elif box.accepts_input():
				box._press()
		elif top != null:
			top.close()
	check(done[0], "roteiro %s termina" % ref)


func test_partner_choice_lia() -> void:
	SaveGame.start_new("Téo")
	await _play("prologo/despertar")
	check(SaveGame.get_flag("intro_done"), "despertar marca intro_done")
	check_eq(int(SaveGame.data.get("bag", {}).get("ingresso", 0)), 1, "ganha o Ingresso Amassado")
	await _play("prologo/bento_primeira", [1])
	check(SaveGame.get_flag("bento_met"), "conhece o Bento")
	await _play("prologo/escolha", [0])
	var party: Array = SaveGame.data.get("party", [])
	check_eq(party.size(), 1, "um parceiro")
	check_eq(str(party[0].species), "faroleira_1", "Lia é Faroleira bebê")
	check_eq(str(party[0].nickname), "Lia", "apelido Lia")
	check_eq(int(party[0].level), 5, "5 anos")
	check(SaveGame.get_flag("partner_lia") and SaveGame.get_flag("has_partner"), "flags do parceiro")
	check(SaveGame.get_flag("npc_gone_lia_cabana") and SaveGame.get_flag("npc_gone_taro_cabana"), "os dois saem da cabana")
	check_eq(int(SaveGame.data.bag.get("pocao_p", 0)), 3, "3 Poções P do Bento")


func test_partner_choice_taro() -> void:
	SaveGame.start_new("Téo")
	await _play("prologo/escolha", [1])
	check_eq(str(SaveGame.data.party[0].species), "grumete_1", "Taro é Grumete bebê")
	check(SaveGame.get_flag("partner_taro"), "flag partner_taro")


func test_jurema_quest() -> void:
	SaveGame.start_new("Téo")
	await _play("vila_mare/jurema_pede")
	check(SaveGame.get_flag("jurema_quest"), "missão aceita")
	await _play("prologo/rede")
	check(SaveGame.get_flag("jurema_net"), "rede solta")
	await _play("vila_mare/jurema_obrigada")
	check(SaveGame.get_flag("jurema_done"), "missão concluída")
	check_eq(int(SaveGame.data.bag.get("antidoto", 0)), 1, "recompensa: antídoto")
	check_eq(int(SaveGame.data.bag.get("pocao_p", 0)), 2, "recompensa: 2 poções")


func test_npc_dialog_order() -> void:
	SaveGame.start_new("Téo")
	var npc := Npc.new()
	npc.setup("jurema", {}, null)
	check_eq(npc.dialog_ref(), "vila_mare/jurema_pede", "Jurema pede a rede primeiro")
	SaveGame.set_flag("jurema_quest")
	check_eq(npc.dialog_ref(), "vila_mare/jurema_onde", "depois lembra onde é")
	SaveGame.set_flag("jurema_net")
	check_eq(npc.dialog_ref(), "vila_mare/jurema_obrigada", "com a rede, agradece")
	npc.free()
	var b := Npc.new()
	b.setup("bento", {}, null)
	check_eq(b.dialog_ref(), "prologo/bento_primeira", "Bento: 1ª conversa")
	SaveGame.set_flag("bento_met")
	check_eq(b.dialog_ref(), "prologo/bento_repete", "Bento: chama para a cabana")
	SaveGame.set_flag("has_partner")
	check_eq(b.dialog_ref(), "prologo/bento_depois", "Bento: aponta a vila")
	b.free()


func test_shop_and_bag() -> void:
	SaveGame.start_new("Téo")
	SaveGame.data["money"] = 300
	var shop := ShopMenu.new().setup("vila_mare")
	Game.open_overlay(shop)
	await tree.process_frame
	shop._buy("pocao_p")
	check_eq(int(SaveGame.data.money), 150, "compra desconta o preço")
	check_eq(int(SaveGame.data.bag.pocao_p), 1, "item vai para a mochila")
	shop._buy("reviver")
	check_eq(int(SaveGame.data.money), 150, "sem moedas, não compra")
	shop.close()
	await tree.process_frame
	var m := Monster.create("faroleira_1", 5)
	m.hp = 3
	check(BagMenu.apply_item("pocao_p", m), "poção cura")
	check(m.hp > 3, "PV sobe")
	m.heal_full()
	check(not BagMenu.apply_item("pocao_p", m), "poção sem efeito com PV cheio")
	check(not BagMenu.apply_item("antidoto", m), "antídoto sem efeito sem veneno")
	m.hp = 0
	check(BagMenu.apply_item("reviver", m), "reviver levanta quem caiu")


func test_maps_and_conditions() -> void:
	SaveGame.start_new("Téo")
	var praia := MapView.new()
	host.add_child(praia)
	praia.build("praia_despertar")
	check(praia.spawns.size() == 2, "Praia tem 2 zonas de selvagens")
	check(not MapView.condition_ok(praia.spawns[0]), "selvagens só depois do parceiro")
	check(praia.interaction_at(Vector2i(43, 19)).is_empty(), "rede da Jurema só aparece com a missão")
	praia.queue_free()
	SaveGame.set_flag("jurema_quest")
	var p2 := MapView.new()
	host.add_child(p2)
	p2.build("praia_despertar")
	check(not p2.interaction_at(Vector2i(43, 19)).is_empty(), "rede aparece com a missão")
	p2.queue_free()
	var vila := MapView.new()
	host.add_child(vila)
	check(vila.build("vila_mare"), "Vila Maré monta")
	var bras := vila.npc_at(Vector2i(19, 4))
	check(bras != null and bras.is_tamer_active(), "Brás vigia a estrada")
	if bras:
		check(Vector2i(19, 6) in bras.vision_cells(), "Brás vê o caminho à frente")
	for id in ["vila_rancho", "vila_loja", "vila_casa_remo", "vila_casa_concha"]:
		var w: Dictionary = {}
		for ww in vila.data.warps:
			if ww.to == id:
				w = ww
		check(not w.is_empty(), "porta para %s" % id)
	vila.queue_free()
	await tree.process_frame
	check(not Data.encounter_table("praia").is_empty(), "tabela de encontro da Praia")
	for e in Data.encounter_table("praia"):
		check(int(Data.species(str(e.species)).get("stage", 0)) == 1, "Praia só tem bebês")
