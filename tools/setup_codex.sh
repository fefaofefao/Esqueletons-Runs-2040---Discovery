#!/usr/bin/env bash
# Prepara um ambiente Linux (Codex, CI local ou máquina nova) para validar o projeto:
#   - Godot 4.7.2 (headless) em ~/.local/bin/godot
#   - (opcional) export templates, para exportar o APK localmente: --with-templates
#   - dependências Python das ferramentas (Pillow, só para regenerar a arte)
# O Android SDK não é instalado aqui: o APK/AAB oficial sai do GitHub Actions.
set -euo pipefail

GODOT_RELEASE="4.7.2-stable"
TEMPLATES_DIR="4.7.2.stable"
BIN="$HOME/.local/bin"
mkdir -p "$BIN"

if ! command -v godot >/dev/null 2>&1; then
  echo ">> Baixando Godot ${GODOT_RELEASE}"
  curl -fsSL --retry 4 -o /tmp/godot.zip "https://github.com/godotengine/godot/releases/download/${GODOT_RELEASE}/Godot_v${GODOT_RELEASE}_linux.x86_64.zip"
  unzip -q -o /tmp/godot.zip -d /tmp/godot
  mv -f "/tmp/godot/Godot_v${GODOT_RELEASE}_linux.x86_64" "$BIN/godot"
  chmod +x "$BIN/godot"
  rm -rf /tmp/godot /tmp/godot.zip
fi

if [[ "${1:-}" == "--with-templates" ]]; then
  DEST="$HOME/.local/share/godot/export_templates/${TEMPLATES_DIR}"
  if [[ ! -d "$DEST" ]]; then
    echo ">> Baixando export templates"
    curl -fsSL --retry 4 -o /tmp/templates.tpz "https://github.com/godotengine/godot/releases/download/${GODOT_RELEASE}/Godot_v${GODOT_RELEASE}_export_templates.tpz"
    unzip -q -o /tmp/templates.tpz -d /tmp/tpl
    mkdir -p "$(dirname "$DEST")"
    mv /tmp/tpl/templates "$DEST"
    rm -rf /tmp/tpl /tmp/templates.tpz
  fi
fi

python3 -m pip install -q -r "$(dirname "$0")/requirements.txt" || echo "aviso: pip falhou (só necessário para regenerar arte)"

cd "$(dirname "$0")/.."
echo ">> Importando o projeto"
"$BIN/godot" --headless --import >/dev/null 2>&1 || godot --headless --import >/dev/null 2>&1
echo ">> Pronto. Verificação completa: tools/check_all.sh"
