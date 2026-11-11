# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versões seguem [SemVer](https://semver.org/lang/pt-BR/).

## [1.1.0] — 2026-11

### Novo
- **Comandos com sintaxe única e flags**: `--banca`, `--cargo`, `--folhas`,
  `--material`, `--disciplina` (e `--n`, `--artigos`, `--horas`, `--prova` onde
  fazem sentido). Sem flags = padrões; forma livre continua valendo.
- **`/grifo`**: ajuda com todos os comandos, flags e um exemplo de cada.
- **Templates por comando** (`assets/templates/`): resumo, revisão, flashcards,
  questões, edital e capa + sumário.
- **Componentes**: `.formula` (RLM/estatística), `table.verdade` (tabela-verdade
  com V/F coloridos), `pre.codigo` (SQL/pseudocódigo) e `.exemplo-frase`
  (análise sintática com rótulo da função).
- **12 ilustrações** para matérias além de Direito: calculadora, gráfico,
  ampulheta, código, rede, diálogo, globo, mapa, escola, hospital, distintivo
  genérico e troféu (46 no total).
- **Fontes offline**: `montar.py --fontes-embutidas` embute Inter e Poppins (OFL).
- **Exemplos novos**: Português — crase (2 folhas) e RLM — proposições (2 folhas).
- **Scripts**: `verificar.py` (lint do HTML-fonte), `verificar_ilustracoes.py`,
  `verificar_contraste.py`, `galeria.py` (galeria gerada dos símbolos) e
  `test_montar.py`.
- **`renderizar.py`**: aponta transbordo de caixa, colunas desequilibradas
  (> 25%) e fonte < 8 pt; flags `--pb` (PNG em cinza), `--json` e `--estrito`.
- **CI** no GitHub Actions; `CONTRIBUTING.md` e templates de issue.

### Melhorado
- **Quebras de linha**: espaço inseparável automático em "art. 59", "§ 1º",
  "inciso IV", "Lei nº 8.112", "30 dias úteis", "p.ú." etc.; quebra opcional depois
  de "/" entre palavras.
- **Tipografia**: hifenização em pt-BR no corpo (não em títulos e tabelas), títulos e
  faixas com linhas equilibradas, respiro uniforme dentro dos blocos, recuo pendente
  nas listas e no gabarito, marcador ✔ alinhado à primeira linha.
- Fonte mínima de 8 pt em todo o design system; flashcards cabem 8 por folha.
- Laranja de exceção (`--excecao`) com contraste 3,3:1 para texto branco.
- `assets/apostila.css` renomeado para `assets/grifo.css`.

### Corrigido
- Seis ilustrações (`i-juiz`, `i-autor`, `i-servidora`, `i-estudante`,
  `i-congresso`, `i-constituicao`) ficavam dentro de um comentário quebrado do
  `ilustracoes.svg`.
- `.com-ilustra`: a ilustração não encolhe nem é invadida por palavras longas.
- "Conveniência/oportunidade" vazava a coluna na Lei 9.784; sigla "ADCPR" da
  Lei 8.112 tinha marcação corrompida e "Produtividade" não cabia na caixa.
- `montar.py` gravava CRLF no Windows.

## [1.0.0] — 2026-11-11
- Primeira versão: skill `grifo`, 13 comandos, design system, 34 ilustrações,
  `montar.py`, `renderizar.py`, três revisores e três exemplos (LGPD,
  Lei 9.784/99, Lei 8.112/90).
