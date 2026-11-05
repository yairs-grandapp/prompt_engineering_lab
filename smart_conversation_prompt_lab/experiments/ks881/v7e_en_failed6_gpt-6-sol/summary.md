# KS-881 eval: v7e_en_failed6_gpt-6-sol — PASS

2026-11-03T11:11:28 | gpt-6-sol | temperature=0.0 | prompt=v7e | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 6/6 | 6/6 | 1303 | 3036 | 0 | $0.25 |

Cost: list price, cached input at the cached price (49488 of 163311 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| still_unclear | Still unclear | distress_assistance_requested@[1, 2] | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| soso_twice | v7: so-so after the re-ask is used | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@4 | 1/1 | 1/1 | distress_unable_to_verify@4 x1 |
| unclear_fine_then_hold | v7: unclear, fine, then hold on (not free) | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 1/1 | 1/1 | distress_unable_to_verify@4 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

