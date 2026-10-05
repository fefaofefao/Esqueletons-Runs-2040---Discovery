#!/usr/bin/env bash
# Verificação local completa (a mesma do CI, sem o APK): dados, publisher, testes headless.
set -euo pipefail
cd "$(dirname "$0")/.."
GODOT="${GODOT:-$(command -v godot || echo "$HOME/.local/bin/godot")}"
python3 tools/validate_data.py
python3 -m unittest discover -s tools/tests
python3 tools/sync_publisher.py --check
python3 tools/check_placeholders.py
"$GODOT" --headless --import >/dev/null 2>&1
"$GODOT" --headless res://tests/run_tests.tscn
echo "check_all: OK"
