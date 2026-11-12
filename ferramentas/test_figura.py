#!/usr/bin/env python3
"""Testes do figura.py (licenças, expressões do gráfico, acervo) e do embutimento de imagens do montar.py.

Uso:  python3 test_figura.py        (sem rede; sai com código 1 se algum falhar)
Licença MIT.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "grifo" / "scripts"))
import json  # noqa: E402
from figura import ACERVO, avaliar_licenca, expressao_segura  # noqa: E402
from montar import embutir_figuras  # noqa: E402


class TestLicenca(unittest.TestCase):
    def test_aceitas(self):
        for lic in ["CC0", "Public domain", "PD-USGov", "CC BY 4.0", "CC BY 3.0", "CC BY-SA 3.0", "CC-BY-SA-4.0"]:
            with self.subTest(lic=lic):
                self.assertTrue(avaliar_licenca(lic)[0])

    def test_recusadas(self):
        for lic in ["", "CC BY-NC 4.0", "CC BY-NC-SA 3.0", "CC BY-ND 4.0", "GFDL", "All rights reserved"]:
            with self.subTest(lic=lic):
                self.assertFalse(avaliar_licenca(lic)[0])

    def test_by_sa_pede_sem_alteracao(self):
        self.assertIn("sem alterar", avaliar_licenca("CC BY-SA 4.0")[1])


class TestExpressao(unittest.TestCase):
    def test_calcula(self):
        import numpy as np
        f = expressao_segura("2*x^2 + sin(pi*x)")
        self.assertTrue(np.allclose(f(np.array([0.0, 1.0])), [0.0, 2.0]))

    def test_constante_vira_vetor(self):
        import numpy as np
        self.assertEqual(expressao_segura("3")(np.zeros(4)).shape, (4,))

    def test_recusa_codigo(self):
        for expr in ["__import__('os')", "x.real", "open('a')", "x[0]", "(lambda: 1)()", "'a'"]:
            with self.subTest(expr=expr):
                with self.assertRaises((ValueError, SyntaxError)):
                    expressao_segura(expr)


class TestAcervo(unittest.TestCase):
    def test_entradas_completas_e_licenca_aceita(self):
        dados = json.loads(ACERVO.read_text(encoding="utf-8"))
        titulos = set()
        for f in dados["figuras"]:
            with self.subTest(titulo=f.get("titulo")):
                for campo in ("area", "tema", "titulo", "licenca", "autor", "rotulos"):
                    self.assertTrue(f.get(campo), campo)
                self.assertTrue(f["titulo"].startswith("File:"))
                self.assertTrue(avaliar_licenca(f["licenca"])[0], f["licenca"])
                self.assertNotIn(f["titulo"], titulos, "duplicada")
                titulos.add(f["titulo"])


class TestEmbutir(unittest.TestCase):
    def test_local_vira_data_uri(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "figuras").mkdir()
            (Path(d) / "figuras" / "x.png").write_bytes(b"\x89PNG\r\n")
            html = embutir_figuras('<img src="figuras/x.png" alt="a">', Path(d))
            self.assertIn('src="data:image/png;base64,', html)

    def test_remota_e_data_ficam(self):
        for src in ["https://exemplo.org/a.png", "data:image/png;base64,AAA"]:
            html = f'<img src="{src}">'
            self.assertEqual(embutir_figuras(html, Path(".")), html)


if __name__ == "__main__":
    unittest.main(verbosity=1)
