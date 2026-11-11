# Idiomas

A skill escreve o material **no idioma do usuário**: o da mensagem dele, ou o pedido
com `--idioma` (`pt-BR`, `pt-PT`, `en`, `es`, `fr`, `it`, `de`, ou qualquer código BCP 47).
Fale com o usuário no mesmo idioma. Comandos com barra (`/resumo`…) valem em qualquer
idioma; em linguagem natural, "make a study guide", "hazme un resumen", "fais-moi une
fiche" seguem o mesmo fluxo.

## O que muda no HTML

1. `<html lang="en">` (o código certo): ativa hifenização da língua e troca os textos
   que o CSS gera (`[VERIFICAR]`, `ATENÇÃO:`, incidência) — já traduzidos para
   en, es, fr, it e de no `grifo.css`.
2. **Todo texto fixo dos templates** é traduzido: rótulos de caixa, tags, cabeçalhos de
   tabela, "Gabarito comentado", "Referências", rodapé, `aria-label`. Use a tabela abaixo.
3. Datas, números e unidades no padrão local: `11/11/2026` (pt/es/fr/it/de),
   `Nov 11, 2026` ou `2026-11-11` (en); vírgula ou ponto decimal conforme a língua.
4. Questões no formato dos exames **daquele país** (ver "Exames" abaixo).

## Rótulos fixos

| pt-BR | en | es | fr | it | de |
|---|---|---|---|---|---|
| Importante | Key point | Importante | Important | Importante | Wichtig |
| Dica | Tip | Consejo | Astuce | Suggerimento | Tipp |
| Pegadinha / Como a banca confunde | Common trap | Trampa frecuente | Piège classique | Trabocchetto | Typische Falle |
| Exceção | Exception | Excepción | Exception | Eccezione | Ausnahme |
| Exemplo | Example | Ejemplo | Exemple | Esempio | Beispiel |
| Regra | Rule | Regla | Règle | Regola | Regel |
| Conceito | Concept | Concepto | Notion | Concetto | Begriff |
| Critério | Criterion | Criterio | Critère | Criterio | Kriterium |
| Questões inéditas | Original questions | Preguntas inéditas | Questions inédites | Domande inedite | Eigene Übungsfragen |
| Gabarito comentado | Answer key with explanations | Solucionario comentado | Corrigé commenté | Soluzioni commentate | Lösungen mit Erklärung |
| Referências | References | Referencias | Références | Riferimenti | Quellen |
| Certo / Errado (C/E) | True / False (T/F) | Verdadero / Falso (V/F) | Vrai / Faux (V/F) | Vero / Falso (V/F) | Richtig / Falsch (R/F) |
| Frente / Verso | Front / Back | Anverso / Reverso | Recto / Verso | Fronte / Retro | Vorderseite / Rückseite |
| atualizado até | updated | actualizado al | mis à jour le | aggiornato al | Stand |
| Sumário | Contents | Índice | Sommaire | Indice | Inhalt |

`.ce` com C/E: troque as letras dentro dos `<span>` (ex.: `<span>T</span><span>F</span>`).
Mnemônicos (`.sigla`) são criados **na língua do material**; nunca traduza uma sigla
portuguesa letra a letra.

## Fontes e escrita

- Inter e Poppins embutidas cobrem o alfabeto latino básico. Para línguas com
  diacríticos do latin-ext (polonês, tcheco, vietnamita, turco…) ou outros alfabetos
  (grego, cirílico, árabe, CJK), **não use `--fontes-embutidas`**: o link do Google Fonts
  carrega os subconjuntos certos, e o CSS cai para as fontes do sistema no que faltar.
- Escrita da direita para a esquerda (árabe, hebraico): `<html lang="ar" dir="rtl">`;
  confira o PNG — setas de `.fluxo` e `.chave` continuam apontando para a direita.

## Exames de outros países

`--nivel concurso` e `--banca` (`bancas.md`) são do Brasil. Para outro país, use o nome
do exame em `--banca` (ex.: `--banca usmle`, `--banca mir`, `--banca "bar exam"`,
`--banca "a-level"`) e, antes de escrever questões, **confira na fonte oficial do exame**
o formato (nº de alternativas, item único × múltiplo, penalidade por erro, uso de
caso clínico). Sem fonte acessível: múltipla escolha de resposta única e aviso
`[VERIFICAR] formato do exame` na entrega. As regras de fidelidade e de questões
inéditas (`fidelidade.md`) valem igual: nada de copiar questões reais.

## Fontes de conteúdo por país

Legislação, normas técnicas e protocolos clínicos mudam de país para país: use a fonte
oficial **da jurisdição do usuário** (ex.: legislation.gov.uk, BOE, Légifrance,
diretrizes da sociedade médica local). Se o usuário não disse o país e o conteúdo
depende disso (direito, tributação, protocolo clínico, currículo escolar), assuma o
país mais provável pelo idioma e diga qual foi na entrega.
