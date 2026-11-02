# Canal Espanha — Regras do canal (clássicos dos anos 50, em espanhol)

Definidas em 02/11/2026. O Claude cuida do canal (pauta, roteiro, imagens, narração, edição, título, descrição e thumbnail);
o dono só dá o aval antes de gastar créditos e antes de publicar.
Usa o mesmo motor e os mesmos agentes do canal Austrália (`engine/render_aus.py`, `engine/aus_kit.py`, workflows do GitHub).

## Comunicação
- Falar com o dono **sempre em português**.
- Conteúdo do canal (roteiro, narração, legendas, títulos, descrição, tags) em **espanhol da Espanha**:
  "coche" (nunca "carro"/"auto"), "coche patrulla", "salpicadero", "maletero", tratamento por "tú".
- Pastas dos episódios: `episodes/esNN-<tema>/`, sempre com `lang.txt` = `es`
  (a transcrição, os rótulos da tela, como FUENTE e SUSCRÍBETE, e a descrição saem em espanhol por causa desse arquivo).

## 0. Formato (baseado na análise do canal de referência, 02/11/2026)
- Formato principal: **lista numerada em contagem regressiva** ("Los 12 coches MÁS … de los años 50").
  Formato secundário: **história de um carro só**, mas só quando houver reviravolta forte (morte, fracasso, escândalo).
- Década-âncora: **anos 50**. Ângulos que funcionam: perigo, absurdo, velocidade, polícia/viaturas.
  Ângulos fracos: "fracassados", "estranhos", "luxuosos" (só com reviravolta forte).
- Toda lista tem **pelo menos 2 carros espanhóis ou fabricados na Espanha** (SEAT 600, Biscúter, Pegaso, Dauphine FASA,
  Renault 4CV "Pelotilla", carros da Guardia Civil etc.). É o diferencial contra os canais latino-americanos.
- Duração: **17–22 min** (roteiro de ~2.800–3.400 palavras). Vídeos de 27–28 min renderam pouco no canal de referência.
- Ritmo de publicação: 2 vídeos por semana quando a produção estabilizar.

## 1. Roteiro e retenção
- Hook nos primeiros 30–60 s começando no momento mais forte, com 2–3 perguntas abertas.
  O número 1 é prometido no hook e só revelado no fim, com a maior reviravolta.
- Cada capítulo termina com um mini-gancho para o próximo número.
- CTA curto no meio (~50%) com pergunta para os comentários ("¿cuál fue el primer coche de tu familia?") e CTA no final.
- Afirmações disputadas sempre com ressalva ("según…", "hay quien dice…"). Números com fonte.
- Nada de inventar mortes, processos ou recalls. O fato do título tem que estar no vídeo.

## 2. Imagens, clipes e edição
- Fotos reais dos modelos: Wikimedia Commons / Openverse / Library of Congress (só domínio público, CC0, CC BY, CC BY-SA).
- Clipes: cinejornais e filmes de época em domínio público (Prelinger, Universal Newsreels), nunca filme de ficção.
- Cenas de IA (Flux) onde não houver foto: estilo "fotografia documental anos 50, Kodachrome, grão".
  Nunca rosto reconhecível de pessoa real (James Dean, pilotos etc. só em foto livre real ou de costas/silhueta).
- **Tragédias (Le Mans 1955, acidente de James Dean): nunca imagem do acidente, de vítimas ou de destroços com pessoas.**
  Só o carro, a pista, a arquibancada antes, ou cena de IA simbólica.
- Mesmas regras de edição do canal Austrália: abre com imagem de carro, sem tela preta, nada repetido (checagem por conteúdo),
  nada parado, cada corte preso à frase da narração, ~40–55% de clipes, legendas amarelas, trilha a -29 dB.
- Cartela de número ("rank") em cada item da lista, com foto do modelo.

## 3. Voz
- Fish Audio, voz masculina de narrador **com sotaque da Espanha** (a voz A do canal Austrália é inglesa; não serve).
  O ID da voz fica no input "voice" do workflow "Gerar narração" até virar segredo próprio. Velocidade 1.0.

## 4. Títulos e thumbnail
- Fórmula: "Los [N] Coches MÁS [ADJETIVO] de los Años 50" / "[N] Coches de los Años 50 Que HOY Estarían PROHIBIDOS".
- 1–2 palavras em CAIXA ALTA, até ~70 caracteres, sempre 3 opções para o teste A/B.
- Evitar o rabicho "No Vas a Creer Que Existieron" até testar (no canal de referência os vídeos com ele foram os mais fracos).
- Thumbnail: o carro mais forte da lista em destaque, fundo com contraste, 2–4 palavras grandes, ano ("AÑOS 50").

## 5. Aval do dono (pontos de parada)
1. Pauta + roteiro (antes de gastar com voz e IA).
2. Vídeo pronto + título/thumbnail (antes de publicar).
