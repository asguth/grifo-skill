#!/usr/bin/env python3
"""Monta um HTML autocontido do Grifo-Skill.

Uso:  python3 montar.py entrada.html saida.html

No HTML de entrada, use os marcadores:
  <!--APOSTILA:CSS-->     -> substituído pelo conteúdo de assets/apostila.css
  <!--APOSTILA:SPRITE-->  -> substituído por um <svg class="sprite"> contendo
                             apenas os <symbol> referenciados via href="#i-..."
Licença MIT.
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "assets"


def carregar_simbolos():
    svg = (BASE / "ilustracoes.svg").read_text(encoding="utf-8")
    estilo = re.search(r"<style>(.*?)</style>", svg, re.S)
    simbolos = {
        m.group(1): m.group(0)
        for m in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', svg, re.S)
    }
    return (estilo.group(1) if estilo else ""), simbolos


def montar(html: str) -> str:
    css = (BASE / "apostila.css").read_text(encoding="utf-8")
    estilo_svg, simbolos = carregar_simbolos()

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
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    entrada, saida = map(Path, sys.argv[1:])
    saida.write_text(montar(entrada.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"ok: {saida}")
