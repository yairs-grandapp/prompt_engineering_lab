# KS-881 eval: v8j_sm_en_targeted2_gpt-6.1-terra — PASS

2026-11-04T10:36:21 | gpt-6.1-terra | temperature=None | prompt=v8j_java | en | inputs_ks881_en.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 5/5 | 15/15 | 1645 | 2083 | 0 | $0.03 |

Cost: list price, cached input at the cached price (108155 of 118108 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| interrupted | Answer cut off | distress_assistance_requested@2 | 4/4 | 12/12 | distress_assistance_requested@1 x3, distress_assistance_requested@2 x3, distress_fall_confirmed@2 x3, distress_unable_to_verify@2 x3 |
| fine_then_refuses | v7: fine, then refuses | distress_unable_to_verify@3 | 1/1 | 3/3 | distress_unable_to_verify@3 x3 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

