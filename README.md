<p align="center">
  <img src="docs/marca/logo.png" alt="Grifo-Skill — apostilas ilustradas de qualquer assunto" width="520">
</p>

<h1 align="center">Grifo-Skill: apostilas ilustradas de qualquer assunto, feitas com IA</h1>

<p align="center">
  <b>Skill gratuita para Claude e Codex que transforma um tema — ou o seu PDF, slides ou
  anotações — em material de estudo A4: resumo esquematizado, mapa, revisão, questões
  inéditas com gabarito comentado e flashcards, com figuras de acervo aberto e revisão em
  três etapas.</b>
</p>

<p align="center">
  <a href="https://github.com/asguth/grifo-skill/releases/latest"><img alt="Versão" src="https://img.shields.io/github/v/release/asguth/grifo-skill?label=vers%C3%A3o&color=243B53"></a>
  <a href="https://github.com/asguth/grifo-skill/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/asguth/grifo-skill/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-243B53">
  <img alt="Claude.ai skill" src="https://img.shields.io/badge/Claude.ai-skill-2F6B8A">
  <img alt="Codex skill" src="https://img.shields.io/badge/Codex-skill-596579">
  <a href="LICENSE"><img alt="Código aberto" src="https://img.shields.io/badge/c%C3%B3digo-aberto-237A57"></a>
  <a href="https://buymeacoffee.com/asguth"><img alt="Buy Me a Coffee" src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-apoie-FFDD00?logo=buymeacoffee&logoColor=000"></a>
</p>

<p align="center"><b>Português</b> · <a href="README.en.md">English</a></p>

<p align="center">
  <img src="docs/demo.gif" alt="Animação folheando apostilas geradas pelo Grifo-Skill: capa, economia, medicina, direito, português, lógica e biologia" width="560">
</p>

<p align="center">
  <a href="#como-usar">Como usar</a> ·
  <a href="#instalação">Instalação</a> ·
  <a href="#exemplos">Exemplos</a> ·
  <a href="#figuras-de-verdade">Figuras</a> ·
  <a href="#como-funciona">Como funciona</a> ·
  <a href="#perguntas-frequentes">FAQ</a> ·
  <a href="#apoie-o-projeto">Apoie</a>
</p>

---

## O que é

Você diz o assunto (ou anexa o arquivo) e o formato. O **Grifo** pesquisa em fontes
confiáveis, monta folhas A4 com **design editorial** — hierarquia clara, cor só onde
carrega significado, legível impresso em preto e branco — e entrega **HTML e PDF**.
Serve para faculdade, medicina, concursos, escola e certificações, em qualquer área.

- **Capa no estilo da marca**, sumário, folhas em duas colunas, questões e gabarito em
  folhas separadas (sem spoiler).
- **Figuras que não são inventadas:** vêm de acervo aberto com crédito ou são calculadas
  a partir de dados ([detalhes](#figuras-de-verdade)).
- **Três revisores** antes da entrega:

| Revisor | O que confere |
|---|---|
| 🔎 Validador de conteúdo | Cada dado, data, fórmula, artigo e gabarito contra a fonte |
| 🎓 Revisor didático | Definição precisa, mecanismo, exemplo, erro comum |
| 🎨 Crítico de design | Layout, hierarquia, cores e figuras nas páginas renderizadas |

## Como usar

Peça do seu jeito. Se faltar o assunto ou o formato, a skill **pergunta antes de começar**:

> **Você:** faz uma apostila desse PDF de farmacologia
> **Grifo:** Qual formato? *Explicação completa* · *Só o mapa* · *Revisão rápida* · *Treino* · *Tudo incluso*
> E qual estilo? *Sóbrio* · *Colorido* · *Pastel* · *P&B*

Ou vá direto ao comando:

| Comando | O que gera | Exemplo |
|---|---|---|
| `/resumo` | Explicação completa (2–4 folhas por padrão, sem limite) + questões + gabarito | `/resumo ciclo de Krebs --nivel faculdade` |
| `/esquema` | Mapa visual (1 folha por padrão) | `/esquema tipos de memória RAM` |
| `/revisao` | Revisão de véspera (1 folha por padrão) | `/revisao derivadas` |
| `/questoes` | Questões **inéditas** + gabarito comentado em folha separada | `/questoes LGPD --nivel concurso --banca cebraspe` |
| `/flashcards` | Cartões frente/verso para recortar | `/flashcards anatomia do coração` |
| `/comparar` | Tabela A × B + confusões comuns | `/comparar mitose vs meiose` |
| `/mnemonico` | Siglas e frases para decorar | `/mnemonico camadas do modelo OSI` |
| `/apostila` | Tudo incluso: capa, sumário, resumos, questões e gabarito | `/apostila microeconomia --material notas.pdf` |
| `/lei-seca` · `/pegadinhas` · `/edital` · `/cronograma` | Para concursos | `/lei-seca Lei 9.784/1999 --artigos 53-55` |
| `/validar` | Roda os 3 revisores num HTML existente | `/validar minha-apostila.html` |
| `/grifo` | Ajuda com todos os comandos e flags | `/grifo questoes` |

Flags: `--formato completo|mapa|revisao|treino|tudo` · `--estilo sobrio|colorido|pastel|pb`
· `--nivel medio|faculdade|concurso|certificacao` · `--folhas N` (sem limite) · `--material arquivo`
· `--idioma en|es|fr|it|de…` · `--banca` (concursos). Detalhes em
[`references/comandos.md`](skills/grifo/references/comandos.md).

**Estilos de cor** — cada pessoa memoriza de um jeito:

| Estilo | Como fica |
|---|---|
| **Sóbrio** (padrão) | azul-marinho e cinza; cor só onde tem significado |
| **Colorido** | cada coluna e bloco num matiz (azul, petróleo, roxo, vinho, índigo, grafite) |
| **Pastel** | os mesmos matizes em tons suaves |
| **P&B** | tons de cinza, para imprimir em preto e branco |

Vermelho, verde e âmbar ficam reservados a erro, acerto e exceção em qualquer estilo.

**Outros idiomas:** *"make a cheat sheet on the cardiac cycle"* sai em inglês,
*"hazme un resumen de fotosíntesis"* sai em espanhol — com rótulos, datas e hifenização
do idioma ([`references/idiomas.md`](skills/grifo/references/idiomas.md)).

## Instalação

**Claude Code** (plugin, com os comandos de barra):
```
/plugin marketplace add asguth/grifo-skill
/plugin install grifo-skill@grifo-skill
```
Digite `/grifo` para ver os comandos. Conflito de nome com outro plugin? Use `/grifo-skill:resumo`.

**Claude.ai / app Claude:** baixe **`grifo-skill.zip`** em
[Releases](https://github.com/asguth/grifo-skill/releases/latest), envie em
**Configurações → Capacidades → Skills** e peça *"faz um resumo de termodinâmica"*.

**Codex:**
```bash
git clone https://github.com/asguth/grifo-skill
cp -r grifo-skill/skills/grifo ~/.codex/skills/grifo
```
Dentro deste repositório, o [`AGENTS.md`](AGENTS.md) já aponta o Codex para a skill.

> PDF e PNG precisam de Python + Playwright (ou Chrome). Sem isso, a skill entrega o HTML
> para imprimir pelo navegador (Ctrl+P → A4, sem margens, gráficos de fundo). Gráficos
> calculados usam matplotlib; moléculas, RDKit (opcionais).

## Exemplos

<p align="center">
  <img src="docs/exemplos/mosaico.png" alt="Primeira folha de cada exemplo: capa de Microeconomia, coração, LGPD, crase, proposições, Lei 8.112, Lei 9.784 e fotossíntese">
</p>

| Material | Área | Mostra | Folhas | PDF |
|---|---|---|---|---|
| [Microeconomia: oferta, demanda e elasticidade](docs/exemplos/economia-oferta-demanda-p1.png) | Economia | `/apostila` com capa e sumário; **gráficos calculados** das equações | 6 | [PDF](exemplos/economia-oferta-demanda.pdf) |
| [Coração: anatomia e ciclo cardíaco](docs/exemplos/medicina-coracao-p1.png) | Medicina | estilo **colorido**; figuras de **acervo aberto** com crédito | 4 | [PDF](exemplos/medicina-coracao.pdf) |
| [LGPD — bases legais](docs/exemplos/lgpd-bases-legais-p1.png) | Proteção de dados | tabela comparativa, fluxo de decisão, mnemônico | 4 | [PDF](exemplos/lgpd-bases-legais.pdf) |
| [Crase](docs/exemplos/portugues-crase-p1.png) | Língua Portuguesa | testes passo a passo, análise de frase | 4 | [PDF](exemplos/portugues-crase.pdf) |
| [Proposições e tabela-verdade](docs/exemplos/rlm-proposicoes-p1.png) | Lógica | tabela-verdade, fórmula | 4 | [PDF](exemplos/rlm-proposicoes.pdf) |
| [Lei 8.112/90 — servidores federais](docs/exemplos/lei-8112-servidores-p1.png) | Direito Administrativo | fluxo de prazos, pirâmide, classificação em chave | 5 | [PDF](exemplos/lei-8112-servidores.pdf) |
| [Lei 9.784/99 — processo administrativo](docs/exemplos/lei-9784-processo-administrativo-p1.png) | Direito Administrativo | delegação × avocação, prazos, chave | 4 | [PDF](exemplos/lei-9784-processo-administrativo.pdf) |
| [Photosynthesis](docs/exemplos/en-photosynthesis-p1.png) | Biology (inglês) | estilo **pastel**; material em outra língua | 1 | [PDF](exemplos/en-photosynthesis.pdf) |

Todas as folhas de cada exemplo estão em [`docs/exemplos/`](docs/exemplos).

## Figuras de verdade

Um modelo de linguagem erra anatomia, proporção e conexões sem perceber. Por isso o Grifo
**não desenha estrutura acadêmica de cabeça**: a figura vem de quem é da área ou sai de
uma conta.

| Conteúdo | De onde vem | Comando |
|---|---|---|
| Anatomia, célula, órgão, planta, mapa, astronomia, espectro | **Acervo curado**: 61 figuras do Wikimedia Commons já conferidas (licença, autor, idioma dos rótulos) | `figura.py acervo "rim"` |
| Qualquer outra estrutura | **Busca no Commons** (OpenStax, Servier, NIH, USGS…), só CC0, domínio público, CC BY e CC BY-SA | `figura.py buscar` / `baixar` |
| Gráfico, curva, dados | **Calculado** com matplotlib a partir da equação ou do CSV | `figura.py grafico` |
| Molécula | **RDKit** a partir do SMILES conferido | `figura.py molecula` |
| Processo, classificação, prazo | Componentes do design system (fluxo, chave, linha do tempo) | — |

O acervo curado cobre:

| Área | Figuras | Exemplos |
|---|---|---|
| Anatomia humana | 21 | coração, valvas, rim, néfron, pulmões, digestório, endócrino, linfático, esqueleto, músculos, pele, neurônio, córtex, olho, orelha |
| Biologia celular | 11 | células animal e vegetal (com versão em português), núcleo, mitocôndria, cloroplasto, mitose, meiose |
| Botânica e ecologia | 7 | fotossíntese, flor, folha, ciclos do carbono, nitrogênio e água, classificação biológica |
| Química | 4 | tabela periódica, camadas eletrônicas, orbitais, diagrama de fases da água |
| Física | 4 | espectro eletromagnético, lente, refração, Modelo Padrão |
| Geociências | 4 | camadas da Terra, placas tectônicas, clima de Köppen |
| Geografia | 4 | Brasil (estados, regiões, biomas), fusos horários |
| Astronomia | 3 | planetas, fases da Lua, estações do ano |
| História | 2 | Tordesilhas e Saragoça, alianças de 1914 |
| Genética | 1 | DNA |

Toda figura sai com autor, fonte e licença na legenda; o `verificar.py` recusa figura sem
crédito. Para ampliar o acervo, veja o [CONTRIBUTING.md](CONTRIBUTING.md).

<details>
<summary><b>Galeria do design system</b> (mascote, ícones e componentes)</summary>

![Mascote e amostra de ícones Lucide](docs/galeria.png)
![Componentes do design system](docs/galeria-componentes.png)
</details>

## Como funciona

```
pedido ─▶ (pergunta assunto/formato, se faltar) ─▶ fontes ─▶ roteiro didático
       ─▶ template + figuras ─▶ verificar.py ─▶ montar.py ─▶ renderizar.py (PDF + PNG + relatório)
       ─▶ 3 revisores ─▶ correções ─▶ entrega
```

- **`grifo.css`** — design editorial: navy para estrutura; âmbar, vermelho e verde só para
  exceção, erro e acerto; estilos `colorido`, `pastel` e `pb`. Contraste ≥ 4,5:1 conferido
  por script; todo destaque tem ícone e rótulo; nenhum texto abaixo de 8 pt.
- **`figura.py`** — acervo curado, busca no Commons, gráfico calculado e molécula.
- **`verificar.py`** — lint do HTML: classes, numeração das folhas, figura sem crédito,
  folha sem o rodapé de crédito e aviso de IA.
- **`montar.py`** — HTML único e autocontido (figuras, mascote e ícones embutidos), espaço
  inseparável em "art. 59" e "30 dias", `--fontes-embutidas` para PDF sem internet.
- **`renderizar.py`** — PDF A4 + PNG por folha + relatório de layout (estouro, transbordo,
  colunas desequilibradas, fonte pequena); `--pb` gera prévia em cinza.

## Regras que a skill segue

- **Fidelidade acima de estética:** todo dado vem de fonte conferida; o resto sai marcado
  `[VERIFICAR]`. Referências com link.
- **Sem cópia:** nada de texto, esquema ou questão de terceiros. Imagem de terceiros só com
  licença aberta e crédito. Atos oficiais podem ser citados (Lei 9.610/98, art. 8º, IV).
- **Aviso em toda folha:** o rodapé imprime "Feito com Grifo-Skill · gerado com IA: confira
  nas fontes".
- **Sem retratos de pessoas reais. Legível em preto e branco.**

## Limitações e responsabilidade

> ⚠️ O Grifo-Skill gera material de estudo com IA. Ele **auxilia** o estudo e **não
> substitui** livros, aulas, atlas, legislação oficial nem orientação de professores.
> Textos, questões e figuras podem conter erros, inclusive conceituais, mesmo depois da
> revisão. Confira tudo nas fontes indicadas. Figuras são de apoio, sem valor de referência
> clínica. O uso é de responsabilidade de quem usa; o projeto é fornecido "no estado em que
> se encontra", sem garantias.

## Perguntas frequentes

**É de graça?** Sim, e o código é aberto.

**Serve para faculdade ou só concurso?** Para qualquer assunto e nível. Concursos ganham
extras (banca, lei seca, pegadinhas, edital).

**Posso usar meu material?** Sim: anexe PDF, slides ou anotações (`--material`); ele vira a
fonte principal.

**Posso vender o que gerar?** Pode, mantendo o crédito "Feito com Grifo-Skill" (o rodapé já
traz) e os créditos das figuras. Confira o conteúdo antes.

**Dá para mudar as cores?** Sim: `--estilo colorido`, `pastel` ou `pb`, ou peça "mais
colorido" / "mais sóbrio".

**Funciona em inglês/espanhol?** Sim, escreve na sua língua (`--idioma` força uma).

## Estrutura

```
skills/grifo/          a skill (vai no grifo-skill.zip)
  SKILL.md             fluxo principal
  references/          comandos, design, ilustrações, idiomas, componentes, fidelidade, bancas
  agentes/             validador de conteúdo, revisor didático, crítico de design
  assets/              grifo.css, acervo.json, templates/, lucide/, mascote/, fontes/
  scripts/             figura.py, verificar.py, montar.py, renderizar.py
commands/              comandos de barra do Claude Code
.claude-plugin/        manifest do plugin e marketplace
exemplos/              fontes HTML, figuras (com crédito) e PDFs dos exemplos
ferramentas/           testes, verificadores, galeria, docs, versão e marca
docs/                  imagens do README e marca
```

## Marca

<img src="docs/marca/icone.png" alt="Ícone do Grifo-Skill" width="96" align="left">

O **Grifo** — mascote do projeto — e o logo podem ser usados em materiais gerados,
apresentações e forks, com o crédito. Arquivos em [`docs/marca/`](docs/marca). Só não use a
marca para sugerir que um material é oficial do projeto quando não é.
<br clear="left">

## Contribuindo

PRs são bem-vindos: figuras para o acervo, exemplos de outras áreas, perfis de banca,
componentes. Veja o [CONTRIBUTING.md](CONTRIBUTING.md) e o [CHANGELOG](CHANGELOG.md).

## Apoie o projeto

O Grifo-Skill é gratuito e vai continuar assim. Se ele te ajudou, dá para apoiar com um café:

<p align="center">
  <a href="https://buymeacoffee.com/asguth"><img alt="Pague um café no Buy Me a Coffee" src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-pague%20um%20caf%C3%A9-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=000"></a>
</p>

Ou deixe uma ⭐, compartilhe com quem estuda e [abra uma issue](https://github.com/asguth/grifo-skill/issues/new/choose)
quando achar um erro.

## Licença

© 2026 Alberto Guth (GT Design). Texto completo em [LICENSE](LICENSE).

- **Design e conteúdo** (CSS, templates, mascote, logo, guias, exemplos):
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br). O material gerado
  incorpora esse design e leva o crédito **"Feito com Grifo-Skill"** — o rodapé das folhas já
  imprime.
- **Código** (scripts, ferramentas, plugin): licença MIT.
- **Terceiros**, sempre com crédito: fontes Inter e Poppins
  ([SIL OFL](skills/grifo/assets/fontes/OFL.txt)), ícones Lucide
  ([ISC](skills/grifo/assets/lucide/LICENSE)) e figuras de acervo aberto, cada uma na sua
  licença. Lista em [CREDITOS.md](CREDITOS.md).
