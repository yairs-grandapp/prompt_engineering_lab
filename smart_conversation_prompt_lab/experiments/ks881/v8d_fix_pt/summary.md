# KS-881 eval: v8d_fix_pt — PASS

2026-11-03T16:19:39 | gpt-6.1-terra | temperature=None | prompt=v8d | pt | inputs_ks881_pt.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 4/4 | 4/4 | 1677 | 2858 | 0 | $0.01 |

Cost: list price, cached input at the cached price (41721 of 47265 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fine_confirmed | Says they're fine and confirms it | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| thanks_during_goodbye | Thanks during the goodbye: no alert | no_fall_confirmed@2 | 3/3 | 3/3 | no_fall_confirmed@2 x3 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

