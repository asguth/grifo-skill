# Comandos — especificação

Cada comando define **estrutura de saída** e **critério de pronto**. Todos seguem o
fluxo do SKILL.md (fonte → roteiro → HTML → montar → renderizar → 3 revisores).

## Sintaxe (igual para todos os comandos)

```
/<comando> <argumento principal> [--flag valor] …
```

| Flag | Valores | Padrão | Vale para |
|---|---|---|---|
| `--banca` | `fgv` `cebraspe` `fcc` `vunesp` `cesgranrio` `ibfc` `quadrix` `indefinida` | `indefinida` | todos que geram questão/pegadinha |
| `--cargo` | texto entre aspas: `--cargo "Analista – ANPD"` | — | todos |
| `--folhas` | número de folhas A4 (`1`–`4`; `/apostila` aceita mais) | o do comando | todos que geram folhas |
| `--material` | caminho de arquivo ou anexo (PDF, apostila, anotações) — vira a fonte primária | — | todos |
| `--disciplina` | classe de cor: `d-portugues` `d-constitucional` `d-administrativo` `d-penal` `d-civil` `d-dados` `d-ti` `d-logica` `d-gestao` `d-contabil` `d-atualidades` (o prefixo `d-` é opcional) | inferida pelo tópico | todos |
| `--n` | quantidade de itens | `/questoes` 10 · `/flashcards` 16 | `/questoes`, `/flashcards` |
| `--artigos` | intervalo ou lista: `1-10`, `5,7,11` | a lei toda | `/lei-seca` |
| `--horas` | horas por semana | — (obrigatório) | `/cronograma` |
| `--prova` | data da prova `dd/mm/aaaa` | — (obrigatório) | `/cronograma` |

**Regras de leitura**
1. **Sem flags = padrões atuais.** `/resumo atos administrativos` funciona sozinho.
2. Tudo que não é flag é o **argumento principal** (tópico, lei, lista, arquivo…).
3. **Forma livre também vale**, e é traduzida para as flags: *"resumo de atos
   administrativos pra FGV, cargo de analista, 2 folhas"* =
   `/resumo atos administrativos --banca fgv --cargo "analista" --folhas 2`.
   As formas posicionais da v1.0 (`/resumo crase fgv`, `/questoes lgpd cebraspe 20`)
   continuam aceitas.
4. `/cmd`, `cmd:` e linguagem natural levam ao **mesmo fluxo**.
5. **Flag desconhecida** ou valor inválido → avisar em uma linha (*"ignorei
   `--cor azul`: flag desconhecida"*) e seguir com o padrão. Nunca parar por isso.
6. **Comando inexistente** → mostrar a ajuda do `/grifo` (abaixo).
7. Conflito de nome com outro plugin no Claude Code → usar o nome com namespace:
   `/grifo-skill:resumo`, `/grifo-skill:grifo` etc.

## /grifo `[ajuda | <comando>]`
Mostra a ajuda. Sem argumento (ou `ajuda`): imprime **exatamente** o bloco abaixo.
Com o nome de um comando (`/grifo questoes`): mostra só a linha dele, as flags que
aceita e o exemplo. Não gera arquivo nem roda o fluxo.

```
GRIFO-SKILL · resumos ilustrados para concursos (MIT)

Sintaxe: /<comando> <tópico> [--banca b] [--cargo "x"] [--folhas N]
                             [--material arquivo] [--disciplina d-x]
Bancas: fgv · cebraspe · fcc · vunesp · cesgranrio · ibfc · quadrix · indefinida (padrão)

/resumo      resumo ilustrado, 1–4 folhas
             /resumo atos administrativos --banca fgv --folhas 2
/esquema     uma folha de mapa visual
             /esquema controle de constitucionalidade
/lei-seca    texto da lei grifado + quadros   [--artigos 1-10]
             /lei-seca Lei 9.784/1999 --artigos 53-55
/comparar    tabela A vs B + como a banca confunde
             /comparar remoção vs redistribuição --banca cebraspe
/pegadinhas  armadilhas típicas da banca
             /pegadinhas licitações --banca fcc
/questoes    questões inéditas + gabarito comentado   [--n 10]
             /questoes LGPD --banca cebraspe --n 20
/flashcards  cartões frente/verso para recortar   [--n 16]
             /flashcards LGPD
/mnemonico   siglas e frases para decorar
             /mnemonico requisitos do ato administrativo
/edital      edital verticalizado com checklist   [--cargo "x"]
             /edital --material edital.pdf --cargo "Técnico Judiciário"
/cronograma  plano semanal com revisões   --horas N --prova dd/mm/aaaa
             /cronograma português, constitucional --horas 20 --prova 15/03/2027
/revisao     uma folha de revisão de véspera
             /revisao processo administrativo
/apostila    capa + sumário + resumos + questões
             /apostila direito administrativo --banca fgv
/validar     roda os 3 revisores num HTML existente
             /validar minha-apostila.html
/grifo       esta ajuda   (/grifo questoes = ajuda de um comando)

Também vale em linguagem natural: "faz um resumo de crase pra FGV".
Conflito com outro plugin? Use /grifo-skill:resumo, /grifo-skill:grifo …
```

---

## /resumo `<tópico> [--banca] [--cargo] [--folhas 1–4] [--material] [--disciplina]`
**Saída:** 1–4 folhas A4 no layout apostila (2 colunas).
**Estrutura:**
1. `.topo` em todas as folhas (logo Grifo, disciplina + tópico, nº da folha).
2. Na 1ª folha: `.titulo-topico` com o nome do assunto (opcional se o tópico for curto).
3. Colunas com `.coluna-cab` (subárea) e `.bloco`s (um por subtema).
4. Cada bloco usa o componente indicado pela forma do conteúdo (design.md §3).
5. Pelo menos: 1 diagrama estrutural (chave, fluxo, pirâmide ou linha do tempo),
   1 tabela comparativa quando houver institutos parecidos, 1 caixa `IMPORTANTE`,
   1 caixa `DICA` ou mnemônico, 1 quadro de pegadinhas da banca.
6. Última folha termina com 3–6 questões de fixação + gabarito comentado + fontes.
**Pronto quando:** cada subtema do item do edital tem bloco; todo dispositivo citado
tem artigo; zero estouro de layout.

## /esquema `<tópico> [--disciplina] [--material]`
**Saída:** 1 folha, retrato. Um mapa do tópico inteiro: raiz no centro/topo,
ramos com `.chave`, `.fluxo` ou SVG próprio, ≤ 12 palavras por nó, ilustração nos
ramos principais. Sem questões. Serve para colar na parede / revisão rápida.

## /lei-seca `<lei> [--artigos 1-10] [--banca] [--folhas] [--material]`
**Saída:** folhas com o **texto literal** do dispositivo em `.lei-seca`, grifado:
- `mark` amarelo = núcleo do dispositivo (o que decorar);
- `mark.troca` rosa = palavras que a banca costuma trocar (prazos, "salvo",
  "vedado", "poderá" × "deverá", "exclusivamente", quóruns);
- ao lado (coluna direita), quadros curtos: "em outras palavras", exceções,
  remissões a outros artigos, súmulas relacionadas.
Texto da lei: copiar da fonte oficial vigente, com a redação atualizada e a indicação
da lei alteradora quando o dispositivo foi modificado ("Redação dada pela Lei X").
Dispositivo revogado: mostrar riscado (`.riscado`) só se for clássico de prova.

## /comparar `<A> vs <B> [vs C] [--banca] [--disciplina]`
**Saída:** 1 folha. `table.comparativo` com critérios em linhas (natureza, requisitos,
prazo, competência, efeitos, exemplos), ✔/✘ onde for binário, linha `.destaque` na
diferença mais cobrada. Abaixo: quadro "COMO A BANCA CONFUNDE" com 3–5 trocas típicas.

## /pegadinhas `<tópico> [--banca] [--folhas 1–2]`
**Saída:** 1–2 folhas. Para cada armadilha: assertiva errada no estilo da banca
(em `.caixa.pegadinha`, palavra trocada em `mark.troca`) → versão correta
(`.caixa.dica`) → fundamento (artigo/súmula). Agrupar por tipo (troca de prazo,
generalização, inversão de regra/exceção, competência trocada…). Ver bancas.md.

## /questoes `<tópico> [--banca] [--n 10] [--cargo] [--material]`
**Saída:** questões **inéditas** (nunca copiar questões reais de provas — elas têm
autoria da banca; pode-se apenas imitar o formato). Formato pela banca:
- Cebraspe: itens Certo/Errado com texto-base comum quando fizer sentido.
- FGV/FCC/Vunesp/Cesgranrio/IBFC: múltipla escolha A–E (conferir no edital se o
  concurso usar outro nº de alternativas).
- Indefinida: metade C/E, metade A–E.
Gabarito comentado em folha separada no final: letra/item, por que está certo,
por que cada distrator está errado (1 linha cada), dispositivo.
Distribuir dificuldade: 30% fácil, 50% média, 20% difícil.

## /flashcards `<tópico> [--n 16] [--material]`
**Saída:** folhas `.flashcards` com frente e verso **na mesma linha** (frente à
esquerda, verso à direita: dobrar no meio) — evita alinhamento de impressão frente/verso.
Frente: pergunta curta ou lacuna ("Prazo para ___"). Verso: resposta + artigo.
8 cartões por folha. Um fato por cartão.

## /mnemonico `<lista ou tópico> [--disciplina]`
**Saída:** meia folha a uma folha. Para cada lista memorizável: sigla (`.sigla`)
ou frase, a lista completa ao lado, e uma ilustração que ancore a imagem mental.
Mnemônico ruim é pior que nenhum: só criar se encurtar de verdade a lista e
não colidir com outra sigla do mesmo tópico.

## /edital `<texto do edital ou --material edital.pdf> [--cargo] [--banca]`
**Saída:** `table.edital` com cada matéria (`tr.materia`) e cada item do conteúdo
programático em linha própria com checkbox, colunas: ☐ | item | peso/nº questões
da matéria | prioridade (★–★★★) | link para o resumo (se já existir).
Prioridade = peso da matéria × recorrência histórica do assunto na banca (quando
souber; senão marcar só pelo peso e dizer isso). Copiar os itens do edital
literalmente (é ato oficial). Resumo no topo: data da prova, nº de questões,
critério de eliminação, cargo.

## /cronograma `<matérias ou edital> --horas N --prova dd/mm/aaaa`
**Saída:** tabela semanal até a prova. Regras:
- Distribuir horas proporcionalmente a peso × dificuldade declarada.
- Revisões espaçadas: 24h, 7 dias, 30 dias após cada tópico novo (bloco "R").
- Últimas 2 semanas: só revisão + questões + simulados.
- 1 bloco semanal de questões mistas por matéria.
Entregar também como tabela simples (o usuário pode querer levar para planilha).

## /revisao `<tópico> [--banca] [--disciplina]`
**Saída:** exatamente 1 folha. Só o essencial: 1 diagrama, 1 tabela, lista
"10 coisas que caem", pegadinhas em 1 linha cada. Fonte mínima 8.5pt.

## /apostila `<disciplina> [tópicos...] [--banca] [--cargo] [--folhas] [--material]`
**Saída:** um único HTML/PDF com: capa (`.folha.capa`), sumário (`.sumario`),
resumos de cada tópico (reutilizar HTMLs-fonte já gerados na pasta se existirem;
gerar os que faltarem), bloco de questões no fim de cada tópico, gabarito geral ao
final. Numerar folhas no `.topo .pag` sequencialmente.

## /validar `<arquivo.html> [--banca] [--material]`
Roda só a etapa 6 (os 3 revisores) sobre um material existente e devolve o
relatório consolidado + correções aplicadas, se o usuário quiser.
