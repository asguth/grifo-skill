#!/usr/bin/env python3
"""Monta um HTML autocontido do Grifo-Skill.

Uso:  python3 montar.py entrada.html saida.html [--fontes-embutidas]

  --fontes-embutidas  troca os <link> do Google Fonts por @font-face com Inter e
                      Poppins embutidas (assets/fontes, OFL): o PDF sai igual sem
                      internet. Acrescenta ~110 KB ao HTML.

No HTML de entrada, use os marcadores:
  <!--APOSTILA:CSS-->     -> substituído pelo conteúdo de assets/grifo.css
  <!--APOSTILA:SPRITE-->  -> substituído por um <svg class="sprite"> contendo
                             apenas os <symbol> referenciados via href="#i-..."

Imagens de figura (<img src="figuras/x.jpg">, caminho relativo ao HTML de entrada)
são embutidas como data URI: o HTML final fica autocontido.

Também troca espaços por &nbsp; onde a quebra de linha separaria referências
legais e números de suas unidades ("art. 59", "§ 1º", "inciso IV", "Lei nº
8.112", "30 dias úteis", "10 %", "art. 36, p.ú." …). Só mexe no texto: nunca
dentro de tags, atributos, comentários, <style> ou <script>.
Licença MIT.
"""
import base64
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
_UNIDADE = (
    r"(?:dias?|m[eê]s(?:es)?|anos?|horas?|minutos?|semanas?|%"
    # en · es · fr · it · de
    r"|days?|weeks?|months?|years?|hours?|minutes?|d[ií]as|años?|jours?|mois|ans|semaines?"
    r"|giorni|mesi|anni|settimane|Tage[n]?|Wochen|Monate[n]?|Jahre[n]?|Stunden"
    # unidades de ciências e saúde
    r"|mL|L|dL|mg|µg|mcg|kg|g|cm|mm|nm|µm|bpm|mmHg|mEq|mmol|UI|IU|°C|K|Hz|kHz|V|mV|W|kW|J|kJ|kcal|Pa|kPa|atm|mol)"
    r"(?![\wÀ-ÿ])"
)

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
    # 30 dias · 3 meses · 2 anos · 24 horas · 10 % · 70 mL · 120 mmHg · 30 days
    rf"(?<=\d){_FECHA}{_WS}(?={_ABRE}{_UNIDADE})",
    # dias úteis
    rf"\bdias{_FECHA}{_WS}(?={_ABRE}úteis\b)",
    # art. 36, p.ú. · p. ú. · parágrafo único
    rf"{_WS}(?={_ABRE}p\.\s?ú\.)",
    rf"\bp\.{_WS}(?=ú\.)",
    rf"\bparágrafo{_WS}(?=único\b)",
]
# ponto de quebra opcional depois de "/" entre letras (conveniência/oportunidade);
# nunca entre dígitos (8.112/1990) — esses ficam juntos.
_RE_BARRA = re.compile(r"(?<=[A-Za-zÀ-ÿ])/(?=[A-Za-zÀ-ÿ])")
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


def quebras_suaves(html: str) -> str:
    """Acrescenta <wbr> depois de "/" entre letras, fora de tags/style/script."""
    inicios, fins = _intervalos_protegidos(html)

    def trocar(m):
        i = bisect.bisect_right(inicios, m.start()) - 1
        if i >= 0 and m.start() < fins[i]:
            return m.group(0)
        return "/<wbr>"

    return _RE_BARRA.sub(trocar, html)


# --------------------------------------------------------------------------
# sprite e CSS
# --------------------------------------------------------------------------
def carregar_simbolos():
    svg = (BASE / "ilustracoes.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)  # comentários não entram no sprite
    estilo = re.search(r"<style>(.*?)</style>", svg, re.S)
    simbolos = {
        m.group(1): embutir_imagens(m.group(0))
        for m in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', svg, re.S)
    }
    return (estilo.group(1) if estilo else ""), simbolos


def icones_lucide() -> dict:
    """{nome: <symbol id="l-nome">} a partir de assets/lucide/lucide.svg (um símbolo por linha)."""
    out = {}
    for linha in (BASE / "lucide" / "lucide.svg").read_text(encoding="utf-8").splitlines():
        m = re.match(r'<symbol id="([^"]+)"', linha)
        if m:
            out[m.group(1)] = linha.replace(f'id="{m.group(1)}"', f'id="l-{m.group(1)}"', 1)
    return out


MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml", ".gif": "image/gif"}


def embutir_imagens(simbolo: str) -> str:
    """<image href="mascote/x.webp"> (relativo a assets/) -> data URI, para o HTML ficar autocontido."""
    def trocar(m):
        arq = BASE / m.group(1)
        if not arq.exists():
            print(f"aviso: imagem {m.group(1)} não existe em assets/", file=sys.stderr)
            return m.group(0)
        b64 = base64.b64encode(arq.read_bytes()).decode("ascii")
        return f'href="data:{MIME.get(arq.suffix.lower(), "application/octet-stream")};base64,{b64}"'

    return re.sub(r'href="(?!#|data:|https?:)([^"]+)"', trocar, simbolo)


def embutir_figuras(html: str, base: Path) -> str:
    """<img src="relativo"> -> data URI (relativo à pasta do HTML de entrada)."""
    def trocar(m):
        src = m.group(2)
        arq = (base / src).resolve()
        if not arq.is_file():
            print(f"aviso: imagem {src} não existe (relativo a {base})", file=sys.stderr)
            return m.group(0)
        mime = MIME.get(arq.suffix.lower(), "application/octet-stream")
        b64 = base64.b64encode(arq.read_bytes()).decode("ascii")
        return f'{m.group(1)}data:{mime};base64,{b64}"'

    return re.sub(r'(<img\b[^>]*?\bsrc=")(?!data:|https?:|//)([^"]+)"', trocar, html)


FONTES = [  # (família, peso, arquivo) — só o subconjunto latin e os pesos usados
    ("Inter", "100 900", "inter-latin-var.woff2"),
    ("Poppins", "600", "poppins-latin-600.woff2"),
    ("Poppins", "700", "poppins-latin-700.woff2"),
    ("Poppins", "800", "poppins-latin-800.woff2"),
    ("Poppins", "900", "poppins-latin-900.woff2"),
]


def css_fontes_embutidas() -> str:
    regras = []
    for familia, peso, arquivo in FONTES:
        b64 = base64.b64encode((BASE / "fontes" / arquivo).read_bytes()).decode("ascii")
        regras.append(
            f"@font-face{{font-family:'{familia}';font-style:normal;font-weight:{peso};"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "/* Inter e Poppins — SIL Open Font License 1.1 (assets/fontes/OFL.txt) */\n" + "\n".join(regras)


def embutir_fontes(html: str) -> str:
    html = re.sub(r'<link[^>]+href="https://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>\s*', "", html)
    estilo = f"<style>\n{css_fontes_embutidas()}\n</style>\n"
    if "<!--APOSTILA:CSS-->" in html:
        return html.replace("<!--APOSTILA:CSS-->", estilo + "<!--APOSTILA:CSS-->", 1)
    return html.replace("</head>", estilo + "</head>", 1)


def versao() -> str:
    """Versão da skill: metadata.version do SKILL.md (atualizada a cada release)."""
    skill = (BASE.parent / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'^\s*version:\s*"?([\w.-]+)"?', skill, re.M)
    return m.group(1) if m else "?"


def montar(html: str, fontes_embutidas: bool = False, base: Path | None = None) -> str:
    css = (BASE / "grifo.css").read_text(encoding="utf-8")
    estilo_svg, simbolos = carregar_simbolos()

    html = quebras_suaves(inseparaveis(html))
    html = embutir_figuras(html, base or Path.cwd())
    if fontes_embutidas:
        html = embutir_fontes(html)

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

    icones = []
    nomes_l = sorted(set(re.findall(r'href="#l-([\w-]+)"', html)))
    if nomes_l:
        lucide = icones_lucide()
        for n in nomes_l:
            if n in lucide:
                icones.append(lucide[n])
            else:
                print(f"aviso: ícone Lucide 'l-{n}' não existe (procure em assets/lucide/nomes.txt)", file=sys.stderr)

    sprite = (
        '<svg xmlns="http://www.w3.org/2000/svg" class="sprite" aria-hidden="true">'
        f"<defs><style>{estilo_svg}</style></defs>"
        + "".join(simbolos[n] for n in usados)
        + "".join(icones)
        + "</svg>"
    )
    if "<!--APOSTILA:CSS-->" not in html:
        print("aviso: marcador <!--APOSTILA:CSS--> não encontrado", file=sys.stderr)
    css += f'\n:root {{ --versao: "v{versao()}"; }}'
    html = html.replace("<!--APOSTILA:CSS-->", f"<style>\n{css}\n</style>")
    html = html.replace("<!--APOSTILA:SPRITE-->", sprite)
    return html


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2 or flags - {"--fontes-embutidas"}:
        sys.exit(__doc__)
    entrada, saida = map(Path, args)
    html = montar(entrada.read_text(encoding="utf-8"), "--fontes-embutidas" in flags, entrada.resolve().parent)
    saida.write_text(html, encoding="utf-8", newline="\n")
    print(f"ok: {saida}")
