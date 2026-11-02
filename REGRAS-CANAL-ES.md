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
- Década-âncora: **anos 50**. Ângulos que funcionam: perigo, absurdo, velocidade, polícia/viaturas.
  Ângulos fracos: "fracassados", "estranhos", "luxuosos" (só com reviravolta forte).
- Toda lista tem **pelo menos 2 carros espanhóis ou fabricados na Espanha** (SEAT 600, Biscúter, Pegaso, Dauphine FASA,
  Renault 4CV "Pelotilla", carros da Guardia Civil etc.).
- Estrutura do roteiro: abertura com a cena mais forte da lista → itens do 12 ao 1, cada um com o carro, o contexto da época e
  o motivo concreto (o "porquê") → o número 1 é o mais surpreendente → fecho com pergunta para os comentários e pedido de inscrição.
  Sem CTA no meio do vídeo.
- Duração: **17–22 min** (~2.800–3.400 palavras). Vídeos de 27–28 min renderam pouco no canal de referência.
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

## 4. Imagens e segurança
- Fotos reais: Wikimedia Commons / Openverse / Library of Congress (só domínio público, CC0, CC BY, CC BY-SA).
- Clipes: cinejornais e filmes de época em domínio público (Prelinger, Universal Newsreels), nunca filme de ficção.
- Cenas de IA (Flux): estilo "fotografia documental anos 50, Kodachrome, grão". Nunca rosto reconhecível de pessoa real.
- **Tragédias (Le Mans 1955, acidente de James Dean): nunca imagem do acidente, de vítimas ou de destroços com pessoas.**
- Marcar "conteúdo alterado ou sintético" no upload quando houver cena realista feita por IA.

## 5. Voz
- Voz masculina de narrador **com sotaque da Espanha** (Fish Audio ou ElevenLabs). Velocidade 1.0.

## 6. Títulos e thumbnail (próprios do canal)
- Fórmula: "Los [N] Coches MÁS [ADJETIVO] de los Años 50" / "[N] Coches de los Años 50 Que HOY Estarían PROHIBIDOS".
- 1–2 palavras em CAIXA ALTA, até ~70 caracteres, sempre 3 opções para o teste A/B.
- Evitar o rabicho "No Vas a Creer Que Existieron" até testar.
- Thumbnail: o carro mais forte da lista em destaque, em foto de época, 2–4 palavras grandes + "AÑOS 50".
  Sem persona/apresentador.

## 7. Aval do dono (pontos de parada)
1. Pauta + roteiro (antes de gastar com voz e IA).
2. Vídeo pronto + título/thumbnail (antes de publicar).
