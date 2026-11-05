# KS-881 realistic set: v8b_real_en_t1_gpt-6.1-terra

481 conversations. Passed (outcome, closing turn and goodbye all right): **478 (99.4%)**.

| Figure | Result |
|---|---|
| **Fall detection:** fell or needed help, and an alert was raised | 267 of 267 (**100.0%**) |
| ... of those, with the right reason (fall / assistance) | 267 of 267 (100.0%) |
| Falls reported as a confirmed fall | 154 of 154 (100.0%) |
| **False detection:** fine, but an alert was raised | 1 of 169 (**0.6%**) |
| ... of those, reported as a fall | 1 of 169 (0.6%) |

| What really happened | Calls | Alert raised | Right outcome | Passed |
|---|---|---|---|---|
| fall | 154 | 100.0% | 100.0% | 98.7% |
| help | 113 | 100.0% | 100.0% | 100.0% |
| fine | 169 | 0.6% | 99.4% | 99.4% |
| unclear | 31 | 100.0% | 100.0% | 100.0% |
| silent | 14 | 100.0% | 100.0% | 100.0% |

Reply time: median 1403 ms, p95 1997 ms, max 5220 ms; 0.0% under 1 s.

## Failed conversations

| Conversation | Senior said | Expected | Vega | Why |
|---|---|---|---|---|
| real_fh/w4 | I fell and I can't move my leg. | distress_fall_confirmed @1 | distress_fall_confirmed @1: "I'm sorry you fell and can't move your leg, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | assistanceRequested missing on a fall with a help request |
| real_fh/w9 | I fell and hit my head. | distress_fall_confirmed @1 | distress_fall_confirmed @1: "I'm sorry you fell and hit your head, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | assistanceRequested missing on a fall with a help request |
| real_d_cf/w2 | Nothing fell, it was the cat. | no_fall_confirmed @2 | distress_fall_confirmed @1: "I'm sorry the cat fell, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | outcome distress_fall_confirmed, expected no_fall_confirmed; closed after 1 answer(s), expected 2 (closed early: skipped the re-ask or the confirming question) |
