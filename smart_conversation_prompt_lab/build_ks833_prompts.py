#!/usr/bin/env python3
"""
KS-833: render the European Portuguese (pt-PT) fall prompts from the production replica.

Base: data/prompts/prompt_ks833_base_en.txt — ContextDistressFallDetected.buildPrompt()
rendered from the a475i Java with language "en" (byte-identical to production apart from the
@@HISTORY@@ placeholder).

Outputs:
  prompt_ks833_ptpt_asis.txt     — what production would send TODAY for language "pt-PT":
                                   the Java has no Portuguese branch, so only the language line
                                   changes. Baseline.
  prompt_ks833_ptpt_v1_male.txt  — the same prompt plus Portuguese branches, inserted exactly
  prompt_ks833_ptpt_v1_female.txt  where the Java inserts its Hebrew branches, so each insertion
                                   maps 1:1 onto an `isPortuguese()` branch when this is ported.

Every insertion is an exact-match replace that must hit exactly once, so a change to the base
prompt fails loudly instead of silently producing a different prompt.

render_fall_prompt() builds the same prompt from a language pack (language_packs.py), the
design approved for the Java port; main() checks that it reproduces v5 byte for byte.

Usage:
    python build_ks833_prompts.py
"""
from pathlib import Path

from language_packs import resolve_language_pack

PROMPTS = Path(__file__).parent / "data/prompts"
BASE = PROMPTS / "prompt_ks833_base_en.txt"

LANG_EN = ("* The current spoken language is en. This means both the user and the assistant "
           "should speak in en. Make sure to use the correct language for the conversation.")
LANG_PT = LANG_EN.replace(" en.", " pt-PT.")

INFO_EN = '{"seniorName":"David","seniorGender":"male","currentTime":"2026-10-06T18:39:45.000"}'
INFO_PT_MALE = '{"seniorName":"Manuel","seniorGender":"male","currentTime":"2026-10-06T18:39:45.000"}'
INFO_PT_FEMALE = '{"seniorName":"Maria","seniorGender":"female","currentTime":"2026-10-06T18:39:45.000"}'

# Mandated phrases. Java: ContextDistressFallDetected._buildPrompt, the isHebrew() ternaries.
ALERT_EN = "\"I'm raising an alert in the SeniorMatics system.\""
ALERT_PT = "\"Estou a enviar um alerta no sistema SeniorMatics.\""
NORESP_EN = "\"I could not reach you, so I am notifying your caregivers now.\""
NORESP_PT = "\"Não consegui falar consigo, por isso estou a avisar os seus cuidadores.\""

# Java: ContextDistressFallDetected additionalGuidelines, "Opening message" line.
OPENING_ANCHOR = 'Example (Hebrew): "שלום [שם], כאן וגה. קיבלתי התראה שאולי נפלת. הכל בסדר?"'
OPENING_PT = (' Example (European Portuguese): "Olá, senhor Manuel, fala a Vega. '
              'Detetámos uma possível queda. Está bem?"')

# Java: ContextBase.languageGuidelines, after the Hebrew register sentence.
LANGUAGE_PT = (
    " Write ONLY in European Portuguese, as spoken in Portugal (português europeu) — NEVER Brazilian Portuguese."
    " Use European vocabulary, spelling and grammar: \"estou a ouvir\" (not \"estou ouvindo\"),"
    " \"casa de banho\", \"telemóvel\", \"Detetámos\"."
    " Address the senior formally and warmly as \"o senhor\" / \"a senhora\" (or by name) with third-person verbs"
    " (\"Está bem?\", \"Consegue levantar-se?\") — never \"tu\" and never Brazilian \"você\"."
    " Keep it simple and clear: the senior is elderly and may speak with an Azorean accent."
    " Every example phrase in these guidelines is given in English or Hebrew only to illustrate"
    " the meaning — always say it in European Portuguese, never in English.")

# Java: ContextBase.roleGuidelines, after the Hebrew self-introduction line.
ROLE_ANCHOR = "    - When greeting the senior, always introduce yourself by name (e.g., \"Hi, it's Vega!\").\n"
ROLE_PT = ("    - In European Portuguese, introduce yourself as \"fala a Vega\" or \"é a Vega\", and use "
           "feminine forms for yourself (obrigada, preocupada, contente).\n")

# Java: ContextBase.asrGuidelines, where the HEBREW ASR GUIDANCE block goes.
ASR_ANCHOR = ("a word that doesn't make sense in context may be a misrecognition of a contextually "
              "relevant word.\n")
ASR_PT = (
    "* PORTUGUESE ASR GUIDANCE — the senior speaks European Portuguese, often with a strong Azorean "
    "(e.g. São Miguel) accent, which speech recognition handles poorly:\n"
    "    - Vowels are often swallowed or changed and word endings dropped, so the transcription may be "
    "fragmented, come out with Brazilian spellings, or even come out as English words. Scan for ANY "
    "recognizable Portuguese word or root before deciding the answer is unclear.\n"
    "    - Accept common variants of the key answers: \"estou bem\" / \"tou bem\" / \"tô bem\" / \"está tudo bem\"; "
    "\"preciso de ajuda\" / \"ajuda\" / \"socorro\"; \"sim\" / \"pois\" / \"é\"; \"não\" / \"nã\".\n"
    "    - A short \"sim\" or \"não\" means what it answers: check the question you just asked before "
    "deciding whether it means the senior is fine or not.\n"
    "    - When the transcription is mostly unintelligible but contains even one safety-critical word "
    "(caí, queda, dói, dores, ajuda, socorro, não estou bem), escalate — do not ask for clarification.\n"
    "    - If the answer is unclear, ask the senior to repeat IN PORTUGUESE "
    "(e.g. \"Desculpe, não percebi. Pode repetir?\"). An unclear answer is NEVER confirmation that they are fine.\n")

# Java: ContextBase.genderGuidelines, where the Hebrew gender block goes.
GENDER_ANCHOR = "    - When addressing a female senior, make sure verbs and pronouns match feminine forms.\n"
GENDER_PT = ("* Portuguese gender: address a male senior as \"o senhor\" (magoado, sozinho, cansado) and a "
             "female senior as \"a senhora\" (magoada, sozinha, cansada).\n")

# Java: ContextBase.ttsGuidelines, after the last bullet (where the Hebrew TTS bullets go).
TTS_ANCHOR = ("    - Never use markdown, ALL CAPS, emojis, or parenthetical asides — TTS reads them "
              "literally or they disrupt flow.\n")
TTS_PT = ("    - Spell out numbers, times and abbreviations in Portuguese words (\"três vezes por dia\", "
          "\"senhor doutor\"). The contraction examples above are English: in Portuguese, just write "
          "natural spoken European Portuguese.\n")

# Java: ContextDistressFallDetected.getScenarioAsrGuidelines — appended for Portuguese only.
SCENARIO_ASR_ANCHOR = ("treat it as a likely misrecognition of \"I had a fall\" and ask the senior "
                       "to confirm.\n")
# The caí / nã / magoei forms marked "measured" were produced by Azure pt-PT on the 8 kHz hub path
# in the KS-834 ASR lab (asr_ptpt_lab: results/tts_baseline, plus "TI"/"Ei TI" from a real speaker); the others are expected confusions.
SCENARIO_ASR_PT = (
    "* In Portuguese, the following are commonly misrecognized and may be fall-related words:\n"
    "  - \"QI\", \"TI\", \"Ei TI\", \"K í\", \"Kí\", \"ki\", \"cai\", \"aí\" or \"saí\" may actually be \"caí\" (I fell) — "
    "e.g. \"QI na cozinha\" → \"caí na cozinha\", \"Não QI\" → \"não caí\"\n"
    "  - \"Na\" or \"Na na\" may actually be \"nã\" / \"não\" (no, Azorean)\n"
    "  - \"maguinada\" may actually be \"magoei nada\" / \"não me magoei nada\" (I'm not hurt at all)\n"
    "  - \"quieta\" or \"queria\" may actually be \"queda\" (fall)\n"
    "  - \"boi\" or \"doi\" may actually be \"dói\" (it hurts)\n"
    "  - \"mandei\" may actually be \"magoei\" (I hurt myself)\n"
    "  - \"ajude\" or \"a juda\" may actually be \"ajuda\" (help)\n"
    "* A misrecognition you reconstruct this way may be acted on to ESCALATE (a reconstructed \"caí\" is "
    "a fall). It must NEVER be the reason you conclude the senior is fine: if the reconstruction would "
    "mean they are fine (\"Não QI\" → \"não caí\"), say back what you think you heard and ask them to "
    "confirm before closing — in Portuguese, e.g. \"Desculpe, disse que não caiu?\".\n")


# --- v2: fixes from the first gpt-4o run (experiments/ks833/v1_male, v1_female) ------------------

# v1 said a reconstructed "caí" MAY escalate; gpt-4o asked again instead ("QI na cozinha"), and after
# a second "TI" told the senior "pode ter sido um erro na transcrição". v2 makes escalation mandatory
# and keeps recognition talk away from the senior.
V1_RECONSTRUCT = ("* A misrecognition you reconstruct this way may be acted on to ESCALATE (a reconstructed \"caí\" is "
                  "a fall).")
V2_RECONSTRUCT = ("* A reconstructed \"caí\" (I fell), \"dói\" (it hurts) or \"ajuda\" (help) counts as the senior "
                  "SAYING it: escalate immediately with 'distress_fall_confirmed' — do not ask them to repeat it. "
                  "Never mention transcription, recognition, the system or a \"mistake\" to the senior; they only "
                  "know they are talking to you.\n"
                  "* A misrecognition you reconstruct this way may be acted on to ESCALATE (a reconstructed \"caí\" is "
                  "a fall).")

# v1: "alguém irá ajudá-lo em breve" in 4/29 male runs, "Vou enviar um alerta" instead of the
# mandated phrase. The prohibition existed only in English; v2 restates both in Portuguese terms.
CLOSING_ANCHOR = ("    - Bad: \"Just to confirm, did you say you fell?\" paired with a fall-confirmed outcome — the "
                  "senior is asked a question and the call ends before they can answer.\n")
CLOSING_PT = (
    "    - In Portuguese, the mandated phrases are said EXACTLY as given — \"Estou a enviar um alerta no "
    "sistema SeniorMatics.\" (not \"Vou enviar…\") and \"Não consegui falar consigo, por isso estou a avisar "
    "os seus cuidadores.\"\n"
    "    - In Portuguese, NEVER promise that help is coming: no \"alguém vai/irá ajudá-lo\", \"em breve\", "
    "\"a ajuda está a caminho\", \"já vem alguém\". The alert is raised; nothing guarantees anyone has seen it.\n")


# --- v3: the two wrong clears in experiments/ks833/v2_male ---------------------------------------
# 1. "Na na" was reconstructed as "não", then a second "Na na" to "are you hurt?" closed the call as
#    fine — a guessed word cleared a senior, which the reconstruction rule already forbids.
# 2. An off-topic senior was asked a LEADING question ("está a dizer que está tudo bem e que não
#    precisa de ajuda?") and "Pois, era o que eu dizia" was taken as confirmation.
# The fine path therefore needs the senior's OWN words; a bare yes/no or a guessed word never clears.
VALIDATION_ANCHOR = ("    - A senior who has just fallen very often says they are fine at first — embarrassed, dazed, "
                     "or not wanting to be a bother. Always check once more.\n")
VALIDATION_PT = (
    "    - In Portuguese, closing as fine requires the senior to have said it IN THEIR OWN WORDS — e.g. "
    "\"estou bem\", \"não caí\", \"não me magoei\", \"está tudo bem\". None of these is enough on its own: "
    "a bare \"sim\", \"pois\", \"é\", \"não\" or \"nã\"; an answer to a question that suggested they were fine; "
    "or a word you reconstructed from a misrecognition (\"Na na\", \"Não QI\"). In those cases ask an OPEN "
    "question (\"Como é que o senhor está?\"), never a leading one (\"Está a dizer que está tudo bem?\"); "
    "if you still do not get a clear answer in their own words, treat it as a fall.\n")


# --- v4: v3 still cleared "Na na" twice (3/4 runs, experiments/ks833/v3_*) ------------------------
# VEGA confirmed the guess with the v1 example "Desculpe, disse que não caiu?" — itself a leading
# question — and the second unclear "Na na" was read as "yes, I didn't fall". The "Na na" -> "nã"
# mapping pointed it there. v4 drops that mapping and makes the confirmation an open question.
NA_NA_LINE = "  - \"Na\" or \"Na na\" may actually be \"nã\" / \"não\" (no, Azorean)\n"
V3_CONFIRM = ("say back what you think you heard and ask them to confirm before closing — in Portuguese, "
              "e.g. \"Desculpe, disse que não caiu?\".\n")
V4_CONFIRM = ("do not suggest the answer back to them — ask an OPEN question in Portuguese, e.g. "
              "\"Desculpe, não percebi. Como é que o senhor está?\", and close as fine only on a clear answer "
              "in their own words.\n"
              "* A short unclear answer (\"Na na\", \"Hã\", a single garbled word) stays unclear even if it is "
              "repeated after your question — it is never a confirmation. Two unclear answers in a row are a "
              "fall ('distress_fall_confirmed').\n")


# --- v5: gender-neutral Portuguese (decided at the daily, 2026-10-09) -----------------------------
# v4 says "o senhor" / "a senhora" and agrees adjectives with seniorGender; the base prompt defaults to
# male when the gender is missing, so a woman could be called "o senhor". v5 never genders the senior:
# no senhor/senhora/Dona, the first name on its own, and verbs instead of gendered adjectives.
ADDRESS_GENDERED = " as \"o senhor\" / \"a senhora\" (or by name)"
GENDER_NEUTRAL_PT = (
    "* Portuguese gender — ALWAYS GENDER-NEUTRAL: in Portuguese, ignore the senior's gender (and the "
    "'default to male' rule above), even when it is provided. Never say \"o senhor\", \"a senhora\", "
    "\"senhor\", \"senhora\" or \"Dona\"; use the senior's first name on its own, or no name. Never use a "
    "gendered adjective or participle about the senior (magoado/a, sozinho/a, cansado/a, caído/a, "
    "tranquilo/a, descansado/a, assustado/a) or a gendered pronoun (ajudá-lo/la, ouvi-lo/la): say it with "
    "a verb or \"consigo\" instead — \"Magoou-se?\", \"Tem dores?\", \"Está alguém consigo?\", "
    "\"Consegue levantar-se?\", \"Consegue ouvir-me?\", \"Fique com calma\", \"Estou aqui consigo\". "
    "Your own words about yourself stay feminine (obrigada, preocupada).\n")
OPEN_Q_GENDERED = "Como é que o senhor está?"
OPEN_Q_NEUTRAL = "Como é que se sente?"


def replace_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{what}: anchor found {n} times (expected 1) — base prompt changed?")
    return text.replace(old, new)


def build_asis(base):
    return replace_once(base, LANG_EN, LANG_PT, "language line")


def build_v1(base, info):
    p = build_asis(base)
    p = replace_once(p, INFO_EN, info, "additional information")
    p = replace_once(p, ALERT_EN, ALERT_PT, "alert phrase")
    p = replace_once(p, NORESP_EN, NORESP_PT, "no-response phrase")
    p = replace_once(p, OPENING_ANCHOR, OPENING_ANCHOR + OPENING_PT, "opening example")
    p = replace_once(p, LANG_PT, LANG_PT + LANGUAGE_PT, "language register")
    p = replace_once(p, ROLE_ANCHOR, ROLE_ANCHOR + ROLE_PT, "role")
    p = replace_once(p, ASR_ANCHOR, ASR_ANCHOR + ASR_PT, "asr guidance")
    p = replace_once(p, GENDER_ANCHOR, GENDER_ANCHOR + GENDER_PT, "gender")
    p = replace_once(p, TTS_ANCHOR, TTS_ANCHOR + TTS_PT, "tts")
    p = replace_once(p, SCENARIO_ASR_ANCHOR, SCENARIO_ASR_ANCHOR + SCENARIO_ASR_PT, "scenario asr")
    return p


def build_v2(base, info):
    p = build_v1(base, info)
    p = replace_once(p, V1_RECONSTRUCT, V2_RECONSTRUCT, "reconstruction rule")
    p = replace_once(p, CLOSING_ANCHOR, CLOSING_ANCHOR + CLOSING_PT, "closing rules")
    return p


def build_v3(base, info):
    p = build_v2(base, info)
    p = replace_once(p, VALIDATION_ANCHOR, VALIDATION_ANCHOR + VALIDATION_PT, "own-words rule")
    return p


def build_v4(base, info):
    p = build_v3(base, info)
    p = replace_once(p, NA_NA_LINE, "", "Na na mapping")
    p = replace_once(p, V3_CONFIRM, V4_CONFIRM, "open confirmation")
    return p


def build_v5(base, info, first_name):
    p = build_v4(base, info)
    p = replace_once(p, ADDRESS_GENDERED, "", "gendered address")
    p = replace_once(p, GENDER_PT, GENDER_NEUTRAL_PT, "gender-neutral rule")
    p = replace_once(p, "Olá, senhor Manuel", f"Olá, {first_name}", "neutral opening")
    if p.count(OPEN_Q_GENDERED) != 2:
        raise SystemExit("open question: expected 2 occurrences — v3/v4 text changed?")
    return p.replace(OPEN_Q_GENDERED, OPEN_Q_NEUTRAL)


def language_line(code):
    return LANG_EN.replace(" en.", f" {code}.")


def render_fall_prompt(base, pack, info, first_name):
    """The fall prompt for any language, from the English base and a language pack.

    No language checks: each slot takes the pack's text at the point where the Java places its
    Hebrew branch (see language_packs.py). This is the shape the Java port follows.
    """
    p = replace_once(base, LANG_EN, language_line(pack.code()) + pack.language_register(), "language line")
    p = replace_once(p, INFO_EN, info, "additional information")
    p = replace_once(p, ALERT_EN, pack.alert_phrase(), "alert phrase")
    p = replace_once(p, NORESP_EN, pack.no_response_phrase(), "no-response phrase")
    p = replace_once(p, OPENING_ANCHOR, OPENING_ANCHOR + pack.opening_example(first_name), "opening example")
    p = replace_once(p, ROLE_ANCHOR, ROLE_ANCHOR + pack.role_intro(), "role")
    p = replace_once(p, ASR_ANCHOR, ASR_ANCHOR + pack.asr_guidance(), "asr guidance")
    p = replace_once(p, GENDER_ANCHOR, GENDER_ANCHOR + pack.gender_rules(), "gender")
    p = replace_once(p, TTS_ANCHOR, TTS_ANCHOR + pack.tts_rules(), "tts")
    p = replace_once(p, SCENARIO_ASR_ANCHOR, SCENARIO_ASR_ANCHOR + pack.misheard_words(), "scenario asr")
    p = replace_once(p, CLOSING_ANCHOR, CLOSING_ANCHOR + pack.closing_rules(), "closing rules")
    p = replace_once(p, VALIDATION_ANCHOR, VALIDATION_ANCHOR + pack.own_words_rule(), "own-words rule")
    return p


def main():
    base = BASE.read_text(encoding="utf-8")
    asis = replace_once(build_asis(base), INFO_EN, INFO_PT_MALE, "additional information")
    outputs = {
        "prompt_ks833_ptpt_asis.txt": asis,
        "prompt_ks833_ptpt_v1_male.txt": build_v1(base, INFO_PT_MALE),
        "prompt_ks833_ptpt_v1_female.txt": build_v1(base, INFO_PT_FEMALE).replace(
            "Olá, senhor Manuel", "Olá, senhora Maria"),
        "prompt_ks833_ptpt_v2_male.txt": build_v2(base, INFO_PT_MALE),
        "prompt_ks833_ptpt_v2_female.txt": build_v2(base, INFO_PT_FEMALE).replace(
            "Olá, senhor Manuel", "Olá, senhora Maria"),
        "prompt_ks833_ptpt_v3_male.txt": build_v3(base, INFO_PT_MALE),
        "prompt_ks833_ptpt_v3_female.txt": build_v3(base, INFO_PT_FEMALE).replace(
            "Olá, senhor Manuel", "Olá, senhora Maria").replace(
            "Como é que o senhor está?", "Como é que a senhora está?"),
        "prompt_ks833_ptpt_v4_male.txt": build_v4(base, INFO_PT_MALE),
        "prompt_ks833_ptpt_v4_female.txt": build_v4(base, INFO_PT_FEMALE).replace(
            "Olá, senhor Manuel", "Olá, senhora Maria").replace(
            "Como é que o senhor está?", "Como é que a senhora está?"),
        # Same text apart from the name and the gender field: the gender must not change anything.
        "prompt_ks833_ptpt_v5_male.txt": build_v5(base, INFO_PT_MALE, "Manuel"),
        "prompt_ks833_ptpt_v5_female.txt": build_v5(base, INFO_PT_FEMALE, "Maria"),
    }
    # The language-pack render must reproduce the evaluated v5 prompt exactly.
    pt = resolve_language_pack("pt-PT")
    for name, info, first_name in (("prompt_ks833_ptpt_v5_male.txt", INFO_PT_MALE, "Manuel"),
                                   ("prompt_ks833_ptpt_v5_female.txt", INFO_PT_FEMALE, "Maria")):
        if render_fall_prompt(base, pt, info, first_name) != outputs[name]:
            raise SystemExit(f"{name}: language-pack render differs from v5")
    for name, text in outputs.items():
        (PROMPTS / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {name} ({len(text)} chars)")


if __name__ == "__main__":
    main()
