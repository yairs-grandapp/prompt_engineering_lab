# KS-881 eval: v8k_sm_pt_hold_gpt-6-sol — FAIL

2026-11-04T10:46:29 | gpt-6-sol | temperature=None | prompt=v8k_java | pt | inputs_ks881_pt.json | runs=3

Pass rule (KS-881 TR v3): every wording passes every run.

| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|
| 7/8 | 22/24 | 1067 | 1637 | 0 | $0.14 |

Cost: list price, cached input at the cached price (356725 of 367530 input tokens cached).

## By scenario

| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |
|---|---|---|---|---|---|
| hold_repeated | v7: keeps saying hold on (no endless loop) | distress_unable_to_verify@3 | 2/2 | 6/6 | distress_unable_to_verify@3 x3, distress_unable_to_verify@4 x3 |
| hold_used_then_hold_again | v7: wait used at the first question, hold on again later | distress_unable_to_verify@5 | 0/1 | 1/3 | distress_unable_to_verify@4 x2, distress_unable_to_verify@5 x1 |
| fine_unsure_then_fine | v7: fine, unsure, then sure | no_fall_confirmed@3 | 3/3 | 9/9 | no_fall_confirmed@3 x9 |
| hold_silent_silent | v7: hold on, silent (free), silent, silent (state machine row 287) | distress_unable_to_verify@4 | 2/2 | 6/6 | distress_unable_to_verify@4 x6 |

`outcome@N` = the outcome and the number of senior answers before the call closed.

## Failures

- `hold_used_then_hold_again/w1#0`: closed after 4 answer(s), expected 5 (closed early: skipped the re-ask or the confirming question) — Vega: 'Olá, Manuel, fala a Vega. Detetámos uma possível queda. Está bem? / Esteja à vontade, Manuel, eu espero. / Está bem? / Precisa de alguma ajuda, Manuel? / Desculpe, não consegui perceber o que disse. A sua segurança é a minha prioridade, por isso estou a enviar um alerta a quem lhe pode prestar ajuda. Vou terminar a chamada agora para dar seguimento ao alerta. Obrigada por falar comigo.'
- `hold_used_then_hold_again/w1#2`: closed after 4 answer(s), expected 5 (closed early: skipped the re-ask or the confirming question) — Vega: 'Olá, Manuel, fala a Vega. Detetámos uma possível queda. Está bem? / Esteja à vontade, Manuel, eu espero. / Está bem? / Precisa de alguma ajuda, Manuel? / Desculpe, não consegui perceber o que disse. A sua segurança é a minha prioridade, por isso estou a enviar um alerta a quem lhe pode prestar ajuda. Vou terminar a chamada agora para dar seguimento ao alerta. Obrigada por falar comigo.'

## Warnings

