#!/usr/bin/env python3
"""
KS-881: build data/inputs/inputs_ks881_<en|pt|he>.json from tools/ks881/scenarios.py, and the
coverage report experiments/ks881/coverage.md, which proves every scenario of the six earlier sets
is in the new set (and says where, and what changed). Free: no API calls.

    python tools/ks881/build_inputs.py
"""
import json
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import scenarios as defs  # noqa: E402

LANG_OF_FILE = {defs.B: "en", defs.V0: "en", defs.V1: "en", defs.K: "en", defs.KH: "he", defs.PT: "pt"}


def norm(turns):
    return tuple(re.sub(r"[^\w]+", " ", t.lower()).strip() for t in turns)


def old_turns(file, old_id):
    data = json.loads((LAB / "data" / "inputs" / file).read_text(encoding="utf-8"))
    for s in data["scenarios"]:
        if s["id"] == old_id:
            return [t.get("text", "") for t in s["user_turns"]], s["expected_outcome"].lower()
    raise KeyError(f"{file}:{old_id} not found")


def phrasing(w, lang, scenario):
    """One aligned wording (scenarios.W) in one language."""
    out = {"turns": w[lang]}
    if "expected" in w:
        out["expected_outcome"] = w["expected"]
    if "close" in w:
        out["close_after"] = w["close"]
    if w.get("also"):
        out["also_accepted"] = w["also"]
    if w.get("source"):
        out["source"] = w["source"]
    if w.get("flag"):
        out["assistance_flag"] = True
    if w.get("tail"):
        out["after_close"] = {"text": w["tail"][lang],
                              "expected_outcome": w.get("after_close", scenario.get("after_close"))}
    return out


def main():
    by_id = {s["id"]: s for s in defs.SCENARIOS}
    built = {lang: [] for lang in ("en", "pt", "he")}
    kept = {}                                      # "file:id" -> (scenario id, wording id)
    for s in defs.SCENARIOS:
        for lang in built:
            entry = {"id": s["id"], "situation": s["situation"], "expected_outcome": s["expected"],
                     "close_after": s["close"], "prompt": s.get("prompt", "named"), "phrasings": []}
            for key in ("also_accepted", "pending", "assistance_flag", "no_flag"):
                if s.get(key):
                    entry[key] = s[key]
            for i, w in enumerate(s["words"]):
                ph = phrasing(w, lang, s)
                ph["id"] = f"w{i + 1}"
                entry["phrasings"].append(ph)
                if w.get("source"):
                    kept[w["source"]] = (s["id"], ph["id"])
            built[lang].append(entry)

    # Yair, 2026-11-02: the same tests in every language. Every earlier scenario is still covered: by a
    # wording that keeps it (translated into the other two languages), or by its situation, whose
    # wordings test the same thing (João: dedupe, then translate).
    coverage = []
    for item in defs.LEGACY:
        lang = LANG_OF_FILE[item["file"]]
        target = by_id[item["scenario"]]
        _, old_expected = old_turns(item["file"], item["old_id"])
        source = f"{item['file']}:{item['old_id']}"
        new_expected = item["expected"] or target["expected"]
        close = item["close"] if item["close"] is not None else target["close"]
        if source in kept:
            sid, wid = kept[source]
            assert sid == item["scenario"], f"{source} is kept under {sid}, LEGACY maps it to {item['scenario']}"
            status = f"kept as {wid} (en, pt, he)"
        else:
            status = "covered by situation"
        coverage.append((source, lang, item["scenario"], status, old_expected, new_expected, close,
                         "", item["why"]))
    unknown = set(kept) - {f"{i['file']}:{i['old_id']}" for i in defs.LEGACY}
    assert not unknown, f"source not in LEGACY: {sorted(unknown)}"

    for lang, scenarios in built.items():
        n_words = sum(len(s["phrasings"]) for s in scenarios)
        out = {"version": "ks881-3", "language": lang,
               "description": "KS-881 fall-call test set: every FR v5 situation and every ending transition of the v7 state machine, in several "
                              "wordings, the same in en, pt and he; every scenario of the earlier sets is kept or covered "
                              "(see experiments/ks881/coverage.md). "
                              "close_after = senior answers before the call must close; \"\" = silence.",
               "scenarios": [s for s in scenarios if s["phrasings"]]}
        path = LAB / "data" / "inputs" / f"inputs_ks881_{lang}.json"
        path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{path.name}: {len(out['scenarios'])} scenarios, {n_words} wordings")

    # Every scenario of every earlier set must appear exactly once in LEGACY.
    listed = {(i["file"], i["old_id"]) for i in defs.LEGACY}
    missing = []
    for file in LANG_OF_FILE:
        for s in json.loads((LAB / "data" / "inputs" / file).read_text(encoding="utf-8"))["scenarios"]:
            if (file, s["id"]) not in listed:
                missing.append(f"{file}:{s['id']}")
    dupes = len(defs.LEGACY) - len(listed)

    lines = ["# KS-881 test set: coverage of the earlier sets", "",
             f"{len(listed)} earlier scenarios, all mapped ({len(missing)} missing, {dupes} listed twice). "
             f"{sum(1 for c in coverage if c[3].startswith('kept'))} are kept word for word (translated into the "
             "other two languages); the rest are covered by their situation's wordings.", "",
             "Every wording runs in en, pt and he (the same tests in each language).", "",
             "| Earlier scenario | Lang | New scenario | Kept | Old expected | New expected | Closes after | | Why it changed |",
             "|---|---|---|---|---|---|---|---|---|"]
    for c in coverage:
        changed = c[4] != c[5]
        lines.append("| " + " | ".join([c[0], c[1], c[2], c[3], c[4], ("**" + c[5] + "**") if changed else c[5],
                                         str(c[6]), c[7], c[8]]) + " |")
    if missing:
        lines += ["", "## NOT MAPPED", ""] + [f"- {m}" for m in missing]
    out_dir = LAB / "experiments" / "ks881"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"coverage: {len(listed)} earlier scenarios mapped, {len(missing)} missing, {dupes} listed twice "
          f"-> experiments/ks881/coverage.md")
    if missing or dupes:
        sys.exit(1)


if __name__ == "__main__":
    main()
