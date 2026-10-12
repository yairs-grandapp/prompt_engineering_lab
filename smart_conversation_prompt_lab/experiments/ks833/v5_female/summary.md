# KS-833 pt-PT eval: v5_female

2026-10-09T11:20:09 | gpt-4o | temperature=None | prompt=prompt_ks833_ptpt_v5_female.txt | inputs=inputs_ks833_ptpt.json | runs=2

| Pass | Outcome | Language | Unsafe clears | p50 ms | p95 ms | Errors |
|---|---|---|---|---|---|---|
| 45/58 (78%) | 100% | 78% | 0 | 1179 | 2081 | 0 |

Unsafe clear = a fall/unclear/silence scenario closed as no_fall_confirmed.

## By scenario

| Scenario | Pass | Outcome ok | Language ok | Outcomes seen |
|---|---|---|---|---|
| safe_estou_bem | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_obrigado | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_gato | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_azorean | 1/2 | 2/2 | 1/2 | no_fall_confirmed x2 |
| safe_apanhar | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| safe_sim_nao | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| help_preciso_ajuda | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_casa_de_banho | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_doi_perna | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_socorro | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| help_nao | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_nao_consigo_levantar | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_nossa_senhora | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| help_fine_then_hip | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| help_deny_then_admit | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| help_misrec_sai | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| unclear_offtopic | 1/2 | 2/2 | 1/2 | no_response_from_resident x2 |
| unclear_nao_sei | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| unclear_cut_off | 0/2 | 2/2 | 0/2 | distress_fall_confirmed x1, no_response_from_resident x1 |
| unclear_contradiction | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| unclear_english_garble | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x1, no_response_from_resident x1 |
| unclear_ha | 1/2 | 2/2 | 1/2 | distress_fall_confirmed x2 |
| silence_full | 2/2 | 2/2 | 2/2 | no_response_from_resident x2 |
| silence_explicit | 2/2 | 2/2 | 2/2 | no_response_from_resident x2 |
| asr_qi_cozinha | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| asr_bare_ti | 1/2 | 2/2 | 1/2 | no_response_from_resident x1, distress_fall_confirmed x1 |
| asr_nao_qi | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |
| asr_na_na | 2/2 | 2/2 | 2/2 | distress_fall_confirmed x2 |
| asr_maguinada | 2/2 | 2/2 | 2/2 | no_fall_confirmed x2 |

## Language violations

- gendered: 14
- closing line ends on a question: 1
- missing pt alert phrase: 1

## Warnings: closing line promises help is coming (0/58 runs)


## Failing runs

- `safe_azorean#1` expected no_fall_confirmed, got [no_fall_confirmed] -> turn 2: gendered: 'sozinha'
- `help_socorro#1` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 2: gendered: 'tranquila'
- `help_fine_then_hip#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 3: gendered: 'tranquila'
- `help_deny_then_admit#1` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 2: gendered: 'sozinha'
- `help_misrec_sai#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 2: gendered: 'tranquila'
- `unclear_offtopic#1` expected distress_fall_confirmed, got [no_response_from_resident] -> turn 4: gendered: 'magoada'; turn 5: gendered: 'tranquila'
- `unclear_nao_sei#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 2: gendered: 'sozinha'
- `unclear_cut_off#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 2: gendered: 'magoada'; turn 3: gendered: 'tranquila'
- `unclear_cut_off#1` expected distress_fall_confirmed, got [no_response_from_resident] -> turn 5: gendered: 'tranquila'
- `unclear_contradiction#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 2: gendered: 'tranquila'
- `unclear_english_garble#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 3: closing line ends on a question; turn 3: missing pt alert phrase
- `unclear_ha#0` expected distress_fall_confirmed, got [distress_fall_confirmed] -> turn 3: gendered: 'tranquila'
- `asr_bare_ti#0` expected distress_fall_confirmed, got [no_response_from_resident] -> turn 4: gendered: 'tranquila'

## Transcripts (first run of each scenario)

### safe_estou_bem — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem.
- **VEGA**: Fico contente em saber que está bem. Tem a certeza de que não se magoou ou precisa de ajuda?
- **SENIOR**: Não, não me magoei.
- **VEGA**: Estou tão feliz por ouvir isso. Cuide-se, Maria. Se precisar de alguma coisa, estou aqui.

### safe_obrigado — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, é a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim, estou bem, obrigado.
- **VEGA**: Fico contente por ouvir isso. Consegue levantar-se sem dificuldade?
- **SENIOR**: Não me dói nada, estou de pé.
- **VEGA**: Que bom saber que está tudo bem e que está de pé! Se precisar de algo, estarei aqui. Cuide-se bem, Maria.

### safe_gato — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Está tudo bem, foi o gato que deitou a cadeira abaixo.
- **VEGA**: Ainda bem que está tudo bem, mas só para confirmar, não se magoou com a cadeira?
- **SENIOR**: Não, não caí, eu estou bem.
- **VEGA**: Estou tão contente por saber que está tudo bem. Cuide-se, e se precisar de alguma coisa, estou aqui.

### safe_azorean — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: tou bem tou bem
- **VEGA**: Ainda bem que está bem, Maria. Só para confirmar, tem a certeza de que não precisa de ajuda ou de que não se magoou?
- **SENIOR**: nã nã me magoei nada
- **VEGA**: Fico contente por saber que está tudo bem consigo. Cuide-se, Maria. Até breve!

### safe_apanhar — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, é a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não caí, estava só a apanhar uma coisa do chão.
- **VEGA**: Fico contente por ouvir isso. Conseguiu levantar-se sem problema?
- **SENIOR**: Sim, estou bem.
- **VEGA**: Fico contente por saber que está tudo bem. Cuide-se, Maria. Adeus e até à próxima!

### safe_sim_nao — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim.
- **VEGA**: Fico contente por ouvir isso. Só para ter a certeza, consegue levantar-se sem problemas?
- **SENIOR**: Não, não me magoei.
- **VEGA**: Que bom saber que está tudo bem. Não hesite em contactar-me se precisar de alguma coisa. Cuide-se!

### help_preciso_ajuda — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Preciso de ajuda.
- **VEGA**: Compreendo, Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo. Adeus.

### help_casa_de_banho — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Caí na casa de banho.
- **VEGA**: Sinto muito em ouvir isso. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo. Adeus e cuide-se.

### help_doi_perna — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Ai, dói-me muito a perna.
- **VEGA**: Lamento ouvir isso. Estou a enviar um alerta no sistema SeniorMatics. Fique onde está, estou aqui consigo. Até já, Maria.

### help_socorro — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Socorro.
- **VEGA**: Não se preocupe, Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo.

### help_nao — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não.
- **VEGA**: Sinto muito por saber que não está bem. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo.

### help_nao_consigo_levantar — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: caí não me consigo levantar
- **VEGA**: Lamento ouvir isso, Maria. Estou a enviar um alerta no sistema SeniorMatics. Por favor, mantenha a calma. Estou aqui consigo.

### help_nossa_senhora — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: ai minha nossa senhora caí aqui
- **VEGA**: Sinto muito ouvir isso. Estou a enviar um alerta no sistema SeniorMatics. Fique com calma, estou aqui consigo.

### help_fine_then_hip — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem.
- **VEGA**: Fico contente em ouvir isso. Só para confirmar, consegue levantar-se sem problemas?
- **SENIOR**: Não... dói-me um bocadinho a anca.
- **VEGA**: Lamento saber que a sua anca dói. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo.

### help_deny_then_admit — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem, estou bem.
- **VEGA**: Fico contente em ouvir isso. Consegue levantar-se sem problemas?
- **SENIOR**: Bem, caí um bocadinho, mas não é nada.
- **VEGA**: Lamento ouvir que caiu. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo. Adeus, Maria.

### help_misrec_sai — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: saí do sofá e boi muito
- **VEGA**: Lamento ouvir isso. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo.

### unclear_offtopic — [no_response_from_resident] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: A minha filha vem amanhã com os meninos.
- **VEGA**: Isso é ótimo, Maria! Antes de mais, pode dizer-me se se sente bem agora? Magoou-se ou precisa de ajuda?
- **SENIOR**: A mesa ao pé da janela, a da cozinha.
- **VEGA**: Maria, parece que não consegui perceber se está tudo bem. Pode confirmar se se sente bem ou se precisa de ajuda?
- **SENIOR**: Pois, era o que eu dizia.
- **VEGA**: Desculpe, não consegui perceber se está tudo bem. Pode explicar mais uma vez se precisa de ajuda ou se se magoou?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que tudo esteja bem. Até breve, Maria.

### unclear_nao_sei — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não sei.
- **VEGA**: Desculpe ouvir isso. Magoou-se, ou consegue levantar-se sozinha?
- **SENIOR**: Não sei bem.
- **VEGA**: Lamento por estar a passar por isto, Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique onde está e mantenha a calma, estou consigo.

### unclear_cut_off — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Sim, estou bem, mas eu
- **VEGA**: Desculpe, não percebi bem. Quer terminar o que estava a dizer? Está magoada ou consegue levantar-se sem problemas?
- **SENIOR**: a perna
- **VEGA**: Estou preocupada com o que mencionou sobre a perna. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, Maria, estou aqui consigo. Adeus e cuide-se.

### unclear_contradiction — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Estou bem... não, não estou.
- **VEGA**: Lamento saber isso, Maria. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo.

### unclear_english_garble — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: the story topology is the island of the government slowly
- **VEGA**: Desculpe, não percebi. Pode repetir? Está tudo bem consigo?
- **SENIOR**: and the more is the way
- **VEGA**: Lamento, mas não consegui perceber. Precisa de ajuda ou magoou-se?

### unclear_ha — [distress_fall_confirmed] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Hã?
- **VEGA**: Desculpe, Maria, não percebi. Pode me dizer se está bem ou se precisa de ajuda?
- **SENIOR**: Hã? O quê?
- **VEGA**: Maria, não estou a conseguir perceber. Estou a enviar um alerta no sistema SeniorMatics. Fique tranquila, estou aqui consigo e vou avisar os seus cuidadores. Adeus e cuide-se.

### silence_full — [no_response_from_resident] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Fique com calma, estou aqui consigo. Adeus, Maria.

### silence_explicit — [no_response_from_resident] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: (silence)
- **VEGA**: Estou preocupada porque não consegui ouvir a sua resposta. Pode me dizer se está tudo bem?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Espero que esteja bem. Adeus e esteja à vontade para nos contactar se precisar de algo.

### asr_qi_cozinha — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: QI na cozinha.
- **VEGA**: Parece que mencionou uma queda na cozinha. Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo.

### asr_bare_ti — [no_response_from_resident] FAIL
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: TI.
- **VEGA**: Desculpe, não percebi bem. Como é que se sente? Está tudo bem consigo?
- **SENIOR**: TI.
- **VEGA**: Desculpe, continuo sem perceber. Como é que se sente, Maria?
- **SENIOR**: (silence)
- **VEGA**: Não consegui falar consigo, por isso estou a avisar os seus cuidadores. Fique tranquila, estou aqui para ajudar. Adeus, Maria.

### asr_nao_qi — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Não QI.
- **VEGA**: Desculpe, não percebi bem. Pode repetir? Como é que se sente?
- **SENIOR**: Sim, não caí, estou bem.
- **VEGA**: Fico contente por saber que está bem. Caso precise de algo, não hesite em chamar. Cuide-se!

### asr_na_na — [distress_fall_confirmed] PASS
- **VEGA**: Olá, Maria, fala a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Na na.
- **VEGA**: Desculpe, não percebi. Como é que se sente?
- **SENIOR**: Na na.
- **VEGA**: Estou a enviar um alerta no sistema SeniorMatics. Fique calma, estou aqui consigo. Adeus, Maria.

### asr_maguinada — [no_fall_confirmed] PASS
- **VEGA**: Olá, Maria, é a Vega. Detetámos uma possível queda. Está bem?
- **SENIOR**: Na Na maguinada.
- **VEGA**: Desculpe, não percebi bem. Poderia dizer novamente como se sente?
- **SENIOR**: Estou bem, não me magoei nada.
- **VEGA**: Fico feliz em saber que está bem e que não se magoou. Se precisar de alguma coisa, estou aqui. Cuide-se, Maria.

