# Abaixo de Zero (canal Antártida) — regras e identidade

Canal brasileiro de documentários sobre a Antártica: mistérios, montanhas, gelo, animais, história e curiosidades.
Referência de estilo: "Por que é impossível explorar a Amazônia profunda" (canal Kairus) — explicativo, calmo, cheio de mapas.
O Claude cuida de temas, roteiro, narração e edição; o dono só dá o aval em cada etapa.

## Decisões do dono (07/11/2026)
- Nome do canal: **Abaixo de Zero**
- Voz: **B — "Meu narrador"** (Fish Audio, id `c9d3da0bdf61417d929dc67966e4befe`), velocidade 1.0
- ant01, título: **Por Que Os Cientistas Temem o Que Existe Sob a Antártida**

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

## Roteiro (pedido do dono, 07/11/2026)
- Roteiro de alta qualidade, **hook forte e impactante** (número ou cena que choca nos primeiros segundos, 2–3 perguntas abertas,
  promessa da maior revelação, que só é paga no fim).
- **CTA na metade** (logo depois de um cliffhanger, ~50%) e **CTA no final**.
- **O CTA final nunca chama outro vídeo** ("no próximo vídeo…", "até o próximo…"): pergunta para os comentários + like/inscrição + agradecimento.
- A voz é escolhida depois do roteiro pronto (teste com o hook final).

## Edição (pedido do dono, 07/11/2026 — estilo do vídeo de referência do Kairus)
- **Imagens e clipes de alta qualidade**, buscados pelo Claude nos bancos livres (NASA SVS/Images, NOAA, USAP/NSF, BAS, USGS,
  Wikimedia Commons, Internet Archive). Mínimo 1080p para clipes e ~1600 px para fotos; descartar imagem borrada, com marca d'água ou texto.
- **Descartar tudo que não tem a ver com o tema** (pedido do dono): toda foto, clipe e cena de IA passa pela revisão das folhas de contato;
  só o que está em `edit/reviewed.json` pode entrar no vídeo (o resto é bloqueado automaticamente).
- **Nada se repete**: nenhuma foto, clipe ou cena de IA duas vezes no mesmo vídeo (checagem automática por conteúdo bloqueia a montagem).
- **Trilha (ant01):** 5 faixas enviadas pelo dono, geradas no Suno (`edit/musica/`), em loop com emendas suaves; mistério usa a faixa de drama
  e frio usa a reflexiva. Uso comercial de música do Suno depende do plano pago do dono na época da geração.
- **Trilha sonora de qualidade e sem risco de direitos autorais**: preferência pela Biblioteca de Áudio do YouTube ("atribuição não obrigatória",
  baixada pelo dono, 1 faixa por clima em `edit/musica/<clima>.mp3`). Kevin MacLeod (CC BY) só como reserva: é legal, mas às vezes gera
  reivindicação falsa de Content ID. Baixa sob a voz.
- **Troca de trilha nos momentos de tensão**, como no vídeo de referência: a música muda junto com o clima da cena
  (ambiente/maravilhamento → tensão → mistério → épico), com transição suave entre faixas. Plano por capítulo em `episodes/<ep>/edit/musica.txt`.
- **Movimento em todas as imagens**, reais ou de IA: zoom lento, pan, parallax; nada parado.
- **Transições diferenciadas** entre as cenas (corte seco, dissolve, zoom, slide, whip, wipe de gelo/neve, flash branco), variando sempre.
- **Nunca tela preta** em nenhum momento: cartelas e gráficos aparecem sobre a cena anterior desfocada/escurecida ou sobre fundo animado de gelo.
- **Layouts de destaque** nos momentos importantes: número gigante (ex.: "3.769 m"), comparação lado a lado (Antártida x Brasil),
  ficha do lugar (nome, profundidade, ano da descoberta), mapa com marcador, linha do tempo, citação em tela.
- Mapas e gráficos animados como assinatura: globo girando até a Antártida, mapa do continente com rótulos, corte do gelo
  (perfil de radar), linha do tempo geológica.
- Cenas de IA (Flux) só onde não há imagem real: interior dos lagos subglaciais, florestas de 90 milhões de anos, dinossauros, montanhas sob o gelo.
- Ritmo 3–6 s por plano, primeiro minuto 2,5–4 s.
- Paleta fria: azul-gelo (#8FD3FF), branco (#F2F6F8), azul-noite (#0A1A2A) e laranja de destaque (#FF7A1A) para números e alertas.
  Tipografia Inter. **Sem legendas gravadas no vídeo** (pedido do dono, 07/11/2026); o .srt pode ir só para o YouTube, se o dono quiser.
- Som: efeitos discretos (vento, gelo rangendo, sonar), silêncio curto antes das revelações.

## Títulos
- Fórmulas: "Por Que É Impossível [X] na Antártica" · "O Que Existe Debaixo do Gelo da Antártica" · "O [Coisa] Que [Paradoxo]".
- Até ~70 caracteres, termo mais buscado no começo (ver agente Palavras-chave com idioma pt e país br). 3 opções para teste A/B.

## Thumbnails
- **O dono faz as thumbnails** (07/11/2026). O Claude entrega sugestões de texto (2–4 palavras, complementando o título, sem repeti-lo)
  e de imagem de fundo para cada vídeo.

## Pauta (atualizada em 07/11/2026, ordem sugerida)
1. ant01 — Por Que Os Cientistas Temem o Que Existe Sob a Antártida (lagos, montanhas, cachoeira de sangue, Thwaites) — **em produção**
2. ant02 — Por que ninguém pode ir para a Antártida (tratado, regras, Rogozov, 2048) — **roteiro pronto, aguardando aval**
3. Os animais que sobrevivem no lugar mais frio da Terra (peixe de sangue transparente, foca-de-weddell, pinguim-imperador, tardígrados)
4. O navio Endurance: achado 107 anos depois a 3 mil metros de profundidade (Shackleton)
5. O que aconteceria se todo o gelo da Antártida derretesse (e o mapa do Brasil depois disso)
6. A Corrida ao Polo Sul: Amundsen x Scott (a vitória e a tragédia)
7. Monte Erebus: o vulcão de lava sob o gelo que solta poeira de ouro
8. Quem é o dono da Antártida? Os 7 países que reivindicam o continente
9. O Brasil na Antártida: a estação que pegou fogo e renasceu
10. Como é passar um inverno inteiro na Antártida (6 meses de noite)
11. Os mitos da Antártida: o que é verdade e o que é teoria da conspiração (Operação Highjump, "base nazista", "muralha de gelo")
12. O iceberg gigante A23a: o maior do mundo, preso por 30 anos e à deriva
13. A Geleira do Juízo Final (Thwaites) por dentro
14. Os Vales Secos: o lugar sem neve onde a NASA treina para Marte
15. A anomalia de Wilkes Land: existe uma cratera gigante sob o gelo?

## Produção (mesmos agentes do repositório, branch deste canal)
- Episódios em `episodes/antNN-<tema>/` com o arquivo `lang` = `pt` (transcrição em português).
- Voz: workflow "Gerar narração" com `voice_test=pt` narra o hook com as vozes PT mais usadas da Fish → dono escolhe.
- Palavras-chave: workflow "Palavras-chave" com `lang=pt`, `country=br`.
