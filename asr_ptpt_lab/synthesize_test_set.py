#!/usr/bin/env python3
"""
KS-834: generate a synthetic "speaker" for the test set with Azure pt-PT neural voices.

This is a pipeline check and an upper bound, NOT an accent test: clean synthetic Lisbon-standard
speech is the easiest possible input. Real speakers (record_test_set.py), especially Azorean ones,
are what the go / no-go must rest on.

Output: recordings/tts_<voice>/<id>.wav at 16 kHz.

Usage:
    .venv/Scripts/python synthesize_test_set.py                         # pt-PT-RaquelNeural
    .venv/Scripts/python synthesize_test_set.py --voice pt-PT-DuarteNeural
"""
import argparse
import csv

import azure.cognitiveservices.speech as speechsdk
from asr_common import ROOT, load_config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="pt-PT-RaquelNeural")
    ap.add_argument("--sentences", default="data/sentences_ptpt.csv")
    args = ap.parse_args()

    key, region = load_config()
    cfg = speechsdk.SpeechConfig(subscription=key, region=region)
    cfg.speech_synthesis_voice_name = args.voice
    cfg.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)

    out_dir = ROOT / "recordings" / f"tts_{args.voice}"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / args.sentences, encoding="utf-8")))
    for r in rows:
        path = out_dir / f"{r['id']}.wav"
        if path.exists():
            continue
        synth = speechsdk.SpeechSynthesizer(speech_config=cfg,
                                            audio_config=speechsdk.audio.AudioOutputConfig(filename=str(path)))
        res = synth.speak_text_async(r["text"]).get()
        del synth  # releases the file handle
        if res.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            d = res.cancellation_details
            path.unlink(missing_ok=True)
            raise SystemExit(f"{r['id']}: synthesis failed: {d.reason} {d.error_details}")
        print(f"{r['id']} ok")
    print(f"Done: {out_dir}")


if __name__ == "__main__":
    main()
