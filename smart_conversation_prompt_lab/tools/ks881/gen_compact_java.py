# -*- coding: utf-8 -*-
"""KS-881: writes the server's compact fall-prompt classes (EnglishCompactFallPrompt, PortugueseCompactFallPrompt,
HebrewCompactFallPrompt) from the lab prompts that passed the tests (data/prompts/prompt_ks881_<label>_<lang>[_unknown]),
so the text the server sends is exactly the tested text. Java 8: string concatenation, one line per source line.

Usage: python tools/ks881/gen_compact_java.py <label> [<repo>]
"""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
label = sys.argv[1]
repo = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "Desktop" / "grandappflutter"
OUT = repo / "picmeinserver/DddSmartConversation/src/com/ddd/services/smartconversation/context/language"
CLASSES = {"en": "EnglishCompactFallPrompt", "pt": "PortugueseCompactFallPrompt", "he": "HebrewCompactFallPrompt"}


def java_string(text):
    lines = text.split("\n")
    parts = []
    for i, line in enumerate(lines):
        esc = line.replace("\\", "\\\\").replace("\"", "\\\"")
        parts.append("\"" + esc + ("\\n" if i < len(lines) - 1 else "") + "\"")
    return "\n\t\t\t+ ".join(parts)


for lang, cls in CLASSES.items():
    named = (LAB / "data/prompts" / f"prompt_ks881_{label}_{lang}.txt").read_text(encoding="utf-8").split("@@SPLIT@@")[0]
    unknown = (LAB / "data/prompts" / f"prompt_ks881_{label}_{lang}_unknown.txt").read_text(encoding="utf-8").split("@@SPLIT@@")[0]
    src = f"""package com.ddd.services.smartconversation.context.language;

/**
 * KS-881 (Yair, 2026-11-03: "minimize the prompt"; the compact prompt family, gpt-6-sol (chosen 2026-11-04) and gpt-6.1-terra): the compact fall-call
 * instructions, {lang}. GENERATED from the lab prompt {label} (KS-881 test sets)
 * (prompt_engineering_lab tools/ks881/gen_compact_java.py): edit the lab text and regenerate, do not edit here.
 * The call's details, the KS-876 farewell line and the history are added after these instructions by
 * ContextDistressFallDetected.buildPromptParts, exactly as for the full prompt.
 */
public final class {cls} extends CompactFallPrompt {{

	private static final String NAMED = {java_string(named.strip())};

	private static final String UNKNOWN = {java_string(unknown.strip())};

	@Override
	public String instructions(boolean identityUnknown) {{
		return identityUnknown ? UNKNOWN : NAMED;
	}}
}}
"""
    (OUT / f"{cls}.java").write_text(src, encoding="utf-8")
    print("wrote", cls)
