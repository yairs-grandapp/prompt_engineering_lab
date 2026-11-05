# KS-881 eval: v8d_fix_en — PASS

2026-11-03T16:19:27 | gpt-6.1-terra | temperature=None | prompt=v8d | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 2/2 | 2/2 | 1742 | 2659 | 0 | $0.01 |

Cost: list price, cached input at the cached price (16161 of 19680 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| thanks_during_goodbye | Thanks during the goodbye: no alert | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

