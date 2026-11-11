# Fidelidade e fontes

Um resumo bonito com um prazo errado reprova o candidato. Este arquivo vale mais
que todo o design system.

## Hierarquia de fontes
1. **Material enviado pelo usuário** (apostila, PDF, edital). Resumir com palavras
   próprias; nunca copiar layout/esquemas de terceiros.
2. **Texto normativo oficial vigente:** planalto.gov.br, in.gov.br (DOU), sites
   .gov.br dos órgãos (resoluções, portarias, regimentos), câmara/senado (legislação
   compilada). Se um portal bloquear acesso automático, usar outro espelho oficial
   (camara.leg.br, legis.senado.leg.br, normas.leg.br) e informar.
3. **Jurisprudência oficial:** súmulas e teses do STF/STJ/TST nos sites dos tribunais.
4. **Doutrina consolidada / manuais de referência** — para conceitos e
   classificações; quando houver divergência, indicar a corrente majoritária e a
   que a banca adota (se souber, com base em questão real que o usuário trouxer).
5. Blogs e resumos de terceiros: só para **localizar** a fonte primária, nunca
   como fonte final.

## Regras de escrita
- Todo dispositivo citado leva **número** (art., inciso, alínea, §). Ex.: "art. 7º, IX".
- Lei alterada: usar a redação vigente e, se a alteração for recente/cobrável,
  marcar com `<span class="selo novidade">Lei X/AAAA</span>`.
- **Números** (prazos, idades, quóruns, percentuais, valores): copiar da fonte.
  Se não conferiu, envolver em `<span class="verificar">…</span>`.
- Classificação doutrinária: dizer de quem é quando não for consenso
  ("segundo Hely Lopes Meirelles…").
- Não inventar súmula, tese, informativo ou número de julgado. Sem fonte = não cita.
- Data de referência: no rodapé, "Atualizado até dd/mm/aaaa — conferir alterações
  posteriores".

## Rodapé de fontes (última folha)
```html
<div class="pequeno"><b>Fontes:</b> Lei 13.709/2018 (redação vigente, consulta em
dd/mm/aaaa); Enunciado CD/ANPD nº 1/2023. Atualizado até dd/mm/aaaa.</div>
```

## Referências com link
- Toda referência que existe on-line vai com link clicável para a **fonte oficial ou
  primária** (`<a href="…">`): planalto.gov.br, DOU, site do tribunal/órgão, DOI do artigo,
  página da editora/norma técnica. O link sai clicável no PDF.
- Só use URL que você abriu ou tem certeza que existe; na dúvida, cite sem link.
- Livros: autor, título em itálico, edição/ano (sem link, a menos que haja página oficial).
