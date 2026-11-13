# Canal de arte em francês — análise da referência e da demanda

Levantamento feito em 13/11/2026, direto nas páginas públicas do YouTube (sem vidIQ).
Referência: **Corvo Cósmico** (@corvo1618), vídeo "A Mulher Que Invadiu o Inferno: O Segredo de Margarida Louca".
Regra do dono: usar **só a estrutura e o estilo de edição**; nenhum vídeo, título ou roteiro do canal é copiado.

## 1. O canal de referência em números
- ~5 semanas de vida, 30 vídeos (1 por dia), 4,64 mil inscritos, ~914 mil visualizações no total.
- Duração: 8 a 10 min (o vídeo analisado tem 8:25 e 1.283 palavras, ~152 palavras/min).
- A audiência é muito concentrada: 4 vídeos somam ~763 mil views (83% do canal). A mediana é ~3,5 mil.
- Os 4 que estouraram usam a mesma fórmula de título: pergunta + número de anos, sem dizer o nome da obra
  ("Como alguém pintou ISSO há 600 anos?", "Como NINGUÉM percebeu ISSO por 130 anos?", "Você consegue achar o assassino nesta pintura?").
- Títulos com o nome da obra ou do pintor ficam quase sempre abaixo de 10 mil.
- Monetização própria: e-book de R$ 27,90 anunciado no meio (2:55) e no fim do vídeo.
- O vídeo tem faixa de áudio dublada em inglês (dublagem automática do YouTube), o que soma views de fora do Brasil.

## 2. Estrutura do roteiro (vídeo analisado)
| Tempo | Bloco | O que faz |
|---|---|---|
| 0:00–0:42 | Gancho | Nome da obra, autor e ano em 1 frase; "parece só X, mas..."; 4 promessas concretas em sequência; "no final você não vai mais ver ela do mesmo jeito". |
| 0:42–2:28 | O que se vê | Tamanho da obra; depois figura por figura, mandando o olhar ("olha", "repara", "agora chega perto"). Uma pergunta puxa a próxima ("Para onde?"). |
| 2:28–2:55 | Segundo foco | Novo detalhe estranho, deixado sem explicação (loop aberto). |
| 2:55–3:10 | CTA do produto | 15 s, logo depois do loop aberto. |
| 3:10–4:40 | Mais detalhes + contexto | Provérbio da época, comparação com outros pintores e obras. |
| 4:40–5:34 | Significado | "Mas afinal, o que significa?"; 2 ou 3 leituras de historiadores, com nomes; contexto histórico. |
| 5:34–6:30 | Vida da pintura | Donos, roubo, leilão, museu atual. |
| 6:30–7:20 | Último segredo | Restauração/ciência: 3 descobertas numeradas. |
| 7:20–8:25 | Fecho | Responde a pergunta do gancho, imagem final, CTA. |

Linguagem: frases curtas, segunda pessoa, verbos de olhar, sem jargão. Cada bloco termina prometendo o seguinte.

## 3. Estilo de edição (medido nos quadros do vídeo)
- **Uma única pintura em altíssima resolução** sustenta ~80% do vídeo.
- **Plano "detalhe"**: a pintura em tela cheia, recortada na figura de que a narração fala, com zoom ou pan lento. Troca a cada 4–6 s.
- **Plano "quadro"**: imagens de apoio (retrato do pintor, mapa, gravura, outra obra, a própria pintura inteira) aparecem inteiras,
  centralizadas, sobre fundo escuro e desfocado, com sombra e um empurrão lento.
- Sem texto na tela, sem legenda queimada, sem tela preta, sem b-roll de vídeo, sem IA. Cor fiel à obra.
- Trilha instrumental contínua e baixa; nenhuma vinheta.
- Thumbnail: recorte fechado da própria pintura (um rosto ou gesto forte), **sem texto**.
- Custo de produção quase zero: imagens em domínio público + narração.

`engine/art_render.py` reproduz esses dois planos (ver `REGRAS.md`).

## 4. Demanda na França
### Canais nativos em francês no mesmo formato
| Canal | Idade | Vídeos | Inscritos | Melhores vídeos | Vídeo típico |
|---|---|---|---|---|---|
| Art Assombri | ~8 meses | 30 | 2,86 mil | 103 mil, 67 mil, 51 mil, 42 mil, 38 mil, 38 mil | 1–15 mil |
| La Face Cachée de l'Art | ~6 semanas | 18 | 1,03 mil | 70 mil, 33 mil, 26 mil, 20 mil, 13 mil, 11 mil | 0,2–2 mil |
| Sous le Vernis | ~4 semanas | 27 | 365 | 86 mil, 4,6 mil | 100–700 |
| Une Fois Vu | ~10 dias | 7 | 200 | 69 mil, 10 mil | 100–500 |
| Le Dessous des Toiles | ~3 semanas | 11 | 80 | 7,9 mil, 3 mil | 150–700 |
| Au-delà du Tableau | ~1 semana | 6 | — | 12 | 0–12 |

Canais antigos de arte em francês (ex.: Scribe Accroupi, 39 mil inscritos) fazem visitas longas a exposições, com 4–13 mil views por vídeo:
público existe, mas o formato "segredo de uma pintura em 9 min" ainda não tem dono.

### Leitura
- **Tem demanda.** Canais franceses com menos de 1.000 inscritos já tiraram vídeos de 70–86 mil views em dias. O formato é puxado pela
  recomendação (home/sugeridos), não pela busca: quase ninguém digita o nome da obra.
- **Tem corrida.** Pelo menos 5 canais franceses idênticos nasceram nas últimas 6 semanas, todos traduzindo os mesmos títulos americanos
  ("Comment avons-nous pu passer à côté...", "Une fois que vous l'avez vu...") e as mesmas obras (Van Gogh, Última Ceia, Arnolfini).
- **O acerto é raro.** Em todos os canais, 1 em cada 4–6 vídeos estoura e o resto fica abaixo de 2 mil. Volume e constância contam.
- **Cuidado ao ler números:** Vuecrypte (47,8 mil inscritos, vídeos de 200–980 mil) e Decoded Art (1,2 milhão num vídeo) aparecem com título em
  francês, mas são canais em inglês com título traduzido e dublagem automática; essas views são mundiais, não francesas.
- Vídeos longos (20–38 min) do Sous le Vernis foram os piores; a faixa que funciona é 8–11 min.

### Onde dá para ganhar
1. **Obras que o francês conhece e pode visitar** (Louvre, Orsay, Orangerie, Versailles) e pintores franceses. Os clones só traduzem a pauta americana.
2. **Qualidade de imagem e de fatos**: vários concorrentes usam IA e afirmações inventadas ("a IA analisou a Ceia"); roteiro com fonte e ressalva dura mais.
3. **Título no molde que estoura** (pergunta + anos, sem nome da obra), mas com texto próprio.
4. **Dublagem automática ligada** desde o primeiro vídeo: a referência ganha views fora do país com ela.

Risco honesto: nicho novo e lotando rápido; não há garantia de que o algoritmo continue empurrando o formato daqui a 3 meses.
Sinal para medir: se em 15 vídeos nenhum passar de 10 mil, rever títulos/thumbnails antes de continuar.
