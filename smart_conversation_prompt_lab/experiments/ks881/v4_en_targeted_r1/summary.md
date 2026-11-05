# KS-881 eval: v4_en_targeted_r1 — FAIL

2026-10-30T15:53:16 | gpt-4o | temperature=None | prompt=v4 | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 27/40 | 27/40 | 1018 | 1795 | 0 | $0.96 |

Cost: list price, cached input at the cached price (619008 of 676237 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| unclear_then_problem | Unclear, then hurt or needs help | assistance_requested@2 | 2/2 | 2/2 | assistance_requested@2 x2 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@[2, 3] | 5/6 | 5/6 | distress_fall_confirmed@2 x1, no_fall_confirmed@2 x2, no_fall_confirmed@3 x3 |
| silence_then_fine | Silent, then clearly okay | no_fall_confirmed@[2, 3] | 2/2 | 2/2 | no_fall_confirmed@3 x2 |
| fine_then_silent | Says fine, then goes silent | no_response_from_resident@3 | 1/3 | 1/3 | no_response_from_resident@2 x2, no_response_from_resident@3 x1 |
| still_unclear | Still unclear | unable_to_verify@2 | 8/14 | 8/14 | distress_fall_confirmed@1 x1, no_response_from_resident@3 x1, no_response_from_resident@4 x1, no_response_from_resident@5 x1, unable_to_verify@1 x1, unable_to_verify@2 x8, unable_to_verify@3 x1 |
| what_twice | "What?" twice | unable_to_verify@2 | 2/2 | 2/2 | unable_to_verify@2 x2 |
| mixed_no_restart | Mixed unclear and silence: the re-ask never restarts | unable_to_verify@2 | 2/6 | 2/6 | no_response_from_resident@2 x1, no_response_from_resident@3 x1, unable_to_verify@2 x2, unable_to_verify@3 x2 |
| interrupted | Answer cut off | assistance_requested@2 | 3/3 | 3/3 | assistance_requested@2 x1, distress_fall_confirmed@2 x1, unable_to_verify@2 x1 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@[2, 3] | 2/2 | 2/2 | no_fall_confirmed@2 x2 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `unclear_then_fine/legacy1#0`: outcome distress_fall_confirmed, expected no_fall_confirmed; goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Are you okay, Jake? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_then_silent/w1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / That's good to hear, Jake. Just to confirm, are you hurt or do you need any help? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_then_silent/w2#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / That's good to hear. Just to be sure, are you hurt anywhere or do you need any help? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy2#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 5 answer(s), expected 2 (asked again instead of closing) — Vega: "Hello Jake, it's Vega. I got an alert that you might have fallen. Are you okay? / I'm doing well, thank you for asking, Jake. I hope you're okay too. Did anything happen? Are you hurt? / It's a lovely day, Jake. Just want to make sure — are you okay and do you need any help? / Just to confirm, Jake, are you okay or do you need any assistance? / Are you okay, Jake? / I haven't heard from you, Jake, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy9#0`: closed after 1 answer(s), expected 2 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a notification that you might have fallen. Are you okay? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy14#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received a notification that you might have fallen. Are you okay? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy18#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / It's Vega, your care assistant. Just checking in to make sure everything is alright. Are you okay, Jake? / It's Vega, Jake. I'm here to make sure you're safe. Are you okay? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy23#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Just to make sure, are you hurt anywhere or do you need help getting up? / Are you okay, Jake? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy24#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 4 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm fine, thank you for asking, Jake. I was just checking in because I got an alert. Are you okay? / I'm having a nice day, thank you for asking, Jake. I just want to make sure you're alright. Are you okay? / Are you okay, Jake? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w2#0`: outcome unable_to_verify, expected no_response_from_resident — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Are you alright, Jake? Can you tell me if everything is okay? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w3#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Hi Jake, are you okay? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w5#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Sorry, I didn't quite catch that — are you okay, Jake? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/legacy1#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Jake, are you okay? / Are you feeling alright, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."

## Warnings

- 'haven't heard from you' said to a senior who spoke: 7
