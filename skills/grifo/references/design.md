# Design — gramática visual "Grifo"

Referência estética: apostilas esquematizadas impressas em espiral — A4, duas
colunas, faixas coloridas, corpo cinza-claro, ✔ nos marcadores, vermelho negrito
nos termos-chave e personagens ilustrados ao lado do texto. O objetivo é que o
aluno **entenda olhando** e **ache a informação em 3 segundos** na revisão.

## 1. Cores

### Cor da disciplina (no `<body>`)
| Classe | Disciplina | Primária | Secundária (faixas) |
|---|---|---|---|
| `d-portugues` | Língua Portuguesa | azul | laranja |
| `d-constitucional` | Dir. Constitucional | vermelho-vinho | azul |
| `d-administrativo` | Dir. Administrativo | magenta | coral |
| `d-penal` | Dir. Penal / Proc. Penal | roxo-acinzentado | salmão |
| `d-civil` | Dir. Civil / Proc. Civil | marrom | petróleo |
| `d-dados` | LGPD, privacidade, proteção de dados | roxo | laranja |
| `d-ti` | TI, sistemas, segurança da informação | verde-petróleo | coral |
| `d-logica` | Raciocínio lógico, matemática, estatística | laranja | azul |
| `d-gestao` | Administração, gestão, negócios | verde | âmbar |
| `d-contabil` | Contabilidade, AFO, economia | azul-aço | salmão |
| `d-atualidades` | Atualidades, legislação específica, outras | cinza-azulado | salmão |

Primária (`--disc`): faixas `.bloco.primaria`, subtítulos `.sub`, diagramas.
Secundária (`--disc-2`): faixas padrão `.bloco`, nº da página.

### Cores semânticas (iguais em todas as disciplinas)
| Função | Cor | Ícone | Componente |
|---|---|---|---|
| Regra / conceito | da disciplina | ◆ | `.caixa.regra`, `.caixa.conceito` |
| Exceção / atenção | laranja | ⚠ | `.caixa.excecao`, `.tag.atencao` |
| Pegadinha / proibido / importante | vermelho | ✘ ! | `.caixa.pegadinha`, `.tag` |
| Dica / macete / correto | verde (caixa) ou laranja (tag DICA) | ✔ ★ | `.caixa.dica`, `.tag.dica` |
| Lei seca | cinza | § | `.lei-seca`, `.caixa.lei` |
| Exemplo / caso | azul | ▶ | `.caixa.exemplo` |

### Marca-texto
- `<mark>` amarelo = palavra-chave para decorar. Máx. ~1 por frase.
- `<mark class="troca">` rosa = palavra que a banca costuma trocar.
- `.chave-v` = vermelho escuro negrito (estilo das apostilas) para o termo-chave do
  parágrafo. Usar no lugar de `mark` em texto corrido dentro de `.bloco`.

## 2. Tipografia e layout
- Títulos: Poppins 800 caixa alta. Corpo: Inter 9–10.5pt. Nunca abaixo de 8pt.
- Layout padrão de folha:
  ```
  .topo (logo · DISCIPLINA / tópico · nº)
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
| Conceito puro | `.bloco` com texto curto + `.chave-v` no termo + ilustração lateral (`.com-ilustra`) |

Diagrama que nenhum componente resolve (ciclo, mapa, Venn, organograma largo):
SVG inline usando as classes utilitárias `f-disc`, `f-claro`, `s-disc`, `t-disc`,
`t-corpo` do `apostila.css` e contorno `#1C2430` 2.5px.

## 4. Ilustrações

### Biblioteca (`assets/ilustracoes.svg`, viewBox 64×64)
- **Personagens:** `i-juiz` (na bancada), `i-autor` (doutrinador), `i-servidora`,
  `i-estudante`, `i-pessoa` (titular/cidadão), `i-grupo` (coletividade).
- **Mascote:** `i-grifo` (dica, abertura), `i-grifo-alerta` (pegadinha).
- **Apontadores:** `i-mao-direita`, `i-mao-esquerda` (estilo apostila de gramática).
- **Direito/Estado:** `i-balanca`, `i-martelo`, `i-documento` (§), `i-constituicao`,
  `i-predio-publico`, `i-congresso`.
- **Dados/TI:** `i-cadeado`, `i-escudo-dados`, `i-banco-dados`, `i-computador`,
  `i-nuvem`, `i-engrenagem`.
- **Estudo:** `i-livro`, `i-cerebro`, `i-lampada`, `i-alvo`, `i-relogio`, `i-calendario`.
- **Sinais:** `i-alerta`, `i-proibido`, `i-check`, `i-lupa`, `i-megafone`, `i-dinheiro`.

Tamanhos: `.ilustra.p` 12mm (ao lado de título), `.ilustra` 18mm, `.ilustra.g` 26mm
(ao lado de bloco), `.ilustra.gg` 36mm (destaque de folha). Use 2–5 ilustrações
por folha: o suficiente para ancorar a memória, não a ponto de virar enfeite.
Cada ilustração tem que **dizer algo** sobre o bloco (juiz ao lado de requisitos
judiciais; cadeado ao lado de segurança). Ilustração sem relação = remover.

### Desenhar uma ilustração nova (quando a biblioteca não tem)
Regras do estilo, obrigatórias:
- viewBox `0 0 64 64`, formas simples (≤ 15 elementos), sem gradientes, sem sombras.
- Contorno `stroke:#1C2430; stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round`.
- Preenchimentos: `var(--disc)`, `var(--disc-claro)`, `var(--disc-2)`, branco,
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
| Contorno e tinta | `#1C2430` |
| Tema (via classe) | `var(--disc)`, `var(--disc-claro)`, `var(--disc-2)` (`.f-disc`, `.f-claro`, `.f-disc2`, `.t-disc`) |
| Neutros | `#FFFFFF`/`#fff`, `#E3E7EC`, `#5A6070`, `#3A3F48`, `#23262C` |
| Pele e cabelo | `#F6C9A0`, `#6B4A32`, `#2F2A26` |
| Madeira (bancada) | `#7A4A2A`, `#9A6236` |
| Marca-texto | `#FFE45C` |
| Semânticas | vermelho `#D6283A`, verde `#16884A`, laranja `#E8790C`, azul `#1F6FD1` |
| Símbolos nacionais | verde `#2E7D4F`, azul `#1F4FA0`, roupa `#3D4F6E` |
| Mascote Grifo | `#E8853A`, `#FFF1DC`, `#C8F27A`, `#6A4C93`, `#F28B82` |

## 5. Checklist visual (o crítico de design usa este)
1. Folha não estoura A4; colunas equilibradas.
2. Toda folha tem `.topo` com nº correto.
3. Hierarquia lê em 3 níveis: faixa → subtítulo → corpo. Nada compete com a faixa.
4. Cores semânticas usadas pelo significado certo (vermelho só para pegadinha/importante).
5. ≥ 1 diagrama/tabela por coluna; nenhum bloco de texto > 6 linhas sem destaque.
6. Marca-texto com parcimônia (se metade da frase está grifada, nada está).
7. Ilustrações relevantes, tamanho consistente, alinhadas, sem cortar texto.
8. Contraste suficiente; legível impresso em P&B (ícone + rótulo em todo bloco semântico).
9. Alinhamentos e espaçamentos consistentes; nada colado na borda.
10. Fonte ≥ 8pt em tudo.
