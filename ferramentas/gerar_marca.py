#!/usr/bin/env python3
"""Gera os arquivos de marca a partir de docs/marca/mascote.png (fonte única).

Uso:  python ferramentas/gerar_marca.py

  docs/marca/logo.png     horizontal, 1600 px de largura, fundo transparente (README)
  docs/marca/icone.png    512×512 (avatar do GitHub e favicon)
  docs/marca/social.png   1280×640 (social preview do GitHub)
  skills/grifo/assets/mascote/grifo.webp   448×448, ≤ 40 KB (usado nas apostilas)
O mascote e a marca são MIT, como o resto do repositório.
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
MARCA = REPO / "docs" / "marca"
MASCOTE = MARCA / "mascote.png"
WEBP = REPO / "skills" / "grifo" / "assets" / "mascote" / "grifo.webp"

AZUL = "#143153"        # cor média do grifo
AZUL_ESCURO = "#0B1D33"
AMARELO = "#FFE45C"     # marca-texto (--mt-chave do design system)
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700'
          '&family=Poppins:wght@700;800;900&display=swap" rel="stylesheet">')


def data_uri(img: Image.Image) -> str:
    b = io.BytesIO()
    img.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode("ascii")


def quadrado(m: Image.Image, lado: int, ocupacao: float = 0.985) -> Image.Image:
    alvo = int(lado * ocupacao)
    w = round(m.width * alvo / m.height)
    c = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    r = m.resize((w, alvo), Image.LANCZOS)
    c.paste(r, ((lado - w) // 2, lado - alvo - (lado - alvo) // 2), r)
    return c


def html(corpo: str, css: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTES}
<style>*{{margin:0;padding:0;box-sizing:border-box}} html,body{{background:transparent}} {css}</style>
</head><body>{corpo}</body></html>"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    m = Image.open(MASCOTE).convert("RGBA")
    src = data_uri(m)

    # WebP das apostilas
    quadrado(m, 448).save(WEBP, "WEBP", quality=88, method=6, alpha_quality=90)
    print(f"ok: {WEBP.relative_to(REPO)} ({WEBP.stat().st_size // 1024} KB)")

    marca_texto = f"""
      .nome{{font-family:Poppins;font-weight:900;color:{AZUL_ESCURO};letter-spacing:-.02em;line-height:1}}
      .nome .g{{background:linear-gradient(transparent 58%,{AMARELO} 58%,{AMARELO} 92%,transparent 92%);padding:0 .06em}}
      .nome .s{{color:{AZUL}}}
      .frase{{font-family:Inter;font-weight:600;color:{AZUL};letter-spacing:.01em}}"""

    pecas = {
        "logo.png": ((1600, 520), True, html(
            f"""<div class="logo"><img src="{src}"><div><div class="nome"><span class="g">Grifo</span><span class="s">-Skill</span></div>
            <div class="frase">Resumos ilustrados para concursos</div></div></div>""",
            marca_texto + """
            .logo{width:1600px;height:520px;display:flex;align-items:center;gap:56px;padding:0 70px}
            .logo img{height:440px}
            .nome{font-size:168px} .frase{font-size:50px;margin-top:22px;padding-left:8px}""")),
        "icone.png": ((512, 512), False, html(
            f"""<div class="ic"><img src="{src}"></div>""",
            f""".ic{{width:512px;height:512px;background:{AMARELO};display:grid;place-items:center}}
            .ic img{{height:400px;transform:translate(6px,8px)}}""")),
        "social.png": ((1280, 640), False, html(
            f"""<div class="soc"><img src="{src}"><div class="txt">
              <div class="nome"><span class="g">Grifo</span><span class="s">-Skill</span></div>
              <div class="frase">Resumos ilustrados para concursos</div>
              <div class="selos"><span>Skill de IA para Claude</span><span>Open source · MIT</span><span>PDF A4 pronto</span></div>
            </div></div>""",
            marca_texto + f"""
            .soc{{width:1280px;height:640px;background:#F6F7F9;display:flex;align-items:center;gap:40px;padding:0 70px;
                  border-bottom:14px solid {AMARELO}}}
            .soc img{{height:500px}}
            .nome{{font-size:118px}} .frase{{font-size:42px;margin-top:18px;color:{AZUL_ESCURO}}}
            .selos{{display:flex;gap:12px;margin-top:34px;flex-wrap:wrap}}
            .selos span{{font-family:Inter;font-weight:700;font-size:22px;color:{AZUL};border:2.5px solid {AZUL};
                         border-radius:999px;padding:6px 18px}}""")),
    }
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for nome, ((w, h), transparente, doc) in pecas.items():
            pag = nav.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            pag.set_content(doc)
            pag.wait_for_load_state("networkidle")
            pag.evaluate("document.fonts.ready")
            pag.wait_for_timeout(200)
            out = MARCA / nome
            pag.screenshot(path=str(out), omit_background=transparente, clip={"x": 0, "y": 0, "width": w, "height": h})
            img = Image.open(out)
            if transparente:  # apara a sobra transparente, mantendo 40 px de respiro
                x0, y0, x1, y1 = img.getbbox()
                img = img.crop((max(x0 - 40, 0), max(y0 - 40, 0), min(x1 + 40, w), min(y1 + 40, h)))
            img.save(out, optimize=True)
            print(f"ok: docs/marca/{nome} {img.width}×{img.height} ({out.stat().st_size // 1024} KB)")
            pag.close()
        nav.close()


if __name__ == "__main__":
    main()
