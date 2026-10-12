# KS-834 pt-PT ASR eval: v2_w20

2026-10-08T15:16:29 | Azure pt-PT | 8 kHz hub path | realtime=False | boost weight=2.0 (28 phrases)

Help heard as SAFE is the dangerous error (a fall answered as 'I'm fine').

## By speaker and boost list

| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | Safe heard as help | Empty | Errors |
|---|---|---|---|---|---|---|---|---|---|
| tts_pt-PT-DuarteNeural / boost on | 150 | 6.5% | 6.5% | 96/97 (99%) | 0 | **0** | 0 | 0 | 0 |
| tts_pt-PT-RaquelNeural / boost on | 150 | 9.6% | 9.5% | 94/97 (97%) | 1 | **0** | 0 | 0 | 0 |

## By category (all speakers)

| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | Safe heard as help | Empty | Errors |
|---|---|---|---|---|---|---|---|---|---|
| azorean / boost on | 30 | 34.4% | 34.4% | 25/26 (96%) | 0 | **0** | 0 | 0 | 0 |
| everyday / boost on | 80 | 2.6% | 2.3% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| help / boost on | 70 | 7.7% | 7.7% | 69/70 (99%) | 1 | **0** | 0 | 0 | 0 |
| hesitation / boost on | 20 | 15.0% | 15.0% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| no / boost on | 20 | 0.0% | 0.0% | 20/20 (100%) | 0 | **0** | 0 | 0 | 0 |
| safe / boost on | 60 | 4.0% | 4.0% | 56/58 (97%) | 0 | **0** | 0 | 0 | 0 |
| yes / boost on | 20 | 5.0% | 5.0% | 20/20 (100%) | 0 | **0** | 0 | 0 | 0 |

## Key-answer intent errors

- `tts_pt-PT-DuarteNeural/s026` boost on: expected **safe**, got other — said “Não me aleijei.”, heard “Não me elejei.”
- `tts_pt-PT-RaquelNeural/a002` boost on: expected **safe**, got other — said “Nã, nã me magoei nada.”, heard “Nã Nã Nã Nã, nã, nã maguinada.”
- `tts_pt-PT-RaquelNeural/h005` boost on: expected **help**, got other — said “Caí.”, heard “K í.”
- `tts_pt-PT-RaquelNeural/s006` boost on: expected **safe**, got other — said “Não caí.”, heard “Não QI.”

## Worst transcriptions (WER ≥ 0.5)

- `tts_pt-PT-RaquelNeural/a007` boost on WER 2.50: “Nã, nã.” → “Nã Nã Nã Nã, nã, nã, nã.”
- `tts_pt-PT-RaquelNeural/h005` boost on WER 2.00: “Caí.” → “K í.”
- `tts_pt-PT-RaquelNeural/a002` boost on WER 1.00: “Nã, nã me magoei nada.” → “Nã Nã Nã Nã, nã, nã maguinada.”
- `tts_pt-PT-RaquelNeural/y003` boost on WER 1.00: “Pois.” → “Pois pois.”
- `tts_pt-PT-DuarteNeural/a002` boost on WER 0.80: “Nã, nã me magoei nada.” → “Nã Nã Nã Nã, Nã, nã me magoei nada.”
- `tts_pt-PT-DuarteNeural/a001` boost on WER 0.50: “Tou bem, tou bem.” → “Estou bem, estou bem.”
- `tts_pt-PT-DuarteNeural/a003` boost on WER 0.50: “Atão, tá tudo bem.” → “Então, está tudo bem?”
- `tts_pt-PT-DuarteNeural/a007` boost on WER 0.50: “Nã, nã.” → “Nã Nã Nã.”
- `tts_pt-PT-DuarteNeural/e034` boost on WER 0.50: “Já vou deitar-me.” → “Já vou deitarme.”
- `tts_pt-PT-DuarteNeural/h022` boost on WER 0.50: “Tenho tonturas.” → “Tem tonturas.”
- `tts_pt-PT-DuarteNeural/h034` boost on WER 0.50: “Ai, caí, que dores.” → “AKI que dores.”
- `tts_pt-PT-DuarteNeural/u006` boost on WER 0.50: “Quem? Eu?” → “Ok eu.”
- `tts_pt-PT-DuarteNeural/u007` boost on WER 0.50: “Ah, é a Vega.” → “A é Vega.”
- `tts_pt-PT-RaquelNeural/a001` boost on WER 0.50: “Tou bem, tou bem.” → “Estou bem, estou bem.”
- `tts_pt-PT-RaquelNeural/a003` boost on WER 0.50: “Atão, tá tudo bem.” → “Então, está tudo bem?”
- `tts_pt-PT-RaquelNeural/h009` boost on WER 0.50: “Caí e não me consigo levantar.” → “QIE, não consigo levantar.”
- `tts_pt-PT-RaquelNeural/s006` boost on WER 0.50: “Não caí.” → “Não QI.”
- `tts_pt-PT-RaquelNeural/u006` boost on WER 0.50: “Quem? Eu?” → “Ok eu.”
- `tts_pt-PT-RaquelNeural/u007` boost on WER 0.50: “Ah, é a Vega.” → “A é Vega.”
