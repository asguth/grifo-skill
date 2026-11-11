# AGENTS.md — Grifo-Skill

Instruções para agentes de código (Codex, Claude Code e outros) trabalhando **neste
repositório**. Para *usar* a skill, o ponto de entrada é `skills/grifo/SKILL.md`.

## Usar a skill a partir daqui
Pedidos de material de estudo ("faz uma apostila de X", "/resumo X", "/esquema X",
"questões de X") seguem `skills/grifo/SKILL.md`: leia-o e siga o fluxo. Os caminhos
`references/`, `assets/`, `scripts/` e `agentes/` citados lá são relativos a `skills/grifo/`.

## Estrutura
- `skills/grifo/` — a skill (é o que vai no `grifo-skill.zip`). Só o necessário para rodar.
- `commands/` + `.claude-plugin/` — slash commands e manifest do plugin do Claude Code.
- `ferramentas/` — scripts de desenvolvimento (verificadores, galeria, docs, versão, marca).
- `exemplos/*-fonte.html` — fontes dos exemplos; o HTML montado não é versionado.
- `docs/` — imagens do README.

## Antes de entregar uma mudança
```bash
python ferramentas/verificar_ilustracoes.py
python ferramentas/test_montar.py
python ferramentas/verificar_contraste.py
python skills/grifo/scripts/verificar.py exemplos/*-fonte.html
python ferramentas/atualizar_docs.py   # remonta, renderiza e falha em aviso de layout
```
Mudou CSS, ilustração ou exemplo? Olhe os PNGs gerados, não só o código.

## Regras
- Design editorial (`skills/grifo/references/design.md`): layout neutro, cor só com
  significado; ilustrações podem ser coloridas.
- Questões em coluna única; gabarito + referências (com link) em folha separada.
- Nada de texto, imagem ou questão de terceiros. Fontes Inter/Poppins são OFL; ícones
  Lucide são ISC.
- Versão: `python ferramentas/versao.py X.Y.Z` (ou só crie a tag `vX.Y.Z`: o workflow de
  release grava a versão e publica o zip).
