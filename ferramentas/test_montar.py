#!/usr/bin/env python3
"""Testes do espaço inseparável do montar.py.

Uso:  python3 test_montar.py        (sai com código 1 se algum falhar)
Licença MIT.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "grifo" / "scripts"))
from montar import inseparaveis, quebras_suaves  # noqa: E402

N = "&nbsp;"

CASOS = [
    # (entrada, esperado)
    ("conforme o art. 59 da lei", f"conforme o art.{N}59 da lei"),
    ("(art. 59)", f"(art.{N}59)"),
    ("Art. 7º, IX", f"Art.{N}7º,{N}IX"),
    ("arts. 5º e 7º", f"arts.{N}5º e 7º"),
    ("§ 1º do art. 13", f"§{N}1º do art.{N}13"),
    ("§§ 2º e 3º", f"§§{N}2º e 3º"),
    ("§ único", f"§{N}único"),
    ("inciso IV", f"inciso{N}IV"),
    ("inc. II do art. 5º", f"inc.{N}II do art.{N}5º"),
    ("alínea a", f"alínea{N}a"),
    ('alínea "b"', f'alínea{N}"b"'),
    ("Lei 8.112/1990", f"Lei{N}8.112/1990"),
    ("Lei nº 13.709", f"Lei{N}nº{N}13.709"),
    ("Lei Complementar 123", f"Lei{N}Complementar{N}123"),
    ("EC 19/1998", f"EC{N}19/1998"),
    ("Súmula Vinculante 13", f"Súmula{N}Vinculante{N}13"),
    ("Súmula 473 do STF", f"Súmula{N}473 do STF"),
    ("prazo de 30 dias", f"prazo de 30{N}dias"),
    ("10 dias úteis", f"10{N}dias{N}úteis"),
    ("3 meses", f"3{N}meses"),
    ("1 mês", f"1{N}mês"),
    ("2 anos e 24 horas", f"2{N}anos e 24{N}horas"),
    ("até 50 %", f"até 50{N}%"),
    ("cerca de 70 mL e 5 L/min", f"cerca de 70{N}mL e 5{N}L/min"),
    ("PA de 120 mmHg a 72 bpm", f"PA de 120{N}mmHg a 72{N}bpm"),
    ("within 30 days", f"within 30{N}days"),
    ("plazo de 15 días", f"plazo de 15{N}días"),
    ("caso 3 Kids", "caso 3 Kids"),
    ("art. 36, p.ú.", f"art.{N}36,{N}p.ú."),
    ("parágrafo único", f"parágrafo{N}único"),
    # marcação inline entre gatilho e alvo
    ("art. <b>59</b>", f"art.{N}<b>59</b>"),
    ("<b>30</b> dias", f"<b>30</b>{N}dias"),
    ("<b>60 dias</b>", f"<b>60{N}dias</b>"),
    # NÃO mexer
    ('<div title="art. 5 aqui">x</div>', '<div title="art. 5 aqui">x</div>'),
    ("<style>.a{} /* art. 5 */</style>", "<style>.a{} /* art. 5 */</style>"),
    ("<!-- 30 dias -->", "<!-- 30 dias -->"),
    ("<script>var s='30 dias'</script>", "<script>var s='30 dias'</script>"),
    ("a Lei no Brasil", "a Lei no Brasil"),
    ("os artistas 5 vezes", "os artistas 5 vezes"),
    ("em 30 dianteiras", "em 30 dianteiras"),
    ("vale 2 anéis", "vale 2 anéis"),
    ("já com&nbsp;art.&nbsp;5", "já com&nbsp;art.&nbsp;5"),  # idempotente
]


class TestInseparaveis(unittest.TestCase):
    def test_casos(self):
        for entrada, esperado in CASOS:
            with self.subTest(entrada=entrada):
                self.assertEqual(inseparaveis(entrada), esperado)

    def test_idempotente(self):
        for entrada, _ in CASOS:
            uma = inseparaveis(entrada)
            with self.subTest(entrada=entrada):
                self.assertEqual(inseparaveis(uma), uma)

    def test_quebra_de_linha_no_fonte(self):
        self.assertEqual(inseparaveis("art.\n   59"), f"art.{N}59")

    def test_quebra_suave_na_barra(self):
        self.assertEqual(quebras_suaves("conveniência/oportunidade"), "conveniência/<wbr>oportunidade")
        self.assertEqual(quebras_suaves("Lei 8.112/1990"), "Lei 8.112/1990")
        self.assertEqual(quebras_suaves('<a href="x/y">e/ou</a>'), '<a href="x/y">e/<wbr>ou</a>')
        self.assertEqual(quebras_suaves("</b>/<i>"), "</b>/<i>")

    def test_minimo_de_casos(self):
        self.assertGreaterEqual(len(CASOS), 15)


if __name__ == "__main__":
    unittest.main(verbosity=1)
