# Abaixo de Zero — onde paramos (07/11/2026, pausado a pedido do dono)

## ant01 — Por Que Os Cientistas Temem o Que Existe Sob a Antártida — **RENDERIZADO (07/11, 26:34)**: branch render-ant01-sob-o-gelo

- Pronto: roteiro, narração (voz B, ~26 min, sem falhas), trilha (5 faixas do dono, edit/musica/), fotos/clipes/IA revisados
  (lista em edit/reviewed.json e edit/skip.json), edição em edit/build_ant01.py.
- Teste local da montagem: 309 planos; faltavam 31 (capítulos 8 e 9: "arquivo" e "thwaites").
- Em andamento ao pausar: geração de 33 cenas de IA (13 que falharam + 20 novas ai_y_*). Ao voltar:
  1. revisar ai_contact_sheet (cenas novas) e atualizar skip.json;
  2. rodar build_ant01.py na pasta de trabalho (a/ = assets do episódio, audio/ = narração) e conferir que não falta plano;
  3. salvar edit/episode.json e disparar "Renderizar vídeo (canal Austrália)" com episode=ant01-sob-o-gelo (usa render_ant.py);
  4. descrição com capítulos e créditos (fotos, clipes, trilha).
## ant02 — Por Que Ninguém Pode Ir Para a Antártida?
- Pronto: roteiro aprovado, narração (ch01 sendo regravado ao pausar), 88 fotos e 27 clipes aprovados, 18 cenas de IA aprovadas.
- Em andamento ao pausar: regeração de 18 cenas de IA. Falta: build_ant02.py (edição), mais material genérico, render.
