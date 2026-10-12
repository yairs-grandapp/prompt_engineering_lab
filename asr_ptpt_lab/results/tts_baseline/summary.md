# KS-834 pt-PT ASR eval: tts_baseline

2026-10-08T14:45:00 | Azure pt-PT | 8 kHz hub path | realtime=False

Help heard as SAFE is the dangerous error (a fall answered as 'I'm fine').

## By speaker and boost list

| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | Safe heard as help | Empty | Errors |
|---|---|---|---|---|---|---|---|---|---|
| tts_pt-PT-RaquelNeural / boost off | 150 | 8.0% | 7.0% | 91/97 (94%) | 2 | **0** | 0 | 1 | 0 |
| tts_pt-PT-RaquelNeural / boost on | 150 | 7.8% | 7.4% | 93/97 (96%) | 1 | **0** | 0 | 1 | 0 |

## By category (all speakers)

| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | Safe heard as help | Empty | Errors |
|---|---|---|---|---|---|---|---|---|---|
| azorean / boost off | 15 | 25.7% | 16.4% | 11/13 (85%) | 0 | **0** | 0 | 0 | 0 |
| azorean / boost on | 15 | 29.1% | 26.4% | 12/13 (92%) | 0 | **0** | 0 | 0 | 0 |
| everyday / boost off | 40 | 2.2% | 1.8% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| everyday / boost on | 40 | 2.2% | 1.8% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| help / boost off | 35 | 10.5% | 10.5% | 33/35 (94%) | 2 | **0** | 0 | 0 | 0 |
| help / boost on | 35 | 8.1% | 8.1% | 34/35 (97%) | 1 | **0** | 0 | 0 | 0 |
| hesitation / boost off | 10 | 13.3% | 13.3% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| hesitation / boost on | 10 | 13.3% | 13.3% | 0/0 (0%) | 0 | **0** | 0 | 0 | 0 |
| no / boost off | 10 | 0.0% | 0.0% | 10/10 (100%) | 0 | **0** | 0 | 0 | 0 |
| no / boost on | 10 | 0.0% | 0.0% | 10/10 (100%) | 0 | **0** | 0 | 0 | 0 |
| safe / boost off | 30 | 4.3% | 4.3% | 28/29 (97%) | 0 | **0** | 0 | 0 | 0 |
| safe / boost on | 30 | 4.3% | 4.3% | 28/29 (97%) | 0 | **0** | 0 | 0 | 0 |
| yes / boost off | 10 | 10.0% | 10.0% | 9/10 (90%) | 0 | **0** | 0 | 1 | 0 |
| yes / boost on | 10 | 10.0% | 10.0% | 9/10 (90%) | 0 | **0** | 0 | 1 | 0 |

## Key-answer intent errors

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
- `tts_pt-PT-RaquelNeural/a002` boost off WER 1.00: “Nã, nã me magoei nada.” → “Na Na maguinada.”
- `tts_pt-PT-RaquelNeural/a002` boost on WER 1.00: “Nã, nã me magoei nada.” → “Na Na maguinada.”
- `tts_pt-PT-RaquelNeural/a007` boost off WER 1.00: “Nã, nã.” → “Na Na.”
- `tts_pt-PT-RaquelNeural/y003` boost off WER 1.00: “Pois.” → “”
- `tts_pt-PT-RaquelNeural/y003` boost on WER 1.00: “Pois.” → “”
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
