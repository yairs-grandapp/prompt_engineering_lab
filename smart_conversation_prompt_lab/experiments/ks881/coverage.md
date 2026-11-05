# KS-881 test set: coverage of the earlier sets

176 earlier scenarios, all mapped (0 missing, 0 listed twice). 44 are kept word for word (translated into the other two languages); the rest are covered by their situation's wordings.

Every wording runs in en, pt and he (the same tests in each language).

| Earlier scenario | Lang | New scenario | Kept | Old expected | New expected | Closes after | | Why it changed |
|---|---|---|---|---|---|---|---|---|
| inputs_baseline.json:scenario_01 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v0.json:scenario_01 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_baseline.json:scenario_02 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v0.json:scenario_02 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_baseline.json:scenario_03 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v0.json:scenario_03 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_baseline.json:scenario_04 | en | silent_twice | kept as w1 (en, pt, he) | distress_fall_confirmed | **no_response_from_resident** | 2 |  | KS-714: silence is no_response_from_resident |
| inputs_v0.json:scenario_04 | en | silent_twice | covered by situation | distress_fall_confirmed | **no_response_from_resident** | 2 |  | KS-714: silence is no_response_from_resident |
| inputs_baseline.json:scenario_05 | en | fine_then_pain | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v0.json:scenario_05 | en | fine_then_pain | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_baseline.json:scenario_06 | en | unclear_then_fine | covered by situation | no_fall_confirmed | **distress_fall_confirmed** | 3 |  | baseline (no fall) and v0 (fall) disagreed; "I got up by myself" implies the fall (no fall also accepted) |
| inputs_v0.json:scenario_06 | en | unclear_then_fine | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 3 |  | baseline (no fall) and v0 (fall) disagreed; "I got up by myself" implies the fall (no fall also accepted) |
| inputs_baseline.json:scenario_07 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v0.json:scenario_07 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_baseline.json:scenario_08 | en | fine_then_fell | kept as w5 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [2, 3] |  | "I did slip a little bit" may or may not be read as the fall; both closings are right |
| inputs_v0.json:scenario_08 | en | fine_then_fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | [2, 3] |  | "I did slip a little bit" may or may not be read as the fall; both closings are right |
| inputs_v0.json:scenario_09 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v0.json:scenario_10 | en | hurt_no_fall | kept as w5 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; "hit my head on the floor" may be read as a fall |
| inputs_v0.json:scenario_11 | en | still_unclear | kept as w6 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | the words "I'm scared" are a call for help (Tony 45602) |
| inputs_v0.json:scenario_12 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v0.json:scenario_13 | en | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v0.json:scenario_14 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v0.json:scenario_15 | en | fell_and_help | kept as w4 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | broken words that include "fell" and "help"; Vega may act at once or re-ask |
| inputs_ks831.json:u1_garbled_story | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831.json:u2_rambling_offtopic | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831.json:u3_broken_fragments | en | still_unclear | kept as w9 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831.json:u4_confused | en | still_unclear | kept as w4 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831.json:u5_asr_noise | en | still_unclear | kept as w2 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831_he.json:u1_garbled_story | he | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831_he.json:u2_rambling_offtopic | he | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831_he.json:u3_broken_fragments | he | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831_he.json:u4_confused | he | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831_he.json:u5_asr_noise | he | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks831.json:f1_i_fell | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_ks831_he.json:f1_i_fell | he | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_ks831.json:f2_hurt | en | hurt_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks831_he.json:f2_hurt | he | hurt_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks831.json:f3_need_help | en | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks831_he.json:f3_need_help | he | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks831.json:ok1_fine | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks831.json:ok2_dropped_something | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks831_he.json:ok1_fine | he | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks831_he.json:ok2_dropped_something | he | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks831.json:s1_silent | en | silent_twice | covered by situation | no_response_from_resident | no_response_from_resident | 2 |  |  |
| inputs_ks831.json:s2_silent_after_greeting_long | en | silent_twice | covered by situation | no_response_from_resident | no_response_from_resident | 2 |  |  |
| inputs_ks831_he.json:s1_silent | he | silent_twice | covered by situation | no_response_from_resident | no_response_from_resident | 2 |  |  |
| inputs_ks831_he.json:s2_silent_after_greeting_long | he | silent_twice | covered by situation | no_response_from_resident | no_response_from_resident | 2 |  |  |
| inputs_ks833_ptpt.json:safe_estou_bem | pt | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks833_ptpt.json:safe_obrigado | pt | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks833_ptpt.json:safe_gato | pt | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks833_ptpt.json:safe_azorean | pt | fine_confirmed | kept as w6 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks833_ptpt.json:safe_sim_nao | pt | fine_confirmed | kept as w7 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | [2, 3] |  | a bare "Sim" is not enough in Portuguese, so "não me magoei" may be the first fine answer; the confirming question after a first "I'm fine" needs a reply |
| inputs_ks833_ptpt.json:safe_apanhar | pt | denial_then_fine | kept as w4 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_ks833_ptpt.json:help_preciso_ajuda | pt | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks833_ptpt.json:help_casa_de_banho | pt | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_ks833_ptpt.json:help_doi_perna | pt | hurt_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks833_ptpt.json:help_socorro | pt | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks833_ptpt.json:help_nao | pt | asks_help | kept as w6 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; a bare "Não" to "Está bem?" means they are not okay |
| inputs_ks833_ptpt.json:help_nao_consigo_levantar | pt | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_ks833_ptpt.json:help_nossa_senhora | pt | fell | kept as w10 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_ks833_ptpt.json:help_fine_then_hip | pt | fine_then_pain | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_ks833_ptpt.json:help_deny_then_admit | pt | fine_then_fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 2 |  |  |
| inputs_ks833_ptpt.json:help_misrec_sai | pt | misheard_alert | kept as w2 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 1 |  | "saí" / "boi" are misheard "caí" / "dói": not certain, so unable to verify at once (Tony 45602) |
| inputs_ks833_ptpt.json:unclear_offtopic | pt | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks833_ptpt.json:unclear_nao_sei | pt | still_unclear | kept as w3 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks833_ptpt.json:unclear_cut_off | pt | interrupted | kept as w3 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | cut off, then only "a perna": unable to verify, or read as a leg problem |
| inputs_ks833_ptpt.json:unclear_contradiction | pt | interrupted | kept as w4 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | [1, 2] |  | "Estou bem... não, não estou" says they are not okay; a re-ask is also fair |
| inputs_ks833_ptpt.json:unclear_english_garble | pt | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks833_ptpt.json:unclear_ha | pt | what_twice | kept as w2 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks833_ptpt.json:silence_full | pt | silent_twice | covered by situation | no_response_from_resident | no_response_from_resident | 2 |  |  |
| inputs_ks833_ptpt.json:silence_explicit | pt | silent_twice | covered by situation | no_response_from_resident | no_response_from_resident | 2 |  |  |
| inputs_ks833_ptpt.json:asr_qi_cozinha | pt | misheard_alert | kept as w1 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 1 |  | a misheard "caí" is not certain: unable to verify at once (Tony 45602) |
| inputs_ks833_ptpt.json:asr_bare_ti | pt | still_unclear | kept as w11 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | [1, 2] |  | KS-881: still unclear after the re-ask is unable_to_verify; "TI" may be a misheard "caí": unable to verify at once (Tony 45602) |
| inputs_ks833_ptpt.json:asr_nao_qi | pt | unclear_then_fine | kept as w5 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | [2, 3] |  | kept from KS-833: fine only after two spoken answers |
| inputs_ks833_ptpt.json:asr_na_na | pt | still_unclear | kept as w10 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_ks833_ptpt.json:asr_maguinada | pt | unclear_then_fine | kept as w6 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | [2, 3] |  | kept from KS-833: fine only after two spoken answers |
| inputs_v1.json:scenario_016 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_023 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_029 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_034 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_045 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_059 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_061 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_063 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_068 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_077 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_094 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_098 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_036 | en | fell_and_help | kept as w5 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | 1 |  |  |
| inputs_v1.json:scenario_002 | en | fell | kept as w7 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_007 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_040 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_056 | en | fell | kept as w8 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_083 | en | fell | kept as w9 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_088 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_092 | en | fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | slipped / tripped / collapsed: a fall, or hurt without saying "fell" |
| inputs_v1.json:scenario_021 | en | hurt_no_fall | kept as w6 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; the injury may be read as a fall |
| inputs_v1.json:scenario_048 | en | hurt_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; the injury may be read as a fall |
| inputs_v1.json:scenario_051 | en | hurt_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; the injury may be read as a fall |
| inputs_v1.json:scenario_074 | en | hurt_no_fall | kept as w7 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; the injury may be read as a fall |
| inputs_v1.json:scenario_012 | en | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested (the first answer asks for help; "I fell" comes too late) |
| inputs_v1.json:scenario_043 | en | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested (the first answer asks for help; "I fell" comes too late) |
| inputs_v1.json:scenario_050 | en | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested (the first answer asks for help; "I fell" comes too late) |
| inputs_v1.json:scenario_066 | en | asks_help | kept as w5 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested (the first answer asks for help; "I fell" comes too late) |
| inputs_v1.json:scenario_086 | en | asks_help | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested (the first answer asks for help; "I fell" comes too late) |
| inputs_v1.json:scenario_009 | en | unwell_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_025 | en | unwell_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_031 | en | unwell_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_038 | en | unwell_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_070 | en | unwell_no_fall | kept as w5 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | [1, 2] |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested; the first answer is vague enough to ask what is wrong |
| inputs_v1.json:scenario_075 | en | unwell_no_fall | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 1 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_003 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_006 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_008 | en | fine_confirmed | kept as w4 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_010 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_015 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_018 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_020 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_026 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_030 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_035 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_039 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_042 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_047 | en | fine_confirmed | kept as w5 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_052 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_055 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_058 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_062 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_067 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_069 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_073 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_076 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_079 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_082 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_085 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_089 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_096 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_100 | en | fine_confirmed | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_022 | en | denial_then_fine | covered by situation | no_fall_confirmed | no_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_011 | en | fine_then_pain | covered by situation | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_080 | en | fine_then_pain | kept as w4 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_001 | en | fine_then_fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_014 | en | fine_then_fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_060 | en | fine_then_fell | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_090 | en | fine_then_fell | kept as w4 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | 2 |  |  |
| inputs_v1.json:scenario_054 | en | unclear_then_fell | kept as w4 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | the first answer implies a fall without saying it; acting at once is also right |
| inputs_v1.json:scenario_072 | en | unclear_then_fell | kept as w5 (en, pt, he) | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | the first answer implies a fall without saying it; acting at once is also right |
| inputs_v1.json:scenario_037 | en | unclear_then_fine | covered by situation | no_fall_confirmed | no_fall_confirmed | 3 |  | FR v3 D16: unclear, then clearly okay, is no alert |
| inputs_v1.json:scenario_091 | en | unclear_then_fine | covered by situation | no_fall_confirmed | no_fall_confirmed | 3 |  | FR v3 D16: unclear, then clearly okay, is no alert |
| inputs_v1.json:scenario_093 | en | unclear_then_fine | covered by situation | no_fall_confirmed | no_fall_confirmed | [2, 3] |  | the first answer may get the re-ask; the confirming question after a first "I'm fine" needs a reply |
| inputs_v1.json:scenario_097 | en | unclear_then_fine | kept as w4 (en, pt, he) | no_fall_confirmed | no_fall_confirmed | [2, 3] |  | the first answer may get the re-ask; the confirming question after a first "I'm fine" needs a reply |
| inputs_v1.json:scenario_071 | en | silence_then_problem | covered by situation | distress_fall_confirmed | distress_fall_confirmed | 2 |  | KS-881: the first silence gets the re-ask |
| inputs_v1.json:scenario_081 | en | silence_then_problem | kept as w3 (en, pt, he) | distress_fall_confirmed | **distress_assistance_requested** | 2 |  | KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested |
| inputs_v1.json:scenario_064 | en | silence_then_fine | covered by situation | no_fall_confirmed | no_fall_confirmed | 3 |  |  |
| inputs_v1.json:scenario_017 | en | silence_then_fine | covered by situation | distress_fall_confirmed | **no_fall_confirmed** | 3 |  | old expectation was a fall alert; the confirming question after a first "I'm fine" needs a reply |
| inputs_v1.json:scenario_087 | en | silence_then_fine | covered by situation | distress_fall_confirmed | **no_fall_confirmed** | 3 |  | old expectation was a fall alert; the confirming question after a first "I'm fine" needs a reply |
| inputs_v1.json:scenario_099 | en | fine_then_silent | kept as w1 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 3 |  | KS-881: fine, then silent through the confirming question and the re-ask; they spoke, so unable to verify (Tony, NUN-1626 44793) |
| inputs_v1.json:scenario_004 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_013 | en | still_unclear | kept as w7 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_019 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_024 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_027 | en | still_unclear | covered by situation | distress_fall_confirmed | distress_fall_confirmed | [1, 2] |  | "managed to get up by myself" implies the fall; unable to verify is also fair |
| inputs_v1.json:scenario_028 | en | still_unclear | kept as w5 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_032 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_033 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_044 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_046 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_049 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_065 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_078 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_084 | en | still_unclear | kept as w8 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | [2, 3] |  | KS-881: still unclear after the re-ask is unable_to_verify; "I guess so" may get the confirming question first |
| inputs_v1.json:scenario_095 | en | still_unclear | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_057 | en | what_twice | covered by situation | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify |
| inputs_v1.json:scenario_053 | en | mixed_no_restart | kept as w3 (en, pt, he) | distress_fall_confirmed | **distress_unable_to_verify** | 2 |  | KS-881: still unclear after the re-ask is unable_to_verify; the silence used the re-ask |
| inputs_v1.json:scenario_005 | en | silent_twice | covered by situation | distress_fall_confirmed | **no_response_from_resident** | 2 |  | KS-714: silence is no_response_from_resident |
| inputs_v1.json:scenario_041 | en | silent_twice | covered by situation | distress_fall_confirmed | **no_response_from_resident** | 2 |  | KS-714: silence is no_response_from_resident |
