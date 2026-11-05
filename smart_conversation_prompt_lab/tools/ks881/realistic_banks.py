# -*- coding: utf-8 -*-
"""KS-881 realistic set: the phrase banks in Portuguese (pt-PT) and Hebrew, line for line with the English banks in
build_realistic.py (same index = same meaning), so a conversation is the same test in every language. The misheard
falls (MIS) use each language's own recognition errors (the prompts' lists). The lab's own wordings: they need a
native speaker's review (Sandra for Portuguese).

Also the unidentified-caller banks (U*), for the NUN-1625/1626 opening "A possible fall was detected. Does anyone
need help?", in all three languages."""

PT = {
    "F": ["Caí.", "Sim, caí.", "Caí na casa de banho.", "Caí na cozinha.", "Escorreguei e caí.", "Dei uma queda.",
          "Tropecei e caí no corredor.", "Caí da cama.", "Sim, caí, mas estou bem.", "Estou no chão.",
          "Dei um trambolhão na sala.", "Caí da cadeira.", "Escorreguei no duche e caí.", "Sim, caí.",
          "Caí nas escadas.", "Caí no jardim.", "Perdi o equilíbrio e caí.", "Caí ao sair da banheira.",
          "Caí ao pé da cama.", "Sim, caí, estou no chão.", "Caí para trás.", "Fui ao chão na cozinha.",
          "Caí, mas já me levantei.", "Caí hoje de manhã.", "Caí quando me levantei.", "Caí ao pé da porta.",
          "Sim, dei uma queda no quarto.", "Caí por cima do cão.", "Escorreguei no tapete e caí.",
          "Caí, estou sentado no chão."],
    "FH": ["Caí e não me consigo levantar.", "Caí, ajude-me por favor.", "Caí e magoei a anca.", "Caí e dói-me o braço.",
           "Caí e preciso de ajuda.", "Caí na casa de banho e dói-me a cabeça.", "Caí e não consigo mexer a perna.",
           "Socorro, caí.", "Caí e estou a sangrar.", "Caí, ligue ao meu filho por favor.", "Caí e dói-me muito o pulso.",
           "Caí e estou tonto.", "Caí de costas e dói.", "Caí e não consigo pôr-me de pé.",
           "Caí, preciso de uma ambulância.", "Caí e bati com a cabeça."],
    "MIS": ["QI na cozinha.", "Kí na casa de banho.", "Ei TI no chão.", "QI da cama.", "Kí no quarto.", "QI no chão.",
            "Ki na cozinha.", "TI no corredor.", "K í da cadeira.", "Kí nas escadas."],
    "H": ["Preciso de ajuda.", "Ajude-me, por favor.", "Socorro.", "Dói-me as costas.", "Bati com a cabeça.",
          "Não me consigo levantar.", "Estou tonto.", "Não me sinto bem.", "Pode ligar à minha filha?",
          "Magoei o joelho.", "Dói.", "Tenho dores.", "Sinto-me muito fraco.", "Dói-me o peito.",
          "Não consigo respirar bem.", "Preciso que venha alguém.", "Dói-me a perna.", "Sinto-me mal disposto.",
          "Magoei as costas.", "Mande alguém, por favor.", "Não consigo pôr-me de pé.", "Dói-me a cabeça.",
          "Não estou a sentir-me bem.", "Preciso de um médico.", "Cortei a mão.", "Chame uma ambulância.",
          "Dói-me o braço.", "Sinto que vou desmaiar."],
    "FI": ["Estou bem.", "Sim, estou bem.", "Estou bem, obrigado.", "Está tudo bem aqui.", "Sim, estou ótimo.",
           "Estou bem, não aconteceu nada.", "Ah, estou bem, querida.", "Estou a andar bem.", "Estou bem, obrigado.",
           "Estou bem, obrigado por perguntar.", "Tudo bem por aqui.", "Estou perfeitamente bem."],
    "D": ["Não caí.", "Não, não caí, só me sentei.", "Não caí, deixei cair um livro.", "Não caiu nada, foi o gato.",
          "Não caí, não se preocupe.", "Não, não caí, só me estava a baixar."],
    "CF": ["Não me magoei nada e não preciso de nada.", "Está tudo bem, não me dói nada.",
           "Estou mesmo bem, não me dói nada e já ando por aqui.", "Tenho a certeza, estou perfeitamente bem.",
           "A sério, não se passa nada.", "Tudo bem, ando normalmente.", "Não me dói nada, estou bem, obrigado.",
           "Estou ótimo, nenhuma dor."],
    "CP": ["Afinal, dói-me a anca.", "Bem, dói-me um bocadinho as costas.", "Afinal, não me consigo levantar.",
           "Sinto-me um bocado tonto, para ser sincero.", "Dói-me o pulso.", "Afinal, preciso de alguma ajuda.",
           "Dói-me o joelho.", "Agora que pergunta, dói-me a cabeça."],
    "CFALL": ["Afinal, caí.", "Bem, caí no corredor.", "Afinal, caí há um minuto."],
    "UNS": ["Não sei bem.", "Não sei.", "Não sei mesmo.", "Não sei bem o que aconteceu."],
    "U": ["O quê?", "Como?", "Quem fala?", "O que disse?", "Hã?", "Desculpe?", "Não a estou a ouvir.", "Está?"],
    "HO": ["Espere.", "Só um momento.", "Espere um segundo.", "Um momento, por favor."],
    "S": [""],
    "YF": ["Sim, caí.", "Sim, caí ao chão.", "Caí, sim."],
}

HE = {
    "F": ["נפלתי.", "כן, נפלתי.", "נפלתי במקלחת.", "נפלתי במטבח.", "החלקתי ונפלתי.", "הייתה לי נפילה.",
          "מעדתי ונפלתי במסדרון.", "נפלתי מהמיטה.", "כן, נפלתי, אבל אני בסדר.", "אני על הרצפה.",
          "נפלתי בסלון.", "נפלתי מהכיסא.", "החלקתי במקלחת ונפלתי.", "כן, נפלתי.", "נפלתי במדרגות.",
          "נפלתי בגינה.", "איבדתי שיווי משקל ונפלתי.", "נפלתי כשיצאתי מהאמבטיה.", "נפלתי ליד המיטה.",
          "כן, נפלתי, אני על הרצפה.", "נפלתי אחורה.", "נפלתי במטבח על הרצפה.", "נפלתי, אבל כבר קמתי.",
          "נפלתי הבוקר.", "נפלתי כשקמתי.", "נפלתי ליד הדלת.", "כן, הייתה לי נפילה בחדר השינה.",
          "נפלתי על הכלב.", "החלקתי על השטיח ונפלתי.", "נפלתי, אני יושב על הרצפה עכשיו."],
    "FH": ["נפלתי ואני לא מצליח לקום.", "נפלתי, תעזרי לי בבקשה.", "נפלתי ונפגעתי בירך.", "נפלתי והיד כואבת לי.",
           "נפלתי ואני צריך עזרה.", "נפלתי במקלחת והראש כואב לי.", "נפלתי ואני לא יכול להזיז את הרגל.",
           "הצילו, נפלתי.", "נפלתי ואני מדמם.", "נפלתי, תתקשרי לבן שלי בבקשה.", "נפלתי וכואב לי מאוד בפרק היד.",
           "נפלתי ויש לי סחרחורת.", "נפלתי על הגב וזה כואב.", "נפלתי ואני לא מצליח לעמוד.",
           "נפלתי, אני צריך אמבולנס.", "נפלתי וקיבלתי מכה בראש."],
    "MIS": ["נפחתי במטבח.", "כפלתי במקלחת.", "נפשתי על הרצפה.", "נפחתי מהמיטה.", "כפלתי בחדר.", "נפחתי על הרצפה.",
            "נפשתי במטבח.", "כפלתי במסדרון.", "נפחתי מהכיסא.", "נפשתי במדרגות."],
    "H": ["אני צריך עזרה.", "תעזרי לי, בבקשה.", "הצילו.", "הגב כואב לי.", "קיבלתי מכה בראש.", "אני לא מצליח לקום.",
          "יש לי סחרחורת.", "אני לא מרגיש טוב.", "את יכולה להתקשר לבת שלי?", "נפגעתי בברך.", "כואב לי.",
          "יש לי כאבים.", "אני מרגיש חלש מאוד.", "כואב לי בחזה.", "קשה לי לנשום.", "אני צריך שמישהו יבוא.",
          "הרגל כואבת לי.", "אני מרגיש בחילה.", "נפגעתי בגב.", "תשלחי מישהו, בבקשה.", "אני לא מצליח לעמוד.",
          "הראש כואב לי.", "אני לא מרגיש בסדר.", "אני צריך רופא.", "חתכתי את היד.", "תזמיני אמבולנס.",
          "היד כואבת לי.", "אני מרגיש שאני עומד להתעלף."],
    "FI": ["אני בסדר.", "כן, אני בסדר.", "אני בסדר, תודה.", "הכל בסדר פה.", "כן, אני מצוין.",
           "אני בסדר, לא קרה כלום.", "אה, אני בסדר, יקירתי.", "אני מרגיש טוב.", "אני מרגיש טוב, תודה.",
           "אני בסדר, תודה ששאלת.", "הכל טוב פה.", "אני בסדר גמור."],
    "D": ["לא נפלתי.", "לא, לא נפלתי, רק התיישבתי.", "לא נפלתי, הפלתי ספר.", "שום דבר לא נפל, זה היה החתול.",
          "לא נפלתי, אל תדאגי.", "לא, לא נפלתי, רק התכופפתי."],
    "CF": ["לא נפגעתי בכלל ואני לא צריך כלום.", "הכל בסדר, שום דבר לא כואב.",
           "אני באמת בסדר, שום דבר לא כואב ואני מסתובב.", "אני בטוח, אני בסדר גמור.", "באמת, שום דבר לא קרה.",
           "הכל טוב, אני הולך כרגיל.", "שום דבר לא כואב, אני בסדר, תודה.", "אני בסדר גמור, אין שום כאב."],
    "CP": ["בעצם, הירך כואבת לי.", "טוב, הגב קצת כואב לי.", "בעצם, אני לא מצליח לקום.", "יש לי קצת סחרחורת, האמת.",
           "פרק היד כואב לי.", "בעצם, אני כן צריך קצת עזרה.", "הברך כואבת לי.", "עכשיו שאת שואלת, הראש כואב לי."],
    "CFALL": ["בעצם, נפלתי.", "טוב, נפלתי במסדרון.", "בעצם, נפלתי לפני דקה."],
    "UNS": ["אני לא בטוח.", "אני לא יודע.", "אני באמת לא יודע.", "אני לא בטוח מה קרה."],
    "U": ["מה?", "סליחה?", "מי זה?", "מה אמרת?", "הא?", "סליחה, מה?", "אני לא שומע אותך.", "הלו?"],
    "HO": ["רגע.", "רק רגע.", "חכי שנייה.", "רגע אחד, בבקשה."],
    "S": [""],
    "YF": ["כן, נפלתי.", "כן, נפלתי על הרצפה.", "נפלתי, כן."],
}

# Unidentified caller (multiplePeoplePresent): Vega asks whether ANYONE needs help.
UNKNOWN = {
    "UF": ("FELL", {
        "en": ["My husband fell in the kitchen.", "My wife has fallen.", "Yes, my mother fell.", "Someone fell in the bathroom.",
               "My father fell on the stairs.", "I fell."],
        "pt": ["O meu marido caiu na cozinha.", "A minha mulher caiu.", "Sim, a minha mãe caiu.", "Alguém caiu na casa de banho.",
               "O meu pai caiu nas escadas.", "Caí."],
        "he": ["בעלי נפל במטבח.", "אשתי נפלה.", "כן, אמא שלי נפלה.", "מישהו נפל במקלחת.", "אבא שלי נפל במדרגות.", "נפלתי."]}),
    "UH": ("HELP", {
        "en": ["Yes, we need help.", "My mother can't get up.", "My husband is in pain.", "Please send someone.",
               "Yes, my wife feels very dizzy.", "We need an ambulance."],
        "pt": ["Sim, precisamos de ajuda.", "A minha mãe não se consegue levantar.", "O meu marido tem dores.",
               "Mande alguém, por favor.", "Sim, a minha mulher está muito tonta.", "Precisamos de uma ambulância."],
        "he": ["כן, אנחנו צריכים עזרה.", "אמא שלי לא מצליחה לקום.", "לבעלי יש כאבים.", "תשלחי מישהו, בבקשה.",
               "כן, לאשתי יש סחרחורת חזקה.", "אנחנו צריכים אמבולנס."]}),
    "UFINE": ("FINE", {
        "en": ["No, we're all fine here.", "Nobody needs help, thank you.", "We're okay, nothing happened.",
               "Everyone is fine here.", "No help needed, we're fine."],
        "pt": ["Não, estamos todos bem.", "Ninguém precisa de ajuda, obrigado.", "Estamos bem, não aconteceu nada.",
               "Está toda a gente bem.", "Não é preciso ajuda, estamos bem."],
        "he": ["לא, כולנו בסדר פה.", "אף אחד לא צריך עזרה, תודה.", "אנחנו בסדר, לא קרה כלום.", "כולם בסדר פה.",
               "לא צריך עזרה, אנחנו בסדר."]}),
    "UCF": ("FINE", {
        "en": ["Nobody is hurt, everyone is fine.", "Really, we're all okay, nobody fell.", "Everyone is up and nothing hurts."],
        "pt": ["Ninguém se magoou, está tudo bem.", "A sério, estamos todos bem, ninguém caiu.",
               "Estão todos de pé e não dói nada a ninguém."],
        "he": ["אף אחד לא נפגע, כולם בסדר.", "באמת, כולנו בסדר, אף אחד לא נפל.", "כולם עומדים ושום דבר לא כואב."]}),
}

UNKNOWN_PATHS = [
    ("fall", ["UF"], 10), ("fall", ["U", "UF"], 6), ("help", ["UH"], 8), ("help", ["U", "UH"], 4),
    ("fine", ["UFINE", "UCF"], 12), ("unclear", ["U", "U"], 4), ("silent", ["S", "S"], 3),
]
