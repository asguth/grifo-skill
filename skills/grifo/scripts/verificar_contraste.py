#!/usr/bin/env python3
"""Confere o contraste do texto branco sobre as cores de cada disciplina.

Uso:  python3 verificar_contraste.py [--minimo 3.0]

Para cada classe .d-* do grifo.css (e o :root), calcula a razão de contraste
WCAG 2.x entre #FFFFFF e --disc e --disc-2 (faixas, cabeçalhos, nº da folha —
texto grande e negrito, onde o mínimo AA é 3:1). Também confere as cores
semânticas fixas usadas como fundo de texto branco. Falha (exit 1) se alguma
ficar abaixo do mínimo. Licença MIT.
"""
import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "assets" / "grifo.css"
SEMANTICAS = ("--excecao", "--pegadinha", "--dica", "--lei", "--exemplo")


def luminancia(hexa: str) -> float:
    hexa = hexa.lstrip("#")
    if len(hexa) == 3:
        hexa = "".join(c * 2 for c in hexa)
    canais = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a: str, b: str) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def paletas(css: str):
    """{nome: {var: cor}} para :root e cada .d-*"""
    out = {}
    raiz = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
    out[":root"] = dict(re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{3,6})", raiz))
    for nome, corpo in re.findall(r"\.(d-[\w-]+)\s*\{([^}]*)\}", css):
        out[nome] = dict(re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{3,6})", corpo))
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    minimo = 3.0
    if "--minimo" in sys.argv:
        minimo = float(sys.argv[sys.argv.index("--minimo") + 1])
    pal = paletas(CSS.read_text(encoding="utf-8"))
    falhas = 0
    print(f"{'paleta':18} {'variável':12} {'cor':8} contraste (branco)")
    for nome, cores in pal.items():
        vars_ = ("--disc", "--disc-2") + (SEMANTICAS if nome == ":root" else ())
        for v in vars_:
            if v not in cores:
                continue
            c = contraste("#FFFFFF", cores[v])
            ok = c >= minimo
            falhas += not ok
            print(f"{nome:18} {v:12} {cores[v]:8} {c:5.2f}:1 {'ok' if ok else 'FALHA'}")
    if falhas:
        print(f"falhou: {falhas} cor(es) abaixo de {minimo}:1")
        sys.exit(1)
    print(f"ok: todas as cores >= {minimo}:1 com texto branco")


if __name__ == "__main__":
    main()
