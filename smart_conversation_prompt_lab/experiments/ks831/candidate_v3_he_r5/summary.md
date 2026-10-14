# KS-831 eval: candidate_v3_he_r5

2026-10-13T15:13:36 | gpt-4o | temperature=None | prompt=prompt_ks831_candidate_v3_he.txt | inputs=inputs_ks831_he.json | runs=5

| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|---|
| 57/60 (95%) | 100% | 95% | 982 | 1534 | 0 | $1.78 |

## By scenario

| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |
|---|---|---|---|---|
| u1_garbled_story | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| u2_rambling_offtopic | 4/5 | 5/5 | 4/5 | distress_fall_confirmed x5 |
| u3_broken_fragments | 4/5 | 5/5 | 4/5 | distress_fall_confirmed x5 |
| u4_confused | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| u5_asr_noise | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f1_i_fell | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f2_hurt | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| f3_need_help | 5/5 | 5/5 | 5/5 | distress_fall_confirmed x5 |
| ok1_fine | 5/5 | 5/5 | 5/5 | no_fall_confirmed x5 |
| ok2_dropped_something | 4/5 | 5/5 | 4/5 | no_fall_confirmed x5 |
| s1_silent | 5/5 | 5/5 | 5/5 | no_response_from_resident x5 |
| s2_silent_after_greeting_long | 5/5 | 5/5 | 5/5 | no_response_from_resident x5 |

## Goodbye violations

- does not end with 'להתראות': 2
- N sentences: 1

## Warnings (1)

- unclear call without 'trouble understanding': 1

## Failing goodbyes

- `u2_rambling_offtopic#2` [distress_fall_confirmed] 'נראה שאתה מתמקד בנושאים אחרים ואני מתקשה להבין אם הכל בסדר איתך. חשוב לי לוודא שאתה בטוח. אני מעבירה התראה במערכת סניורמטיקס. בבקשה שמור על עצמך, דוד. להתראות.' -> 5 sentences
- `u3_broken_fragments#2` [distress_fall_confirmed] 'אני מתקשה להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. תדאג לעצמך, להתראות דוד.' -> does not end with 'להתראות'
- `ok2_dropped_something#2` [no_fall_confirmed] 'אני שמחה שהכול בסדר אצלך. שמור על עצמך, להתראות דוד.' -> does not end with 'להתראות'

## Sample passing goodbyes

- `u1_garbled_story` [distress_fall_confirmed] 'אני מתקשה להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך, דוד. להתראות.'
- `u2_rambling_offtopic` [distress_fall_confirmed] 'אני מתקשה להבין אותך, דיוויד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך, דיוויד. להתראות.'
- `u3_broken_fragments` [distress_fall_confirmed] 'אני מתקשה להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך, דוד. להתראות.'
- `u4_confused` [distress_fall_confirmed] 'קשה לי להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך, דוד. להתראות.'
- `u5_asr_noise` [distress_fall_confirmed] 'אני מתקשה להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך, דוד. להתראות.'
- `f1_i_fell` [distress_fall_confirmed] 'מצטערת ששמעתי שנפלת, דוד. אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך, דוד. להתראות.'
- `f2_hurt` [distress_fall_confirmed] 'אני מצטערת שכואב לך, דוד. אני מעבירה התראה במערכת סניורמטיקס. נא לשמור על עצמך, להתראות.'
- `f3_need_help` [distress_fall_confirmed] 'מצטערת לשמוע שאתה צריך עזרה, דיוויד. אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך. להתראות.'
- `ok1_fine` [no_fall_confirmed] 'שמחה לשמוע שהכל באמת בסדר, דוד. תשמור על עצמך. להתראות.'
- `ok2_dropped_something` [no_fall_confirmed] 'אני שמחה שהכול בסדר, דוד. תשמור על עצמך. להתראות.'
- `s1_silent` [no_response_from_resident] 'דוד, אני לא שמעתי ממך. לא שמעתי ממך, והבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. בבקשה תשמור על עצמך. להתראות.'
- `s2_silent_after_greeting_long` [no_response_from_resident] 'דוד, אני לא שומעת ממך. אני מעבירה התראה במערכת סניורמטיקס. בבקשה שמור על עצמך. להתראות.'
