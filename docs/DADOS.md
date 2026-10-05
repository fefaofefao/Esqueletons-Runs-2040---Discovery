# Formatos de dados

Todo conteúdo fica em JSON (`data/`) e todo texto visível é uma chave de tradução (`i18n/*.csv`). O `tools/validate_data.py` confere tudo o que está descrito aqui.

## Traduções — `i18n/*.csv`
```
keys,pt_BR,en,es
MENU_NEW_GAME,Novo jogo,New game,Nueva partida
```
- PT-BR é o idioma de origem. EN e ES não podem ficar vazios nem iguais ao PT, exceto as chaves listadas em `i18n/allow_identical.txt`.
- Placeholders `{player}`, `{v}`, `{n}`... precisam ser os mesmos nos 3 idiomas.
- Cada CSV novo precisa ser registrado em `project.godot` (`internationalization/locale/translations`); o validador avisa.
- Limites de espaço (ver `UiTheme`): diálogo com 3 linhas de 288 px; rótulo de menu com 160 px; valor com 90 px. O PT-BR precisa caber com 30% de folga.

## Regiões — `data/regions.json`
```json
{"regions": {"praia": {"name_key": "REGION_PRAIA", "act": "prologo", "tint": [1, 0.97, 0.92], "music": "", "maps": ["praia_despertar", "cabana_bento"]}}}
```
`maps` lista os mapas da região, inclusive os que ainda vão existir (portas podem apontar para eles).

## Mapas — `data/maps/<id>.json`
| Campo | Descrição |
|---|---|
| `id`, `region`, `name_key` | identificação; `name_key` aparece no letreiro |
| `tileset` | id em `data/tilesets/` (padrão `overworld`) |
| `legend` | caractere → terreno do tileset |
| `ground` | linhas de texto, todas com a mesma largura |
| `spawn` | `{x, y, facing}` |
| `props` | `{type, x, y, dialog?}`; `type` vem de `data/props.json` |
| `npcs` | `{id, x, y, facing, ...sobrescritas}`; `id` vem de `data/npcs.json` |
| `warps` | `{x, y, to, tx, ty, facing, sfx?, locked_message?}`; `tx/ty = -1` usa o spawn do destino |
| `ambient` | `sea_sparkle`, `leaves`, `dust_motes` |
| `tint`, `music`, `indoor`, `always_banner` | opcionais |

Terrenos atuais: `sand`, `water`, `deep`, `grass`, `flowers`, `path`, `bush`, `dock`, `floor`, `wall`, `wall_window`, `wall_top`, `mat`, `void`. As transições são automáticas.

## Objetos — `data/props.json` (gerado por `tools/art/gen_props.py`)
`rect` no atlas, `frames`, `fps`, `origin` (pés), `collision` (células relativas), `layer` (`y` = ordenado por profundidade, `ground` = no chão), `light` opcional.

## NPCs — `data/npcs.json`
```json
{"npcs": {"bento": {"name_key": "SPK_BENTO", "role": "lore", "sprite": "res://assets/sprites/bento.png",
  "frames": 2, "idle_fps": 1.2, "behavior": "look_around", "look_dirs": ["left", "down", "right"],
  "dialog": [{"if_not": "bento_met", "dialog": "prologo/bento_primeira"}, {"dialog": "prologo/bento_repete"}]}}}
```
`role` é obrigatório (dica, humor, lore, missão, domador), porque todo NPC precisa de uma razão para existir.

## Diálogos — `data/dialogs/<arquivo>.json`
```json
{"dialogs": {"id": [
  {"speaker": "SPK_BENTO", "say": "DLG_..."},
  {"speaker": "SPK_BENTO", "say": "DLG_...", "choice": [{"text": "OPT_...", "goto": "arquivo/id", "set_flag": "f"}]},
  {"set_flag": "bento_met"},
  {"if": "flag", "say": "..."}, {"if_not": "flag", "goto": "arquivo/id"}
]}}
```
Referência: `"arquivo/id"`. Cada caixa tem no máximo 3 linhas; textos maiores são paginados, mas o teste de overflow exige caber em uma caixa.

## Batalha (fase 2)
- `data/battle.json`: regras e constantes da seção 9 (ver `docs/DECISOES.md`).
- `data/items.json`: `{"items": {id: {name_key, desc_key, kind: heal|cure|revive|key, amount?, fraction?, price, battle, target}}}`.
- **Golpe** (`data/moves.json` na fase 3c; `data/test/moves_test.json` hoje):
  `{name_key, desc_key, type, category: physical|magical|status, power, accuracy, pp, target: enemy|all_enemies|self|ally|all_allies, priority, effects: [...]}`.
  Efeitos: `{"kind": "poison", "chance"}`, `{"kind": "stat", "stat": atk|mag|def|res|spd, "stages": ±n, "chance"}`, `{"kind": "heal", "percent"}`, `{"kind": "cure"}`.
- **Espécie usada pelo motor:** `name_key`, `type`, `base` (`hp, atk, mag, def, res, spd`; na fase 3 pode se chamar `stats`), `base_xp`, `sprite` (folha 64×32: frente 0–31, costas 32–63) e `learnset` `[[nível, golpe], ...]`.
- **Esqueleto no save** (`party`): `{uid, species, nickname, level, xp, hp, moves: [{id, pp}], poison_turns, golden}`. `bag`: `{item: quantidade}`. `respawn`: `{map, x, y, facing}`.

## Esqueletos (fase 3a)
- **Selvagens no mapa:** `spawns` no JSON do mapa, `[{id, table, x, y, radius, count, behavior?: patrol|circle|chase|shy|fast}]`. A tabela vem de `encounters.json` (teste: `data/test/encounters_test.json`), `[{species, min_level, max_level, rarity?, weight?}]`.
- **Linha de crescimento:** cada estágio tem `line`, `stage` (1–3), `growth_levels` `[idade 1→2, idade 2→3]`, `growth_move` opcional (aprendido ao crescer), `gender` (`m`/`f`, para "Dourado/Dourada") e `rarity`.
- **Save:** `ossuary` `{espécie: {seen, defeated, recruited, golden_seen, golden_recruited, marker, golden_right}}` e `ranch` (mesma forma de `party`).
- `battle.json`: `golden {chance, stat_bonus, marker_bonus}` e `marker {by_rarity, per_level_above, min, max, refuse_keeps}`.

## Formatos das próximas fases (o validador já os confere)

### `data/species.json` (gerado por `tools/bestiary/build.py`)
Campos extras usados pelo jogo: `gender`, `map_behavior`, `starter` (linha), `entry_key`, `number`, `base_xp`, `sprite` (folha 64×32), `map_sprite` (folha 32×16, 2 quadros) e, a partir da 3c, `learnset` e `growth_move` por estágio.

### Formato base
```json
{
  "lines": [{"id": "lanterneiro", "type": "fisico|magico|cura|veneno", "region": "minas", "rarity": "comum",
             "growth_levels": [16, 32], "signature_move": "golpe_id",
             "stages": [{"id": "lanterneiro_1", "name_key": "SPECIES_...", "stats": {"hp": 0, "atk": 0, "mag": 0, "def": 0, "res": 0, "spd": 0}}, {}, {}]}],
  "uniques": [{"id": "...", "type": "...", "region": "...", "name_key": "...", "stats": {}}],
  "king": {"id": "rei_esqueleto", "name_key": "...", "stats": {}}
}
```
Regras: 24 linhas × 3 estágios + 7 únicos + Rei = 80; níveis crescentes; bandas de atributos (250–320 / 360–430 / 470–540; únicos 450–520; Rei ≈ 600); 6 ± 1 linhas por tipo; assinatura única; no máximo 2 nomes com o mesmo prefixo de 3 letras por idioma; nenhum nome numerado ou descritivo.

### `data/moves.json` (fase 3c)
`{"moves": [{"id", "name_key", "type", "power", "accuracy", "pp", "target", "effect"}]}`: 16 físicos, 16 mágicos, 12 de cura e 12 de veneno.

### `data/encounters.json` (fase 4)
`{"tables": {"zona": [{"species": "lanterneiro_2", "stage": 2, "min_level": 18, "max_level": 21, "rarity": "comum"}]}}`. Estágio 2/3 nunca abaixo do nível de crescimento.

### `data/cities.json` (fase 4)
`{"cities": [{"id", "region", "ranch": true, "shop": "shop_id", "tamer_houses": [..2-3..], "npcs": [..3-6..]}]}`

### `data/routes.json` (fase 4)
`{"routes": [{"id", "from", "to", "paths": [{"kind": "tamers|wild|shortcut", "required": false}]}]}`: no mínimo 2 caminhos, nenhum obrigatório.

### `data/balance.json` (fase 3c)
Metas de nível por região, constantes de dano/XP/marcador e chance de Golden (1/40).
