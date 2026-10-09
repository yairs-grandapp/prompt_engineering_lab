#!/usr/bin/env python3
"""
KS-835: synthesize the VEGA test lines with each candidate Azure pt-PT voice, for listening and latency.

Mirrors the production TTS path (picmeinserver SmartConversation): audio is requested at 24 kHz, like
Google streaming today, and downsampled to TEXT_TO_SPEECH_SAMPLE_RATE = 16 kHz before it goes to the
hub. The 16 kHz file is the one to judge; the 24 kHz original is kept for reference.

Latency is measured on a warm connection (opened before the request, as a long-running server would
keep it): time to first audio = request sent -> first non-empty audio chunk (Synthesizing event).

Output: results/<label>/<voice>/<line>_16k.wav and _24k.wav, results.csv, summary.md, listen.html.

Usage:
    ../asr_ptpt_lab/.venv/Scripts/python synthesize_azure.py --label azure_first_pass
    ../asr_ptpt_lab/.venv/Scripts/python synthesize_azure.py --label smoke --voices pt-PT-RaquelNeural --lines greeting
"""
import argparse
import csv
import html
import json
import os
import statistics
import threading
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf
from dotenv import load_dotenv
from scipy.signal import resample_poly

import azure.cognitiveservices.speech as speechsdk

ROOT = Path(__file__).parent
SOURCE_RATE = 24000
HUB_RATE = 16000  # SmartConversation.TEXT_TO_SPEECH_SAMPLE_RATE


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def load_config():
    # Same dev key as the KS-834 ASR lab; a local .env here takes precedence.
    load_dotenv(ROOT / ".env")
    load_dotenv(ROOT.parent / "asr_ptpt_lab" / ".env")
    key, region = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise SystemExit("Set AZURE_SPEECH_KEY / AZURE_SPEECH_REGION (dev key) in tts_ptpt_lab/.env "
                         "or asr_ptpt_lab/.env.")
    return key, region


def ssml(voice, text):
    # Voices that are not native pt-PT speak it through <lang>; native ones must not get the tag.
    body = html.escape(text)
    if not voice.startswith("pt-PT-"):
        body = f"<lang xml:lang='pt-PT'>{body}</lang>"
    return ("<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='pt-PT'>"
            f"<voice name='{voice}'>{body}</voice></speak>")


def synthesize(synth, voice, text):
    first = {}
    start = [0.0]

    def on_chunk(evt):
        if "t" not in first and evt.result.audio_data:
            first["t"] = time.perf_counter()

    synth.synthesizing.connect(on_chunk)
    try:
        start[0] = time.perf_counter()
        result = synth.speak_ssml_async(ssml(voice, text)).get()
        total_ms = (time.perf_counter() - start[0]) * 1000
    finally:
        synth.synthesizing.disconnect_all()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        detail = result.cancellation_details
        return None, None, total_ms, f"{detail.reason}: {detail.error_details}"
    ttfa_ms = (first["t"] - start[0]) * 1000 if "t" in first else None
    return result.audio_data, ttfa_ms, total_ms, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--voices", default=None, help="comma-separated; default data/voices_azure.tsv")
    ap.add_argument("--lines", default=None, help="comma-separated line ids; default all")
    args = ap.parse_args()

    key, region = load_config()
    voices = read_tsv(ROOT / "data/voices_azure.tsv")
    if args.voices:
        keep = args.voices.split(",")
        voices = [v for v in voices if v["voice"] in keep] or [{"voice": v, "kind": "", "status": "", "note": ""}
                                                               for v in keep]
    lines = read_tsv(ROOT / "data/lines_ptpt.tsv")
    if args.lines:
        lines = [l for l in lines if l["id"] in args.lines.split(",")]

    cfg = speechsdk.SpeechConfig(subscription=key, region=region)
    cfg.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Raw24Khz16BitMonoPcm)
    out_dir = ROOT / "results" / args.label
    rows = []
    chars = 0
    for v in voices:
        vdir = out_dir / v["voice"].replace(":", "_")
        vdir.mkdir(parents=True, exist_ok=True)
        synth = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=None)
        speechsdk.Connection.from_speech_synthesizer(synth).open(True)  # warm, like a running server
        for line in lines:
            audio, ttfa, total, err = synthesize(synth, v["voice"], line["text"])
            chars += len(line["text"])
            row = {"voice": v["voice"], "line": line["id"], "ttfa_ms": round(ttfa) if ttfa else "",
                   "total_ms": round(total), "audio_s": "", "error": err}
            if audio:
                pcm = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0
                sf.write(vdir / f"{line['id']}_24k.wav", pcm, SOURCE_RATE, subtype="PCM_16")
                sf.write(vdir / f"{line['id']}_16k.wav", resample_poly(pcm, 2, 3), HUB_RATE, subtype="PCM_16")
                row["audio_s"] = round(len(pcm) / SOURCE_RATE, 2)
            rows.append(row)
            print(f"{v['voice']:40s} {line['id']:12s} ttfa={row['ttfa_ms']}ms total={row['total_ms']}ms "
                  f"{err[:120]}")

    with open(out_dir / "results.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    meta = {"label": args.label, "date": datetime.now().isoformat(timespec="seconds"), "region": region,
            "sdk": speechsdk.__version__, "characters": chars, "source_rate": SOURCE_RATE, "hub_rate": HUB_RATE}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    write_summary(out_dir, meta, voices, lines, rows)
    write_listen_page(out_dir, voices, lines, rows)
    print(f"{chars} characters synthesized. Listen: {out_dir / 'listen.html'}")


def write_summary(out_dir, meta, voices, lines, rows):
    out = [f"# KS-835 Azure pt-PT TTS: {meta['label']}", "",
           f"{meta['date']} | region {meta['region']} | SDK {meta['sdk']} | {meta['characters']} characters | "
           f"judge the 16 kHz files (production hub rate)", "",
           "Time to first audio = request sent on a warm connection -> first audio chunk.", "",
           "| Voice | Kind | Status | TTFA median ms | TTFA max ms | Errors |", "|---|---|---|---|---|---|"]
    for v in voices:
        rs = [r for r in rows if r["voice"] == v["voice"]]
        t = [r["ttfa_ms"] for r in rs if r["ttfa_ms"] != ""]
        out.append(f"| {v['voice']} | {v['kind']} | {v['status']} | "
                   f"{statistics.median(t) if t else '-'} | {max(t) if t else '-'} | "
                   f"{sum(1 for r in rs if r['error'])} |")
    errs = [r for r in rows if r["error"]]
    if errs:
        out += ["", "## Errors", ""] + [f"- `{r['voice']}` / {r['line']}: {r['error']}" for r in errs]
    out += ["", "## Lines", ""] + [f"- **{l['id']}** ({l['what it tests']}): {l['text']}" for l in lines]
    (out_dir / "summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def write_listen_page(out_dir, voices, lines, rows, name="listen.html"):
    # A voice may carry "folder" (a results/<label> run) so one page can compare runs side by side.
    ok = {(r["voice"], r["line"]) for r in rows if not r["error"]}
    parts = ["<!doctype html><meta charset='utf-8'><title>KS-835 pt-PT voices</title>",
             "<style>body{font-family:system-ui,sans-serif;margin:16px;max-width:1100px}"
             "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px;vertical-align:top}"
             "th{background:#f3f3f3;text-align:left}audio{width:220px}.t{color:#555;font-size:.9em}</style>",
             "<h1>KS-835 — European Portuguese voices (16 kHz, as the hub plays them)</h1>",
             "<table><tr><th>Line</th>" + "".join(f"<th>{html.escape(v['voice'])}<div class=t>"
                                                   f"{html.escape(v['kind'])} · {html.escape(v['status'])}</div></th>"
                                                   for v in voices) + "</tr>"]
    for l in lines:
        cells = []
        for v in voices:
            src = f"{v['voice'].replace(':', '_')}/{l['id']}_16k.wav"
            if v.get("folder"):
                src = f"{v['folder']}/{src}"
            cells.append(f"<td><audio controls preload=none src='{src}'></audio></td>"
                         if (v["voice"], l["id"]) in ok else "<td>error</td>")
        parts.append(f"<tr><td><b>{l['id']}</b><div class=t>{html.escape(l['text'])}</div></td>{''.join(cells)}</tr>")
    parts.append("</table>")
    (out_dir / name).write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
