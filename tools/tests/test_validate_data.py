"""Garante que o validate_data.py realmente pega os erros (dados quebrados de propósito)."""
import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_validator(root: Path):
    spec = importlib.util.spec_from_file_location("validate_data", ROOT / "tools" / "validate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = root
    mod.DATA = root / "data"
    return mod


class ValidateDataTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for d in ("data", "i18n", "config", "scripts", "assets"):
            shutil.copytree(ROOT / d, self.tmp / d)
        shutil.copy(ROOT / "project.godot", self.tmp / "project.godot")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_validator(self):
        mod = load_validator(self.tmp)
        code = mod.main()
        return code, "\n".join(mod.errors)

    def test_current_data_is_valid(self):
        code, errs = self.run_validator()
        self.assertEqual(code, 0, errs)

    def test_untranslated_key_fails(self):
        path = self.tmp / "i18n" / "ui.csv"
        rows = list(csv.reader(path.open(encoding="utf-8")))
        rows.append(["TEST_KEY", "Olá mundo", "Olá mundo", ""])
        with path.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(rows)
        code, errs = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("TEST_KEY em en igual ao PT-BR", errs)
        self.assertIn("TEST_KEY vazia em es", errs)

    def test_species_rules(self):
        def stage(i, s, n, total):
            per = total // 6
            return {"id": f"{s}_{i}", "name_key": n, "stats": {k: per for k in ["hp", "atk", "mag", "def", "res", "spd"]}}
        lines = []
        for i in range(23):  # 23 linhas -> 69 + 7 + 1 = 77 espécies
            lines.append({"id": f"l{i}", "type": "fisico", "region": "bosque", "growth_levels": [30, 14],
                          "signature_move": "golpe_x", "stages": [stage(1, f"l{i}", "MENU_NEW_GAME", 300),
                                                                  stage(2, f"l{i}", "MENU_NEW_GAME", 400),
                                                                  stage(3, f"l{i}", "MENU_NEW_GAME", 900)]})
        (self.tmp / "data" / "species.json").write_text(json.dumps({"lines": lines, "uniques": [], "king": None}))
        code, errs = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("total 69", errs)
        self.assertIn("fora de ordem", errs)
        self.assertIn("fora da banda", errs)
        self.assertIn("tipo magico com 0 linhas", errs)
        self.assertIn("golpe assinatura golpe_x repetido", errs)
        self.assertIn("prefixo", errs)

    def test_city_and_route_rules(self):
        (self.tmp / "data" / "cities.json").write_text(json.dumps({"cities": [
            {"id": "vila", "ranch": False, "shop": "", "tamer_houses": ["a"], "npcs": ["x"]}]}))
        (self.tmp / "data" / "routes.json").write_text(json.dumps({"routes": [{"id": "r1", "paths": [{"kind": "wild"}]}]}))
        code, errs = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("sem rancho", errs)
        self.assertIn("sem loja", errs)
        self.assertIn("casas de domadores", errs)
        self.assertIn("sem caminho alternativo", errs)

    def test_broken_map_reference(self):
        path = self.tmp / "data" / "maps" / "praia_despertar.json"
        m = json.loads(path.read_text(encoding="utf-8"))
        m["warps"].append({"x": 22, "y": 18, "to": "lugar_nenhum", "tx": 0, "ty": 0})
        m["props"].append({"type": "prop_que_nao_existe", "x": 5, "y": 15})
        path.write_text(json.dumps(m))
        code, errs = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("lugar_nenhum", errs)
        self.assertIn("prop_que_nao_existe", errs)


    def test_progression_rules(self):
        path = self.tmp / "data" / "encounters.json"
        enc = json.loads(path.read_text(encoding="utf-8"))
        for t in ("rota1_sul", "rota1_oeste", "rota1_campo", "rota1_norte", "tunel"):
            for e in enc["tables"][t]:  # salto logo depois do Brás
                e["min_level"], e["max_level"] = 13, 14
        enc["tables"]["tunel"][0]["max_level"] = 21      # quase a idade do Ramalho
        path.write_text(json.dumps(enc))
        code, errs = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("bosque começa com selvagens de", errs)
        self.assertIn("tunel tem flautista_1 com 21 anos", errs)

if __name__ == "__main__":
    unittest.main()
