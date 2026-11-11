#!/usr/bin/env python3
"""Lint do HTML-fonte do Grifo-Skill (antes de montar/renderizar).

Uso:  python3 verificar.py arquivo-fonte.html [outro.html …] [--estrito]

ERROS (exit 1):
  - classe usada que não existe no grifo.css (nem num <style> do próprio arquivo);
  - <use href="#i-…"> apontando para ilustração que não existe no sprite;
  - .folha sem .topo (exceto .folha.capa);
  - numeração das folhas (.topo .pag) fora de sequência.
AVISOS (exit 0, ou 1 com --estrito):
  - sobrou class="verificar" ([VERIFICAR] no texto final);
  - .coluna sem nenhum diagrama, tabela ou ilustração;
  - <style> inline com mais de 20 linhas (use as classes do design system);
  - marcador de template não preenchido ([[…]]).
Licença MIT.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LIMITE_STYLE = 20
# o que conta como "elemento visual" numa coluna (design.md §2 e §5)
VISUAIS = {
    "chave", "fluxo", "linha-tempo", "piramide", "piramide-legenda", "sigla", "relacao",
    "comparativo", "rotulada", "verdade", "edital", "formula", "codigo", "exemplo-frase",
    "ilustra", "flashcards",
    "questao", "gabarito",  # coluna só de questões/gabarito dispensa diagrama
}
VISUAIS_TAGS = {"table", "svg", "img"}


def classes_do_css(css: str) -> set:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\{[^{}]*\}", "{}", css)            # tira as declarações
    css = re.sub(r'\[[^\]]*\]|"[^"]*"', "", css)      # tira [atributos] e strings
    return set(re.findall(r"\.(-?[A-Za-z_][\w-]*)", css))


def ids_do_sprite() -> set:
    svg = re.sub(r"<!--.*?-->", "", (ASSETS / "ilustracoes.svg").read_text(encoding="utf-8"), flags=re.S)
    return set(re.findall(r'<symbol\s[^>]*\bid="([^"]+)"', svg))


class No:
    __slots__ = ("tag", "classes", "attrs", "filhos", "pai", "texto", "linha")

    def __init__(self, tag, attrs, pai, linha):
        self.tag, self.attrs, self.pai, self.linha = tag, dict(attrs), pai, linha
        self.classes = set((self.attrs.get("class") or "").split())
        self.filhos, self.texto = [], []

    def descendentes(self):
        for f in self.filhos:
            yield f
            yield from f.descendentes()

    def todo_texto(self):
        return "".join(self.texto) + "".join(f.todo_texto() for f in self.filhos)


VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
          "source", "track", "wbr", "use", "path", "circle", "rect", "ellipse", "line",
          "polygon", "polyline", "stop"}


class Arvore(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = No("#doc", [], None, 0)
        self.atual = self.raiz
        self.styles = []  # (linha, texto)

    def handle_starttag(self, tag, attrs):
        no = No(tag, attrs, self.atual, self.getpos()[0])
        self.atual.filhos.append(no)
        if tag not in VAZIOS:
            self.atual = no

    def handle_startendtag(self, tag, attrs):
        self.atual.filhos.append(No(tag, attrs, self.atual, self.getpos()[0]))

    def handle_endtag(self, tag):
        no = self.atual
        while no is not self.raiz and no.tag != tag:
            no = no.pai
        if no is not self.raiz:
            self.atual = no.pai

    def handle_data(self, data):
        self.atual.texto.append(data)
        if self.atual.tag == "style":
            self.styles.append((self.atual.linha, data))


def verificar(caminho: Path, classes_css: set, ids: set):
    erros, avisos = [], []
    texto = caminho.read_text(encoding="utf-8")
    arv = Arvore()
    arv.feed(texto)
    todos = list(arv.raiz.descendentes())

    # classes declaradas em <style> do próprio arquivo também valem
    locais = set()
    for linha, st in arv.styles:
        locais |= classes_do_css(st)
        n = st.strip().count("\n") + 1
        if n > LIMITE_STYLE:
            avisos.append(f"linha {linha}: <style> inline com {n} linhas (> {LIMITE_STYLE}); use as classes do grifo.css")
    conhecidas = classes_css | locais

    desconhecidas = {}
    for no in todos:
        for c in no.classes:
            if c not in conhecidas:
                desconhecidas.setdefault(c, no.linha)
        href = no.attrs.get("href") or no.attrs.get("xlink:href") or ""
        if no.tag == "use" and href.startswith("#i-") and href[1:] not in ids:
            erros.append(f"linha {no.linha}: ilustração {href} não existe em ilustracoes.svg")
    for c, linha in sorted(desconhecidas.items(), key=lambda x: x[1]):
        erros.append(f"linha {linha}: classe .{c} não existe no grifo.css")

    folhas = [n for n in todos if n.tag == "div" and "folha" in n.classes]
    esperado = None
    for i, f in enumerate(folhas, 1):
        if "capa" in f.classes:
            continue
        topo = next((d for d in f.descendentes() if "topo" in d.classes), None)
        if topo is None:
            if "sumario" not in f.classes:
                erros.append(f"linha {f.linha}: folha {i} sem .topo")
            continue
        pag = next((d for d in topo.descendentes() if "pag" in d.classes), None)
        if pag is None:
            erros.append(f"linha {topo.linha}: .topo da folha {i} sem .pag (número da folha)")
            continue
        num = pag.todo_texto().strip()
        if not num.isdigit():
            erros.append(f"linha {pag.linha}: número da folha {i} não é numérico: {num!r}")
            continue
        n = int(num)
        if esperado is not None and n != esperado:
            erros.append(f"linha {pag.linha}: folha numerada {num}, esperado {esperado:02d}")
        esperado = n + 1

    marcadores = [(i, m.group(0)) for i, linha in enumerate(texto.splitlines(), 1)
                  for m in re.finditer(r"\[\[[^\]]{0,80}\]\]", linha)]
    if marcadores:
        i, primeiro = marcadores[0]
        avisos.append(f"linha {i}: {len(marcadores)} marcador(es) de template não preenchido(s); "
                      f"o primeiro é {primeiro}")

    for no in todos:
        if "verificar" in no.classes:
            trecho = re.sub(r"\s+", " ", no.todo_texto()).strip()[:60]
            avisos.append(f"linha {no.linha}: sobrou [VERIFICAR]: {trecho!r}")

    for no in todos:
        if "coluna" in no.classes:
            tem = any((d.tag in VISUAIS_TAGS and "sprite" not in d.classes) or (d.classes & VISUAIS)
                      for d in no.descendentes())
            if not tem:
                cab = next((d for d in no.descendentes() if "coluna-cab" in d.classes), None)
                nome = re.sub(r"\s+", " ", cab.todo_texto()).strip() if cab else "(sem cabeçalho)"
                avisos.append(f"linha {no.linha}: coluna {nome!r} sem diagrama, tabela ou ilustração")
    return erros, avisos


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    estrito = "--estrito" in sys.argv
    if not args:
        sys.exit(__doc__)
    classes_css = classes_do_css((ASSETS / "grifo.css").read_text(encoding="utf-8"))
    ids = ids_do_sprite()
    falhou = False
    for a in args:
        caminho = Path(a)
        erros, avisos = verificar(caminho, classes_css, ids)
        for e in erros:
            print(f"ERRO  {caminho.name}: {e}")
        for w in avisos:
            print(f"aviso {caminho.name}: {w}")
        if not erros and not avisos:
            print(f"ok: {caminho.name}")
        falhou |= bool(erros) or (estrito and bool(avisos))
    sys.exit(1 if falhou else 0)


if __name__ == "__main__":
    main()
