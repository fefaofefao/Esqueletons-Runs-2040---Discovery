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
| `assets/title/*` (logo HD e camadas da tela inicial) | `tools/art/gen_title.py` (desenho procedural) | Original do projeto |
| `assets/sfx/*.wav` | `tools/art/gen_sfx.py` (síntese chiptune) | Original do projeto |
| Textos e traduções (`i18n/*.csv`) | escritos para o jogo | Original do projeto |

Música: ainda não há (fase 6). Toda faixa adicionada deve ser registrada aqui, com origem e licença (original ou CC0).

## Fontes de terceiros (SIL Open Font License 1.1)
| Fonte | Uso | Vai no jogo? | Licença |
|---|---|---|---|
| **Nunito** — The Nunito Project Authors | textos da tela inicial | sim (`assets/fonts/nunito/`) | OFL 1.1 (`assets/fonts/nunito/OFL.txt`) |
| **Lilita One** — Juan Montoreano | letras do logo (rasterizadas na imagem) | não, só a imagem do logo | OFL 1.1 (`tools/art/fonts/OFL-LilitaOne.txt`) |
| **Orbitron** — Matt McInerney | "2040" e "EDITION · DISCOVERY" do logo | não, só a imagem do logo | OFL 1.1 (`tools/art/fonts/OFL-Orbitron.txt`) |

## Motor
**Godot Engine** — licença MIT.
Copyright (c) 2014-present Godot Engine contributors.
Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.
O aviso completo da licença e as licenças de terceiros embutidas no motor serão exibidos na tela de créditos do jogo (fase 6).

## Ferramentas de desenvolvimento (não vão no jogo)
- Python 3 e Pillow (HPND), usados só para gerar a arte.
