#!/usr/bin/env python3
"""
KS-834: run recorded test-set audio through Azure pt-PT ASR the way the server does, and score it.

For every recordings/<speaker>/<id>.wav: downsample to 8 kHz, push into continuous recognition
(with and/or without the proposed fall boost list), then score against the sentence text:
  - WER (accents kept — 'caí'/'cai' differ in meaning) and WER ignoring accents,
  - intent accuracy on the agreed answers (help / safe / yes / no) — the number that matters for
    VEGA: a help sentence heard as safe is the dangerous error and is counted separately,
  - empty results (the recognizer returned nothing for real speech).

Writes results/<label>/results.csv and summary.md.

Usage:
    .venv/Scripts/python evaluate.py --label first_pass                       # all speakers, boost on+off
    .venv/Scripts/python evaluate.py --label azores --speakers maria_azores --boost on
"""
import argparse
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import jiwer

from asr_common import (BOOST_WEIGHT, LANGUAGE, PT_BOOST_PHRASES, ROOT, intent_of, load_config, normalise,
                        recognize_wav, speech_config)

KEY_INTENTS = ("help", "safe", "yes", "no")


def wer(ref, hyp):
    if not ref:
        return 0.0
    return jiwer.wer(ref, hyp) if hyp else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--speakers", default=None, help="comma-separated; default all under recordings/")
    ap.add_argument("--boost", choices=["on", "off", "both"], default="both")
    ap.add_argument("--sentences", default="data/sentences_ptpt.csv")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--phrases-file", default=None,
                    help="boost phrases, one per line (default: asr_common.PT_BOOST_PHRASES)")
    ap.add_argument("--weight", type=float, default=BOOST_WEIGHT,
                    help="phrase-list weight, 0-2 (production uses 1.5)")
    ap.add_argument("--realtime", action="store_true", help="pace audio at real speed like the hub")
    ap.add_argument("--rescore", action="store_true",
                    help="re-apply intent scoring to results/<label>/results.csv without calling Azure")
    args = ap.parse_args()

    if args.rescore:
        rescore(args.label)
        return
    key, region = load_config()
    cfg = speech_config(key, region)
    phrases = (PT_BOOST_PHRASES if not args.phrases_file else
               [l.strip() for l in open(ROOT / args.phrases_file, encoding="utf-8") if l.strip()
                and not l.startswith("#")])
    sentences = {r["id"]: r for r in csv.DictReader(open(ROOT / args.sentences, encoding="utf-8"))}
    rec_root = ROOT / "recordings"
    speakers = (args.speakers.split(",") if args.speakers
                else sorted(p.name for p in rec_root.iterdir() if p.is_dir() and p.name != "live"))
    modes = {"on": [True], "off": [False], "both": [False, True]}[args.boost]

    jobs = []
    for spk in speakers:
        for wav in sorted((rec_root / spk).glob("*.wav")):
            if wav.stem in sentences:
                for boost in modes:
                    jobs.append((spk, wav, boost))
    if not jobs:
        raise SystemExit("No recordings found. Run record_test_set.py or synthesize_test_set.py first.")
    print(f"{args.label}: {len(jobs)} recognitions ({len(speakers)} speakers, boost={args.boost}, {LANGUAGE})")

    def run(job):
        spk, wav, boost = job
        s = sentences[wav.stem]
        r = recognize_wav(cfg, wav, phrases if boost else None, realtime=args.realtime, weight=args.weight)
        ref = normalise(s["text"])
        hyp = normalise(r["text"])
        got = intent_of(r["text"])
        return {
            "speaker": spk, "id": s["id"], "category": s["category"], "boost": "on" if boost else "off",
            "reference": s["text"], "hypothesis": r["text"],
            "wer": round(wer(ref, hyp), 3),
            "wer_no_accents": round(wer(normalise(s["text"], False), normalise(r["text"], False)), 3),
            "intent_expected": s["intent"], "intent_got": got,
            "intent_ok": got == s["intent"], "empty": not r["text"], "error": r["error"],
            "latency_ms": round(r["ms"]),
        }

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(run, jobs))

    out_dir = ROOT / "results" / args.label
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    meta = {"label": args.label, "date": datetime.now().isoformat(timespec="seconds"),
            "language": LANGUAGE, "speakers": speakers, "boost": args.boost, "realtime": args.realtime,
            "boost_phrases": phrases, "weight": args.weight}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    write_summary(out_dir, meta, results)


def rescore(label):
    out_dir = ROOT / "results" / label
    with open(out_dir / "results.csv", encoding="utf-8") as f:
        results = list(csv.DictReader(f))
    for r in results:
        r["wer"] = float(r["wer"])
        r["wer_no_accents"] = float(r["wer_no_accents"])
        r["empty"] = r["empty"] == "True"
        r["intent_got"] = intent_of(r["hypothesis"])
        r["intent_ok"] = r["intent_got"] == r["intent_expected"]
    with open(out_dir / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
    write_summary(out_dir, meta, results)


def _stats(rs):
    key = [r for r in rs if r["intent_expected"] in KEY_INTENTS]
    help_rs = [r for r in rs if r["intent_expected"] == "help"]
    return {
        "n": len(rs),
        "wer": sum(r["wer"] for r in rs) / len(rs) if rs else 0,
        "wer_na": sum(r["wer_no_accents"] for r in rs) / len(rs) if rs else 0,
        "intent": (sum(r["intent_ok"] for r in key), len(key)),
        "help_missed": sum(r["intent_got"] != "help" for r in help_rs),
        "help_as_safe": sum(r["intent_got"] == "safe" for r in help_rs),
        "safe_as_help": sum(r["intent_expected"] == "safe" and r["intent_got"] == "help" for r in rs),
        "empty": sum(r["empty"] for r in rs),
        "errors": sum(bool(r["error"]) for r in rs),
    }


def _row(name, s):
    ok, n = s["intent"]
    return (f"| {name} | {s['n']} | {100 * s['wer']:.1f}% | {100 * s['wer_na']:.1f}% | "
            f"{ok}/{n} ({100 * ok / n if n else 0:.0f}%) | {s['help_missed']} | **{s['help_as_safe']}** | "
            f"{s['safe_as_help']} | {s['empty']} | {s['errors']} |")


def write_summary(out_dir, meta, results):
    head = ("| Group | N | WER | WER (no accents) | Key-answer intent | Help missed | Help heard as SAFE | "
            "Safe heard as help | Empty | Errors |\n|---|---|---|---|---|---|---|---|---|---|")
    lines = [f"# KS-834 pt-PT ASR eval: {meta['label']}", "",
             f"{meta['date']} | Azure {meta['language']} | 8 kHz hub path | realtime={meta['realtime']} | boost weight={meta.get('weight', 1.5)} ({len(meta.get('boost_phrases', []))} phrases)", "",
             "Help heard as SAFE is the dangerous error (a fall answered as 'I'm fine').", "",
             "## By speaker and boost list", "", head]
    groups = {}
    for r in results:
        groups.setdefault((r["speaker"], r["boost"]), []).append(r)
    for (spk, boost), rs in sorted(groups.items()):
        lines.append(_row(f"{spk} / boost {boost}", _stats(rs)))
    lines += ["", "## By category (all speakers)", "", head]
    cats = {}
    for r in results:
        cats.setdefault((r["category"], r["boost"]), []).append(r)
    for (cat, boost), rs in sorted(cats.items()):
        lines.append(_row(f"{cat} / boost {boost}", _stats(rs)))
    lines += ["", "## Key-answer intent errors", ""]
    for r in results:
        if r["intent_expected"] in KEY_INTENTS and not r["intent_ok"]:
            lines.append(f"- `{r['speaker']}/{r['id']}` boost {r['boost']}: expected **{r['intent_expected']}**, "
                         f"got {r['intent_got']} — said “{r['reference']}”, heard “{r['hypothesis']}”")
    lines += ["", "## Worst transcriptions (WER ≥ 0.5)", ""]
    for r in sorted(results, key=lambda x: -x["wer"]):
        if r["wer"] < 0.5:
            break
        lines.append(f"- `{r['speaker']}/{r['id']}` boost {r['boost']} WER {r['wer']:.2f}: "
                     f"“{r['reference']}” → “{r['hypothesis']}”" + (f" [error: {r['error']}]" if r["error"] else ""))
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:8 + len(groups)]))
    print(f"Summary: {out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
