#!/usr/bin/env python3
"""
KS-833: score the fall prompt in European Portuguese (pt-PT).

The prompt files come from build_ks833_prompts.py (production replica + Portuguese branches) with
an @@HISTORY@@ placeholder. The request mirrors production: one user message, response_format
json_object, and NO temperature unless --temperature is given.

A run passes only if the outcome is right AND every VEGA line passes the language checks:
  - no English (a sentence-level stop-word check),
  - no Brazilian forms (você, estar + gerund, BR-only vocabulary/spelling),
  - no informal "tu" forms,
  - on an alert outcome, the Portuguese mandated phrase (when --alert-phrase/--noresp-phrase given),
  - a closing line never ends on a question.

Heuristics only — a Portuguese speaker should still read the transcripts in summary.md.

Usage:
    python ks833_eval.py --prompt prompt_ks833_ptpt_asis.txt --runs 3 --label asis_male
    python ks833_eval.py --prompt prompt_ks833_ptpt_v1_male.txt --runs 3 --label v1_male --pt-phrases
"""
import argparse
import json
import os
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import openai
from dotenv import load_dotenv

ROOT = Path(__file__).parent
ASSISTANT_PREFIX = "@ASSISTANT@: "
USER_PREFIX = "@USER@: "
NO_RESPONSE = "<<NO RESPONSE>>"
IN_PROGRESS = "conversation_in_progress"
FALL_CONFIRMED = "distress_fall_confirmed"
NO_RESPONSE_OUTCOME = "no_response_from_resident"

# Must match build_ks833_prompts.ALERT_PT / NORESP_PT.
ALERT_PT = "estou a enviar um alerta no sistema seniormatics"
NORESP_PT = "nao consegui falar consigo, por isso estou a avisar os seus cuidadores"

ENGLISH_WORDS = {"the", "you", "your", "are", "i'm", "i", "okay", "ok", "hello", "hi", "it's", "is",
                 "alert", "raising", "caregivers", "please", "sorry", "fine", "fall", "fell", "hurt",
                 "and", "to", "in", "system", "now", "help", "goodbye", "take", "care", "glad"}
BRAZILIAN = [
    (re.compile(r"\bvoc[eê]s?\b"), "você"),
    (re.compile(r"\b(estou|está|esta|estamos|estão|estao|estava|fico|vou ficar)\s+\w+(ando|endo|indo)\b"),
     "estar + gerund"),
    (re.compile(r"\b(banheiro|celular|registro|ônibus|tchau|oi)\b"), "BR vocabulary"),
    (re.compile(r"\bdetect(amos|ei|ou|ado|ada)\b"), "BR spelling (detect-)"),
]
# The prompt forbids promising that help is coming (CLOSE_POLITELY_GUIDELINE). Reported as a warning.
PROMISES = re.compile(r"\b(algu[eé]m (ir[aá]|vai|v[eê]m|est[aá] a caminho)|a caminho|em breve|"
                      r"j[aá] (vai|v[eê]m) (algu[eé]m|ajuda)|ajuda (vai|est[aá]) a chegar|v[aã]o ajud[aá]-l[oa])\b")
# v5 (gender-neutral): gendered address or agreement about the senior. VEGA's own feminine words
# (obrigada, preocupada) are allowed, so they are not listed.
GENDERED = re.compile(r"\b(senhor|senhora|dona|magoad[oa]s?|sozinh[oa]s?|cansad[oa]s?|ca[ií]d[oa]s?|"
                      r"tranquil[oa]s?|descansad[oa]s?|assustad[oa]s?|ferid[oa]s?|"
                      r"\w+-l[oa]s?)\b")
INFORMAL = re.compile(r"\b(tu|estás|caíste|magoaste|consegues|podes|precisas|queres|te)\b")


def fold(text):
    """Lowercase, straighten quotes, strip accents — for phrase matching only."""
    t = (text or "").replace("’", "'").replace("‘", "'").lower()
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def check_line(text, outcome, args):
    """Returns violations for one VEGA line."""
    low = (text or "").replace("’", "'").lower()
    violations = []
    words = re.findall(r"[a-z']+", re.sub(r"seniormatics|vega", "", low))
    english = [w for w in words if w in ENGLISH_WORDS]
    if len(english) >= 3:
        violations.append(f"english: {' '.join(english[:5])}")
    for rx, name in BRAZILIAN:
        m = rx.search(low)
        if m:
            violations.append(f"brazilian ({name}): '{m.group(0)}'")
    m = INFORMAL.search(low)
    if m:
        violations.append(f"informal tu: '{m.group(0)}'")
    if args.neutral:
        m = GENDERED.search(low)
        if m:
            violations.append(f"gendered: '{m.group(0)}'")
    if outcome != IN_PROGRESS:
        if text.strip().endswith("?"):
            violations.append("closing line ends on a question")
        if args.pt_phrases:
            if outcome == FALL_CONFIRMED and ALERT_PT not in fold(text):
                violations.append("missing pt alert phrase")
            if outcome == NO_RESPONSE_OUTCOME and NORESP_PT not in fold(text):
                violations.append("missing pt no-response phrase")
    return violations


def call_llm(client, model, prompt, temperature):
    kwargs = dict(model=model, messages=[{"role": "user", "content": prompt}],
                  response_format={"type": "json_object"})
    if temperature is not None:
        kwargs["temperature"] = temperature
    start = time.perf_counter()
    for attempt in range(4):
        try:
            r = client.chat.completions.create(**kwargs)
            break
        except (openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError):
            if attempt == 3:
                raise
            time.sleep(2 ** attempt * 2)
            start = time.perf_counter()
    ms = (time.perf_counter() - start) * 1000
    return json.loads(r.choices[0].message.content), ms, r.usage.prompt_tokens, r.usage.completion_tokens


def accepted_outcomes(scenario):
    # "also_accepted": the scripts end in silence, so an unclear script can legitimately close
    # under the prompt's SILENCE RULE instead of as a fall. Both outcomes alert the caregivers.
    return {o.strip().lower() for o in [scenario["expected_outcome"]] + scenario.get("also_accepted", [])}


def rescore(label, inputs):
    """Re-apply the current scenario expectations to a stored run, without calling the LLM."""
    out_dir = ROOT / "experiments" / "ks833" / label
    data = json.loads((out_dir / "results.json").read_text(encoding="utf-8"))
    scenarios = {s["id"]: s for s in
                 json.loads((ROOT / "data/inputs" / inputs).read_text(encoding="utf-8"))["scenarios"]}
    for r in data["results"]:
        r["outcome_ok"] = r["outcome"] in accepted_outcomes(scenarios[r["scenario_id"]])
        r["passed"] = r["outcome_ok"] and r["language_ok"]
    data["meta"]["rescored_with"] = inputs
    (out_dir / "results.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    write_summary(out_dir, data["meta"], data["results"])


def run_one(client, args, template, scenario, run_idx):
    history, transcript, latencies, violations, warnings = [], [], [], [], []
    tokens_in = tokens_out = 0
    turns = scenario["user_turns"]
    ui = silences_after = 0
    outcome = "TIMEOUT"
    for _ in range(args.max_turns):
        prompt = template.replace("@@HISTORY@@", "\n".join(history)).strip()
        try:
            parsed, ms, ti, to = call_llm(client, args.model, prompt, args.temperature)
        except Exception as e:  # noqa: BLE001 - recorded, not fatal to the batch
            outcome = "ERROR"
            transcript.append({"role": "error", "text": str(e)})
            break
        latencies.append(ms)
        tokens_in += ti
        tokens_out += to
        text = parsed.get("text", "")
        out = str(parsed.get("conversationOutcome", IN_PROGRESS)).strip().lower()
        history.append(ASSISTANT_PREFIX + text)
        transcript.append({"role": "assistant", "text": text, "outcome": out})
        violations += [f"turn {len(latencies)}: {v}" for v in check_line(text, out, args)]
        if out != IN_PROGRESS:
            m = PROMISES.search((text or "").lower())
            if m:
                warnings.append(f"promises help: '{m.group(0)}'")
        if out != IN_PROGRESS:
            outcome = out
            break
        if ui < len(turns):
            user = turns[ui].get("text", "")
            ui += 1
        else:
            user = ""
            silences_after += 1
            if silences_after > args.extra_silence:
                break
        history.append(USER_PREFIX + (user if user.strip() else NO_RESPONSE))
        transcript.append({"role": "user", "text": user or "(silence)"})

    expected = scenario["expected_outcome"].strip().lower()
    outcome_ok = outcome in accepted_outcomes(scenario)
    # A guessed reconstruction ("Não QI" -> "não caí") must never be enough to close as fine.
    spoken = sum(1 for t in transcript if t["role"] == "user" and t["text"] != "(silence)")
    min_fine = scenario.get("min_spoken_turns_before_fine")
    if min_fine and outcome == "no_fall_confirmed" and spoken < min_fine:
        violations.append(f"closed as fine after {spoken} spoken answer(s), needs {min_fine}")
    return {
        "scenario_id": scenario["id"], "category": scenario.get("category", ""), "run": run_idx,
        "expected": expected, "outcome": outcome, "outcome_ok": outcome_ok,
        "language_ok": not violations, "violations": violations, "warnings": warnings,
        "passed": outcome_ok and not violations,
        "latencies_ms": latencies, "tokens_in": tokens_in, "tokens_out": tokens_out,
        "transcript": transcript,
    }


def pct(values, q):
    if not values:
        return 0
    s = sorted(values)
    return s[min(len(s) - 1, int(round(q / 100 * (len(s) - 1))))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", help="file under data/prompts")
    ap.add_argument("--inputs", default="inputs_ks833_ptpt.json", help="file under data/inputs")
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--temperature", type=float, default=None, help="omit to match production")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-turns", type=int, default=10)
    ap.add_argument("--extra-silence", type=int, default=2)
    ap.add_argument("--only", default=None, help="comma-separated scenario ids")
    ap.add_argument("--pt-phrases", action="store_true",
                    help="require the Portuguese mandated phrases on alert outcomes")
    ap.add_argument("--neutral", action="store_true",
                    help="flag gendered address/agreement about the senior (v5 gender-neutral prompts)")
    ap.add_argument("--label", required=True)
    ap.add_argument("--rescore", action="store_true",
                    help="re-score experiments/ks833/<label> against --inputs; no LLM calls")
    ap.add_argument("--retry-errors", action="store_true",
                    help="re-run only the ERROR conversations of experiments/ks833/<label>, sequentially")
    args = ap.parse_args()
    if args.rescore:
        rescore(args.label, args.inputs)
        return
    if not args.prompt:
        ap.error("--prompt is required unless --rescore")

    load_dotenv(ROOT / ".env")
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    template = (ROOT / "data/prompts" / args.prompt).read_text(encoding="utf-8")
    assert "@@HISTORY@@" in template, "prompt must be rendered with the @@HISTORY@@ placeholder"
    scenarios = json.loads((ROOT / "data/inputs" / args.inputs).read_text(encoding="utf-8"))["scenarios"]
    if args.only:
        keep = set(args.only.split(","))
        scenarios = [s for s in scenarios if s["id"] in keep]

    out_dir = ROOT / "experiments" / "ks833" / args.label
    if args.retry_errors:
        # Re-run only the conversations that hit an API error (e.g. 429 rate limit) and merge them back.
        data = json.loads((out_dir / "results.json").read_text(encoding="utf-8"))
        by_id = {s["id"]: s for s in scenarios}
        for k, r in enumerate(data["results"]):
            if r["outcome"] == "ERROR":
                data["results"][k] = run_one(client, args, template, by_id[r["scenario_id"]], r["run"])
                print(f"retried {r['scenario_id']}#{r['run']}: {data['results'][k]['outcome']}")
        (out_dir / "results.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
        write_summary(out_dir, data["meta"], data["results"])
        return

    jobs = [(s, i) for s in scenarios for i in range(args.runs)]
    print(f"{args.label}: {len(scenarios)} scenarios x {args.runs} runs = {len(jobs)} conversations "
          f"({args.model}, temperature={args.temperature}, prompt={args.prompt})")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda j: run_one(client, args, template, *j), jobs))

    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"label": args.label, "date": datetime.now().isoformat(timespec="seconds"),
            "model": args.model, "temperature": args.temperature, "prompt": args.prompt,
            "inputs": args.inputs, "runs": args.runs, "pt_phrases": args.pt_phrases,
            "neutral": args.neutral}
    (out_dir / "results.json").write_text(json.dumps({"meta": meta, "results": results}, indent=1,
                                                     ensure_ascii=False), encoding="utf-8")
    write_summary(out_dir, meta, results)


def write_summary(out_dir, meta, results):
    lat = [ms for r in results for ms in r["latencies_ms"]]
    n = len(results)
    unsafe = [r for r in results if r["expected"] != "no_fall_confirmed" and r["outcome"] == "no_fall_confirmed"]
    lines = [f"# KS-833 pt-PT eval: {meta['label']}", "",
             f"{meta['date']} | {meta['model']} | temperature={meta['temperature']} | "
             f"prompt={meta['prompt']} | inputs={meta['inputs']} | runs={meta['runs']}", "",
             "| Pass | Outcome | Language | Unsafe clears | p50 ms | p95 ms | Errors |",
             "|---|---|---|---|---|---|---|",
             f"| {sum(r['passed'] for r in results)}/{n} ({100 * sum(r['passed'] for r in results) / n:.0f}%) "
             f"| {100 * sum(r['outcome_ok'] for r in results) / n:.0f}% "
             f"| {100 * sum(r['language_ok'] for r in results) / n:.0f}% "
             f"| {len(unsafe)} | {pct(lat, 50):.0f} | {pct(lat, 95):.0f} "
             f"| {sum(r['outcome'] == 'ERROR' for r in results)} |", "",
             "Unsafe clear = a fall/unclear/silence scenario closed as no_fall_confirmed.", "",
             "## By scenario", "", "| Scenario | Pass | Outcome ok | Language ok | Outcomes seen |",
             "|---|---|---|---|---|"]
    by = {}
    for r in results:
        by.setdefault(r["scenario_id"], []).append(r)
    for sid, rs in by.items():
        seen = {}
        for r in rs:
            seen[r["outcome"]] = seen.get(r["outcome"], 0) + 1
        lines.append(f"| {sid} | {sum(r['passed'] for r in rs)}/{len(rs)} | "
                     f"{sum(r['outcome_ok'] for r in rs)}/{len(rs)} | {sum(r['language_ok'] for r in rs)}/{len(rs)} | "
                     + ", ".join(f"{k} x{v}" for k, v in seen.items()) + " |")
    viol = {}
    for r in results:
        for v in r["violations"]:
            key = re.sub(r"^turn \d+: ", "", v).split(":")[0]
            viol[key] = viol.get(key, 0) + 1
    lines += ["", "## Language violations", ""] + [f"- {k}: {v}" for k, v in
                                                   sorted(viol.items(), key=lambda x: -x[1])]
    warns = [w for r in results for w in r["warnings"]]
    lines += ["", f"## Warnings: closing line promises help is coming ({len(warns)}/{n} runs)", ""]
    lines += [f"- `{r['scenario_id']}#{r['run']}`: {'; '.join(r['warnings'])}" for r in results if r["warnings"]]
    lines += ["", "## Failing runs", ""]
    for r in results:
        if not r["passed"]:
            lines.append(f"- `{r['scenario_id']}#{r['run']}` expected {r['expected']}, got [{r['outcome']}] "
                         f"-> {'; '.join(r['violations']) or 'wrong outcome'}")
    lines += ["", "## Transcripts (first run of each scenario)", ""]
    for sid, rs in by.items():
        r = rs[0]
        lines.append(f"### {sid} — [{r['outcome']}] {'PASS' if r['passed'] else 'FAIL'}")
        for t in r["transcript"]:
            who = "VEGA" if t["role"] == "assistant" else ("SENIOR" if t["role"] == "user" else "ERROR")
            lines.append(f"- **{who}**: {t['text']}")
        lines.append("")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:7]))
    print(f"Summary: {out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
