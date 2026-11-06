# Canal República Tcheca — história de armas (dobra do Iron Armory)

Criado em 06/11/2026. Referência: **Iron Armory** (@ironarmoryyt), analisado em `canal-tcheco/ANALISE-IRON-ARMORY.md`.
O Claude cuida do canal (pauta, roteiro, imagens, narração, gráficos, edição, título, descrição e thumbnail);
o dono dá o aval antes de gastar créditos grandes (voz do episódio inteiro + cenas de IA) e antes de publicar.

## 1. Comunicação e idioma
- Falar com o dono **sempre em português**.
- Conteúdo do canal (roteiro, narração, legendas, títulos, descrição, tags) em **tcheco**.
- Pastas: `episodes/czNN-<tema>/`, sempre com `lang.txt` = `cs` (transcrição e rótulos da tela em tcheco).
- **Números sempre por extenso na narração** ("devatenáct set padesát osm", "vzor padesát osm"):
  no teste de voz, a Fish leu "1958" em inglês e "58" em sueco. Nos gráficos (HyperFrames) os números ficam em algarismos.

## 2. Conteúdo
- Formato do canal de referência: **documentário de uma arma só**, com pergunta/reviravolta no título
  ("Por que X...", "O que aconteceu com X depois da guerra", "X não foi feito para Y — foi feito para algo pior").
- **Ângulo tcheco** (o que a dobra acrescenta): metade dos vídeos sobre armas tchecas/tchecoslovacas
  (vz. 58, CZ 75, ZB vz. 26/Bren, Škorpion, vz. 52, Sa 23, BREN, ouriço tcheco, armas de 1948 para Israel, a "píšťala" hussita),
  metade sobre lendas mundiais que já provaram demanda no canal de referência (Dragunov, FAMAS, MP40, StG 44, MG42, PKM),
  sempre com uma ponte para a história tcheca quando ela existir de verdade.
- Estrutura: hook no meio da ação com 2–3 perguntas abertas → contexto curto → engenharia (o "por dentro") →
  serviço e história → legado/hoje → resposta prometida no hook. CTA curto no meio (logo após um cliffhanger) e no fim
  (pergunta para os comentários + inscrição).
- Duração: **~20 min**. A voz Fish fala ~122 palavras/min em tcheco → roteiro de **~2.300–2.500 palavras**.
- Fatos com fonte; afirmações disputadas com ressalva ("podle dostupných zpráv", "historici zmiňují").

## 3. Segurança (política de armas do YouTube)
- Só história, engenharia e contexto. **Nada de instrução** de fabricação, conversão para automático, modificação, compra ou venda;
  nenhum link de loja ou fabricante na descrição.
- Sem violência gráfica, sem vítimas; tragédias (1968 etc.) contadas com respeito, sem imagem de mortos.
- Cenas de IA: nunca rosto reconhecível de pessoa real; marcar "conteúdo alterado ou sintético" no upload.

## 4. Edição (estilo do canal de referência + motor do canal Austrália/ES)
- Visual "pergaminho e blueprint": fundo de papel envelhecido, grade técnica, tinta preta, carimbo vermelho-ferrugem.
- **Material real é o principal do vídeo (pedido do dono, 06/11/2026):** banco de fotos e clipes primeiro
  (Wikimedia Commons / Openverse / LoC para fotos; cinejornais de domínio público + Pexels/Pixabay/Commons para clipes),
  com muitas buscas por tema. Meta de ~45% do tempo de imagem em clipes.
- **Cenas de IA só onde não houver foto ou clipe real que sirva**, geradas no **Replicate (Flux)** — o workflow
  "Gerar imagens IA" agora usa Replicate por padrão. Nas listas de montagem, a IA fica sempre por último em cada cena.
- **Gráficos HyperFrames só o essencial** (~3–5 por vídeo: mapa, ficha técnica, comparação, linha do tempo),
  gerados por `engine/hf_graphics.py` a partir de `episodes/<ep>/graphics.json`.
- Mesmo motor e regras de montagem dos outros canais: nunca tela preta, nada parado, nada repetido, cada corte preso à frase,
  legendas amarelas gravadas + .srt, trilha baixa (-29 dB), voz a 1.0, render paralelo no GitHub.

## 5. Voz
- Padrão: Fish Audio (voz do canal, `s2.1-pro`) — fala tcheco inteligível desde que os números venham por extenso.
- Alternativa em teste: ElevenLabs `eleven_multilingual_v2` (o plano atual não permite saída PCM; `agent/tts.py` agora cai para MP3).

## 6. Títulos e thumbnail
- Títulos em tcheco, curiosidade/paradoxo, até ~70 caracteres, 3 opções para teste A/B.
  Fórmulas da referência: "Proč X...", "Co se stalo s X po válce", "X nebyl postaven k Y — ale k něčemu horšímu".
- Thumbnail no estilo da referência: arma renderizada (foto real ou IA) sobre pergaminho com desenho técnico,
  2–3 palavras pretas enormes em fonte condensada (Anton), opcional medalhão/brasão. Ex.: "ODMÍTLI KALAŠNIKOV".

## 7. Aval do dono (pontos de parada)
1. Roteiro + voz de teste (antes de narrar o episódio inteiro e gerar ~60 cenas de IA, ~US$4).
2. Vídeo pronto + título/thumbnail (antes de publicar).
