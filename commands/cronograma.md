---
description: Plano semanal até a prova com revisões espaçadas
argument-hint: <matérias ou edital> --horas N --prova dd/mm/aaaa
disable-model-invocation: true
---

**Primeiro passo obrigatório:** carregue a skill do plugin com a ferramenta **Skill**,
nome `grifo-skill:grifo` (ou `grifo`). Ela informa a pasta da skill ("Base directory");
todos os caminhos citados (`references/`, `scripts/`, `assets/templates/`) são relativos
a essa pasta — não procure os arquivos em outro lugar nem improvise um layout próprio.

Depois execute o comando `/cronograma` com os argumentos, exatamente como o usuário digitou
(não reescreva, não reordene, não remova aspas):

$ARGUMENTS

Interprete as flags pela seção "Sintaxe" de `references/comandos.md` (sem flags = padrões;
flag desconhecida = avisar e seguir) e siga o fluxo completo do SKILL.md com a
especificação de `/cronograma`, partindo do template em `assets/templates/`.
