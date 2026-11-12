#!/usr/bin/env python3
"""Testes do figura.py (licenças aceitas) e do embutimento de imagens do montar.py.

Uso:  python3 test_figura.py        (sem rede; sai com código 1 se algum falhar)
Licença MIT.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "grifo" / "scripts"))
from figura import avaliar_licenca  # noqa: E402
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
