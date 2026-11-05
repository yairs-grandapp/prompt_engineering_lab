# KS-881 eval: v7b_en_pick20 — FAIL

2026-11-02T19:55:35 | gpt-4o | temperature=0.0 | prompt=v7b | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 14/20 | 14/20 | 1123 | 2041 | 0 | $0.67 |

Cost: list price, cached input at the cached price (448512 of 479288 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fine_then_pain | Says they're fine, then mentions pain | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| silence_then_fine | Silent, then clearly okay | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| denial_then_fine | Denial alone, then fine | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| interrupted | Answer cut off | distress_assistance_requested@1 | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| still_unclear | Still unclear | distress_assistance_requested@[1, 2] | 0/1 | 0/1 | distress_unable_to_verify@2 x1 |
| what_twice | "What?" twice | distress_unable_to_verify@2 | 1/1 | 1/1 | distress_unable_to_verify@2 x1 |
| fine_then_silent | Says fine, then goes silent | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@3 | 0/1 | 0/1 | no_fall_confirmed@2 x1 |
| silent_twice | Silent twice | no_response_from_resident@2 | 1/1 | 1/1 | no_response_from_resident@2 x1 |
| unknown_visitor_fine | Another person's "I'm fine" (closes until NUN-1591) | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| thanks_during_goodbye | Thanks during the goodbye: no alert | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| help_during_goodbye | Help asked during the goodbye | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| hold_wait_then_fine | v7: hold on, silent (free), then fine and confirms | no_fall_confirmed@4 | 1/1 | 1/1 | no_fall_confirmed@4 x1 |
| soso_twice | v7: so-so after the re-ask is used | distress_assistance_requested@2 | 0/1 | 0/1 | distress_unable_to_verify@2 x1 |
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@4 | 0/1 | 0/1 | distress_unable_to_verify@3 x1 |
| hold_silent_silent | v7: hold on, silent (free), silent again | distress_unable_to_verify@3 | 0/1 | 0/1 | no_response_from_resident@3 x1 |
| unclear_fine_then_hold | v7: unclear, fine, then hold on (not free) | distress_unable_to_verify@3 | 0/1 | 0/1 | distress_unable_to_verify@5 x1 |
| feels_terrible_during_goodbye | v7: feels terrible during the no-fall goodbye | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| unknown_bare_no | v7: nobody identified, a bare no, then confirms | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `still_unclear/w4#0`: outcome distress_unable_to_verify, expected distress_assistance_requested — Vega: "Hi Jake, it's Vega! I received a fall alert. Are you okay? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `past_fall_now_fine/w1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega! I received a fall alert and just wanted to check in. Are you okay? / I'm glad to hear you didn't fall today. Are you feeling okay now, or do you need any help? / I'm happy everything is alright. Take care. Goodbye."
- `soso_twice/w1#0`: outcome distress_unable_to_verify, expected distress_assistance_requested — Vega: "Hi Jake, it's Vega! I received a fall alert. Are you okay? / What's wrong, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `hold_repeated/w1#0`: closed after 3 answer(s), expected 4 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega! I received a fall alert. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `hold_silent_silent/w1#0`: outcome no_response_from_resident, expected distress_unable_to_verify — Vega: "Hi Jake, it's Vega! I received a fall alert. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `unclear_fine_then_hold/w1#0`: closed after 5 answer(s), expected 3 (asked again instead of closing) — Vega: "Hi Jake, it's Vega! I received a fall alert. Are you okay? / Are you okay, Jake? / That's good to hear. Are you hurt anywhere, or can you get up okay? / Take your time, Jake, I'll wait. / Are you hurt anywhere, or can you get up okay? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."

## Warnings

- 'haven't heard from you' said to a senior who spoke: 1
