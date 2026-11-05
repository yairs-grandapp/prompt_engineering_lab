# KS-881 eval: v8g_fix_en — PASS

2026-11-03T17:04:02 | gpt-6.1-terra | temperature=None | prompt=v8g | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 3/3 | 3/3 | 1554 | 2211 | 0 | $0.01 |

Cost: list price, cached input at the cached price (18800 of 22267 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| still_unclear | Still unclear | distress_unable_to_verify@2 | 2/2 | 2/2 | distress_unable_to_verify@2 x2 |
| unclear_then_problem | Unclear, then hurt or needs help | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

