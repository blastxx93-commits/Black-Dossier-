# Era das Feras: pacote gráfico "Dossiê Fóssil" (HyperFrames)

Usado a partir do fe04. As cartelas são composições do HyperFrames (HTML, CSS e GSAP), renderizadas uma vez por episódio pelo
`engine/hf_cards.py` e cortadas em um MP4 por cartela (`hf/<id>.mp4`). O renderizador do canal toca cada uma como um clipe.

Tipos de cartela: titulo, capitulo, rotulo (lower third sobre a cena), ficha, numero, mapa, linha (linha do tempo), comparar,
frase, escala, perguntas e cta. No build, use `F.hf(tipo, ...)`. `F.export_hf(ep, "edit/hf_cards.json")` grava as durações finais,
e o workflow render-aus renderiza as cartelas no job `cards`.

Fornecedores, todos vendorizados para o render não depender de CDN:
- GSAP 3.14.2: `vendor/gsap.min.js`.
- Mapa do Brasil: @svg-maps/brazil 2.0.0, licença CC BY 4.0, VictorCazanave/svg-maps (`vendor/brazil.json`).
- HyperFrames CLI 0.9.46, via npx no runner.
