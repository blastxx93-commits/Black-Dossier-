# Canal Antártica — regras e identidade (proposta de 07/11/2026, aguardando aval do dono)

Canal brasileiro de documentários sobre a Antártica: mistérios, montanhas, gelo, animais, história e curiosidades.
Referência de estilo: "Por que é impossível explorar a Amazônia profunda" (canal Kairus) — explicativo, calmo, cheio de mapas.
O Claude cuida de temas, roteiro, narração e edição; o dono só dá o aval em cada etapa.

## Nome (escolher 1)
- **Continente Gelado** (sugestão principal) · Abaixo de Zero · Terra Austral

## Formato
- Idioma: **português do Brasil** (roteiro, narração, legendas, título, descrição). Conversa com o dono também em português.
- Duração: **~25 min** (roteiro de ~4.000–4.200 palavras; medir a velocidade real da voz no teste e ajustar).
- Episódios independentes, sem "no último vídeo".
- Estrutura: hook em ação (data, lugar, fato que choca) em 45–60 s com 2–3 perguntas abertas → capítulos curtos que
  terminam com mini-gancho → CTA no meio (~50%, logo após um cliffhanger) → grande reviravolta no fim → pergunta nos comentários.
- Sempre que possível, comparar escalas com o Brasil (área do Brasil, Paraná, Pão de Açúcar, Pico da Neblina) e trazer o Brasil
  para a história (PROANTAR, Estação Comandante Ferraz, litoral brasileiro).
- Números grandes por extenso no texto da narração (a voz lê melhor); anos em algarismos.
- Fatos com fonte (lista no fim do roteiro); hipóteses e polêmicas sempre com ressalva ("segundo as estimativas", "nunca foi provado").
  Mistério sim, desinformação não: nada de "pirâmides", "base nazista" ou "entrada para a Terra oca" apresentados como verdade.

## Edição (estilo Kairus adaptado)
- Imagens reais em primeiro lugar: NASA (Scientific Visualization Studio, Landsat, MODIS), NOAA, USAP/NSF, British Antarctic Survey,
  Wikimedia Commons (domínio público / CC BY / CC BY-SA). Clipes de drone, satélite e expedições históricas (Scott, Shackleton, Byrd).
- Mapas e gráficos animados como assinatura: globo girando até a Antártica, mapa do continente com rótulos, corte do gelo
  (perfil de radar), comparação de tamanho com o Brasil, linha do tempo geológica.
- Cenas de IA (Flux) só onde não há imagem real: lagos subglaciais, florestas de 90 milhões de anos, dinossauros, interior das montanhas.
- Ritmo 3–6 s por plano, primeiro minuto 2,5–4 s; nada estático (zoom/pan lento), nada de tela preta, nada repetido.
- Paleta fria: azul-gelo (#8FD3FF), branco (#F2F6F8), azul-noite (#0A1A2A) e laranja de destaque (#FF7A1A) para números e alertas.
  Tipografia Inter. Legendas brancas com contorno escuro (ou amarelas, a decidir) gravadas + .srt.
- Som: trilha ambiente/cinemática baixa (-29 dB sob a voz), vento e gelo rangendo como efeitos discretos, silêncio curto antes das revelações.

## Títulos
- Fórmulas: "Por Que É Impossível [X] na Antártica" · "O Que Existe Debaixo do Gelo da Antártica" · "O [Coisa] Que [Paradoxo]".
- Até ~70 caracteres, termo mais buscado no começo (ver agente Palavras-chave com idioma pt e país br). 3 opções para teste A/B.

## Thumbnails (2 por vídeo, teste A/B)
- A: imagem real ou IA impactante do tema (ex.: corte do gelo com o lago embaixo), 2–4 palavras grandes, uma em laranja.
- B: mapa/globo estilizado da Antártica com seta ou destaque + pergunta curta.

## Pauta inicial (ordem sugerida)
1. O que existe debaixo do gelo da Antártica (lagos, montanhas, cachoeira de sangue) — **ant01, roteiro pronto**
2. Por que é (quase) proibido ir para a Antártica — Tratado Antártico, quem pode ir e como
3. Os animais que sobrevivem no lugar mais frio da Terra (peixe de sangue transparente, foca-de-weddell, pinguim-imperador)
4. O navio Endurance: achado 107 anos depois a 3 mil metros de profundidade
5. O que aconteceria se todo o gelo da Antártica derretesse (e o que muda no litoral do Brasil)
6. Monte Erebus: o vulcão de lava sob o gelo que solta poeira de ouro
7. A Geleira do Juízo Final (Thwaites) por dentro
8. Quem é o dono da Antártica? Os 7 países que reivindicam o continente
9. O Brasil na Antártica: a estação que pegou fogo e renasceu
10. Como é passar um inverno inteiro na Antártica (6 meses de noite)
11. Os mitos da Antártica: o que é verdade e o que é teoria da conspiração
12. A Corrida ao Polo Sul: Amundsen x Scott

## Produção (mesmos agentes do repositório, branch deste canal)
- Episódios em `episodes/antNN-<tema>/` com o arquivo `lang` = `pt` (transcrição em português).
- Voz: workflow "Gerar narração" com `voice_test=pt` narra o hook com as vozes PT mais usadas da Fish → dono escolhe.
- Palavras-chave: workflow "Palavras-chave" com `lang=pt`, `country=br`.
