# KS-833 pt-PT eval: v3_female

2026-10-08T16:23:59 | gpt-4o | temperature=None | prompt=prompt_ks833_ptpt_v3_female.txt | inputs=inputs_ks833_ptpt.json | runs=2

| Pass | Outcome | Language | Unsafe clears | p50 ms | p95 ms | Errors |
|---|---|---|---|---|---|---|
| 43/58 (74%) | 76% | 97% | 1 | 1155 | 1883 | 0 |

Unsafe clear = a fall/unclear/silence scenario closed as no_fall_confirmed.

## By scenario

| Scenario | Pass | Outcome ok | Language ok | Outcomes seen |
|---|---|---|---|---|
| safe_estou_bem | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_obrigado | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_gato | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_azorean | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_apanhar | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_sim_nao | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| help_preciso_ajuda | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_casa_de_banho | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_doi_perna | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_socorro | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_nao | 0/2 | 0/2 | 2/2 | no_response_from_resident x2 |
| help_nao_consigo_levantar | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_nossa_senhora | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_fine_then_hip | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_deny_then_admit | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_misrec_sai | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| unclear_offtopic | 0/2 | 0/2 | 1/2 | no_response_from_resident x2 |
| unclear_nao_sei | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| unclear_cut_off | 0/2 | 0/2 | 2/2 | no_response_from_resident x2 |
| unclear_contradiction | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| unclear_english_garble | 0/2 | 0/2 | 2/2 | no_response_from_resident x2 |
| unclear_ha | 0/2 | 0/2 | 2/2 | no_response_from_resident x2 |
| silence_full | 2/2 | 2/2 | 2/2 | no_response_from_resident x2 |
| silence_explicit | 1/2 | 2/2 | 1/2 | no_response_from_resident x2 |
| asr_qi_cozinha | 1/2 | 1/2 | 2/2 | no_response_from_resident x1, distress_fall_confirmed x1 |
| asr_bare_ti | 1/2 | 1/2 | 2/2 | no_response_from_resident x1, distress_fall_confirmed x1 |
| asr_nao_qi | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| asr_na_na | 0/2 | 0/2 | 2/2 | no_response_from_resident x1, no_fall_confirmed x1 |
| asr_maguinada | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |

## Language violations

- missing pt no-response phrase: 2

## Warnings: closing line promises help is coming (6/58 runs)

- `help_nao#0`: promises help: 'em breve'
- `help_fine_then_hip#0`: promises help: 'alguém irá'
- `unclear_nao_sei#0`: promises help: 'alguém irá'
- `unclear_contradiction#0`: promises help: 'alguém vai'
- `asr_qi_cozinha#1`: promises help: 'em breve'
- `asr_na_na#0`: promises help: 'em breve'

## Failing runs

- `help_nao#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `help_nao#1` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_offtopic#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_offtopic#1` expected distress_fall_confirmed, got [no_response_from_resident] -> turn 5: missing pt no-response phrase
- `unclear_cut_off#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_cut_off#1` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_english_garble#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_english_garble#1` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_ha#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `unclear_ha#1` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `silence_explicit#0` expected no_response_from_resident, got [no_response_from_resident] -> turn 2: missing pt no-response phrase
- `asr_qi_cozinha#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `asr_bare_ti#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `asr_na_na#0` expected distress_fall_confirmed, got [no_response_from_resident] -> wrong outcome
- `asr_na_na#1` expected distress_fall_confirmed, got [no_fall_confirmed] -> wrong outcome

## Transcripts (first run of each scenario)

### safe_estou_bem — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem.
- **VEGA**: Ainda bem, mas só para confirmar, consegue levantar-se sem problemas?
- **SENIOR**: Não, não me magoei.
- **VEGA**: Fico contente em saber que está tudo bem, senhora Maria. Cuide-se bem, e estou sempre aqui se precisar de algo. Tenha uma boa tarde!

### safe_obrigado — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim, estou bem, obrigado.
- **VEGA**: Fico contente de ouvir isso, mas só para ter certeza, consegue levantar-se sem problemas?
- **SENIOR**: Não me dói nada, estou de pé.
- **VEGA**: Que bom saber que está bem e de pé! Se precisar de alguma coisa, não hesite em dizer. Tenha um bom dia, senhora Maria!

### safe_gato — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Está tudo bem, foi o gato que deitou a cadeira abaixo.
- **VEGA**: Ainda bem que está tudo bem. A senhora magoou-se ou precisa de ajuda para se levantar?
- **SENIOR**: Não, não caí, eu estou bem.
- **VEGA**: Fico contente por saber que está tudo bem, senhora Maria. Se precisar de algo, estou aqui para ajudar. Desejo-lhe um bom dia!

### safe_azorean — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: tou bem tou bem
- **VEGA**: Fico contente de saber que está bem. Consegue levantar-se ou precisa de alguma ajuda?
- **SENIOR**: nã nã me magoei nada
- **VEGA**: Fico aliviada por saber que está tudo bem e que não se magoou. Cuide-se e, caso precise de algo, estou aqui para ajudar.

### safe_apanhar — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não caí, estava só a apanhar uma coisa do chão.
- **VEGA**: Que bom ouvir isso! A senhora está-se a sentir bem e não precisa de ajuda para se levantar ou alguma outra coisa?
- **SENIOR**: Sim, estou bem.
- **VEGA**: Fico contente em saber que está tudo bem. Tenha um bom dia, senhora Maria. Até à próxima!

### safe_sim_nao — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim.
- **VEGA**: Fico contente por ouvir isso. A senhora consegue levantar-se sem dificuldade?
- **SENIOR**: Não, não me magoei.
- **VEGA**: Que bom saber que não se magoou. Mantenha-se segura. Se precisar de algo, estou aqui para ajudar.

### help_preciso_ajuda — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Preciso de ajuda.
- **VEGA**: Lamento saber disso, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo. Adeus.

### help_casa_de_banho — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Recebi uma notificação de que pode ter ocorrido uma queda. Está tudo bem com a senhora?
- **SENIOR**: Caí na casa de banho.
- **VEGA**: Lamento saber que caiu, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Por favor, fique onde está, vou ficar consigo. Tenha calma.

### help_doi_perna — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Ai, dói-me muito a perna.
- **VEGA**: Lamento saber que se magoou, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo. Adeus e cuide-se bem.

### help_socorro — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Socorro.
- **VEGA**: Sinto muito em saber que precisa de ajuda. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha a calma, estou aqui consigo. Adeus e espero que tudo fique bem.

### help_nao — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não.
- **VEGA**: Entendo, senhora Maria. Está magoada ou precisa de ajuda?
- **SENIOR**: (silence)
- **VEGA**: Senhora Maria, não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que tudo fique bem em breve. Adeus, cuide-se.

### help_nao_consigo_levantar — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: caí não me consigo levantar
- **VEGA**: Lamento muito ouvir isso, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, vou ficar consigo enquanto está a chegar ajuda. Cuide-se, por favor. Adeus!

### help_nossa_senhora — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: ai minha nossa senhora caí aqui
- **VEGA**: Lamento muito ouvir isso, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo. Adeus e cuide-se.

### help_fine_then_hip — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem.
- **VEGA**: Fico contente em saber que está bem. Só para confirmar, machucou-se em algum lugar ou consegue levantar-se sem dificuldade?
- **SENIOR**: Não... dói-me um bocadinho a anca.
- **VEGA**: Lamento saber que a sua anca dói. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se calma, alguém irá verificar como está. Cuide-se, senhora Maria.

### help_deny_then_admit — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem, estou bem.
- **VEGA**: Fico contente por saber que está bem, senhora Maria. Consegue levantar-se bem ou precisa de alguma ajuda?
- **SENIOR**: Bem, caí um bocadinho, mas não é nada.
- **VEGA**: Sinto muito por saber isso, senhora Maria. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha-se calma. Adeus, e cuidem-se.

### help_misrec_sai — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: saí do sofá e boi muito
- **VEGA**: Lamento saber que está a doer. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, eu estou aqui consigo. Adeus.

### unclear_offtopic — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: A minha filha vem amanhã com os meninos.
- **VEGA**: Fico contente por saber que a sua filha vem amanhã. E quanto à possibilidade de ter caído, está a sentir-se bem? Consegue mexer-se bem ou precisa de ajuda?
- **SENIOR**: A mesa ao pé da janela, a da cozinha.
- **VEGA**: Compreendo, mas estou um pouco preocupada com a possibilidade de ter caído. Pode confirmar-me se está tudo bem consigo? Se não me responder, vou precisar de alertar os seus cuidadores.
- **SENIOR**: Pois, era o que eu dizia.
- **VEGA**: Peço desculpa, não percebi bem o que estava a dizer. Só para confirmar, a senhora está mesmo bem ou precisa de assistência?
- **SENIOR**: (silence)
- **VEGA**: Como não consegui falar consigo, vou avisar os seus cuidadores para garantir que tudo está bem. Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Cuide-se bem, senhora Maria.

### unclear_nao_sei — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não sei.
- **VEGA**: Não tem problema, senhora Maria. Consegue dizer-me se sente alguma dor ou se conseguiu levantar-se?
- **SENIOR**: Não sei bem.
- **VEGA**: Não se preocupe, estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, alguém irá ajudá-la em breve. Adeus, senhora Maria.

### unclear_cut_off — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim, estou bem, mas eu
- **VEGA**: Desculpe, parece que não consegui ouvir tudo. A senhora está bem e consegue levantar-se sem ajuda?
- **SENIOR**: a perna
- **VEGA**: Parece que foi interrompida. Pode repetir o que disse sobre a perna? Estou aqui para ajudar.
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Cuide-se bem, senhora Maria. Até breve!

### unclear_contradiction — [distress_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem... não, não estou.
- **VEGA**: Desculpe, parece que está com dificuldades. Vou enviar um alerta para os seus cuidadores imediatamente. Estou a enviar um alerta no sistema SeniorMatics. Por favor, fique onde está, alguém vai ajudar em breve. Cuide-se, adeus querido.

### unclear_english_garble — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: the story topology is the island of the government slowly
- **VEGA**: Desculpe, não percebi. Pode repetir? Está a senhora bem?
- **SENIOR**: and the more is the way
- **VEGA**: Estou preocupada porque não consegui entender bem o que a senhora disse. Pode, por favor, confirmar se está bem ou se precisa de ajuda?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Tome cuidado, espero que esteja bem. Adeus.

### unclear_ha — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Hã?
- **VEGA**: Desculpe, não percebi. Pode repetir? Está bem, senhora Maria?
- **SENIOR**: Hã? O quê?
- **VEGA**: Senhora Maria, queria apenas confirmar se está bem. Pode dizer-me se precisa de ajuda ou se está magoada?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Fique descansada, estamos cá para ajudar. Adeus, senhora Maria.

### silence_full — [no_response_from_resident] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Cuide-se e até breve.

### silence_explicit — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: (silence)
- **VEGA**: Como não consegui ouvir uma resposta da senhora, estou a avisar os seus cuidadores. Despeço-me com carinho e espero que esteja tudo bem.

### asr_qi_cozinha — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: QI na cozinha.
- **VEGA**: Entendi que disse algo sobre "caí na cozinha". Só para confirmar, está magoada ou precisa de ajuda?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Fique tranquila, a senhora Maria. Adeus.

### asr_bare_ti — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: TI.
- **VEGA**: Desculpe, não percebi bem o que disse. Pode confirmar se a senhora está bem? Consegue levantar-se sem ajuda?
- **SENIOR**: TI.
- **VEGA**: Parece que não consegui perceber muito bem a última resposta. Pode repetir, por favor? A senhora está bem?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que esteja tudo bem. Adeus, senhora Maria.

### asr_nao_qi — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não QI.
- **VEGA**: Desculpe, disse que não caiu? Só quero ter a certeza de que está tudo bem consigo.
- **SENIOR**: Sim, não caí, estou bem.
- **VEGA**: Ainda bem que está tudo bem, senhora Maria. Se precisar de alguma coisa, estou aqui. Tenha um bom dia!

### asr_na_na — [no_response_from_resident] FAIL
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Na na.
- **VEGA**: Desculpe, disse que não caiu? Consegue levantar-se e está a sentir-se bem?
- **SENIOR**: Na na.
- **VEGA**: Desculpe, não percebi bem. Está mesmo tudo bem ou há algo que esteja a precisar de ajuda?
- **SENIOR**: (silence)
- **VEGA**: Senhora Maria, não consegui falar consigo, por isso estou a avisar os seus cuidadores. Mantenha-se calma, alguém estará a par da situação em breve. Cuide-se.

### asr_maguinada — [no_fall_confirmed] PASS
- **VEGA**: Olá, senhora Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Na Na maguinada.
- **VEGA**: Desculpe, disse que não se magoou? Por favor, confirme para eu ter certeza de que está tudo bem.
- **SENIOR**: Estou bem, não me magoei nada.
- **VEGA**: Fico contente por ouvir que está bem e não se magoou. Se precisar de algo, estou aqui. Cuide-se, senhora Maria!

