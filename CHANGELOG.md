# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versões seguem [SemVer](https://semver.org/lang/pt-BR/). A cada tag `vX.Y.Z` o workflow
de release grava a versão na skill (aparece ao lado do logo em cada folha) e publica o zip.

## [Não lançado]

### Alterado
- **Sem limite de folhas**: o tamanho de cada comando vira padrão, não teto. `--folhas N`
  aceita qualquer número (antes 1–4); `/resumo`, `/esquema`, `/revisao`, `/comparar` e
  `/pegadinhas` crescem quando o conteúdo pede, sem cortar nem comprimir conteúdo.

## [1.1.0] — 2026-11-12

### Adicionado
- **Capa no estilo do banner do repositório**: mascote, título em navy, selos, faixa da
  marca e rodapé com crédito e aviso de IA (`.marca-capa`, `.banner-capa`, `.selos-capa`).
- **Acervo curado de figuras** (`assets/acervo.json`, `figura.py acervo`): 61 arquivos do
  Wikimedia Commons conferidos (existem, licença aceita, autor, idioma dos rótulos) em
  anatomia humana, biologia celular, genética, botânica e ecologia, química, física,
  geociências, astronomia, geografia e história.
- **`figura.py grafico`**: gráfico calculado com matplotlib a partir de expressões em `x`
  (avaliação restrita, sem código arbitrário) ou de CSV; `--pontos` marca equilíbrio/raiz
  com guias; cores do Grifo e traço por série (P&B); SVG determinístico.
- Exemplo **`economia-oferta-demanda`**: `/apostila` com capa e sumário e três gráficos
  calculados das equações do texto.
- `verificar.py`: ERRO em folha sem `.rodape-folha` (crédito + aviso de IA).
- **Estilos de cor** (`--estilo`, `data-tema`): `sobrio` (padrão), `colorido` (cada coluna
  e bloco num matiz), `pastel` (matizes suaves) e `pb` (cinza para impressão). Seis matizes
  de tópico que não colidem com vermelho/verde/âmbar; `cor-1`…`cor-6` fixam a cor de um
  tópico. A skill pergunta o estilo junto com o formato.
- **Figuras de acervo aberto ou geradas a partir de dados** (`references/ilustracoes.md`):
  `scripts/figura.py` busca no Wikimedia Commons (OpenStax, Servier, NIH…) só licenças
  CC0, domínio público, CC BY e CC BY-SA, baixa, reduz, põe fundo branco e devolve o
  `<figure>` com o crédito; avisa em obra derivada; desenha moléculas com RDKit.
  Componente `.figura.aberta` com `.credito`, `.larga` e chamadas numeradas sobre imagem
  sem rótulos (`.sobre` + `.marca`). O `montar.py` embute as imagens.
- `verificar.py`: ERRO em figura sem crédito, imagem remota ou inexistente; aviso em figura
  desenhada à mão em SVG e em imagem > 900 KB.
- **Aviso de IA e atribuição em toda folha**: o rodapé imprime "Feito com Grifo-Skill ·
  gerado com IA: confira nas fontes" (traduzido por `lang`); seção "Limitações e
  responsabilidade" no README; a entrega termina com o aviso.
- `CREDITOS.md` com fontes, ícones e figuras dos exemplos.
- **Outros idiomas** (`--idioma`, `references/idiomas.md`): material na língua do usuário,
  textos do CSS traduzidos (en, es, fr, it, de), hifenização por `lang`, exames de outros
  países, espaço inseparável também em en/es/fr/it/de e unidades (mL, mmHg, bpm…).
- Exemplos `medicina-coracao` (colorido; coração rotulado em português e sistema de
  condução da OpenStax com tabela "Na figura → Português") e `en-photosynthesis` (inglês,
  pastel; cloroplasto da OpenStax); `README.en.md`.

### Corrigido
- Capa com título e subtítulo brancos sobre fundo branco (invisíveis).
- `figura.py`: `baixar`/`reduzir` definidos duas vezes; a 2ª versão, sem fundo branco no
  lugar da transparência, sobrescrevia a correta.
- Subscrito e sobrescrito abaixo de 8 pt (`sub`, `sup`).
- `montar.py` não troca mais espaços por `&nbsp;` dentro de `<pre>`/`<code>`.
- `atualizar_docs.py` só apaga PNGs antigos depois de regenerar tudo com sucesso.
- Rodapé de exemplo em `componentes.md` duplicava o crédito ("Grifo-Skill · MIT").
- Regras do SKILL.md com numeração repetida.

### Alterado
- Descrições do plugin, CSS e sprite sem "(MIT)" solto: design e conteúdo são CC BY 4.0,
  código MIT. READMEs reescritos; GIF, mosaico (2 linhas), galeria e social preview
  regenerados.
- **Licença**: código continua MIT; design e conteúdo (CSS, templates, mascote, logo,
  guias, exemplos) passam a **CC BY 4.0**, com crédito "Feito com Grifo-Skill" nos
  materiais gerados. Terceiros mantêm a licença de origem, sempre com crédito.
- Imagem de terceiros passa a ser aceita **só com licença aberta e crédito** (antes: nenhuma).
- Logo do README em cartão branco arredondado (legível no tema escuro do GitHub), nome
  numa cor só, sem grifo amarelo; social preview com mascote menor.
- `renderizar.py` mede texto de SVG no tamanho real (escala do viewBox).
- Galeria mostra o mascote e uma amostra de ícones Lucide por área.
- Verificador de contraste cobre os matizes e o estilo `pb` (67 pares).

### Removido
- **Biblioteca de ilustrações prontas** (57 símbolos: personagens, objetos, saúde e
  ciências). O sprite só tem o mascote; ícones ao lado do texto são Lucide. Figuras
  rotuladas desenhadas à mão em SVG deixam de ser método: a IA erra anatomia sem perceber.

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
