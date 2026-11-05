# KS-881 eval: v8k_real_en_t1_gpt-6-sol — FAIL

2026-11-04T11:00:54 | gpt-6-sol | temperature=None | prompt=v8k_java | en | inputs_ks881_realistic_en.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 517/518 | 517/518 | 1127 | 1467 | 0 | $1.68 |

Cost: list price, cached input at the cached price (3865423 of 3973070 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| real_f | fall: F | distress_fall_confirmed@1 | 48/48 | 48/48 | distress_fall_confirmed@1 x48 |
| real_fh | fall: FH | distress_fall_confirmed@1 | 19/19 | 19/19 | distress_fall_confirmed@1 x19 |
| real_mis_yf | fall: MIS > YF | distress_fall_confirmed@[1, 2] | 19/19 | 19/19 | distress_fall_confirmed@1 x19 |
| real_u_f | fall: U > F | distress_fall_confirmed@2 | 17/17 | 17/17 | distress_fall_confirmed@2 x17 |
| real_s_f | fall: S > F | distress_fall_confirmed@2 | 14/14 | 14/14 | distress_fall_confirmed@2 x14 |
| real_ho_f | fall: HO > F | distress_fall_confirmed@2 | 10/10 | 10/10 | distress_fall_confirmed@2 x10 |
| real_ho_s_f | fall: HO > S > F | distress_fall_confirmed@3 | 7/7 | 7/7 | distress_fall_confirmed@3 x7 |
| real_fi_cfall | fall: FI > CFALL | distress_fall_confirmed@2 | 10/10 | 10/10 | distress_fall_confirmed@2 x10 |
| real_uns_f | fall: UNS > F | distress_fall_confirmed@2 | 10/10 | 10/10 | distress_fall_confirmed@2 x10 |
| real_h | help: H | distress_assistance_requested@1 | 41/41 | 41/41 | distress_assistance_requested@1 x41 |
| real_u_h | help: U > H | distress_assistance_requested@2 | 12/12 | 12/12 | distress_assistance_requested@2 x12 |
| real_s_h | help: S > H | distress_assistance_requested@2 | 10/10 | 10/10 | distress_assistance_requested@2 x10 |
| real_fi_cp | help: FI > CP | distress_assistance_requested@2 | 24/24 | 24/24 | distress_assistance_requested@2 x24 |
| real_d_cp | help: D > CP | distress_assistance_requested@2 | 10/10 | 10/10 | distress_assistance_requested@2 x10 |
| real_uns_h | help: UNS > H | distress_assistance_requested@2 | 10/10 | 10/10 | distress_assistance_requested@2 x10 |
| real_ho_h | help: HO > H | distress_assistance_requested@2 | 6/6 | 6/6 | distress_assistance_requested@2 x6 |
| real_fi_cf | fine: FI > CF | no_fall_confirmed@2 | 72/72 | 72/72 | no_fall_confirmed@2 x72 |
| real_d_cf | fine: D > CF | no_fall_confirmed@2 | 29/29 | 29/29 | no_fall_confirmed@2 x29 |
| real_u_fi_cf | fine: U > FI > CF | no_fall_confirmed@3 | 13/14 | 13/14 | no_fall_confirmed@2 x1, no_fall_confirmed@3 x13 |
| real_s_fi_cf | fine: S > FI > CF | no_fall_confirmed@3 | 14/14 | 14/14 | no_fall_confirmed@3 x14 |
| real_ho_fi_cf | fine: HO > FI > CF | no_fall_confirmed@3 | 10/10 | 10/10 | no_fall_confirmed@3 x10 |
| real_ho_s_fi_cf | fine: HO > S > FI > CF | no_fall_confirmed@4 | 10/10 | 10/10 | no_fall_confirmed@4 x10 |
| real_uns_fi_cf | fine: UNS > FI > CF | no_fall_confirmed@3 | 10/10 | 10/10 | no_fall_confirmed@3 x10 |
| real_u_u | unclear: U > U | distress_unable_to_verify@2 | 14/14 | 14/14 | distress_unable_to_verify@2 x14 |
| real_fi_s_s | unclear: FI > S > S | distress_unable_to_verify@3 | 7/7 | 7/7 | distress_unable_to_verify@3 x7 |
| real_uns_uns | unclear: UNS > UNS | distress_unable_to_verify@2 | 10/10 | 10/10 | distress_unable_to_verify@2 x10 |
| real_s_s | silent: S > S | no_response_from_resident@2 | 14/14 | 14/14 | no_response_from_resident@2 x14 |
| real_unk_uf | fall: UF | distress_fall_confirmed@1 | 10/10 | 10/10 | distress_fall_confirmed@1 x10 |
| real_unk_u_uf | fall: U > UF | distress_fall_confirmed@2 | 6/6 | 6/6 | distress_fall_confirmed@2 x6 |
| real_unk_uh | help: UH | distress_assistance_requested@1 | 8/8 | 8/8 | distress_assistance_requested@1 x8 |
| real_unk_u_uh | help: U > UH | distress_assistance_requested@2 | 4/4 | 4/4 | distress_assistance_requested@2 x4 |
| real_unk_ufine_ucf | fine: UFINE > UCF | no_fall_confirmed@2 | 12/12 | 12/12 | no_fall_confirmed@2 x12 |
| real_unk_u_u | unclear: U > U | distress_unable_to_verify@2 | 4/4 | 4/4 | distress_unable_to_verify@2 x4 |
| real_unk_s_s | silent: S > S | no_response_from_resident@2 | 3/3 | 3/3 | no_response_from_resident@2 x3 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `real_u_fi_cf/w13#0`: closed after 2 answer(s), expected 3 (closed early: skipped the re-ask or the confirming question) — Vega: "Hi Jake, it's Vega. I received a fall alert. Are you okay? / Hi Jake, it's Vega. I received a fall alert. Are you okay? / I'm glad you're okay, Jake. Goodbye."

## Warnings

