# KS-881 eval: v7f_en_fix2_gpt-6.1-terra — PASS

2026-11-03T11:41:40 | gpt-6.1-terra | temperature=0.0 | prompt=v7f | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 2/2 | 2/2 | 1430 | 3609 | 0 | $0.00 |

Cost: list price, cached input at the cached price (42039 of 42607 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell_and_help | Fell and asks for help | distress_fall_confirmed@1 | 1/1 | 1/1 | distress_fall_confirmed@1 x1 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

