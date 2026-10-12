# KS-834 real-speaker check: João (Lisbon pt-PT), 2026-10-08

Laptop mic, 16 kHz → 8 kHz hub path, Azure pt-PT, continuous recognition. Recordings
(`recordings/live/joao_*`, local only) re-run through `recognize_wav` with boost off and boost_v2 @ 1.5.

| Check | Boost off | Boost on (boost_v2, 1.5) |
|---|---|---|
| Bare "Caí" recognised | 3/8 ("QI", "TI", "Ei TI" otherwise) | **8/8** |
| "Não caí", "Não me magoei" | ok | ok |
| "Sim", "Não", "Pois" (one word) | ok | ok |
| "Estou bem" / "Preciso de ajuda" / "Não estou bem" / "Caí no chão" / long mixed sentence | all ok | all ok |
| Help heard as safe | 0 | 0 |

Session 1 (216 s, free conversation): 10 utterances, identical with and without boost, all intents right.
Session 2 (55 s + 158 s, targeted weak spots incl. ~2 m distance): results above.
New misrecognition seen: "TI" / "Ei TI" for "Caí" — added to the KS-833 prompt protection list.
