# Créditos e licenças

## Conteúdo do jogo
Todo o conteúdo abaixo é **original**, criado para este projeto. Nenhum pack ou asset de terceiros foi usado. Cada arquivo é gerado por um script versionado, que serve de registro de origem.

| Arquivo(s) | Origem | Licença |
|---|---|---|
| `assets/fonts/pixel.fnt`, `pixel.png` (fonte "OssosPixel") | `tools/art/gen_font.py`, glifos desenhados à mão | Original do projeto |
| `assets/tiles/overworld.png`, `data/tilesets/overworld.json` | `tools/art/gen_tiles.py` | Original do projeto |
| `assets/sprites/player.png`, `bento.png`, `shadow.png` | `tools/art/gen_chars.py`, pixel art em ASCII | Original do projeto |
| `assets/props/props.png`, `data/props.json` | `tools/art/gen_props.py` | Original do projeto |
| `assets/ui/*`, `assets/icons/*`, `icon.png` | `tools/art/gen_ui.py` | Original do projeto |
| `assets/sfx/*.wav` | `tools/art/gen_sfx.py` (síntese chiptune) | Original do projeto |
| Textos e traduções (`i18n/*.csv`) | escritos para o jogo | Original do projeto |

Música: ainda não há (fase 6). Toda faixa adicionada deve ser registrada aqui, com origem e licença (original ou CC0).

## Motor
**Godot Engine** — licença MIT.
Copyright (c) 2014-present Godot Engine contributors.
Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.
O aviso completo da licença e as licenças de terceiros embutidas no motor serão exibidos na tela de créditos do jogo (fase 6).

## Ferramentas de desenvolvimento (não vão no jogo)
- Python 3 e Pillow (HPND), usados só para gerar a arte.
