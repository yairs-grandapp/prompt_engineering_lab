# KS-881 eval: v8k_sm_en_t1_gpt-6.1-terra — PASS

2026-11-04T10:54:19 | gpt-6.1-terra | temperature=None | prompt=v8k_java | en | inputs_ks881_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 198/198 | 198/198 | 1448 | 1945 | 0 | $0.29 |

Cost: list price, cached input at the cached price (1580404 of 1646879 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 12/12 | 12/12 | distress_fall_confirmed@1 x12 |
| fell_not_hurt | Clearly fell (says not hurt) | distress_fall_confirmed@1 | 3/3 | 3/3 | distress_fall_confirmed@1 x3 |
| hurt_no_fall | Hurt without saying they fell | distress_assistance_requested@1 | 7/7 | 7/7 | distress_assistance_requested@1 x7 |
| fell_and_help | Fell and asks for help | distress_fall_confirmed@1 | 5/5 | 5/5 | distress_fall_confirmed@1 x5 |
| asks_help | Needs help | distress_assistance_requested@1 | 8/8 | 8/8 | distress_assistance_requested@1 x8 |
| unwell_no_fall | Unwell without a fall | distress_assistance_requested@1 | 6/6 | 6/6 | distress_assistance_requested@1 x6 |
| no_fall_but_problem | Denial with a problem | distress_assistance_requested@1 | 3/3 | 3/3 | distress_assistance_requested@1 x3 |
| fine_confirmed | Says they're fine and confirms it | no_fall_confirmed@2 | 9/9 | 9/9 | no_fall_confirmed@2 x9 |
| denial_then_fine | Denial alone, then fine | no_fall_confirmed@2 | 4/4 | 4/4 | no_fall_confirmed@2 x4 |
| denial_then_help | Denial alone, then a problem | distress_assistance_requested@2 | 4/4 | 4/4 | distress_assistance_requested@2 x4 |
| fine_then_pain | Says they're fine, then mentions pain | distress_assistance_requested@2 | 5/5 | 5/5 | distress_assistance_requested@2 x5 |
| fine_then_fell | Says they're fine, then mentions a fall | distress_fall_confirmed@2 | 6/6 | 6/6 | distress_fall_confirmed@2 x6 |
| unclear_then_fell | Unclear, then fell | distress_fall_confirmed@2 | 6/6 | 6/6 | distress_fall_confirmed@1 x1, distress_fall_confirmed@2 x5 |
| unclear_then_problem | Unclear, then hurt or needs help | distress_assistance_requested@2 | 3/3 | 3/3 | distress_assistance_requested@2 x3 |
| unclear_then_fine | Unclear, then clearly okay (D16) | no_fall_confirmed@3 | 6/6 | 6/6 | no_fall_confirmed@2 x1, no_fall_confirmed@3 x5 |
| silence_then_problem | Silent, then fell or needs help | distress_fall_confirmed@2 | 4/4 | 4/4 | distress_assistance_requested@2 x2, distress_fall_confirmed@2 x2 |
| silence_then_fine | Silent, then clearly okay | no_fall_confirmed@3 | 2/2 | 2/2 | no_fall_confirmed@3 x2 |
| fine_then_silent | Says fine, then goes silent | distress_unable_to_verify@3 | 2/2 | 2/2 | distress_unable_to_verify@3 x2 |
| still_unclear | Still unclear | distress_unable_to_verify@2 | 11/11 | 11/11 | distress_assistance_requested@1 x1, distress_unable_to_verify@2 x9, distress_unable_to_verify@3 x1 |
| what_twice | "What?" twice | distress_unable_to_verify@2 | 2/2 | 2/2 | distress_unable_to_verify@2 x2 |
| mixed_no_restart | Mixed unclear and silence: the re-ask never restarts | distress_unable_to_verify@2 | 5/5 | 5/5 | distress_unable_to_verify@2 x5 |
| interrupted | Answer cut off | distress_assistance_requested@2 | 4/4 | 4/4 | distress_assistance_requested@1 x1, distress_assistance_requested@2 x1, distress_fall_confirmed@2 x1, distress_unable_to_verify@2 x1 |
| silent_twice | Silent twice | no_response_from_resident@2 | 1/1 | 1/1 | no_response_from_resident@2 x1 |
| past_fall_now_hurt | Past fall, hurt now | distress_assistance_requested@2 | 2/2 | 2/2 | distress_assistance_requested@2 x2 |
| past_fall_now_fine | Past fall, fine now | no_fall_confirmed@3 | 2/2 | 2/2 | no_fall_confirmed@3 x2 |
| help_during_goodbye | Help asked during the goodbye | no_fall_confirmed@2 | 4/4 | 4/4 | no_fall_confirmed@2 x4 |
| unknown_other_fell | Another person says someone fell | distress_fall_confirmed@1 | 2/2 | 2/2 | distress_fall_confirmed@1 x2 |
| thanks_during_goodbye | Thanks during the goodbye: no alert | no_fall_confirmed@2 | 3/3 | 3/3 | no_fall_confirmed@2 x3 |
| unknown_other_needs_help | Another person says someone needs help | distress_assistance_requested@1 | 2/2 | 2/2 | distress_assistance_requested@1 x2 |
| unknown_silent_twice | Nobody identified, silent twice | no_response_from_resident@2 | 1/1 | 1/1 | no_response_from_resident@2 x1 |
| unknown_visitor_fine | Another person's "I'm fine" (closes until NUN-1591) | no_fall_confirmed@2 | 2/2 | 2/2 | no_fall_confirmed@2 x2 |
| fine_silent_then_fine | B12: fine, silent, then fine | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| fine_unclear_twice | B13: fine, then unclear twice | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| fine_unclear_then_fine | B14: fine, unclear, then fine | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| denial_unclear_twice | B19: denial, then unclear twice | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| unclear_fine_then_silent | B27: unclear, fine, then silent | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| silent_fine_then_silent | B39: silent, fine, then silent | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| unknown_still_unclear | B49: nobody identified, still unclear | distress_unable_to_verify@2 | 1/1 | 1/1 | distress_unable_to_verify@2 x1 |
| turn_limit | B40: fine, then keeps talking off-topic | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| unknown_silence_then_fell | B50: nobody identified, silent, then someone fell | distress_fall_confirmed@2 | 1/1 | 1/1 | distress_fall_confirmed@2 x1 |
| unknown_self_fell | B51: nobody identified, the person who fell answers | distress_fall_confirmed@1 | 1/1 | 1/1 | distress_fall_confirmed@1 x1 |
| hold_then_fell | v7: hold on, then says they fell during the wait | distress_fall_confirmed@2 | 2/2 | 2/2 | distress_fall_confirmed@2 x2 |
| hold_then_help | v7: hold on, then needs help during the wait | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| hold_then_fine | v7: hold on, then fine during the wait, then confirms | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| hold_then_unclear | v7: hold on, then unclear twice | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| hold_wait_then_fell | v7: hold on, silent (free), then fell when asked again | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| hold_wait_then_help | v7: hold on, silent (free), then needs help when asked again | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| hold_wait_then_fine | v7: hold on, silent (free), then fine and confirms | no_fall_confirmed@4 | 1/1 | 1/1 | no_fall_confirmed@4 x1 |
| fine_hold_then_fine | v7: fine, hold on, then confirms during the wait | no_fall_confirmed@3 | 2/2 | 2/2 | no_fall_confirmed@3 x2 |
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@3 | 2/2 | 2/2 | distress_unable_to_verify@3 x1, distress_unable_to_verify@4 x1 |
| fine_hold_then_fell | v7: fine, hold on, then says they fell | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| fine_hold_then_help | v7: fine, hold on, then mentions pain | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_hold_wait_then_fine | v7: fine, hold on, silent (free), then confirms | no_fall_confirmed@4 | 2/2 | 2/2 | no_fall_confirmed@4 x2 |
| fine_hold_wait_then_fell | v7: fine, hold on, silent (free), then fell | distress_fall_confirmed@4 | 2/2 | 2/2 | distress_fall_confirmed@4 x2 |
| soso_then_help | v7: so-so, then says what is wrong | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| soso_twice | v7: so-so after the re-ask is used | distress_assistance_requested@2 | 2/2 | 2/2 | distress_assistance_requested@2 x2 |
| fine_hold_wait_then_help | v7: fine, hold on, silent (free), then help | distress_assistance_requested@4 | 1/1 | 1/1 | distress_assistance_requested@4 x1 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 1/1 | 1/1 | distress_unable_to_verify@5 x1 |
| soso_then_fine | v7: so-so, then fine, then confirms | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| fine_soso_then_help | v7: fine, so-so, then says what is wrong | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_soso_twice | v7: fine, so-so, so-so again | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| unclear_then_hold | v7: unclear, then hold on (no longer free) | distress_unable_to_verify@2 | 1/1 | 1/1 | distress_unable_to_verify@2 x1 |
| unclear_fine_then_fell | v7: unclear, fine, then fell | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| unclear_fine_then_help | v7: unclear, fine, then pain | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| unclear_fine_then_soso | v7: unclear, fine, then so-so | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| unclear_fine_then_unclear | v7: unclear, fine, then unclear | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| unclear_denial_then_denial | v7: unclear, denial, then denial | no_fall_confirmed@3 | 1/1 | 1/1 | no_fall_confirmed@3 x1 |
| unclear_fine_then_hold | v7: unclear, fine, then hold on (not free) | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| fine_unclear_then_fell | v7: fine, unclear, then fell | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| fine_unclear_then_help | v7: fine, unclear, then help | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_unclear_then_hold | v7: fine, unclear, then hold on (not free) | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 3/3 | 3/3 | no_fall_confirmed@3 x3 |
| overlap_fine_then_hurt | v7: "I'm fine" continued with a problem in the same answer | distress_assistance_requested@1 | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| fine_then_refuses | v7: fine, then refuses | distress_unable_to_verify@3 | 1/1 | 1/1 | distress_unable_to_verify@3 x1 |
| sad_but_fine | v7: a bit lonely, not hurt | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |
| feels_terrible_during_goodbye | v7: feels terrible during the no-fall goodbye | no_fall_confirmed@2 | 2/2 | 2/2 | no_fall_confirmed@2 x2 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 2/2 | 2/2 | distress_unable_to_verify@4 x2 |
| unknown_bare_yes | v7: nobody identified, a bare yes | distress_assistance_requested@1 | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| unknown_bare_no | v7: nobody identified, a bare no, then confirms | no_fall_confirmed@2 | 1/1 | 1/1 | no_fall_confirmed@2 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

