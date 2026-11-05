# KS-881 realistic set (en): v8g_real_en_t1_gpt-6-sol

518 conversations. Passed (outcome, closing turn and goodbye all right): **514 (99.2%)**.

| Figure | Result |
|---|---|
| **Fall detection:** fell or needed help, and an alert was raised | 295 of 295 (**100.0%**) |
| ... of those, with the right reason (fall / assistance) | 295 of 295 (100.0%) |
| Falls reported as a confirmed fall | 170 of 170 (100.0%) |
| **False detection:** fine, but an alert was raised | 0 of 171 (**0.0%**) |
| ... of those, reported as a fall | 0 of 171 (0.0%) |

| What really happened | Calls | Alert raised | Right outcome | Passed |
|---|---|---|---|---|
| fall | 154 | 100.0% | 100.0% | 100.0% |
| help | 113 | 100.0% | 100.0% | 100.0% |
| fine | 159 | 0.0% | 100.0% | 99.4% |
| unclear | 31 | 100.0% | 100.0% | 90.3% |
| silent | 14 | 100.0% | 100.0% | 100.0% |
| fall (nobody identified) | 16 | 100.0% | 100.0% | 100.0% |
| help (nobody identified) | 12 | 100.0% | 100.0% | 100.0% |
| fine (nobody identified) | 12 | 0.0% | 100.0% | 100.0% |
| unclear (nobody identified) | 4 | 100.0% | 100.0% | 100.0% |
| silent (nobody identified) | 3 | 100.0% | 100.0% | 100.0% |

Reply time: median 1187 ms, p95 1625 ms, max 5436 ms; 4.6% under 1 s.

## Failed conversations

| Conversation | Senior said | Expected | Vega | Why |
|---|---|---|---|---|
| real_d_cf/w5 | Nothing fell, it was the cat. | no_fall_confirmed @2 | no_fall_confirmed @1: "I'm glad you're okay, Jake. Goodbye." | closed after 1 answer(s), expected 2 (closed early: skipped the re-ask or the confirming question) |
| real_fi_s_s/w2 | All good here. · (silence) · (silence) · (silence) | distress_unable_to_verify @3 | distress_unable_to_verify @4: "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | closed after 4 answer(s), expected 3 (asked again instead of closing) |
| real_fi_s_s/w3 | I'm doing fine. · (silence) · (silence) · (silence) | distress_unable_to_verify @3 | distress_unable_to_verify @4: "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | closed after 4 answer(s), expected 3 (asked again instead of closing) |
| real_fi_s_s/w7 | Everything's fine here. · (silence) · (silence) · (silence) | distress_unable_to_verify @3 | distress_unable_to_verify @4: "I'm having trouble understanding you, Jake. Your safety is my top priority, so I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | closed after 4 answer(s), expected 3 (asked again instead of closing) |
