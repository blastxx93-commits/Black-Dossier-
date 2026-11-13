# Canal de arte em francês — regras de produção

Conversa com o dono em português; todo o conteúdo do canal em **francês**. Só a estrutura e o estilo de edição vêm da referência:
temas, títulos e textos são sempre próprios.

## Identidade (a confirmar pelo dono)
- Nome do canal: **Regardez Mieux** (@RegardezMieux, livre em 13/11/2026). Voz Fish em francês: `8143ff09113b48d0a75dd3fa025821e4`.
- Promessa: "Un tableau, regardé de près. Vous ne le verrez plus de la même façon."
- Foco: obras expostas na França e pintores franceses, mais os grandes clássicos europeus com ângulo novo.

## Vídeo
- 8–11 min, 1.250–1.550 palavras (~150 palavras/min), 1 obra por vídeo.
- Ritmo de publicação: **1 vídeo por dia** (decisão do dono).
- Estrutura fixa do roteiro:
  1. **Accroche** (até 40 s): obra, autor, ano em 1 frase; "à première vue... mais"; 3–4 promessas concretas; "vous ne la verrez plus de la même façon".
  2. **Ce que l'on voit**: tamanho real; depois figura por figura, guiando o olhar ("regardez", "remontez", "suivez").
  3. **La vraie histoire / le contexte**.
  4. CTA curto de inscrição logo depois de um gancho (~45–50%).
  5. **Comment le peintre a travaillé**.
  6. **Les détails qui changent tout** (numerados).
  7. **La vie du tableau** (donos, escândalos, museu).
  8. **Le dernier secret** (restauração, raio X, ciência) + resposta à pergunta do gancho + CTA final com pergunta para comentários.
- Fatos conferidos em fonte; frase atribuída leva "on raconte que", leitura de historiador leva "selon"/"beaucoup d'historiens".
- Nada de "a IA descobriu", maldições ou afirmações sem fonte.

## Edição (`engine/art_render.py`)
- Imagem principal com pelo menos 3.840 px de largura (Commons; `agent/fetch_commons.py` baixa e grava os créditos).
- Só dois planos: `detail` (recorte em tela cheia com movimento lento) e `card` (imagem inteira sobre fundo escuro desfocado).
- 4–6 s por plano; o recorte mostra exatamente o que a frase descreve; o zoom termina no detalhe citado.
- Abrir e fechar com a obra inteira em `card`; voltar a ela a cada mudança de bloco.
- `card` para tudo que não é a obra: retrato do pintor, esboços, mapas, outras obras, documentos.
- Sem texto na tela, sem tela preta, sem IA, sem filtro de cor (só vinheta leve). Dissolve de 0,35 s.
- Trilha instrumental baixa e contínua (-24 dB sob a voz).
- Só domínio público, CC0, CC BY ou CC BY-SA; créditos em `credits.json` e na descrição.

## Título
- Até ~60 caracteres, sem o nome da obra; pergunta ou paradoxo + número (anos, tamanho, preço) quando houver.
- Nome do pintor só se for dos muito buscados (Van Gogh, Léonard de Vinci, Monet, Picasso).
- 3 opções por vídeo para o teste A/B; nunca tradução de título de outro canal.

## Thumbnail
- Recorte fechado da própria pintura, sem texto: um rosto, um gesto ou o detalhe prometido no título. 2 recortes por vídeo para A/B.

## Publicação
- Descrição: 2 frases de gancho, perguntas que o vídeo responde, ficha da obra (título, autor, data, museu), créditos das imagens, fontes.
- Idioma do vídeo: francês; dublagem automática ligada; marcar "conteúdo alterado" só se houver imagem sintética (não há).

## Pauta inicial (nenhuma destas está no canal de referência)
1. Le Radeau de la Méduse — Géricault (Louvre) · piloto em `episodes/art-fr01-radeau`
2. La Liberté guidant le peuple — Delacroix (Louvre): o que a restauração de 2024 mudou
3. Le Sacre de Napoléon — David (Louvre): quem está no quadro e não estava lá
4. Un enterrement à Ornans — Courbet (Orsay)
5. Le Tricheur à l'as de carreau — Georges de La Tour (Louvre)
6. Les Noces de Cana — Véronèse (Louvre): o maior quadro do museu, cortado ao meio por Napoleão
7. Le Verrou — Fragonard (Louvre)
8. L'Angélus — Millet (Orsay): o que Dalí viu e o raio X confirmou
9. Le Serment du Jeu de paume — David: o quadro que nunca foi terminado
10. Impression, soleil levant — Monet (Marmottan): a hora exata da pintura
11. La Mort de Marat — David
12. Les Raboteurs de parquet — Caillebotte (Orsay)

## Fluxo de um episódio
1. `episodes/<ep>/narration/ch00_hook.txt … chNN.txt` (um arquivo por bloco) e `images.json` (títulos no Commons).
2. `python3 agent/fetch_commons.py <ep>` baixa as imagens e grava `credits.json` (pode rodar de novo: pula as já baixadas).
3. GitHub → Actions → **Gerar narração** → episódio, `voice` = ID da voz francesa, `lang` = `fr`.
4. `edit/plan.json`: planos por capítulo, cada um com `cue` = primeiras palavras da frase que ele ilustra.
5. `python3 engine/art_build.py <ep> --assets <pasta do episódio no branch assets>` gera `edit/episode.json` com os tempos reais
   (sem `--assets`, estima os tempos pelo texto para uma prévia muda).
6. `python3 engine/art_render.py episodes/<ep>/edit/episode.json` renderiza em 1080p (`--preview` = 720p).
