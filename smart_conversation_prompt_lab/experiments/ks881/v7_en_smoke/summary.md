# KS-881 eval: v7_en_smoke — FAIL

2026-11-02T17:00:30 | gpt-4o | temperature=0.0 | prompt=v7 | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 13/18 | 13/18 | 1267 | 4076 | 0 | $0.56 |

Cost: list price, cached input at the cached price (362624 of 395900 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 1/1 | 1/1 | distress_fall_confirmed@1 x1 |
| fell_and_help | Fell and asks for help | distress_fall_confirmed@1 | 1/1 | 1/1 | distress_fall_confirmed@1 x1 |
| asks_help | Needs help | distress_assistance_requested@1 | 0/1 | 0/1 | distress_assistance_requested@2 x1 |
| fine_confirmed | Says they're fine and confirms it | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| still_unclear | Still unclear | distress_unable_to_verify@2 | 1/1 | 1/1 | distress_unable_to_verify@2 x1 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| silent_twice | Silent twice | no_response_from_resident@2 | 1/1 | 1/1 | no_response_from_resident@2 x1 |
| help_during_goodbye | Help asked during the goodbye | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| hold_then_fell | v7: hold on, then says they fell during the wait | distress_fall_confirmed@2 | 1/1 | 1/1 | distress_fall_confirmed@2 x1 |
| hold_wait_then_fine | v7: hold on, silent (free), then fine and confirms | no_fall_confirmed@4 | 0/1 | 0/1 | no_fall_confirmed@3 x1 |
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@4 | 0/1 | 0/1 | distress_unable_to_verify@3 x1 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 0/1 | 0/1 | distress_unable_to_verify@4 x1 |
| fine_hold_then_fine | v7: fine, hold on, then confirms during the wait | no_fall_confirmed@3 | 0/1 | 0/1 | distress_unable_to_verify@5 x1 |
| soso_then_help | v7: so-so, then says what is wrong | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| fine_soso_then_help | v7: fine, so-so, then says what is wrong | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| unknown_bare_yes | v7: nobody identified, a bare yes | distress_assistance_requested@1 | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| fine_then_refuses | v7: fine, then refuses | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| unclear_fine_then_fell | v7: unclear, fine, then fell | distress_fall_confirmed@3 | 1/1 | 1/1 | distress_fall_confirmed@3 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `asks_help/w6#0`: closed after 2 answer(s), expected 1 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received a fall alert and just wanted to check in. Are you okay? / I'm sorry to hear that, Jake. Do you need any help or are you hurt? / I'm sorry you're not feeling well, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `hold_wait_then_fine/w1#0`: closed after 3 answer(s), expected 4 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a fall alert and just wanted to check in. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / I'm happy everything is alright. Take care. Goodbye."
- `hold_repeated/w1#0`: closed after 3 answer(s), expected 4 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a fall alert and just wanted to check in. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `hold_used_then_hold_again/w1#0`: closed after 4 answer(s), expected 5 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a fall alert. Are you okay? / Take your time, Jake, I'll wait. / Are you okay, Jake? / Can you get up without any trouble, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_hold_then_fine/w1#0`: outcome distress_unable_to_verify, expected no_fall_confirmed; closed after 5 answer(s), expected 3 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received a fall alert and just wanted to check in. Are you okay? / That's good to hear. Are you able to get up and move around without any trouble? / Take your time, Jake, I'll wait. / I'm glad to hear you're not hurt. Is there anything else you need help with? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."

## Warnings

