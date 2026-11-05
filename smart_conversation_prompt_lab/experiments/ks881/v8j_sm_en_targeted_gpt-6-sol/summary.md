# KS-881 eval: v8j_sm_en_targeted_gpt-6-sol — FAIL

2026-11-04T10:33:48 | gpt-6-sol | temperature=None | prompt=v8j_java | en | inputs_ks881_en.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 17/18 | 53/54 | 1117 | 1634 | 0 | $0.23 |

Cost: list price, cached input at the cached price (492264 of 510257 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| still_unclear | Still unclear | distress_unable_to_verify@2 | 11/11 | 33/33 | distress_assistance_requested@1 x3, distress_unable_to_verify@2 x27, distress_unable_to_verify@3 x3 |
| turn_limit | B40: fine, then keeps talking off-topic | distress_unable_to_verify@3 | 1/1 | 3/3 | distress_unable_to_verify@3 x3 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 0/1 | 2/3 | distress_unable_to_verify@4 x1, distress_unable_to_verify@5 x2 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 3/3 | 9/9 | no_fall_confirmed@3 x9 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 2/2 | 6/6 | distress_unable_to_verify@4 x6 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `hold_used_then_hold_again/w1#2`: closed after 4 answer(s), expected 5 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a fall alert. Are you okay? / Take your time, Jake, I'll wait. / Are you okay? / Do you need any help, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye"

## Warnings

- 'haven't heard from you' said to a senior who spoke: 1
- unclear call without 'trouble understanding': 1
