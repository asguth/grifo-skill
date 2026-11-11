---
description: Roda os 3 revisores (conteúdo, didática, design) num HTML
argument-hint: <arquivo.html> [--banca b] [--material arq]
---

**Primeiro passo obrigatório:** carregue a skill do plugin com a ferramenta **Skill**,
nome `grifo-skill:grifo` (ou `grifo`). Ela informa a pasta da skill ("Base directory");
todos os caminhos citados (`references/`, `scripts/`, `assets/templates/`) são relativos
a essa pasta — não procure os arquivos em outro lugar nem improvise um layout próprio.

Depois execute o comando `/validar` com os argumentos, exatamente como o usuário digitou
(não reescreva, não reordene, não remova aspas):

$ARGUMENTS

Interprete as flags pela seção "Sintaxe" de `references/comandos.md` (sem flags = padrões;
flag desconhecida = avisar e seguir) e siga o fluxo completo do SKILL.md com a
especificação de `/validar`, partindo do template em `assets/templates/`.
