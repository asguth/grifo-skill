---
name: grifo
description: Monta apostilas, resumos, mapas, revisões, questões e flashcards ilustrados de qualquer assunto (faculdade, concursos, escola, certificações) em HTML/PDF A4 com design editorial, validação de conteúdo, revisão didática e crítica de design. Use para /resumo, /esquema, /lei-seca, /comparar, /pegadinhas, /questoes, /flashcards, /mnemonico, /edital, /cronograma, /revisao, /apostila, /validar, /grifo ou qualquer pedido de material de estudo.
license: MIT
metadata:
  version: "1.0.0"
---

# Grifo-Skill

Gera material de estudo **nível universitário** sobre **qualquer assunto**, a partir de
um tema ou de um arquivo do usuário: folhas A4 em duas colunas, hierarquia editorial
sóbria, diagramas, tabelas, ilustrações e questões inéditas. Tudo passa por três
revisores (conteúdo, didática, design) antes da entrega.

Caminhos abaixo são relativos à pasta deste SKILL.md.

| Caminho | O que é | Quando ler |
|---|---|---|
| `references/comandos.md` | Sintaxe, flags e especificação de cada comando | Sempre: só a seção "Sintaxe" e a do comando |
| `references/design.md` | Paleta, hierarquia, qual componente usar, ilustrações e ícones | Antes do HTML |
| `references/componentes.md` | HTML de cada componente | Antes do HTML |
| `references/fidelidade.md` | Fontes, citação e referências com link | Antes de pesquisar |
| `references/bancas.md` | Estilo de bancas de concurso | Só se houver banca |
| `agentes/*.md` | Prompts dos 3 revisores | Etapa 6 |
| `assets/templates/*.html` | Esqueleto de cada comando | Início da etapa 4 |
| `assets/lucide/nomes.txt` | 2.052 ícones Lucide (`nome: tags`) | Use `grep`, nunca leia inteiro |
| `scripts/verificar.py`, `montar.py`, `renderizar.py` | Lint → HTML autocontido → PDF/PNG + revisão de layout | Etapa 5 |

## Comandos

```
/<comando> <assunto ou arquivo> [--formato f] [--nivel n] [--banca b] [--folhas N] [--material arq]
```
`/resumo`, `/esquema`, `/lei-seca`, `/comparar`, `/pegadinhas`, `/questoes`, `/flashcards`,
`/mnemonico`, `/edital`, `/cronograma`, `/revisao`, `/apostila`, `/validar`, `/grifo` (ajuda).
`/cmd`, `cmd:` e linguagem natural → mesmo fluxo. Flag desconhecida → avisar e seguir com o
padrão. Comando inexistente → mostrar a ajuda do `/grifo`. Detalhes em `references/comandos.md`.

## Fluxo (siga na ordem)

### 1. Entender o pedido — e perguntar quando faltar
Se o pedido não trouxer **assunto/arquivo** ou **formato**, pergunte **uma vez**, numa
única mensagem (no Claude Code, com a ferramenta de pergunta se houver), oferecendo opções:

1. **Assunto ou arquivo:** "Sobre qual assunto — ou qual arquivo (PDF, slides, anotações) —
   você quer o material?"
2. **Formato:**
   - **Explicação completa** — resumo didático 2–4 folhas + questões + gabarito (padrão de `/resumo`);
   - **Só o mapa** — 1 folha de esquema visual (`/esquema`);
   - **Revisão rápida** — 1 folha de véspera (`/revisao`);
   - **Treino** — questões + gabarito comentado (`/questoes`) ou flashcards;
   - **Tudo incluso** — capa, sumário, resumo, mapa, flashcards, questões e gabarito (`/apostila`).
3. **Nível** (só se não der para inferir): ensino médio, faculdade (padrão), concurso
   (pergunte a banca), certificação.

Com assunto e formato definidos (pelo usuário ou pela flag/comando), **não pergunte mais nada**:
decida o resto. Liberdade de criação: escolha componentes, ordem e ênfase pelo que ensina melhor.

### 2. Levantar o conteúdo (fidelidade antes de beleza)
Ler `references/fidelidade.md`. Material do usuário > fonte oficial/primária > literatura
de referência. Todo número, data, fórmula, artigo ou definição técnica é conferido; sem
fonte acessível → `<span class="verificar">`. Guarde as fontes **com URL** para as referências.

### 3. Roteiro didático (nível faculdade)
Para cada subtema: definição precisa → mecanismo/por quê → exemplo → erro comum.
Escolha o componente pela forma do conteúdo (`references/design.md` §3) e ilustre tudo
que tem estrutura. Texto corrido só para conceito, curto e grifado.

### 4. Escrever o HTML-fonte a partir do template
Copie `assets/templates/<comando>.html` para `<slug>-fonte.html` e troque todo `[[MARCADOR]]`.
- Só classes do design system (`references/componentes.md`); `style=""` só para ajuste pontual.
- **Questões sempre em coluna única**, numa folha só delas. **Gabarito comentado e
  referências em folha separada, depois das questões** (nada de spoiler na mesma folha).
- Referências com link: `<a href="URL oficial">título</a>`.
- Imagens: **ícone Lucide** (`<svg class="ico"><use href="#l-NOME"/></svg>`, ache o nome com
  `grep -i termo assets/lucide/nomes.txt`) ou **ilustração da biblioteca**
  (`<svg class="ilustra g"><use href="#i-NOME"/></svg>`, lista em `design.md` §4).
  Só desenhe SVG novo se nenhum dos dois servir — custa tokens.

### 5. Verificar, montar e renderizar
```bash
python3 <skill>/scripts/verificar.py <slug>-fonte.html
python3 <skill>/scripts/montar.py <slug>-fonte.html <slug>.html     # [--fontes-embutidas]
python3 <skill>/scripts/renderizar.py <slug>.html <saida> --json     # [--pb]
```
Corrija todo ERRO do lint e todo aviso de layout (estouro, transbordo, colunas
desequilibradas, fonte < 8 pt) antes de seguir. Sem Python/navegador: entregue o HTML
(Ctrl+P → A4, sem margens, gráficos de fundo).

### 6. Validação (3 revisores que não escreveram o material)
Com subagentes: rode os três em paralelo, cada um com o seu `agentes/*.md` + caminhos do
HTML e dos PNGs + fontes usadas. Sem subagentes: três passes em sequência, relendo do zero.
Corrija BLOQUEANTES e IMPORTANTES, remonte e renderize (máx. 2 rodadas).

### 7. Entregar
HTML + PDF. Em 2–4 linhas: o que foi gerado, `[VERIFICAR]` restantes, fontes principais.

## Regras inegociáveis
1. **Fidelidade > estética.** Nada de memória sem conferência; dúvida = `[VERIFICAR]`.
2. **Direitos autorais.** Não copiar texto, esquemas, imagens ou questões de terceiros.
   Atos oficiais podem ser citados literalmente (Lei 9.610/98, art. 8º, IV).
3. **Sem retratos de pessoas reais** (use `i-autor` + nome).
4. **Legível em P&B.** Cor nunca é o único portador de significado: ícone + rótulo.
5. **Densidade de apostila.** Frases diretas, sem "neste resumo veremos"; bloco > 6 linhas
   sem destaque = reescrever.
