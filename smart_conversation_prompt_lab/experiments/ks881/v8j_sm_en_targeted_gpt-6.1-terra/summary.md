# KS-881 eval: v8j_sm_en_targeted_gpt-6.1-terra — PASS

2026-11-04T10:39:57 | gpt-6.1-terra | temperature=None | prompt=v8j_java | en | inputs_ks881_en.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 18/18 | 54/54 | 1442 | 1951 | 0 | $0.09 |

Cost: list price, cached input at the cached price (494622 of 512998 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| still_unclear | Still unclear | distress_unable_to_verify@2 | 11/11 | 33/33 | distress_assistance_requested@1 x3, distress_unable_to_verify@2 x27, distress_unable_to_verify@3 x3 |
| turn_limit | B40: fine, then keeps talking off-topic | distress_unable_to_verify@3 | 1/1 | 3/3 | distress_unable_to_verify@3 x3 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 1/1 | 3/3 | distress_unable_to_verify@5 x3 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 3/3 | 9/9 | no_fall_confirmed@3 x9 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 2/2 | 6/6 | distress_unable_to_verify@4 x6 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

