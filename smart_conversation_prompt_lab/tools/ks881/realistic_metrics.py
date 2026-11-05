# -*- coding: utf-8 -*-
"""KS-881 realistic set: the figures Yair, Alon and Tony asked for (2026-11-03) from a ks881_eval run.

- Fall detection: of the calls where the senior fell or needed help, how many raised an alert (and how many
  with the right reason).
- False detection: of the calls where the senior was fine, how many raised an alert (and how many as a fall).
- Every failed conversation, with what the senior said and what Vega did.

Usage: python tools/ks881/realistic_metrics.py <experiment label>  ->  experiments/ks881/<label>/metrics.md
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
ALERTS = {"distress_fall_confirmed", "distress_assistance_requested", "distress_unable_to_verify",
          "no_response_from_resident"}
label = sys.argv[1]
lang = sys.argv[2] if len(sys.argv) > 2 else "en"
run_dir = LAB / "experiments" / "ks881" / label
res = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
res = res["results"] if isinstance(res, dict) else res
inputs = json.loads((LAB / "data" / "inputs" / f"inputs_ks881_realistic_{lang}.json").read_text(encoding="utf-8"))
truth_of = {s["id"]: s["truth"] for s in inputs["scenarios"]}
unknown_ids = {s["id"] for s in inputs["scenarios"] if s.get("prompt") == "unknown"}


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "n/a"


rows = {}
for r in res:
    t = truth_of[r["scenario"]] + (" (nobody identified)" if r["scenario"] in unknown_ids else "")
    d = rows.setdefault(t, {"n": 0, "alert": 0, "exact": 0, "fall": 0, "pass": 0})
    d["n"] += 1
    d["alert"] += r["outcome"] in ALERTS
    d["exact"] += r["outcome"] == r["expected"]
    d["fall"] += r["outcome"] == "distress_fall_confirmed"
    d["pass"] += bool(r["passed"])

need = [r for r in res if truth_of[r["scenario"]] in ("fall", "help")]
fine = [r for r in res if truth_of[r["scenario"]] == "fine"]
falls = [r for r in res if truth_of[r["scenario"]] == "fall"]
lines = [f"# KS-881 realistic set ({lang}): {label}", "",
         f"{len(res)} conversations. Passed (outcome, closing turn and goodbye all right): "
         f"**{sum(bool(r['passed']) for r in res)} ({pct(sum(bool(r['passed']) for r in res), len(res))})**.", "",
         "| Figure | Result |", "|---|---|",
         f"| **Fall detection:** fell or needed help, and an alert was raised | "
         f"{sum(r['outcome'] in ALERTS for r in need)} of {len(need)} "
         f"(**{pct(sum(r['outcome'] in ALERTS for r in need), len(need))}**) |",
         f"| ... of those, with the right reason (fall / assistance) | "
         f"{sum(r['outcome'] == r['expected'] for r in need)} of {len(need)} "
         f"({pct(sum(r['outcome'] == r['expected'] for r in need), len(need))}) |",
         f"| Falls reported as a confirmed fall | {sum(r['outcome'] == 'distress_fall_confirmed' for r in falls)} of "
         f"{len(falls)} ({pct(sum(r['outcome'] == 'distress_fall_confirmed' for r in falls), len(falls))}) |",
         f"| **False detection:** fine, but an alert was raised | {sum(r['outcome'] in ALERTS for r in fine)} of "
         f"{len(fine)} (**{pct(sum(r['outcome'] in ALERTS for r in fine), len(fine))}**) |",
         f"| ... of those, reported as a fall | {sum(r['outcome'] == 'distress_fall_confirmed' for r in fine)} of "
         f"{len(fine)} ({pct(sum(r['outcome'] == 'distress_fall_confirmed' for r in fine), len(fine))}) |",
         "", "| What really happened | Calls | Alert raised | Right outcome | Passed |", "|---|---|---|---|---|"]
for t in [x + y for y in ("", " (nobody identified)") for x in ("fall", "help", "fine", "unclear", "silent")]:
    d = rows.get(t)
    if d:
        lines.append(f"| {t} | {d['n']} | {pct(d['alert'], d['n'])} | {pct(d['exact'], d['n'])} | "
                     f"{pct(d['pass'], d['n'])} |")
lat = sorted(x for r in res for x in r["latencies_ms"])
if lat:
    q = lambda p: lat[min(len(lat) - 1, int(len(lat) * p))]  # noqa: E731
    lines += ["", f"Reply time: median {q(.5):.0f} ms, p95 {q(.95):.0f} ms, max {lat[-1]:.0f} ms; "
                  f"{pct(sum(x <= 1000 for x in lat), len(lat))} under 1 s."]
lines += ["", "## Failed conversations", "", "| Conversation | Senior said | Expected | Vega | Why |", "|---|---|---|---|---|"]
for r in res:
    if r["passed"]:
        continue
    said = " · ".join(t["text"] for t in r["transcript"] if t["role"] == "user") or "(nothing)"
    last = next((t for t in reversed(r["transcript"]) if t["role"] == "assistant"), {})
    lines.append(f"| {r['scenario']}/{r['phrasing']} | {said} | {r['expected']} @{r['close_after']} | "
                 f"{r['outcome']} @{r['answers_before_close']}: \"{last.get('text', '')}\" | "
                 f"{'; '.join(r['violations'])} |")
(run_dir / "metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:16]))
print(f"... {sum(not r['passed'] for r in res)} failed conversations listed in {run_dir / 'metrics.md'}")
