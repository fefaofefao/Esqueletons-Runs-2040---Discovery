class_name Monster
extends RefCounted
## Um esqueleto (do jogador ou inimigo): espécie, nível, XP, atributos, PV,
## golpes com PP, status (veneno) e estágios de atributo da batalha.
## Serializa para o save com to_dict/from_dict.

const STATS: Array[String] = ["hp", "atk", "mag", "def", "res", "spd"]

static var _next_uid := 1

var uid := 0
var species_id := ""
var nickname := ""
var level := 1
var xp := 0
var hp := 1
var moves: Array = []  # [{"id": String, "pp": int}]
var poison_turns := 0
var golden := false
## Só durante a batalha
var stages := {}
var side := 0
var participated := false


static func create(species: String, lvl: int, golden_flag: bool = false) -> Monster:
	var m := Monster.new()
	m.uid = _next_uid
	_next_uid += 1
	m.species_id = species
	m.level = clampi(lvl, 1, int(Data.battle_rules().get("level_max", 50)))
	m.xp = xp_for_level(m.level)
	m.golden = golden_flag
	m.moves = []
	for mid in learnset_up_to(species, m.level).slice(-4):
		m.moves.append({"id": mid, "pp": int(Data.move(mid).get("pp", 10))})
	m.hp = m.max_hp()
	return m


static func from_dict(d: Dictionary) -> Monster:
	var m := Monster.new()
	m.uid = int(d.get("uid", 0))
	if m.uid == 0:
		m.uid = _next_uid
	_next_uid = maxi(_next_uid, m.uid + 1)
	m.species_id = str(d.get("species", ""))
	m.nickname = str(d.get("nickname", ""))
	m.level = int(d.get("level", 1))
	m.xp = int(d.get("xp", xp_for_level(m.level)))
	m.golden = bool(d.get("golden", false))
	m.moves = []
	for mv in d.get("moves", []):
		m.moves.append({"id": str(mv["id"]), "pp": int(mv.get("pp", 0))})
	m.poison_turns = int(d.get("poison_turns", 0))
	m.hp = clampi(int(d.get("hp", m.max_hp())), 0, m.max_hp())
	return m


func to_dict() -> Dictionary:
	return {"uid": uid, "species": species_id, "nickname": nickname, "level": level, "xp": xp,
		"hp": hp, "moves": moves.duplicate(true), "poison_turns": poison_turns, "golden": golden}


func info() -> Dictionary:
	return Data.species(species_id)


func display_name() -> String:
	if nickname != "":
		return nickname
	var n := TranslationServer.translate(str(info().get("name_key", species_id)))
	return n


func type() -> String:
	return str(info().get("type", "fisico"))


func base_stat(stat: String) -> int:
	var base = info().get("base", info().get("stats", {}))
	return int(base.get(stat, 50))


## Atributo calculado pelo nível (sem estágios). Golden: +10% em todos.
func stat(s: String) -> int:
	var rules: Dictionary = Data.battle_rules().get("stat_formula", {})
	var b := base_stat(s)
	var v: int
	if s == "hp":
		v = int(2 * b * level / 100.0) + level * int(rules.get("hp_add_level", 1)) + int(rules.get("hp_add", 10))
	else:
		v = int(2 * b * level / 100.0) + int(rules.get("stat_add", 5))
	if golden:
		v = int(round(v * 1.1))
	return v


func max_hp() -> int:
	return stat("hp")


## Atributo efetivo na batalha (com estágios -3..+3).
func battle_stat(s: String) -> float:
	return stat(s) * stage_multiplier(int(stages.get(s, 0)))


static func stage_multiplier(stage: int) -> float:
	return (2.0 + stage) / 2.0 if stage >= 0 else 2.0 / (2.0 - stage)


func is_fainted() -> bool:
	return hp <= 0


func is_poisoned() -> bool:
	return poison_turns > 0


func hp_ratio() -> float:
	return float(hp) / maxf(1.0, float(max_hp()))


func reset_battle_state() -> void:
	stages = {}
	participated = false


func heal_full() -> void:
	hp = max_hp()
	poison_turns = 0
	for mv in moves:
		mv["pp"] = int(Data.move(str(mv["id"])).get("pp", 10))


# ------------------------------------------------------------ XP e níveis
static func xp_for_level(n: int) -> int:
	var k := float(Data.battle_rules().get("xp", {}).get("curve_k", 0.8))
	return int(k * pow(maxf(n, 1) - 1, 3)) if n > 1 else 0


func xp_to_next() -> int:
	return xp_for_level(level + 1) - xp


## Golpes aprendidos até o nível (ordem do learnset).
static func learnset_up_to(species: String, lvl: int) -> Array:
	var out := []
	for entry in Data.species(species).get("learnset", []):
		if int(entry[0]) <= lvl and not out.has(str(entry[1])):
			out.append(str(entry[1]))
	return out


static func moves_learned_at(species: String, lvl: int) -> Array:
	var out := []
	for entry in Data.species(species).get("learnset", []):
		if int(entry[0]) == lvl:
			out.append(str(entry[1]))
	return out


func knows(move_id: String) -> bool:
	for mv in moves:
		if mv["id"] == move_id:
			return true
	return false


## Soma XP e devolve a lista de níveis alcançados (o PV sobe junto com o máximo).
func gain_xp(amount: int) -> Array:
	var reached := []
	var cap := int(Data.battle_rules().get("level_max", 50))
	xp += amount
	while level < cap and xp >= xp_for_level(level + 1):
		var old_max := max_hp()
		level += 1
		hp = mini(max_hp(), hp + (max_hp() - old_max)) if hp > 0 else 0
		reached.append(level)
	if level >= cap:
		xp = mini(xp, xp_for_level(cap))
	return reached
