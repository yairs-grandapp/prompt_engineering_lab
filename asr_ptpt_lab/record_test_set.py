#!/usr/bin/env python3
"""
KS-834: record a speaker reading the pt-PT test set, one WAV per sentence.

Saves 16 kHz mono WAVs to recordings/<speaker>/<id>.wav (evaluate.py downsamples to the hub's
8 kHz). Already-recorded sentences are skipped, so a session can be stopped and resumed.

Per sentence: Enter = start, Enter = stop, then Enter = keep / r = redo / p = play / s = skip.
q at any prompt quits.

Usage:
    .venv/Scripts/python record_test_set.py --speaker joao_lisboa
    .venv/Scripts/python record_test_set.py --speaker maria_azores --only a001,a002
"""
import argparse
import csv

import numpy as np
import sounddevice as sd
import soundfile as sf

from asr_common import ROOT

RATE = 16000


def record_until_enter(device):
    chunks = []
    with sd.InputStream(samplerate=RATE, channels=1, dtype="float32", device=device,
                        callback=lambda indata, *a: chunks.append(indata.copy())):
        input("  recording… Enter to stop ")
    return np.concatenate(chunks) if chunks else np.zeros((0, 1), dtype=np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speaker", required=True, help="e.g. joao_lisboa, maria_azores (no spaces)")
    ap.add_argument("--sentences", default="data/sentences_ptpt.csv")
    ap.add_argument("--only", default=None, help="comma-separated sentence ids")
    ap.add_argument("--device", default=None)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(ROOT / args.sentences, encoding="utf-8")))
    if args.only:
        keep = set(args.only.split(","))
        rows = [r for r in rows if r["id"] in keep]
    out_dir = ROOT / "recordings" / args.speaker
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = [r for r in rows if not (out_dir / f"{r['id']}.wav").exists()]
    print(f"{args.speaker}: {len(rows) - len(todo)}/{len(rows)} already recorded, {len(todo)} to go.\n"
          "Read each sentence naturally, as you would answer Vega on the phone.\n")

    for i, r in enumerate(todo, 1):
        while True:
            print(f"[{i}/{len(todo)}] {r['id']}  »  {r['text']}")
            cmd = input("  Enter to start (s skip, q quit) ").strip().lower()
            if cmd == "q":
                print(f"\nStopped. Recordings in {out_dir}")
                return
            if cmd == "s":
                break
            audio = record_until_enter(args.device)
            peak = float(np.abs(audio).max()) if audio.size else 0.0
            print(f"  {len(audio) / RATE:.1f}s, peak {peak:.2f}" + ("  ⚠ very quiet" if peak < 0.05 else ""))
            choice = input("  Enter keep / r redo / p play ").strip().lower()
            while choice == "p":
                sd.play(audio, RATE)
                sd.wait()
                choice = input("  Enter keep / r redo / p play ").strip().lower()
            if choice == "r":
                continue
            sf.write(str(out_dir / f"{r['id']}.wav"), audio, RATE)
            break
    print(f"\nDone. Recordings in {out_dir}")


if __name__ == "__main__":
    main()
