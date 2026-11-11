#!/usr/bin/env python3
"""Monta um HTML autocontido do Grifo-Skill.

Uso:  python3 montar.py entrada.html saida.html

No HTML de entrada, use os marcadores:
  <!--APOSTILA:CSS-->     -> substituído pelo conteúdo de assets/grifo.css
  <!--APOSTILA:SPRITE-->  -> substituído por um <svg class="sprite"> contendo
                             apenas os <symbol> referenciados via href="#i-..."

Também troca espaços por &nbsp; onde a quebra de linha separaria referências
legais e números de suas unidades ("art. 59", "§ 1º", "inciso IV", "Lei nº
8.112", "30 dias úteis", "10 %", "art. 36, p.ú." …). Só mexe no texto: nunca
dentro de tags, atributos, comentários, <style> ou <script>.
Licença MIT.
"""
import bisect
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "assets"

# --------------------------------------------------------------------------
# espaço inseparável
# --------------------------------------------------------------------------
_INLINE = r"(?:b|strong|i|em|mark|span|small|u|sup|sub|a)"
_ABRE = rf"(?:<{_INLINE}\b[^>]*>)*"     # tags inline que podem abrir antes do alvo
_FECHA = rf"(?:</{_INLINE}>)*"           # tags inline que podem fechar depois do gatilho
_WS = r"(?P<ws>[ \t\r\n]+)"
_ROMANO = r"[IVXLC]+\b"
_UNIDADE = r"(?:dias?|m[eê]s(?:es)?|anos?|horas?|minutos?|semanas?|%)(?![\wÀ-ÿ])"

# Cada regra: gatilho + fechamentos inline + ESPAÇO + (?=aberturas inline + alvo).
# Só o grupo "ws" é substituído.
REGRAS = [
    # art. 59 · arts. 5º · Art. 7º
    rf"\b[Aa]rts?\.{_FECHA}{_WS}(?={_ABRE}\d)",
    # § 1º · §§ 2º · § único
    rf"§§?{_FECHA}{_WS}(?={_ABRE}(?:\d|[úu]nico))",
    # inc. IV · inciso II · incisos I
    rf"\b(?:[Ii]nc\.|[Ii]ncisos?){_FECHA}{_WS}(?={_ABRE}{_ROMANO})",
    # alínea a · alíneas "b"
    rf"\b[Aa]l[íi]neas?{_FECHA}{_WS}(?={_ABRE}[\"“'‘]?[a-z]\b)",
    # Lei 8.112 · Lei nº · LC 123 · EC 19 · Súmula 473 · Súmula Vinculante 13 · Decreto 9.094 · MP 1.000
    rf"\b(?:Leis?|LC|EC|Decreto(?:-[Ll]ei)?|Súmulas?|Vinculante|Complementar|MP){_FECHA}{_WS}"
    rf"(?={_ABRE}(?:n[º°]|\d|Vinculante|Complementar))",
    # nº 8.112
    rf"\bn[º°]\.?{_FECHA}{_WS}(?={_ABRE}\d)",
    # 5º, II  (dispositivo seguido de inciso)
    rf"(?<=\d[º°],){_FECHA}{_WS}(?={_ABRE}{_ROMANO})",
    # 30 dias · 3 meses · 2 anos · 24 horas · 10 %
    rf"(?<=\d){_FECHA}{_WS}(?={_ABRE}{_UNIDADE})",
    # dias úteis
    rf"\bdias{_FECHA}{_WS}(?={_ABRE}úteis\b)",
    # art. 36, p.ú. · p. ú. · parágrafo único
    rf"{_WS}(?={_ABRE}p\.\s?ú\.)",
    rf"\bp\.{_WS}(?=ú\.)",
    rf"\bparágrafo{_WS}(?=único\b)",
]
_RE_REGRAS = [re.compile(r) for r in REGRAS]
_PROTEGIDO = re.compile(
    r"<!--.*?-->|<(style|script)\b.*?</\1\s*>|<[^>]*>", re.S | re.I
)


def _intervalos_protegidos(html: str):
    inicios, fins = [], []
    for m in _PROTEGIDO.finditer(html):
        inicios.append(m.start())
        fins.append(m.end())
    return inicios, fins


def inseparaveis(html: str) -> str:
    """Troca por &nbsp; os espaços que não podem virar quebra de linha."""
    for rx in _RE_REGRAS:
        inicios, fins = _intervalos_protegidos(html)

        def trocar(m):
            pos = m.start("ws")
            i = bisect.bisect_right(inicios, pos) - 1
            if i >= 0 and pos < fins[i]:
                return m.group(0)  # dentro de tag/comentário/style/script
            ini, fim = m.start("ws") - m.start(), m.end("ws") - m.start()
            return m.group(0)[:ini] + "&nbsp;" + m.group(0)[fim:]

        html = rx.sub(trocar, html)
    return html


# --------------------------------------------------------------------------
# sprite e CSS
# --------------------------------------------------------------------------
def carregar_simbolos():
    svg = (BASE / "ilustracoes.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)  # comentários não entram no sprite
    estilo = re.search(r"<style>(.*?)</style>", svg, re.S)
    simbolos = {
        m.group(1): m.group(0)
        for m in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', svg, re.S)
    }
    return (estilo.group(1) if estilo else ""), simbolos


def montar(html: str) -> str:
    css = (BASE / "grifo.css").read_text(encoding="utf-8")
    estilo_svg, simbolos = carregar_simbolos()

    html = inseparaveis(html)

    usados, fila = [], re.findall(r'href="#(i-[\w-]+)"', html)
    while fila:  # resolve dependências (símbolo que usa outro símbolo)
        nome = fila.pop(0)
        if nome in usados:
            continue
        if nome not in simbolos:
            print(f"aviso: ilustração '{nome}' não existe na biblioteca", file=sys.stderr)
            continue
        usados.append(nome)
        fila += re.findall(r'href="#(i-[\w-]+)"', simbolos[nome])

    sprite = (
        '<svg xmlns="http://www.w3.org/2000/svg" class="sprite" aria-hidden="true">'
        f"<defs><style>{estilo_svg}</style></defs>"
        + "".join(simbolos[n] for n in usados)
        + "</svg>"
    )
    if "<!--APOSTILA:CSS-->" not in html:
        print("aviso: marcador <!--APOSTILA:CSS--> não encontrado", file=sys.stderr)
    html = html.replace("<!--APOSTILA:CSS-->", f"<style>\n{css}\n</style>")
    html = html.replace("<!--APOSTILA:SPRITE-->", sprite)
    return html


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    entrada, saida = map(Path, sys.argv[1:])
    saida.write_text(montar(entrada.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    print(f"ok: {saida}")
