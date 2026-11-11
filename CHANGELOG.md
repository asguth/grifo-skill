# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versões seguem [SemVer](https://semver.org/lang/pt-BR/). A cada tag `vX.Y.Z` o workflow
de release grava a versão na skill (aparece ao lado do logo em cada folha) e publica o zip.

## [1.0.0] — 2026-11

Primeira versão pública.

- **Skill `grifo`** para Claude Code (plugin), Claude.ai (zip) e Codex (`~/.codex/skills`):
  apostilas, resumos, mapas, revisões, questões e flashcards ilustrados de **qualquer
  assunto** (faculdade, concursos, ensino médio, certificações), em HTML e PDF A4.
- **Pergunta antes de começar** quando falta o assunto/arquivo ou o formato (explicação
  completa, só o mapa, revisão rápida, treino ou tudo incluso).
- **14 comandos** com sintaxe única e flags (`--formato`, `--nivel`, `--folhas`,
  `--material`, `--banca`…), mais `/grifo` de ajuda.
- **Design editorial**: paleta neutra com cores semânticas (navy, blue, amber, red,
  green, slate), contraste ≥ 4,5:1, legível em P&B; versão da skill ao lado do logo.
- **Ilustrações**: 47 próprias e coloridas (com o mascote Grifo) + 2.052 ícones Lucide
  por nome, sem gastar tokens desenhando SVG.
- **Questões sem spoiler**: coluna única; gabarito comentado e referências com link em
  folha separada.
- **Três revisores** (conteúdo, didática, design) antes da entrega.
- **Scripts**: `verificar.py` (lint), `montar.py` (HTML autocontido, espaço inseparável
  em "art. 59"/"30 dias", fontes embutidas opcionais) e `renderizar.py` (PDF, PNG e
  revisão de layout em JSON).
- **Templates** por comando, cinco exemplos (LGPD, Lei 8.112, Lei 9.784, crase,
  lógica proposicional), CI e templates de issue.
