#!/usr/bin/env python3
"""Gera a galeria de ilustrações e componentes do Grifo-Skill.

Uso:  python3 galeria.py [pasta_exemplos] [pasta_docs]
      (padrão: <repo>/exemplos e <repo>/docs)

1. Lê os <symbol> de assets/ilustracoes.svg (na ordem do arquivo, agrupados
   pelos comentários de seção) e escreve exemplos/galeria-fonte.html —
   nunca editar esse arquivo à mão: ele é sobrescrito.
2. Monta (montar.py) -> exemplos/galeria.html.
3. Renderiza (renderizar.py) e copia a folha 1 para docs/galeria.png e a
   folha 2 para docs/galeria-componentes.png.
Licença MIT.
"""
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
REPO = SKILL.parent.parent
SPRITE = SKILL / "assets" / "ilustracoes.svg"
COLUNAS = 10

CABECA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Galeria Grifo</title>
<!-- GERADO POR scripts/galeria.py — não editar à mão -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Poppins:wght@600;700;800;900&display=swap" rel="stylesheet">
<!--APOSTILA:CSS-->
<style>
.gal-grupo{font-family:var(--fonte-titulo);font-weight:800;font-size:8.5pt;text-transform:uppercase;color:var(--disc);border-bottom:1.5px solid var(--disc-claro);margin-top:1.5mm}
.gal{display:grid;grid-template-columns:repeat(%(col)d,minmax(0,1fr));gap:1.2mm 1mm}
.gal div{text-align:center;font-size:8pt;color:var(--tinta-2);overflow-wrap:anywhere;line-height:1.1}
.gal svg{width:14mm;height:14mm;display:block;margin:0 auto .5mm}
</style>
</head><body class="d-penal"><!--APOSTILA:SPRITE-->
"""

TOPO = ('<div class="topo"><div class="logo"><svg viewBox="0 0 64 64"><use href="#i-grifo"/></svg></div>'
        '<div class="titulo-topo">{titulo}<small>design system grifo</small></div><div class="pag">{n:02d}</div></div>')

RODAPE = ('<div class="rodape-folha"><span>Grifo-Skill · MIT</span>'
          '<span>Gerado por scripts/galeria.py · {n} ilustrações</span></div>')

# Folha 2: amostra de componentes (atualize quando criar componente novo).
COMPONENTES = """
<div class="apostila-colunas">
 <div class="coluna"><div class="coluna-cab">Blocos e listas</div>
  <div class="bloco"><div class="faixa">Penas restritivas de direito</div><div class="corpo">
   <div class="sub">Interdição temporária de direitos</div>
   <div class="com-ilustra"><ul class="check"><li>Cargo público;</li><li>Profissão;</li><li>Habilitação;</li><li>Concurso público.</li></ul><svg class="ilustra g"><use href="#i-documento"/></svg></div>
  </div></div>
  <div class="bloco primaria"><div class="faixa">Requisitos subjetivos</div><div class="corpo"><div class="com-ilustra esq"><svg class="ilustra gg"><use href="#i-juiz"/></svg><p>Quando a culpabilidade, os antecedentes e a conduta social <span class="chave-v">indicarem</span>.</p></div></div></div>
 </div>
 <div class="coluna"><div class="coluna-cab">Destaques</div>
  <div class="tag-caixa"><span class="tag">Importante</span><p>Atos normativos secundários <span class="chave-v">não</span> são objeto de controle.</p></div>
  <div class="tag-caixa dica"><span class="tag dica">Dica</span><div class="relacao"><div class="de">Norma superior</div><div class="seta">➜</div><div class="para">Fundante</div></div></div>
  <div class="caixa pegadinha"><div class="rotulo">Pegadinha</div><div class="corpo">Banca troca <mark class="troca">reclusão</mark> por detenção.</div></div>
  <div class="sigla"><div class="letra"><b>L</b><span>Livre</span></div><div class="letra"><b>I</b><span>Informada</span></div><div class="letra"><b>I</b><span>Inequívoca</span></div></div>
 </div>
</div>
"""


def simbolos_por_grupo(svg: str):
    """[(grupo, [ids])] na ordem do arquivo; grupo = texto do último comentário de seção."""
    corpo = svg[svg.index("<svg"):]
    grupos, atual = [], None
    for m in re.finditer(r'<!--(.*?)-->|<symbol\s[^>]*\bid="([^"]+)"', corpo, re.S):
        if m.group(1) is not None:
            nome = re.split(r"[:(.]", m.group(1).strip())[0].strip()
            if nome and not nome.lower().startswith("selo"):
                atual = nome
            continue
        if not grupos or grupos[-1][0] != atual:
            grupos.append((atual or "Outros", []))
        grupos[-1][1].append(m.group(2))
    return grupos


def gerar_fonte() -> tuple[str, int]:
    grupos = simbolos_por_grupo(SPRITE.read_text(encoding="utf-8"))
    total = sum(len(ids) for _, ids in grupos)
    partes = [CABECA % {"col": COLUNAS}]
    partes.append('<div class="folha">' + TOPO.format(titulo="Galeria de ilustrações", n=1))
    for grupo, ids in grupos:
        partes.append(f'<div class="gal-grupo">{html.escape(grupo)} · {len(ids)}</div><div class="gal">')
        partes += [f'<div><svg><use href="#{i}"/></svg>{i}</div>' for i in ids]
        partes.append("</div>")
    partes.append(RODAPE.format(n=total) + "</div>\n")
    partes.append('<div class="folha">' + TOPO.format(titulo="Galeria de componentes", n=2))
    partes.append(COMPONENTES + RODAPE.format(n=total) + "</div>\n</body></html>\n")
    return "".join(partes), total


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    exemplos = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "exemplos"
    docs = Path(sys.argv[2]) if len(sys.argv) > 2 else REPO / "docs"
    fonte, total = gerar_fonte()
    (exemplos / "galeria-fonte.html").write_text(fonte, encoding="utf-8", newline="\n")
    print(f"ok: galeria-fonte.html com {total} ilustrações")
    py = sys.executable
    subprocess.run([py, str(AQUI / "montar.py"), str(exemplos / "galeria-fonte.html"),
                    str(exemplos / "galeria.html")], check=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([py, str(AQUI / "renderizar.py"), str(exemplos / "galeria.html"), tmp], check=True)
        docs.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(tmp) / "galeria-p1.png", docs / "galeria.png")
        shutil.copy(Path(tmp) / "galeria-p2.png", docs / "galeria-componentes.png")
    print(f"ok: {docs / 'galeria.png'} e {docs / 'galeria-componentes.png'}")


if __name__ == "__main__":
    main()
