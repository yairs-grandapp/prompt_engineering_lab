# KS-881 eval: v8l_sm_pt_alerts_gpt-6-sol — PASS

2026-11-05T11:13:50 | gpt-6-sol | temperature=None | prompt=v8l_java | pt | inputs_ks881_pt.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 110/110 | 110/110 | 1520 | 2528 | 0 | $0.59 |

Cost: list price, cached input at the cached price (985107 of 1031448 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 12/12 | 12/12 | distress_assistance_requested@1 x1, distress_fall_confirmed@1 x11 |
| fell_not_hurt | Clearly fell (says not hurt) | distress_fall_confirmed@1 | 3/3 | 3/3 | distress_fall_confirmed@1 x3 |
| hurt_no_fall | Hurt without saying they fell | distress_assistance_requested@1 | 7/7 | 7/7 | distress_assistance_requested@1 x7 |
| fell_and_help | Fell and asks for help | distress_fall_confirmed@1 | 5/5 | 5/5 | distress_fall_confirmed@1 x5 |
| asks_help | Needs help | distress_assistance_requested@1 | 8/8 | 8/8 | distress_assistance_requested@1 x8 |
| unwell_no_fall | Unwell without a fall | distress_assistance_requested@1 | 6/6 | 6/6 | distress_assistance_requested@1 x6 |
| no_fall_but_problem | Denial with a problem | distress_assistance_requested@1 | 3/3 | 3/3 | distress_assistance_requested@1 x3 |
| denial_then_help | Denial alone, then a problem | distress_assistance_requested@2 | 4/4 | 4/4 | distress_assistance_requested@2 x4 |
| fine_then_pain | Says they're fine, then mentions pain | distress_assistance_requested@2 | 5/5 | 5/5 | distress_assistance_requested@2 x5 |
| fine_then_fell | Says they're fine, then mentions a fall | distress_fall_confirmed@2 | 6/6 | 6/6 | distress_fall_confirmed@2 x5, distress_fall_confirmed@3 x1 |
| unclear_then_fell | Unclear, then fell | distress_fall_confirmed@2 | 6/6 | 6/6 | distress_fall_confirmed@2 x6 |
| unclear_then_problem | Unclear, then hurt or needs help | distress_assistance_requested@2 | 3/3 | 3/3 | distress_assistance_requested@2 x3 |
| silence_then_problem | Silent, then fell or needs help | distress_fall_confirmed@2 | 4/4 | 4/4 | distress_assistance_requested@2 x2, distress_fall_confirmed@2 x2 |
| interrupted | Answer cut off | distress_assistance_requested@2 | 4/4 | 4/4 | distress_assistance_requested@1 x1, distress_assistance_requested@2 x1, distress_fall_confirmed@2 x1, distress_unable_to_verify@2 x1 |
| past_fall_now_hurt | Past fall, hurt now | distress_assistance_requested@2 | 2/2 | 2/2 | distress_assistance_requested@2 x2 |
| unknown_other_fell | Another person says someone fell | distress_fall_confirmed@1 | 2/2 | 2/2 | distress_fall_confirmed@1 x2 |
| unknown_other_needs_help | Another person says someone needs help | distress_assistance_requested@1 | 2/2 | 2/2 | distress_assistance_requested@1 x2 |
| unknown_self_fell | B51: nobody identified, the person who fell answers | distress_fall_confirmed@1 | 1/1 | 1/1 | distress_fall_confirmed@1 x1 |
| unknown_silence_then_fell | B50: nobody identified, silent, then someone fell | distress_fall_confirmed@2 | 1/1 | 1/1 | distress_fall_confirmed@2 x1 |
| hold_then_fell | v7: hold on, then says they fell during the wait | distress_fall_confirmed@2 | 2/2 | 2/2 | distress_fall_confirmed@2 x2 |
| hold_then_help | v7: hold on, then needs help during the wait | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| hold_wait_then_fell | v7: hold on, silent (free), then fell when asked again | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| hold_wait_then_help | v7: hold on, silent (free), then needs help when asked again | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_hold_then_fell | v7: fine, hold on, then says they fell | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| fine_hold_then_help | v7: fine, hold on, then mentions pain | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_hold_wait_then_fell | v7: fine, hold on, silent (free), then fell | distress_fall_confirmed@4 | 2/2 | 2/2 | distress_fall_confirmed@4 x2 |
| soso_then_help | v7: so-so, then says what is wrong | distress_assistance_requested@2 | 1/1 | 1/1 | distress_assistance_requested@2 x1 |
| fine_hold_wait_then_help | v7: fine, hold on, silent (free), then help | distress_assistance_requested@4 | 1/1 | 1/1 | distress_assistance_requested@4 x1 |
| soso_twice | v7: so-so after the re-ask is used | distress_assistance_requested@2 | 2/2 | 2/2 | distress_assistance_requested@2 x2 |
| fine_soso_then_help | v7: fine, so-so, then says what is wrong | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_soso_twice | v7: fine, so-so, so-so again | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| unclear_fine_then_fell | v7: unclear, fine, then fell | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| unclear_fine_then_soso | v7: unclear, fine, then so-so | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| unclear_fine_then_help | v7: unclear, fine, then pain | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |
| fine_unclear_then_fell | v7: fine, unclear, then fell | distress_fall_confirmed@3 | 2/2 | 2/2 | distress_fall_confirmed@3 x2 |
| overlap_fine_then_hurt | v7: "I'm fine" continued with a problem in the same answer | distress_assistance_requested@1 | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| unknown_bare_yes | v7: nobody identified, a bare yes | distress_assistance_requested@1 | 1/1 | 1/1 | distress_assistance_requested@1 x1 |
| fine_unclear_then_help | v7: fine, unclear, then help | distress_assistance_requested@3 | 1/1 | 1/1 | distress_assistance_requested@3 x1 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

