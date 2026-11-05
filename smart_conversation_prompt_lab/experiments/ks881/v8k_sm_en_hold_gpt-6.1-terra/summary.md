# KS-881 eval: v8k_sm_en_hold_gpt-6.1-terra — PASS

2026-11-04T10:47:16 | gpt-6.1-terra | temperature=None | prompt=v8k_java | en | inputs_ks881_en.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 8/8 | 24/24 | 1411 | 2094 | 0 | $0.05 |

Cost: list price, cached input at the cached price (280086 of 296008 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@3 | 2/2 | 6/6 | distress_unable_to_verify@3 x3, distress_unable_to_verify@4 x3 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 1/1 | 3/3 | distress_unable_to_verify@5 x3 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 3/3 | 9/9 | no_fall_confirmed@3 x9 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 2/2 | 6/6 | distress_unable_to_verify@4 x6 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

- 'haven't heard from you' said to a senior who spoke: 1
- unclear call without 'trouble understanding': 1
