#!/usr/bin/env python3
"""
KS-835: synthesize the VEGA test lines with AWS Polly pt-PT voices, for listening and latency.

Polly returns 16 kHz PCM directly, which is already the hub playback rate
(SmartConversation.TEXT_TO_SPEECH_SAMPLE_RATE), so no resampling is needed.

Time to first audio = request sent -> first audio bytes read from the streamed response. The first
line of each voice also pays for the HTTPS connection; later lines reuse it.

Output: results/<label>/<voice>/<line>_16k.wav, results.csv, summary.md, listen.html.

Credentials: tts_ptpt_lab/.env (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION), see .env.example.

Usage:
    ../asr_ptpt_lab/.venv/Scripts/python synthesize_polly.py --label polly_first_pass
"""
import argparse
import csv
import json
import os
import statistics
import time
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import soundfile as sf
from dotenv import load_dotenv

from synthesize_azure import read_tsv, write_listen_page

ROOT = Path(__file__).parent
HUB_RATE = 16000

# Polly pt-PT (describe_voices): Ines supports neural + standard; Cristiano is standard-only and male,
# so not a VEGA candidate. Polly has no generative pt-PT voice.
VOICES = [{"voice": "Ines", "engine": "neural", "kind": "native pt-PT neural (Polly)", "status": "GA", "note": ""}]


def synthesize(polly, voice, engine, text):
    start = time.perf_counter()
    r = polly.synthesize_speech(Text=text, VoiceId=voice, Engine=engine, LanguageCode="pt-PT",
                                OutputFormat="pcm", SampleRate=str(HUB_RATE))
    stream = r["AudioStream"]
    first = stream.read(1024)
    ttfa_ms = (time.perf_counter() - start) * 1000
    audio = first + stream.read()
    return audio, ttfa_ms, (time.perf_counter() - start) * 1000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--lines", default=None, help="comma-separated line ids; default all")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    region = os.environ.get("AWS_REGION")
    if not (os.environ.get("AWS_ACCESS_KEY_ID") and region):
        raise SystemExit("Set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_REGION in tts_ptpt_lab/.env")
    polly = boto3.client("polly", region_name=region)
    lines = read_tsv(ROOT / "data/lines_ptpt.tsv")
    if args.lines:
        lines = [l for l in lines if l["id"] in args.lines.split(",")]

    out_dir = ROOT / "results" / args.label
    rows, chars = [], 0
    for v in VOICES:
        vdir = out_dir / v["voice"]
        vdir.mkdir(parents=True, exist_ok=True)
        for line in lines:
            row = {"voice": v["voice"], "line": line["id"], "ttfa_ms": "", "total_ms": "", "audio_s": "", "error": ""}
            try:
                audio, ttfa, total = synthesize(polly, v["voice"], v["engine"], line["text"])
                pcm = np.frombuffer(audio, dtype=np.int16)
                sf.write(vdir / f"{line['id']}_16k.wav", pcm, HUB_RATE, subtype="PCM_16")
                row.update(ttfa_ms=round(ttfa), total_ms=round(total), audio_s=round(len(pcm) / HUB_RATE, 2))
            except Exception as e:  # noqa: BLE001 - recorded per line
                row["error"] = str(e)
            chars += len(line["text"])
            rows.append(row)
            print(f"{v['voice']:10s} {line['id']:12s} ttfa={row['ttfa_ms']}ms total={row['total_ms']}ms {row['error'][:120]}")

    with open(out_dir / "results.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    meta = {"label": args.label, "date": datetime.now().isoformat(timespec="seconds"), "region": region,
            "boto3": boto3.__version__, "characters": chars, "hub_rate": HUB_RATE, "voices": VOICES}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    out = [f"# KS-835 AWS Polly pt-PT TTS: {args.label}", "",
           f"{meta['date']} | region {region} | {chars} characters | 16 kHz PCM (hub rate)", "",
           "| Voice | Engine | TTFA median ms | TTFA max ms | Errors |", "|---|---|---|---|---|"]
    for v in VOICES:
        t = [r["ttfa_ms"] for r in rows if r["voice"] == v["voice"] and r["ttfa_ms"] != ""]
        out.append(f"| {v['voice']} | {v['engine']} | {statistics.median(t) if t else '-'} | "
                   f"{max(t) if t else '-'} | {sum(1 for r in rows if r['voice'] == v['voice'] and r['error'])} |")
    (out_dir / "summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    write_listen_page(out_dir, VOICES, lines, rows)
    print(f"{chars} characters synthesized. Listen: {out_dir / 'listen.html'}")


if __name__ == "__main__":
    main()
