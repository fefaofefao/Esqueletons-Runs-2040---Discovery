class_name ScriptActions
extends RefCounted
## Ações de roteiro usadas nos diálogos ({"action": ...}). Formato em docs/DADOS.md.
##   give_partner {species, age, nickname, flag}  dá o parceiro inicial (fixo)
##   battle {kind, enemies, tamer_key, reward, items, win_flag, tips, marker}
##   heal                                         cura toda a equipe
##   give_item {item, n}  ·  give_money {n}  ·  marker {species, amount}
##   ranch  ·  shop {id}  ·  respawn (Rancho atual vira o ponto de volta)
##   hide_npc {id}                                o NPC some (para sempre)
##   sfx {name}
## run() devolve false se o roteiro deve parar (ex.: derrota na batalha).


static func run(n: Dictionary) -> bool:
	match str(n.get("action", "")):
		"give_partner":
			var m := Monster.create(str(n.species), int(n.get("age", 5)))
			m.nickname = TranslationServer.translate(str(n.get("nickname", "")))
			var party: Array = SaveGame.data.get("party", [])
			party.insert(0, m.to_dict())
			SaveGame.data["party"] = party
			SaveGame.data["partner_uid"] = m.uid
			Ossuary.mark_seen(m)
			Ossuary.entry(m.species_id)["recruited"] = true
			if n.has("flag"):
				SaveGame.set_flag(str(n.flag))
			Audio.sfx("recruit")
		"battle":
			var info := {"kind": str(n.get("kind", "tamer")), "enemies": n.get("enemies", []),
				"tamer_key": str(n.get("tamer_key", "BTL_TAMER_DEFAULT")), "reward": int(n.get("reward", 0)),
				"tips": n.get("tips", [])}
			var result: String = await Game.start_battle(info)
			if result != "win":
				return false
			if n.has("win_flag"):
				SaveGame.set_flag(str(n.win_flag))
			for it in n.get("items", []):
				_add_item(str(it[0]), int(it[1]))
				await Game.show_message("MSG_GOT_ITEM", {"item": TranslationServer.translate(str(Data.item(str(it[0])).get("name_key", ""))), "n": int(it[1])})
			if n.has("marker"):
				await _marker(str(n.marker.species), int(n.marker.amount))
		"heal":
			for key in ["party"]:
				var arr: Array = SaveGame.data.get(key, [])
				for i in arr.size():
					var mm := Monster.from_dict(arr[i])
					mm.heal_full()
					arr[i] = mm.to_dict()
			Audio.sfx("heal")
		"give_item":
			_add_item(str(n.item), int(n.get("n", 1)))
			Audio.sfx("save")
			await Game.show_message("MSG_GOT_ITEM", {"item": TranslationServer.translate(str(Data.item(str(n.item)).get("name_key", ""))), "n": int(n.get("n", 1))})
		"give_money":
			SaveGame.data["money"] = int(SaveGame.data.get("money", 0)) + int(n.n)
			Audio.sfx("save")
			await Game.show_message("MSG_GOT_MONEY", {"n": int(n.n)})
		"marker":
			await _marker(str(n.species), int(n.amount))
		"ranch":
			var r := RanchMenu.new()
			Game.open_overlay(r)
			await r.closed
		"shop":
			var s := ShopMenu.new().setup(str(n.id))
			Game.open_overlay(s)
			await s.closed
		"respawn":
			if Game.world and Game.world.player:
				SaveGame.data["respawn"] = {"map": Game.world.map_id, "x": Game.world.player.cell.x,
					"y": Game.world.player.cell.y, "facing": Game.world.player.facing}
		"hide_npc":
			SaveGame.set_flag("npc_gone_" + str(n.id))
			if Game.world and Game.world.map:
				Game.world.map.remove_npc(str(n.id))
		"sfx":
			Audio.sfx(str(n.name))
		_:
			push_warning("ScriptActions: ação desconhecida %s" % str(n.get("action", "")))
	return true


static func _add_item(id: String, count: int) -> void:
	if not SaveGame.data.has("bag"):
		SaveGame.data["bag"] = {}
	SaveGame.data["bag"][id] = int(SaveGame.data["bag"].get(id, 0)) + count


static func _marker(species: String, amount: int) -> void:
	var e := Ossuary.entry(species)
	var before := int(e["marker"])
	e["seen"] = true
	e["marker"] = mini(100, before + amount)
	await Game.show_message("RECRUIT_MARKER", {"name": TranslationServer.translate(str(Data.species(species).get("name_key", ""))), "a": before, "b": int(e["marker"])})
