# Figuras didáticas: de onde vêm

Leia quando o assunto pede uma imagem que **ensina a estrutura** (anatomia, célula,
órgão, circuito, molécula, mapa, montagem de laboratório, gráfico de um fenômeno).

**Regra central: a IA não desenha estrutura acadêmica de cabeça.** Um modelo de
linguagem erra proporção, posição e conexões sem perceber, e um erro de anatomia na
figura é erro de conteúdo. Por isso a figura vem de **quem é da área** (acervo aberto,
revisado) ou é **calculada a partir de dados exatos** (gerador). Desenho SVG feito à mão
para anatomia, célula, órgão ou aparelho é **proibido**: o `verificar.py` acusa.

## 1. Escolha a origem (nesta ordem)

| Conteúdo | Origem | Como |
|---|---|---|
| Anatomia, histologia, célula, órgão, organismo, aparelho de laboratório | **Acervo aberto** | `figura.py acervo` → `baixar` (§2) |
| Mapa (geografia, história, clima, geologia), astronomia, espectro, tabela periódica | **Acervo aberto** | `figura.py acervo` → `baixar` (§2) |
| Molécula, reação, fórmula estrutural | **Gerador**: RDKit a partir do SMILES | `figura.py molecula` (§3) |
| Gráfico de função, curva, dados (física, economia, estatística, cinética) | **Gerador**: matplotlib a partir da equação ou dos dados | `figura.py grafico` (§3) |
| Circuito elétrico | **Gerador**: schemdraw (símbolos padronizados) | §3 |
| Processo, rito, algoritmo, classificação (sem forma física) | **Componente** do Grifo (`.fluxo`, `.chave`, `.linha-tempo`…) | `componentes.md` |
| Ancorar a memória ao lado de um bloco | **Ícone Lucide** | `design.md` §4 |

Não achou figura confiável com licença aberta? **Não invente.** Use um componente
(fluxo, tabela) e indique na referência onde ver a imagem ("ver Netter, prancha X" ou o
link do capítulo da OpenStax). Melhor sem figura do que com figura errada.

## 2. Acervo aberto (Wikimedia Commons)

**Comece pelo acervo curado** (`assets/acervo.json`): 61 figuras já conferidas — existem,
licença aceita, autor e idioma dos rótulos anotados — em anatomia humana, biologia
celular, genética, botânica e ecologia, química, física, geociências, astronomia,
geografia e história.

```bash
python3 <skill>/scripts/figura.py acervo                 # áreas e quantidades
python3 <skill>/scripts/figura.py acervo "rim"           # por tema, área ou tag (sem acento também)
python3 <skill>/scripts/figura.py baixar "File:2610 The Kidney.jpg" figuras/ --nome rim
```
Não achou no acervo? Busque no Commons (abaixo). Achou figura boa que serve a outros
materiais? Ela pode entrar no acervo por PR (`CONTRIBUTING.md`).

O Commons reúne as figuras da **OpenStax** (livros didáticos revisados por pares, CC BY),
**Servier Medical Art** (CC BY), **NIH** (domínio público) e milhares de diagramas
traduzidos. Tudo com licença declarada, que o script lê sozinho.

```bash
python3 <skill>/scripts/figura.py buscar "OpenStax heart anatomy"
python3 <skill>/scripts/figura.py buscar "heart diagram pt"          # versão já em português
python3 <skill>/scripts/figura.py buscar "Servier kidney"            # ilustração sem rótulos
python3 <skill>/scripts/figura.py baixar "File:Nome do arquivo.png" figuras/ --nome rim-corte
```

- **Termos em inglês** acham mais. Tente `<termo> pt` (ou `es`, `fr`…) para achar a
  versão já traduzida para a língua do material.
- `baixar` grava `figuras/slug.png` (fundo branco, reduzida) e `figuras/slug.json`
  (autor, licença, links) e imprime o `<figure>` com o crédito pronto.
- **Licenças aceitas:** CC0, domínio público, CC BY, CC BY-SA. Recusadas: NC (não
  comercial), ND (sem derivadas), só GFDL, sem licença.
- **CC BY-SA:** use a imagem **sem alterar** e diga "sem alterações" no crédito.
- **Obra derivada** (tradução, versão recortada): o script avisa. Confira a licença do
  original; uma tradução marcada como domínio público de um original CC BY-SA continua
  CC BY-SA. Credite o autor original e o tradutor.
- **Confira a figura** como confere um número (`fidelidade.md`): abra o PNG, veja se mostra
  o que o texto diz, na vista que a legenda declara. Figura de fonte aberta também erra.

### Rótulos e idioma
1. **Melhor:** figura já rotulada na língua do material (busque `… pt`).
2. **Rótulos em outra língua** (comum na OpenStax, em inglês): mantenha a figura e ponha
   ao lado uma tabela **"Na figura → Português"** com os termos na ordem do processo. Para
   estudante de saúde, o termo em inglês também ensina.
3. **Figura sem rótulos** (Servier, "unannotated", "unlabeled") **com licença CC0, domínio
   público ou CC BY:** sobreponha chamadas numeradas em HTML (§4). Não sobreponha em CC BY-SA.

## 3. Geradores (a figura sai dos dados)

```bash
python3 <skill>/scripts/figura.py molecula "CC(=O)Oc1ccccc1C(=O)O" figuras/aas.svg   # pip install rdkit
python3 <skill>/scripts/figura.py grafico "oferta = 10 + x/3" "demanda = 60 - x/2" figuras/mercado.svg \
        --x 0,120 --eixos "Quantidade,Preço (R$)" --pontos "60,30,E"                  # pip install matplotlib
python3 <skill>/scripts/figura.py grafico --csv figuras/titulacao.csv figuras/titulacao.svg --eixos "V (mL),pH"
```
- **`grafico`**: expressões em `x` com aritmética e funções numpy da lista (sin, exp, log,
  sqrt, where…); nada de código arbitrário. `--pontos` marca o que foi **calculado**
  (equilíbrio, raiz, máximo) com guias até os eixos. Cores do Grifo e um traço por série
  (legível em P&B); eixo começa em 0 quando os dados são positivos. Mesmo comando, mesmo
  arquivo (SVG sem data).
- **SMILES** conferido no PubChem antes. A fórmula molecular impressa pelo script é a
  checagem: se não bate com a fonte, o SMILES está errado.
- **Gráfico fora do padrão** (barras, dispersão, histograma, área): escreva um script curto em `figuras/`, gere SVG com
  `plt.savefig("figuras/x.svg", bbox_inches="tight")`, fonte ≥ 8 pt no tamanho final,
  eixos com nome e unidade, cores com sentido (legenda diz o que é cada uma). A curva
  vem da equação ou de dados citados, nunca de "formato aproximado" de memória.
- **Circuito** (schemdraw, `pip install schemdraw`): mesmo esquema; símbolos da norma que
  o curso usa (IEC ou ANSI). Mínimo:
  ```python
  import schemdraw, schemdraw.elements as e
  with schemdraw.Drawing(file="figuras/rc.svg") as d:
      d += e.SourceV().label("12 V"); d += e.Resistor().right().label("1 kΩ")
      d += e.Capacitor().down().label("10 µF"); d += e.Line().left()
  ```
- Crédito de figura gerada: `<span class="credito">Gerado com RDKit/matplotlib a partir de …</span>`.

## 4. HTML

```html
<figure class="figura aberta lado">                <!-- .lado: imagem | texto; .larga: imagem maior -->
  <img src="figuras/coracao-corte-pt.png" alt="Corte frontal do coração…">
  <div> … tabela "Na figura → Português", sequência, cores … </div>
  <figcaption>Corte frontal, vista anterior.
    <span class="credito">Imagem: Autor, <a href="página no Commons">Wikimedia Commons</a>,
    <a href="link da licença">CC BY 4.0</a>.</span></figcaption>
</figure>
```

Chamadas numeradas sobre imagem sem rótulos (só CC0/PD/CC BY):
```html
<figure class="figura aberta lado">
  <div class="sobre">
    <img src="figuras/rim-servier.png" alt="…">
    <b class="marca" style="left:38%;top:22%">1</b>
    <b class="marca" style="left:55%;top:61%">2</b>
  </div>
  <ol class="legenda"><li>Córtex renal</li><li>Pelve renal</li></ol>
  <figcaption>… <span class="credito">Imagem: Servier Medical Art, CC BY 4.0, com chamadas acrescentadas.</span></figcaption>
</figure>
```
- `left`/`top` em % da imagem. Posicione, **renderize e olhe o PNG**: a chamada tem que
  cair sobre a estrutura certa. Errou a posição = erro de conteúdo.
- O caminho de `src` é relativo ao HTML-fonte; o `montar.py` embute a imagem.
- `verificar.py` dá ERRO em figura sem `.credito`, imagem remota (`http…`) ou arquivo que
  não existe; avisa em imagem > 900 KB.

## 5. Checklist da figura (o crítico de design usa este)
1. **Origem válida:** acervo aberto com licença aceita ou gerador a partir de dados.
   Nada desenhado à mão para estrutura física.
2. **Correta e coerente com o texto:** mostra o que a legenda diz, na vista declarada.
3. **Crédito completo:** autor, onde (link), licença (link); "sem alterações" em CC BY-SA;
   "com chamadas acrescentadas" quando houver.
4. **Legível:** rótulos da imagem ≥ ~7 pt no tamanho impresso; se ficarem menores, use
   `.larga` ou largura total.
5. **Idioma resolvido:** rótulos na língua do material, ou tabela de tradução ao lado.
6. **Cor explicada** na legenda quando carrega sentido (O₂, carga, tecido).
7. **Sem retrato** de pessoa real.
8. Ocupa o espaço que merece: figura central ≥ metade da largura da folha.
