# KS-831 eval: baseline_pt_r1

2026-10-13T15:17:57 | gpt-4o | temperature=None | prompt=prompt_ks831_baseline_pt.txt | inputs=inputs_ks833_ptpt.json | runs=1

| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |
|---|---|---|---|---|---|---|
| 0/29 (0%) | 90% | 0% | 1276 | 1886 | 0 | $1.02 |

## By scenario

| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |
|---|---|---|---|---|
| safe_estou_bem | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |
| safe_obrigado | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |
| safe_gato | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |
| safe_azorean | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |
| safe_apanhar | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |
| safe_sim_nao | 0/1 | 0/1 | 0/1 | distress_fall_confirmed x1 |
| help_preciso_ajuda | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_casa_de_banho | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_doi_perna | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_socorro | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_nao | 0/1 | 0/1 | 0/1 | no_response_from_resident x1 |
| help_nao_consigo_levantar | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_nossa_senhora | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_fine_then_hip | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_deny_then_admit | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| help_misrec_sai | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| unclear_offtopic | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| unclear_nao_sei | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| unclear_cut_off | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| unclear_contradiction | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| unclear_english_garble | 0/1 | 0/1 | 0/1 | no_response_from_resident x1 |
| unclear_ha | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| silence_full | 0/1 | 1/1 | 0/1 | no_response_from_resident x1 |
| silence_explicit | 0/1 | 1/1 | 0/1 | no_response_from_resident x1 |
| asr_qi_cozinha | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| asr_bare_ti | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| asr_nao_qi | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |
| asr_na_na | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| asr_maguinada | 0/1 | 1/1 | 0/1 | no_fall_confirmed x1 |

## Goodbye violations

- does not end with 'adeus': 27
- invites reply: 26
- missing alert phrase: 5
- could-not-reach: 4
- promise: 2
- N sentences: 2

## Warnings (8)

- 'I fell' call without 'sorry': 4
- unclear call without 'trouble understanding': 4

## Failing goodbyes

- `safe_estou_bem#0` [no_fall_confirmed] 'Estou mesmo feliz por ouvir que está tudo bem, Manuel. Cuide-se, e se precisar de alguma coisa, estou por aqui. Até já!' -> invites reply: 'se precisar'; does not end with 'adeus'
- `safe_obrigado#0` [no_fall_confirmed] 'Fico muito contente por saber que está tudo bem consigo. Tenha um resto de dia excelente, Manuel. Se precisar de algo, estou aqui para ajudar.' -> invites reply: 'se precisar'; invites reply: 'estou aqui'; does not end with 'adeus'
- `safe_gato#0` [no_fall_confirmed] 'Ainda bem que está tudo bem, Manuel. Se precisar de alguma coisa, estarei aqui. Tome conta de si e tenha um bom dia!' -> invites reply: 'se precisar'; does not end with 'adeus'
- `safe_azorean#0` [no_fall_confirmed] 'Fico muito contente em saber que está bem e não se magoou, Manuel. Se precisar de alguma coisa, estou por aqui. Tenha um bom dia!' -> invites reply: 'se precisar'; does not end with 'adeus'
- `safe_apanhar#0` [no_fall_confirmed] 'Fico contente em saber que está tudo bem. Cuide-se e, se precisar de algo, estou aqui para ajudar. Até logo!' -> invites reply: 'se precisar'; invites reply: 'estou aqui'; does not end with 'adeus'
- `safe_sim_nao#0` [distress_fall_confirmed] 'Lamento saber que não consegue levantar-se sozinho. Estou a enviar um alerta no sistema SeniorMatics. Fique calmo, e estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `help_preciso_ajuda#0` [distress_fall_confirmed] 'Estou a enviar um alerta no sistema SeniorMatics. Fique com calma, estou aqui consigo, adeus.' -> invites reply: 'estou aqui'
- `help_casa_de_banho#0` [distress_fall_confirmed] 'Lamento saber que caiu, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Fique com calma, estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `help_doi_perna#0` [distress_fall_confirmed] 'Lamento muito que se tenha magoado. Estou a enviar um alerta no sistema SeniorMatics. Fique calmo, alguém estará consigo em breve. Despeço-me com carinho.' -> promise: 'em breve'; does not end with 'adeus'
- `help_socorro#0` [distress_fall_confirmed] 'Estou a enviar um alerta no sistema SeniorMatics. Fique comigo, estou aqui. Adeus, Manuel.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `help_nao#0` [no_response_from_resident] 'Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que tudo fique bem, Manuel. Até breve.' -> could-not-reach; does not end with 'adeus'; missing alert phrase
- `help_nao_consigo_levantar#0` [distress_fall_confirmed] 'Lamento saber que caiu e não consegue levantar-se. Estou a enviar um alerta no sistema SeniorMatics. Fique com calma, estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `help_nossa_senhora#0` [distress_fall_confirmed] 'Sinto muito em saber que caiu, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Fique calmo, vou estar consigo, e tratarei de avisar os seus cuidadores. Adeus e cuide-se.' -> does not end with 'adeus'
- `help_fine_then_hip#0` [distress_fall_confirmed] 'Lamento saber disso, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Fique calmo, e estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `help_deny_then_admit#0` [distress_fall_confirmed] 'Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha a calma, vou ficar aqui consigo. Adeus, Manuel.' -> does not end with 'adeus'
- `help_misrec_sai#0` [distress_fall_confirmed] 'Lamento saber que tem dores. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se tranquilo, estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `unclear_offtopic#0` [distress_fall_confirmed] 'Lamento, não estou a perceber se precisa de ajuda. Diga-me se está tudo bem consigo ou se magoou-se, por favor.' -> invites reply: 'diga-me'; does not end with 'adeus'; missing alert phrase
- `unclear_nao_sei#0` [distress_fall_confirmed] 'Não se preocupe, Manuel. Estou a enviar um alerta no sistema SeniorMatics. Fique calmo, estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `unclear_cut_off#0` [distress_fall_confirmed] 'Parece que houve um problema com a sua perna. Estou a enviar um alerta no sistema SeniorMatics. Fique calmo, estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `unclear_contradiction#0` [distress_fall_confirmed] 'Lamento ouvir isso, Manuel. Estou aqui para ajudar. Estou a enviar um alerta no sistema SeniorMatics. Mantenha-se calmo e alguém irá entrar em contacto consigo. Adeus e cuide-se bem.' -> invites reply: 'estou aqui'; promise: 'alguém irá'; 5 sentences; does not end with 'adeus'
- `unclear_english_garble#0` [no_response_from_resident] 'Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que tudo esteja bem. Até breve, Manuel.' -> could-not-reach; does not end with 'adeus'; missing alert phrase
- `unclear_ha#0` [distress_fall_confirmed] 'Não consegui perceber. Parece que há problemas de comunicação. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquilo, estou aqui consigo.' -> invites reply: 'estou aqui'; does not end with 'adeus'
- `silence_full#0` [no_response_from_resident] 'Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Mantenha a calma, estou aqui consigo. Adeus, Manuel!' -> invites reply: 'estou aqui'; could-not-reach; does not end with 'adeus'; missing alert phrase
- `silence_explicit#0` [no_response_from_resident] 'Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Fique descansado, estarei aqui se precisar de alguma coisa. Adeus.' -> invites reply: 'se precisar'; could-not-reach; missing alert phrase
- `asr_qi_cozinha#0` [distress_fall_confirmed] 'Oh, não! Parece que caiu na cozinha. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se calmo, estou aqui consigo. Adeus, Manuel.' -> invites reply: 'estou aqui'; 5 sentences; does not end with 'adeus'
- `asr_bare_ti#0` [distress_fall_confirmed] 'Lamento, mas como não consegui entender a sua resposta, vou enviar um alerta para os seus cuidadores. Estou a enviar um alerta no sistema SeniorMatics. Fique com calma, e desejamos tudo de bom para si.' -> does not end with 'adeus'
- `asr_nao_qi#0` [no_fall_confirmed] 'Fico muito contente por saber que está bem. Se precisar de algo, estou aqui para ajudar. Até logo, Manuel.' -> invites reply: 'se precisar'; invites reply: 'estou aqui'; does not end with 'adeus'
- `asr_na_na#0` [distress_fall_confirmed] 'Estou a enviar um alerta no sistema SeniorMatics. Vou ficar aqui consigo. Cuide-se bem, Manuel.' -> does not end with 'adeus'
- `asr_maguinada#0` [no_fall_confirmed] 'Fico muito contente em saber que está tudo bem consigo. Tenha um ótimo dia, Manuel. Se precisar de alguma coisa, estou aqui.' -> invites reply: 'se precisar'; invites reply: 'estou aqui'; does not end with 'adeus'

## Sample passing goodbyes

