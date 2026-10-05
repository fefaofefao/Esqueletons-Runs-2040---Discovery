#!/usr/bin/env python3
"""Regera todas as regiões da fase 4c em diante, na ordem certa.
O Castelo roda por último porque liga o pós-jogo às regiões anteriores
(farol aceso na Praia e os ecos dos Guardiões). O refine.py fecha a fila:
bordas orgânicas, copas e detalhes em todos os mapas externos."""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ["minas", "pantano", "ossorio", "picos", "deserto", "castelo", "extras", "refine"]

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE))
    for name in ORDER:
        runpy.run_path(str(HERE / f"{name}.py"), run_name="__main__")
