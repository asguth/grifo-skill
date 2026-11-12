# Design — gramática visual "Grifo"

Referência estética: apostilas esquematizadas impressas em espiral — A4, duas
colunas, faixas coloridas, corpo cinza-claro, ✔ nos marcadores, vermelho negrito
nos termos-chave e figuras que mostram a estrutura do assunto. O objetivo é que o
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
- Contraste mínimo 4,5:1 em todo texto (no repositório: `ferramentas/verificar_contraste.py`).

### 1.1 Estilos de cor (`data-tema` no `<html>`; flag `--estilo`)

| Estilo | Para quem | O que muda |
|---|---|---|
| `sobrio` (padrão) | quem prefere página calma, foco no texto | navy em toda a estrutura; cor só semântica |
| `colorido` | quem memoriza por cor | cada coluna e cada bloco ganha um matiz (rotação automática); faixa cheia no matiz |
| `pastel` | quer cor sem cansar a vista | mesmos matizes em faixas claras, texto no matiz, corpo levemente tingido |
| `pb` | vai imprimir em preto e branco | tudo em cinza, inclusive ilustrações |

- Matizes de tópico (`--m1`…`--m6`): azul `#1F5F99`, petróleo `#0B6767`, roxo `#5B3A9B`,
  vinho `#9A2C68`, índigo `#34459A`, grafite `#3E4A59`. **Nenhum é vermelho, verde ou
  âmbar**: essas três continuam reservadas ao significado, em qualquer estilo.
- Mesmo assunto, mesma cor: com `class="cor-3"` (1–6) num `.bloco`, `.coluna`, `.folha` ou
  `.caixa` o tópico fica sempre com aquele matiz (ex.: "Cardiologia" roxo nas 4 folhas).
  Vale em qualquer estilo e vence a rotação. Use para dar identidade a tópicos que voltam.
- No `colorido`, 1 bloco = 1 cor; não misture duas cores de tópico no mesmo bloco.
- Os pares de contraste de todos os matizes estão no `ferramentas/verificar_contraste.py`.

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
| Conceito puro | `.bloco` com texto curto + `.chave-v` no termo + ícone lateral (`.com-ilustra`) |
| Estrutura física (órgão, célula, molécula, circuito) | `.figura` de acervo aberto ou gerador (`ilustracoes.md`) |

Diagrama abstrato que nenhum componente resolve (ciclo, Venn, organograma largo):
SVG inline usando as classes utilitárias `f-disc`, `f-claro`, `s-disc`, `t-disc`,
`t-corpo` do `grifo.css`. Mapa e estrutura física: `.figura` (§4).

## 4. Ícones, mascote e figuras

Não existe biblioteca de ilustrações prontas: desenho genérico ao lado do texto não
ensina e, feito por IA, sai com cara de clip-art. São três coisas, cada uma no seu papel:

1. **Ícone Lucide** (2.052 ícones de traço, ISC) para ancorar a memória ao lado de um bloco:
   `<svg class="ico"><use href="#l-NOME"/></svg>`. Ache o nome com
   `grep -i termo assets/lucide/nomes.txt` (formato `nome: tags`). Grande, ao lado de bloco:
   `class="ilustra g ico"` dentro de `.com-ilustra`. Cor: herda o texto; `.ico.vermelho` /
   `.verde` / `.laranja` só quando o ícone carrega significado. Use 0–3 por folha e só
   quando o ícone **diz algo** do bloco (balança ao lado de princípios; cadeado ao lado de
   segurança). Sem relação = remover.
2. **Mascote Grifo**: `i-grifo` (cabeçalho, abertura), `i-grifo-dica` (selo ★: macete) e
   `i-grifo-alerta` (selo !: pegadinha), em `assets/ilustracoes.svg`. É um WebP em
   `assets/mascote/grifo.webp` que o `montar.py` embute. Não recolorir, distorcer nem
   redesenhar.
3. **Figura didática** (anatomia, célula, molécula, circuito, gráfico, mapa): vem de
   **acervo aberto** ou de **gerador a partir de dados**, nunca desenhada à mão pela IA.
   Método, licenças, crédito e HTML em `references/ilustracoes.md`.

Tamanhos do ícone: `.ilustra.p` 12mm (ao lado de título), `.ilustra` 18mm, `.ilustra.g`
26mm (ao lado de bloco), `.ilustra.gg` 36mm.

Diagrama abstrato que nenhum componente resolve (ciclo, Venn, organograma largo) pode ser
SVG inline simples com as classes utilitárias do `grifo.css`; estrutura física, nunca.

### Paleta do sprite
O `ferramentas/verificar_ilustracoes.py` (repositório) só aceita no `ilustracoes.svg` as
cores do mascote e dos selos: contorno `#1C2430`, amarelo `#FFE45C`, vermelho `#B42318`,
branco. Toda classe usada dentro de um `<symbol>` precisa estar no `<style>` do próprio
sprite, sem seletor de ancestral (`svg .x{}` não atravessa a shadow tree do `<use>`).

## 5. Checklist visual (o crítico de design usa este)
1. Folha não estoura A4; colunas equilibradas.
2. Toda folha tem `.topo` com nº correto.
3. Hierarquia lê em 3 níveis: faixa → subtítulo → corpo. Nada compete com a faixa.
4. Cores semânticas usadas pelo significado certo; folha predominantemente neutra.
5. ≥ 1 diagrama/tabela por coluna; nenhum bloco de texto > 6 linhas sem destaque.
6. Marca-texto com parcimônia (se metade da frase está grifada, nada está).
7. Ícones relevantes e alinhados, sem cortar texto. Assunto com estrutura física tem figura
   de acervo aberto ou gerada, com crédito (checklist em `ilustracoes.md` §5).
11. Estilo pedido aplicado (`data-tema`); no colorido/pastel, tópico que se repete
   mantém a mesma cor (`cor-N`).
8. Contraste suficiente; legível impresso em P&B (ícone + rótulo em todo bloco semântico).
9. Alinhamentos e espaçamentos consistentes; nada colado na borda.
10. Fonte ≥ 8pt em tudo.
