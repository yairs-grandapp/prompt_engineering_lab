# KS-881 eval: v8n_he_fall_r5_gpt-6-sol — PASS

2026-11-05T15:06:53 | gpt-6-sol | temperature=None | prompt=v8n_java | he | inputs_ks881_he.json | runs=5

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 18/18 | 90/90 | 2061 | 3290 | 0 | $0.38 |

Cost: list price, cached input at the cached price (658648 of 667721 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 10/10 | 50/50 | distress_fall_confirmed@1 x50 |
| fell_and_help | Fell and asks for help | distress_fall_confirmed@1 | 5/5 | 25/25 | distress_fall_confirmed@1 x25 |
| misheard_alert | A misheard fall or help word | distress_unable_to_verify@1 | 3/3 | 15/15 | distress_unable_to_verify@1 x15 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

- echoes the senior's words: 'בדרך': 1
