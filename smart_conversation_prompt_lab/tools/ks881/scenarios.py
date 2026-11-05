"""
KS-881: the fall-call test set, one definition for en / pt / he.

Each scenario is one situation or transition from the KS-881 functional requirements (FR v3), with
its expected outcome and WHEN the call must close (`close`: the number of senior answers before the
closing; a list means any of those). Every scenario has several genuinely different wordings, and
every wording is the SAME test in en, pt and he (W(en, pt, he), Yair 2026-11-02); a wording is a list
of senior turns, "" = silence. Speech-recognition cases use each language's own realistic
misrecognition of the same words. When the script runs out the senior is silent, exactly like the
KS-831 runner.

Greeting assumed in every script: Vega asks whether the senior is okay.

LEGACY maps every scenario of the six earlier sets (data/inputs/inputs_*.json) onto one of these, so
"every scenario covered by the previous prompt" is in the set (Yair, FR handover). The genuinely
different ones are kept word for word as a wording (`source=`) and translated; the rest are covered by
their situation's wordings (João, 2026-11-02: dedupe, then translate). Where the KS-881 rules change the
old expectation, the entry says why. LEGACY's `extend` is historical (the kept wordings carry their
own turns).

Hebrew and Portuguese wordings are the lab's own and need a native speaker's review.
"""

FELL, HELP, UNABLE, NONE, FINE = (
    "distress_fall_confirmed", "distress_assistance_requested", "distress_unable_to_verify",
    "no_response_from_resident", "no_fall_confirmed")
# KS-881 TR v3 (NUN-1626 names). Silence rule (Tony, NUN-1626 44793; João 2026-11-02): no_response only
# when the senior never spoke; spoke, then unclear or silent, is unable to verify.

S = ""  # silence


def W(en, pt, he, **kw):
    """One wording, the same test in every language (Yair, 2026-11-02: the same tests for each language).
    kw: expected, close, also (also-accepted outcomes), tail (dict en/pt/he: speech during the goodbye),
    after_close, source (the earlier scenario it keeps, "file:id"), flag (True: a fall with a help
    signal, so the confirmed fall must carry assistanceRequested; v7 P10). Speech-recognition cases use a
    realistic misrecognition of the same words in each language, not a literal translation."""
    return dict(en=en, pt=pt, he=he, **kw)


def T(en, pt, he):
    return dict(en=en, pt=pt, he=he)


SCENARIOS = [
    # ---- clear answers: alert at once, never held back by the re-ask -----------------------------
    dict(id="fell", situation="Clearly fell", expected=FELL, close=1, words=[
        W(["Yes, I fell in the kitchen."], ["Sim, caí na cozinha."], ["כן, נפלתי במטבח."]),
        W(["I've fallen and I can't get up."], ["Caí e não me consigo levantar."], ["נפלתי ואני לא מצליח לקום."],
          flag=True),
        W(["I took a tumble next to the bed."], ["Dei uma queda ao pé da cama."], ["עפתי ליד המיטה."]),
        # v7 (P8): a fall earlier today is a fall now.
        W(["I fell this morning in the bathroom."], ["Caí hoje de manhã na casa de banho."], ["נפלתי הבוקר באמבטיה."]),
        W(["I went down on the bathroom floor, I'm still lying here."],
          ["Fui ao chão na casa de banho, ainda estou aqui deitado."],
          ["נחתתי על הרצפה באמבטיה, אני עדיין שוכב פה."]),
        W(["I lost my footing on the stairs and fell."], ["Escorreguei nas escadas e caí."], ["מעדתי במדרגות ונפלתי."]),
        # Falls told without the word "fell".
        W(["I tripped over the rug in the hallway.", "My hip is really hurting."],
          ["Tropecei no tapete do corredor.", "Dói-me muito a anca."],
          ["מעדתי על השטיח במסדרון.", "הירך ממש כואבת לי."], close=[1, 2], source="inputs_v1.json:scenario_002"),
        W(["I rolled off the bed.", "I'm on the floor next to my bed, my arm hurts."],
          ["Rebolei da cama abaixo.", "Estou no chão ao pé da cama, dói-me o braço."],
          ["התגלגלתי מהמיטה.", "אני על הרצפה ליד המיטה, כואבת לי היד."], close=[1, 2],
          source="inputs_v1.json:scenario_056"),
        W(["I collapsed while walking to the bathroom.", "My legs just stopped working and I went down."],
          ["Fui abaixo quando ia para a casa de banho.", "As pernas deixaram de funcionar e fui ao chão."],
          ["קרסתי בדרך לשירותים.", "הרגליים פשוט הפסיקו לעבוד ונחתתי על הרצפה."], close=[1, 2],
          source="inputs_v1.json:scenario_083"),
        W(["Oh my God, I fell here!"], ["Ai minha nossa senhora, caí aqui!"], ["אוי אלוהים, נפלתי פה!"],
          source="inputs_ks833_ptpt.json:help_nossa_senhora"),
    ]),
    dict(id="fell_not_hurt", situation="Clearly fell (says not hurt)", expected=FELL, close=1, no_flag=True, words=[
        W(["I fell, but I'm not hurt."], ["Caí, mas não me magoei."], ["נפלתי, אבל לא נפגעתי."]),
        W(["I had a little fall, nothing's broken, I'm fine really."],
          ["Dei uma quedinha, não parti nada, estou bem a sério."],
          ["נפלתי קצת, שום דבר לא נשבר, אני באמת בסדר."]),
        W(["Yes I slipped and fell down, but no pain at all."], ["Sim, escorreguei e caí, mas não me dói nada."],
          ["כן, החלקתי ונפלתי, אבל שום דבר לא כואב."]),
    ]),
    dict(id="hurt_no_fall", situation="Hurt without saying they fell", expected=HELP, close=1, words=[
        W(["My hip hurts a lot, I can't get up."], ["Dói-me muito a anca, não me consigo levantar."],
          ["הירך כואבת לי מאוד, אני לא מצליח לקום."]),
        W(["I've cut my hand and it's bleeding quite badly."], ["Cortei-me na mão e está a sangrar muito."],
          ["חתכתי את היד והיא מדממת מאוד."]),
        W(["I think I broke my wrist, it's really swollen."], ["Acho que parti o pulso, está muito inchado."],
          ["אני חושב ששברתי את פרק היד, הוא ממש נפוח."]),
        W(["Ow, my back, it's killing me."], ["Ai, as costas, estão a matar-me."], ["איי, הגב, הוא הורג אותי."]),
        W(["I'm bleeding, I hit my head on the floor.", "There's blood everywhere, please help me."],
          ["Estou a sangrar, bati com a cabeça no chão.", "Há sangue por todo o lado, ajude-me por favor."],
          ["אני מדמם, קיבלתי מכה בראש מהרצפה.", "יש דם בכל מקום, תעזרי לי בבקשה."], also=[FELL],
          source="inputs_v0.json:scenario_10"),
        W(["I twisted my ankle on the stairs.", "It's really swollen, I'm sitting on the bottom step."],
          ["Torci o tornozelo nas escadas.", "Está muito inchado, estou sentado no último degrau."],
          ["נקע לי הקרסול במדרגות.", "הוא ממש נפוח, אני יושב על המדרגה התחתונה."],
          source="inputs_v1.json:scenario_021"),
        W(["AAAHH! Oh God, it hurts!", "My leg! I think I broke my leg!"],
          ["AAAI! Ai meu Deus, dói!", "A perna! Acho que parti a perna!"],
          ["אאאה! אלוהים, כואב!", "הרגל! אני חושב ששברתי את הרגל!"], source="inputs_v1.json:scenario_074"),
    ]),
    # KS-881 (NUN-1626, yuvalo 45082): a fall wins over help, and the help request rides on the flag.
    dict(id="fell_and_help", situation="Fell and asks for help", expected=FELL, close=1, assistance_flag=True,
         words=[
        W(["I fell and I need help."], ["Caí e preciso de ajuda."], ["נפלתי ואני צריך עזרה."]),
        W(["I've fallen, please help me."], ["Caí, ajude-me por favor."], ["נפלתי, תעזרי לי בבקשה."]),
        W(["I had a fall and I'm hurt, I need someone."], ["Dei uma queda e magoei-me, preciso de alguém."],
          ["נפלתי ונפגעתי, אני צריך מישהו."]),
        # Moved from `fell` (2026-11-02): they ask for help too, so the flag is checked on them.
        # 2 Nov run: the fall closes on the first turn, so the help words must be in it for the flag.
        W(["I... the... fell... kitchen... help... can't... head..."],
          ["Eu... a... caí... cozinha... ajuda... não... cabeça..."],
          ["אני... ה... נפלתי... מטבח... עזרה... לא יכול... ראש..."],
          close=[1, 2], also=[HELP], source="inputs_v0.json:scenario_15"),
        # v7 (state machine review, 2026-11-02): crying cannot be recognised, so the stage directions
        # ("*sobbing*", "*crying*") are gone; speech recognition only ever gives the words.
        # 3 Nov run (gpt-6.1-terra): the fall closes on the first turn, so the help words must be in it.
        W(["I... I... I fell... please send someone..."],
          ["Eu... eu... caí... mande alguém, por favor..."],
          ["אני... אני... נפלתי... בבקשה תשלחי מישהו..."], source="inputs_v1.json:scenario_036"),
    ]),
    dict(id="asks_help", situation="Needs help", expected=HELP, close=1, words=[
        W(["Please, I need help."], ["Por favor, preciso de ajuda."], ["בבקשה, אני צריך עזרה."]),
        W(["Help me, please."], ["Socorro, ajude-me."], ["תעזרי לי, בבקשה."]),
        W(["Can you send someone over? I need a hand."], ["Pode mandar alguém? Preciso de uma mão."],
          ["את יכולה לשלוח מישהו? אני צריך עזרה."]),
        W(["Call an ambulance, please."], ["Chame uma ambulância, por favor."], ["תזמיני אמבולנס, בבקשה."]),
        W(["help... please..."], ["ajuda... por favor..."], ["עזרה... בבקשה..."], source="inputs_v1.json:scenario_066"),
        # v7 (P1): a bare "no" to "are you okay?" is the answer to the question asked: not okay, at once.
        W(["No.", "I'm not well."], ["Não.", "Não estou bem."], ["לא.", "אני לא בסדר."], close=1,
          source="inputs_ks833_ptpt.json:help_nao"),
        # v7 (P6): asking for someone is assistance requested.
        W(["Call my daughter, please."], ["Ligue à minha filha, por favor."], ["תתקשרי לבת שלי, בבקשה."]),
        # KS-881 (Tony 45602): the words "I'm scared" are a call for help, with no question first.
        W(["I'm scared."], ["Tenho medo."], ["אני מפחד."]),
    ]),
    # KS-881 (Tony 45602; João/Yair 5 Nov): a partly heard or misheard fall, help or pain word is not certain.
    # It alerts at once, as unable to verify, never as a confirmed fall or help (v7 P3 said: the matching alert).
    dict(id="misheard_alert", situation="A misheard fall or help word", expected=UNABLE, close=1, words=[
        # Speech recognition: "fell" misheard, in each language's own way.
        W(["I well down in the kitchen.", "Yes, I fell."], ["QI na cozinha.", "Sim, caí."],
          ["נבלתי במטבח.", "כן, נפלתי."], source="inputs_ks833_ptpt.json:asr_qi_cozinha"),
        W(["I well off the sofa and it hearts a lot.", "Yes, I fell and it hurts."],
          ["Saí do sofá e boi muito.", "Sim, caí e dói muito."],
          ["נבלתי מהספה וכועב לי מאוד.", "כן, נפלתי וכואב לי."], source="inputs_ks833_ptpt.json:help_misrec_sai"),
        # "help" misheard.
        W(["Hep me, pease."], ["Ajuta-me, por fafor."], ["אני צריך אזרה."]),
    ]),
    dict(id="unwell_no_fall", situation="Unwell without a fall", expected=HELP, close=1, words=[
        W(["I feel really dizzy."], ["Estou com muitas tonturas."], ["מסתובב לי הראש מאוד."]),
        W(["I'm having trouble breathing."], ["Custa-me a respirar."], ["קשה לי לנשום."]),
        W(["I feel like I'm going to faint."], ["Sinto que vou desmaiar."], ["אני מרגיש שאני עומד להתעלף."]),
        W(["I feel very sick, something isn't right."], ["Sinto-me muito mal, alguma coisa não está bem."],
          ["אני מרגיש מאוד רע, משהו לא בסדר."]),
        W(["Everything looks blurry and strange.", "I can't see properly and I feel very confused."],
          ["Está tudo desfocado e estranho.", "Não vejo bem e estou muito confuso."],
          ["הכל נראה מטושטש ומוזר.", "אני לא רואה טוב ואני מאוד מבולבל."], close=[1, 2],
          source="inputs_v1.json:scenario_070"),
        # v7: "I feel terrible" is said, so it counts (how they sound does not).
        W(["I feel terrible."], ["Sinto-me péssimo."], ["אני מרגיש נורא."]),
    ]),
    dict(id="no_fall_but_problem", situation="Denial with a problem", expected=HELP, close=1, words=[
        W(["I didn't fall, but I can't get up."], ["Não caí, mas não me consigo levantar."],
          ["לא נפלתי, אבל אני לא מצליח לקום."]),
        W(["I'm not hurt, but I need some help."], ["Não me magoei, mas preciso de ajuda."],
          ["לא נפגעתי, אבל אני צריך עזרה."]),
        W(["No, I didn't fall, I just feel awful and dizzy."], ["Não, não caí, só me sinto muito mal e com tonturas."],
          ["לא, לא נפלתי, אני פשוט מרגיש נורא ויש לי סחרחורת."]),
    ]),

    # ---- fine: needs the confirming question, then no alert --------------------------------------
    dict(id="fine_confirmed", situation="Says they're fine and confirms it", expected=FINE, close=2, words=[
        W(["I'm fine, thank you.", "I'm not hurt at all, I can move fine."],
          ["Estou bem, obrigado.", "Não me magoei nada, consigo mexer-me bem."],
          ["אני בסדר, תודה.", "לא נפגעתי בכלל, אני זז בסדר."]),
        W(["Oh, that was just the cat knocking a chair over. I'm okay.", "Nothing hurts, I'm standing up."],
          ["Foi só o gato que deitou a cadeira abaixo. Estou bem.", "Não me dói nada, estou de pé."],
          ["זה רק החתול שהפיל כיסא. אני בסדר.", "שום דבר לא כואב לי, אני עומד."]),
        W(["I'm perfectly well.", "Nothing hurts, I can move around fine."],
          ["Estou ótimo.", "Não me dói nada, consigo andar bem."],
          ["אני מרגיש מצוין.", "שום דבר לא כואב, אני מסתובב בלי בעיה."]),
        W(["Oh for heaven's sake, stop bothering me! I'm fine!",
           "I'm perfectly alright, I told you. I was just watching my show."],
          ["Oh, por amor de Deus, deixe-me em paz! Estou bem!",
           "Estou perfeitamente bem, já lhe disse. Estava só a ver o meu programa."],
          ["נו באמת, תפסיקי להטריד אותי! אני בסדר!", "אני לגמרי בסדר, אמרתי לך. רק ראיתי את התוכנית שלי."],
          source="inputs_v1.json:scenario_008"),
        W(["I'm doing my physical therapy exercises on the floor.",
           "The therapist told me to do these stretches every day. I'm fine!"],
          ["Estou a fazer os exercícios da fisioterapia no chão.",
           "O fisioterapeuta mandou-me fazer estes alongamentos todos os dias. Estou bem!"],
          ["אני עושה את תרגילי הפיזיותרפיה על הרצפה.", "הפיזיותרפיסט אמר לי לעשות את המתיחות האלה כל יום. אני בסדר!"],
          source="inputs_v1.json:scenario_047"),
        # Dialect / casual speech (the Azorean "tou bem" in each language's own register).
        W(["Ah'm fine, ah'm fine.", "Nah, ain't hurt nothin'."], ["tou bem tou bem", "nã nã me magoei nada"],
          ["סבבה, סבבה.", "לא, כלום לא קרה לי."], source="inputs_ks833_ptpt.json:safe_azorean"),
        # v7 (P1, R2-Q1): a bare "yes" to "are you okay?" is a reassuring answer, and a bare "no" to
        # "are you hurt?" is the second one.
        W(["Yes.", "I'm not hurt, and I can get up fine."], ["Sim.", "Não me magoei, e consigo levantar-me bem."],
          ["כן.", "לא נפגעתי, ואני מצליח לקום בסדר."], source="inputs_ks833_ptpt.json:safe_sim_nao"),
        # v7 (P12): an irritated repeat is fine.
        W(["I'm fine.", "I told you, I'm fine!"], ["Estou bem.", "Já lhe disse, estou bem!"],
          ["אני בסדר.", "אמרתי לך, אני בסדר!"]),
        # v7 (P4): a near-fall is treated like "I'm fine".
        W(["I nearly fell, but I grabbed the table.", "Nothing hurts, and I can get up fine."],
          ["Quase caí, mas agarrei-me à mesa.", "Não me dói nada, e consigo levantar-me bem."],
          ["כמעט נפלתי, אבל נתפסתי בשולחן.", "שום דבר לא כואב, ואני מצליח לקום בסדר."]),
    ]),
    dict(id="denial_then_fine", situation="Denial alone, then fine", expected=FINE, close=2, words=[
        W(["I didn't fall.", "No, I don't need any help, I'm fine."],
          ["Não caí.", "Não, não preciso de ajuda, estou bem."],
          ["לא נפלתי.", "לא, אני לא צריך עזרה, אני בסדר."]),
        W(["I'm not hurt.", "No, I don't need anything, everything is okay."],
          ["Não me magoei.", "Não, não preciso de nada, está tudo bem."],
          ["לא נפגעתי.", "לא, אני לא צריך כלום, הכל בסדר."]),
        W(["I don't need help.", "I'm sure, I'm absolutely fine."],
          ["Não preciso de ajuda.", "Tenho a certeza, estou mesmo bem."],
          ["אני לא צריך עזרה.", "אני בטוח, אני לגמרי בסדר."]),
        W(["I didn't fall, I was just picking something up off the floor.", "No, I'm fine."],
          ["Não caí, estava só a apanhar uma coisa do chão.", "Não, estou bem."],
          ["לא נפלתי, רק הרמתי משהו מהרצפה.", "לא, אני בסדר."], source="inputs_ks833_ptpt.json:safe_apanhar"),
    ]),
    dict(id="denial_then_help", situation="Denial alone, then a problem", expected=HELP, close=2, words=[
        W(["I didn't fall.", "Well, actually I can't get up off the sofa."],
          ["Não caí.", "Mas a verdade é que não me consigo levantar do sofá."],
          ["לא נפלתי.", "אבל בעצם אני לא מצליח לקום מהספה."]),
        W(["I'm not hurt.", "But I do need someone to help me."],
          ["Não me magoei.", "Mas preciso que alguém me ajude."],
          ["לא נפגעתי.", "אבל אני צריך שמישהו יעזור לי."]),
        W(["No, I didn't fall.", "I feel very dizzy though."], ["Não, não caí.", "Mas estou com muitas tonturas."],
          ["לא, לא נפלתי.", "אבל יש לי סחרחורת חזקה."]),
        # v7 (P1): a bare "yes" to "do you need any help?" is help.
        W(["I didn't fall.", "Yes."], ["Não caí.", "Sim."], ["לא נפלתי.", "כן."]),
    ]),

    # ---- fine first, then a problem ---------------------------------------------------------------
    dict(id="fine_then_pain", situation="Says they're fine, then mentions pain", expected=HELP, close=2, words=[
        W(["I'm okay.", "Well, my knee does hurt quite a bit."], ["Estou bem.", "Bem... dói-me bastante o joelho."],
          ["אני בסדר.", "טוב, הברך די כואבת לי."]),
        W(["I'm fine, don't worry.", "Actually my head is aching badly."],
          ["Estou bem, não se preocupe.", "Aliás, dói-me muito a cabeça."],
          ["אני בסדר, אל תדאגי.", "בעצם הראש כואב לי מאוד."]),
        W(["Yes, I'm alright.", "Hmm, my shoulder is very sore."], ["Sim, estou bem.", "Hum, o ombro dói-me muito."],
          ["כן, אני בסדר.", "הממ, הכתף מאוד כואבת לי."]),
        W(["I'm okay I think.", "But there's some blood on my forehead from where I hit the shelf."],
          ["Acho que estou bem.", "Mas tenho um bocado de sangue na testa, bati na prateleira."],
          ["אני חושב שאני בסדר.", "אבל יש לי קצת דם על המצח, נתקלתי במדף."], source="inputs_v1.json:scenario_080"),
        # v7 (P12): pain of any degree, "a little" included.
        W(["I'm fine.", "It hurts a little."], ["Estou bem.", "Dói um bocadinho."], ["אני בסדר.", "כואב קצת."]),
        # Not tested: a bare "no" after "I'm fine". It means not hurt to "are you hurt?" but help to
        # "can you get up?", and Vega chooses which one to ask.
    ]),
    dict(id="fine_then_fell", situation="Says they're fine, then mentions a fall", expected=FELL, close=2, words=[
        W(["I'm alright.", "Well, actually I did fall a little while ago."],
          ["Estou bem.", "Bem, a verdade é que caí há bocado."],
          ["אני בסדר.", "טוב, בעצם נפלתי לפני רגע."]),
        W(["I didn't fall.", "Okay, yes, I did have a tumble earlier."],
          ["Não caí.", "Pronto, sim, dei uma queda mais cedo."],
          ["לא נפלתי.", "טוב, כן, נפלתי קצת קודם."]),
        W(["I'm fine.", "I slipped and fell, but I got back up."],
          ["Estou bem.", "Escorreguei e caí, mas já me levantei."],
          ["אני בסדר.", "החלקתי ונפלתי, אבל קמתי."]),
        W(["Yes.", "Fell. Hurts."], ["Sim.", "Caí. Dói."], ["כן.", "נפלתי. כואב."], flag=True,
          source="inputs_v1.json:scenario_090"),
        W(["I'm fine, don't worry.", "Well actually I did slip a little bit.", "Yes, I fell, my hip hurts."],
          ["Estou bem, não se preocupe.", "Bem, na verdade escorreguei um bocadinho.", "Sim, caí, dói-me a anca."],
          ["אני בסדר, אל תדאגי.", "טוב, בעצם החלקתי קצת.", "כן, נפלתי, כואבת לי הירך."], close=[2, 3],
          source="inputs_baseline.json:scenario_08"),
        # v7 (P10, R2-Q6): a fall with a help signal carries the flag, at any answer.
        W(["I'm fine.", "Actually I fell, and I need help getting up."],
          ["Estou bem.", "Afinal caí, e preciso de ajuda para me levantar."],
          ["אני בסדר.", "בעצם נפלתי, ואני צריך עזרה לקום."], flag=True),
    ]),

    # ---- unclear or silent first: the one re-ask, then follow the clear answer --------------------
    dict(id="unclear_then_fell", situation="Unclear, then fell", expected=FELL, close=2, words=[
        W(["I, I, I...", "I fell."], ["Eu, eu, eu...", "Caí."], ["אני, אני, אני...", "נפלתי."]),
        W(["The kettle, the... what...", "I've fallen on the floor."], ["A chaleira, a... o quê...", "Caí no chão."],
          ["הקומקום... מה...", "נפלתי על הרצפה."]),
        W(["Gardens and she was one of twelve sisters.", "Yes, I fell down in the hallway."],
          ["Os jardins e ela era uma de doze irmãs.", "Sim, caí no corredor."],
          ["גינות והיא הייתה אחת משתים עשרה אחיות.", "כן, נפלתי במסדרון."]),
        W(["I managed to stand back up on my own.", "But my shoulder is very sore from the fall."],
          ["Consegui levantar-me sozinho.", "Mas o ombro dói-me muito da queda."],
          ["הצלחתי לקום לבד.", "אבל הכתף מאוד כואבת לי מהנפילה."], close=[1, 2], source="inputs_v1.json:scenario_054"),
        W(["I don't know what happened.", "I was standing and then I was on the floor somehow."],
          ["Não sei o que aconteceu.", "Estava de pé e de repente estava no chão."],
          ["אני לא יודע מה קרה.", "עמדתי ופתאום הייתי על הרצפה."], close=[1, 2], source="inputs_v1.json:scenario_072"),
        W(["What?", "I fell, I can't get up, please help."], ["O quê?", "Caí, não me consigo levantar, ajude-me."],
          ["מה?", "נפלתי, אני לא מצליח לקום, תעזרי לי."], flag=True),
    ]),
    dict(id="unclear_then_problem", situation="Unclear, then hurt or needs help", expected=HELP, close=2, words=[
        # DEMO 4:14 (...1793121283557): ASR heard "I think that with my leg".
        # 3 Nov (Yair): a garbled answer that names a part of the body is unclear like any other: the re-ask
        # first, then unable to verify if it is still unclear (FR v5).
        W(["I think that with my leg.", "My leg hurts, I can't get up."],
          ["Acho que com a minha perna.", "Dói-me a perna, não me consigo levantar."],
          ["אני חושב שעם הרגל שלי.", "כואבת לי הרגל, אני לא מצליח לקום."]),
        W(["Mm, the... the thing.", "Please help me."], ["Hum, a... a coisa.", "Ajude-me, por favor."],
          ["ממ, ה... הדבר.", "תעזרי לי, בבקשה."]),
        W(["What day is it today?", "I feel really dizzy."], ["Que dia é hoje?", "Estou com muitas tonturas."],
          ["איזה יום היום?", "מסתובב לי הראש מאוד."]),
    ]),
    # v7 (state machine REASK -> CQ_LATE): an "I'm fine" to the re-ask is the FIRST reassuring answer, so
    # the confirming question always follows and the call closes after 3 answers (was [2, 3] in v6).
    dict(id="unclear_then_fine", situation="Unclear, then clearly okay (D16)", expected=FINE, close=3, words=[
        W(["Huh? What?", "Oh sorry, I was half asleep. I'm fine.", "I'm not hurt at all, I can move fine."],
          ["Hã? O quê?", "Ah, desculpe, estava meio a dormir. Estou bem.", "Não me magoei nada, consigo mexer-me bem."],
          ["מה? מה?", "אה סליחה, הייתי חצי ישן. אני בסדר.", "לא נפגעתי בכלל, אני זז בסדר."]),
        W(["The bus didn't come on Tuesday.", "Oh, yes, I'm okay.", "Nothing hurts at all, I'm fine."],
          ["O autocarro não veio na terça.", "Ah, sim, estou bem.", "Não me dói nada, estou bem."],
          ["האוטובוס לא הגיע ביום שלישי.", "אה, כן, אני בסדר.", "שום דבר לא כואב, אני בסדר."]),
        W(["Who's this?", "Ah, Vega. I'm fine, thanks.", "No, I don't need anything."],
          ["Quem fala?", "Ah, a Vega. Estou bem, obrigado.", "Não, não preciso de nada."],
          ["מי זה?", "אה, וגה. אני בסדר, תודה.", "לא, אני לא צריך כלום."]),
        W(["I lost my balance for a second but I grabbed the table.",
           "I didn't actually fall. I'm standing up and I feel fine now.", "I'm not hurt at all, I can move fine."],
          ["Perdi o equilíbrio um segundo, mas agarrei-me à mesa.",
           "Não cheguei a cair. Estou de pé e sinto-me bem.", "Não me magoei nada, consigo mexer-me bem."],
          ["איבדתי שיווי משקל לשנייה אבל נתפסתי בשולחן.", "לא באמת נפלתי. אני עומד ואני מרגיש בסדר.",
           "לא נפגעתי בכלל, אני זז בסדר."], close=2, source="inputs_v1.json:scenario_097"),
        # ^ v7 (P4): a near-fall is a first "fine", not unclear, so it closes after 2.
        # Speech recognition: "I didn't fall" / "not hurt at all" misheard, in each language's own way.
        W(["No, I didn't ball.", "Yes, I didn't fall, I'm fine.", "I'm not hurt, and I can get up fine."],
          ["Não QI.", "Sim, não caí, estou bem.", "Não me magoei, e consigo levantar-me bem."],
          ["לא נבלתי.", "כן, לא נפלתי, אני בסדר.", "לא נפגעתי, ואני מצליח לקום בסדר."], source="inputs_ks833_ptpt.json:asr_nao_qi"),
        W(["Na na, not hurt a tall.", "I'm fine, I'm not hurt at all.", "I'm fine, nothing hurts."],
          ["Na Na maguinada.", "Estou bem, não me magoei nada.", "Estou bem, não me dói nada."],
          ["נה נה, לנפקתי בחלל.", "אני בסדר, לא נפגעתי בכלל.", "אני בסדר, שום דבר לא כואב."],
          source="inputs_ks833_ptpt.json:asr_maguinada"),
    ]),
    dict(id="silence_then_problem", situation="Silent, then fell or needs help", expected=FELL, close=2, words=[
        W([S, "I just fell, I was trying to get to the phone."], [S, "Acabei de cair, ia atender o telefone."],
          [S, "הרגע נפלתי, ניסיתי להגיע לטלפון."]),
        W([S, "Yes, I'm on the floor, I fell."], [S, "Sim, estou no chão, caí."], [S, "כן, אני על הרצפה, נפלתי."]),
        W([S, "...help..."], [S, "...ajuda..."], [S, "...עזרה..."], expected=HELP, source="inputs_v1.json:scenario_081"),
        W([S, "My back hurts so much."], [S, "Doem-me tanto as costas."], [S, "הגב כל כך כואב לי."], expected=HELP),
    ]),
    dict(id="silence_then_fine", situation="Silent, then clearly okay", expected=FINE, close=3, words=[
        W([S, "Sorry, I was in the other room. I'm fine.", "I'm not hurt at all, I can move fine."],
          [S, "Desculpe, estava na outra sala. Estou bem.", "Não me magoei nada, consigo mexer-me bem."],
          [S, "סליחה, הייתי בחדר השני. אני בסדר.", "לא נפגעתי בכלל, אני זז בסדר."]),
        W([S, "Oh, I didn't hear you. All good here.", "No, I don't need any help."],
          [S, "Ah, não a ouvi. Está tudo bem.", "Não, não preciso de ajuda."],
          [S, "אה, לא שמעתי אותך. הכל טוב פה.", "לא, אני לא צריך עזרה."]),
    ]),
    # KS-881 TR v3 (Tony, NUN-1626 44793): they spoke, so a later silence is unable to verify.
    dict(id="fine_then_silent", situation="Says fine, then goes silent", expected=UNABLE, close=3, words=[
        W(["I'm fine.", S, S], ["Estou bem.", S, S], ["אני בסדר.", S, S], source="inputs_v1.json:scenario_099"),
        W(["Yes, I'm okay.", S, S], ["Sim, estou bem.", S, S], ["כן, אני בסדר.", S, S]),
    ]),

    # ---- still unclear after the re-ask: unable to verify -----------------------------------------
    dict(id="still_unclear", situation="Still unclear", expected=UNABLE, close=2, words=[
        # DEMO 4:14 then 4:17 (...1793121462233).
        # 3 Nov (Yair): a garbled answer that names a part of the body is unclear like any other: the re-ask
        # first, then unable to verify if it is still unclear (FR v5).
        W(["I think that with my leg.", "I, I, I."], ["Acho que com a minha perna.", "Eu, eu, eu."],
          ["אני חושב שעם הרגל שלי.", "אני, אני, אני."]),
        W(["The story topology is the island of the government slowly.", "Purple seven the window."],
          ["A topologia da história é a ilha do governo devagar.", "Roxo sete a janela."],
          ["הסיפור של הטופולוגיה הוא האי של הממשלה לאט.", "סגול שבע החלון."], source="inputs_ks831.json:u5_asr_noise"),
        W(["I don't know.", "I'm not sure."], ["Não sei.", "Não sei bem."], ["אני לא יודע.", "אני לא בטוח."],
          source="inputs_ks833_ptpt.json:unclear_nao_sei"),
        W(["Where is Mary? Is Mary here?", "I want Mary."], ["Onde está a Maria? A Maria está aqui?", "Quero a Maria."],
          ["איפה מרים? מרים פה?", "אני רוצה את מרים."], expected=HELP, close=[1, 2],
          source="inputs_ks831.json:u4_confused"),  # v7 (P6): asking for someone is help
        W(["Leave me alone!", "Go away, stop calling me."], ["Deixe-me em paz!", "Vá-se embora, pare de me ligar."],
          ["תעזבי אותי בשקט!", "לכי מפה, תפסיקי להתקשר אליי."], source="inputs_v1.json:scenario_028"),
        W(["I don't know where I am.", "What is this place? I'm scared."],
          ["Não sei onde estou.", "Que sítio é este? Tenho medo."],
          ["אני לא יודע איפה אני.", "מה זה המקום הזה? אני מפחד."], expected=HELP, close=2,
          source="inputs_v0.json:scenario_11"),  # Tony (45602): the words "I'm scared" are help
        W(["Oh, it's such a lovely day outside, isn't it?", "Have you seen how nice the garden looks today?"],
          ["Está um dia tão bonito lá fora, não está?", "Já viu como o jardim está bonito hoje?"],
          ["איזה יום יפה בחוץ, נכון?", "ראית כמה הגינה יפה היום?"], source="inputs_v1.json:scenario_013"),
        W(["Hmm... I guess so...", "I'm not really sure, to be honest."],
          ["Hum... acho que sim...", "Para ser sincero, não tenho bem a certeza."],
          ["הממ... אני מניח שכן...", "האמת, אני לא ממש בטוח."], close=3, source="inputs_v1.json:scenario_084"),
        # ^ v7 (R2-Q1): "I guess so" first is a reassuring answer; the unsure reply to the confirming
        # question gets the re-ask, and the silence after it is unable to verify, after 3.
        W(["Wha... the... um.", "Is it the. No the."], ["O quê... o... hum.", "É o. Não o."], ["מה... ה... אממ.", "זה ה. לא ה."],
          source="inputs_ks831.json:u3_broken_fragments"),
        # Speech recognition: a short garbled answer, repeated.
        W(["Na na.", "Na na."], ["Na na.", "Na na."], ["נה נה.", "נה נה."], source="inputs_ks833_ptpt.json:asr_na_na"),
        W(["Tee.", "Tee."], ["TI.", "TI."], ["טי.", "טי."], close=[1, 2],
          # ^ "TI" may be a misheard "caí": unable to verify at once (Tony 45602) or after the re-ask.
          source="inputs_ks833_ptpt.json:asr_bare_ti"),
    ]),
    dict(id="what_twice", situation="\"What?\" twice", expected=UNABLE, close=2, words=[
        W(["What?", "What? I can't hear you."], ["O quê?", "O quê? Não a ouço."], ["מה?", "מה? אני לא שומע."]),
        W(["Huh?", "Sorry, what are you saying?"], ["Hã?", "Desculpe, o que é que está a dizer?"],
          ["הא?", "סליחה, מה את אומרת?"], source="inputs_ks833_ptpt.json:unclear_ha"),
    ]),
    # KS-881 TR v3 (Tony, NUN-1626 44793): once the senior has spoken, a later silence is unable to
    # verify too ("the senior did respond"). Replaces João's 2026-10-30 "the last answer decides".
    dict(id="mixed_no_restart", situation="Mixed unclear and silence: the re-ask never restarts",
         expected=UNABLE, close=2, words=[
        W([S, "The garden, the... Tuesday.", "What?"], [S, "O jardim, a... terça.", "O quê?"],
          [S, "הגינה, ה... יום שלישי.", "מה?"]),   # silence -> unclear -> "what?" (Tony 44883 pt 2)
        W(["The garden, the... Tuesday.", S], ["O jardim, a... terça.", S], ["הגינה, ה... יום שלישי.", S]),
        W([S, "What?"], [S, "O quê?"], [S, "מה?"], source="inputs_v1.json:scenario_053"),
        W(["What?", S], ["Hã?", S], ["מה?", S]),
        W(["Mm, the thing.", "What?"], ["Hum, a coisa.", "O quê?"], ["ממ, הדבר.", "מה?"]),
    ]),
    dict(id="interrupted", situation="Answer cut off", expected=HELP, close=2, words=[
        W(["Yes, I'm fine, but I", "my hip hurts."], ["Sim, estou bem, mas eu", "dói-me a anca."],
          ["כן, אני בסדר, אבל אני", "כואבת לי הירך."]),
        W(["Yes... but I", "I fell."], ["Sim... mas eu", "caí."], ["כן... אבל אני", "נפלתי."], expected=FELL),
        W(["Yes, but", "the... the"], ["Sim, mas", "o... o"], ["כן, אבל", "ה... ה"], expected=UNABLE,
          source="inputs_ks833_ptpt.json:unclear_cut_off"),
        # v7 (P1): "I'm fine… no, I'm not" is not okay: help at once.
        W(["I'm fine... no, I'm not."], ["Estou bem... não, não estou."], ["אני בסדר... לא, אני לא."],
          close=1, source="inputs_ks833_ptpt.json:unclear_contradiction"),
    ]),

    # ---- silence ----------------------------------------------------------------------------------
    dict(id="silent_twice", situation="Silent twice", expected=NONE, close=2, words=[
        W([S, S], [S, S], [S, S], source="inputs_baseline.json:scenario_04"),
    ]),

    # ---- past falls (Tony 44883 point 1) ----------------------------------------------------------
    # v7 (P8): a fall yesterday or earlier with no problem now is unclear -> re-ask -> confirming question.
    dict(id="past_fall_now_fine", situation="Past fall, fine now", expected=FINE, close=3, words=[
        W(["I fell last year, but not today.", "Yes, I'm fine today.", "Nothing hurts at all, I'm fine."],
          ["Caí no ano passado, mas hoje não.", "Sim, hoje estou bem.", "Não me dói nada, estou bem."],
          ["נפלתי בשנה שעברה, אבל לא היום.", "כן, היום אני בסדר.", "שום דבר לא כואב, אני בסדר."]),
        W(["I had a fall last month.", "I'm okay now, thank you.", "I'm not hurt at all, I can move fine."],
          ["Dei uma queda no mês passado.", "Agora estou bem, obrigado.", "Não me magoei nada, consigo mexer-me bem."],
          ["נפלתי בחודש שעבר.", "עכשיו אני בסדר, תודה.", "לא נפגעתי בכלל, אני זז בסדר."]),
    ]),
    # v7 (P8): a past fall alone is unclear, so the re-ask comes first; pain now is help, not a fall.
    dict(id="past_fall_now_hurt", situation="Past fall, hurt now", expected=HELP, close=2, words=[
        W(["I had a fall last week.", "My back still hurts badly."],
          ["Dei uma queda na semana passada.", "As costas ainda me doem muito."],
          ["נפלתי בשבוע שעבר.", "הגב עדיין כואב לי מאוד."]),
        W(["I fell a few days ago.", "And now my knee is very swollen."],
          ["Caí há uns dias.", "E agora o joelho está muito inchado."],
          ["נפלתי לפני כמה ימים.", "ועכשיו הברך מאוד נפוחה."]),
    ]),

    # ---- speech during a no-fall goodbye (KS-739 re-evaluation) ------------------------------------
    dict(id="help_during_goodbye", situation="Help asked during the goodbye", expected=FINE, close=2,
         after_close=HELP, words=[
        W(["I'm fine.", "I'm not hurt at all, I can move fine."],
          ["Estou bem.", "Não me magoei nada, consigo mexer-me bem."],
          ["אני בסדר.", "לא נפגעתי בכלל, אני זז בסדר."],
          tail=T("Wait, actually my leg hurts.", "Espere, afinal dói-me a perna.", "רגע, בעצם כואבת לי הרגל.")),
        W(["All good here.", "No, I don't need anything."], ["Está tudo bem.", "Não, não preciso de nada."],
          ["הכל טוב פה.", "לא, אני לא צריך כלום."],
          tail=T("Hold on, I need help.", "Espere, preciso de ajuda.", "רגע, אני צריך עזרה.")),
        W(["I'm okay.", "Nothing hurts, I'm fine."], ["Estou bem.", "Não me dói nada, estou bem."],
          ["אני בסדר.", "שום דבר לא כואב, אני בסדר."],
          tail=T("Actually, I did fall.", "Espere, afinal caí.", "רגע, בעצם נפלתי."), after_close=FELL),
        # v7 (P11): feeling unwell over the goodbye is acted on too.
        W(["I'm fine.", "I'm not hurt, and I can get up fine."], ["Estou bem.", "Não me magoei, e consigo levantar-me bem."], ["אני בסדר.", "לא נפגעתי, ואני מצליח לקום בסדר."],
          tail=T("Wait, I feel very dizzy.", "Espere, estou com muitas tonturas.", "רגע, יש לי סחרחורת חזקה.")),
    ]),
    dict(id="thanks_during_goodbye", situation="Thanks during the goodbye: no alert", expected=FINE, close=2,
         after_close=FINE, words=[
        W(["I'm fine.", "I'm not hurt at all, I can move fine."],
          ["Estou bem.", "Não me magoei nada, consigo mexer-me bem."],
          ["אני בסדר.", "לא נפגעתי בכלל, אני זז בסדר."], tail=T("Thank you, bye.", "Obrigado, adeus.", "תודה, להתראות.")),
        # v7 (P11): unclear speech or a "hold on" over a no-fall goodbye changes nothing.
        W(["I'm fine.", "I'm not hurt, and I can get up fine."], ["Estou bem.", "Não me magoei, e consigo levantar-me bem."], ["אני בסדר.", "לא נפגעתי, ואני מצליח לקום בסדר."],
          tail=T("The kettle, the... Tuesday.", "A chaleira, a... terça.", "הקומקום, ה... יום שלישי.")),
        W(["I'm okay.", "Nothing hurts, I can get up fine."], ["Estou bem.", "Não me dói nada, consigo levantar-me bem."], ["אני בסדר.", "שום דבר לא כואב, אני מצליח לקום בסדר."],
          tail=T("Hold on.", "Espere.", "רגע.")),
    ]),

    # ---- nobody identified (NUN-1592 prompt; NUN-1626 rules delivered by KS-881) --------------------
    dict(id="unknown_other_fell", situation="Another person says someone fell", expected=FELL, close=1,
         prompt="unknown", words=[
        W(["My husband fell, he's on the floor."], ["O meu marido caiu, está no chão."], ["בעלי נפל, הוא על הרצפה."]),
        W(["Yes, my mother has fallen in the bathroom."], ["Sim, a minha mãe caiu na casa de banho."],
          ["כן, אמא שלי נפלה באמבטיה."]),
    ]),
    dict(id="unknown_other_needs_help", situation="Another person says someone needs help", expected=HELP,
         close=1, prompt="unknown", words=[
        W(["My wife hurt her back, she needs help."], ["A minha mulher magoou as costas, precisa de ajuda."],
          ["אשתי נפגעה בגב, היא צריכה עזרה."]),
        W(["Yes, my dad needs help, he can't get up."], ["Sim, o meu pai precisa de ajuda, não se consegue levantar."],
          ["כן, אבא שלי צריך עזרה, הוא לא מצליח לקום."]),
    ]),
    dict(id="unknown_silent_twice", situation="Nobody identified, silent twice", expected=NONE, close=2,
         prompt="unknown", words=[W([S, S], [S, S], [S, S])]),
    # KS-881 TR v3 known limit: until NUN-1591 ships, an unidentified "I'm OK" closes as no fall (NUN-1626
    # option B), after the confirming question.
    dict(id="unknown_visitor_fine", situation="Another person's \"I'm fine\" (closes until NUN-1591)",
         expected=FINE, close=2, prompt="unknown", words=[
        W(["Nobody needs help, we're all fine.", "Everyone's okay, nobody is hurt."],
          ["Ninguém precisa de ajuda, estamos todos bem.", "Está toda a gente bem, ninguém se magoou."],
          ["אף אחד לא צריך עזרה, כולנו בסדר.", "כולם בסדר, אף אחד לא נפגע."]),
        W(["I'm just visiting, everything is fine here.", "No, nobody fell."],
          ["Estou só de visita, está tudo bem aqui.", "Não, ninguém caiu."],
          ["אני רק מבקר, הכל בסדר פה.", "לא, אף אחד לא נפל."]),
    ]),
    # ---- decision-tree gaps (KS-881 Fall Call Decision Tree, 2026-11-02): one scenario per branch ---
    dict(id="fine_silent_then_fine", situation="B12: fine, silent, then fine", expected=FINE, close=3, words=[
        W(["I'm fine.", S, "Sorry, yes, I'm okay, nothing hurts."],
          ["Estou bem.", S, "Desculpe, sim, estou bem, não me dói nada."],
          ["אני בסדר.", S, "סליחה, כן, אני בסדר, שום דבר לא כואב."]),
    ]),
    dict(id="fine_unclear_twice", situation="B13: fine, then unclear twice", expected=UNABLE, close=3, words=[
        W(["I'm fine.", "The kettle, the... Tuesday.", "Mm, the garden."],
          ["Estou bem.", "A chaleira, a... terça.", "Hum, o jardim."],
          ["אני בסדר.", "הקומקום, ה... יום שלישי.", "ממ, הגינה."]),
    ]),
    dict(id="fine_unclear_then_fine", situation="B14: fine, unclear, then fine", expected=FINE, close=3, words=[
        W(["I'm fine.", "What? Who's this?", "Oh, Vega. No, I'm not hurt at all, I can move fine."],
          ["Estou bem.", "O quê? Quem fala?", "Ah, a Vega. Não, não me magoei nada, consigo mexer-me bem."],
          ["אני בסדר.", "מה? מי זה?", "אה, וגה. לא, לא נפגעתי בכלל, אני זז בסדר."]),
    ]),
    dict(id="denial_unclear_twice", situation="B19: denial, then unclear twice", expected=UNABLE, close=3, words=[
        W(["I didn't fall.", "Hmm, the... what?", "The thing, the..."],
          ["Não caí.", "Hum, o... o quê?", "A coisa, a..."],
          ["לא נפלתי.", "הממ, ה... מה?", "הדבר, ה..."]),
    ]),
    # B27 / B39, v7 (REASK -> CQ_LATE): the "I'm fine" after the re-ask is the first reassuring answer, so
    # the confirming question always follows, and the silence after it is unable to verify (was [2, 3]
    # with no fall also accepted in v6).
    dict(id="unclear_fine_then_silent", situation="B27: unclear, fine, then silent", expected=UNABLE,
         close=3, words=[
        W(["Is it Sunday?", "Oh, I'm fine.", S], ["É domingo?", "Ah, estou bem.", S], ["היום יום ראשון?", "אה, אני בסדר.", S]),
    ]),
    dict(id="silent_fine_then_silent", situation="B39: silent, fine, then silent", expected=UNABLE,
         close=3, words=[
        W([S, "Oh, I'm fine.", S], [S, "Ah, estou bem.", S], [S, "אה, אני בסדר.", S]),
    ]),
    # B40, v7: "I'm fine" then off-topic twice follows the rules (fine -> confirming question -> off-topic
    # = unclear -> re-ask -> off-topic again), so it closes after 3; the turn limit is never reached by the
    # rules (state machine section 5). Kept under its old id for the LEGACY map.
    dict(id="turn_limit", situation="B40: fine, then keeps talking off-topic", expected=UNABLE, close=3, words=[
        W(["I'm fine, but let me tell you about my garden.", "The roses are lovely this year, my daughter planted them.",
           "And the tomatoes too, we had so many.", "Oh, and the neighbour's cat...", "And then on Sunday..."],
          ["Estou bem, mas deixe-me falar-lhe do meu jardim.", "As rosas estão lindas este ano, foi a minha filha que as plantou.",
           "E os tomates também, tivemos tantos.", "Ah, e o gato da vizinha...", "E depois no domingo..."],
          ["אני בסדר, אבל תני לי לספר לך על הגינה שלי.", "הוורדים יפים השנה, הבת שלי שתלה אותם.",
           "וגם העגבניות, היו לנו כל כך הרבה.", "אה, והחתול של השכנה...", "ואז ביום ראשון..."]),
    ]),
    dict(id="unknown_still_unclear", situation="B49: nobody identified, still unclear", expected=UNABLE, close=2,
         prompt="unknown", words=[
        W(["Who? What is this?", "The kettle, the... Tuesday."], ["Quem? O que é isto?", "A chaleira, a... terça."],
          ["מי? מה זה?", "הקומקום, ה... יום שלישי."]),
    ]),
    dict(id="unknown_silence_then_fell", situation="B50: nobody identified, silent, then someone fell",
         expected=FELL, close=2, prompt="unknown", words=[
        W([S, "Yes, my husband fell in the kitchen."], [S, "Sim, o meu marido caiu na cozinha."],
          [S, "כן, בעלי נפל במטבח."]),
    ]),
    dict(id="unknown_self_fell", situation="B51: nobody identified, the person who fell answers", expected=FELL,
         close=1, prompt="unknown", words=[
        W(["I fell, I'm on the floor."], ["Caí, estou no chão."], ["נפלתי, אני על הרצפה."]),
    ]),

    # =============================================================================================
    # v7: KS-881 Fall Call State Machine (2 Nov 2026). Replies to the confirming question never start with
    # a bare "no": Vega chooses "are you hurt?" or "can you get up?", and "no" means opposite things to them
    # (v7 smoke 2026-11-02). One scenario per ending transition that the set
    # above does not reach (reports/KS-881/dev/coverage_count.js: 50 ending transitions). `close` counts
    # EVERY senior turn, so the free "hold on" and the silence after it are included (the state
    # machine's N does not count them). FELL+HELP wordings carry flag=True (assistanceRequested).
    # =============================================================================================

    # ---- the free wait at the first question (HOLD_FIRST, FIRST_AGAIN) ----------------------------
    dict(id="hold_then_fell", situation="v7: hold on, then says they fell during the wait", expected=FELL,
         close=2, words=[
        W(["Hold on, let me get to the phone.", "I fell, I'm on the floor."],
          ["Espere, deixe-me chegar ao telefone.", "Caí, estou no chão."],
          ["רגע, תני לי להגיע לטלפון.", "נפלתי, אני על הרצפה."]),
        W(["Wait a moment.", "I fell and I need help."], ["Espere um momento.", "Caí e preciso de ajuda."],
          ["חכי רגע.", "נפלתי ואני צריך עזרה."], flag=True),
    ]),
    dict(id="hold_then_help", situation="v7: hold on, then needs help during the wait", expected=HELP, close=2,
         words=[
        W(["Hold on.", "My back hurts, I can't get up."], ["Espere.", "Doem-me as costas, não me consigo levantar."],
          ["רגע.", "הגב כואב לי, אני לא מצליח לקום."]),
    ]),
    dict(id="hold_then_fine", situation="v7: hold on, then fine during the wait, then confirms", expected=FINE,
         close=3, words=[
        W(["Hold on.", "Okay, I'm here. I'm fine.", "I'm not hurt, and I can get up fine."],
          ["Espere.", "Pronto, já cá estou. Estou bem.", "Não me magoei, e consigo levantar-me bem."],
          ["רגע.", "טוב, אני פה. אני בסדר.", "לא נפגעתי, ואני מצליח לקום בסדר."]),
    ]),
    dict(id="hold_then_unclear", situation="v7: hold on, then unclear twice", expected=UNABLE, close=3, words=[
        W(["Hold on.", "The kettle, the... Tuesday.", "What?"], ["Espere.", "A chaleira, a... terça.", "O quê?"],
          ["רגע.", "הקומקום, ה... יום שלישי.", "מה?"]),
    ]),
    dict(id="hold_wait_then_fell", situation="v7: hold on, silent (free), then fell when asked again",
         expected=FELL, close=3, words=[
        W(["Hold on.", S, "Sorry, I fell in the bathroom."], ["Espere.", S, "Desculpe, caí na casa de banho."],
          ["רגע.", S, "סליחה, נפלתי באמבטיה."]),
        W(["Wait.", S, "I fell, please help me."], ["Espere.", S, "Caí, ajude-me por favor."],
          ["חכי.", S, "נפלתי, תעזרי לי בבקשה."], flag=True),
    ]),
    dict(id="hold_wait_then_help", situation="v7: hold on, silent (free), then needs help when asked again",
         expected=HELP, close=3, words=[
        W(["Hold on.", S, "I need help, I feel very dizzy."], ["Espere.", S, "Preciso de ajuda, estou com muitas tonturas."],
          ["רגע.", S, "אני צריך עזרה, יש לי סחרחורת חזקה."]),
    ]),
    dict(id="hold_wait_then_fine", situation="v7: hold on, silent (free), then fine and confirms", expected=FINE,
         close=4, words=[
        W(["Hold on.", S, "Sorry, I'm fine.", "Nothing hurts, and I can get up fine."], ["Espere.", S, "Desculpe, estou bem.", "Não me dói nada, e consigo levantar-me bem."],
          ["רגע.", S, "סליחה, אני בסדר.", "שום דבר לא כואב, ואני מצליח לקום בסדר."]),
    ]),
    # The review's loop: "are you okay?" -> "hold on" -> "are you okay?" -> "hold on" -> ... The wait is
    # free once per call; the second "hold on" is unclear (re-ask), the third ends the call.
    dict(id="hold_repeated", situation="v7: keeps saying hold on (no endless loop)", expected=UNABLE, close=4,
         words=[
        W(["Hold on.", S, "Hold on.", "Hold on."], ["Espere.", S, "Espere.", "Espere."], ["רגע.", S, "רגע.", "רגע."]),
        W(["Wait.", "Wait.", "Wait."], ["Espere.", "Espere.", "Espere."], ["חכי.", "חכי.", "חכי."], close=3),
    ]),

    # ---- the free wait at the confirming question (HOLD_CQ, CQ_AGAIN) ------------------------------
    dict(id="fine_hold_then_fine", situation="v7: fine, hold on, then confirms during the wait", expected=FINE,
         close=3, words=[
        W(["I'm fine.", "Hold on.", "I'm not hurt, and I can get up fine."], ["Estou bem.", "Espere.", "Não me magoei, e consigo levantar-me bem."],
          ["אני בסדר.", "רגע.", "לא נפגעתי, ואני מצליח לקום בסדר."]),
        W(["I didn't fall.", "Wait a second.", "No, I don't need any help."],
          ["Não caí.", "Espere um segundo.", "Não, não preciso de ajuda."],
          ["לא נפלתי.", "חכי שנייה.", "לא, אני לא צריך עזרה."]),
    ]),
    dict(id="fine_hold_then_fell", situation="v7: fine, hold on, then says they fell", expected=FELL, close=3,
         words=[
        W(["I'm okay.", "Hold on.", "Actually, I did fall."], ["Estou bem.", "Espere.", "Afinal, caí."],
          ["אני בסדר.", "רגע.", "בעצם, נפלתי."]),
        W(["I'm okay.", "Hold on.", "I fell and I need help to get up."],
          ["Estou bem.", "Espere.", "Caí e preciso de ajuda para me levantar."],
          ["אני בסדר.", "רגע.", "נפלתי ואני צריך עזרה לקום."], flag=True),
    ]),
    dict(id="fine_hold_then_help", situation="v7: fine, hold on, then mentions pain", expected=HELP, close=3, words=[
        W(["I'm fine.", "Hold on.", "My knee hurts quite a bit."], ["Estou bem.", "Espere.", "Dói-me bastante o joelho."],
          ["אני בסדר.", "רגע.", "הברך די כואבת לי."]),
    ]),
    dict(id="fine_hold_wait_then_fine", situation="v7: fine, hold on, silent (free), then confirms", expected=FINE,
         close=4, words=[
        W(["I'm fine.", "Hold on.", S, "I'm not hurt, and I can get up fine."], ["Estou bem.", "Espere.", S, "Não me magoei, e consigo levantar-me bem."],
          ["אני בסדר.", "רגע.", S, "לא נפגעתי, ואני מצליח לקום בסדר."]),
        W(["I didn't fall.", "Hold on.", S, "Sorry, I'm fine, really."], ["Não caí.", "Espere.", S, "Desculpe, estou bem, a sério."],
          ["לא נפלתי.", "רגע.", S, "סליחה, אני בסדר, באמת."]),
    ]),
    dict(id="fine_hold_wait_then_fell", situation="v7: fine, hold on, silent (free), then fell", expected=FELL,
         close=4, words=[
        W(["I'm fine.", "Hold on.", S, "Well, I did fall."], ["Estou bem.", "Espere.", S, "Bem, caí."],
          ["אני בסדר.", "רגע.", S, "טוב, נפלתי."]),
        W(["I'm fine.", "Hold on.", S, "I fell, please send someone."], ["Estou bem.", "Espere.", S, "Caí, mande alguém por favor."],
          ["אני בסדר.", "רגע.", S, "נפלתי, בבקשה תשלחי מישהו."], flag=True),
    ]),
    dict(id="fine_hold_wait_then_help", situation="v7: fine, hold on, silent (free), then help", expected=HELP,
         close=4, words=[
        W(["I'm fine.", "Hold on.", S, "Actually, I can't get up."], ["Estou bem.", "Espere.", S, "Afinal, não me consigo levantar."],
          ["אני בסדר.", "רגע.", S, "בעצם, אני לא מצליח לקום."]),
    ]),
    # The wait was used at the first question, so a "hold on" at the confirming question is unclear: the re-ask.
    # The silence after it closes the call by the rules (unable to verify: they spoke). The first "hold on" got
    # the free wait, so it is not one of the 5 answers (Tony 45602); the limit is not reached.
    dict(id="hold_used_then_hold_again", situation="v7: wait used at the first question, hold on again later",
         expected=UNABLE, close=5, words=[
        W(["Hold on.", S, "I'm fine.", "Hold on.", S], ["Espere.", S, "Estou bem.", "Espere.", S],
          ["רגע.", S, "אני בסדר.", "רגע.", S]),
    ]),

    # ---- "so-so" (R2-Q5, R3-Q2) -------------------------------------------------------------------
    dict(id="soso_then_help", situation="v7: so-so, then says what is wrong", expected=HELP, close=2, words=[
        W(["More or less.", "My hip hurts."], ["Mais ou menos.", "Dói-me a anca."], ["ככה ככה.", "הירך כואבת לי."]),
    ]),
    # Lab review (Yair, 2026-11-03): help or unable to verify are both okay here.
    dict(id="soso_twice", situation="v7: so-so after the re-ask is used", expected=HELP, close=2, words=[
        W(["So-so.", "Just so-so."], ["Mais ou menos.", "Assim-assim."], ["ככה ככה.", "סתם ככה ככה."],
          also=[UNABLE]),
        W(["What?", "More or less."], ["O quê?", "Mais ou menos."], ["מה?", "ככה ככה."], also=[UNABLE]),
    ]),
    dict(id="soso_then_fine", situation="v7: so-so, then fine, then confirms", expected=FINE, close=3, words=[
        W(["So-so.", "Just tired, I'm okay.", "I'm not hurt, and I can get up fine."], ["Mais ou menos.", "Só cansado, estou bem.", "Não me magoei, e consigo levantar-me bem."],
          ["ככה ככה.", "סתם עייף, אני בסדר.", "לא נפגעתי, ואני מצליח לקום בסדר."]),
    ]),
    dict(id="fine_soso_then_help", situation="v7: fine, so-so, then says what is wrong", expected=HELP, close=3,
         words=[
        W(["I'm fine.", "So-so.", "My knee."], ["Estou bem.", "Mais ou menos.", "O joelho."], ["אני בסדר.", "ככה ככה.", "הברך."]),
    ]),
    # Lab review (Yair, 2026-11-03): help or unable to verify are both okay here.
    dict(id="fine_soso_twice", situation="v7: fine, so-so, so-so again", expected=HELP, close=3, words=[
        W(["I'm okay.", "More or less.", "So-so."], ["Estou bem.", "Mais ou menos.", "Assim-assim."],
          ["אני בסדר.", "ככה ככה.", "ככה ככה."], also=[UNABLE]),
    ]),

    # ---- the re-ask: what the transitions above do not reach (REASK) -------------------------------
    dict(id="unclear_then_hold", situation="v7: unclear, then hold on (no longer free)", expected=UNABLE, close=2,
         words=[
        W(["What?", "Hold on."], ["O quê?", "Espere."], ["מה?", "רגע."]),
    ]),

    # ---- after the re-ask, the confirming question (CQ_LATE) ---------------------------------------
    dict(id="unclear_fine_then_fell", situation="v7: unclear, fine, then fell", expected=FELL, close=3, words=[
        W(["What?", "Oh, I'm fine.", "Well, I did fall a moment ago."], ["O quê?", "Ah, estou bem.", "Bem, caí há bocado."],
          ["מה?", "אה, אני בסדר.", "טוב, נפלתי לפני רגע."]),
        W(["Who's this?", "I'm okay.", "I fell and I need help."], ["Quem fala?", "Estou bem.", "Caí e preciso de ajuda."],
          ["מי זה?", "אני בסדר.", "נפלתי ואני צריך עזרה."], flag=True),
    ]),
    dict(id="unclear_fine_then_help", situation="v7: unclear, fine, then pain", expected=HELP, close=3, words=[
        W(["What?", "Oh, I'm fine.", "My wrist hurts a bit."], ["O quê?", "Ah, estou bem.", "Dói-me um bocado o pulso."],
          ["מה?", "אה, אני בסדר.", "פרק היד קצת כואב לי."]),
    ]),
    dict(id="unclear_fine_then_soso", situation="v7: unclear, fine, then so-so", expected=HELP, close=3, words=[
        W(["Huh?", "I'm fine.", "So-so."], ["Hã?", "Estou bem.", "Mais ou menos."], ["הא?", "אני בסדר.", "ככה ככה."]),
    ]),
    dict(id="unclear_fine_then_unclear", situation="v7: unclear, fine, then unclear", expected=UNABLE, close=3,
         words=[
        W(["What?", "I'm fine.", "The garden, the... Tuesday."], ["O quê?", "Estou bem.", "O jardim, a... terça."],
          ["מה?", "אני בסדר.", "הגינה, ה... יום שלישי."]),
    ]),
    dict(id="unclear_fine_then_hold", situation="v7: unclear, fine, then hold on (not free)", expected=UNABLE,
         close=3, words=[
        W(["What?", "I'm fine.", "Hold on."], ["O quê?", "Estou bem.", "Espere."], ["מה?", "אני בסדר.", "רגע."]),
    ]),
    dict(id="unclear_denial_then_denial", situation="v7: unclear, denial, then denial", expected=FINE, close=3,
         words=[
        W(["What?", "I didn't fall.", "No, I don't need any help."], ["O quê?", "Não caí.", "Não, não preciso de ajuda."],
          ["מה?", "לא נפלתי.", "לא, אני לא צריך עזרה."]),
    ]),

    # ---- after the confirming question, the re-ask (REASK_LATE) ------------------------------------
    dict(id="fine_unclear_then_fell", situation="v7: fine, unclear, then fell", expected=FELL, close=3, words=[
        W(["I'm fine.", "The... the kettle.", "I fell in the kitchen."], ["Estou bem.", "A... a chaleira.", "Caí na cozinha."],
          ["אני בסדר.", "ה... הקומקום.", "נפלתי במטבח."]),
        W(["I'm fine.", "What?", "I fell, I can't get up."], ["Estou bem.", "O quê?", "Caí, não me consigo levantar."],
          ["אני בסדר.", "מה?", "נפלתי, אני לא מצליח לקום."], flag=True),
    ]),
    dict(id="fine_unclear_then_help", situation="v7: fine, unclear, then help", expected=HELP, close=3, words=[
        W(["I'm fine.", "What?", "I need help, my back hurts."], ["Estou bem.", "O quê?", "Preciso de ajuda, doem-me as costas."],
          ["אני בסדר.", "מה?", "אני צריך עזרה, הגב כואב לי."]),
    ]),
    dict(id="fine_unclear_then_hold", situation="v7: fine, unclear, then hold on (not free)", expected=UNABLE,
         close=3, words=[
        W(["I'm fine.", "What?", "Hold on."], ["Estou bem.", "O quê?", "Espere."], ["אני בסדר.", "מה?", "רגע."]),
    ]),
    dict(id="fine_unsure_then_fine", situation="v7: fine, unsure, then sure", expected=FINE, close=3, words=[
        # 3 Nov run (gpt-6.1-terra): "I think so" answers "Are you hurt anywhere?" as "yes, I'm hurt"; the
        # unsure answer must be unsure whatever the confirming question is.
        W(["I'm fine.", "I'm not sure.", "I'm sure, nothing hurts."], ["Estou bem.", "Não sei bem.", "Tenho a certeza, não me dói nada."],
          ["אני בסדר.", "אני לא בטוח.", "אני בטוח, שום דבר לא כואב."]),
        # B4 (state machine): "I haven't tried" is not reassuring; the re-ask repeats the confirming question.
        W(["I'm fine.", "I haven't tried.", "I can get up fine, nothing hurts."],
          ["Estou bem.", "Ainda não experimentei.", "Consigo levantar-me bem, não me dói nada."],
          ["אני בסדר.", "עוד לא ניסיתי.", "אני מצליח לקום בסדר, שום דבר לא כואב."]),
        W(["I'm okay.", "A bit shaken.", "I'm not hurt, and I can get up fine."], ["Estou bem.", "Um bocado abalado.", "Não me magoei, e consigo levantar-me bem."],
          ["אני בסדר.", "קצת מזועזע.", "לא נפגעתי, ואני מצליח לקום בסדר."]),
    ]),
    dict(id="fine_then_refuses", situation="v7: fine, then refuses", expected=UNABLE, close=3, words=[
        W(["I'm fine.", "Leave me alone.", "Go away."], ["Estou bem.", "Deixe-me em paz.", "Vá-se embora."],
          ["אני בסדר.", "תעזבי אותי בשקט.", "לכי מפה."]),
    ]),

    # ---- other v7 decisions -----------------------------------------------------------------------
    # Speech over Vega is a continuation of the same answer; in the lab it is one merged turn.
    dict(id="overlap_fine_then_hurt", situation="v7: \"I'm fine\" continued with a problem in the same answer",
         expected=HELP, close=1, words=[
        W(["I'm fine... but I hit my head."], ["Estou bem... mas bati com a cabeça."], ["אני בסדר... אבל קיבלתי מכה בראש."]),
    ]),
    # R2-Q4: mild sadness with no injury is no fall; Portuguese ends on the sad farewell.
    dict(id="sad_but_fine", situation="v7: a bit lonely, not hurt", expected=FINE, close=2, words=[
        W(["I'm okay, just a bit lonely today.", "I'm not hurt, and I can get up fine."], ["Estou bem, só um bocadinho sozinho hoje.", "Não me magoei, e consigo levantar-me bem."],
          ["אני בסדר, רק קצת בודד היום.", "לא נפגעתי, ואני מצליח לקום בסדר."]),
    ]),
    # P1 on an unidentified call: "Does anyone need help?" -> "Yes" is help, "No" is a first fine.
    # ---- 2 Nov v7 review: paths no scenario covered --------------------------------------------------
    dict(id="hold_silent_silent", situation="v7: hold on, silent (free), silent, silent (state machine row 287)",
         expected=UNABLE, close=4,
         words=[
        # A "hold on" counts as speaking, so the end is unable to verify, never no response.
        W(["Hold on.", S, S, S], ["Espere.", S, S, S], ["רגע.", S, S, S]),
        W(["One moment, please.", S, S, S], ["Só um momento, por favor.", S, S, S], ["שנייה, בבקשה.", S, S, S]),
    ]),
    dict(id="feels_terrible_during_goodbye", situation="v7: feels terrible during the no-fall goodbye",
         expected=FINE, close=2, after_close=HELP, words=[
        W(["I'm fine.", "Nothing hurts, I can get up."], ["Estou bem.", "Não me dói nada, consigo levantar-me."],
          ["אני בסדר.", "שום דבר לא כואב, אני מצליח לקום."],
          tail=T("Actually, I feel terrible.", "Afinal, sinto-me muito mal.", "בעצם, אני מרגיש נורא.")),
        W(["I'm okay.", "No, I'm not hurt."], ["Estou bem.", "Não, não me magoei."], ["אני בסדר.", "לא, לא נפגעתי."],
          tail=T("Wait, call my daughter.", "Espere, ligue à minha filha.", "רגע, תתקשרי לבת שלי.")),
    ]),
    dict(id="unknown_bare_yes", situation="v7: nobody identified, a bare yes", expected=HELP, close=1,
         prompt="unknown", words=[W(["Yes."], ["Sim."], ["כן."])]),
    dict(id="unknown_bare_no", situation="v7: nobody identified, a bare no, then confirms", expected=FINE, close=2,
         prompt="unknown", words=[
        W(["No.", "Nobody is hurt, everyone is fine."], ["Não.", "Ninguém está magoado, está tudo bem."], ["לא.", "אף אחד לא נפגע, כולם בסדר."]),
    ]),
]


def L(file, old_id, scenario, expected=None, close=None, also=None, extend=None, why=""):
    return dict(file=file, old_id=old_id, scenario=scenario, expected=expected, close=close,
                also_accepted=also, extend=extend, why=why)


B, V0, V1, K, KH, PT = ("inputs_baseline.json", "inputs_v0.json", "inputs_v1.json", "inputs_ks831.json",
                        "inputs_ks831_he.json", "inputs_ks833_ptpt.json")
SILENT_NOW = "KS-714: silence is no_response_from_resident"
UNCLEAR_NOW = "KS-881: still unclear after the re-ask is unable_to_verify"
HURT_NOW = "KS-881 (answer A): hurt / help / unwell without saying they fell is assistance_requested"
CONFIRM_Q = "the confirming question after a first \"I'm fine\" needs a reply"

LEGACY = [
    # baseline = v0 01-08 (v0 is a copy that changed scenario_06); both ids are kept.
    L(B, "scenario_01", "fell"), L(V0, "scenario_01", "fell"),
    L(B, "scenario_02", "fine_confirmed"), L(V0, "scenario_02", "fine_confirmed"),
    L(B, "scenario_03", "still_unclear", why=UNCLEAR_NOW), L(V0, "scenario_03", "still_unclear", why=UNCLEAR_NOW),
    L(B, "scenario_04", "silent_twice", why=SILENT_NOW), L(V0, "scenario_04", "silent_twice", why=SILENT_NOW),
    L(B, "scenario_05", "fine_then_pain", why=HURT_NOW), L(V0, "scenario_05", "fine_then_pain", why=HURT_NOW),
    # "I'm fine now, I got up by myself" implies the fall, like v1 scenario_027; the prompt counts
    # getting back up as saying they fell. The old "no fall" is still accepted.
    L(B, "scenario_06", "unclear_then_fine", expected=FELL, also=[FINE],
      why="baseline (no fall) and v0 (fall) disagreed; \"I got up by myself\" implies the fall (no fall also accepted)"),
    L(V0, "scenario_06", "unclear_then_fine", expected=FELL, also=[FINE],
      why="baseline (no fall) and v0 (fall) disagreed; \"I got up by myself\" implies the fall (no fall also accepted)"),
    L(B, "scenario_07", "still_unclear", why=UNCLEAR_NOW), L(V0, "scenario_07", "still_unclear", why=UNCLEAR_NOW),
    L(B, "scenario_08", "fine_then_fell", close=[2, 3],
      why="\"I did slip a little bit\" may or may not be read as the fall; both closings are right"),
    L(V0, "scenario_08", "fine_then_fell", close=[2, 3],
      why="\"I did slip a little bit\" may or may not be read as the fall; both closings are right"),
    L(V0, "scenario_09", "fell"),
    L(V0, "scenario_10", "hurt_no_fall", also=["distress_fall_confirmed"],
      why=HURT_NOW + "; \"hit my head on the floor\" may be read as a fall"),
    L(V0, "scenario_11", "still_unclear", expected="distress_assistance_requested", close=2,
      why="the words \"I'm scared\" are a call for help (Tony 45602)"),
    L(V0, "scenario_12", "still_unclear", why=UNCLEAR_NOW),
    L(V0, "scenario_13", "asks_help", why=HURT_NOW),
    L(V0, "scenario_14", "fell"),
    L(V0, "scenario_15", "fell_and_help", close=[1, 2], also=["distress_assistance_requested"],
      why="broken words that include \"fell\" and \"help\"; Vega may act at once or re-ask"),
    # ks831 (en) and its Hebrew copy
    *[L(f, i, "still_unclear", why=UNCLEAR_NOW) for f in (K, KH)
      for i in ("u1_garbled_story", "u2_rambling_offtopic", "u3_broken_fragments", "u4_confused", "u5_asr_noise")],
    *[L(f, "f1_i_fell", "fell") for f in (K, KH)],
    *[L(f, "f2_hurt", "hurt_no_fall", why=HURT_NOW) for f in (K, KH)],
    *[L(f, "f3_need_help", "asks_help", why=HURT_NOW) for f in (K, KH)],
    *[L(f, i, "fine_confirmed") for f in (K, KH) for i in ("ok1_fine", "ok2_dropped_something")],
    *[L(f, i, "silent_twice") for f in (K, KH) for i in ("s1_silent", "s2_silent_after_greeting_long")],
    # ks833 (pt-PT)
    *[L(PT, i, "fine_confirmed") for i in ("safe_estou_bem", "safe_obrigado", "safe_gato", "safe_azorean")],
    L(PT, "safe_sim_nao", "fine_confirmed", close=[2, 3], extend=["Sim, estou bem."],
      why="a bare \"Sim\" is not enough in Portuguese, so \"não me magoei\" may be the first fine answer; " + CONFIRM_Q),
    L(PT, "safe_apanhar", "denial_then_fine"),
    L(PT, "help_preciso_ajuda", "asks_help", why=HURT_NOW),
    L(PT, "help_casa_de_banho", "fell"),
    L(PT, "help_doi_perna", "hurt_no_fall", why=HURT_NOW),
    L(PT, "help_socorro", "asks_help", why=HURT_NOW),
    L(PT, "help_nao", "asks_help", why=HURT_NOW + "; a bare \"Não\" to \"Está bem?\" means they are not okay"),
    L(PT, "help_nao_consigo_levantar", "fell"),
    L(PT, "help_nossa_senhora", "fell"),
    L(PT, "help_fine_then_hip", "fine_then_pain", why=HURT_NOW),
    L(PT, "help_deny_then_admit", "fine_then_fell"),
    L(PT, "help_misrec_sai", "misheard_alert", expected="distress_unable_to_verify", close=1,
      why="\"saí\" / \"boi\" are misheard \"caí\" / \"dói\": not certain, so unable to verify at once (Tony 45602)"),
    L(PT, "unclear_offtopic", "still_unclear", why=UNCLEAR_NOW),
    L(PT, "unclear_nao_sei", "still_unclear", why=UNCLEAR_NOW),
    L(PT, "unclear_cut_off", "interrupted", expected="distress_unable_to_verify", also=["distress_assistance_requested"],
      why="cut off, then only \"a perna\": unable to verify, or read as a leg problem"),
    L(PT, "unclear_contradiction", "interrupted", expected="distress_assistance_requested", close=[1, 2],
      also=["distress_unable_to_verify"], why="\"Estou bem... não, não estou\" says they are not okay; a re-ask is also fair"),
    L(PT, "unclear_english_garble", "still_unclear", why=UNCLEAR_NOW),
    L(PT, "unclear_ha", "what_twice", why=UNCLEAR_NOW),
    L(PT, "silence_full", "silent_twice"),
    L(PT, "silence_explicit", "silent_twice"),
    L(PT, "asr_qi_cozinha", "misheard_alert", expected="distress_unable_to_verify", close=1,
      why="a misheard \"caí\" is not certain: unable to verify at once (Tony 45602)"),
    L(PT, "asr_bare_ti", "still_unclear", close=[1, 2],
      why=UNCLEAR_NOW + "; \"TI\" may be a misheard \"caí\": unable to verify at once (Tony 45602)"),
    L(PT, "asr_nao_qi", "unclear_then_fine", close=[2, 3], why="kept from KS-833: fine only after two spoken answers"),
    L(PT, "asr_na_na", "still_unclear", why=UNCLEAR_NOW),
    L(PT, "asr_maguinada", "unclear_then_fine", close=[2, 3], why="kept from KS-833: fine only after two spoken answers"),
]

# inputs_v1.json: scenario -> (new scenario, overrides). Grouped by where they land.
V1_MAP = {
    "fell": "016 023 029 034 045 059 061 063 068 077 094 098",
    "fell_and_help": "036",                              # "I fell... please send someone"
    "fell_slipped": "002 007 040 056 083 088 092",       # slipped / tripped / rolled off: fell, or hurt
    "hurt_no_fall": "021 048 051 074",
    "asks_help": "012 043 050 066 086",
    "unwell_no_fall": "009 025 031 038 070 075",
    "fine_confirmed": "003 006 008 010 015 018 020 026 030 035 039 042 047 052 055 058 062 067 069 073 076 079 "
                      "082 085 089 096 100",
    "denial_then_fine": "022",
    "fine_then_pain": "011 080",
    "fine_then_fell": "001 014 060 090",
    "unclear_then_fell": "054 072",
    "unclear_then_fine": "037 091",
    "unclear_then_fine_ext": "093 097",
    "silence_then_problem": "071 081",
    "silence_then_fine": "064",
    "silence_then_fine_ext": "017 087",
    "fine_then_silent": "099",
    "still_unclear": "004 013 019 024 027 028 032 033 044 046 049 065 078 084 095",
    "what_twice": "057",
    "mixed_no_restart": "053",
    "silent_twice": "005 041",
}
V1_OVERRIDES = {
    "fell_slipped": dict(scenario="fell", close=[1, 2], also=["distress_assistance_requested"],
                         why="slipped / tripped / collapsed: a fall, or hurt without saying \"fell\""),
    "hurt_no_fall": dict(also=["distress_fall_confirmed"], why=HURT_NOW + "; the injury may be read as a fall"),
    "asks_help": dict(why=HURT_NOW + " (the first answer asks for help; \"I fell\" comes too late)"),
    "unwell_no_fall": dict(why=HURT_NOW),
    "fine_then_pain": dict(why=HURT_NOW),
    "unclear_then_fell": dict(close=[1, 2], also=["distress_assistance_requested"],
                              why="the first answer implies a fall without saying it; acting at once is also right"),
    "unclear_then_fine": dict(why="FR v3 D16: unclear, then clearly okay, is no alert"),
    "unclear_then_fine_ext": dict(scenario="unclear_then_fine", close=[2, 3], extend=["I'm not hurt at all, I can move fine."],
                                  why="the first answer may get the re-ask; " + CONFIRM_Q),
    "silence_then_problem": dict(why="KS-881: the first silence gets the re-ask"),
    "silence_then_fine_ext": dict(scenario="silence_then_fine", extend=["I'm not hurt at all, I can move fine."],
                                  why="old expectation was a fall alert; " + CONFIRM_Q),
    "fine_then_silent": dict(why="KS-881: fine, then silent through the confirming question and the re-ask; "
                                 "they spoke, so unable to verify (Tony, NUN-1626 44793)"),
    "still_unclear": dict(why=UNCLEAR_NOW),
    "what_twice": dict(why=UNCLEAR_NOW),
    "mixed_no_restart": dict(why=UNCLEAR_NOW + "; the silence used the re-ask"),
    "silent_twice": dict(why=SILENT_NOW),
}
for group, ids in V1_MAP.items():
    o = V1_OVERRIDES.get(group, {})
    for n in ids.split():
        LEGACY.append(L(V1, f"scenario_{n}", o.get("scenario", group), close=o.get("close"),
                        also=o.get("also"), extend=o.get("extend"), why=o.get("why", "")))
for item in LEGACY:
    # 027 "I managed to get up by myself": getting up implies the fall (prompt: "I got myself up off the
    # floor" is saying they fell); unable to verify is also fair.
    if item["file"] == V1 and item["old_id"] == "scenario_027":
        item.update(expected=FELL, close=[1, 2], also_accepted=[UNABLE],
                    why="\"managed to get up by myself\" implies the fall; unable to verify is also fair")
    # 084 "Hmm... I guess so..." may be read as a hesitant "fine" (confirming question, then the re-ask):
    # then it closes on the 3rd answer, which is silence after speech: still unable to verify (Tony 44793).
    if item["file"] == V1 and item["old_id"] == "scenario_084":
        item.update(close=[2, 3],
                    why=UNCLEAR_NOW + "; \"I guess so\" may get the confirming question first")
    # 070 "Everything looks blurry and strange": vague enough that asking what is wrong first is fair.
    if item["file"] == V1 and item["old_id"] == "scenario_070":
        item.update(close=[1, 2], why=HURT_NOW + "; the first answer is vague enough to ask what is wrong")
    # 081 "<silence> | ...help...": a request for help, no fall said.
    if item["file"] == V1 and item["old_id"] == "scenario_081":
        item.update(expected=HELP, why=HURT_NOW)
