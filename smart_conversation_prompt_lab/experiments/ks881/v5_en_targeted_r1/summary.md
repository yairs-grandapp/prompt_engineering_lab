# KS-881 eval: v5_en_targeted_r1 — FAIL

2026-10-30T16:00:37 | gpt-4o | temperature=None | prompt=v5 | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 33/40 | 33/40 | 1094 | 1646 | 0 | $0.92 |

Cost: list price, cached input at the cached price (595712 of 648060 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| unclear_then_problem | Unclear, then hurt or needs help | assistance_requested@2 | 2/2 | 2/2 | assistance_requested@2 x2 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@[2, 3] | 5/6 | 5/6 | distress_fall_confirmed@2 x1, no_fall_confirmed@2 x4, no_fall_confirmed@3 x1 |
| silence_then_fine | Silent, then clearly okay | no_fall_confirmed@[2, 3] | 2/2 | 2/2 | no_fall_confirmed@2 x2 |
| fine_then_silent | Says fine, then goes silent | no_response_from_resident@3 | 3/3 | 3/3 | no_response_from_resident@3 x3 |
| still_unclear | Still unclear | unable_to_verify@2 | 9/14 | 9/14 | distress_fall_confirmed@1 x1, no_response_from_resident@4 x1, unable_to_verify@1 x1, unable_to_verify@2 x9, unable_to_verify@3 x2 |
| what_twice | "What?" twice | unable_to_verify@2 | 2/2 | 2/2 | unable_to_verify@2 x2 |
| mixed_no_restart | Mixed unclear and silence: the re-ask never restarts | unable_to_verify@2 | 5/6 | 5/6 | no_response_from_resident@2 x1, unable_to_verify@2 x5 |
| interrupted | Answer cut off | assistance_requested@2 | 3/3 | 3/3 | assistance_requested@2 x1, distress_fall_confirmed@2 x1, unable_to_verify@2 x1 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@[2, 3] | 2/2 | 2/2 | no_fall_confirmed@2 x2 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `unclear_then_fine/legacy1#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Are you okay, Jake? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy2#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I got an alert that you might have fallen. Are you okay? / I'm fine, thank you. Just to confirm, are you okay? Did anything happen? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy14#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I got an alert that you might have fallen. Are you okay? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy18#0`: closed after 1 answer(s), expected 2 (closed early: skipped the re-ask or the confirming question); goodbye: 5 sentences — Vega: "Hi Jake, it's Vega. I got an alert that you might have fallen. Are you okay? / It's Vega. I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy23#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that there might have been a fall. Are you okay? / I'm glad to hear that, but I just want to double-check to make sure. Are you hurt anywhere, or do you need any help? / I'm having trouble understanding if you're alright, Jake. Are you feeling any pain or discomfort at all? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy24#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 4 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm doing well, thank you for asking, Jake. I want to make sure you're alright. Did you have a fall or do you need any help? / I'm having a nice day, thank you, Jake. But I'm here because I received a fall alert for you. Are you okay? / Jake, are you okay? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w2#0`: outcome unable_to_verify, expected no_response_from_resident — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm sorry, I didn't quite understand that. Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."

## Warnings

- 'haven't heard from you' said to a senior who spoke: 5
