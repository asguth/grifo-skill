#!/usr/bin/env python3
"""Renderiza um HTML do Grifo-Skill em PDF A4 e PNG (uma imagem por folha).

Uso:  python3 renderizar.py apostila.html [pasta_saida] [--pb] [--json] [--estrito]

  --pb       salva também <nome>-pN-pb.png em tons de cinza (leitura em P&B)
  --json     imprime o relatório em JSON (para os agentes revisores) em vez de texto
  --estrito  sai com código 1 se houver qualquer aviso (uso em CI)

Requer Playwright com Chromium (pip install playwright && playwright install chromium).
Se não houver Playwright, tenta Chrome/Chromium headless só para o PDF.

Revisão de layout (cada item vira um aviso com tipo, folha e elemento):
  pagina      folha mais alta que A4 (o conteúdo vai quebrar em outra página)
  lateral     elemento que vaza pela lateral da folha
  transborda  conteúdo maior que a própria caixa (scrollWidth > clientWidth)
  colunas     diferença de altura entre as colunas da folha > 25%
  fonte       texto com fonte calculada < 8 pt
Licença MIT.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

A4_ALTURA_PX = 1123  # 297mm a 96 dpi
LIMITE_COLUNAS = 0.25
FONTE_MIN_PT = 8

JS_REVISAO = r"""
({alt, limCol, fonteMin}) => {
  const avisos = [];
  const desc = el => {
    const cls = (el.className && (el.className.baseVal ?? el.className)) || '';
    const txt = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50);
    return `<${el.tagName.toLowerCase()}${cls ? ' class="' + cls + '"' : ''}>` + (txt ? ` "${txt}"` : '');
  };
  const add = (tipo, folha, msg, el) => avisos.push({tipo, folha, msg, elemento: el ? desc(el) : null});

  document.querySelectorAll('.folha').forEach((f, i) => {
    const n = i + 1, r = f.getBoundingClientRect();
    if (r.height > alt + 2)
      add('pagina', n, `altura ${Math.round(r.height)}px > A4 (${alt}px): conteúdo vai quebrar em outra página`);

    const transbordam = [];
    f.querySelectorAll('*').forEach(el => {
      if (el.closest('.sprite')) return;
      const e = el.getBoundingClientRect();
      if (e.width && (e.right > r.right + 1 || e.left < r.left - 1)) {
        add('lateral', n, 'vaza pela lateral da folha', el);
        return;
      }
      const cs = getComputedStyle(el);
      // conteúdo maior que a própria caixa: mede o texto próprio e os filhos em
      // fluxo (ignora posicionados, ex. setas ::after do .fluxo, e SVG interno)
      if (el.clientWidth > 0 && cs.display !== 'inline' && !(el instanceof SVGElement)
          && cs.overflowX === 'visible') {
        const dentroDir = e.left + el.clientLeft + el.clientWidth;
        const dentroEsq = e.left + el.clientLeft;
        let excesso = 0;
        for (const c of el.childNodes) {
          let rects = [];
          if (c.nodeType === 3 && c.textContent.trim()) {
            const rg = document.createRange(); rg.selectNodeContents(c); rects = [...rg.getClientRects()];
          } else if (c.nodeType === 1 && !(c instanceof SVGElement && c.tagName.toLowerCase() !== 'svg')) {
            const p = getComputedStyle(c).position;
            if (p === 'absolute' || p === 'fixed') continue;
            rects = [...c.getClientRects()];
          }
          for (const q of rects) {
            if (!q.width) continue;
            excesso = Math.max(excesso, q.right - dentroDir, dentroEsq - q.left);
          }
        }
        if (excesso > 1.5) transbordam.push([el, excesso]);
      }
      // fonte < mínimo em elemento com texto próprio
      const temTexto = [...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim());
      if (temTexto && cs.visibility !== 'hidden' && cs.display !== 'none') {
        const pt = parseFloat(cs.fontSize) * 0.75;
        if (pt < fonteMin - 0.05) add('fonte', n, `fonte ${pt.toFixed(1)}pt < ${fonteMin}pt`, el);
      }
    });

    // reporta só o elemento mais interno de cada cadeia que transborda
    for (const [el, ex] of transbordam)
      if (!transbordam.some(([o]) => o !== el && el.contains(o)))
        add('transborda', n, `conteúdo ${Math.round(ex)}px maior que a caixa`, el);

    f.querySelectorAll('.apostila-colunas').forEach(g => {
      const cols = [...g.querySelectorAll(':scope > .coluna')];
      if (cols.length < 2) return;
      const alturas = cols.map(c => {
        const filhos = [...c.children];
        if (!filhos.length) return 0;
        return filhos[filhos.length - 1].getBoundingClientRect().bottom - c.getBoundingClientRect().top;
      });
      const max = Math.max(...alturas), min = Math.min(...alturas);
      if (max > 0 && (max - min) / max > limCol)
        add('colunas', n, `colunas desequilibradas: ${alturas.map(a => Math.round(a)).join(' × ')}px `
            + `(diferença de ${Math.round(100 * (max - min) / max)}% > ${Math.round(100 * limCol)}%)`);
    });
  });

  // agrupa avisos iguais (mesma folha, tipo e elemento)
  const unicos = [], chaves = new Set();
  for (const a of avisos) {
    const k = [a.tipo, a.folha, a.msg, a.elemento].join('|');
    if (!chaves.has(k)) { chaves.add(k); unicos.push(a); }
  }
  return unicos;
}
"""


def com_playwright(html: Path, saida: Path, pb: bool):
    from playwright.sync_api import sync_playwright

    pngs = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=2)
        pag.goto(html.resolve().as_uri())
        pag.wait_for_load_state("networkidle")
        pag.evaluate("document.fonts.ready")
        pag.wait_for_timeout(300)
        pdf = saida / f"{html.stem}.pdf"
        pag.pdf(path=str(pdf), format="A4", print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})

        folhas = pag.query_selector_all(".folha")
        for i, f in enumerate(folhas, 1):
            png = saida / f"{html.stem}-p{i}.png"
            f.screenshot(path=str(png))
            pngs.append(str(png))
            if pb:
                from PIL import Image  # Pillow vem junto na maioria dos ambientes
                cinza = saida / f"{html.stem}-p{i}-pb.png"
                Image.open(png).convert("L").save(cinza)
                pngs.append(str(cinza))

        avisos = pag.evaluate(JS_REVISAO, {"alt": A4_ALTURA_PX, "limCol": LIMITE_COLUNAS,
                                           "fonteMin": FONTE_MIN_PT})
        nav.close()
    return {"arquivo": str(html), "folhas": len(folhas), "pdf": str(pdf), "pngs": pngs,
            "avisos": avisos, "ok": not avisos}


def com_chrome(html: Path, saida: Path):
    for nome in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        exe = shutil.which(nome)
        if exe:
            subprocess.run([exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={saida / (html.stem + '.pdf')}", html.resolve().as_uri()],
                           check=True, capture_output=True)
            return True
    return False


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    desconhecidas = flags - {"--pb", "--json", "--estrito"}
    if not args or desconhecidas:
        sys.exit(__doc__ + (f"\nflag desconhecida: {', '.join(sorted(desconhecidas))}" if desconhecidas else ""))
    html = Path(args[0])
    saida = Path(args[1]) if len(args) > 1 else html.parent
    saida.mkdir(parents=True, exist_ok=True)
    try:
        rel = com_playwright(html, saida, "--pb" in flags)
    except ImportError:
        if com_chrome(html, saida):
            print("ok: PDF gerado via Chrome headless (sem PNG/checagem — instale Playwright)")
            return
        sys.exit("erro: instale Playwright ou Chrome para renderizar")

    if "--json" in flags:
        print(json.dumps(rel, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {rel['folhas']} folha(s) -> {saida}")
        for a in rel["avisos"]:
            el = f" {a['elemento']}" if a["elemento"] else ""
            print(f"LAYOUT [{a['tipo']}] folha {a['folha']}:{el} — {a['msg']}")
        if not rel["avisos"]:
            print("LAYOUT: sem avisos")
    if "--estrito" in flags and rel["avisos"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
