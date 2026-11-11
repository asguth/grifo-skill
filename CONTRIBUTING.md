# Contribuindo com o Grifo-Skill

Obrigado por ajudar! O Grifo-Skill é MIT e vive de contribuições pequenas e bem
conferidas. Prefira ícone Lucide a desenhar ilustração nova: a biblioteca só cresce
com desenhos que nenhum dos 2.052 ícones resolve. Este guia cobre os três tipos de PR mais comuns.

## Antes de qualquer PR

Instale uma vez:

```bash
pip install playwright pillow
python -m playwright install chromium
```

Rode os verificadores (são os mesmos do CI) e só abra o PR com tudo passando:

```bash
python ferramentas/verificar_ilustracoes.py           # biblioteca de ilustrações
python ferramentas/test_montar.py                     # espaço inseparável
python ferramentas/verificar_contraste.py             # contraste das cores
python skills/grifo/scripts/verificar.py exemplos/*-fonte.html
```

Se mexeu em CSS, ilustração ou exemplo, **re-renderize e olhe os PNGs** — não confie
só no código:

```bash
python skills/grifo/scripts/montar.py exemplos/X-fonte.html exemplos/X.html
python skills/grifo/scripts/renderizar.py exemplos/X.html saida --pb
```

O `renderizar.py` precisa terminar com `LAYOUT: sem avisos`. **Anexe ao PR o PNG da
folha afetada** (antes e depois, se for mudança visual).

## Propor uma ilustração

1. Leia `skills/grifo/references/design.md` §4 (estilo, paleta permitida e a regra do
   sprite).
2. Desenhe em `viewBox="0 0 64 64"`, no máximo 15 elementos, contorno `#1C2430` 2.5px,
   sem gradiente, só cores da paleta. Use as classes do sprite (`kf`, `k`, `f-disc`,
   `f-claro`, `f-disc2`…) da paleta de ilustração.
3. Acrescente o `<symbol id="i-…">` em `skills/grifo/assets/ilustracoes.svg`, na seção
   de comentário certa (ou crie uma: `<!-- NOME DA SEÇÃO -->`).
4. Rode `ferramentas/verificar_ilustracoes.py` e `ferramentas/galeria.py` (atualiza `docs/galeria.png`).
5. Liste o novo id em `design.md` §4 e anexe o recorte da galeria ao PR.

Não aceitamos: retrato ou caricatura de pessoa real, brasão/logotipo real, emblemas
protegidos (ex.: cruz vermelha), nem desenho copiado de apostila, livro ou banco de
imagens.

## Melhorar um perfil de banca

`skills/grifo/references/bancas.md` descreve o estilo de cada banca. Para propor
mudança:

- descreva **padrões** (formato, tamanho de enunciado, tipo de pegadinha), nunca cole
  questões reais — elas têm autoria da banca;
- cite de onde veio a observação (ex.: "provas de 2022–2025 para cargos de nível
  superior, conferidas no site da banca");
- se possível, inclua no PR um exemplo de questão **inédita** no novo padrão.

## Exemplos e conteúdo

- Todo artigo, prazo e número precisa estar conferido na fonte oficial vigente
  (`references/fidelidade.md`); diga no PR qual fonte usou.
- Erro de conteúdo num exemplo é prioridade máxima: abra uma issue "Erro de conteúdo"
  mesmo que não vá corrigir.
- Questões dos exemplos são sempre inéditas.

## Estilo dos commits

Um commit por mudança, mensagem em português no imperativo ou descritiva
(`feat(css): …`, `fix(ilustracoes): …`, `docs(exemplos): …`).
Ao mudar algo visível, registre em `CHANGELOG.md` na seção "Não lançado".
