# Black Dossier — Regras do canal

Definidas pelo dono do canal (27–29/10/2026). O Claude segue estas regras em todo episódio.

## Comunicação
- Falar com o dono **sempre em português**, inclusive nas anotações entre uma etapa e outra.
- Conteúdo do canal (roteiro, narração, legendas, títulos, descrição) em **inglês**.
- O Claude escolhe sozinho as imagens e os clipes; mostra o hook antes de narrar quando houver mudança grande de formato.

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

## 1. Imagens e vídeos: nada repetido, nada de tela preta
- **Nunca tela preta**, nem como pausa dramática. Onde faltar imagem ou houver pausa, **preencher com imagem gerada por IA**.
  A montagem é bloqueada se aparecer um plano preto, e os cartões de texto aparecem sobre a cena anterior escurecida.
- **Mesclar clipes de vídeo com imagens** (fotos reais + cenas de IA): clipes nos momentos de movimento, sem precisar usar todos.
  Clipes vêm de cinejornais e filmes de época em domínio público (Universal Newsreels, Prelinger), nunca de filmes de ficção.
- **Ritmo**: ~3–5 s por plano; primeiro minuto com cortes rápidos (2,5–4 s); evitar a mesma tela parada por mais de ~8 s.
- **1 imagem de IA por cena** (economia). Sem rosto de pessoa real gerado por IA: pessoas reais sem foto livre aparecem como
  silhueta no dossiê; documentos encenados levam o carimbo "DRAMATIZATION". Sem cenas de violência gráfica ou vítimas.
- Conferir toda imagem gerada: descartar e regerar as que tiverem texto inventado/errado, rosto de pessoa real ou objeto fora de época.
- Nenhuma imagem, clipe ou cena de IA aparece duas vezes no mesmo vídeo (nem com outro corte ou zoom).
- A montagem é bloqueada automaticamente se houver repetição (`engine/edit_kit.py` verifica antes de gerar o vídeo).
- Para cobrir ~20 min sem repetir e com cortes rápidos são necessárias ~80–100 cenas de IA (~US$5–6 por episódio no Flux 1.1 Pro Ultra),
  além das fotos reais e clipes de arquivo. Manter saldo no Replicate antes de começar.

## 1b. Som, legendas e edição
- Trilha sonora **baixa**, sem atrapalhar a narração (abaixa sozinha quando a voz entra).
- Efeitos de transição **discretos**, com volume baixo.
- Cenas **sincronizadas com a narração**: cada corte ancorado na frase que ele ilustra.
- **Legendas amarelas**, estilo documentário de TV, tamanho moderado, gravadas no vídeo (+ arquivo .srt para o YouTube).
- Entregar sempre: versão para celular (leve) e versão 1080p para o YouTube.

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
- Foto real de arquivo (ou objeto forte, como o chapéu caído) em sépia à direita, **com destaque e bem visível**, painel escuro à esquerda.
- Até 4 palavras: linha 1 branca, linha 2 **amarela** (#E5C428), faixa vermelha, rodapé com ano/lugar em máquina de escrever.
- Topo "BLACK DOSSIER · FILE 00X" em vermelho, carimbo no canto inferior direito. Nunca texto em cima do rosto.

As duas contam a mesma promessa do título, cada uma do seu jeito.

## 6. Palavras-chave com demanda
- Antes de fechar título, descrição e tags, o agente `Palavras-chave` (GitHub) puxa as sugestões de busca do YouTube
  para o tema (o que as pessoas realmente digitam). Título, primeiras linhas da descrição e tags usam os termos mais buscados.
- Tags: 15–20, misturando termos amplos (mafia documentary, true crime) e específicos com demanda.
