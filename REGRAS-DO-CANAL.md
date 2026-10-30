# Black Dossier — Regras do canal (valem a partir do EP03)

Definidas pelo dono do canal em 27/10/2026. O Claude segue estas regras em todo episódio.

## 0. Episódios independentes e retenção
- Os antigos EP01 (Apalachin) e EP02 (Valachi) **não serão publicados**. O canal começa no caso Bonanno = **FILE 001**.
- Cada vídeo é independente: nada de "no último episódio", "o homem do nosso último arquivo" ou gancho para o próximo tema.
- Foco total em retenção:
  - hook começa no meio da ação (o momento mais forte), sem biografia;
  - 2–3 perguntas abertas no hook, pagas ao longo do vídeo (a maior reviravolta é prometida no hook e entregue no fim);
  - toda virada de capítulo termina com um mini-gancho;
  - frases curtas e contexto comprimido;
  - CTA no meio do vídeo (logo após um gancho/cliffhanger) e no final.
- **Duração: ~20 minutos a partir do FILE 002** (roteiro de ~3.300–3.400 palavras; a voz da Fish fala ~170 palavras/min, medido no FILE 002). O FILE 001 (Bonanno) fica com ~14 min.

## 1. Imagens e vídeos: nada repetido
- Nenhuma imagem, clipe ou cena de IA aparece duas vezes no mesmo vídeo (nem com outro corte ou zoom).
- A montagem é bloqueada automaticamente se houver repetição (`engine/edit_kit.py` verifica antes de gerar o vídeo).
- Para cobrir ~16–18 min sem repetir: mais fotos reais e clipes de arquivo por episódio, cartelas de texto (datas, citações, números) e
  1 cena de IA por momento que não tem foto. Custo de IA sobe para ~20–30 imagens (~US$1,20–1,80 por episódio), mais ~US$0,06 da thumbnail ilustrada.

## 2. CTA no meio e no final (atualizado 28/10/2026)
- **Nada de CTA logo depois do hook.**
- **No meio do vídeo** (~50%): logo depois de um cliffhanger de fim de capítulo, curto (~10 s), prometendo a resposta.
  Modelo: "One second before the answer. If this file has you hooked, subscribe and turn on notifications. It's free, and it keeps these investigations coming. Now, ..."
- **No final**: pergunta para os comentários + CTA de inscrição.
- Na tela: cartela "SUBSCRIBE" no estilo do canal durante o CTA.

## 3. Texto sem repetição de palavras
- O roteiro passa por `engine/script_check.py` antes de ir para a narração: aponta palavras e expressões repetidas demais,
  frases que começam igual em sequência e muletas ("And", "But", "that", "really"…).
- Nomes próprios podem repetir quando necessário, mas alternando com pronomes e apelidos ("the boss", "the soldier").

## 4. Títulos
- Virais e de curiosidade: prometem um segredo, um paradoxo ou um choque, sem mentir sobre o conteúdo.
- **Nome de personagem só se for famoso de verdade** (que as pessoas pesquisam): Al Capone, Lucky Luciano, John Gotti,
  Bugsy Siegel, Frank Sinatra, JFK, "O Poderoso Chefão"/Don Corleone etc. Nomes desconhecidos (Valachi, Bonanno, Croswell)
  ficam fora do título e vão para a descrição e as tags.
- Até ~60 caracteres; sempre 3 opções para teste A/B.
- Exemplos: "The Mafia Boss Who Vanished for 19 Months" · "The Man Who Told the FBI Everything" · "Why the Mafia Feared This Prison Kiss".

## 5. Thumbnails: sempre 2 por episódio, para teste A/B
Cada episódio sai com **duas** thumbnails em estilos diferentes, para o teste A/B do YouTube ("Testar e comparar").

**A — Ilustrada (estilo quadrinho)** · `engine/thumbnail_comic.py`
- Ilustração gerada pelo agente de IA: mafioso **fictício** à esquerda (terno risca de giz, chapéu, gravata vermelha),
  cenário de época à direita (Nova York, Little Italy, carros antigos), céu claro e cores vivas.
- Título grande em serifa preta no céu, à direita: 1 palavra forte + datas/ano (ex.: "MAFIA / 1891 – 1992").
- Nunca rosto de pessoa real nem de personagem de filme (Don Corleone, etc.): o personagem é inventado e representa a época.
- Prompt com `"guard": "fictional"` e `"raw": false` no ai_prompts.json (1 imagem, ~US$0,06).

**B — Realista (dossiê sépia)** · `engine/thumbnail.py`
- Foto real de arquivo em sépia à direita, painel escuro à esquerda.
- Até 4 palavras: linha 1 branca, linha 2 **amarela** (#E5C428), faixa vermelha, rodapé com ano/lugar em máquina de escrever.
- Topo "BLACK DOSSIER · FILE 00X" em vermelho, carimbo no canto inferior direito. Nunca texto em cima do rosto.

As duas contam a mesma promessa do título, cada uma do seu jeito.

## 6. Palavras-chave com demanda
- Antes de fechar título, descrição e tags, o agente `Palavras-chave` (GitHub) puxa as sugestões de busca do YouTube
  para o tema (o que as pessoas realmente digitam). Título, primeiras linhas da descrição e tags usam os termos mais buscados.
- Tags: 15–20, misturando termos amplos (mafia documentary, true crime) e específicos com demanda.

## Canal Austrália (branch canal-australia)
- Só assuntos de 2026 e atualidade; dados com fonte e data. Pauta automática: workflow "Pauta (canal Austrália)".
- Hook impactante nos primeiros 30–60 s (número/fato real que choca), CTA no meio e no fim.
- A partir do vídeo 3: no mínimo 15 minutos de narração. Voz nunca é acelerada/desacelerada (speed 1.0).
- Voz padrão: Fish Audio, voz A (1178e1b397ac47d5966842d3f1fe1019). Trilha a -29 dB sob a voz.
- Edição: sem imagens repetidas (checagem por conteúdo), sem tela preta, nada estático, transições dinâmicas,
  cada plano preso à palavra da narração, meta de ~40% de clipes entre o material de imagem.
- Ao publicar: marcar "conteúdo alterado ou sintético" quando houver cena realista feita por IA.

### Títulos (padrão a partir do vídeo 4, inspirado em canais de notícias automotivas)
- Fórmula: [Marca/assunto] Just [VERBO FORTE] in Australia — [consequência ou reação]!
  Ex.: "Tesla Just CANCELLED the Cybertruck for Australia — 7 Years of Deposits Refunded!"
- Outras formas que funcionam: "[Número] [coisa] in Australia — [consequência]"; "X Owners Waited MONTHS… — Here's What X Just Did".
- 1 a 2 palavras em CAIXA ALTA (o verbo ou o número), travessão no meio, 60–90 caracteres, termina com "!" quando couber.
- Palavras de impacto: JUST, CAUGHT, CANCELLED, AXED, RECALLED, PLUNGED, SLASHED, SHOCKED, DISASTER, SERIOUS TROUBLE.
- Regra de ouro: o fato do título tem que ser verdadeiro e aparecer no vídeo com fonte. Nada de "fechou todas as lojas",
  "PERMANENTLY CLOSED" ou incêndio que não aconteceu (risco de strike, desmonetização e processo).
- Thumbnail: fundo com mais contraste e leve desfoque; persona masculina fictícia (IA) com a expressão do tema; texto curto.
