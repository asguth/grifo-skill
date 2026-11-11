#!/usr/bin/env python3
"""Mostra ou troca a versão do Grifo-Skill em todos os lugares de uma vez.

Uso:  python ferramentas/versao.py            # mostra
      python ferramentas/versao.py 1.2.0      # grava em SKILL.md, plugin.json e marketplace.json

Fonte da verdade: metadata.version do skills/grifo/SKILL.md (o montar.py a imprime ao
lado do logo de cada folha). O workflow de release chama este script com a tag.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "grifo" / "SKILL.md"
PLUGIN = REPO / ".claude-plugin" / "plugin.json"
MARKET = REPO / ".claude-plugin" / "marketplace.json"


def atual() -> str:
    return re.search(r'^\s*version:\s*"([^"]+)"', SKILL.read_text(encoding="utf-8"), re.M).group(1)


def gravar(v: str):
    if not re.fullmatch(r"\d+\.\d+\.\d+", v):
        sys.exit(f"versão inválida: {v!r} (use X.Y.Z)")
    t = SKILL.read_text(encoding="utf-8")
    SKILL.write_text(re.sub(r'(^\s*version:\s*")[^"]+(")', rf"\g<1>{v}\2", t, count=1, flags=re.M),
                     encoding="utf-8", newline="\n")
    for arq, chaves in ((PLUGIN, [["version"]]), (MARKET, [["metadata", "version"], ["plugins", 0, "version"]])):
        d = json.loads(arq.read_text(encoding="utf-8"))
        for ch in chaves:
            alvo = d
            for k in ch[:-1]:
                alvo = alvo[k]
            alvo[ch[-1]] = v
        arq.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        gravar(sys.argv[1].lstrip("v"))
    print(atual())
