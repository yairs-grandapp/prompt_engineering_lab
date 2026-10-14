# KS-831 eval: baseline_he_r2

2026-10-13T15:17:05 | gpt-4o | temperature=None | prompt=prompt_ks831_baseline_he.txt | inputs=inputs_ks831_he.json | runs=2

| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|---|
| 0/24 (0%) | 96% | 0% | 1068 | 1707 | 0 | $0.79 |

## By scenario

| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |
|---|---|---|---|---|
| u1_garbled_story | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| u2_rambling_offtopic | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| u3_broken_fragments | 0/2 | 1/2 | 0/2 | distress_fall_confirmed x1, no_response_from_resident x1 |
| u4_confused | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| u5_asr_noise | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| f1_i_fell | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| f2_hurt | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| f3_need_help | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x2 |
| ok1_fine | 0/2 | 2/2 | 0/2 | no_fall_confirmed x2 |
| ok2_dropped_something | 0/2 | 2/2 | 0/2 | no_fall_confirmed x2 |
| s1_silent | 0/2 | 2/2 | 0/2 | no_response_from_resident x2 |
| s2_silent_after_greeting_long | 0/2 | 2/2 | 0/2 | no_response_from_resident x2 |

## Goodbye violations

- does not end with 'להתראות': 22
- invites reply: 15
- missing alert phrase: 7
- could-not-reach: 5
- promise: 2
- question: 2
- N sentences: 1
- says 'you fell' to a senior who never said so: 1

## Warnings (8)

- unclear call without 'trouble understanding': 7
- 'I fell' call without 'sorry': 1

## Failing goodbyes

- `u1_garbled_story#0` [distress_fall_confirmed] 'אני מעבירה התראה במערכת סניורמטיקס. תישאר היכן שאתה, ואני אתך. נתראה בקרוב.' -> promise: 'בקרוב'; does not end with 'להתראות'
- `u1_garbled_story#1` [distress_fall_confirmed] 'אני מתנצלת שלא הבנתי אותך עד עכשיו. נראה שקשה להבין אם אתה בסדר או לא, ולכן אני אעביר התראה ליתר ביטחון. אני מעבירה התראה במערכת סניורמטיקס. תרגיש טוב ולהתראות, דוד.' -> does not end with 'להתראות'
- `u2_rambling_offtopic#0` [distress_fall_confirmed] 'דוד, אני דואגת ולא בטוחה שהבנתי אותך נכון. האם אתה בטוח שאתה בסדר ושהכל בסדר איתך? אני כאן לעזור אם יש צורך.' -> question; invites reply: 'אני כאן'; does not end with 'להתראות'; missing alert phrase
- `u2_rambling_offtopic#1` [distress_fall_confirmed] 'נראה שהשיחה שלנו קצת מתבלבלת. קשה לי לדעת אם אתה בסדר או זקוק לעזרה. אני מעבירה התראה במערכת סניורמטיקס. דאגו לטפל במדיך! להתראות, שמור על עצמך.' -> 5 sentences; does not end with 'להתראות'
- `u3_broken_fragments#0` [distress_fall_confirmed] 'נשמע שיש בעיה. אני מעבירה התראה במערכת סניורמטיקס. תישאר במקום ואני דואגת שתקבל עזרה. כל טוב!' -> does not end with 'להתראות'
- `u3_broken_fragments#1` [no_response_from_resident] 'לא הצלחתי ליצור איתך קשר, אני מעדכנת את המטפלים שלך. תשמור על עצמך, ואני כאן אם תזדקק לי.' -> invites reply: 'אני כאן'; could-not-reach; does not end with 'להתראות'; missing alert phrase
- `u4_confused#0` [distress_fall_confirmed] 'אוי, אני כאן כדי לעזור לך. רק רציתי לדעת אם אתה בסדר או אם נפלת. אתה מרגיש כאבים או צריך עזרה?' -> says 'you fell' to a senior who never said so; question; invites reply: 'אני כאן'; does not end with 'להתראות'; missing alert phrase
- `u4_confused#1` [distress_fall_confirmed] 'אני מצטערת לשמוע שאתה לא מבין. אני מעבירה התראה במערכת סניורמטיקס. תישאר רגוע, אני כאן איתך. להתראות, דויד.' -> invites reply: 'אני כאן'; does not end with 'להתראות'
- `u5_asr_noise#0` [distress_fall_confirmed] 'אני לא מצליחה להבין את מה שאתה אומר. אני מעבירה התראה במערכת סניורמטיקס. תשאר איפה שאתה, אני כאן איתך.' -> invites reply: 'אני כאן'; does not end with 'להתראות'
- `u5_asr_noise#1` [distress_fall_confirmed] 'אני מצטערת, דוד, אני לא מצליחה להבין אותך בבירור. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, ולהתראות.' -> does not end with 'להתראות'
- `f1_i_fell#0` [distress_fall_confirmed] 'אני מצטערת לשמוע שנפלת. אני מעבירה התראה במערכת סניורמטיקס. תשאר במקום ותהיה רגוע, אני אשאר איתך. להתראות דוד.' -> does not end with 'להתראות'
- `f1_i_fell#1` [distress_fall_confirmed] 'אני מצטערת לשמוע שנפלת. אני מעבירה התראה במערכת סניורמטיקס. אנא הישאר רגוע, ביי דוד.' -> does not end with 'להתראות'
- `f2_hurt#0` [distress_fall_confirmed] 'אני מצטערת לשמוע על הכאב שלך. אני מעבירה התראה במערכת סניורמטיקס. בבקשה תישאר במקומך, ואני כאן איתך. להתראות ואשמח לעזור לך בכל דבר שתצטרך.' -> invites reply: 'אני כאן'; does not end with 'להתראות'
- `f2_hurt#1` [distress_fall_confirmed] 'אני מצטערת לשמוע. אני מעבירה התראה במערכת סניורמטיקס. תשאר רגוע, ואני כאן איתך.' -> invites reply: 'אני כאן'; does not end with 'להתראות'
- `f3_need_help#0` [distress_fall_confirmed] 'אני מעבירה התראה במערכת סניורמטיקס. תישאר איפה שאתה, ואני כאן אתך.' -> invites reply: 'אני כאן'; does not end with 'להתראות'
- `f3_need_help#1` [distress_fall_confirmed] 'אני מצטערת לשמוע שאתה זקוק לעזרה. אני מעבירה התראה במערכת סניורמטיקס. תישאר רגוע ואני אמשיך להיות איתך כאן. להתראות, דוד.' -> does not end with 'להתראות'
- `ok1_fine#0` [no_fall_confirmed] 'אני שמחה לשמוע שהכל בסדר ואין לך כאבים. תשמור על עצמך, ואם יש בעיות נוספות, אני כאן בשבילך. שיהיה לך יום נהדר, דוד!' -> invites reply: 'אני כאן'; does not end with 'להתראות'
- `ok1_fine#1` [no_fall_confirmed] 'אני שמחה לשמוע שהכל בסדר אצלך. תמשיך לשמור על עצמך. אם תצטרך משהו, אני פה. להתראות!' -> invites reply: 'אם תצטרך'; invites reply: 'אני פה'
- `ok2_dropped_something#0` [no_fall_confirmed] 'נהדר לשמוע שאתה בטוב דוד. תשמור על עצמך, ואם תצטרך משהו, אני כאן בשבילך. שיהיה לך יום נעים!' -> invites reply: 'אם תצטרך'; invites reply: 'אני כאן'; does not end with 'להתראות'
- `ok2_dropped_something#1` [no_fall_confirmed] 'אני שמחה לשמוע שהכל בסדר. שמור על עצמך ואם תצטרך משהו, אני כאן. להתראות!' -> invites reply: 'אם תצטרך'; invites reply: 'אני כאן'
- `s1_silent#0` [no_response_from_resident] 'לא הצלחתי ליצור איתך קשר, אני מעדכנת את המטפלים שלך. אם אתה שומע אותי ורוצה ליצור קשר, אתה תמיד יכול להושיט עזרה. שיהיה יום טוב ולהתראות.' -> could-not-reach; does not end with 'להתראות'; missing alert phrase
- `s1_silent#1` [no_response_from_resident] 'לא הצלחתי ליצור איתך קשר, אני מעדכנת את המטפלים שלך. תהיה בטוח שיהיה מי שידאג עבורך. להתראות, דיויד.' -> could-not-reach; does not end with 'להתראות'; missing alert phrase
- `s2_silent_after_greeting_long#0` [no_response_from_resident] 'לא הצלחתי ליצור איתך קשר, אני מעדכנת את המטפלים שלך. שמור על עצמך ונתראה בקרוב.' -> promise: 'בקרוב'; could-not-reach; does not end with 'להתראות'; missing alert phrase
- `s2_silent_after_greeting_long#1` [no_response_from_resident] 'לא הצלחתי ליצור איתך קשר, אני מעדכנת את המטפלים שלך. שיהיה לך המשך יום טוב ודאגה מקצועית בהצלחה.' -> could-not-reach; does not end with 'להתראות'; missing alert phrase

## Sample passing goodbyes

