# KS-833 pt-PT eval: v1_female

2026-10-08T16:18:13 | gpt-4o | temperature=None | prompt=prompt_ks833_ptpt_v1_female.txt | inputs=inputs_ks833_ptpt.json | runs=1

| Pass | Outcome | Language | Unsafe clears | p50 ms | p95 ms | Errors |
|---|---|---|---|---|---|---|
| 19/29 (66%) | 72% | 90% | 0 | 1192 | 2033 | 4 |

Unsafe clear = a fall/unclear/silence scenario closed as no_fall_confirmed.

## By scenario

| Scenario | Pass | Outcome ok | Language ok | Outcomes seen |
|---|---|---|---|---|
| safe_estou_bem | 1/1 | 1/1 | 1/1 | no_fall_confirmed x1 |
| safe_obrigado | 0/1 | 0/1 | 1/1 | ERROR x1 |
| safe_gato | 1/1 | 1/1 | 1/1 | no_fall_confirmed x1 |
| safe_azorean | 0/1 | 0/1 | 1/1 | ERROR x1 |
| safe_apanhar | 1/1 | 1/1 | 1/1 | no_fall_confirmed x1 |
| safe_sim_nao | 1/1 | 1/1 | 1/1 | no_fall_confirmed x1 |
| help_preciso_ajuda | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_casa_de_banho | 0/1 | 0/1 | 1/1 | ERROR x1 |
| help_doi_perna | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_socorro | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_nao | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_nao_consigo_levantar | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_nossa_senhora | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_fine_then_hip | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_deny_then_admit | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| help_misrec_sai | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| unclear_offtopic | 0/1 | 0/1 | 0/1 | no_response_from_resident x1 |
| unclear_nao_sei | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| unclear_cut_off | 0/1 | 0/1 | 1/1 | no_response_from_resident x1 |
| unclear_contradiction | 0/1 | 0/1 | 1/1 | ERROR x1 |
| unclear_english_garble | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| unclear_ha | 0/1 | 1/1 | 0/1 | distress_fall_confirmed x1 |
| silence_full | 1/1 | 1/1 | 1/1 | no_response_from_resident x1 |
| silence_explicit | 1/1 | 1/1 | 1/1 | no_response_from_resident x1 |
| asr_qi_cozinha | 0/1 | 0/1 | 1/1 | no_response_from_resident x1 |
| asr_bare_ti | 0/1 | 0/1 | 1/1 | no_response_from_resident x1 |
| asr_nao_qi | 1/1 | 1/1 | 1/1 | no_fall_confirmed x1 |
| asr_na_na | 1/1 | 1/1 | 1/1 | distress_fall_confirmed x1 |
| asr_maguinada | 1/1 | 1/1 | 1/1 | no_fall_confirmed x1 |

## Language violations

- closing line ends on a question: 2
- missing pt alert phrase: 2
- missing pt no-response phrase: 1

## Warnings: closing line promises help is coming (1/29 runs)

- `unclear_nao_sei#0`: promises help: 'em breve'

## Failing runs

- `safe_obrigado#0` expected no_fall_confirmed, got [ERROR] -> wrong outcome
- `safe_azorean#0` expected no_fall_confirmed, got [ERROR] -> wrong outcome
- `help_casa_de_banho#0` expected distress_fall_confirmed, got [ERROR] -> wrong outcome
- `unclear_offtopic#0` expected distress_fall_confirmed, got [no_response_from_resident] -> turn 5: missing pt no-response phrase
- `unclear_cut_off#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_contradiction#0` expected distress_fall_confirmed, got [ERROR] -> wrong outcome
- `unclear_english_garble#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 3: closing line ends on a question; turn 3: missing pt alert phrase
- `unclear_ha#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 3: closing line ends on a question; turn 3: missing pt alert phrase
- `asr_qi_cozinha#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `asr_bare_ti#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome

## Transcripts (first run of each scenario)

### safe_estou_bem — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem.
- **VEGA**: Que bom ouvir isso. Só para confirmar, a senhora não se magoou em parte nenhuma?
- **SENIOR**: Não, não me magoei.
- **VEGA**: Fico feliz em saber que está tudo bem, senhora Maria. Tome cuidado e tenha um bom dia. Se precisar de algo, estou por aqui.

### safe_obrigado — [ERROR] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim, estou bem, obrigado.
- **ERROR**: Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4o in organization org-pgHm4rd1QdeSukC7Z43ZiXJr on tokens per min (TPM): Limit 450000, Used 448125, Requested 4891. Please try again in 402ms. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}

### safe_gato — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Está tudo bem, foi o gato que deitou a cadeira abaixo.
- **VEGA**: Que alívio ouvir isso, senhora Maria! Só para confirmar, consegue levantar-se bem e não se magoou?
- **SENIOR**: Não, não caí, eu estou bem.
- **VEGA**: Estou tão contente por saber que está tudo bem e não se magoou. Cuide-se bem e tenha um ótimo dia! Até à próxima, senhora Maria.

### safe_azorean — [ERROR] FAIL
- **VEGA**: Olá, senhora Maria, é a Vega. Recebi um alerta de queda. Está tudo bem consigo?
- **SENIOR**: tou bem tou bem
- **ERROR**: Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4o in organization org-pgHm4rd1QdeSukC7Z43ZiXJr on tokens per min (TPM): Limit 450000, Used 448200, Requested 4890. Please try again in 412ms. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}

### safe_apanhar — [no_fall_confirmed] PASS
- **VEGA**: Olá, dona Maria, fala a Vega. Detetámos uma possível queda. Está tudo bem?
- **SENIOR**: Não caí, estava só a apanhar uma coisa do chão.
- **VEGA**: Que bom ouvir isso. A senhora está magoada ou precisa de ajuda para se levantar?
- **SENIOR**: Sim, estou bem.
- **VEGA**: Estou aliviada em saber que está tudo bem consigo. Tome cuidado e, se precisar de alguma coisa, estou aqui. Até logo, dona Maria.

### safe_sim_nao — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim.
- **VEGA**: Que bom ouvir isso. Está magoada ou precisa de ajuda para se levantar?
- **SENIOR**: Não, não me magoei.
- **VEGA**: Fico muito contente em saber que está tudo bem. Cuide-se bem e se precisar de algo, estou aqui. Até à próxima, senhora Maria.

### help_preciso_ajuda — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Preciso de ajuda.
- **VEGA**: Lamento ouvir isso. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se calma; estou aqui consigo. Adeus, senhora Maria.

### help_casa_de_banho — [ERROR] FAIL
- **VEGA**: Olá senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Caí na casa de banho.
- **ERROR**: Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4o in organization org-pgHm4rd1QdeSukC7Z43ZiXJr on tokens per min (TPM): Limit 450000, Used 448192, Requested 4890. Please try again in 410ms. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}

### help_doi_perna — [distress_fall_confirmed] PASS
- **VEGA**: Olá senhora Maria, é a Vega. Recebi uma notificação de que talvez tenha caído. Está tudo bem consigo?
- **SENIOR**: Ai, dói-me muito a perna.
- **VEGA**: Sinto muito saber isso. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se onde está e eu ficarei aqui consigo. Cuide-se e esteja em segurança, senhora Maria.

### help_socorro — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Socorro.
- **VEGA**: Entendo, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo. Adeus, cuide-se bem.

### help_nao — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não.
- **VEGA**: Lamento saber isso. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estarei por aqui.

### help_nao_consigo_levantar — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, é a Vega. Detetámos uma possível queda. Está tudo bem consigo?
- **SENIOR**: caí não me consigo levantar
- **VEGA**: Entendo, sinto muito por saber disso. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo e alguém será notificado. Tome cuidado e adeus.

### help_nossa_senhora — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: ai minha nossa senhora caí aqui
- **VEGA**: Lamento muito ouvir isso. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se calma. Eu estou consigo e vou apoiar no que for necessário. Adeus, Maria.

### help_fine_then_hip — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem.
- **VEGA**: Ótimo ouvir isso! Só para ter a certeza, consegue levantar-se sem problemas?
- **SENIOR**: Não... dói-me um bocadinho a anca.
- **VEGA**: Lamento ouvir isso, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Por favor, fique onde está e mantenha-se tranquila.

### help_deny_then_admit — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem, estou bem.
- **VEGA**: Fico contente por saber que está bem. Só queria confirmar, consegue levantar-se sem dificuldade?
- **SENIOR**: Bem, caí um bocadinho, mas não é nada.
- **VEGA**: Entendo, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se calma. Adeus e cuide-se bem.

### help_misrec_sai — [distress_fall_confirmed] PASS
- **VEGA**: Olá senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: saí do sofá e boi muito
- **VEGA**: Lamento saber que a senhora está magoada. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, vou dar seguimento para que alguém venha ao seu auxílio. Cuide-se, estou aqui consigo.

### unclear_offtopic — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: A minha filha vem amanhã com os meninos.
- **VEGA**: Desculpe, não percebi completamente a resposta. Consegue confirmar se está tudo bem ou se precisa de ajuda?
- **SENIOR**: A mesa ao pé da janela, a da cozinha.
- **VEGA**: Desculpe, não percebi bem. Pode confirmar se está tudo bem ou se precisa de ajuda?
- **SENIOR**: Pois, era o que eu dizia.
- **VEGA**: Desculpe a insistência, mas preciso ter a certeza de que está tudo bem. Pode dizer-me se está magoada ou se caiu?
- **SENIOR**: (silence)
- **VEGA**: Como não consegui falar consigo, vou avisar os seus cuidadores. Espero que tudo esteja bem. Adeus, senhora Maria.

### unclear_nao_sei — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não sei.
- **VEGA**: Lamento ouvir isso. Pode dizer-me se sente alguma dor ou se precisa de ajuda?
- **SENIOR**: Não sei bem.
- **VEGA**: Parece que está a ter dificuldades em saber se está bem. Estou a enviar um alerta no sistema SeniorMatics. Mantenha-se calma, senhora Maria, e em breve alguém irá atender à sua situação. Até já.

### unclear_cut_off — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim, estou bem, mas eu
- **VEGA**: Compreendo, senhora Maria. Pode confirmar se consegue levantar-se sozinha ou se se magoou de alguma forma?
- **SENIOR**: a perna
- **VEGA**: Desculpe, não percebi bem. A sua perna está magoada? Pode descrever um pouco mais o que está a sentir?
- **SENIOR**: (silence)
- **VEGA**: Senhora Maria, não consegui ouvir a sua resposta anterior. A sua perna está magoada? Precisa de ajuda?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Por favor, esteja tranquila, irei alertá-los agora. Tenha cuidado.

### unclear_contradiction — [ERROR] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem... não, não estou.
- **ERROR**: Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4o in organization org-pgHm4rd1QdeSukC7Z43ZiXJr on tokens per min (TPM): Limit 450000, Used 448088, Requested 4892. Please try again in 397ms. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}

### unclear_english_garble — [distress_fall_confirmed] FAIL
- **VEGA**: Olá senhora Maria, é a Vega. Detetámos uma possível queda. Está tudo bem consigo?
- **SENIOR**: the story topology is the island of the government slowly
- **VEGA**: Desculpe, não percebi bem. A senhora está bem? Pode confirmar se precisa de ajuda ou se está magoada?
- **SENIOR**: and the more is the way
- **VEGA**: Desculpe, não consegui perceber. A senhora está ferida ou precisa de ajuda?

### unclear_ha — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Hã?
- **VEGA**: Desculpe, não percebi. A senhora está bem ou precisa de alguma ajuda?
- **SENIOR**: Hã? O quê?
- **VEGA**: Desculpe, senhora Maria, não consegui perceber. Estou preocupada consigo. Está ferida ou precisa de ajuda?

### silence_full — [no_response_from_resident] PASS
- **VEGA**: Olá, senhora Maria, é a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Cuide-se bem, senhora Maria, e estou por aqui caso precise de algo.

### silence_explicit — [no_response_from_resident] PASS
- **VEGA**: Olá, senhora Maria, é a Vega! Detetámos uma possível queda. Está tudo bem consigo?
- **SENIOR**: (silence)
- **VEGA**: Senhora Maria, não consegui ouvir a sua resposta. Está tudo bem consigo?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que esteja bem. Adeus, senhora Maria.

### asr_qi_cozinha — [no_response_from_resident] FAIL
- **VEGA**: Olá senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: QI na cozinha.
- **VEGA**: Parece que ouviu "caí na cozinha", por favor confirme se recebeu corretamente. Magoou-se?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Tome cuidado, senhora Maria. Até breve!

### asr_bare_ti — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: TI.
- **VEGA**: Desculpe, não percebi. A senhora pode confirmar se está bem?
- **SENIOR**: TI.
- **VEGA**: Desculpe, continuo a não perceber bem. A senhora consegue dizer-me se se sente magoada ou precisa de ajuda?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que esteja bem. Se precisar de alguma coisa, por favor, lembre-se que estou sempre aqui para ajudar. Até breve.

### asr_nao_qi — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, é a Vega. Detetámos uma possível queda. Está tudo bem?
- **SENIOR**: Não QI.
- **VEGA**: Desculpe, disse que não caiu? Só quero ter a certeza de que está bem.
- **SENIOR**: Sim, não caí, estou bem.
- **VEGA**: Fico contente em saber que está tudo bem. Tenha um bom dia, senhora Maria! Se precisar de algo, estou por aqui.

### asr_na_na — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Na na.
- **VEGA**: Desculpe, disse que não caiu? Só quero ter a certeza de que está tudo bem.
- **SENIOR**: Na na.
- **VEGA**: Terei de alertar os seus cuidadores, pois não consegui entender claramente se realmente está bem. Estou a enviar um alerta no sistema SeniorMatics. Tenha um bom dia e cuide-se bem!

### asr_maguinada — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Na Na maguinada.
- **VEGA**: Desculpe, senhora Maria, quis dizer que não se magoou? Consegue levantar-se ou precisa de ajuda?
- **SENIOR**: Estou bem, não me magoei nada.
- **VEGA**: Fico contente por saber que está bem e que não se magoou. Se precisar de alguma coisa, estou aqui. Tome cuidado e tenha um bom dia!

