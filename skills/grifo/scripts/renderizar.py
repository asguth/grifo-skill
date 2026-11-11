#!/usr/bin/env python3
"""Renderiza um HTML do Grifo-Skill em PDF A4 e PNG (uma imagem por folha).

Uso:  python3 renderizar.py apostila.html [pasta_saida]

Requer Playwright com Chromium (pip install playwright && playwright install chromium).
Se não houver Playwright, tenta Chrome/Chromium headless só para o PDF.
Saída: <nome>.pdf e <nome>-p1.png, <nome>-p2.png ... (para revisão visual).
Também imprime avisos de layout: folhas que estouram a altura A4 e
elementos que vazam pela lateral. Licença MIT.
"""
import shutil
import subprocess
import sys
from pathlib import Path

A4_ALTURA_PX = 1123  # 297mm a 96 dpi


def com_playwright(html: Path, saida: Path):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=2)
        pag.goto(html.resolve().as_uri())
        pag.wait_for_timeout(400)
        pag.pdf(path=str(saida / f"{html.stem}.pdf"), format="A4", print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})

        folhas = pag.query_selector_all(".folha")
        for i, f in enumerate(folhas, 1):
            f.screenshot(path=str(saida / f"{html.stem}-p{i}.png"))

        problemas = pag.evaluate(
            """(alt) => {
              const out = [];
              document.querySelectorAll('.folha').forEach((f, i) => {
                const h = f.getBoundingClientRect().height;
                if (h > alt + 2) out.push(`folha ${i+1}: altura ${Math.round(h)}px > A4 (${alt}px) — conteúdo vai quebrar em outra página`);
                const r = f.getBoundingClientRect();
                f.querySelectorAll('*').forEach(el => {
                  const e = el.getBoundingClientRect();
                  if (e.width && (e.right > r.right + 1 || e.left < r.left - 1))
                    out.push(`folha ${i+1}: <${el.tagName.toLowerCase()} class="${el.className.baseVal ?? el.className}"> vaza pela lateral`);
                });
              });
              return [...new Set(out)].slice(0, 30);
            }""",
            A4_ALTURA_PX,
        )
        nav.close()
    return len(folhas), problemas


def com_chrome(html: Path, saida: Path):
    for nome in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        exe = shutil.which(nome)
        if exe:
            subprocess.run([exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={saida / (html.stem + '.pdf')}", html.resolve().as_uri()],
                           check=True, capture_output=True)
            return True
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    html = Path(sys.argv[1])
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else html.parent
    saida.mkdir(parents=True, exist_ok=True)
    try:
        n, probs = com_playwright(html, saida)
        print(f"ok: {n} folha(s) -> {saida}")
        for pr in probs:
            print("LAYOUT:", pr)
        if not probs:
            print("LAYOUT: sem estouros detectados")
    except ImportError:
        if com_chrome(html, saida):
            print("ok: PDF gerado via Chrome headless (sem PNG/checagem — instale Playwright)")
        else:
            sys.exit("erro: instale Playwright ou Chrome para renderizar")
