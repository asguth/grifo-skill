# Comandos — especificação

Cada comando define **estrutura de saída** e **critério de pronto**. Todos seguem o
fluxo do SKILL.md (fonte → roteiro → HTML → montar → renderizar → 3 revisores).

---

## /resumo `<tópico> [banca] [cargo]`
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

## /esquema `<tópico>`
**Saída:** 1 folha, retrato. Um mapa do tópico inteiro: raiz no centro/topo,
ramos com `.chave`, `.fluxo` ou SVG próprio, ≤ 12 palavras por nó, ilustração nos
ramos principais. Sem questões. Serve para colar na parede / revisão rápida.

## /lei-seca `<lei> [artigos]`
**Saída:** folhas com o **texto literal** do dispositivo em `.lei-seca`, grifado:
- `mark` amarelo = núcleo do dispositivo (o que decorar);
- `mark.troca` rosa = palavras que a banca costuma trocar (prazos, "salvo",
  "vedado", "poderá" × "deverá", "exclusivamente", quóruns);
- ao lado (coluna direita), quadros curtos: "em outras palavras", exceções,
  remissões a outros artigos, súmulas relacionadas.
Texto da lei: copiar da fonte oficial vigente, com a redação atualizada e a indicação
da lei alteradora quando o dispositivo foi modificado ("Redação dada pela Lei X").
Dispositivo revogado: mostrar riscado (`.riscado`) só se for clássico de prova.

## /comparar `<A> vs <B> [vs C]`
**Saída:** 1 folha. `table.comparativo` com critérios em linhas (natureza, requisitos,
prazo, competência, efeitos, exemplos), ✔/✘ onde for binário, linha `.destaque` na
diferença mais cobrada. Abaixo: quadro "COMO A BANCA CONFUNDE" com 3–5 trocas típicas.

## /pegadinhas `<tópico> [banca]`
**Saída:** 1–2 folhas. Para cada armadilha: assertiva errada no estilo da banca
(em `.caixa.pegadinha`, palavra trocada em `mark.troca`) → versão correta
(`.caixa.dica`) → fundamento (artigo/súmula). Agrupar por tipo (troca de prazo,
generalização, inversão de regra/exceção, competência trocada…). Ver bancas.md.

## /questoes `<tópico> [banca] [n=10]`
**Saída:** questões **inéditas** (nunca copiar questões reais de provas — elas têm
autoria da banca; pode-se apenas imitar o formato). Formato pela banca:
- Cebraspe: itens Certo/Errado com texto-base comum quando fizer sentido.
- FGV/FCC/Vunesp/Cesgranrio/IBFC: múltipla escolha A–E (conferir no edital se o
  concurso usar outro nº de alternativas).
- Indefinida: metade C/E, metade A–E.
Gabarito comentado em folha separada no final: letra/item, por que está certo,
por que cada distrator está errado (1 linha cada), dispositivo.
Distribuir dificuldade: 30% fácil, 50% média, 20% difícil.

## /flashcards `<tópico> [n=16]`
**Saída:** folhas `.flashcards` com frente e verso **na mesma linha** (frente à
esquerda, verso à direita: dobrar no meio) — evita alinhamento de impressão frente/verso.
Frente: pergunta curta ou lacuna ("Prazo para ___"). Verso: resposta + artigo.
8 cartões por folha. Um fato por cartão.

## /mnemonico `<lista ou tópico>`
**Saída:** meia folha a uma folha. Para cada lista memorizável: sigla (`.sigla`)
ou frase, a lista completa ao lado, e uma ilustração que ancore a imagem mental.
Mnemônico ruim é pior que nenhum: só criar se encurtar de verdade a lista e
não colidir com outra sigla do mesmo tópico.

## /edital `<texto ou PDF do edital> [cargo]`
**Saída:** `table.edital` com cada matéria (`tr.materia`) e cada item do conteúdo
programático em linha própria com checkbox, colunas: ☐ | item | peso/nº questões
da matéria | prioridade (★–★★★) | link para o resumo (se já existir).
Prioridade = peso da matéria × recorrência histórica do assunto na banca (quando
souber; senão marcar só pelo peso e dizer isso). Copiar os itens do edital
literalmente (é ato oficial). Resumo no topo: data da prova, nº de questões,
critério de eliminação, cargo.

## /cronograma `<edital ou matérias> <horas/semana> <data da prova>`
**Saída:** tabela semanal até a prova. Regras:
- Distribuir horas proporcionalmente a peso × dificuldade declarada.
- Revisões espaçadas: 24h, 7 dias, 30 dias após cada tópico novo (bloco "R").
- Últimas 2 semanas: só revisão + questões + simulados.
- 1 bloco semanal de questões mistas por matéria.
Entregar também como tabela simples (o usuário pode querer levar para planilha).

## /revisao `<tópico>`
**Saída:** exatamente 1 folha. Só o essencial: 1 diagrama, 1 tabela, lista
"10 coisas que caem", pegadinhas em 1 linha cada. Fonte mínima 8.5pt.

## /apostila `<disciplina> [tópicos...]`
**Saída:** um único HTML/PDF com: capa (`.folha.capa`), sumário (`.sumario`),
resumos de cada tópico (reutilizar HTMLs-fonte já gerados na pasta se existirem;
gerar os que faltarem), bloco de questões no fim de cada tópico, gabarito geral ao
final. Numerar folhas no `.topo .pag` sequencialmente.

## /validar `<arquivo.html>`
Roda só a etapa 6 (os 3 revisores) sobre um material existente e devolve o
relatório consolidado + correções aplicadas, se o usuário quiser.
