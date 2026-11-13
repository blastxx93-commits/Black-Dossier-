# Era das Feras (dobra em PT-BR do canal Mundo Fósil) — regras e identidade

Formato "o animal de hoje contra cada fera do passado": rodadas em escala crescente, veredito e placar.
Referência de edição: vídeo do tigre do Mundo Fósil (enviado pelo dono em 13/11/2026).

## Formato (pedido do dono, 13/11/2026)
- Português do Brasil. Vídeos de **12 a 15 min** (roteiro de ~1.900–2.200 palavras; a voz PT fala ~150 palavras/min).
- **Hook impactante** (cena/número que choca + 2–3 perguntas abertas + promessa paga só no fim) e **foco máximo em retenção**:
  rodadas curtas, cada uma termina com um gancho para a próxima, placar sempre na tela, reviravolta no final.
- CTA no meio (logo depois de um gancho, ~50%) e no final (pergunta para os comentários + like/inscrição). Nunca chamar "o próximo vídeo".
- Fatos com ressalva quando são estimativas ("estimativas de até…"); nada inventado.

## Edição (template `engine/render_feras.py` + `engine/feras_kit.py`)
- **Bem dinâmico**: plano médio ~3 s (2–4 s), nada parado (Ken Burns em toda foto), clipes 1080p mesclados com cenas de IA.
- Layouts do canal: etiqueta marfim com serifa (nome do animal), barra de medida ("200 kg"), cartela serifada sobre a cena desfocada,
  **cartela de rodada** (número + nome + 10 pontos de progresso), **VS em tela dividida**, **veredito** (cena vira preto e branco + carimbo),
  **placar** TIGRE × FERAS com o número virando, **ficha técnica**, **HUD** de rodada/placar no canto durante as lutas.
- Efeitos sonoros **baixos** (pedido do dono 13/11/2026: −9 dB no kit todo, transições −12 dB), só pontuando a cena.
- **Transições variadas** (fade, slide, punch, blur, zoom, whip, wipe, flash, mono) e **efeitos sonoros variados em cada transição**
  (4 whooshes diferentes, swipe, whip, impacto, reverse, obturador…), mais sons de assinatura: sino na rodada, impacto + rosnado no VS,
  batimento + obturador + carimbo no veredito, tiques + vitória/derrota no placar. Kit sintetizado: `engine/feras_audio.py` (sem direitos autorais).
- Trilha baixa sob a voz, trocando com o clima (tensão nas lutas, épico nas vitórias, drama no final).
- Nunca tela preta; nenhuma imagem/clipe repetido (checagem automática).

## Revisão obrigatória (pedido do dono, 13/11/2026)
- **Toda imagem de IA é revisada** antes de entrar: anatomia (patas, olhos, caudas, presas), texto/marca d'água, animal errado ou
  fora de época, artefatos. Reprovadas vão para `edit/skip.json` e são regeradas.
- **Narração revisada** capítulo por capítulo: transcrição x roteiro (palavras trocadas, sons estranhos), tom e silêncios (`qa_narracao.md`).
- Clipes: mínimo 1080p, sem marca d'água, só o animal certo.

## Economia no Replicate (pedido do dono, 13/11/2026)
- Meta: **~60–70 imagens de IA por vídeo** (o fe01 precisou de ~140 por falta de clipes).
- **Duas faixas de modelo** (`"tier"` no ai_prompts.json): `"hero"` = Flux 1.1 Pro Ultra (~US$0,06) só para o animal em destaque
  e os duelos; `"cheap"` = Flux Dev (mais barato), ampliado para 1080p, para paisagens, fundos, detalhes, pegadas, cavernas.
- **Mais clipes reais grátis** (Pixabay, Unsplash, Pexels se houver chave) antes de pedir cena de IA; buscas simples ("tiger", "wolf").
- Fundos das cartelas reaproveitam a cena desfocada (nenhuma imagem nova para cartela).
- Cada rodada usa as próprias imagens + as do tigre e da paisagem (o tigre aparece em todas as rodadas).
- Prompts revisados antes de gerar (anatomia descrita explicitamente) para reduzir regerações.
