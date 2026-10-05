class_name Ossuary
extends RefCounted
## Ossário e marcador de recrutamento, guardados em SaveGame.data["ossuary"]:
##   {espécie: {seen, defeated, recruited, golden_seen, golden_recruited, marker, golden_right}}
## Regras (seção 8): cada vitória sobre um selvagem soma 20–50% ao marcador da
## espécie (raridade e diferença de idade); derrotar um Golden soma +99%. Em 100%
## ele pede para entrar. Se um Golden deixou o marcador em 99%, a próxima vitória
## sobre a espécie completa e oferece a versão Golden ("direito ao Golden").


static func entry(species: String) -> Dictionary:
	if not SaveGame.data.has("ossuary"):
		SaveGame.data["ossuary"] = {}
	var o: Dictionary = SaveGame.data["ossuary"]
	if not o.has(species):
		o[species] = {"seen": false, "defeated": false, "recruited": false, "golden_seen": false,
			"golden_recruited": false, "marker": 0, "golden_right": false}
	return o[species]


static func mark_seen(m: Monster) -> void:
	var e := entry(m.species_id)
	e["seen"] = true
	if m.golden:
		e["golden_seen"] = true


static func marker_gain(m: Monster, party_level: float) -> int:
	var r: Dictionary = Data.battle_rules().get("marker", {})
	if m.golden:
		return int(Data.battle_rules().get("golden", {}).get("marker_bonus", 99))
	var base := int(r.get("by_rarity", {}).get(str(m.info().get("rarity", "comum")), 30))
	var above := maxf(0.0, m.level - party_level)
	var gain := base + int(above * float(r.get("per_level_above", 2)))
	return clampi(gain, int(r.get("min", 20)), int(r.get("max", 50)))


## Registra a vitória sobre um selvagem. Devolve {"species", "before", "after", "offer", "golden"}.
static func register_win(m: Monster, party_level: float) -> Dictionary:
	var e := entry(m.species_id)
	e["seen"] = true
	e["defeated"] = true
	var before := int(e["marker"])
	if m.golden:
		e["golden_right"] = true
	var after := mini(100, before + marker_gain(m, party_level))
	e["marker"] = after
	return {"species": m.species_id, "before": before, "after": after, "offer": after >= 100,
		"golden": bool(e["golden_right"]), "level": m.level}


## O jogador aceitou: cria o recruta (Golden se havia direito) e zera o marcador.
static func accept(species: String, level: int) -> Monster:
	var e := entry(species)
	var golden := bool(e["golden_right"])
	var m := Monster.create(species, level, golden)
	e["marker"] = 0
	e["golden_right"] = false
	e["recruited"] = true
	if golden:
		e["golden_recruited"] = true
	return m


static func refuse(species: String) -> void:
	var r: Dictionary = Data.battle_rules().get("marker", {})
	if not bool(r.get("refuse_keeps", true)):
		entry(species)["marker"] = 0


## Coloca o recruta na equipe (até 4) ou no Rancho. Devolve "party" ou "ranch".
static func add_to_team(m: Monster) -> String:
	if not SaveGame.data.has("party"):
		SaveGame.data["party"] = []
	if not SaveGame.data.has("ranch"):
		SaveGame.data["ranch"] = []
	var size := int(Data.battle_rules().get("party_size", 4))
	if SaveGame.data["party"].size() < size:
		SaveGame.data["party"].append(m.to_dict())
		return "party"
	SaveGame.data["ranch"].append(m.to_dict())
	return "ranch"


## Percentual de conclusão (só espécies reais; bonecos de teste não contam).
static func completion() -> Dictionary:
	var ids := Data.all_species_ids(false)
	var total := ids.size()
	var seen := 0
	var recruited := 0
	var golden := 0
	for id in ids:
		var e: Dictionary = SaveGame.data.get("ossuary", {}).get(id, {})
		if e.get("seen", false):
			seen += 1
		if e.get("recruited", false):
			recruited += 1
		if e.get("golden_recruited", false):
			golden += 1
	return {"total": total, "seen": seen, "recruited": recruited, "golden": golden,
		"percent": 0 if total == 0 else int(round(100.0 * recruited / total))}


## Sorteio de Golden para um selvagem (1/40 por padrão; nunca para domadores e chefes).
static func roll_golden(rng: RandomNumberGenerator, battle_kind: String = "wild") -> bool:
	if battle_kind != "wild":
		return false
	return rng.randf() < float(Data.battle_rules().get("golden", {}).get("chance", 0.025))
