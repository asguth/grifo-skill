---
description: Ajuda do Grifo-Skill — lista todos os comandos, flags e exemplos
argument-hint: [ajuda | <comando>]
---

**Primeiro passo obrigatório:** carregue a skill do plugin com a ferramenta **Skill**,
nome `grifo-skill:grifo` (ou `grifo`). Ela informa a pasta da skill ("Base directory");
todos os caminhos citados (`references/`, `scripts/`, `assets/`) são relativos a essa
pasta — não procure os arquivos em outro lugar.

Depois execute o comando `/grifo` (ajuda) com os argumentos:

$ARGUMENTS

Sem argumento ou com `ajuda`: mostre **exatamente** o bloco de ajuda da seção `/grifo`
de `references/comandos.md`, dentro de um bloco de código. Com o nome de um comando
(ex.: `questoes`): mostre só a linha desse comando, as flags que ele aceita e o exemplo.
Não gere arquivos e não rode o fluxo de produção.
