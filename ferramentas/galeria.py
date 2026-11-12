#!/usr/bin/env python3
"""Gera a galeria (mascote, amostra de ícones Lucide e componentes) do Grifo-Skill.

Uso:  python3 galeria.py [pasta_exemplos] [pasta_docs]
      (padrão: <repo>/exemplos e <repo>/docs)

1. Lê os <symbol> de assets/ilustracoes.svg (o mascote), junta uma amostra de
   ícones Lucide por área e escreve exemplos/galeria-fonte.html —
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

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "grifo"
AQUI = SKILL / "scripts"
SPRITE = SKILL / "assets" / "ilustracoes.svg"
COLUNAS = 10
# amostra de ícones Lucide por área (não há biblioteca de ilustrações prontas)
LUCIDE = [
    ("Direito e Estado", "scale gavel landmark scroll-text file-text stamp shield-check lock users user-round"),
    ("Saúde e biologia", "heart-pulse stethoscope brain microscope dna pill syringe bone activity sprout"),
    ("Exatas e TI", "calculator sigma chart-line chart-column flask-conical atom cpu database code network"),
    ("Estudo e sinais", "book-open lightbulb target clock calendar-days triangle-exclamation-point ban circle-check search messages-square"),
]

CABECA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Galeria Grifo</title>
<!-- GERADO POR scripts/galeria.py — não editar à mão -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Poppins:wght@600;700;800;900&display=swap" rel="stylesheet">
<!--APOSTILA:CSS-->
<style>
.gal-grupos{display:flex;flex-wrap:wrap;gap:0 4mm}
.gal-bloco{flex:0 0 calc(var(--n) * (100%% - 4mm) / %(col)d)}
.gal-bloco.cheio{flex-basis:100%%}
.gal-bloco .gal{grid-template-columns:repeat(var(--n),minmax(0,1fr))}
.gal-grupo{font-family:var(--fonte-titulo);font-weight:800;font-size:8.5pt;text-transform:uppercase;color:var(--disc);border-bottom:1.5px solid var(--disc-claro);margin-top:1.5mm}
.gal{display:grid;grid-template-columns:repeat(%(col)d,minmax(0,1fr));gap:1.2mm 1mm}
.gal div{text-align:center;font-size:8pt;color:var(--tinta-2);hyphens:manual;overflow-wrap:normal;line-height:1.1}
.gal svg{width:12.5mm;height:12.5mm;display:block;margin:0 auto .5mm}
.gal svg.ico{width:10mm;height:10mm;margin:1.2mm auto 1mm;color:var(--navy)}
.gal-nota{font-size:8.6pt;color:var(--tinta-2);margin-top:3mm}
</style>
</head><body><!--APOSTILA:SPRITE-->
"""

TOPO = ('<div class="topo"><div class="logo"><svg viewBox="0 0 64 64"><use href="#i-grifo"/></svg></div>'
        '<div class="titulo-topo">{titulo}<small>design system grifo</small></div><div class="pag">{n:02d}</div></div>')

RODAPE = ('<div class="rodape-folha"><span>Grifo-Skill</span>'
          '<span>ferramentas/galeria.py · mascote + {n} ícones Lucide de amostra (2.052 no total)</span></div>')

# Folha 2: amostra de componentes (atualize quando criar componente novo).
COMPONENTES = """
<div class="apostila-colunas">
 <div class="coluna"><div class="coluna-cab">Blocos e listas</div>
  <div class="bloco"><div class="faixa">Penas restritivas de direito</div><div class="corpo">
   <div class="sub">Interdição temporária de direitos</div>
   <div class="com-ilustra"><ul class="check"><li>Cargo público;</li><li>Profissão;</li><li>Habilitação;</li><li>Concurso público.</li></ul><svg class="ilustra g ico"><use href="#l-file-text"/></svg></div>
  </div></div>
  <div class="bloco primaria"><div class="faixa">Requisitos subjetivos</div><div class="corpo"><div class="com-ilustra esq"><svg class="ilustra gg ico"><use href="#l-gavel"/></svg><p>Quando a culpabilidade, os antecedentes e a conduta social <span class="chave-v">indicarem</span>.</p></div></div></div>
  <div class="bloco escura"><div class="faixa">Fórmula · probabilidade</div><div class="corpo">
   <div class="formula"><span class="rot">Probabilidade clássica</span><i>P</i>(<i>A</i>) = <span class="frac"><span>casos favoráveis</span><span>casos possíveis</span></span></div>
  </div></div>
  <div class="bloco"><div class="faixa">Tabela-verdade · conjunção</div><div class="corpo">
   <table class="verdade"><tr><th>p</th><th>q</th><th class="res">p ∧ q</th></tr>
   <tr><td class="v">V</td><td class="v">V</td><td class="v res">V</td></tr>
   <tr><td class="v">V</td><td class="f">F</td><td class="f res">F</td></tr>
   <tr><td class="f">F</td><td class="v">V</td><td class="f res">F</td></tr>
   <tr><td class="f">F</td><td class="f">F</td><td class="f res">F</td></tr></table>
  </div></div>
 </div>
 <div class="coluna"><div class="coluna-cab">Destaques</div>
  <div class="tag-caixa"><span class="tag">Importante</span><p>Atos normativos secundários <span class="chave-v">não</span> são objeto de controle.</p></div>
  <div class="tag-caixa dica"><span class="tag dica">Dica</span><div class="relacao"><div class="de">Norma superior</div><div class="seta">➜</div><div class="para">Fundante</div></div></div>
  <div class="caixa pegadinha"><div class="rotulo">Pegadinha</div><div class="corpo">Banca troca <mark class="troca">reclusão</mark> por detenção.</div></div>
  <div class="bloco"><div class="faixa">Ícones Lucide · ISC · 2.052 nomes</div><div class="corpo">
   <p style="display:flex;flex-wrap:wrap;gap:3mm;align-items:center"><svg class="ico"><use href="#l-scale"/></svg><svg class="ico"><use href="#l-gavel"/></svg><svg class="ico"><use href="#l-brain"/></svg><svg class="ico"><use href="#l-book-open"/></svg><svg class="ico"><use href="#l-calculator"/></svg><svg class="ico"><use href="#l-database"/></svg><svg class="ico"><use href="#l-flask-conical"/></svg><svg class="ico"><use href="#l-globe"/></svg><svg class="ico vermelho"><use href="#l-octagon-x"/></svg><svg class="ico verde"><use href="#l-circle-check"/></svg><svg class="ico laranja"><use href="#l-triangle-exclamation-point"/></svg></p>
   <p class="pequeno"><code>&lt;svg class="ico"&gt;&lt;use href="#l-scale"/&gt;&lt;/svg&gt;</code> · nomes em <code>assets/lucide/nomes.txt</code></p>
  </div></div>
  <div class="sigla"><div class="letra"><b>L</b><span>Livre</span></div><div class="letra"><b>I</b><span>Informada</span></div><div class="letra"><b>I</b><span>Inequívoca</span></div></div>
  <div class="bloco contorno"><div class="faixa">Código · SQL</div><div class="corpo">
   <pre class="codigo"><span class="rot">SQL</span><b>SELECT</b> nome, cargo
  <b>FROM</b> servidor
 <b>WHERE</b> lotacao = 'SEDE'
 <b>ORDER BY</b> nome;</pre>
  </div></div>
  <div class="bloco primaria"><div class="faixa">Análise sintática</div><div class="corpo">
   <p class="exemplo-frase"><span class="termo" data-funcao="sujeito">Os candidatos</span> <span class="termo" data-funcao="verbo">estudaram</span> <span class="termo destaque" data-funcao="objeto direto">a lei seca</span>.</p>
  </div></div>
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
    grupos = [(g, [f"#{i}" for i in ids]) for g, ids in grupos]
    grupos += [(g, [f"#l-{n}" for n in nomes.split()]) for g, nomes in LUCIDE]
    total = sum(len(nomes.split()) for _, nomes in LUCIDE)
    partes = [CABECA % {"col": COLUNAS}]
    partes.append('<div class="folha">' + TOPO.format(titulo="Mascote e ícones", n=1))
    # grupos pequenos dividem a mesma linha; grupos com >= COLUNAS/2 itens ocupam a largura toda
    partes.append('<div class="gal-grupos">')
    for grupo, ids in grupos:
        cheio = len(ids) * 2 >= COLUNAS
        n = COLUNAS if cheio else len(ids)
        partes.append(f'<div class="gal-bloco{" cheio" if cheio else ""}" style="--n:{n}">'
                      f'<div class="gal-grupo">{html.escape(grupo)} · {len(ids)}</div><div class="gal">')
        for i in ids:
            cls = ' class="ico"' if i.startswith("#l-") else ""
            partes.append(f'<div><svg{cls}><use href="{i}"/></svg>{i[3:]}</div>')
        partes.append("</div></div>")
    partes.append("</div>")
    partes.append('<p class="gal-nota"><b>Figuras didáticas</b> (anatomia, célula, molécula, circuito) não vêm daqui: '
                  'vêm de acervo aberto com crédito ou de gerador a partir de dados. '
                  'Ver <code>references/ilustracoes.md</code> e <code>scripts/figura.py</code>.</p>')
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
    print(f"ok: galeria-fonte.html com mascote e {total} ícones")
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
