#!/usr/bin/env python3
"""Regenera tudo o que o README mostra (ferramenta do repositório, fora da skill).

Uso:  python ferramentas/atualizar_docs.py

1. monta cada exemplos/<slug>-fonte.html -> exemplos/<slug>.html
2. renderiza: PDF em exemplos/<slug>.pdf e PNG por folha em docs/exemplos/
   (redimensionado para 1100 px de largura, otimizado)
3. regenera a galeria (docs/galeria.png, docs/galeria-componentes.png)
4. monta docs/demo.gif: folheia a 1ª folha de cada exemplo com transição suave
5. docs/exemplos/mosaico.png: as folhas 1 lado a lado (prévia do README)
Falha se algum exemplo tiver aviso de layout.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
S = REPO / "skills" / "grifo" / "scripts"
EXEMPLOS = REPO / "exemplos"
DOCS = REPO / "docs"
LARGURA_PNG = 1100
COM_CAPA = {"economia-oferta-demanda"}
LARGURA_GIF = 560
ORDEM = [  # ordem de exibição no GIF e no mosaico (o 1º abre com a capa)
    "economia-oferta-demanda", "medicina-coracao", "lgpd-bases-legais", "portugues-crase",
    "rlm-proposicoes", "lei-8112-servidores", "lei-9784-processo-administrativo", "en-photosynthesis",
]


def rodar(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        sys.exit(f"falhou: {' '.join(map(str, args))}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    destino = DOCS / "exemplos"
    destino.mkdir(parents=True, exist_ok=True)
    velhos = set(destino.glob("*.png"))  # só some o que não for regenerado, e só no fim

    paginas = {}
    for fonte in sorted(EXEMPLOS.glob("*-fonte.html")):
        slug = fonte.name[: -len("-fonte.html")]
        if slug == "galeria":
            continue
        html = EXEMPLOS / f"{slug}.html"
        rodar(S / "montar.py", fonte, html)
        with tempfile.TemporaryDirectory() as tmp:
            rel = json.loads(rodar(S / "renderizar.py", html, tmp, "--json"))
            if rel["avisos"]:
                sys.exit(f"{slug}: {len(rel['avisos'])} aviso(s) de layout — corrija antes:\n"
                         + "\n".join(f"  folha {a['folha']} [{a['tipo']}] {a['msg']}" for a in rel["avisos"]))
            shutil.copy(Path(tmp) / f"{slug}.pdf", EXEMPLOS / f"{slug}.pdf")
            paginas[slug] = []
            for i in range(1, rel["folhas"] + 1):
                im = Image.open(Path(tmp) / f"{slug}-p{i}.png").convert("RGB")  # noqa
                im = im.resize((LARGURA_PNG, round(im.height * LARGURA_PNG / im.width)), Image.LANCZOS)
                out = destino / f"{slug}-p{i}.png"
                im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
                paginas[slug].append(out)
        print(f"ok: {slug} ({rel['folhas']} folhas)")

    for velho in velhos - {p for lista in paginas.values() for p in lista} - {destino / "mosaico.png"}:
        velho.unlink()

    rodar(REPO / "ferramentas" / "galeria.py")
    print("ok: galeria")

    # --- GIF: folhas 1 e 2 de cada exemplo, corte seco (fade gera quadros pesados e borrados) ---
    quadros = []
    for s in ORDEM:
        pags = paginas.get(s, [])
        # apostila com capa: capa + 1ª folha de conteúdo (pula o sumário)
        escolhidas = [pags[0], pags[2]] if s in COM_CAPA and len(pags) > 2 else pags[:2]
        for png in escolhidas:
            im = Image.open(png).convert("RGB")
            quadros.append(im.resize((LARGURA_GIF, round(im.height * LARGURA_GIF / im.width)), Image.LANCZOS))
    duracoes = [1600] * len(quadros)
    paleta = [q.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for q in quadros]
    gif = DOCS / "demo.gif"
    paleta[0].save(gif, save_all=True, append_images=paleta[1:], duration=duracoes, loop=0, optimize=True,
                   disposal=1)
    print(f"ok: {gif.relative_to(REPO)} ({gif.stat().st_size // 1024} KB, {len(quadros)} quadros)")

    # --- mosaico das folhas 1 ---
    miniat = [Image.open(paginas[s][0]).convert("RGB") for s in ORDEM if s in paginas]
    w, gap, por_linha = 360, 24, 4
    miniat = [m.resize((w, round(m.height * w / m.width)), Image.LANCZOS) for m in miniat]
    h = max(m.height for m in miniat)
    linhas = -(-len(miniat) // por_linha)
    mosaico = Image.new("RGB", (por_linha * w + (por_linha + 1) * gap, linhas * h + (linhas + 1) * gap), "#E9ECEF")
    for i, m in enumerate(miniat):
        lin, col = divmod(i, por_linha)
        mosaico.paste(m, (gap + col * (w + gap), gap + lin * (h + gap)))
    mosaico.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(destino / "mosaico.png", optimize=True)
    print("ok: docs/exemplos/mosaico.png")


if __name__ == "__main__":
    main()
