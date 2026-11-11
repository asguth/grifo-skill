# Design — gramática visual "Grifo"

Referência estética: apostilas esquematizadas impressas em espiral — A4, duas
colunas, faixas coloridas, corpo cinza-claro, ✔ nos marcadores, vermelho negrito
nos termos-chave e personagens ilustrados ao lado do texto. O objetivo é que o
aluno **entenda olhando** e **ache a informação em 3 segundos** na revisão.

## 1. Cores (sistema editorial)

O documento é **predominantemente neutro**. Cor só quando comunica significado — se uma
cor sai sem perder hierarquia ou sentido, tire. Nada de gradiente decorativo nem de cor
"para enfeitar". Uma folha sem exceções não precisa de âmbar; sem proibições, não precisa
de vermelho.

| Cor | Hex | Uso | Componentes |
|---|---|---|---|
| **Navy** | `#243B53` | títulos, cabeçalhos de seção e de tabela, estrutura | `.coluna-cab`, `.bloco.primaria`, `th`, `.chave`, `.fluxo` |
| **Blue** | `#2F6B8A` | apoio, relação entre conceitos, termo-chave | `.chave-v`, `.caixa.exemplo`, links |
| **Amber** | `#A85D00` | exceções, condições importantes, pontos que confundem, prazos de atenção | `.caixa.excecao`, `.tag` IMPORTANTE, `.atencao-txt` |
| **Red** | `#B42318` | proibições, interpretações erradas, pegadinhas, riscos | `.caixa.pegadinha`, `tr.destaque`, `td.nao` |
| **Green** | `#237A57` | permitido, procedimento válido, alternativa correta | `.caixa.dica`, `.tag.dica`, `td.sim` |
| **Slate** | `#596579` | referências, notas, metadados | `.caixa.lei`, `.pequeno`, rodapé |
| Neutros | `#202A35` tinta · `#F4F6F8` superfície · `#E7EDF2` superfície 2 | fundo de blocos, faixas comuns | `.bloco > .corpo`, `.faixa` |

- Faixa de seção comum: **tipografia navy sobre fundo neutro**; barra sólida navy só em
  `.bloco.primaria` (com parcimônia: 1–2 por coluna).
- Um componente = no máximo uma cor semântica. Nunca pintar um parágrafo inteiro para
  destacar uma frase.
- Caixas de aviso/erro/sucesso: fundo pálido + texto e ícone da cor semântica.
- Contraste mínimo 4,5:1 em todo texto (`scripts/verificar_contraste.py`).

### Marca-texto
- `<mark>` amarelo = palavra para decorar (é o "grifo" do nome). Máx. ~1 por frase.
- `<mark class="troca">` vermelho pálido = palavra que costuma ser trocada/confundida.
- `.chave-v` = termo-chave em azul negrito (em vez de `mark` dentro de `.bloco`).

## 2. Tipografia e layout
- Títulos: Poppins 800 caixa alta. Corpo: Inter 9–10.5pt. Nunca abaixo de 8pt.
- Layout padrão de folha:
  ```
  .topo (logo + versão · MATÉRIA / tópico · nº)
  .titulo-topico (só na 1ª folha do assunto, opcional)
  .apostila-colunas → 2 × .coluna → .coluna-cab + .bloco …
  ```
- Uma folha = uma `.folha`. Conteúdo que não cabe vai para nova `.folha`
  (o `renderizar.py` acusa estouro). Não reduzir fonte para caber.
- Equilibrar colunas: a diferença de altura entre as duas colunas deve ser < 25%.
- Respiro: nenhum bloco colado na borda; gap entre blocos ≥ 2.5mm.
- Cada coluna tem pelo menos 1 elemento visual (diagrama, tabela, ilustração).

## 3. Qual componente usar (forma do conteúdo → componente)
| O conteúdo é… | Use |
|---|---|
| Classificação / espécies / tipos | `.chave` (raiz → ramos) |
| Processo, procedimento, rito, fluxo de decisão | `.fluxo` (horizontal) ou `.fluxo.vertical`; decisão = `.passo.decisao` |
| Prazos / evolução histórica / gerações de direitos | `.linha-tempo` |
| Hierarquia (normas, órgãos, níveis) | `.piramide-legenda` (SVG) ou `.piramide` |
| A vs B (vs C) | `table.comparativo` |
| Termo ↔ definição curta, 2–5 pares | `table.rotulada` |
| Relação de dependência/causa (norma superior → fundante) | `.relacao` |
| Lista de requisitos/hipóteses | `ul.check` dentro de `.bloco` |
| Lista para decorar com ≥ 3 itens | `.sigla` (mnemônico) |
| Regra + exceções | `.caixa.regra` seguida de `.caixa.excecao` |
| Ponto que mais cai / alerta | `.tag-caixa` com `.tag` IMPORTANTE |
| Macete | `.tag-caixa.dica` |
| Artigo literal | `.lei-seca` |
| Caso prático | `.caixa.exemplo` |
| Fórmula (RLM, estatística, financeira) | `.formula` (com `.frac` para frações) |
| Lógica proposicional: valores de conectivos | `table.verdade` |
| SQL, pseudocódigo, comando de terminal | `pre.codigo` |
| Frase analisada (sintaxe, crase, regência, concordância) | `.exemplo-frase` com `.termo[data-funcao]` |
| Conceito puro | `.bloco` com texto curto + `.chave-v` no termo + ilustração lateral (`.com-ilustra`) |

Diagrama que nenhum componente resolve (ciclo, mapa, Venn, organograma largo):
SVG inline usando as classes utilitárias `f-disc`, `f-claro`, `s-disc`, `t-disc`,
`t-corpo` do `grifo.css` e contorno `#1C2430` 2.5px.

## 4. Ilustrações e ícones

Ordem de preferência (do mais barato em tokens ao mais caro):
1. **Ícone Lucide** (2.052 ícones de traço, ISC): `<svg class="ico"><use href="#l-NOME"/></svg>`.
   Ache o nome com `grep -i termo assets/lucide/nomes.txt` (formato `nome: tags`). Grande,
   ao lado de bloco: `class="ilustra g ico"`. Cor: herda o texto; `.ico.vermelho` /
   `.verde` / `.laranja` só quando o ícone carrega significado.
2. **Ilustração da biblioteca** (flat, colorida): `<svg class="ilustra g"><use href="#i-NOME"/></svg>`.
3. **SVG novo inline** — só se nada acima servir.

As **ilustrações têm paleta própria, mais viva** (azul `#3D7CC9`, coral `#F2875F`,
azul-claro `#DCEAF7`, amarelo `#FFE45C`, pele, madeira), via `.f-disc`, `.f-disc2`,
`.f-claro`. Essa cor fica só nos desenhos; texto, caixas e faixas seguem a §1.

### Biblioteca (`assets/ilustracoes.svg`, viewBox 64×64)
- **Personagens:** `i-juiz` (na bancada), `i-autor` (doutrinador), `i-servidora`,
  `i-estudante`, `i-pessoa` (titular/cidadão), `i-grupo` (coletividade).
- **Mascote:** `i-grifo` (neutro: cabeçalho, abertura), `i-grifo-dica` (selo ★: macete,
  dica) e `i-grifo-alerta` (selo !: pegadinha). É o único símbolo raster: um WebP em
  `assets/mascote/grifo.webp` (≤ 40 KB) que o `montar.py` embute como data URI; as poses
  reaproveitam a mesma imagem e só acrescentam o selo vetorial. viewBox 0 0 240 240.
  Não recolorir, distorcer nem redesenhar o mascote.
- **Apontadores:** `i-mao-direita`, `i-mao-esquerda` (estilo apostila de gramática).
- **Direito/Estado:** `i-balanca`, `i-martelo`, `i-documento` (§), `i-constituicao`,
  `i-predio-publico`, `i-congresso`.
- **Dados/TI:** `i-cadeado`, `i-escudo-dados`, `i-banco-dados`, `i-computador`,
  `i-nuvem`, `i-engrenagem`.
- **Estudo:** `i-livro`, `i-cerebro`, `i-lampada`, `i-alvo`, `i-relogio`, `i-calendario`.
- **Sinais:** `i-alerta`, `i-proibido`, `i-check`, `i-lupa`, `i-megafone`, `i-dinheiro`.
- **Exatas e TI:** `i-calculadora`, `i-grafico` (barras + tendência), `i-ampulheta`,
  `i-codigo` (`</>`), `i-rede` (nós ligados).
- **Línguas, humanas e sociedade:** `i-dialogo` (balões de fala), `i-globo`, `i-mapa`,
  `i-escola`, `i-hospital` (placa "H", sem cruz vermelha — emblema protegido),
  `i-policia` (distintivo genérico, sem brasão real), `i-trofeu`.

A galeria completa (gerada por `scripts/galeria.py`) fica em `docs/galeria.png`.

Tamanhos: `.ilustra.p` 12mm (ao lado de título), `.ilustra` 18mm, `.ilustra.g` 26mm
(ao lado de bloco), `.ilustra.gg` 36mm (destaque de folha). Use 2–5 ilustrações
por folha: o suficiente para ancorar a memória, não a ponto de virar enfeite.
Cada ilustração tem que **dizer algo** sobre o bloco (juiz ao lado de requisitos
judiciais; cadeado ao lado de segurança). Ilustração sem relação = remover.

### Desenhar uma ilustração nova (quando a biblioteca não tem)
Regras do estilo, obrigatórias:
- viewBox `0 0 64 64`, formas simples (≤ 15 elementos), sem gradientes, sem sombras.
- Contorno `stroke:#1C2430; stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round`.
- Preenchimentos: classes `.f-disc` (azul), `.f-claro` (azul-claro), `.f-disc2` (coral), branco,
  pele `#F6C9A0`, amarelo `#FFE45C`; vermelho/verde/laranja só com sentido semântico.
- Personagens: cabeça circular grande (r≈10), olhos de ponto, corpo em "sino".
  **Nunca** desenhar caricatura de pessoa real; para autor real, `i-autor` + nome.
- Bandeiras, mapas e símbolos nacionais: versões simplificadas planas.
- Inserir inline na folha como `<svg class="ilustra g" viewBox="0 0 64 64">…</svg>`.
  Se ficar boa e for reutilizável, sugerir ao usuário adicioná-la à biblioteca.

### Regra do sprite (ao adicionar símbolos à biblioteca)
- Toda classe usada dentro de um `<symbol>` precisa estar declarada no `<style>`
  do **próprio** `ilustracoes.svg`, **sem seletor de ancestral**: `.f-disc{…}`
  funciona; `svg .f-disc{…}` (como no `grifo.css`) **não** atravessa a shadow tree
  criada pelo `<use>` e a ilustração sai preta.
- Nada de `<symbol>` dentro de comentário, e nada de `-->` dentro do comentário de
  cabeçalho (fecha o comentário antes da hora).
- `id` único, sempre com `viewBox`; `<use>` interno só para ids que existem.
- Rode `python3 scripts/verificar_ilustracoes.py` (falha com exit 1 se algo disso
  quebrar) e `python3 scripts/galeria.py` para ver o símbolo na galeria.

### Paleta permitida nas ilustrações
Qualquer cor fora desta lista faz o `verificar_ilustracoes.py` falhar.

| Uso | Cores |
|---|---|
| Contorno e tinta | `#1C2430`, `#202A35` |
| Ilustração (via classe) | `#3D7CC9` azul · `#F2875F` coral · `#DCEAF7` azul-claro |
| Layout | `#243B53`, `#2F6B8A`, neutros `#FFFFFF` `#F4F6F8` `#E7EDF2` `#E3E7EC` |
| Roupas/objetos | `#5A6070`, `#3A3F48`, `#23262C`, `#596579`, `#3D4F6E` |
| Pele, cabelo, madeira | `#F6C9A0`, `#6B4A32`, `#2F2A26`, `#7A4A2A`, `#9A6236` |
| Marca-texto | `#FFE45C` |
| Semânticas | âmbar `#A85D00`, vermelho `#B42318`, verde `#237A57` |
| Símbolos nacionais | `#2E7D4F`, `#1F4FA0` |

## 5. Checklist visual (o crítico de design usa este)
1. Folha não estoura A4; colunas equilibradas.
2. Toda folha tem `.topo` com nº correto.
3. Hierarquia lê em 3 níveis: faixa → subtítulo → corpo. Nada compete com a faixa.
4. Cores semânticas usadas pelo significado certo; folha predominantemente neutra.
5. ≥ 1 diagrama/tabela por coluna; nenhum bloco de texto > 6 linhas sem destaque.
6. Marca-texto com parcimônia (se metade da frase está grifada, nada está).
7. Ilustrações relevantes, tamanho consistente, alinhadas, sem cortar texto.
8. Contraste suficiente; legível impresso em P&B (ícone + rótulo em todo bloco semântico).
9. Alinhamentos e espaçamentos consistentes; nada colado na borda.
10. Fonte ≥ 8pt em tudo.
