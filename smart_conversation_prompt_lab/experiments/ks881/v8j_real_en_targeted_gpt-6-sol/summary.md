# KS-881 eval: v8j_real_en_targeted_gpt-6-sol — PASS

2026-11-04T10:38:37 | gpt-6-sol | temperature=None | prompt=v8j_java | en | inputs_ks881_realistic_en.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 108/108 | 324/324 | 1114 | 1444 | 0 | $1.04 |

Cost: list price, cached input at the cached price (2557458 of 2605993 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| real_fi_cf | fine: FI > CF | no_fall_confirmed@2 | 72/72 | 216/216 | no_fall_confirmed@2 x216 |
| real_d_cf | fine: D > CF | no_fall_confirmed@2 | 29/29 | 87/87 | no_fall_confirmed@2 x87 |
| real_fi_s_s | unclear: FI > S > S | distress_unable_to_verify@3 | 7/7 | 21/21 | distress_unable_to_verify@3 x21 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

