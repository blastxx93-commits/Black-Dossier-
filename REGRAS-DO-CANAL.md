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
  - CTA depois do hook curto (~6 s).

## 1. Imagens e vídeos: nada repetido
- Nenhuma imagem, clipe ou cena de IA aparece duas vezes no mesmo vídeo (nem com outro corte ou zoom).
- A montagem é bloqueada automaticamente se houver repetição (`engine/edit_kit.py` verifica antes de gerar o vídeo).
- Para cobrir ~16–18 min sem repetir: mais fotos reais e clipes de arquivo por episódio, cartelas de texto (datas, citações, números) e
  1 cena de IA por momento que não tem foto. Custo de IA sobe para ~20–30 imagens (~US$1,20–1,80 por episódio), mais ~US$0,06 da thumbnail ilustrada.

## 2. CTA depois do hook e no final
- **Depois do hook** (antes do capítulo 1), uma frase curta, ~8–10 s, sem quebrar o clima. Modelo:
  "Before we open this file: if you're into the real stories behind the American Mafia, subscribe and turn on notifications. Black Dossier releases a new file every week."
- **No final**: CTA de inscrição + pergunta para os comentários + gancho do próximo episódio.
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
