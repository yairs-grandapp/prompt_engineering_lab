# KS-881 eval: v8l_real_pt_alerts_gpt-6-sol — PASS

2026-11-05T11:23:00 | gpt-6-sol | temperature=None | prompt=v8l_java | pt | inputs_ks881_realistic_pt.json | runs=1

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 295/295 | 295/295 | 1496 | 2484 | 0 | $1.37 |

Cost: list price, cached input at the cached price (2505013 of 2574046 input tokens cached).

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
| real_unk_uf | fall: UF | distress_fall_confirmed@1 | 10/10 | 10/10 | distress_fall_confirmed@1 x10 |
| real_unk_u_uf | fall: U > UF | distress_fall_confirmed@2 | 6/6 | 6/6 | distress_fall_confirmed@2 x6 |
| real_unk_uh | help: UH | distress_assistance_requested@1 | 8/8 | 8/8 | distress_assistance_requested@1 x8 |
| real_unk_u_uh | help: U > UH | distress_assistance_requested@2 | 4/4 | 4/4 | distress_assistance_requested@2 x4 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures


## Warnings

