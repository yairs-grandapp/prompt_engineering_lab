# KS-881 eval: v2_en_r1 — FAIL

2026-10-30T15:38:03 | gpt-4o | temperature=None | prompt=v2 | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 164/211 | 164/211 | 1121 | 2122 | 22 | $6.54 |

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 27/30 | 27/30 | assistance_requested@2 x5, distress_fall_confirmed@1 x25 |
| fell_not_hurt | Clearly fell (says not hurt) | distress_fall_confirmed@1 | 2/3 | 2/3 | distress_fall_confirmed@1 x2, no_response_from_resident@3 x1 |
| hurt_no_fall | Hurt without saying they fell | assistance_requested@1 | 10/10 | 10/10 | assistance_requested@1 x10 |
| asks_help | Needs help | assistance_requested@1 | 11/11 | 11/11 | assistance_requested@1 x11 |
| unwell_no_fall | Unwell without a fall | assistance_requested@1 | 10/10 | 10/10 | assistance_requested@1 x10 |
| no_fall_but_problem | Denial with a problem | assistance_requested@1 | 2/3 | 2/3 | ERROR@0 x1, assistance_requested@1 x2 |
| fine_confirmed | Says they're fine and confirms it | no_fall_confirmed@2 | 30/34 | 30/34 | ERROR@0 x1, ERROR@1 x2, ERROR@2 x1, no_fall_confirmed@2 x30 |
| denial_then_fine | Denial alone, then fine | no_fall_confirmed@2 | 4/4 | 4/4 | no_fall_confirmed@2 x4 |
| denial_then_help | Denial alone, then a problem | assistance_requested@2 | 2/3 | 2/3 | ERROR@1 x1, assistance_requested@2 x2 |
| fine_then_pain | Says they're fine, then mentions pain | assistance_requested@2 | 5/6 | 5/6 | ERROR@2 x1, assistance_requested@2 x5 |
| fine_then_fell | Says they're fine, then mentions a fall | distress_fall_confirmed@2 | 6/8 | 6/8 | assistance_requested@2 x2, distress_fall_confirmed@2 x6 |
| unclear_then_fell | Unclear, then fell | distress_fall_confirmed@2 | 2/5 | 2/5 | ERROR@0 x2, distress_fall_confirmed@2 x3 |
| unclear_then_problem | Unclear, then hurt or needs help | assistance_requested@2 | 3/3 | 3/3 | assistance_requested@2 x3 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@3 | 6/8 | 6/8 | ERROR@0 x1, no_fall_confirmed@2 x3, no_fall_confirmed@3 x4 |
| silence_then_problem | Silent, then fell or needs help | distress_fall_confirmed@2 | 3/6 | 3/6 | ERROR@1 x1, ERROR@2 x1, assistance_requested@2 x3, distress_fall_confirmed@2 x1 |
| silence_then_fine | Silent, then clearly okay | no_fall_confirmed@3 | 3/5 | 3/5 | ERROR@2 x1, no_fall_confirmed@2 x1, no_fall_confirmed@3 x3 |
| fine_then_silent | Says fine, then goes silent | unable_to_verify@3 | 0/3 | 0/3 | ERROR@1 x1, no_response_from_resident@3 x2 |
| still_unclear | Still unclear | unable_to_verify@2 | 19/29 | 19/29 | ERROR@0 x1, ERROR@2 x1, ERROR@3 x2, no_fall_confirmed@2 x1, no_response_from_resident@3 x1, no_response_from_resident@4 x2, unable_to_verify@2 x19, unable_to_verify@3 x2 |
| what_twice | "What?" twice | unable_to_verify@2 | 2/3 | 2/3 | no_response_from_resident@3 x1, unable_to_verify@2 x2 |
| mixed_no_restart | Mixed unclear and silence: the re-ask never restarts | unable_to_verify@2 | 1/6 | 1/6 | ERROR@0 x1, ERROR@2 x1, no_response_from_resident@2 x1, unable_to_verify@2 x1, unable_to_verify@3 x2 |
| interrupted | Answer cut off | assistance_requested@2 | 2/3 | 2/3 | ERROR@0 x1, assistance_requested@2 x1, distress_fall_confirmed@2 x1 |
| silent_twice | Silent twice | no_response_from_resident@2 | 4/4 | 4/4 | no_response_from_resident@2 x4 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@3 | 0/2 | 0/2 | ERROR@2 x1, no_fall_confirmed@2 x1 |
| past_fall_now_hurt | Past fall, hurt now | assistance_requested@[1, 2] | 2/2 | 2/2 | assistance_requested@2 x2 |
| help_during_goodbye | Help asked during the goodbye | no_fall_confirmed@2 | 3/3 | 3/3 | no_fall_confirmed@2 x3 |
| thanks_during_goodbye | Thanks during the goodbye: no alert | no_fall_confirmed@2 | 1/2 | 1/2 | no_fall_confirmed@2 x1, no_response_from_resident@4 x1 |
| unknown_other_fell | Another person says someone fell | distress_fall_confirmed@1 | 1/2 | 1/2 | assistance_requested@1 x1, distress_fall_confirmed@1 x1 |
| unknown_other_needs_help | Another person says someone needs help | assistance_requested@1 | 2/2 | 2/2 | assistance_requested@1 x2 |
| unknown_silent_twice | Nobody identified, silent twice | no_response_from_resident@2 | 1/1 | 1/1 | no_response_from_resident@2 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `fell/w3#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fell/w4#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fell/legacy20#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fell_not_hurt/w2#0`: outcome no_response_from_resident, expected distress_fall_confirmed; closed after 3 answer(s), expected 1 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm glad you're okay. Just to make sure, is there any pain or discomfort anywhere? / Sorry, I didn't quite catch that. Are you experiencing any pain or discomfort? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `no_fall_but_problem/w2#0`: outcome ERROR, expected assistance_requested — Vega: ''
- `fine_confirmed/w3#0`: outcome ERROR, expected no_fall_confirmed — Vega: ''
- `fine_confirmed/legacy5#0`: outcome ERROR, expected no_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Thanks for letting me know, Jake. Just double-checking, you're not hurt and everything is okay, right?"
- `fine_confirmed/legacy23#0`: outcome ERROR, expected no_fall_confirmed — Vega: "Hello Jake, it's Vega. I received an alert that you might have fallen. Are you alright?"
- `fine_confirmed/legacy29#0`: outcome ERROR, expected no_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay?"
- `denial_then_help/w3#0`: outcome ERROR, expected assistance_requested — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay?"
- `fine_then_pain/w2#0`: outcome ERROR, expected assistance_requested — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / That's good to hear, Jake. Can I confirm that you're not hurt anywhere and are able to move around normally?"
- `fine_then_fell/legacy1#0`: outcome assistance_requested, expected distress_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / That's good to hear, Jake. Just to be sure, are you able to get up and move around comfortably? / I'm sorry to hear you slipped, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_then_fell/legacy3#0`: outcome assistance_requested, expected distress_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm glad to hear you didn't fall, Jake. Just to make sure, do you need any help or assistance with anything? / I'm sorry to hear about your tumble, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `unclear_then_fell/w1#0`: outcome ERROR, expected distress_fall_confirmed — Vega: ''
- `unclear_then_fell/legacy1#0`: outcome ERROR, expected distress_fall_confirmed — Vega: ''
- `unclear_then_fell/legacy2#0`: goodbye: says 'you fell' to a senior who never said so — Vega: "Hi Jake, it's Vega. I received a notification that you might have fallen. Are you okay? / It's alright, Jake. Just to make sure, are you currently feeling okay or do you need any assistance? / I'm sorry to hear you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `unclear_then_fine/legacy1#0`: outcome ERROR, expected no_fall_confirmed — Vega: ''
- `unclear_then_fine/legacy3#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm sorry for the interruption, Jake. I just want to make sure you're alright. Can you let me know if you're okay? / I'm glad to hear everything is alright, Jake. Take care and have a good day. Goodbye."
- `silence_then_problem/w1#0`: outcome ERROR, expected distress_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay?"
- `silence_then_problem/w2#0`: outcome ERROR, expected distress_fall_confirmed — Vega: "Hi Jake, it's Vega. I received a notification that you might have fallen. Are you okay? / Are you alright, Jake?"
- `silence_then_problem/legacy2#0`: outcome assistance_requested, expected distress_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / Hi Jake, just checking if you can hear me. Are you okay? / I'm sorry you need help, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `silence_then_fine/legacy1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Sorry, I didn't hear a response, Jake. Are you alright? / I'm glad to hear you're okay, Jake. Thanks for letting me know. Take care. Goodbye."
- `silence_then_fine/legacy2#0`: outcome ERROR, expected no_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Jake, are you okay?"
- `fine_then_silent/w1#0`: outcome no_response_from_resident, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / That's good to hear, Jake. Just to make sure, are you hurt anywhere or can you get up easily? / Jake, are you there? Just checking in again to see if you're okay. Can you let me know? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `fine_then_silent/w2#0`: outcome ERROR, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay?"
- `fine_then_silent/legacy1#0`: outcome no_response_from_resident, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I got an alert that you might have fallen. Are you okay? / I'm glad to hear you're feeling fine, Jake. Just to double-check, are you able to get up without any issues? / Jake, are you able to get up without any issues? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/w4#0`: outcome ERROR, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm not sure about Mary right now, Jake. But I need to know, are you okay? / Just to make sure I understand, Jake. Are you feeling alright?"
- `still_unclear/w5#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm sorry if I'm bothering you, Jake. I just want to make sure you're safe. Are you sure everything is alright? / I understand, Jake. I just need to ensure you're alright. Can you please let me know if you need any help? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy2#0`: outcome ERROR, expected unable_to_verify — Vega: ''
- `still_unclear/legacy3#0`: outcome ERROR, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / I'm sorry to hear that, Jake. Are you feeling alright or do you need help?"
- `still_unclear/legacy8#0`: outcome ERROR, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / It sounds like you're not sure, Jake. Is there anything you're feeling or experiencing that might indicate if you are hurt or need help? / Are you okay, Jake?"
- `still_unclear/legacy10#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Hi Jake, it's Vega. I'm checking in to see if you're okay. Did you fall or need any help? / You seem a bit confused, Jake. I'm here to help. Are you feeling alright? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy14#0`: outcome no_fall_confirmed, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / I'm glad to hear you were able to get up, Jake. Are you sure you're not hurt or need any help now? / I'm happy everything is alright. Take care. Goodbye."
- `still_unclear/legacy16#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 4 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / Today is Tuesday, Jake. Can you please let me know if you're okay? / I'm not sure about your breakfast, Jake. Right now, I need to know if you're alright. Are you okay? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy23#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm glad to hear that, Jake. Can you just confirm whether you feel okay or if you need help with anything? / Are you feeling any pain, or do you need assistance getting up, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `still_unclear/legacy24#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 4 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have had a fall. Are you okay? / I'm doing well, thank you for asking, Jake. But I'm concerned about you right now - are you okay? / I appreciate your concern, Jake. However, I want to make sure that you're doing well. Can you let me know if everything is alright with you? / Jake, can you hear me? Are you okay? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `what_twice/w2#0`: outcome no_response_from_resident, expected unable_to_verify; closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Are you okay, Jake? / Jake, I'm trying to check if you're alright. Could you let me know if everything is okay or if you need any help? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w2#0`: outcome ERROR, expected unable_to_verify — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Did you say something happened in the garden, Jake? Are you okay?"
- `mixed_no_restart/w3#0`: outcome ERROR, expected unable_to_verify — Vega: ''
- `mixed_no_restart/w4#0`: outcome no_response_from_resident, expected unable_to_verify — Vega: "Hi Jake, this is Vega. I received an alert that you might have fallen. Are you okay? / Are you okay, Jake? / I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/w5#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received a notification that you might have fallen. Are you okay? / Jake, it sounds like you might not have caught my question. Are you alright? / Are you okay, Jake? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `mixed_no_restart/legacy1#0`: closed after 3 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / I'm concerned since I haven't heard from you, Jake. Are you okay? / Sorry, I didn't quite catch that, Jake. Are you okay? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `interrupted/w3#0`: outcome ERROR, expected unable_to_verify — Vega: ''
- `past_fall_now_fine/w1#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Thanks for letting me know, Jake. Just to confirm, are you hurt or need help right now? / I'm happy to hear that everything is okay. Take care, Jake. Goodbye."
- `past_fall_now_fine/w2#0`: outcome ERROR, expected no_fall_confirmed — Vega: "Hi Jake, it's Vega. I received an alert that you might have fallen. Are you okay? / Thank you for letting me know, Jake. Just to make sure, are you feeling alright now?"
- `thanks_during_goodbye/w1#0`: outcome no_response_from_resident, expected no_fall_confirmed; closed after 4 answer(s), expected 2 (asked again instead of closing) — Vega: "Hi Jake, it's Vega. I received an alert that you may have fallen. Are you okay? / I'm glad to hear that you're fine. Just to make sure, are you able to get up and move around normally? / It's good to know you're not hurt. Are you able to get up and move around without any help, Jake? / Jake, are you able to get up and move around without assistance? / I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `unknown_other_fell/w1#0`: outcome assistance_requested, expected distress_fall_confirmed — Vega: "Hi, it's Vega! A possible fall was detected. Does anyone need help? / I'm sorry to hear about your husband. I'm raising an alert in the SeniorMatics system. Please take care. Goodbye."

## Warnings

- 'haven't heard from you' said to a senior who spoke: 5
