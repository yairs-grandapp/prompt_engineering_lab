# pt-PT ASR lab (KS-834)

Small tester for Microsoft Azure speech recognition in European Portuguese (pt-PT), for VEGA
(KS-832). Nothing here touches the app server: it reproduces the server's recognition path
(`picmeinserver/DddAsr/.../AsrEngineAzure.java`) on this machine.

What it mirrors from production:
- **8 kHz / 16-bit / mono PCM** pushed into Azure **continuous recognition** (the hub's audio rate).
  Mic and file audio are downsampled to 8 kHz first, so results match what a call sounds like.
- An optional **phrase boost list**, weight 1.5 (`AsrEngineAzure.BOOST_WEIGHT`). The pt-PT list is
  `PT_BOOST_PHRASES` in `asr_common.py` — a proposal, measured with and without.

## Setup

```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
copy .env.example .env      # then fill AZURE_SPEECH_KEY / AZURE_SPEECH_REGION (dev key)
```

## 1. Talk to it

```
.venv/Scripts/python live_mic.py                # with boost list
.venv/Scripts/python live_mic.py --no-boost
.venv/Scripts/python live_mic.py --save joao    # also keep the audio
```
Prints partials while you speak and each final result with the intent it maps to
(help / safe / yes / no / other).

## 2. Test set — `data/sentences_ptpt.csv` (150 sentences)

| Category | # | Intent |
|---|---|---|
| safe ("Estou bem", "Não caí", "Não me magoei") | 30 | safe (1 other) |
| help ("Preciso de ajuda", "Caí na casa de banho", "Dói-me a anca") | 35 | help |
| yes / no ("Sim", "Pois", "Não", "Não, obrigado") | 20 | yes / no |
| everyday (medication, family, weather, greetings) | 40 | other |
| Azorean forms ("Tou bem", "Nã, nã me magoei", "Atão", "Ai minha Nossa Senhora que eu caí") | 15 | mixed |
| hesitation ("Hã? O quê?", "Espere, deixe-me ver") | 10 | other |

The Azorean lines are written approximations — have an Azorean speaker review and say them their way.
`asr_common.intent_of` is checked to give every sentence its labelled intent.

## 3. Collect audio

```
.venv/Scripts/python record_test_set.py --speaker joao_lisboa      # real speaker, resumable
.venv/Scripts/python synthesize_test_set.py                        # Azure pt-PT voice: pipeline check / best case only
```
Recordings stay local (`recordings/` is git-ignored) — they are people's voices.

## 4. Evaluate

```
.venv/Scripts/python evaluate.py --label first_pass                # all speakers, boost off and on
```
`results/<label>/summary.md`: WER (accents kept and ignored), key-answer intent accuracy, and
**help heard as safe** — the dangerous error — per speaker, per category, with every intent error listed.

## Cost (Azure list prices, standard tier)
Real-time speech-to-text is billed per audio hour (about $1/h). The full set is ~8 minutes of audio,
so one speaker × boost on+off is roughly $0.30. Synthesizing the set once is ~4k characters (cents).
