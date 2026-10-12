#!/usr/bin/env python3
"""
KS-833: one class per conversation language — the lab version of the design approved in the
KS-833 technical requirements, so the Java port is a transcription of this file.

Every piece of fall-check prompt text that depends on the language lives in a language pack.
The prompt code (render_fall_prompt) never checks the language: it asks the pack. Adding a
language is one new pack class plus one line in LANGUAGE_PACKS; because the methods are
abstract, a pack that leaves a piece out cannot be instantiated.

Slots mirror the Java branch points (ContextBase / ContextDistressFallDetected). Insertion
texts are placed exactly where the Java places its Hebrew branch text, so rendering the
English base prompt with a pack reproduces what the Java would send for that language.

Language codes: the Monitor can save "pt" (the phone's language) or "pt-PT" (the dictionary
server list), and other spellings are possible, so the registry matches on the language part
only, ignoring case, region and separator. Any unknown code gets English, as production does
today.
"""
import re
from abc import ABC, abstractmethod


class ConversationLanguagePack(ABC):
    """Language-specific text for the fall-check prompt. One subclass per language."""

    @abstractmethod
    def code(self):
        """Canonical BCP-47 code, written into the prompt's language line ("pt-PT")."""

    @abstractmethod
    def language_register(self):
        """ContextBase.languageGuidelines: appended to the language line."""

    @abstractmethod
    def role_intro(self):
        """ContextBase.roleGuidelines: line after the 'introduce yourself by name' bullet."""

    @abstractmethod
    def asr_guidance(self):
        """ContextBase.asrGuidelines: block after the generic misrecognition rule."""

    @abstractmethod
    def gender_rules(self):
        """ContextBase.genderGuidelines: block after the generic gender bullets."""

    @abstractmethod
    def tts_rules(self):
        """ContextBase.ttsGuidelines: bullets after the generic TTS bullets."""

    @abstractmethod
    def opening_example(self, first_name):
        """ContextDistressFallDetected: extra example after the 'Opening message' examples."""

    @abstractmethod
    def alert_phrase(self):
        """ContextDistressFallDetected: mandated phrase for distress_fall_confirmed."""

    @abstractmethod
    def no_response_phrase(self):
        """ContextDistressFallDetected: mandated phrase for no_response_from_resident."""

    @abstractmethod
    def closing_rules(self):
        """ContextDistressFallDetected: bullets after the closing Good/Bad examples."""

    @abstractmethod
    def own_words_rule(self):
        """ContextDistressFallDetected: bullet after 'a senior who has just fallen ... check once more'."""

    @abstractmethod
    def misheard_words(self):
        """ContextDistressFallDetected.getScenarioAsrGuidelines: block after the English list."""

    @abstractmethod
    def asr_boost_phrases(self):
        """ContextDistressFallDetected.getAsrBoostPhrases (used by KS-834, not in the prompt)."""


class EnglishPack(ConversationLanguagePack):
    def code(self):
        return "en-US"

    def language_register(self):
        return ""

    def role_intro(self):
        return ""

    def asr_guidance(self):
        return ""

    def gender_rules(self):
        return ""

    def tts_rules(self):
        return ""

    def opening_example(self, first_name):
        return ""

    def alert_phrase(self):
        return "\"I'm raising an alert in the SeniorMatics system.\""

    def no_response_phrase(self):
        return "\"I could not reach you, so I am notifying your caregivers now.\""

    def closing_rules(self):
        return ""

    def own_words_rule(self):
        return ""

    def misheard_words(self):
        return ""

    def asr_boost_phrases(self):
        return ["fell", "fallen", "fall",
                "hurts", "pain", "help",
                "bleeding", "broken",
                "dizzy", "fine", "okay"]


class HebrewPack(ConversationLanguagePack):
    """Transcribed from the isHebrew() branches of ContextBase and ContextDistressFallDetected."""

    def code(self):
        return "he-IL"

    def language_register(self):
        return (" Write in spoken, conversational Hebrew (שפה מדוברת) — not formal or literary register."
                " Spell out acronyms in full (e.g., \"בית חולים\" not \"ביה״ח\")."
                " Transliterate foreign names into Hebrew letters.")

    def role_intro(self):
        return "    - In Hebrew, introduce yourself as \"כאן וגה\" (not \"זה וגה\" which is masculine).\n"

    def asr_guidance(self):
        return ("* HEBREW ASR GUIDANCE — Hebrew speech recognition is often fragmented or garbled. Apply these rules:\n"
                "    - The transcription may contain nonsense syllables, broken words, or only partial recognition. "
                "Do NOT dismiss the response — scan for ANY recognizable Hebrew word or root.\n"
                "    - If you find a meaningful word embedded in noise (e.g., \"נפל\" (fell) inside \"נפל נקש םלמ\"), "
                "treat it as a real signal. State what you think you heard and act on it.\n"
                "    - Hebrew words that sound similar should be considered as possible misrecognitions of contextually relevant words. "
                "For example in a fall scenario: \"נפח\" (swelled), \"נפש\" (soul), \"כפל\" (doubled) may be misrecognitions of \"נפל\" (fell). "
                "\"כואב\" (hurts) may appear as \"כועס\" (angry). \"עזרה\" (help) may appear as \"עזרא\" or \"אזרה\".\n"
                "    - When the transcription is mostly unintelligible but contains even one safety-critical word "
                "(fall, pain, help, not okay), escalate — do not ask for clarification.\n"
                "    - Elderly Hebrew speakers may mix formal and informal registers, use Yiddish-origin words, "
                "or speak with accents that further degrade ASR accuracy. Be generous in interpretation.\n")

    def gender_rules(self):
        return ("* Hebrew gender — CRITICAL RULES:\n"
                "    - You (Vega) are ALWAYS female: use בודקת, שמחה, רוצה, רציתי (not בודק, שמח, רוצה, רצתי).\n"
                "    - The SENIOR's gender determines how you address THEM. Default to male.\n"
                "    - Add nikud ONLY to gender-specific words where male/female spelling is identical but pronunciation differs:\n"
                "      Senior male (default): נפלתָ, חווִיתָ, הלכתָ, שֶׁלְּךָ\n"
                "      Senior female: נפלתְ, חווִיתְ, הלכתְ, שֶׁלָּךְ\n")

    def tts_rules(self):
        return ("    - Do NOT add nikud to regular Hebrew words — nikud degrades TTS pronunciation. Only add nikud to "
                "gender-specific words where male/female forms differ (see gender guidelines).\n"
                "    - Write in spoken conversational style. Spell out numbers and abbreviations in Hebrew words.\n")

    def opening_example(self, first_name):
        return ""  # the Hebrew example is part of the shared text in production

    def alert_phrase(self):
        return "\"אני מעבירה התראה במערכת סניורמטיקס.\""

    def no_response_phrase(self):
        return "\"לא הצלחתי ליצור איתך קשר, אני מעדכנת את המטפלים שלך.\""

    def closing_rules(self):
        return ""

    def own_words_rule(self):
        return ""

    def misheard_words(self):
        return ""

    def asr_boost_phrases(self):
        return ["נפלתי", "נפל", "נפלה",
                "כואב", "כואב לי",
                "עזרה",
                "לא בסדר",
                "הראש", "הרגל", "היד",
                "דם", "שבור",
                "סחרחורת",
                "בסדר", "הכל בסדר",
                "לא נפלתי",
                "בסדר גמור"]


class PortuguesePack(ConversationLanguagePack):
    """European Portuguese, prompt v5 (gender-neutral). Evaluated in experiments/ks833/v5_*."""

    def code(self):
        return "pt-PT"

    def language_register(self):
        return (" Write ONLY in European Portuguese, as spoken in Portugal (português europeu) — NEVER Brazilian Portuguese."
                " Use European vocabulary, spelling and grammar: \"estou a ouvir\" (not \"estou ouvindo\"),"
                " \"casa de banho\", \"telemóvel\", \"Detetámos\"."
                " Address the senior formally and warmly with third-person verbs"
                " (\"Está bem?\", \"Consegue levantar-se?\") — never \"tu\" and never Brazilian \"você\"."
                " Keep it simple and clear: the senior is elderly and may speak with an Azorean accent."
                " Every example phrase in these guidelines is given in English or Hebrew only to illustrate"
                " the meaning — always say it in European Portuguese, never in English.")

    def role_intro(self):
        return ("    - In European Portuguese, introduce yourself as \"fala a Vega\" or \"é a Vega\", and use "
                "feminine forms for yourself (obrigada, preocupada, contente).\n")

    def asr_guidance(self):
        return ("* PORTUGUESE ASR GUIDANCE — the senior speaks European Portuguese, often with a strong Azorean "
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

    def gender_rules(self):
        return ("* Portuguese gender — ALWAYS GENDER-NEUTRAL: in Portuguese, ignore the senior's gender (and the "
                "'default to male' rule above), even when it is provided. Never say \"o senhor\", \"a senhora\", "
                "\"senhor\", \"senhora\" or \"Dona\"; use the senior's first name on its own, or no name. Never use a "
                "gendered adjective or participle about the senior (magoado/a, sozinho/a, cansado/a, caído/a, "
                "tranquilo/a, descansado/a, assustado/a) or a gendered pronoun (ajudá-lo/la, ouvi-lo/la): say it with "
                "a verb or \"consigo\" instead — \"Magoou-se?\", \"Tem dores?\", \"Está alguém consigo?\", "
                "\"Consegue levantar-se?\", \"Consegue ouvir-me?\", \"Fique com calma\", \"Estou aqui consigo\". "
                "Your own words about yourself stay feminine (obrigada, preocupada).\n")

    def tts_rules(self):
        return ("    - Spell out numbers, times and abbreviations in Portuguese words (\"três vezes por dia\", "
                "\"senhor doutor\"). The contraction examples above are English: in Portuguese, just write "
                "natural spoken European Portuguese.\n")

    def opening_example(self, first_name):
        return (f' Example (European Portuguese): "Olá, {first_name}, fala a Vega. '
                'Detetámos uma possível queda. Está bem?"')

    def alert_phrase(self):
        return "\"Estou a enviar um alerta no sistema SeniorMatics.\""

    def no_response_phrase(self):
        return "\"Não consegui falar consigo, por isso estou a avisar os seus cuidadores.\""

    def closing_rules(self):
        return ("    - In Portuguese, the mandated phrases are said EXACTLY as given — \"Estou a enviar um alerta no "
                "sistema SeniorMatics.\" (not \"Vou enviar…\") and \"Não consegui falar consigo, por isso estou a avisar "
                "os seus cuidadores.\"\n"
                "    - In Portuguese, NEVER promise that help is coming: no \"alguém vai/irá ajudá-lo\", \"em breve\", "
                "\"a ajuda está a caminho\", \"já vem alguém\". The alert is raised; nothing guarantees anyone has seen it.\n")

    def own_words_rule(self):
        return ("    - In Portuguese, closing as fine requires the senior to have said it IN THEIR OWN WORDS — e.g. "
                "\"estou bem\", \"não caí\", \"não me magoei\", \"está tudo bem\". None of these is enough on its own: "
                "a bare \"sim\", \"pois\", \"é\", \"não\" or \"nã\"; an answer to a question that suggested they were fine; "
                "or a word you reconstructed from a misrecognition (\"Na na\", \"Não QI\"). In those cases ask an OPEN "
                "question (\"Como é que se sente?\"), never a leading one (\"Está a dizer que está tudo bem?\"); "
                "if you still do not get a clear answer in their own words, treat it as a fall.\n")

    def misheard_words(self):
        # caí / magoei forms measured on Azure pt-PT at 8 kHz in the KS-834 lab (asr_ptpt_lab).
        return ("* In Portuguese, the following are commonly misrecognized and may be fall-related words:\n"
                "  - \"QI\", \"TI\", \"Ei TI\", \"K í\", \"Kí\", \"ki\", \"cai\", \"aí\" or \"saí\" may actually be \"caí\" (I fell) — "
                "e.g. \"QI na cozinha\" → \"caí na cozinha\", \"Não QI\" → \"não caí\"\n"
                "  - \"maguinada\" may actually be \"magoei nada\" / \"não me magoei nada\" (I'm not hurt at all)\n"
                "  - \"quieta\" or \"queria\" may actually be \"queda\" (fall)\n"
                "  - \"boi\" or \"doi\" may actually be \"dói\" (it hurts)\n"
                "  - \"mandei\" may actually be \"magoei\" (I hurt myself)\n"
                "  - \"ajude\" or \"a juda\" may actually be \"ajuda\" (help)\n"
                "* A reconstructed \"caí\" (I fell), \"dói\" (it hurts) or \"ajuda\" (help) counts as the senior "
                "SAYING it: escalate immediately with 'distress_fall_confirmed' — do not ask them to repeat it. "
                "Never mention transcription, recognition, the system or a \"mistake\" to the senior; they only "
                "know they are talking to you.\n"
                "* A misrecognition you reconstruct this way may be acted on to ESCALATE (a reconstructed \"caí\" is "
                "a fall). It must NEVER be the reason you conclude the senior is fine: if the reconstruction would "
                "mean they are fine (\"Não QI\" → \"não caí\"), do not suggest the answer back to them — ask an OPEN "
                "question in Portuguese, e.g. \"Desculpe, não percebi. Como é que se sente?\", and close as fine only "
                "on a clear answer in their own words.\n"
                "* A short unclear answer (\"Na na\", \"Hã\", a single garbled word) stays unclear even if it is "
                "repeated after your question — it is never a confirmation. Two unclear answers in a row are a "
                "fall ('distress_fall_confirmed').\n")

    def asr_boost_phrases(self):
        # KS-834 boost_v2 (asr_ptpt_lab/data/boost/boost_v2.txt), weight 1.5.
        return ["caí", "eu caí", "já caí", "caí no chão", "não caí",
                "queda", "dói", "dói-me", "dores",
                "magoei", "magoei-me", "não me magoei",
                "ajuda", "preciso de ajuda", "socorro",
                "não estou bem", "estou bem", "tou bem", "está tudo bem",
                "levantar", "não consigo levantar",
                "sangue", "partido", "tonturas",
                "sim", "não", "nã", "pois"]


# --- Registry ---------------------------------------------------------------------------------

LANGUAGE_PACKS = {
    "en": EnglishPack,
    "he": HebrewPack,
    "pt": PortuguesePack,
}
DEFAULT_LANGUAGE = "en"


def language_part(code):
    """'pt-PT', 'pt_pt', ' PT ', 'pt' -> 'pt'. Empty or missing -> ''."""
    return re.split(r"[-_]", (code or "").strip(), maxsplit=1)[0].lower()


def resolve_language_pack(code):
    """The pack for any form of a language code; unknown or empty codes get English."""
    return LANGUAGE_PACKS.get(language_part(code), LANGUAGE_PACKS[DEFAULT_LANGUAGE])()
