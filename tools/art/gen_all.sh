#!/usr/bin/env bash
# Regenera toda a arte e os sons do projeto a partir dos scripts.
set -euo pipefail
cd "$(dirname "$0")"
python3 gen_font.py
python3 gen_tiles.py
python3 gen_chars.py
python3 gen_props.py
python3 gen_ui.py
python3 gen_sfx.py
python3 gen_battle.py
python3 gen_title.py
