# KS-881 eval: v8b_en_fix4 — PASS

2026-11-03T12:12:23 | gpt-6.1-terra | temperature=0.0 | prompt=v8b | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 4/4 | 4/4 | 1563 | 2322 | 0 | $0.01 |

Cost: list price, cached input at the cached price (31424 of 35703 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| denial_then_fine | Denial alone, then fine | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| unclear_fine_then_soso | v7: unclear, fine, then so-so | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_soso_then_help | v7: fine, so-so, then says what is wrong | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

