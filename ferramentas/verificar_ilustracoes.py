#!/usr/bin/env python3
"""Verifica o sprite do mascote (assets/ilustracoes.svg).

Uso:  python3 verificar_ilustracoes.py [caminho/ilustracoes.svg]

Falha (exit 1) se algum símbolo:
  - tiver id duplicado;
  - não tiver viewBox;
  - usar classe que não existe no <style> do próprio sprite;
  - usar <use> apontando para id inexistente;
  - usar cor fora da paleta do mascote (references/design.md §4);
  - usar <image> que não aponte para um arquivo de assets/ com até 40 KB;
e também se o arquivo não for XML válido ou houver <symbol> fora do <svg>
(por exemplo, dentro de comentário).
Avisa (sem falhar) quando um símbolo 64×64 passa de 15 elementos.
Licença MIT.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_PADRAO = Path(__file__).resolve().parent.parent / "skills" / "grifo" / "assets" / "ilustracoes.svg"
NS = "{http://www.w3.org/2000/svg}"

# Só o mascote e os selos vivem no sprite (references/design.md §4).
PALETA = {"#1C2430", "#FFFFFF", "#FFE45C", "#B42318"}
LIMITE_ELEMENTOS = 15
LIMITE_IMAGEM = 40 * 1024  # mascote raster (WebP)
RE_SIMBOLO = re.compile(r"<symbol\s[^>]*\bid=")
RE_COR = re.compile(r"#[0-9A-Fa-f]{3,8}\b")


def normalizar(cor: str) -> str:
    cor = cor.upper()
    if len(cor) == 4:  # #abc -> #AABBCC
        cor = "#" + "".join(c * 2 for c in cor[1:])
    return cor


def classes_do_estilo(estilo: str) -> set:
    return set(re.findall(r"\.([A-Za-z][\w-]*)", re.sub(r"\{[^}]*\}", "{}", estilo)))


def verificar(caminho: Path):
    erros, avisos = [], []
    texto = caminho.read_text(encoding="utf-8")

    try:
        raiz = ET.fromstring(texto)
    except ET.ParseError as e:
        return [f"XML inválido: {e}"], avisos

    sem_comentarios = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    n_regex = len(RE_SIMBOLO.findall(texto))
    n_validos = len(RE_SIMBOLO.findall(sem_comentarios))
    if n_regex != n_validos:
        erros.append(f"{n_regex - n_validos} <symbol> dentro de comentário (não serão usados)")

    estilo = "".join(e.text or "" for e in raiz.iter(f"{NS}style"))
    classes_ok = classes_do_estilo(estilo)
    for cor in RE_COR.findall(estilo):
        if normalizar(cor) not in PALETA:
            erros.append(f"<style>: cor {cor} fora da paleta")

    simbolos = list(raiz.iter(f"{NS}symbol"))
    ids = [s.get("id") for s in simbolos]
    vistos = set()
    for i in ids:
        if i in vistos:
            erros.append(f"id duplicado: {i}")
        vistos.add(i)

    for s in simbolos:
        sid = s.get("id") or "(sem id)"
        vb = s.get("viewBox")
        if not vb:
            erros.append(f"{sid}: sem viewBox")
        filhos = [el for el in s.iter() if el is not s and el.tag not in (f"{NS}g", f"{NS}title")]
        if vb == "0 0 64 64" and len(filhos) > LIMITE_ELEMENTOS:
            avisos.append(f"{sid}: {len(filhos)} elementos (> {LIMITE_ELEMENTOS})")
        for el in s.iter():
            for c in (el.get("class") or "").split():
                if c not in classes_ok:
                    erros.append(f"{sid}: classe .{c} não existe no <style> do sprite")
            href = el.get("href") or el.get("{http://www.w3.org/1999/xlink}href")
            if el.tag == f"{NS}use" and href:
                if not href.startswith("#") or href[1:] not in vistos:
                    erros.append(f"{sid}: <use> aponta para {href}, que não existe")
            for attr in ("fill", "stroke", "style", "stop-color", "color"):
                for cor in RE_COR.findall(el.get(attr) or ""):
                    if normalizar(cor) not in PALETA:
                        erros.append(f"{sid}: cor {cor} fora da paleta ({attr})")
            if el.tag in (f"{NS}linearGradient", f"{NS}radialGradient", f"{NS}filter"):
                erros.append(f"{sid}: <{el.tag.replace(NS, '')}> não é permitido (estilo flat)")
            if el.tag == f"{NS}image":
                # raster só para o mascote: arquivo em assets/, embutido pelo montar.py
                arq = caminho.parent / (href or "")
                if not href or href.startswith(("data:", "http")):
                    erros.append(f"{sid}: <image> deve apontar para um arquivo em assets/ (ex.: mascote/grifo.webp)")
                elif not arq.is_file():
                    erros.append(f"{sid}: <image> aponta para {href}, que não existe")
                elif arq.stat().st_size > LIMITE_IMAGEM:
                    erros.append(f"{sid}: {href} tem {arq.stat().st_size // 1024} KB (> {LIMITE_IMAGEM // 1024} KB)")
    return erros, avisos


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else SVG_PADRAO
    erros, avisos = verificar(caminho)
    for a in avisos:
        print("aviso:", a)
    for e in erros:
        print("ERRO:", e)
    n = len(RE_SIMBOLO.findall(re.sub(r"<!--.*?-->", "", caminho.read_text(encoding="utf-8"), flags=re.S)))
    if erros:
        print(f"falhou: {len(erros)} erro(s) em {caminho.name}")
        sys.exit(1)
    print(f"ok: {n} símbolos verificados em {caminho.name}")


if __name__ == "__main__":
    main()
