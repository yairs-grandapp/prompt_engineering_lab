#!/usr/bin/env python3
"""
KS-834: talk to Azure pt-PT speech recognition live, through the same 8 kHz path the hub uses.

Prints partial results as you speak and each final result with the intent it would map to
(help / safe / yes / no / other). Ctrl+C to stop.

Usage:
    .venv/Scripts/python live_mic.py                 # pt-PT, with the proposed fall boost list
    .venv/Scripts/python live_mic.py --no-boost      # without the boost list
    .venv/Scripts/python live_mic.py --save session  # also keep the audio in recordings/live/
"""
import argparse
import queue
import sys
import time
from datetime import datetime

import numpy as np
import sounddevice as sd
import soundfile as sf

import azure.cognitiveservices.speech as speechsdk
from asr_common import (LANGUAGE, PT_BOOST_PHRASES, ROOT, intent_of, load_config, make_recognizer,
                        speech_config, to_hub_pcm)

MIC_RATE = 16000
BLOCK_MS = 20


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--language", default=LANGUAGE)
    ap.add_argument("--no-boost", action="store_true")
    ap.add_argument("--device", default=None, help="sounddevice input device (index or name)")
    ap.add_argument("--save", default=None, help="name for a WAV copy under recordings/live/")
    args = ap.parse_args()

    key, region = load_config()
    cfg = speech_config(key, region, args.language)
    rec, stream = make_recognizer(cfg, None if args.no_boost else PT_BOOST_PHRASES)

    def on_recognizing(evt):
        sys.stdout.write("\r  … " + evt.result.text[-100:] + " " * 10)
        sys.stdout.flush()

    def on_recognized(evt):
        r = evt.result
        if r.reason == speechsdk.ResultReason.RecognizedSpeech and r.text:
            print(f"\r[{datetime.now():%H:%M:%S}] FINAL ({intent_of(r.text)}): {r.text}" + " " * 20)
        elif r.reason == speechsdk.ResultReason.NoMatch:
            print(f"\r[{datetime.now():%H:%M:%S}] (no match)" + " " * 40)

    def on_canceled(evt):
        d = evt.cancellation_details
        print(f"\nCANCELED: {d.reason} {d.error_details or ''}")

    rec.recognizing.connect(on_recognizing)
    rec.recognized.connect(on_recognized)
    rec.canceled.connect(on_canceled)

    audio_q = queue.Queue()
    kept = []

    def callback(indata, frames, time_info, status):
        audio_q.put(indata.copy())

    rec.start_continuous_recognition_async().get()
    print(f"Listening in {args.language} (8 kHz hub path, boost={'off' if args.no_boost else 'on'}). "
          f"Speak Portuguese — Ctrl+C to stop.")
    try:
        with sd.InputStream(samplerate=MIC_RATE, channels=1, dtype="float32", device=args.device,
                            blocksize=int(MIC_RATE * BLOCK_MS / 1000), callback=callback):
            while True:
                block = audio_q.get()
                if args.save:
                    kept.append(block)
                stream.write(to_hub_pcm(block, MIC_RATE))
    except KeyboardInterrupt:
        pass
    finally:
        stream.close()
        time.sleep(1.0)
        rec.stop_continuous_recognition_async().get()
        if args.save and kept:
            out = ROOT / "recordings" / "live" / f"{args.save}_{datetime.now():%Y%m%d_%H%M%S}.wav"
            out.parent.mkdir(parents=True, exist_ok=True)
            sf.write(str(out), np.concatenate(kept), MIC_RATE)
            print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
