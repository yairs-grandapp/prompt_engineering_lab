# KS-831 eval: candidate_v2_fell_r5

2026-10-13T14:34:06 | gpt-4o | temperature=None | prompt=prompt_ks831_candidate_v2.txt | inputs=inputs_ks831.json | runs=5

| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|---|
| 15/15 (100%) | 100% | 100% | 910 | 1893 | 0 | $0.31 |

## By scenario

| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |
|---|---|---|---|---|
| f1_i_fell | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f2_hurt | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f3_need_help | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |

## Goodbye violations


## Warnings (0)


## Failing goodbyes


## Sample passing goodbyes

- `f1_i_fell` [distress_fall_confirmed] "I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `f2_hurt` [distress_fall_confirmed] "I'm sorry you need help, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `f3_need_help` [distress_fall_confirmed] "I'm sorry you need help, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
