# KS-881 eval: v7e_en_failed6_gpt-5.4-mini — FAIL

2026-11-03T10:38:33 | gpt-5.4-mini | temperature=0.0 | prompt=v7e | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 3/6 | 3/6 | 875 | 1832 | 0 | $0.03 |

Cost: list price, cached input at the cached price (159104 of 170591 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| still_unclear | Still unclear | distress_assistance_requested@[1, 2] | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@3 | 0/1 | 0/1 | no_fall_confirmed@2 x1 |
| soso_twice | v7: so-so after the re-ask is used | distress_assistance_requested@2 | 1/1 | 1/1 | distress_unable_to_verify@2 x1 |
| unclear_fine_then_hold | v7: unclear, fine, then hold on (not free) | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@4 | 0/1 | 0/1 | no_response_from_resident@6 x1 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 0/1 | 0/1 | no_response_from_resident@4 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `past_fall_now_fine/w1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it’s Vega. I got a fall alert, and I just want to check, are you okay? / Are you okay now, Jake? / I'm glad to hear you're okay, Jake. Goodbye."
- `hold_repeated/w1#0`: outcome no_response_from_resident, expected distress_unable_to_verify; closed after 6 answer(s), expected 4 (asked again instead of closing) — Vega: "Hi Jake, it’s Vega. I got a fall alert, and I just want to check, are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / Are you okay, Jake? / Are you okay, Jake? / Are you okay, Jake? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `hold_silent_silent/w1#0`: outcome no_response_from_resident, expected distress_unable_to_verify — Vega: "Hi Jake, it’s Vega. I got a fall alert. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / Are you okay, Jake? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."

## Warnings

- 'haven't heard from you' said to a senior who spoke: 2
