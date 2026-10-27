# Black Dossier — fluxo de produção

Canal: Black Dossier (@BlackDossiermf). Idioma: inglês. Duração padrão: ~20 min (~2.900–3.000 palavras a ~145 wpm).
Narração: gerada pelo dono do canal no ElevenLabs e enviada ao Claude. Edição: motor próprio (`engine/render.py`).

## Estrutura do repositório
```
engine/
  render.py            motor de edição (episode.json -> MP4)
  test_episode.json    exemplo de episódio com todos os tipos de plano
episodes/
  ep01-apalachin/      roteiro de narração do EP01
```
Áudios, imagens e vídeos renderizados não entram no Git (ver `.gitignore`).

## Etapas de cada episódio
1. Pesquisa — fatos checados em fontes, listadas no fim do roteiro.
2. Roteiro — hook nos primeiros 30–55 s, open loops a cada capítulo, teaser do próximo episódio no final.
3. Narração — dono gera no ElevenLabs, de preferência 1 arquivo por capítulo (hook = capítulo 0).
4. Edição — cada capítulo tem lista de planos; o tempo das imagens se ajusta sozinho à duração do áudio.
5. Entrega — MP4 1080p, -14 LUFS, + thumbnail, título, descrição, tags e capítulos.

## Como renderizar
```
pip install pillow        # + ffmpeg instalado no sistema
python3 engine/render.py episodes/ep01-apalachin/episode.json --preview   # 960x540 rápido
python3 engine/render.py episodes/ep01-apalachin/episode.json             # 1080p final
```

## Agente de imagens (nuvem)
Busca imagens livres para cada plano do roteiro em Wikimedia Commons, Library of Congress e Openverse.
Só aceita domínio público, CC0, CC BY e CC BY-SA (nada de NC/ND), com mínimo de 800 px.

1. Os planos de cada episódio ficam em `episodes/<ep>/shots.json` (id, busca, buscas alternativas, quantidade).
2. Pelo celular: GitHub → repositório → **Actions** → **Agente de imagens** → **Run workflow** → nome da pasta do episódio.
   Para refazer só alguns planos, preencha "only" com os ids separados por vírgula.
3. O resultado vai para o branch **assets**, pasta do episódio: imagens por plano, `contact_sheet_*.jpg`
   (miniaturas numeradas para escolher), `credits.csv` (licença e autor de cada arquivo) e `report.md`.
4. Escolha pela folha de contato (ex.: "hoover_portrait 2") e o Claude monta a edição com essas.

Planos sem resultado aparecem no relatório: esses viram imagem gerada por IA ou arquivo enviado por você.

## Agente de narração (Fish Audio)
Gera a voz de cada capítulo a partir de `episodes/<ep>/narration/*.txt` e já transcreve palavra por palavra.
GitHub → Actions → **Gerar narração** → Run workflow → pasta do episódio. Resultado no branch `assets`:
`narration_audio/*.flac` (edição), `audio/*.mp3` e `words/*.words.json` (sincronia).
Segredos: `FISH_API_KEY`, `FISH_VOICE_ID`. Opcional (variável): `FISH_MODEL` (padrão `s2.1-pro`).

## Agente de imagens IA (Replicate / Flux)
Gera as cenas sem foto livre a partir de `episodes/<ep>/ai_prompts.json` (prompt por plano + estilo do canal).
GitHub → Actions → **Gerar imagens IA** → Run workflow. Resultado: `ai/<plano>_<n>.jpg` + `ai_contact_sheet_*.jpg`.
Padrão: Flux 1.1 Pro Ultra, 16:9 (~2752x1536), 2 opções por plano. Pula planos que já têm imagem.
Regra: nunca rosto reconhecível de pessoa real (o agente reforça isso em todo prompt).
Segredo: `REPLICATE_API_TOKEN`.

## O que enviar para editar
- Áudios da narração (MP3/WAV), nomeados ch00_hook, ch01 … ch08.
- Imagens: domínio público (Library of Congress, FBI Vault, NARA, Wikimedia Commons) ou geradas por IA. Nomeie pelo plano do roteiro (ex.: farm_dusk.jpg).
- Música e efeitos com licença (Biblioteca de Áudio do YouTube serve).
- Opcional: fontes .ttf da marca (Special Elite, Bebas Neue) em `engine/fonts/`.

## Regras de segurança (YouTube)
- Nunca foto real de cena de crime ou corpo; nada de sangue ou arma apontada para a câmera.
- Afirmações disputadas sempre com ressalva ("reportedly", "never proven").
- Jornais e memorandos recriados com nome fictício e etiqueta "DRAMATIZATION".
- Marcar "conteúdo alterado ou sintético" no upload quando houver imagem realista feita por IA de pessoa ou evento real.

## Tipos de plano do motor
black, image (Ken Burns: in/out/left/right/up/down, legenda), typewriter, statement, title, chapter,
dossier (foto + ficha + carimbo), counter, document (memorando "dramatization"), timeline, video.
Grade padrão: contraste 1.08, saturação 0.72, grão 9, vinheta. Música abaixa sozinha quando a voz fala.
