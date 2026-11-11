# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versões seguem [SemVer](https://semver.org/lang/pt-BR/). A cada tag `vX.Y.Z` o workflow
de release grava a versão na skill (aparece ao lado do logo em cada folha) e publica o zip.

## [Não lançado]

### Adicionado
- **Estilos de cor** (`--estilo`, `data-tema`): `sobrio` (padrão), `colorido` (cada coluna
  e bloco num matiz), `pastel` (matizes suaves) e `pb` (cinza para impressão). Seis matizes
  de tópico que não colidem com vermelho/verde/âmbar; `cor-1`…`cor-6` fixam a cor de um
  tópico. A skill pergunta o estilo junto com o formato.
- **Figuras rotuladas desenhadas do zero** (`.figura`, chamadas numeradas, legenda HTML,
  paleta científica) e o guia `references/ilustracoes.md` (método em camadas, convenções
  de vista e de cor por área, checklist).
- **13 ilustrações de saúde e ciências** com sombra e brilho: coração, pulmões, neurônio,
  célula, DNA, microscópio, estetoscópio, cápsula, frasco, átomo, molécula, planta, osso.
- **Outros idiomas** (`--idioma`, `references/idiomas.md`): material na língua do usuário,
  textos do CSS traduzidos (en, es, fr, it, de), hifenização por `lang`, exames de outros
  países, espaço inseparável também em en/es/fr/it/de e unidades (mL, mmHg, bpm…).
- Exemplos `medicina-coracao` (colorido, 2 figuras do zero) e `en-photosynthesis`
  (inglês, pastel); `README.en.md`.

### Alterado
- Logo do README em cartão branco arredondado (legível no tema escuro do GitHub), nome
  numa cor só, sem grifo amarelo; social preview com mascote menor.
- `renderizar.py` mede texto de SVG no tamanho real (escala do viewBox).
- Galeria agrupa seções pequenas na mesma linha (cabe em 1 A4 com 60 símbolos).
- Verificador de contraste cobre os matizes e o estilo `pb` (67 pares).

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
