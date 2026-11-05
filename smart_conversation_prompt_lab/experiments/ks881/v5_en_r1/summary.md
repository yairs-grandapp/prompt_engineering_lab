# KS-881 eval: v5_en_r1 — FAIL

2026-10-30T16:08:08 | gpt-4o | temperature=None | prompt=v5 | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 203/211 | 203/211 | 1290 | 1846 | 0 | $4.07 |

Cost: list price, cached input at the cached price (2844416 of 2962136 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 30/30 | 30/30 | assistance_requested@2 x2, distress_fall_confirmed@1 x27, distress_fall_confirmed@2 x1 |
| fell_not_hurt | Clearly fell (says not hurt) | distress_fall_confirmed@1 | 3/3 | 3/3 | distress_fall_confirmed@1 x3 |
| hurt_no_fall | Hurt without saying they fell | assistance_requested@1 | 10/10 | 10/10 | assistance_requested@1 x10 |
| asks_help | Needs help | assistance_requested@1 | 11/11 | 11/11 | assistance_requested@1 x11 |
| unwell_no_fall | Unwell without a fall | assistance_requested@1 | 9/10 | 9/10 | assistance_requested@1 x9, assistance_requested@2 x1 |
| no_fall_but_problem | Denial with a problem | assistance_requested@1 | 3/3 | 3/3 | assistance_requested@1 x3 |
| fine_confirmed | Says they're fine and confirms it | no_fall_confirmed@2 | 33/34 | 33/34 | no_fall_confirmed@1 x1, no_fall_confirmed@2 x33 |
| denial_then_fine | Denial alone, then fine | no_fall_confirmed@2 | 4/4 | 4/4 | no_fall_confirmed@2 x4 |
| denial_then_help | Denial alone, then a problem | assistance_requested@2 | 3/3 | 3/3 | assistance_requested@2 x3 |
| fine_then_pain | Says they're fine, then mentions pain | assistance_requested@2 | 6/6 | 6/6 | assistance_requested@2 x6 |
| fine_then_fell | Says they're fine, then mentions a fall | distress_fall_confirmed@2 | 8/8 | 8/8 | distress_fall_confirmed@2 x7, distress_fall_confirmed@3 x1 |
| unclear_then_fell | Unclear, then fell | distress_fall_confirmed@2 | 5/5 | 5/5 | distress_fall_confirmed@1 x1, distress_fall_confirmed@2 x4 |
| unclear_then_problem | Unclear, then hurt or needs help | assistance_requested@2 | 3/3 | 3/3 | assistance_requested@2 x3 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@[2, 3] | 8/8 | 8/8 | distress_fall_confirmed@2 x1, no_fall_confirmed@2 x5, no_fall_confirmed@3 x2 |
| silence_then_problem | Silent, then fell or needs help | distress_fall_confirmed@2 | 6/6 | 6/6 | assistance_requested@2 x3, distress_fall_confirmed@2 x3 |
| silence_then_fine | Silent, then clearly okay | no_fall_confirmed@[2, 3] | 5/5 | 5/5 | no_fall_confirmed@2 x4, no_fall_confirmed@3 x1 |
| fine_then_silent | Says fine, then goes silent | no_response_from_resident@3 | 0/3 | 0/3 | no_response_from_resident@2 x3 |
| still_unclear | Still unclear | unable_to_verify@2 | 27/29 | 27/29 | no_response_from_resident@3 x1, unable_to_verify@2 x26, unable_to_verify@3 x2 |
| what_twice | "What?" twice | unable_to_verify@2 | 3/3 | 3/3 | unable_to_verify@2 x3 |
| mixed_no_restart | Mixed unclear and silence: the re-ask never restarts | unable_to_verify@2 | 5/6 | 5/6 | no_response_from_resident@2 x1, unable_to_verify@2 x5 |
| interrupted | Answer cut off | assistance_requested@2 | 3/3 | 3/3 | assistance_requested@2 x1, distress_fall_confirmed@2 x1, unable_to_verify@2 x1 |
| silent_twice | Silent twice | no_response_from_resident@2 | 4/4 | 4/4 | no_response_from_resident@2 x4 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@[2, 3] | 2/2 | 2/2 | no_fall_confirmed@2 x2 |
| past_fall_now_hurt | Past fall, hurt now | assistance_requested@[1, 2] | 2/2 | 2/2 | assistance_requested@2 x2 |
| help_during_goodbye | Help asked during the goodbye | no_fall_confirmed@2 | 3/3 | 3/3 | no_fall_confirmed@2 x3 |
| thanks_during_goodbye | Thanks during the goodbye: no alert | no_fall_confirmed@2 | 2/2 | 2/2 | no_fall_confirmed@2 x2 |
| unknown_other_fell | Another person says someone fell | distress_fall_confirmed@1 | 2/2 | 2/2 | distress_fall_confirmed@1 x2 |
| unknown_other_needs_help | Another person says someone needs help | assistance_requested@1 | 2/2 | 2/2 | assistance_requested@1 x2 |
| unknown_silent_twice | Nobody identified, silent twice | no_response_from_resident@2 | 1/1 | 1/1 | no_response_from_resident@2 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `unwell_no_fall/legacy5#0`: closed after 2 answer(s), expected 1 (asked again instead of closing) — Vega: "Hello Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Are you feeling dizzy or unwell, Jake? / I'm sorry you're not feeling well, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_confirmed/legacy20#0`: closed after 1 answer(s), expected 2 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / That sounds like a lovely activity. I'm glad to hear you're fine. Take care, Jake. Goodbye."
- `fine_then_silent/w1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / I'm glad to hear you're fine. Are you sure you're not hurt anywhere? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_then_silent/w2#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a notification that you might have fallen. Are you okay? / I'm glad to hear that, Jake. Just to double-check, are you hurt or do you need any help? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_then_silent/legacy1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm glad to hear that, Jake. Just to confirm, are you experiencing any pain or do you need any help? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy2#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I got an alert that you might have fallen. Are you okay? / I'm doing well, thank you for asking! Just to make sure, are you hurt or do you need any help? / Jake, I'm asking about your well-being because I received an alert that you might have fallen. Are you alright? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy14#0`: outcome no_response_from_resident, expected distress_fall_confirmed; closed after 3 answer(s), expected [1, 2] (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm sorry you had to go through that, Jake. Since you mentioned managing to get up by yourself, just to confirm, are you hurt anywhere or do you need any assistance now? / I'm sorry you went through that, Jake. Since you're back in your chair now, just to double check, do you need any help or are you feeling alright? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w2#0`: outcome unable_to_verify, expected no_response_from_resident — Vega: "Hi Jake, it's Vega. I've received an alert that you might have fallen. Are you okay? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."

## Warnings

- 'haven't heard from you' said to a senior who spoke: 5
