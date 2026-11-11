---
name: grifo
description: Monta apostilas e resumos ilustrados para concursos públicos (estilo esquematizado - faixas coloridas, 2 colunas, personagens, fluxogramas, tabelas, lei seca grifada) em HTML/PDF A4, com validação de conteúdo, revisão didática e crítica de design. Use para /resumo, /esquema, /lei-seca, /comparar, /pegadinhas, /questoes, /flashcards, /mnemonico, /edital, /cronograma, /revisao, /apostila, /validar, /grifo (ajuda) ou qualquer pedido de resumo/material de estudo para concurso.
license: MIT
---

# Grifo-Skill

Gera material de estudo para concursos no padrão das apostilas esquematizadas
comerciais: **página A4, duas colunas, faixas de seção coloridas, corpo cinza-claro,
listas com ✔, termos-chave em vermelho negrito, personagens e ícones ilustrados ao
lado do texto, fluxogramas, pirâmides, tabelas comparativas e lei seca grifada.**

Todo material passa por **três revisores independentes** antes da entrega:
conteúdo (fidelidade à lei/fonte), didática (é fácil de entender e cobre o que cai)
e design (layout, legibilidade, consistência visual).

Pastas desta skill (caminhos relativos a este SKILL.md):

| Caminho | O que é | Quando ler |
|---|---|---|
| `references/comandos.md` | Especificação de cada comando | Sempre, só a seção do comando pedido |
| `references/componentes.md` | Catálogo HTML de todos os componentes | Antes de escrever o HTML |
| `references/design.md` | Gramática visual, estilo das ilustrações, regras de layout | Antes de escrever o HTML |
| `references/bancas.md` | Perfis de banca (Cebraspe, FGV, FCC, Vunesp, Cesgranrio…) | Quando houver questões/pegadinhas |
| `references/fidelidade.md` | Regras de fonte e citação | Antes de pesquisar/escrever |
| `agentes/*.md` | Prompts dos 3 revisores | Etapa de validação |
| `assets/grifo.css` | Design system (não editar por apostila) | Injetado pelo `montar.py` |
| `assets/ilustracoes.svg` | Biblioteca de ilustrações (ids `i-*`) | Consultar ids disponíveis |
| `scripts/montar.py` | Injeta CSS + ilustrações usadas → HTML autocontido | Sempre |
| `scripts/renderizar.py` | HTML → PDF A4 + PNG por folha + relatório de layout (`--json`, `--pb`) | Sempre que possível |
| `scripts/verificar.py` | Lint do HTML-fonte (classes, ilustrações, folhas, marcadores) | Antes de montar |
| `assets/templates/*.html` | Esqueleto de cada comando, com os marcadores do `montar.py` | Início do passo 4 |

## Comandos

Sintaxe única (detalhes e ajuda completa em `references/comandos.md`, seção "Sintaxe"):
```
/<comando> <tópico> [--banca b] [--cargo "x"] [--folhas N] [--material arquivo] [--disciplina d-x]
```

| Comando | Gera |
|---|---|
| `/resumo <tópico>` | Resumo ilustrado completo, 1–4 folhas A4 |
| `/esquema <tópico>` | Uma folha só de mapa visual (diagrama do tópico inteiro) |
| `/lei-seca <lei> [--artigos 1-10]` | Lei seca esquematizada: texto literal grifado + quadros laterais |
| `/comparar <A> vs <B> [vs C]` | Folha comparativa (tabela + diferenças-pegadinha) |
| `/pegadinhas <tópico>` | Folha de armadilhas típicas da banca |
| `/questoes <tópico> [--n 10]` | Questões inéditas no estilo da banca + gabarito comentado |
| `/flashcards <tópico> [--n 16]` | Cartões frente/verso para recortar |
| `/mnemonico <lista ou tópico>` | Siglas/frases de memorização com quadro visual |
| `/edital <edital>` | Edital verticalizado com checklist e peso por matéria |
| `/cronograma <matérias> --horas N --prova dd/mm/aaaa` | Plano semanal com revisões espaçadas |
| `/revisao <tópico>` | Folha única de revisão véspera (super-resumo) |
| `/apostila <disciplina> [tópicos...]` | Junta folhas: capa, sumário, resumos, questões |
| `/validar <arquivo.html>` | Roda só os 3 revisores sobre um material existente |
| `/grifo [comando]` | Ajuda: lista comandos, flags e um exemplo de cada |

**Como interpretar o pedido**
- `/resumo X`, `resumo: X` e *"faz um resumo de X pra FGV"* → **mesmo fluxo**.
  Linguagem natural vira flags: banca, cargo, nº de folhas, material anexado.
- **Sem flags = padrões.** Formas posicionais antigas (`/questoes lgpd cebraspe 20`)
  continuam valendo.
- **Flag desconhecida ou valor inválido** → avisar em uma linha e seguir com o padrão.
- **Comando inexistente** (`/resumao`, `/simulado`) → mostrar a ajuda do `/grifo`
  (bloco em `references/comandos.md`) e sugerir o comando mais próximo.
- `/grifo` ou `/grifo ajuda` → só mostrar a ajuda; não gerar arquivo.
- No Claude Code, se o nome colidir com outro plugin: `/grifo-skill:resumo`.

## Parâmetros comuns

- **banca**: `cebraspe`, `fgv`, `fcc`, `vunesp`, `cesgranrio`, `ibfc`, `quadrix`,
  ou `indefinida` (padrão). Com `indefinida`, questões saem em **dois formatos**
  (certo/errado e múltipla escolha A–E) e as pegadinhas cobrem os padrões comuns.
  Se o usuário citar "Cebraspe ou FGV", usar `indefinida` priorizando essas duas.
- **cargo / órgão**: ajusta profundidade e exemplos (ex.: ANPD → foco regulatório).
- **material**: PDF, apostila, anotações, prints. Se fornecido, é a fonte primária.
- **disciplina**: define a cor (`<body class="d-...">`, lista em `references/design.md`).
  Se não informada, inferir pelo tópico.

## Fluxo de trabalho (siga na ordem)

### 1. Entender o pedido
Identificar comando, tópico, banca, cargo e material. Perguntar **no máximo uma vez**
e só se faltar o tópico. Todo o resto tem padrão.

### 2. Levantar o conteúdo (fidelidade antes de beleza)
Ler `references/fidelidade.md`. Resumo:
- Material do usuário > texto oficial (Planalto, DOU, sites .gov.br, regimentos) >
  súmulas/informativos oficiais > doutrina consolidada.
- Dispositivo citado = conferido na fonte. Sem fonte acessível → `<span class="verificar">`.
- Anotar as fontes usadas: vão no rodapé da última folha.

### 3. Roteiro didático
Antes do HTML, montar mentalmente o roteiro: subtemas → para cada um escolher
**o componente pela forma do conteúdo** (tabela em `references/design.md` §3).
Regra de ouro: **ilustre tudo que tem estrutura** (classificação, processo,
hierarquia, comparação, prazos, regra+exceção). Texto corrido só para conceito puro,
e mesmo assim curto, em bloco, com termos-chave grifados.

### 4. Escrever o HTML-fonte (a partir do template)
Ler `references/componentes.md` e `references/design.md`. **Copiar o template do
comando** para `<slug>-fonte.html` e preencher — não escrever o esqueleto do zero
(economiza tokens e padroniza a saída):

| Comando | Template (`assets/templates/`) |
|---|---|
| `/resumo`, `/esquema`, `/lei-seca`, `/comparar`, `/pegadinhas`, `/mnemonico` | `resumo.html` (apague o que não usar) |
| `/revisao` | `revisao.html` |
| `/flashcards` | `flashcards.html` (8 cartões por folha) |
| `/questoes` | `questoes.html` |
| `/edital`, `/cronograma` | `edital.html` |
| `/apostila` | `capa-sumario.html` + um `resumo.html` por tópico |

- Trocar **todo** `[[MARCADOR]]` (o `verificar.py` avisa se sobrar) e a classe
  `d-…` do `<body>` (cor da disciplina).
- Nunca escrever CSS próprio extenso: usar as classes do design system. Ajustes
  pontuais via `style=""` são aceitáveis (ex.: largura de coluna).
- Ilustrações: `<svg class="ilustra g"><use href="#i-juiz"/></svg>`. Ids disponíveis
  em `references/design.md` §4 (galeria: `docs/galeria.png` do repositório).
  Se precisar de algo que não existe, desenhar um SVG inline novo **no mesmo estilo**
  (regras em `references/design.md` §4).

### 5. Verificar, montar e renderizar
```bash
python3 <skill>/scripts/verificar.py <slug>-fonte.html          # lint: classes, ids, folhas
python3 <skill>/scripts/montar.py <slug>-fonte.html <slug>.html  # [--fontes-embutidas]
python3 <skill>/scripts/renderizar.py <slug>.html <pasta-saida> --json
```
- `verificar.py`: corrigir todo ERRO antes de montar.
- `montar.py` injeta CSS + ilustrações usadas e protege referências com espaço
  inseparável ("art. 59", "30 dias"). `--fontes-embutidas` embute Inter e Poppins
  (PDF igual sem internet).
- `renderizar.py` gera PDF + PNG por folha e o relatório de layout (estouro de página,
  vazamento lateral, transbordo de caixa, colunas desequilibradas, fonte < 8 pt).
  Corrigir todo aviso antes de seguir (encurtar texto, mover bloco, criar nova folha).
  `--pb` gera também PNGs em cinza para conferir a leitura em P&B.
- Sem Python/navegador disponível: entregar o HTML (imprime em PDF pelo navegador,
  Ctrl+P → A4, margens nenhuma, gráficos de fundo ligado).

### 6. Validação (3 revisores independentes)
Os revisores **não podem ter escrito o material**: precisam olhar a frio.

- **Se houver ferramenta de subagentes (Agent/Task)**: lançar os três em paralelo,
  cada um com o conteúdo do respectivo arquivo de `agentes/` como prompt, mais:
  caminho do HTML final, caminhos dos PNGs, banca, e a lista de fontes usadas.
  - `agentes/validador-conteudo.md` — confere cada afirmação contra a fonte.
  - `agentes/revisor-didatico.md` — clareza, cobertura do que cai, densidade.
  - `agentes/critico-design.md` — olha os PNGs e o HTML, aplica o checklist visual.
- **Sem subagentes**: fazer os três passes em sequência, cada um relendo o arquivo
  do zero com o checklist do respectivo `agentes/*.md`, sem se apoiar na memória de
  como foi escrito.

Cada revisor devolve itens classificados **BLOQUEANTE / IMPORTANTE / SUGESTÃO**.
Corrigir todos os BLOQUEANTES e IMPORTANTES; re-montar, re-renderizar.
No máximo 2 rodadas; o que restar vira nota na entrega.

### 7. Entregar
- HTML final (autocontido) + PDF quando gerado.
- Em 2–4 linhas: o que foi gerado, itens `[VERIFICAR]` restantes, fontes.
- Não descrever o conteúdo do arquivo: o usuário vai abrir.

## Regras inegociáveis

1. **Fidelidade > estética.** Número, prazo, quórum, artigo, exceção: da fonte, nunca
   de memória sem conferência. Dúvida = `[VERIFICAR]`, nunca invenção.
2. **Direitos autorais.** Não copiar texto, esquemas ou imagens de apostilas,
   cursinhos ou livros de terceiros. Lei e atos oficiais podem ser citados
   literalmente (não têm proteção autoral — Lei 9.610/98, art. 8º, IV).
   Material do usuário serve de fonte para resumir com palavras próprias.
3. **Sem fotos de terceiros nem retratos de pessoas reais.** Autores/doutrinadores
   reais = personagem genérico (`i-autor`) + nome escrito. Prédios, bandeiras,
   símbolos: desenhar em SVG no estilo da biblioteca.
4. **Legível em P&B.** Cor nunca é o único portador de significado: todo bloco
   semântico tem ícone e rótulo.
5. **Densidade de apostila, não de slide.** Frases telegráficas, sem introdução,
   sem "neste resumo veremos". Mas nada de parede de texto: bloco > 6 linhas
   sem destaque = reescrever ou quebrar.
