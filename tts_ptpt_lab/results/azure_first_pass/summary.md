# KS-835 Azure pt-PT TTS: azure_first_pass

2026-10-09T11:40:52 | region westeurope | SDK 1.52.0 | 3042 characters | judge the 16 kHz files (production hub rate)

Time to first audio = request sent on a warm connection -> first audio chunk.

| Voice | Kind | Status | TTFA median ms | TTFA max ms | Errors |
|---|---|---|---|---|---|
| pt-PT-RaquelNeural | native pt-PT neural | GA | 442.0 | 591 | 0 |
| pt-PT-FernandaNeural | native pt-PT neural | GA | 210.5 | 489 | 0 |
| pt-PT-Harper:MAI-Voice-2.1 | native pt-PT HD (MAI) | Preview | 879.5 | 1305 | 0 |
| pt-PT-Harper:MAI-Voice-2.1-Flash | native pt-PT fast (MAI) | Preview | 427.0 | 788 | 0 |
| en-US-Ava:DragonHDLatestNeural | multilingual HD speaking pt-PT | GA | 277.0 | 597 | 0 |
| pt-BR-Thalita:DragonHDLatestNeural | Brazilian HD speaking pt-PT | GA | 316.5 | 693 | 0 |

## Lines

- **greeting** (opening line, name, "Detetámos"): Olá, Manuel, fala a Vega. Detetámos uma possível queda. Está bem?
- **alert** (mandated alert phrase, brand name): Estou a enviar um alerta no sistema SeniorMatics. Estou aqui consigo.
- **no_response** (mandated no-response phrase): Não consegui falar consigo, por isso estou a avisar os seus cuidadores.
- **clarify** (question intonation, short words): Desculpe, não percebi. Como é que se sente? Magoou-se, ou consegue levantar-se?
- **reminder** (long sentence, numbers, time, name): Ainda bem que está tudo bem, Maria. Lembre-se de tomar os dois comprimidos às oito e meia da noite, e se precisar de alguma coisa, estou aqui.
- **azores** (place name, digits read aloud): Hoje em Ponta Delgada estão 19 graus, e amanhã à tarde pode chover em São Miguel.
