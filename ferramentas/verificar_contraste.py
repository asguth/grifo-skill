#!/usr/bin/env python3
"""Confere o contraste (WCAG 2.x) de cada par texto/fundo usado no grifo.css.

Uso:  python3 verificar_contraste.py
Mínimo 4,5:1 (texto normal; rótulos de 8–9 pt contam como normais).
Falha (exit 1) se algum par ficar abaixo. Licença MIT.
"""
import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "skills" / "grifo" / "assets" / "grifo.css"
MINIMO = 4.5
# (texto, fundo) como os componentes realmente combinam
PARES = [
    ("#FFFFFF", "--navy"), ("#FFFFFF", "--azul"), ("#FFFFFF", "--slate"),
    ("#FFFFFF", "--ambar"), ("#FFFFFF", "--verm"), ("#FFFFFF", "--verde"),
    ("--navy", "--sup-2"), ("--navy", "--sup"), ("--tinta", "--sup"), ("--tinta", "--papel"),
    ("--azul", "--papel"), ("--azul", "--sup"), ("--slate", "--papel"), ("--slate", "--sup"),
    ("--ambar", "--ambar-claro"), ("--verm", "--verm-claro"), ("--verde", "--verde-claro"),
    ("--azul", "--azul-claro"), ("--tinta", "--mt-chave"), ("--tinta", "--mt-troca"),
]
# matizes de tópico (estilos colorido/pastel): faixa cheia, faixa clara, corpo pálido
for _i in range(1, 7):
    _m = f"--m{_i}"
    PARES += [("#FFFFFF", _m), (_m, f"{_m}-claro"), (_m, f"{_m}-palido"), (_m, "--papel"),
              ("--tinta", f"{_m}-palido"), ("--tinta", f"{_m}-claro")]
# estilo pb (bloco [data-tema="pb"]): os mesmos papéis em cinza
PARES_PB = [("#FFFFFF", "--navy"), ("#FFFFFF", "--slate"), ("#FFFFFF", "--verm"), ("#FFFFFF", "--verde"),
            ("#FFFFFF", "--ambar"), ("--navy", "--sup-2"), ("--azul", "--sup"), ("--ambar", "--ambar-claro"),
            ("--verm", "--verm-claro"), ("--tinta", "--mt-chave"), ("--tinta", "--mt-troca")]


def luminancia(hexa: str) -> float:
    hexa = hexa.lstrip("#")
    canais = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a: str, b: str) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    raiz = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
    cores = dict(re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{6})", raiz))
    pb = re.search(r'\[data-tema="pb"\]\s*\{(.*?)\}', css, re.S)
    cores_pb = {**cores, **dict(re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{6})", pb.group(1)))} if pb else cores
    cores_base = cores
    falhas = 0
    todos = [(t, f, cores) for t, f in PARES] + [(t, f, cores_pb) for t, f in PARES_PB]
    for texto, fundo, cores in todos:
        a, b = cores.get(texto, texto), cores.get(fundo, fundo)
        if not (a.startswith("#") and b.startswith("#")):
            sys.exit(f"cor não encontrada no grifo.css: {texto} / {fundo}")
        c = contraste(a, b)
        ok = c >= MINIMO
        falhas += not ok
        print(f"{texto:10} sobre {fundo:13} {c:5.2f}:1 {'ok' if ok else 'FALHA'}{' (pb)' if cores is cores_pb and cores_pb is not cores_base else ''}")
    if falhas:
        sys.exit(f"falhou: {falhas} par(es) abaixo de {MINIMO}:1")
    print(f"ok: {len(todos)} pares >= {MINIMO}:1")


if __name__ == "__main__":
    main()
