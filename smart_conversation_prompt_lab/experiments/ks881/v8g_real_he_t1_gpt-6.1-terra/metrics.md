# KS-881 realistic set (he): v8g_real_he_t1_gpt-6.1-terra

518 conversations. Passed (outcome, closing turn and goodbye all right): **515 (99.4%)**.

| Figure | Result |
|---|---|
| **Fall detection:** fell or needed help, and an alert was raised | 295 of 295 (**100.0%**) |
| ... of those, with the right reason (fall / assistance) | 295 of 295 (100.0%) |
| Falls reported as a confirmed fall | 170 of 170 (100.0%) |
| **False detection:** fine, but an alert was raised | 1 of 171 (**0.6%**) |
| ... of those, reported as a fall | 0 of 171 (0.0%) |

| What really happened | Calls | Alert raised | Right outcome | Passed |
|---|---|---|---|---|
| fall | 154 | 100.0% | 100.0% | 100.0% |
| help | 113 | 100.0% | 100.0% | 98.2% |
| fine | 159 | 0.6% | 99.4% | 99.4% |
| unclear | 31 | 100.0% | 100.0% | 100.0% |
| silent | 14 | 100.0% | 100.0% | 100.0% |
| fall (nobody identified) | 16 | 100.0% | 100.0% | 100.0% |
| help (nobody identified) | 12 | 100.0% | 100.0% | 100.0% |
| fine (nobody identified) | 12 | 0.0% | 100.0% | 100.0% |
| unclear (nobody identified) | 4 | 100.0% | 100.0% | 100.0% |
| silent (nobody identified) | 3 | 100.0% | 100.0% | 100.0% |

Reply time: median 1534 ms, p95 2070 ms, max 5005 ms; 0.0% under 1 s.

## Failed conversations

| Conversation | Senior said | Expected | Vega | Why |
|---|---|---|---|---|
| real_h/w9 | אני צריך שמישהו יבוא. | distress_assistance_requested @1 | distress_assistance_requested @1: "צר לי שאתה צריך שמישהו יבוא, דייוויד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דייוויד. להתראות." | goodbye: promise: 'מישהו יבוא' |
| real_h/w37 | אני צריך שמישהו יבוא. | distress_assistance_requested @1 | distress_assistance_requested @1: "צר לי שאתה צריך שמישהו יבוא, דוד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות." | goodbye: promise: 'מישהו יבוא' |
| real_d_cf/w5 | שום דבר לא נפל, זה היה החתול. · באמת, שום דבר לא קרה. · (silence) | no_fall_confirmed @2 | distress_unable_to_verify @3: "קשה לי להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות." | outcome distress_unable_to_verify, expected no_fall_confirmed; closed after 3 answer(s), expected 2 (asked again instead of closing) |
