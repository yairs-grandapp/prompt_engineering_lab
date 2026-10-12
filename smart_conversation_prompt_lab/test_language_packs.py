#!/usr/bin/env python3
"""
KS-833: tests for the language packs and the language-code registry.

    python -m unittest test_language_packs -v
"""
import unittest

import build_ks833_prompts as b
from language_packs import (ConversationLanguagePack, EnglishPack, HebrewPack, LANGUAGE_PACKS,
                            PortuguesePack, resolve_language_pack)

BASE = b.BASE.read_text(encoding="utf-8")


def render(code, info=b.INFO_PT_MALE, first_name="Manuel"):
    return b.render_fall_prompt(BASE, resolve_language_pack(code), info, first_name)


class RegistryTest(unittest.TestCase):
    def test_every_form_of_a_code_resolves_to_its_language(self):
        cases = {
            PortuguesePack: ["pt", "pt-PT", "pt_PT", "PT-pt", "pt-pt", " pt-PT ", "pt-BR"],
            HebrewPack: ["he", "he-IL", "HE_il"],
            EnglishPack: ["en", "en-US", "EN-gb"],
        }
        for pack, codes in cases.items():
            for code in codes:
                with self.subTest(code=code):
                    self.assertIsInstance(resolve_language_pack(code), pack)

    def test_unknown_or_missing_codes_get_english(self):
        for code in ["zh-CN", "es-IL", "", None, "-"]:
            with self.subTest(code=code):
                self.assertIsInstance(resolve_language_pack(code), EnglishPack)

    def test_every_registered_pack_renders(self):
        for key in LANGUAGE_PACKS:
            with self.subTest(language=key):
                self.assertIn(resolve_language_pack(key).alert_phrase(), render(key))

    def test_a_pack_missing_a_piece_cannot_be_created(self):
        class IncompletePack(ConversationLanguagePack):
            def code(self):
                return "zh-CN"
        with self.assertRaises(TypeError):
            IncompletePack()


class PortugueseParityTest(unittest.TestCase):
    """The pack must reproduce the evaluated v5 prompt, whatever form the code arrives in."""

    def test_render_matches_v5_files(self):
        for code in ["pt", "pt-PT", "pt_PT", "PT-pt"]:
            for info, name, gender in ((b.INFO_PT_MALE, "Manuel", "male"), (b.INFO_PT_FEMALE, "Maria", "female")):
                with self.subTest(code=code, gender=gender):
                    expected = (b.PROMPTS / f"prompt_ks833_ptpt_v5_{gender}.txt").read_text(encoding="utf-8")
                    self.assertEqual(render(code, info, name), expected)

    def test_no_gendered_address_of_the_senior(self):
        prompt = render("pt-PT")
        for gendered in ["o senhor está", "a senhora está", "Olá, senhor", "Olá, senhora"]:
            self.assertNotIn(gendered, prompt)

    def test_mandated_phrases_and_no_english_ones(self):
        prompt = render("pt-PT")
        self.assertIn(PortuguesePack().alert_phrase(), prompt)
        self.assertIn(PortuguesePack().no_response_phrase(), prompt)
        self.assertNotIn(EnglishPack().alert_phrase(), prompt)
        self.assertNotIn(EnglishPack().no_response_phrase(), prompt)


class EnglishAndHebrewTest(unittest.TestCase):
    def test_english_render_is_the_base_with_the_language_code(self):
        expected = BASE.replace(b.LANG_EN, b.language_line("en-US")).replace(b.INFO_EN, b.INFO_PT_MALE)
        self.assertEqual(render("en-US"), expected)

    def test_hebrew_render_adds_each_hebrew_branch_once(self):
        prompt = render("he-IL")
        pack = HebrewPack()
        for text in [pack.language_register(), pack.role_intro(), pack.asr_guidance(),
                     pack.gender_rules(), pack.tts_rules(), pack.alert_phrase(), pack.no_response_phrase()]:
            with self.subTest(text=text[:40]):
                self.assertEqual(prompt.count(text), 1)
        self.assertIn("The current spoken language is he-IL.", prompt)


class BoostPhrasesTest(unittest.TestCase):
    def test_portuguese_list_is_boost_v2(self):
        phrases = PortuguesePack().asr_boost_phrases()
        self.assertEqual(len(phrases), 28)
        self.assertEqual(len(set(phrases)), 28)
        for word in ["caí", "queda", "dói", "ajuda", "socorro", "estou bem", "nã", "pois"]:
            self.assertIn(word, phrases)


if __name__ == "__main__":
    unittest.main()
