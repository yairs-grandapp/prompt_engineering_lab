# KS-881 eval: v8k_sm_en_hold_gpt-6-sol — FAIL

2026-11-04T10:45:52 | gpt-6-sol | temperature=None | prompt=v8k_java | en | inputs_ks881_en.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 7/8 | 23/24 | 1107 | 1608 | 0 | $0.13 |

Cost: list price, cached input at the cached price (287956 of 298653 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@4 | 1/2 | 5/6 | distress_unable_to_verify@3 x2, distress_unable_to_verify@4 x4 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 1/1 | 3/3 | distress_unable_to_verify@5 x3 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 3/3 | 9/9 | no_fall_confirmed@3 x9 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 2/2 | 6/6 | distress_unable_to_verify@4 x6 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `hold_repeated/w2#0`: closed after 4 answer(s), expected 3 (asked again instead of closing) — Vega: "Hi Jake, I'm Vega. I received a fall alert. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye"

## Warnings

