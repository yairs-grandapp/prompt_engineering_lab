# KS-881 realistic set: v7g_real_en_t1_gpt-6.1-terra

481 conversations. Passed (outcome, closing turn and goodbye all right): **480 (99.8%)**.

| Figure | Result |
|---|---|
| **Fall detection:** fell or needed help, and an alert was raised | 267 of 267 (**100.0%**) |
| ... of those, with the right reason (fall / assistance) | 267 of 267 (100.0%) |
| Falls reported as a confirmed fall | 154 of 154 (100.0%) |
| **False detection:** fine, but an alert was raised | 0 of 169 (**0.0%**) |
| ... of those, reported as a fall | 0 of 169 (0.0%) |

| What really happened | Calls | Alert raised | Right outcome | Passed |
|---|---|---|---|---|
| fall | 154 | 100.0% | 100.0% | 99.4% |
| help | 113 | 100.0% | 100.0% | 100.0% |
| fine | 169 | 0.0% | 100.0% | 100.0% |
| unclear | 31 | 100.0% | 100.0% | 100.0% |
| silent | 14 | 100.0% | 100.0% | 100.0% |

Reply time: median 1455 ms, p95 2089 ms, max 4033 ms; 0.0% under 1 s.

## Failed conversations

| Conversation | Senior said | Expected | Vega | Why |
|---|---|---|---|---|
| real_fh/w9 | I fell and hit my head. | distress_fall_confirmed @1 | distress_fall_confirmed @1: "I'm sorry you fell and hit your head, Jake. I'm raising an alert in the SeniorMatics system. Please take care, Jake. Goodbye." | assistanceRequested missing on a fall with a help request |
