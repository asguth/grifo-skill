#!/usr/bin/env python3
"""Figuras didáticas confiáveis para o Grifo-Skill: acervo aberto ou gerada a partir de dados.

Uso:
  python3 figura.py buscar "termos" [--n 12] [--todas]
      Procura no Wikimedia Commons (onde estão as figuras da OpenStax, Servier Medical
      Art, NIH e muitas outras) e lista título, licença, autor e tamanho. Por padrão só
      mostra licenças aceitas (CC0, domínio público, CC BY, CC BY-SA); --todas mostra
      também as recusadas, com o motivo.
      Dica: "OpenStax heart" para figuras de livro didático; "Servier unlabeled heart"
      ou "(unannotated)" para imagem sem rótulos, que recebe chamadas numeradas.

  python3 figura.py baixar "File:Nome.jpg" pasta/ [--largura 1280] [--nome slug]
      Baixa a imagem (já redimensionada pelo Commons), grava pasta/slug.<ext> e
      pasta/slug.json (título, autor, licença, links) e imprime o HTML da <figure>
      com o crédito pronto. Recusa licença NC, ND, GFDL-only ou sem licença.

  python3 figura.py molecula "SMILES" saida.svg [--largura 600]
      Desenha a fórmula estrutural a partir do SMILES (RDKit: pip install rdkit).
      Ligações e átomos saem da notação, não de desenho à mão. Confira o SMILES no
      PubChem antes.

Precisa de internet para buscar/baixar. Licença MIT.
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
# A política do Wikimedia pede User-Agent identificável; defina GRIFO_UA com um contato
# (ex.: "MeuProjeto/1.0 (https://… ; email)") para ter limites de requisição maiores.
UA = os.environ.get("GRIFO_UA") or "study-figures/1.0 (open-licensed figure fetcher; python-urllib)"
EXTS = {".jpg", ".jpeg", ".png", ".svg", ".webp", ".gif", ".tif", ".tiff"}


# --------------------------------------------------------------------------
# licença
# --------------------------------------------------------------------------
def avaliar_licenca(curta: str, url: str = "") -> tuple[bool, str]:
    """(aceita, observação). Aceita CC0, domínio público, CC BY e CC BY-SA."""
    s = (curta or "").strip().lower()
    if not s:
        return False, "sem licença declarada"
    if re.search(r"\bnc\b|non-?commercial", s):
        return False, "NC (uso não comercial) — recusada"
    if re.search(r"\bnd\b|no ?deriv", s):
        return False, "ND (sem derivadas) — recusada"
    if "cc0" in s or "public domain" in s or s.startswith("pd") or "domínio público" in s:
        return True, "domínio público / CC0"
    if re.search(r"cc[ -]by[ -]sa", s):
        return True, "CC BY-SA: use sem alterar a imagem e com crédito"
    if re.search(r"cc[ -]by\b", s):
        return True, "CC BY: crédito obrigatório"
    if "gfdl" in s:
        return False, "só GFDL (exige anexar a licença inteira) — recusada"
    return False, f"licença não reconhecida ({curta}) — confira à mão"


def limpar(htm: str) -> str:
    texto = re.sub(r"<[^>]+>", "", htm or "")
    return re.sub(r"\s+", " ", html.unescape(texto)).strip()


# --------------------------------------------------------------------------
# Commons
# --------------------------------------------------------------------------
def api(params: dict) -> dict:
    params = {"format": "json", "formatversion": "2", "maxlag": "5", **params}
    url = API + "?" + urllib.parse.urlencode(params)
    for tentativa in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            corpo = urllib.request.urlopen(req, timeout=40).read()
            dados = json.loads(corpo)
            if dados.get("error", {}).get("code") == "maxlag":
                raise ValueError("maxlag")
            return dados
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, json.JSONDecodeError) as e:
            espera = 5 * (tentativa + 1)
            print(f"aviso: Commons respondeu {e!s:.60}; nova tentativa em {espera}s", file=sys.stderr)
            time.sleep(espera)
    sys.exit("erro: Commons não respondeu (limite de requisições ou sem rede). Tente de novo em alguns minutos.")


def info_arquivos(params: dict, largura: int = 0) -> list[dict]:
    p = {"action": "query", "prop": "imageinfo",
         "iiprop": "url|size|mime|extmetadata",
         "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist|Credit|ImageDescription|UsageTerms|AttributionRequired",
         **params}
    if largura:
        p["iiurlwidth"] = str(largura)
    paginas = api(p).get("query", {}).get("pages", [])
    out = []
    for pg in sorted(paginas, key=lambda x: x.get("index", 0)):
        ii = (pg.get("imageinfo") or [{}])[0]
        meta = {k: (v or {}).get("value", "") for k, v in (ii.get("extmetadata") or {}).items()}
        aceita, obs = avaliar_licenca(meta.get("LicenseShortName", ""), meta.get("LicenseUrl", ""))
        out.append({
            "titulo": pg.get("title", ""),
            "pagina": ii.get("descriptionurl", ""),
            "url": ii.get("url", ""),
            "miniatura": ii.get("thumburl", ""),
            "bytes": ii.get("size", 0),
            "largura": ii.get("width"),
            "altura": ii.get("height"),
            "mime": ii.get("mime", ""),
            "licenca": meta.get("LicenseShortName", ""),
            "licenca_url": meta.get("LicenseUrl", ""),
            "autor": limpar(meta.get("Artist", "")),
            "credito": limpar(meta.get("Credit", "")),
            "descricao": limpar(meta.get("ImageDescription", ""))[:300],
            "aceita": aceita,
            "obs": obs,
        })
    return out


def buscar(termos: str, n: int, todas: bool):
    res = info_arquivos({"generator": "search", "gsrsearch": f"filetype:bitmap|drawing {termos}",
                         "gsrnamespace": "6", "gsrlimit": str(max(n * 2, 10))})
    mostrados = 0
    for r in res:
        if not todas and not r["aceita"]:
            continue
        marca = "ok " if r["aceita"] else "NÃO"
        print(f"[{marca}] {r['titulo']}")
        print(f"      {r['largura']}×{r['altura']} · {r['licenca'] or 'sem licença'} · {r['obs']}")
        print(f"      autor: {r['autor'][:90] or '?'}")
        if r["descricao"]:
            print(f"      {r['descricao'][:140]}")
        mostrados += 1
        if mostrados >= n:
            break
    if not mostrados:
        print("nada com licença aceita; tente outros termos (em inglês costuma render mais) ou --todas")


def slug(texto: str) -> str:
    t = re.sub(r"^File:", "", texto)
    t = Path(t).stem.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60] or "figura"


PADRAO = (500, 960, 1280, 1920)  # larguras de miniatura em cache no Commons


def baixar(titulo: str, pasta: Path, largura: int, nome: str | None):
    largura = next((w for w in PADRAO if w >= largura), PADRAO[-1])
    if not titulo.startswith("File:"):
        titulo = "File:" + titulo
    res = info_arquivos({"titles": titulo}, largura)
    if not res or not res[0]["url"]:
        sys.exit(f"erro: {titulo} não encontrado no Commons")
    r = res[0]
    if not r["aceita"]:
        sys.exit(f"erro: licença recusada para {titulo}: {r['obs']}")
    # miniatura em largura padrão do Commons (o original costuma ser recusado com 429);
    # SVG e TIFF chegam como PNG renderizado
    url = r["miniatura"] or r["url"]
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".png"
    pasta.mkdir(parents=True, exist_ok=True)
    base = nome or slug(titulo)
    destino = pasta / f"{base}{'.jpg' if ext == '.jpeg' else ext}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for tentativa in range(4):
        try:
            dados = urllib.request.urlopen(req, timeout=90).read()
            break
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if tentativa == 3:
                sys.exit(f"erro ao baixar {url}: {e}")
            time.sleep(5 * (tentativa + 1))
    destino.write_bytes(dados)
    reduzir(destino, largura)
    r["arquivo"] = destino.name
    r["baixado_em"] = time.strftime("%Y-%m-%d")
    (pasta / f"{base}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ok: {destino} ({destino.stat().st_size // 1024} KB)")
    print(f"licença: {r['licenca']} — {r['obs']}")
    if re.search(r"deriv|translat|tradu|based on|modified|revised", " ".join([r["credito"], r["autor"], r["descricao"]]), re.I):
        print("ATENÇÃO: obra derivada. Confira a licença do original (uma tradução marcada como domínio\n"
              "público de um original CC BY-SA continua CC BY-SA) e credite os dois autores.")
    print("\nHTML (ajuste alt, legenda e o caminho relativo ao HTML-fonte):\n")
    print(html_figura(r, f"{pasta.name}/{destino.name}"))


def reduzir(arq: Path, largura: int):
    """Reduz raster maior que `largura` px, põe fundo branco no lugar da transparência
    (no PDF e no P&B o fundo some) e recomprime. Precisa de Pillow."""
    try:
        from PIL import Image
    except ImportError:
        print("aviso: sem Pillow, a imagem fica no tamanho original", file=sys.stderr)
        return
    im = Image.open(arq)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fundo = Image.new("RGBA", im.size, "white")
        fundo.alpha_composite(im)
        im = fundo
    im = im.convert("RGB")
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    if arq.suffix.lower() in {".jpg", ".jpeg"}:
        im.save(arq, quality=85, optimize=True, progressive=True)
    else:  # diagrama: 256 cores bastam e reduzem muito o PNG
        im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(arq, optimize=True)


PADRAO = (500, 960, 1280, 1920)  # larguras de miniatura em cache no Commons


def baixar(titulo: str, pasta: Path, largura: int, nome: str | None):
    largura = next((w for w in PADRAO if w >= largura), PADRAO[-1])
    if not titulo.startswith("File:"):
        titulo = "File:" + titulo
    res = info_arquivos({"titles": titulo}, largura)
    if not res or not res[0]["url"]:
        sys.exit(f"erro: {titulo} não encontrado no Commons")
    r = res[0]
    if not r["aceita"]:
        sys.exit(f"erro: licença recusada para {titulo}: {r['obs']}")
    # miniatura em largura padrão do Commons (o original costuma ser recusado com 429);
    # SVG e TIFF chegam como PNG renderizado
    url = r["miniatura"] or r["url"]
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".png"
    pasta.mkdir(parents=True, exist_ok=True)
    base = nome or slug(titulo)
    destino = pasta / f"{base}{'.jpg' if ext == '.jpeg' else ext}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for tentativa in range(4):
        try:
            dados = urllib.request.urlopen(req, timeout=90).read()
            break
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if tentativa == 3:
                sys.exit(f"erro ao baixar {url}: {e}")
            time.sleep(5 * (tentativa + 1))
    destino.write_bytes(dados)
    reduzir(destino, largura)
    r["arquivo"] = destino.name
    r["baixado_em"] = time.strftime("%Y-%m-%d")
    (pasta / f"{base}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ok: {destino} ({destino.stat().st_size // 1024} KB)")
    print(f"licença: {r['licenca']} — {r['obs']}")
    if re.search(r"deriv|translat|tradu|based on|modified|revised", " ".join([r["credito"], r["autor"], r["descricao"]]), re.I):
        print("ATENÇÃO: obra derivada. Confira a licença do original (uma tradução marcada como domínio\n"
              "público de um original CC BY-SA continua CC BY-SA) e credite os dois autores.")
    print("\nHTML (ajuste alt, legenda e o caminho relativo ao HTML-fonte):\n")
    print(html_figura(r, f"{pasta.name}/{destino.name}"))


def reduzir(arq: Path, largura: int):
    """Reduz raster maior que `largura` px (Pillow) e recomprime; mantém o formato."""
    try:
        from PIL import Image
    except ImportError:
        print("aviso: sem Pillow, a imagem fica no tamanho original", file=sys.stderr)
        return
    im = Image.open(arq)
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    if arq.suffix.lower() in {".jpg", ".jpeg"}:
        im.convert("RGB").save(arq, quality=85, optimize=True, progressive=True)
    else:
        im.save(arq, optimize=True)


def html_figura(r: dict, src: str) -> str:
    autor = html.escape((r["autor"] or "autoria na página do arquivo")[:120])
    lic = html.escape(r["licenca"])
    lic_html = f'<a href="{html.escape(r["licenca_url"])}">{lic}</a>' if r["licenca_url"] else lic
    return (
        '<figure class="figura aberta">\n'
        f'  <img src="{html.escape(src)}" alt="[[descrição curta da imagem]]">\n'
        "  <figcaption>[[o que a figura mostra; vista; o que as cores significam]]\n"
        f'    <span class="credito">Imagem: {autor}, <a href="{html.escape(r["pagina"])}">Wikimedia Commons</a>, '
        f"{lic_html}.</span></figcaption>\n"
        "</figure>"
    )


# --------------------------------------------------------------------------
# molécula (RDKit)
# --------------------------------------------------------------------------
def molecula(smiles: str, saida: Path, largura: int):
    try:
        from rdkit import Chem
        from rdkit.Chem.Draw import rdMolDraw2D
    except ImportError:
        sys.exit("erro: instale o RDKit (pip install rdkit) para desenhar moléculas")
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        sys.exit(f"erro: SMILES inválido: {smiles}")
    altura = round(largura * 0.6)
    d = rdMolDraw2D.MolDraw2DSVG(largura, altura)
    op = d.drawOptions()
    op.clearBackground = False
    op.bondLineWidth = 2
    op.fixedFontSize = 22
    op.addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", d.GetDrawingText())
    saida.write_text(svg, encoding="utf-8")
    from rdkit.Chem.rdMolDescriptors import CalcMolFormula
    print(f"ok: {saida} · fórmula {CalcMolFormula(mol)}")
    print(f'HTML: <figure class="figura aberta"><img src="{saida.name}" alt="Fórmula estrutural"> '
          '<figcaption>[[nome]]. <span class="credito">Desenho gerado com RDKit a partir do SMILES.</span>'
          "</figcaption></figure>")


# --------------------------------------------------------------------------
def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a or a[0] in {"-h", "--help"}:
        sys.exit(__doc__)

    def opt(nome, padrao=None):
        if nome in a:
            i = a.index(nome)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return padrao

    cmd = a.pop(0)
    if cmd == "buscar":
        n = int(opt("--n", 12))
        todas = "--todas" in a
        a = [x for x in a if x != "--todas"]
        if not a:
            sys.exit(__doc__)
        buscar(" ".join(a), n, todas)
    elif cmd == "baixar":
        largura, nome = int(opt("--largura", 1280)), opt("--nome")
        if len(a) != 2:
            sys.exit(__doc__)
        baixar(a[0], Path(a[1]), largura, nome)
    elif cmd == "molecula":
        largura = int(opt("--largura", 600))
        if len(a) != 2:
            sys.exit(__doc__)
        molecula(a[0], Path(a[1]), largura)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
