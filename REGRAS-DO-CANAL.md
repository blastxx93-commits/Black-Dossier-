# Black Dossier — Regras do canal (valem a partir do EP03)

Definidas pelo dono do canal em 27/10/2026. O Claude segue estas regras em todo episódio.

## 1. Imagens e vídeos: nada repetido
- Nenhuma imagem, clipe ou cena de IA aparece duas vezes no mesmo vídeo (nem com outro corte ou zoom).
- A montagem é bloqueada automaticamente se houver repetição (`engine/edit_kit.py` verifica antes de gerar o vídeo).
- Para cobrir ~16–18 min sem repetir: mais fotos reais e clipes de arquivo por episódio, cartelas de texto (datas, citações, números) e
  1 cena de IA por momento que não tem foto. Custo de IA sobe para ~20–30 imagens (~US$1,20–1,80 por episódio).

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

## 5. Thumbnail: padrão fixo do canal (`engine/thumbnail.py`)
- 1280×720, foto ou cena em preto e branco/sépia ocupando a direita, painel escuro à esquerda.
- Texto em 2 linhas, no máximo 4 palavras: linha 1 branca, linha 2 **amarela** (#E5C428), fonte grossa.
- Faixa vermelha embaixo do texto, rodapé com o ano/lugar em fonte de máquina de escrever.
- Topo: "BLACK DOSSIER · FILE 00X" em vermelho. Carimbo vermelho no canto inferior direito.
- Sempre um rosto ou objeto forte do lado direito; nunca texto em cima do rosto.

## 6. Palavras-chave com demanda
- Antes de fechar título, descrição e tags, o agente `Palavras-chave` (GitHub) puxa as sugestões de busca do YouTube
  para o tema (o que as pessoas realmente digitam). Título, primeiras linhas da descrição e tags usam os termos mais buscados.
- Tags: 15–20, misturando termos amplos (mafia documentary, true crime) e específicos com demanda.
