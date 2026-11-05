# -*- coding: utf-8 -*-
"""KS-881 realistic test set (Yair with Alon and Tony, 2026-11-03): about 500 conversations of what is likely
to happen on a fall call, 1-5 senior answers each, with the rare, tricky cases ("so-so", "I fell last year") left
to the separate tricky set (inputs_ks881_<lang>.json).

Each conversation is a PATH (a sequence of answer kinds) filled with phrases from the banks below. The expected
outcome and the answer it closes on are computed by the same state machine as reports/KS-881/dev/loopcheck.js
(the v7 rules, 5-message limit), so every expectation follows the agreed rules. Every phrase means the same
whatever Vega asked (no bare "yes"/"no": the 3 Nov run showed "I think so" flips meaning with the question).

Usage: python tools/ks881/build_realistic.py  ->  data/inputs/inputs_ks881_realistic_en.json
"""
import json
import random
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
SEED = 881
TARGET = 480

FELL, HELP_O, UNABLE, NONE, FINE_O = ("distress_fall_confirmed", "distress_assistance_requested",
                                      "distress_unable_to_verify", "no_response_from_resident", "no_fall_confirmed")
OUT = {"fall": FELL, "assist": HELP_O, "unable": UNABLE, "noresp": NONE, "nofall": FINE_O}

# ---- phrase banks (English). Kind -> state-machine class. ------------------------------------------------
BANK = {
    "F": ("FELL", [  # a clear fall, no help words
        "I fell.", "Yes, I fell.", "I fell in the bathroom.", "I fell down in the kitchen.", "I slipped and fell.",
        "I had a fall.", "I tripped and fell in the hallway.", "I fell out of bed.", "Yes, I fell, but I'm okay.",
        "I'm on the floor.", "I took a tumble in the living room.", "I fell off the chair.",
        "I slipped in the shower and fell.", "Yes, I've fallen.", "I fell on the stairs.",
        "I fell over in the garden.", "I lost my balance and fell.", "I fell getting out of the bath.",
        "I fell next to the bed.", "Yes, I fell, I'm on the floor.", "I fell backwards.", "I went down in the kitchen.",
        "I fell, but I got back up.", "I fell this morning.", "I fell when I stood up.", "I fell by the door.",
        "Yes, I had a fall in the bedroom.", "I fell over the dog.", "I slipped on the rug and fell.",
        "I fell, I'm sitting on the floor now."]),
    "FH": ("FELLHELP", [  # a fall with a help signal in the same answer: the flag must be set
        "I fell and I can't get up.", "I fell, please help me.", "I fell and hurt my hip.",
        "I fell and my arm hurts.", "I've fallen and I need help.", "I fell in the bathroom and my head hurts.",
        "I fell and I can't move my leg.", "Help, I fell down.", "I fell and I'm bleeding.",
        "I fell, call my son please.", "I fell and my wrist hurts a lot.", "I fell and I feel dizzy.",
        "I fell on my back and it hurts.", "I fell and I can't stand up.", "I fell, I need an ambulance.",
        "I fell and hit my head."]),
    # KS-881 (Tony 45602; João/Yair 5 Nov): a misheard fall word is not certain: unable to verify at once.
    "MIS": ("MISHEARD", [  # a fall word misheard by speech recognition (P3)
        "I well down.", "I well in the bathroom.", "I felt down in the kitchen.", "I held down on the floor.",
        "I well off the bed.", "I felt on the floor.", "I well in the kitchen.", "I held on the floor.",
        "I felt in the hallway.", "I well over."]),
    "H": ("HELP", [  # help without a fall
        "I need help.", "Please help me.", "Help.", "My back hurts.", "I hit my head.", "I can't get up.",
        "I feel dizzy.", "I don't feel well.", "Can you call my daughter?", "I hurt my knee.", "It hurts.",
        "I'm in pain.", "I feel very weak.", "My chest hurts.", "I can't breathe well.", "I need someone to come.",
        "My leg hurts.", "I feel sick.", "I hurt my back.", "Please send someone.", "I can't stand up.",
        "My head hurts.", "I'm not feeling good.", "I need a doctor.", "I cut my hand.", "Call an ambulance.",
        "My arm hurts.", "I feel faint."]),
    "FI": ("FINE", [  # a first reassuring answer
        "I'm fine.", "Yes, I'm okay.", "I'm alright, thank you.", "Everything's fine here.", "Yeah, I'm good.",
        "I'm okay, nothing happened.", "Oh, I'm fine, dear.", "I'm doing fine.", "I'm well, thanks.",
        "I'm okay, thanks for checking.", "All good here.", "I'm perfectly fine."]),
    "D": ("DENIAL", [  # a denial
        "I didn't fall.", "No, I didn't fall, I just sat down.", "No fall, I dropped a book.",
        "Nothing fell, it was the cat.", "I didn't fall, don't worry.", "No, I didn't fall, I was just bending down."]),
    "CF": ("FINE", [  # the second reassuring answer, whatever the confirming question was
        "I'm not hurt at all, and I don't need anything.", "Everything is fine, nothing hurts.",
        "I'm really okay, nothing hurts and I'm up and about.", "I'm sure, I'm perfectly fine.",
        "Honestly, nothing is wrong.", "All good, I'm walking around normally.",
        "Nothing hurts, I'm fine, thank you.", "I'm absolutely fine, no pain at all."]),
    "CP": ("HELP", [  # the confirming question reveals a problem
        "Actually, my hip hurts.", "Well, my back hurts a bit.", "Actually, I can't get up.",
        "I feel a bit dizzy, to be honest.", "My wrist hurts.", "Actually, I do need some help.",
        "My knee is hurting.", "Now that you ask, my head hurts."]),
    "CFALL": ("FELL", ["Actually, I did fall.", "Well, I fell in the hallway.", "Actually, I fell a minute ago."]),
    "UNS": ("UNCLEAR", ["I'm not sure.", "I don't know.", "I don't really know.", "I'm not sure what happened."]),
    "U": ("UNCLEAR", ["What?", "Sorry?", "Who is this?", "What did you say?", "Hmm?", "Pardon?",
                      "I can't hear you.", "Hello?"]),
    "HO": ("HOLD", ["Hold on.", "Just a moment.", "Wait a second.", "One moment, please."]),
    "S": ("SILENCE", [""]),
    "YF": ("FELL", ["Yes, I fell.", "Yes, I fell down.", "I did fall, yes."]),  # confirms a misheard fall
}

# ---- paths: (truth, kinds, weight). Truth is what really happened, for the metrics. -----------------------
PATHS = [
    ("fall", ["F"], 40), ("fall", ["FH"], 16), ("fall", ["MIS", "YF"], 16), ("fall", ["U", "F"], 14),
    ("fall", ["S", "F"], 12), ("fall", ["HO", "F"], 8), ("fall", ["HO", "S", "F"], 6), ("fall", ["FI", "CFALL"], 8),
    ("fall", ["UNS", "F"], 8),
    ("help", ["H"], 34), ("help", ["U", "H"], 10), ("help", ["S", "H"], 8), ("help", ["FI", "CP"], 20),
    ("help", ["D", "CP"], 8), ("help", ["UNS", "H"], 8), ("help", ["HO", "H"], 5),
    ("fine", ["FI", "CF"], 60), ("fine", ["D", "CF"], 24), ("fine", ["U", "FI", "CF"], 12),
    ("fine", ["S", "FI", "CF"], 12), ("fine", ["HO", "FI", "CF"], 8), ("fine", ["HO", "S", "FI", "CF"], 8),
    ("fine", ["FI", "UNS", "CF"], 8), ("fine", ["UNS", "FI", "CF"], 8),
    ("unclear", ["U", "U"], 12), ("unclear", ["FI", "S", "S"], 6), ("unclear", ["UNS", "UNS"], 8),
    ("silent", ["S", "S"], 12),
]


# ---- the state machine (a port of loopcheck.js step/rawStep) ---------------------------------------------
def raw_step(v, c):
    n = dict(v)
    if c != "SILENCE":
        n["spoken"] = True

    def count():
        n["counted"] += 1

    st = v["st"]
    if c == "MISHEARD":  # KS-881 (Tony 45602): alert at once, as unable to verify
        count(); return "unable", n
    if st in ("FIRST", "FIRST_AGAIN", "HOLD_FIRST"):
        if st == "HOLD_FIRST" and c == "SILENCE":
            n["st"] = "FIRST_AGAIN"; return None, n
        if c == "HOLD" and not v["holdUsed"] and st == "FIRST":
            n["holdUsed"] = True; n["st"] = "HOLD_FIRST"; return None, n
        count()
        if c in ("FELL", "FELLHELP"): return "fall", n
        if c == "HELP": return "assist", n
        if c in ("FINE", "DENIAL"): n["st"] = "CQ"; return None, n
        n["st"] = "REASK"; return None, n
    if st in ("CQ", "CQ_AGAIN", "HOLD_CQ"):
        if st == "HOLD_CQ" and c == "SILENCE":
            n["st"] = "CQ_AGAIN"; return None, n
        if c == "HOLD" and not v["holdUsed"] and st == "CQ":
            n["holdUsed"] = True; n["st"] = "HOLD_CQ"; return None, n
        count()
        if c in ("FINE", "DENIAL"): return "nofall", n
        if c in ("FELL", "FELLHELP"): return "fall", n
        if c == "HELP": return "assist", n
        n["st"] = "REASK_LATE"; return None, n
    if st == "REASK":
        count()
        if c in ("FELL", "FELLHELP"): return "fall", n
        if c in ("HELP", "SOSO"): return "assist", n
        if c in ("FINE", "DENIAL"): n["st"] = "CQ_LATE"; return None, n
        if c == "SILENCE": return ("unable" if v["spoken"] else "noresp"), n
        return "unable", n
    if st in ("CQ_LATE", "REASK_LATE"):
        count()
        if c in ("FINE", "DENIAL"): return "nofall", n
        if c in ("FELL", "FELLHELP"): return "fall", n
        if c in ("HELP", "SOSO"): return "assist", n
        return "unable", n
    raise ValueError(st)


def run(classes):
    v = {"st": "FIRST", "holdUsed": False, "spoken": False, "counted": 0, "turns": 0}
    for i, c in enumerate(classes, 1):
        end, n = raw_step(v, c)
        n["turns"] = v["turns"] + 1
        if not end and n["counted"] >= 5:  # the 5th answer ends the call; the free wait is not an answer (Tony 45602)
            end = "fall" if c in ("FELL", "FELLHELP") else "assist" if c == "HELP" else (
                "unable" if n["spoken"] else "noresp")
        if end:
            return end, i
        v = n
    raise ValueError(f"path does not end: {classes}")


def main():
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent))
    from realistic_banks import PT, HE, UNKNOWN, UNKNOWN_PATHS
    texts = {"en": {k: v[1] for k, v in BANK.items()}, "pt": PT, "he": HE}
    for lang in ("pt", "he"):
        for k, (_, lst) in BANK.items():
            assert len(texts[lang][k]) == len(lst), f"{lang} {k}: {len(texts[lang][k])} vs {len(lst)}"
    classes_of = {k: v[0] for k, v in BANK.items()}
    for k, (c, by_lang) in UNKNOWN.items():
        classes_of[k] = c
        for lang in ("en", "pt", "he"):
            texts[lang][k] = by_lang[lang]
        assert len({len(v) for v in by_lang.values()}) == 1, k

    rnd = random.Random(SEED)
    total_w = sum(w for _, _, w in PATHS)

    def build(paths, prompt, prefix, share):
        """Index tuples per path, the same draw order as ks881-realistic-1 (rnd.choice == randrange on a list)."""
        out = []
        seen = set()  # one set per prompt kind, as ks881-realistic-1 had for the named paths
        for truth, kinds, w in paths:
            classes = [classes_of[k] for k in kinds]
            end, close = run(classes)
            n = max(1, round(share(w)))
            picks, tries = [], 0
            while len(picks) < n and tries < n * 50:
                tries += 1
                idx = tuple(rnd.randrange(len(texts["en"][k])) for k in kinds)
                key = tuple(texts["en"][k][j] for k, j in zip(kinds, idx))  # as ks881-realistic-1: by English text
                if key in seen:
                    continue
                seen.add(key)
                picks.append(idx)
            distinct = len(picks)
            reps = []
            while len(picks) + len(reps) < n:
                reps.append(picks[len(reps) % distinct])
            out.append((truth, kinds, end, close, prompt, prefix, picks + reps, distinct))
        return out

    named = build(PATHS, "named", "real_", lambda w: TARGET * w / total_w)
    unknown = build(UNKNOWN_PATHS, "unknown", "real_unk_", lambda w: w)

    # Yair, 2026-11-03: "I'm fine" followed by an unsure answer is a tricky case (FR v5: "asks again"); it stays in
    # the tricky set (fine_unsure_then_fine) and leaves this one. Generated first and dropped after, so every other
    # conversation is the same as in ks881-realistic-1.
    MOVED_TO_TRICKY = {"real_fi_uns_cf"}
    for lang in ("en", "pt", "he"):
        scenarios = []
        for truth, kinds, end, close, prompt, prefix, picks, distinct in named + unknown:
            sid = prefix + "_".join(kinds).lower()
            if sid in MOVED_TO_TRICKY:
                continue
            words = []
            for i, idx in enumerate(picks):
                w = {"id": f"w{i + 1}", "turns": [texts[lang][k][j] for k, j in zip(kinds, idx)]}
                if i >= distinct:
                    w["repeat_of"] = f"w{(i - distinct) % distinct + 1}"
                words.append(w)
            s = {"id": sid, "situation": f"{truth}: " + " > ".join(kinds), "truth": truth,
                 "expected_outcome": OUT[end], "close_after": close, "prompt": prompt, "phrasings": words}
            if "MIS" in kinds:
                s["close_after"] = 1  # KS-881 (Tony 45602): a misheard fall is unable to verify at once
            if end == "fall":
                if "FH" in kinds:
                    s["assistance_flag"] = True
                elif "UF" not in kinds:
                    s["no_flag"] = True
            scenarios.append(s)
        out = {"version": "ks881-realistic-3", "language": lang,
               "description": "KS-881 realistic set: likely fall-call conversations (Yair, Alon, Tony 2026-11-03), "
                              "named and unidentified callers; expectations from the v7 state machine with the "
                              "5-message limit. pt and he are the lab's own wordings, for native review.",
               "scenarios": scenarios}
        path = LAB / "data" / "inputs" / f"inputs_ks881_realistic_{lang}.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        n = sum(len(s["phrasings"]) for s in scenarios)
        by = {}
        for s in scenarios:
            key = s["truth"] + ("/unknown" if s["prompt"] == "unknown" else "")
            by[key] = by.get(key, 0) + len(s["phrasings"])
        print(f"{path.name}: {len(scenarios)} paths, {n} conversations; {by}")


if __name__ == "__main__":
    main()
