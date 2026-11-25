# Canal Espanha — Regras do canal (clássicos dos anos 50, em espanhol)

Definidas em 02/11/2026. O Claude cuida do canal (pauta, roteiro, imagens, narração, edição, título, descrição e thumbnail);
o dono só dá o aval antes de gastar créditos e antes de publicar.

**Do canal Austrália vem SÓ o estilo de edição** (seção 3).
Estrutura de roteiro, tipo de pauta, fórmula de título, thumbnail e CTA **não** vêm de lá:
são próprios deste canal, baseados no nicho de clássicos (canal de referência analisado em 02/11/2026).

## 1. Comunicação e idioma
- Falar com o dono **sempre em português**.
- Conteúdo do canal (roteiro, narração, legendas, títulos, descrição, tags) em **espanhol da Espanha**:
  "coche" (nunca "carro"/"auto"), "salpicadero", "maletero", tratamento por "tú".
- Pastas dos episódios: `episodes/esNN-<tema>/`, sempre com `lang.txt` = `es`
  (a transcrição, os rótulos da tela, como FUENTE e SUSCRÍBETE, e a descrição saem em espanhol por causa desse arquivo).

## 2. Conteúdo (próprio do canal)
- Formato principal: **lista numerada em contagem regressiva** ("Los 12 coches MÁS … de los años 50").
  Formato secundário: **história de um carro só**, mas só quando houver reviravolta forte (morte do criador, fracasso, escândalo).
- **Época do canal: carros de 1950 a 1999** (anos 50 a 90; ampliada pelo dono em 19/11/2026, antes era só até 1979). Nada de antes de 1950, nem como item de lista
  (modelos lançados antes, como o Fusca, só entram pela versão fabricada nos anos 50–70).
  Começar pelos anos 50, que é o que mais rende no nicho; anos 60 e 70 entram depois, ou em listas próprias.
  Ângulos que funcionam: perigo, absurdo, velocidade, polícia/viaturas.
  Ângulos fracos: "fracassados", "estranhos", "luxuosos" (só com reviravolta forte).
- Toda lista tem **pelo menos 2 carros espanhóis ou fabricados na Espanha** (SEAT 600, Biscúter, Pegaso, Dauphine FASA,
  Renault 4CV "Pelotilla", carros da Guardia Civil etc.).
- Estrutura do roteiro: abertura com a cena mais forte da lista → itens do 12 ao 1, cada um com o carro, o contexto da época e
  o motivo concreto (o "porquê") → o número 1 é o mais surpreendente → fecho com pedido de inscrição.
- **CTAs (pedido do dono, 24/11/2026 — substitui a regra de 23/11)**:
  - **CTA aos ~3 minutos**: pergunta **de onde a pessoa está assistindo** ("¿Desde dónde nos estás viendo? Escríbelo en los comentarios" — **sem citar nomes de países**, pedido do dono 24/11) + pedido de inscrição.
  - **CTA final**: **agradece a quem ficou até o final**, pede inscrição de novo e pede **feedback** ("dime en los
    comentarios qué te ha parecido y qué tema quieres para el próximo vídeo").
- **Público (pedido do dono, 24/11/2026)**: aprofundar no público **latino — México, Colômbia e Argentina** — além da Espanha.
  Temas com carros e histórias desses países (ex.: VW Sedán/Vocho no México, Renault 4 e Simca na Colômbia, Ford Falcon,
  IKA/Torino e Fiat 600 "Fitito" na Argentina) e listas que misturem Espanha + América Latina.
- **CTR (pedido do dono, 24/11/2026)**: todo tema vem com 3–5 títulos fortes e 2–3 ideias de thumbnail chamativa
  (no máximo 3–4 palavras, contraste forte, um carro grande e reconhecível, um elemento de curiosidade: preço, "PROHIBIDO",
  seta, X vermelho, antes/depois).
- Duração: **mínimo 12 min** (pedido do dono, 25/11/2026 — ~2.300 palavras de narração; medido nos vídeos: ~185 palavras/min com as pausas).
  Se faltar fato com fonte para chegar lá, aumentar a lista (10 itens) ou aprofundar cada item — nunca inventar.
- **Temas de valor/preço (pedido do dono, 23/11/2026)**: só entram carros com preço real e citável (leilão, estimativa de casa
  de leilão ou anúncio datado). Carro sem preço encontrado fica fora da lista.
- Fatos com fonte; afirmações disputadas com ressalva ("según…", "hay quien dice…"). Nada de inventar mortes ou recalls.

## 3. Edição (herdada do canal Austrália)
Mesmo motor (`engine/render_aus.py`, `engine/aus_kit.py`) e mesmas regras de montagem:
- O vídeo abre sempre com imagem de carro; nunca tela preta; nada parado (Ken Burns e movimento em tudo).
- Nenhuma imagem, clipe ou cena de IA repetida (checagem por conteúdo); só material revisado na folha de contato.
- Cada corte preso à frase da narração; planos longos são divididos; transições dinâmicas e efeitos discretos.
- Mistura de fotos reais, clipes de arquivo e cenas de IA (meta de ~40–55% de clipes).
- Cartelas gráficas do motor: número do ranking com foto do modelo, números grandes, citações, perguntas.
- Legendas amarelas gravadas no vídeo + .srt; trilha sintetizada a -29 dB sob a voz; voz sempre a 1.0.
- Render paralelo no GitHub (workflow "Renderizar vídeo") com versão de entrega leve.

## 3b. Visual diferente a cada vídeo (pedido do dono, 09/11/2026)
- Cada episódio usa um **tema visual** de `engine/themes.py` (no build: `A.THEME = "..."`): cores das cartelas,
  fonte dos títulos, fundo dos gráficos, tratamento de cor do vídeo inteiro, cor da legenda e thumbnail (`--theme`).
- Temas: `clasico` (ep. 1–3), `retro60` (quente/anos 60), `noir_oro` (preto e dourado), `revista` (ciano/magenta),
  `periodico` (quase P&B, jornal). Nunca repetir o tema do episódio anterior; escolher o que combina com o assunto.

## 3c. Template Race (pedido do dono, 19/11/2026) — vale do es10 em diante
- Os vídeos passam a ser renderizados com o **template Race** em HyperFrames: `python3 engine/hf_race.py <workdir>`
  (estilo canal de corrida: cortes rápidos com chicote/flash, punch-in a cada ~2,4 s, linhas de velocidade, letra Anton inclinada,
  vermelho #e10600, cartela do número com impacto e tremor, chip de local/ano, HUD com a posição da lista).
- A montagem continua igual (build_esXX.py com aus_kit → episode.json); só o render final muda. es01–es09 ficam como estão.
- A rotação de temas da seção 3b deixa de valer para os vídeos novos (o template Race é o visual do canal).
- Movimento (20/11/2026): nada de "apresentação de slides". Cada foto troca de movimento a cada ~2,2 s (pan, tilt, push com
  rotação, pull-back, diagonal), algumas entram como "card" inclinado sobre a própria foto desfocada e outras viram tela dividida.
- Sempre carro na tela (20/11/2026): cartelas (números, frases, perguntas, título) aparecem POR CIMA de foto de carro em
  movimento e somem em ~3 s; nada de cartela sobre fundo preto. Planos curtos: MAX_HOLD ~6 s nos próximos vídeos, por isso
  pedir o dobro de fotos por carro na busca (n 16–20) e o máximo de clipes.
- **Primeiro minuto = clipes (20/11/2026):** o vídeo abre com clipes reais de arquivo (não fotos); o hook usa o máximo de clipes.
  Só propor temas que tenham boa quantidade de clipes reais, principalmente para o hook (checar a disponibilidade antes do roteiro).
- Temas diferenciados, fugindo do formato "lista de carros" de sempre; sempre trazer subtemas.
- Trilha: trocar a sintetizada por música real com licença livre (crédito do compositor na descrição) assim que a busca estiver pronta.

## 4. Imagens e segurança
- **Prioridade máxima para material real (pedido do dono, 02/11/2026):** fotos reais dos modelos e clipes de arquivo de época
  em primeiro lugar, buscando bastante (várias buscas por carro, muitas opções). Cena de IA **só** onde não houver foto ou
  clipe real que sirva — e só é gerada depois de revisar o material real, para tapar os buracos.
- Fotos reais: Wikimedia Commons / Openverse / Library of Congress (só domínio público, CC0, CC BY, CC BY-SA).
- Clipes: cinejornais e filmes de época em domínio público (Prelinger, Universal Newsreels), nunca filme de ficção.
- Cenas de IA (Flux): estilo "fotografia documental anos 50, Kodachrome, grão". Nunca rosto reconhecível de pessoa real.
- **Tragédias (Le Mans 1955, acidente de James Dean): nunca imagem do acidente, de vítimas ou de destroços com pessoas.**
- Marcar "conteúdo alterado ou sintético" no upload quando houver cena realista feita por IA.

## 5. Voz
- Voz masculina de narrador **com sotaque da Espanha** (Fish Audio ou ElevenLabs). Velocidade 1.0.
- **Checagem obrigatória da narração (pedido do dono, 19/11/2026):** antes de editar, rodar
  `python3 agent/check_narration.py <assets/ep> episodes/<ep>/narration` em toda narração. Ele aponta silêncios/ruído
  longos, fala embaralhada (trechos que não batem com o roteiro) e distorção. Capítulo com problema é gerado de novo
  (narrate.yml com `only`) até passar limpo. Nunca editar nem renderizar com narração reprovada.
- Escrever por extenso o que a voz pode ler errado: siglas e modelos com números (ex.: "2CV" → "Dos Caballos").

## 6. Títulos e thumbnail (próprios do canal)
- Fórmula: "Los [N] Coches MÁS [ADJETIVO] de los Años 50" / "[N] Coches de los Años 50 Que HOY Estarían PROHIBIDOS".
- 1–2 palavras em CAIXA ALTA, até ~70 caracteres, sempre 3 opções para o teste A/B.
- Evitar o rabicho "No Vas a Creer Que Existieron" até testar.
- Thumbnail: o carro mais forte da lista em destaque, em foto de época, 2–4 palavras grandes + "AÑOS 50".
  Sem persona/apresentador.

## 7. Aval do dono (pontos de parada)
1. Pauta + roteiro (antes de gastar com voz e IA).
2. Vídeo pronto + título/thumbnail (antes de publicar).

## Palavras-chave (25/11)
Todo pacote de publicação leva `publish/palavras_chave.txt`, montado com pesquisa no vidIQ: termos de alta procura com volume e concorrência, termos de nicho e as tags prontas para copiar e colar. Dar prioridade a termos com volume alto e concorrência baixa (ex.: autos clásicos, autos de colección, autos antiguos, historia de autos).

## Vocabulário: autos / carros / coches (25/11)
- Título, thumbnail e tags: usar "autos" (às vezes "carros"). É o termo com mais busca e o que o público latino usa.
- Narração: misturar. Usar "autos"/"carros" ao falar da América Latina e "coches" ao falar da Espanha.
- Tags: sempre incluir as três formas (autos, carros, coches) para captar todas as buscas.
