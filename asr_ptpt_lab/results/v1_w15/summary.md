# KS-834 pt-PT ASR eval: v1_w15

2026-10-08T15:10:23 | Azure pt-PT | 8 kHz hub path | realtime=False | boost weight=1.5 (20 phrases)

Help heard as SAFE is the dangerous error (a fall answered as 'I'm fine').

## By speaker and boost list

| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | Safe heard as help | Empty | Errors |
|---|---|---|---|---|---|---|---|---|---|
| tts_pt-PT-DuarteNeural / boost off | 150 | 7.3% | 6.3% | 91/97 (94%) | 3 | **0** | 1 | 2 | 0 |
| tts_pt-PT-DuarteNeural / boost on | 150 | 6.4% | 5.7% | 94/97 (97%) | 1 | **0** | 0 | 0 | 0 |
| tts_pt-PT-RaquelNeural / boost off | 150 | 8.0% | 7.0% | 91/97 (94%) | 2 | **0** | 0 | 1 | 0 |
| tts_pt-PT-RaquelNeural / boost on | 150 | 7.8% | 7.4% | 93/97 (96%) | 1 | **0** | 0 | 1 | 0 |

## By category (all speakers)

| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | Safe heard as help | Empty | Errors |
|---|---|---|---|---|---|---|---|---|---|
| azorean / boost off | 30 | 24.2% | 14.8% | 21/26 (81%) | 1 | **0** | 1 | 0 | 0 |
| azorean / boost on | 30 | 28.1% | 23.4% | 23/26 (88%) | 1 | **0** | 0 | 0 | 0 |
| everyday / boost off | 80 | 2.6% | 2.3% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| everyday / boost on | 80 | 2.6% | 2.3% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| help / boost off | 70 | 10.3% | 10.3% | 66/70 (94%) | 4 | **0** | 0 | 2 | 0 |
| help / boost on | 70 | 6.3% | 6.3% | 69/70 (99%) | 1 | **0** | 0 | 0 | 0 |
| hesitation / boost off | 20 | 15.0% | 15.0% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| hesitation / boost on | 20 | 15.0% | 15.0% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| no / boost off | 20 | 0.0% | 0.0% | 20/20 (100%) | 0 | **0** | 0 | 0 | 0 |
| no / boost on | 20 | 0.0% | 0.0% | 20/20 (100%) | 0 | **0** | 0 | 0 | 0 |
| safe / boost off | 60 | 4.0% | 4.0% | 56/58 (97%) | 0 | **0** | 0 | 0 | 0 |
| safe / boost on | 60 | 4.0% | 4.0% | 56/58 (97%) | 0 | **0** | 0 | 0 | 0 |
| yes / boost off | 20 | 5.0% | 5.0% | 19/20 (95%) | 0 | **0** | 0 | 1 | 0 |
| yes / boost on | 20 | 5.0% | 5.0% | 19/20 (95%) | 0 | **0** | 0 | 1 | 0 |

## Key-answer intent errors

- `tts_pt-PT-DuarteNeural/a002` boost off: expected **safe**, got help — said “Nã, nã me magoei nada.”, heard “Na Na me magoei nada.”
- `tts_pt-PT-DuarteNeural/a006` boost off: expected **help**, got other — said “Nã consigo, nã consigo levantar.”, heard “Nem consigo nem consigo levantar.”
- `tts_pt-PT-DuarteNeural/a006` boost on: expected **help**, got other — said “Nã consigo, nã consigo levantar.”, heard “Nem consigo nem consigo levantar.”
- `tts_pt-PT-DuarteNeural/a007` boost off: expected **no**, got other — said “Nã, nã.”, heard “Na Na.”
- `tts_pt-PT-DuarteNeural/a007` boost on: expected **no**, got other — said “Nã, nã.”, heard “Na Na.”
- `tts_pt-PT-DuarteNeural/h005` boost off: expected **help**, got other — said “Caí.”, heard “”
- `tts_pt-PT-DuarteNeural/h018` boost off: expected **help**, got other — said “Magoei-me.”, heard “”
- `tts_pt-PT-DuarteNeural/s026` boost off: expected **safe**, got other — said “Não me aleijei.”, heard “Não me elejei.”
- `tts_pt-PT-DuarteNeural/s026` boost on: expected **safe**, got other — said “Não me aleijei.”, heard “Não me elejei.”
- `tts_pt-PT-RaquelNeural/a002` boost off: expected **safe**, got other — said “Nã, nã me magoei nada.”, heard “Na Na maguinada.”
- `tts_pt-PT-RaquelNeural/a002` boost on: expected **safe**, got other — said “Nã, nã me magoei nada.”, heard “Na Na maguinada.”
- `tts_pt-PT-RaquelNeural/a007` boost off: expected **no**, got other — said “Nã, nã.”, heard “Na Na.”
- `tts_pt-PT-RaquelNeural/h005` boost off: expected **help**, got other — said “Caí.”, heard “K í.”
- `tts_pt-PT-RaquelNeural/h005` boost on: expected **help**, got other — said “Caí.”, heard “K í.”
- `tts_pt-PT-RaquelNeural/h030` boost off: expected **help**, got other — said “Caí, mas acho que não é nada.”, heard “QI, mas acho que não é nada.”
- `tts_pt-PT-RaquelNeural/s006` boost off: expected **safe**, got other — said “Não caí.”, heard “Não QI.”
- `tts_pt-PT-RaquelNeural/s006` boost on: expected **safe**, got other — said “Não caí.”, heard “Não QI.”
- `tts_pt-PT-RaquelNeural/y003` boost off: expected **yes**, got other — said “Pois.”, heard “”
- `tts_pt-PT-RaquelNeural/y003` boost on: expected **yes**, got other — said “Pois.”, heard “”

## Worst transcriptions (WER ≥ 0.5)

- `tts_pt-PT-RaquelNeural/h005` boost off WER 2.00: “Caí.” → “K í.”
- `tts_pt-PT-RaquelNeural/h005` boost on WER 2.00: “Caí.” → “K í.”
- `tts_pt-PT-DuarteNeural/a007` boost off WER 1.00: “Nã, nã.” → “Na Na.”
- `tts_pt-PT-DuarteNeural/a007` boost on WER 1.00: “Nã, nã.” → “Na Na.”
- `tts_pt-PT-DuarteNeural/h005` boost off WER 1.00: “Caí.” → “”
- `tts_pt-PT-DuarteNeural/h018` boost off WER 1.00: “Magoei-me.” → “”
- `tts_pt-PT-RaquelNeural/a002` boost off WER 1.00: “Nã, nã me magoei nada.” → “Na Na maguinada.”
- `tts_pt-PT-RaquelNeural/a002` boost on WER 1.00: “Nã, nã me magoei nada.” → “Na Na maguinada.”
- `tts_pt-PT-RaquelNeural/a007` boost off WER 1.00: “Nã, nã.” → “Na Na.”
- `tts_pt-PT-RaquelNeural/y003` boost off WER 1.00: “Pois.” → “”
- `tts_pt-PT-RaquelNeural/y003` boost on WER 1.00: “Pois.” → “”
- `tts_pt-PT-DuarteNeural/a001` boost on WER 0.50: “Tou bem, tou bem.” → “Estou bem, estou bem.”
- `tts_pt-PT-DuarteNeural/a003` boost off WER 0.50: “Atão, tá tudo bem.” → “Então, está tudo bem?”
- `tts_pt-PT-DuarteNeural/a003` boost on WER 0.50: “Atão, tá tudo bem.” → “Então, está tudo bem?”
- `tts_pt-PT-DuarteNeural/e034` boost off WER 0.50: “Já vou deitar-me.” → “Já vou deitarme.”
- `tts_pt-PT-DuarteNeural/e034` boost on WER 0.50: “Já vou deitar-me.” → “Já vou deitarme.”
- `tts_pt-PT-DuarteNeural/h022` boost off WER 0.50: “Tenho tonturas.” → “Tem tonturas.”
- `tts_pt-PT-DuarteNeural/h022` boost on WER 0.50: “Tenho tonturas.” → “Tem tonturas.”
- `tts_pt-PT-DuarteNeural/h034` boost off WER 0.50: “Ai, caí, que dores.” → “AKI que dores.”
- `tts_pt-PT-DuarteNeural/h034` boost on WER 0.50: “Ai, caí, que dores.” → “AKI que dores.”
- `tts_pt-PT-DuarteNeural/u006` boost off WER 0.50: “Quem? Eu?” → “Ok eu.”
- `tts_pt-PT-DuarteNeural/u006` boost on WER 0.50: “Quem? Eu?” → “Ok eu.”
- `tts_pt-PT-DuarteNeural/u007` boost off WER 0.50: “Ah, é a Vega.” → “A é Vega.”
- `tts_pt-PT-DuarteNeural/u007` boost on WER 0.50: “Ah, é a Vega.” → “A é Vega.”
- `tts_pt-PT-RaquelNeural/a001` boost on WER 0.50: “Tou bem, tou bem.” → “Estou bem, estou bem.”
- `tts_pt-PT-RaquelNeural/a003` boost on WER 0.50: “Atão, tá tudo bem.” → “Então, está tudo bem?”
- `tts_pt-PT-RaquelNeural/a007` boost on WER 0.50: “Nã, nã.” → “Nã Nã Nã.”
- `tts_pt-PT-RaquelNeural/h034` boost off WER 0.50: “Ai, caí, que dores.” → “AEQI que dores.”
- `tts_pt-PT-RaquelNeural/s006` boost off WER 0.50: “Não caí.” → “Não QI.”
- `tts_pt-PT-RaquelNeural/s006` boost on WER 0.50: “Não caí.” → “Não QI.”
- `tts_pt-PT-RaquelNeural/u006` boost off WER 0.50: “Quem? Eu?” → “Ok eu.”
- `tts_pt-PT-RaquelNeural/u006` boost on WER 0.50: “Quem? Eu?” → “Ok eu.”
- `tts_pt-PT-RaquelNeural/u007` boost off WER 0.50: “Ah, é a Vega.” → “A é Vega.”
- `tts_pt-PT-RaquelNeural/u007` boost on WER 0.50: “Ah, é a Vega.” → “A é Vega.”
