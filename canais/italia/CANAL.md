# Canal Itália — formato "dossiê de museu"

Modelo: vídeo "As balas mais cruéis da história e por que foram proibidas" (100 Anos Luz).
Idioma: italiano. Duração: SEMPRE entre 10 e 15 min (roteiro de ~1.850–2.400 palavras; Fish ~170 wpm). Alvo padrão: ~11–12 min.

## Narração
Fish Audio, voz italiana: `b60329816f6f4f04bf7555fe2354c468`.
Actions → Gerar narração → campo "voice" com o ID acima.

## Estrutura do roteiro
1. Gancho 60 s: frase-definição → número chocante → descrição física → pergunta moral.
2. 8–12 itens em escalada (~40 s cada): título falado → mecanismo → efeito no corpo → contexto/tratado → ponte.
3. Callback ao início + frase-resumo + CTA de uma linha.

## Estilo visual
Fundo branco; título do bloco em caixa-alta no topo + subtítulo (data/local/fonte);
1–3 imagens centrais; lower-thirds pretos; palavra-impacto verde grossa no canto inferior esquerdo (~1/min);
cartões de documento bege com carimbo; troca de visual a cada ~5 s.
Thumb (feita pelo dono): fundo branco, texto vermelho caixa-alta, colagem de recortes.

## Controle de qualidade da narração (sempre)
Todo capítulo gerado passa por `agent/audio_qa.py`:
1. Limpeza: corte de ronco/chiado, redução de ruído, redução de eco/reverberação entre palavras, de-esser, nivelamento e limitador (sem clipping).
2. Escuta automática (Whisper) e comparação palavra por palavra com o roteiro: palavra pulada, acrescentada, trocada ou embolada,
   gagueira (frase repetida), silêncio morto > 1,6 s, velocidade fora de 120–205 wpm, clipping, início ou fim cortado.
3. Capítulo reprovado é regerado automaticamente (até 3 tentativas) e fica a melhor versão.
4. Relatório em `qa_narracao.md` (branch assets) e no resumo da execução. Se algo continuar com defeito, o workflow falha e avisa.
Workflow: Actions → Gerar narração → lang = `it`, voice = ID acima.

## Imagens e cartões (regra do dono, a partir do IT02)
- Muita imagem: alvo de ~110–130 telas por vídeo de 9 min, quase todas fotos, pinturas, gravuras ou clipes de arquivo.
- Cartões de documento: no máximo ~1 por minuto (≈ 8–10 por vídeo) e nunca dois seguidos.
  Usar só para tratado, número-chave ou citação; o resto vira imagem com etiqueta preta.
- Escolher temas com muito material visual livre (pinturas, gravuras, fotos de arquivo) e rodar o agente de imagens
  com ~50 buscas (em inglês e italiano) logo no início, antes de montar a edição.
- Sem IA por enquanto (Replicate sem saldo).
