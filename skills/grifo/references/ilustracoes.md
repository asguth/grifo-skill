# Ilustrações desenhadas do zero

Leia quando o assunto pede uma imagem que **ensina a estrutura** (anatomia, célula,
circuito, ciclo, aparelho, mapa, montagem experimental) e nenhum ícone Lucide ou
símbolo da biblioteca resolve. Um coração com as câmaras rotuladas ensina; um ícone de
coração ao lado do texto só enfeita. Para medicina, biologia, química, física,
engenharia e geografia, **a figura rotulada é o centro da folha**, não um detalhe.

## 1. Ícone ou figura?

| Precisa… | Faça | Formato |
|---|---|---|
| ancorar a memória ao lado de um bloco | símbolo da biblioteca ou ícone Lucide | `<svg class="ilustra g"><use href="#i-…"/></svg>` |
| mostrar partes, posição, caminho ou mecanismo | **figura rotulada** desenhada do zero | `<figure class="figura">` com SVG inline + legenda numerada |
| mostrar etapas sem forma física (rito, algoritmo) | componente (`.fluxo`, `.chave`…) | `references/componentes.md` |

Biblioteca de saúde e ciências (64×64, já com volume): `i-coracao`, `i-pulmoes`,
`i-neuronio`, `i-celula`, `i-dna`, `i-microscopio`, `i-estetoscopio`, `i-capsula`,
`i-frasco`, `i-atomo`, `i-molecula`, `i-planta`, `i-osso`, além de `i-cerebro` e
`i-hospital`.

## 2. Método (siga na ordem)

1. **Confira a estrutura real antes de desenhar** (`fidelidade.md`): partes, posição
   relativa, proporção aproximada, o que liga em quê. Anote na fonte as 6–14 estruturas
   que vão ganhar número. Desenho errado é erro de conteúdo, não de estética.
2. **Fixe a convenção de vista** e escreva-a na legenda (`figcaption`):
   - Anatomia: **posição anatômica**; vista anterior mostra o lado **direito do paciente
     à esquerda** de quem olha. Diga o corte: frontal, sagital, transversal.
   - Química: estrutura com ângulos corretos (água ≈ 104,5°, metano tetraédrico…).
   - Física: eixos e sentido positivo indicados; vetores com seta e rótulo.
   - Mapas: norte para cima, escala ou "sem escala".
3. **Esboce em camadas**, nesta ordem no SVG (o que vem depois fica por cima):
   1. o que passa **por trás** (vasos que entram, fundo, eixos);
   2. a **silhueta** principal (contorno `.contorno` + cor base);
   3. **sombra** (`.f-sombra`) num lado só, sempre o mesmo (direita/baixo) — dá volume;
   4. **estruturas internas** (cavidades, organelas, componentes) em tom mais claro;
   5. o que passa **na frente** (vasos anteriores, setas de fluxo);
   6. **brilho** (`.f-brilho`) pequeno no lado oposto à sombra;
   7. **chamadas numeradas** e linhas-guia — por último, sobre tudo.
4. **Numere na ordem de leitura** (seguindo o fluxo, ou de cima para baixo, da
   esquerda para a direita). A legenda `ol.legenda` repete a mesma ordem.
5. **Monte, renderize e olhe o PNG** (não só o código). Corrija o que falhar no §5.

## 3. Esqueleto

```html
<figure class="figura lado legenda-2">           <!-- .lado: desenho | legenda; .legenda-2: 2 colunas -->
  <svg viewBox="0 0 200 170" role="img" aria-label="Corte frontal do coração…">
    <path class="f-musculo contorno" d="…"/>      <!-- silhueta -->
    <path class="f-sombra" d="…"/>                <!-- volume -->
    <path class="seta-fluxo s-venoso" d="…"/>     <!-- fluxo -->
    <path class="guia" d="M14 104 L52 98"/>       <!-- linha-guia até a estrutura pequena -->
    <g class="chamada" transform="translate(12 104)"><circle r="5"/><text>4</text></g>
  </svg>
  <ol class="legenda"><li>Veia cava superior</li>…</ol>
  <figcaption>Corte frontal, vista anterior. Azul = pobre em O₂; vermelho = rico em O₂.</figcaption>
</figure>
```

- `viewBox` livre (use ~200 de largura): a figura escala para a coluna ou para a folha
  inteira. Figura grande e central: bloco **fora** de `.apostila-colunas`, largura total.
- Texto dentro do SVG: só os **números** das chamadas (`r="5"`, `text` 7 unidades).
  Nomes ficam na legenda, que é HTML (quebra, hifeniza, traduz). Exceção: rótulo de eixo
  ou de 1–2 palavras com `.rotulo-svg`. O `renderizar.py` mede o tamanho real
  (escala do viewBox) e acusa texto < 8 pt.
- Até ~14 chamadas por figura. Mais que isso: divida em duas figuras (visão geral +
  detalhe), como a folha 2 do exemplo `exemplos/medicina-coracao-fonte.html`.
- Chamada sobre a própria estrutura quando ela é grande; estrutura pequena (valva,
  nó, organela) → chamada **fora** do desenho com `.guia` até ela.
- **Repetir uma forma** (tilacoides, alvéolos, dentes de engrenagem): escreva cada
  elemento; não use `<g id>` + `<use>` dentro do SVG inline — o clone vive numa shadow
  tree e perde as classes do `grifo.css` (sai preto) e o original continua visível.
- SVG inline pode ter `fill="#…"` direto para tons intermediários (câmaras claras etc.);
  prefira as classes abaixo para manter a paleta coerente entre figuras.

## 4. Paleta por área (classes para SVG inline; no sprite, as mesmas sem `f-`)

| Área | Convenção | Classes |
|---|---|---|
| Cardiovascular | rico em O₂ vermelho, pobre em O₂ azul (vale para artéria pulmonar = azul) | `.f-arterial` `.s-arterial` `.f-venoso` `.s-venoso` |
| Anatomia geral | músculo rosado, tecido claro, osso creme, gordura amarela | `.f-musculo` `.f-musculo2` `.f-tecido` `.f-osso` `.f-gordura` |
| Célula | citoplasma creme, núcleo lilás | `.f-citoplasma` `.f-nucleo` |
| Botânica / ecologia | folha verde, água azul-clara | `.f-planta` `.f-planta2` `.f-agua` |
| Química (CPK) | O vermelho, H branco, C cinza-escuro, N azul, S amarelo, Cl verde | `.f-arterial` (O), `.f-branco` (H), `#3A3F48` (C), `.f-venoso` (N) |
| Física | carga + vermelho, − azul; vetores na cor do tópico | `.s-arterial` `.s-venoso` `.s-disc` |
| Volume | sombra 15% e brilho branco | `.f-sombra` `.f-brilho` |
| Traço | contorno `#1C2430`, 1,6 (figura) ou 2,5 (ícone 64×64) | `.contorno` · `.guia` |

Vermelho e verde na figura têm sentido de **convenção da área**, não de "erro/acerto";
por isso a legenda sempre diz o que a cor significa (regra do P&B do `design.md`).
No estilo `pb` as figuras saem em cinza: a legenda e os números continuam bastando.

## 5. Checklist da figura (o crítico de design usa este)

1. **Reconhecível em 1 segundo** pela silhueta, mesmo sem cor.
2. **Correta**: estruturas no lugar certo, na vista declarada; nada inventado.
3. **3 tons por forma**: base, sombra no mesmo lado em todas, brilho pequeno.
4. **Traço uniforme**: mesma espessura no desenho todo; nada de contorno fino ao lado de grosso sem motivo.
5. **Chamadas legíveis**: não cobrem a estrutura vizinha, não se sobrepõem, linha-guia curta e reta.
6. **Legenda = números**: mesma ordem, mesmo total; nome técnico correto na língua do material.
7. **Cor explicada** na `figcaption` quando carrega sentido (O₂, carga, tipo de tecido).
8. **Sem retrato** de pessoa real e **sem cópia** de figura de livro/atlas: desenhe
   do conhecimento conferido, nunca decalcando imagem de terceiros.
9. Ocupa o espaço que merece: figura central ≥ metade da largura da folha.

## 6. O que deixa uma ilustração "ruim" (e o conserto)

| Sintoma | Conserto |
|---|---|
| parece clip-art genérico ao lado do texto | troque por figura rotulada que mostra a estrutura do assunto |
| chapado, sem volume | sombra lateral + brilho (§2, passo 3) |
| ícone não diz nada do bloco | remova; ilustração sem relação não entra |
| tudo da mesma cor | cor de convenção da área + interior mais claro que a parede |
| rótulos dentro do desenho, apertados | números + legenda HTML |
| figura pequena num canto | bloco de largura total, figura ≥ 50% da folha |

Ficou boa e é reutilizável? Sugira ao usuário levá-la para a biblioteca
(`assets/ilustracoes.svg`, regras no `design.md` §4).
