# -*- coding: utf-8 -*-
"""KS-881 step 3 (minimized prompts, lab draft), en / pt / he.

Builds data/prompts/prompt_ks881_<label>_<lang>[_unknown].txt from v8_<lang>_instructions.txt and the input part
the server renders for v7g, and copies v7g's server checks. The unidentified variant is derived the way the
server derives it: the NUN-1625/1626 preamble and rules first (pt and he: the server's own text, from the v7g
render), [name] slots removed, the unidentified opening, gender-neutral address.

Usage: python tools/ks881/build_v8.py <label>
"""
import json
import shutil
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
P = LAB / "data" / "prompts"
HERE = Path(__file__).parent
label = sys.argv[1] if len(sys.argv) > 1 else "v8"
PRE = json.loads((HERE / "v8_unknown_preambles.json").read_text(encoding="utf-8"))
PRE["en"] = (
    "More than one person was in the home, so NOBODY HAS BEEN IDENTIFIED: you do not know who fell, and the "
    "person who answers you may be the one who fell, another senior or a visitor. Below, \"the senior\" means "
    "whoever answers you. If they tell you that someone else fell, is hurt or needs help, treat it exactly as if "
    "they had said it about themselves.\n"
    "* VISITOR RULE: a visitor may report a fall or request assistance. Never say or suggest that you now know who "
    "fell. Until caregivers can close such an incident themselves, a clear \"we're fine\" still closes as "
    "'no_fall_confirmed' after the confirming question, like any senior's.\n"
    "* A bare \"No\" to \"Does anyone need help?\" is a first reassuring answer: ask the confirming question. A bare "
    "\"Yes\" is a request for help: 'distress_assistance_requested'.\n"
    "* NAME RULE: you do not know who you are talking to. Never use, guess or invent a name, even if someone tells "
    "you one, and never address anyone by a label or role (\"resident\", \"senior\", \"sir\", \"madam\").\n"
    "* GENDER: you do not know the gender of whoever answers: never assume male or female. The mandated phrases "
    "are said word for word.\n\n")

LANG = {
    "en": dict(
        greeting=("1. GREETING (empty history): greet them by name, say you are Vega and received a fall alert, and "
                  "ask one question: are they okay? Outcome 'conversation_in_progress'."),
        greeting_unknown=("1. GREETING (empty history): introduce yourself as Vega, then say this sentence word for "
                          "word and nothing else: \"A possible fall was detected. Does anyone need help?\" Do not ask "
                          "whether the person answering fell or is okay. Outcome 'conversation_in_progress'."),
        drop=[" Use the senior's gender from the call's details for grammar (default male). Where these examples "
              "show [name], use the senior's first name.", " (you may add their first name)"]),
    "pt": dict(
        greeting=("1. CUMPRIMENTO (histórico vazio): cumprimente o sénior pelo nome, apresente-se como Vega, diga que "
                  "recebeu um alerta de queda e faça uma só pergunta: se está bem. Exemplo: \"Olá, [name], fala a "
                  "Vega. Detetámos uma possível queda. Está bem?\" Resultado 'conversation_in_progress'."),
        greeting_unknown=("1. CUMPRIMENTO (histórico vazio): apresente-se como Vega e depois diga esta frase, palavra "
                          "por palavra, e mais nada: \"Foi detetada uma possível queda. Alguém precisa de ajuda?\" Não "
                          "pergunte se quem atende caiu ou se está bem. Resultado 'conversation_in_progress'."),
        drop=[" Onde estes exemplos mostram [name], use o primeiro nome do sénior."]),
    "he": dict(
        greeting=("1. ברכה (היסטוריה ריקה): ברכי את הקשיש בשמו, הציגי את עצמך כוגה, אמרי שקיבלת התראה על נפילה, "
                  "ושאלי שאלה אחת: האם הכל בסדר. דוגמה: \"שלום [name], כאן וגה. קיבלתי התראה שאולי נפלתָ. הכל "
                  "בסדר?\" תוצאה 'conversation_in_progress'."),
        greeting_unknown=("1. ברכה (היסטוריה ריקה): הציגי את עצמך כוגה, ואז אמרי את המשפט הזה מילה במילה, ותו לא: "
                          "\"זוהתה נפילה אפשרית. האם מישהו צריך עזרה?\" אל תשאלי אם מי שעונה נפל או אם הוא בסדר. "
                          "תוצאה 'conversation_in_progress'."),
        drop=[" איפה שהדוגמאות מראות [name], השתמשי בשם הפרטי של הקשיש.", " (אפשר להוסיף את השם הפרטי שלו)"]),
}

langs = sys.argv[2].split(",") if len(sys.argv) > 2 else list(LANG)
for lang in langs:
    c = LANG[lang]
    named = (HERE / f"v8_{lang}_instructions.txt").read_text(encoding="utf-8").strip()
    assert c["greeting"] in named, f"{lang}: greeting not found"
    unknown = named.replace(c["greeting"], c["greeting_unknown"])
    for d in c["drop"]:
        assert d in unknown, f"{lang}: not found: {d[:40]}"
        unknown = unknown.replace(d, "")
    unknown = unknown.replace(", [name]", "").replace(" [name]", "")
    assert "[name]" not in unknown, f"{lang}: [name] left"
    unknown = PRE[lang] + unknown
    for sfx, ins in (("", named), ("_unknown", unknown)):
        src = (P / f"prompt_ks881_v7g_{lang}{sfx}.txt").read_text(encoding="utf-8")
        inp = src.split("@@SPLIT@@", 1)[1]
        (P / f"prompt_ks881_{label}_{lang}{sfx}.txt").write_text(ins + "\n@@SPLIT@@" + inp, encoding="utf-8")
shutil.copy(P / "server_checks_ks881_v7g.json", P / f"server_checks_ks881_{label}.json")
print(f"{label}: {', '.join(langs)} written (named + unknown)")
