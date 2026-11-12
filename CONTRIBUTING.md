# Contribuindo com o Grifo-Skill

Obrigado por ajudar! O Grifo-Skill vive de contribuições pequenas e bem conferidas.
Código entra sob MIT; design, guias e exemplos sob CC BY 4.0 (ver `LICENSE`): ao abrir um
PR você concorda com isso. Não há biblioteca de ilustrações prontas: figura didática vem
de acervo aberto ou de gerador a partir de dados. Este guia cobre os tipos de PR mais comuns.

## Antes de qualquer PR

Instale uma vez:

```bash
pip install playwright pillow
python -m playwright install chromium
```

Rode os verificadores (são os mesmos do CI) e só abra o PR com tudo passando:

```bash
python ferramentas/verificar_ilustracoes.py           # sprite do mascote
python ferramentas/test_montar.py                     # espaço inseparável
python ferramentas/test_figura.py                     # licenças e imagens embutidas
python ferramentas/verificar_contraste.py             # contraste das cores
python skills/grifo/scripts/verificar.py exemplos/*-fonte.html
```

Se mexeu em CSS, figura ou exemplo, **re-renderize e olhe os PNGs** — não confie
só no código:

```bash
python skills/grifo/scripts/montar.py exemplos/X-fonte.html exemplos/X.html
python skills/grifo/scripts/renderizar.py exemplos/X.html saida --pb
```

O `renderizar.py` precisa terminar com `LAYOUT: sem avisos`. **Anexe ao PR o PNG da
folha afetada** (antes e depois, se for mudança visual).

## Figuras dos exemplos e acervos

1. Leia `skills/grifo/references/ilustracoes.md`. Figura de estrutura física (anatomia,
   célula, aparelho) **não** é desenhada à mão em SVG.
2. Busque e baixe com `python skills/grifo/scripts/figura.py buscar "…"` e `baixar`: o
   script só aceita CC0, domínio público, CC BY e CC BY-SA e grava o crédito no `.json`.
3. Coloque o arquivo em `exemplos/figuras/`, use `<figure class="figura aberta">` com
   `.credito` e acrescente a linha em `CREDITOS.md`.
4. Confira a figura contra a fonte: figura de acervo também erra.

Não aceitamos: imagem NC/ND ou sem licença, retrato de pessoa real, brasão/logotipo
real, nem imagem copiada de apostila, livro ou banco de imagens.

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
