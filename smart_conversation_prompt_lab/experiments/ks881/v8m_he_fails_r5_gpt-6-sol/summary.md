# KS-881 eval: v8m_he_fails_r5_gpt-6-sol — FAIL

2026-11-05T13:43:01 | gpt-6-sol | temperature=None | prompt=v8m_java | he | inputs_ks881_he.json | runs=5

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 1/3 | 9/15 | 2327 | 5100 | 0 | $0.08 |

Cost: list price, cached input at the cached price (130593 of 132299 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| fell | Clearly fell | distress_fall_confirmed@1 | 0/1 | 4/5 | distress_fall_confirmed@1 x4, distress_unable_to_verify@2 x1 |
| misheard_alert | A misheard fall or help word | distress_unable_to_verify@1 | 0/1 | 0/5 | distress_assistance_requested@1 x5 |
| fine_then_fell | Says they're fine, then mentions a fall | distress_fall_confirmed@2 | 1/1 | 5/5 | distress_fall_confirmed@2 x5 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `fell/w3#0`: outcome distress_unable_to_verify, expected distress_fall_confirmed; closed after 2 answer(s), expected 1 (asked again instead of closing) — Vega: 'שלום דוד, כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל בסדר? / דוד, נפלתָ ליד המיטה? / קשה לי להבין אותך, דוד. הבטיחות שלך היא בראש סדר העדיפויות שלי, ולכן אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות.'
- `misheard_alert/w3#0`: outcome distress_assistance_requested, expected distress_unable_to_verify — Vega: 'שלום דייוויד, כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל בסדר? / צר לי שאתה צריך עזרה, דייוויד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דייוויד. להתראות.'
- `misheard_alert/w3#1`: outcome distress_assistance_requested, expected distress_unable_to_verify — Vega: 'שלום דוד, כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל בסדר? / צר לי שאתה צריך עזרה, דוד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות.'
- `misheard_alert/w3#3`: outcome distress_assistance_requested, expected distress_unable_to_verify — Vega: 'שלום דוד, כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל בסדר? / צר לי שאתה צריך עזרה, דוד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות.'
- `misheard_alert/w3#2`: outcome distress_assistance_requested, expected distress_unable_to_verify — Vega: 'שלום דוד, כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל בסדר? / צר לי שאתה צריך עזרה, דוד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות.'
- `misheard_alert/w3#4`: outcome distress_assistance_requested, expected distress_unable_to_verify — Vega: 'שלום דוד, כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל בסדר? / צר לי שאתה צריך עזרה, דוד. אני מעבירה התראה במערכת סניורמטיקס. שמור על עצמך, דוד. להתראות.'

## Warnings

