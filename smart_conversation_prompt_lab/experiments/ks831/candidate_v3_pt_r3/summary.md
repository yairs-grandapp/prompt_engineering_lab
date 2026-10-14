# KS-831 eval: candidate_v3_pt_r3

2026-10-13T15:16:23 | gpt-4o | temperature=None | prompt=prompt_ks831_candidate_v3_pt.txt | inputs=inputs_ks833_ptpt.json | runs=3

| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|---|
| 80/87 (92%) | 97% | 95% | 1398 | 2328 | 0 | $3.20 |

## By scenario

| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |
|---|---|---|---|---|
| safe_estou_bem | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |
| safe_obrigado | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |
| safe_gato | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |
| safe_azorean | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |
| safe_apanhar | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |
| safe_sim_nao | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |
| help_preciso_ajuda | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_casa_de_banho | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_doi_perna | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_socorro | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_nao | 2/3 | 2/3 | 3/3 | distress_fall_confirmed x2, no_response_from_resident x1 |
| help_nao_consigo_levantar | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_nossa_senhora | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_fine_then_hip | 2/3 | 3/3 | 2/3 | distress_fall_confirmed x3 |
| help_deny_then_admit | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| help_misrec_sai | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| unclear_offtopic | 2/3 | 2/3 | 3/3 | distress_fall_confirmed x2, no_response_from_resident x1 |
| unclear_nao_sei | 2/3 | 3/3 | 2/3 | distress_fall_confirmed x3 |
| unclear_cut_off | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| unclear_contradiction | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| unclear_english_garble | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| unclear_ha | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| silence_full | 3/3 | 3/3 | 3/3 | no_response_from_resident x3 |
| silence_explicit | 3/3 | 3/3 | 3/3 | no_response_from_resident x3 |
| asr_qi_cozinha | 2/3 | 2/3 | 3/3 | no_response_from_resident x1, distress_fall_confirmed x2 |
| asr_bare_ti | 2/3 | 3/3 | 2/3 | distress_fall_confirmed x3 |
| asr_nao_qi | 2/3 | 3/3 | 2/3 | no_fall_confirmed x3 |
| asr_na_na | 3/3 | 3/3 | 3/3 | distress_fall_confirmed x3 |
| asr_maguinada | 3/3 | 3/3 | 3/3 | no_fall_confirmed x3 |

## Goodbye violations

- invites reply: 2
- does not end with 'adeus': 1
- missing alert phrase: 1
- N sentences: 1

## Warnings (14)

- unclear call without 'trouble understanding': 7
- 'I fell' call without 'sorry': 4
- 'haven't heard from you' said to a senior who spoke: 3

## Failing goodbyes

- `help_nao#1` [no_response_from_resident] 'Não tive resposta sua e a sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.' -> wrong outcome
- `help_fine_then_hip#0` [distress_fall_confirmed] 'Lamento que a anca lhe doa, Manuel. Estou a enviar um alerta no sistema SeniorMatics.' -> does not end with 'adeus'
- `unclear_offtopic#2` [no_response_from_resident] 'Não tive resposta sua e a sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.' -> wrong outcome
- `unclear_nao_sei#0` [distress_fall_confirmed] 'Estou a ter alguma dificuldade em perceber. Estou preocupada com a sua segurança, por isso vou enviar um alerta no sistema SeniorMatics. Por favor cuide-se, Manuel. Adeus.' -> missing alert phrase
- `asr_qi_cozinha#0` [no_response_from_resident] 'Não tive resposta sua e a sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.' -> wrong outcome
- `asr_bare_ti#0` [distress_fall_confirmed] 'Estou com dificuldades em perceber o que está a dizer, Manuel. A sua segurança é a minha prioridade. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide de si. Adeus.' -> 5 sentences
- `asr_nao_qi#0` [no_fall_confirmed] 'Fico contente por saber que está tudo bem. Se precisar de algo, estou aqui. Adeus.' -> invites reply: 'se precisar'; invites reply: 'estou aqui'

## Sample passing goodbyes

- `safe_estou_bem` [no_fall_confirmed] 'Fico feliz por saber que está tudo bem. Tenha um ótimo dia, Manuel. Adeus.'
- `safe_obrigado` [no_fall_confirmed] 'Fico feliz em saber que está tudo bem. Tome cuidado. Adeus.'
- `safe_gato` [no_fall_confirmed] 'Estou feliz por saber que não se magoou. Agradeço por confirmar. Até à próxima, Manuel. Adeus.'
- `safe_azorean` [no_fall_confirmed] 'Estou feliz por saber que está tudo bem. Cuide-se. Adeus.'
- `safe_apanhar` [no_fall_confirmed] 'Que bom saber que está tudo bem. Fico contente. Cuide-se bem. Adeus.'
- `safe_sim_nao` [no_fall_confirmed] 'Estou contente por saber que não se magoou. Tenha um bom dia, Manuel. Adeus.'
- `help_preciso_ajuda` [distress_fall_confirmed] 'Lamento que precise de ajuda, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.'
- `help_casa_de_banho` [distress_fall_confirmed] 'Lamento que tenha caído, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `help_doi_perna` [distress_fall_confirmed] 'Lamento que a sua perna esteja a doer, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `help_socorro` [distress_fall_confirmed] 'Lamento que precise de ajuda, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `help_nao` [distress_fall_confirmed] 'Lamento saber Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `help_nao_consigo_levantar` [distress_fall_confirmed] 'Sinto muito que tenha caído, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, fique com calma. Adeus.'
- `help_nossa_senhora` [distress_fall_confirmed] 'Lamento que tenha caído, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `help_fine_then_hip` [distress_fall_confirmed] 'Lamento saber que tem dores na anca, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `help_deny_then_admit` [distress_fall_confirmed] 'Lamento que tenha caído, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.'
- `help_misrec_sai` [distress_fall_confirmed] 'Estou a compreender que se magoou. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.'
- `unclear_offtopic` [distress_fall_confirmed] 'Estou com dificuldades em perceber a sua resposta, Manuel. A sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.'
- `unclear_nao_sei` [distress_fall_confirmed] 'Estou a ter dificuldade em perceber, Manuel. A sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `unclear_cut_off` [distress_fall_confirmed] 'Lamento que a sua perna esteja a causar desconforto, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor cuide-se. Adeus.'
- `unclear_contradiction` [distress_fall_confirmed] 'Desculpe ouvir isso, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `unclear_english_garble` [distress_fall_confirmed] 'Estou a ter dificuldades em compreender o que está a dizer, Manuel. A sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.'
- `unclear_ha` [distress_fall_confirmed] 'Estou a ter dificuldade em perceber, Manuel. A sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide de si. Adeus.'
- `silence_full` [no_response_from_resident] 'Não tive resposta sua e a sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se, Manuel. Adeus.'
- `silence_explicit` [no_response_from_resident] 'Não tive resposta sua e a sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Please take care, Manuel. Adeus.'
- `asr_qi_cozinha` [distress_fall_confirmed] 'Sinto muito que tenha caído, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Por favor, tome cuidado. Adeus.'
- `asr_bare_ti` [distress_fall_confirmed] 'Estou a ter dificuldades em perceber, Manuel. A sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Por favor, cuide-se. Adeus.'
- `asr_nao_qi` [no_fall_confirmed] 'Fico contente por saber que está tudo bem, Manuel. Tenha um bom dia. Adeus.'
- `asr_na_na` [distress_fall_confirmed] 'Estou a ter dificuldades em perceber-lhe, Manuel. A sua segurança é a minha prioridade, por isso estou a enviar um alerta no sistema SeniorMatics. Tome cuidado. Adeus.'
- `asr_maguinada` [no_fall_confirmed] 'Fico contente de saber que está tudo bem. Desejo-lhe um resto de dia tranquilo. Adeus.'
