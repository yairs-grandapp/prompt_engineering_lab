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

Usage:
    python build_ks833_prompts.py
"""
from pathlib import Path

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


def main():
    base = BASE.read_text(encoding="utf-8")
    asis = replace_once(build_asis(base), INFO_EN, INFO_PT_MALE, "additional information")
    outputs = {
        "prompt_ks833_ptpt_asis.txt": asis,
        "prompt_ks833_ptpt_v1_male.txt": build_v1(base, INFO_PT_MALE),
        "prompt_ks833_ptpt_v1_female.txt": build_v1(base, INFO_PT_FEMALE).replace(
            "Olá, senhor Manuel", "Olá, senhora Maria"),
    }
    for name, text in outputs.items():
        (PROMPTS / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {name} ({len(text)} chars)")


if __name__ == "__main__":
    main()
