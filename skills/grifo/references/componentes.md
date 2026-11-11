# Catálogo de componentes (copiar e adaptar)

Todas as classes vêm de `assets/grifo.css`. Não inventar classes novas;
ajustes pontuais via `style=""`.

## Folha e cabeçalho corrido
```html
<div class="folha">
  <div class="topo">
    <div class="logo"><svg viewBox="0 0 64 64"><use href="#i-grifo"/></svg></div>
    <div class="titulo-topo">Direito Constitucional<small>Controle de constitucionalidade</small></div>
    <div class="pag">01</div>
  </div>
  <div class="titulo-topico">Controle de constitucionalidade</div> <!-- só na 1ª folha -->
  <div class="apostila-colunas">
    <div class="coluna"> <div class="coluna-cab">Noções gerais</div> … blocos … </div>
    <div class="coluna"> <div class="coluna-cab">Espécies</div> … blocos … </div>
  </div>
  <div class="rodape-folha"><span>Grifo-Skill · MIT</span><span>Atualizado até 11/11/2026</span></div>
</div>
```
Cabeçalho alternativo de 1ª folha (estilo resumo único):
```html
<div class="cabecalho">
  <span class="disciplina">LGPD</span>
  <div><h1>Bases legais</h1><div class="fonte">Lei 13.709/2018, arts. 7º a 11</div></div>
  <div class="meta"><span class="incidencia" data-n="3"></span></div>
</div>
```

## Bloco (faixa + corpo cinza)
```html
<div class="bloco">            <!-- faixa secundária (salmão/laranja) -->
  <div class="faixa">Requisitos para substituição</div>
  <div class="corpo">
    <div class="sub">Objetivos</div>
    <p>Pena <span class="chave-v">não superior a 4 anos</span>, crime sem violência…</p>
  </div>
</div>
<div class="bloco primaria"> … </div>  <!-- faixa na cor primária -->
<div class="bloco escura"> … </div>    <!-- faixa cinza-escura -->
<div class="bloco contorno"> … </div>  <!-- corpo branco com borda -->
<div class="bloco pill"> … </div>      <!-- faixa arredondada centralizada -->
```

## Texto + ilustração
```html
<div class="com-ilustra">          <!-- ilustração à direita -->
  <ul class="check"><li>Cargo público;</li><li>Profissão;</li></ul>
  <svg class="ilustra g"><use href="#i-documento"/></svg>
</div>
<div class="com-ilustra esq">      <!-- ilustração à esquerda -->
  <svg class="ilustra gg"><use href="#i-juiz"/></svg>
  <p>Quando a culpabilidade… <span class="chave-v">indicarem</span>.</p>
</div>
```

## Listas
```html
<ul class="check"><li>…</li></ul>        <!-- ✔ em caixinha (cor da disciplina) -->
<ul class="check verde"><li>…</li></ul>  <!-- ✔ em círculo verde -->
```

## Tags IMPORTANTE / DICA / ATENÇÃO
```html
<div class="tag-caixa"><span class="tag">Importante</span>
  <p>Atos normativos secundários <span class="chave-v">não</span> são objeto de controle de constitucionalidade.</p>
</div>
<div class="tag-caixa dica"><span class="tag dica">Dica</span> … </div>
<span class="tag atencao">Atenção</span>   <!-- inline -->
<p class="atencao-txt">não confundir com…</p>  <!-- texto "ATENÇÃO:" itálico vermelho -->
```

## Caixas semânticas
```html
<div class="caixa regra"><div class="rotulo">Regra</div><div class="corpo">…</div></div>
<div class="caixa excecao"><div class="rotulo">Exceção</div><div class="corpo">…</div></div>
<div class="caixa pegadinha"><div class="rotulo">Pegadinha</div><div class="corpo">…</div></div>
<div class="caixa dica"><div class="rotulo">Macete</div><div class="corpo">…</div></div>
<div class="caixa exemplo"><div class="rotulo">Caso</div><div class="corpo">…</div></div>
<div class="caixa conceito"><div class="rotulo">Conceito</div><div class="corpo">…</div></div>
```

## Lei seca
```html
<div class="lei-seca"><span class="disp">Art. 7º, IX</span> para atender aos interesses
  <mark>legítimos</mark> do controlador ou de terceiro, <mark class="troca">exceto</mark> no caso de…</div>
```

## Chave (classificação)
```html
<div class="chave">
  <div class="raiz">Passado<small>ontem, antes</small></div>
  <div class="ramos">
    <div class="ramo"><div class="no">Perfeito<small>-ei, -ou</small></div>
      <div class="desc"><b>Ações concluídas.</b> Eu <b>comprei</b> um livro.</div></div>
    <div class="ramo"><div class="no">Imperfeito</div><div class="desc">…</div></div>
  </div>
</div>
```

## Fluxo (processo / decisão)
```html
<div class="fluxo">
  <div class="passo"><span class="t">Denúncia</span>MP oferece</div>
  <div class="passo decisao"><span class="t">Recebe?</span>juiz decide</div>
  <div class="passo fim"><span class="t">Citação</span>réu</div>
</div>
<div class="fluxo vertical"> … </div>
```

## Linha do tempo
```html
<div class="linha-tempo">
  <div class="marco"><span class="quando">1ª geração</span>Liberdade</div>
  <div class="marco"><span class="quando">2ª geração</span>Igualdade</div>
  <div class="marco"><span class="quando">3ª geração</span>Fraternidade</div>
</div>
```

## Pirâmide com legenda (SVG + lista)
```html
<div class="piramide-legenda">
  <svg viewBox="0 0 100 90">
    <polygon points="50,2 64,26 36,26" fill="#C0263A"/>
    <polygon points="36,28 64,28 76,50 24,50" fill="#E8790C"/>
    <polygon points="24,52 76,52 88,72 12,72" fill="#F2B63C"/>
    <polygon points="12,74 88,74 98,88 2,88" fill="#E8897A"/>
  </svg>
  <ol>
    <li><i style="background:#C0263A"></i>CF + tratados de DH com status de emenda</li>
    <li><i style="background:#E8790C"></i>Normas supralegais (tratados de DH)</li>
    <li><i style="background:#F2B63C"></i>Atos normativos primários</li>
    <li><i style="background:#E8897A"></i>Atos normativos secundários</li>
  </ol>
</div>
```
Pirâmide só em CSS: `.piramide > .nivel` (até 5 níveis, topo primeiro).

## Tabelas
```html
<table class="comparativo">
  <tr><th>Critério</th><th>Art. 7º (comuns)</th><th>Art. 11 (sensíveis)</th></tr>
  <tr><td class="criterio">Legítimo interesse</td><td class="sim"></td><td class="nao"></td></tr>
  <tr class="destaque"><td class="criterio">Prevenção à fraude</td><td class="nao"></td><td class="sim"></td></tr>
</table>

<table class="rotulada">
  <tr><td>Constituição rígida</td><td>Fundamento de validade das demais normas</td></tr>
</table>
```

## Relação A → B
```html
<div class="relacao"><div class="de">Norma superior</div><div class="seta">➜</div><div class="para">Fundante</div></div>
```

## Mnemônico
```html
<div class="sigla">
  <div class="letra"><b>L</b><span>Livre</span></div>
  <div class="letra"><b>I</b><span>Informada</span></div>
  <div class="letra"><b>I</b><span>Inequívoca</span></div>
</div>
```

## Chips, selos, destaques inline
```html
<span class="chip">-va / -ia</span> <span class="chip cheio">LGPD</span>
<span class="chip sim">pode</span> <span class="chip nao">não pode</span>
<span class="selo cai-muito">Cai muito</span> <span class="selo novidade">Lei 14.xxx/2024</span>
<span class="selo decore">Decore</span>
<span class="chave-v">termo</span> <mark>chave</mark> <mark class="troca">troca</mark>
<span class="verificar">dado não conferido</span>
```

## Questões e gabarito
```html
<div class="questao">
  <div class="cab"><span class="n">01</span><span class="estilo">C/E</span>estilo Cebraspe · inédita</div>
  <p>O tratamento de dado sensível pode fundamentar-se no legítimo interesse do controlador.</p>
  <div class="ce"><span>C</span><span>E</span></div>
</div>
<div class="questao">
  <div class="cab"><span class="n">02</span><span class="estilo">A–E</span>estilo FGV · inédita</div>
  <p>Enunciado com caso…</p>
  <ol class="alternativas"><li>…</li><li>…</li><li>…</li><li>…</li><li>…</li></ol>
</div>
<div class="gabarito"><h4>Gabarito comentado</h4>
  <div class="item"><b>01 — Errado.</b> O art. 11 não prevê legítimo interesse…</div>
</div>
```

## Flashcards (frente | verso na mesma linha; dobrar ao meio)
```html
<p class="flashcards-instrucao">✂ Recorte nas linhas tracejadas e dobre ao meio.</p>
<div class="flashcards">
  <div class="card frente"><span class="lado">frente</span>Quantas bases legais tem o art. 7º?</div>
  <div class="card verso"><span class="lado">verso</span>10 (incisos I a X)</div>
</div>
```

## Edital verticalizado
```html
<table class="edital">
  <tr><th></th><th>Conteúdo</th><th>Peso</th><th>Prioridade</th></tr>
  <tr class="materia"><td colspan="4">Língua Portuguesa — 15 questões</td></tr>
  <tr><td class="check"></td><td>1. Compreensão e interpretação de textos.</td><td class="peso">1,0</td><td>★★★</td></tr>
</table>
```

## Capa e sumário
```html
<div class="folha capa">
  <div class="titulo-capa">Direito Constitucional</div>
  <div class="sub-capa">Apostila visual — Concurso X · Cargo Y</div>
  <svg class="ilustra gg" style="margin-top:20mm"><use href="#i-constituicao"/></svg>
  <div class="info-capa">Gerada com Grifo-Skill (MIT) · atualizado até dd/mm/aaaa</div>
</div>
<div class="folha sumario"><h2 class="secao">Sumário</h2>
  <ol><li>Teoria da Constituição<span class="pg">03</span></li></ol></div>
```
