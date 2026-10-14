# KS-831 eval: candidate_v3_en_r5

2026-10-13T15:12:36 | gpt-4o | temperature=None | prompt=prompt_ks831_candidate_v3.txt | inputs=inputs_ks831.json | runs=5

| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|---|
| 60/60 (100%) | 100% | 100% | 895 | 1300 | 0 | $1.40 |

## By scenario

| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |
|---|---|---|---|---|
| u1_garbled_story | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| u2_rambling_offtopic | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| u3_broken_fragments | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| u4_confused | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| u5_asr_noise | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f1_i_fell | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f2_hurt | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f3_need_help | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| ok1_fine | 5/5 | 5/5 | 5/5 | no_fall_confirmed x5 |
| ok2_dropped_something | 5/5 | 5/5 | 5/5 | no_fall_confirmed x5 |
| s1_silent | 5/5 | 5/5 | 5/5 | no_response_from_resident x5 |
| s2_silent_after_greeting_long | 5/5 | 5/5 | 5/5 | no_response_from_resident x5 |

## Goodbye violations


## Warnings (1)

- unclear call without 'trouble understanding': 1

## Failing goodbyes


## Sample passing goodbyes

- `u1_garbled_story` [distress_fall_confirmed] "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `u2_rambling_offtopic` [distress_fall_confirmed] "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `u3_broken_fragments` [distress_fall_confirmed] "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `u4_confused` [distress_fall_confirmed] "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `u5_asr_noise` [distress_fall_confirmed] "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `f1_i_fell` [distress_fall_confirmed] "I'm sorry you fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `f2_hurt` [distress_fall_confirmed] "I'm sorry you need help, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `f3_need_help` [distress_fall_confirmed] "I'm sorry you need help, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `ok1_fine` [no_fall_confirmed] "I'm happy everything is alright. Take care. Goodbye."
- `ok2_dropped_something` [no_fall_confirmed] "I'm glad to hear that everything's okay. Take care, Jake. Goodbye."
- `s1_silent` [no_response_from_resident] "I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
- `s2_silent_after_greeting_long` [no_response_from_resident] "I haven't heard from you, and your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye."
