#!/usr/bin/env python3
"""
KS-831: score fall-call goodbyes against the approved functional requirements.

The prompt files are rendered from the real Java (ContextDistressFallDetected.buildPrompt),
not transcribed, so they match production byte for byte apart from the conversation history,
which replaces the @@HISTORY@@ placeholder. The request mirrors production too: one user
message, response_format json_object, and NO temperature unless --temperature is given
(production sends none, so OpenAI's default applies).

A run passes only if the outcome is right AND, when the call ends, the goodbye meets every rule.

Prompts come from tools/ks831/render_ks831.py (baseline = origin/a475i as is, candidate_vN = with
tools/ks831/candidate_vN.patch).

KEY SAFETY: only the dev key may be used. The key is read from OPENAI_DEV_API_KEY (or OPENAI_API_KEY) in
.env; its fingerprint is printed and the run refuses to start unless --key-fingerprint matches it, and
always refuses the server keys listed in BLOCKED_KEY_FINGERPRINTS. --dry-run makes no API call and
prints the number of conversations and an estimated cost.

Usage:
    python ks831_eval.py --prompt prompt_ks831_baseline.txt --runs 3 --label baseline_r3 --dry-run
    python ks831_eval.py --prompt prompt_ks831_baseline.txt --runs 3 --label baseline_r3 --key-fingerprint <fp>
    python ks831_eval.py --prompt prompt_ks831_candidate_v1.txt --runs 5 --label candidate_v1_r5 --key-fingerprint <fp>
"""
import argparse
import hashlib
import sys
import json
import os
import re
import statistics
import time
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
NO_FALL = "no_fall_confirmed"
NO_RESPONSE_OUTCOME = "no_response_from_resident"
ALERT_OUTCOMES = {FALL_CONFIRMED, NO_RESPONSE_OUTCOME}
ALERT_PHRASE = "i'm raising an alert in the seniormatics system"

# USD per 1M tokens (input, output), OpenAI list price as last checked; the summary's cost is an
# estimate from the returned token counts, not the invoice.
PRICES = {"gpt-4o": (2.50, 10.00)}
# Keys the lab must never spend: sha256(key)[:10]. 4b1a8630d4 is the key in the local conversation
# server config (C:\grandapp_server_local\startupConfigs\picmein.conversation.json).
BLOCKED_KEY_FINGERPRINTS = {"4b1a8630d4": "conversation server key"}

# The goodbye rules are the same in every language (manager, 2026-10-13); only the words the checker
# looks for are translated. Hebrew and Portuguese lists are the lab's own and need a native review.
LANGS = {
    "en": {
        "alert": ALERT_PHRASE,
        "goodbye": "goodbye",
        # Functional requirement: never ask a question or offer more help.
        "invitations": [
            "let me know", "if you need", "anything else", "i'm here", "i am here", "here with you",
            "here for you", "staying with you", "stay with you", "call me", "tell me", "reach out",
            "feel free", "talk to me", "i'll be here", "i will be here",
        ],
        # Must not change: never promise that help is on the way or that someone is coming.
        "promises": [
            "on the way", "on their way", "someone will", "somebody will", "is coming", "are coming",
            "will be with you", "will come", "will check on you", "check on you", "will be there",
            "be there soon", "shortly", "help will", "will help you", "will arrive", "dispatched",
        ],
        # Functional requirement: never "I could not reach you" or any variant.
        "could_not_reach": re.compile(
            r"\b(could ?n[o']t|could not|was ?n[o']t able to|was not able to|unable to|can ?n[o']t|cannot)"
            r"\s+(reach|get through to|contact)\b"),
        "alert_word": "alert",
        "you_fell": re.compile(r"\byou fell\b"),
        "senior_fell": re.compile(r"\b(fell|fall|fallen)\b"),
        "not_heard": "haven't heard from you",
        "reason_unclear": ("trouble understanding",),
        "reason_fell": ("sorry",),
    },
    "pt": {
        "alert": "estou a enviar um alerta no sistema seniormatics",
        "goodbye": "adeus",
        "invitations": [
            "diga-me", "avise-me", "se precisar", "estou aqui", "estou consigo", "fico consigo",
            "fico aqui", "ligue-me", "chame-me", "mais alguma coisa", "qualquer coisa",
        ],
        "promises": [
            "a caminho", "em breve", "brevemente", "já vem", "alguém vai", "alguém irá", "alguém virá",
            "vai ajudá", "irá ajudá", "vão ajudá", "vai chegar", "vão chegar", "vem aí", "vêm aí",
        ],
        "could_not_reach": re.compile(r"não consegui (falar|contactar|chegar|comunicar|entrar em contacto)"),
        "alert_word": "alerta",
        "you_fell": re.compile(r"\b(caiu|ca[ií]do|ca[ií]da)\b"),
        # KS-833 ASR forms of "caí" count as the senior saying it.
        "senior_fell": re.compile(r"ca[ií]|queda|\bqi\b|\bti\b|k í|kí"),
        "not_heard": "não tive resposta",
        "reason_unclear": ("perceb", "entend"),
        "reason_fell": ("lamento", "sinto muito"),
    },
    "he": {
        "alert": "אני מעבירה התראה במערכת סניורמטיקס",
        "goodbye": "להתראות",
        "invitations": [
            "תגיד לי", "תגידי לי", "תודיע לי", "תודיעי לי", "אם תצטרך", "אם תצטרכי", "אני כאן", "אני פה",
            "אני איתך", "נשארת איתך", "תתקשר", "תתקשרי", "עוד משהו", "משהו נוסף",
        ],
        "promises": [
            "בדרך", "בקרוב", "מישהו יגיע", "מישהו יבוא", "יגיעו", "יבואו", "יעזרו לך", "עזרה תגיע",
            "תגיע עזרה", "יבדקו",
        ],
        "could_not_reach": re.compile(r"לא הצלחתי (ליצור|להשיג|לדבר|להגיע)"),
        "alert_word": "התראה",
        "you_fell": re.compile(r"נפלת"),
        "senior_fell": re.compile(r"נפל"),
        "not_heard": "לא שמעתי",
        "reason_unclear": ("להבין",),
        "reason_fell": ("מצטערת", "צר לי"),
    },
}
LANG = LANGS["en"]


def set_language(code):
    global LANG
    LANG = LANGS[code]


def normalise(text):
    # Curly apostrophes (GPT-5+) and Hebrew nikud (the prompt asks for it on gendered words) are
    # stripped so the word lists match.
    text = (text or "").replace("’", "'").replace("‘", "'")
    return re.sub("[֑-ׇ]", "", text).strip()


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def check_goodbye(text, outcome, senior_spoke, senior_text=""):
    """Returns (violations, warnings) for a terminal message."""
    t = normalise(text)
    low = t.lower()
    violations = []
    warnings = []
    # Manager (2026-10-13): say back what the senior said; "hurt" and "need help" are not "fell".
    if LANG["you_fell"].search(low) and not LANG["senior_fell"].search(normalise(senior_text).lower()):
        violations.append("says 'you fell' to a senior who never said so")
    if "?" in t:
        violations.append("question")
    for p in LANG["invitations"]:
        if p in low:
            violations.append(f"invites reply: '{p}'")
    for p in LANG["promises"]:
        if p in low:
            violations.append(f"promise: '{p}'")
    if LANG["could_not_reach"].search(low):
        violations.append("could-not-reach")
    n = len(sentences(t))
    if n > 4:
        violations.append(f"{n} sentences")
    goodbye = LANG["goodbye"]
    # Manager (2026-10-13): the last word need not be "Goodbye"; the last sentence must say goodbye
    # ("Goodbye, David." and "להתראות דוד." pass).
    last = sentences(low)[-1] if sentences(low) else ""
    if goodbye not in last:
        violations.append(f"last sentence does not say '{goodbye}'")
    if low.count(goodbye) > 1:
        violations.append("says goodbye twice")
    if outcome in ALERT_OUTCOMES and LANG["alert"] not in low:
        violations.append("missing alert phrase")
    if outcome == NO_FALL and LANG["alert_word"] in low:
        violations.append("mentions an alert on an 'I'm fine' call")
    if senior_spoke and LANG["not_heard"] in low:
        warnings.append("'haven't heard from you' said to a senior who spoke")
    return violations, warnings


def check_reason(text, category):
    """Warnings only: the approved openings are examples, not mandated wording."""
    low = normalise(text).lower()
    if category == "unclear" and not any(w in low for w in LANG["reason_unclear"]):
        return ["unclear call without 'trouble understanding'"]
    if category in ("fell", "help") and not any(w in low for w in LANG["reason_fell"]):
        return ["'I fell' call without 'sorry'"]
    return []


def call_llm(client, model, prompt, temperature, reasoning_effort):
    kwargs = dict(model=model, messages=[{"role": "user", "content": prompt}],
                  response_format={"type": "json_object"})
    if temperature is not None:
        kwargs["temperature"] = temperature
    if reasoning_effort:
        kwargs["reasoning_effort"] = reasoning_effort
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
    content = r.choices[0].message.content
    parsed = json.loads(content)
    return parsed, ms, r.usage.prompt_tokens, r.usage.completion_tokens


def run_one(client, args, template, scenario, run_idx):
    history = []
    transcript = []
    latencies = []
    tokens_in = tokens_out = 0
    turns = scenario["user_turns"]
    ui = 0
    silences_after = 0
    senior_spoke = False
    outcome = "TIMEOUT"
    final_text = ""
    for _ in range(args.max_turns):
        prompt = template.replace("@@HISTORY@@", "\n".join(history)).strip()
        try:
            parsed, ms, ti, to = call_llm(client, args.model, prompt, args.temperature, args.reasoning_effort)
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
        if out != IN_PROGRESS:
            outcome = out
            final_text = text
            break
        if ui < len(turns):
            user = turns[ui].get("text", "")
            ui += 1
        else:
            user = ""
            silences_after += 1
            if silences_after > args.extra_silence:
                outcome = "TIMEOUT"
                break
        if user.strip():
            senior_spoke = True
        history.append(USER_PREFIX + (user if user.strip() else NO_RESPONSE))
        transcript.append({"role": "user", "text": user or "(silence)"})

    expected = scenario["expected_outcome"].strip().lower()
    outcome_ok = outcome == expected
    violations, warnings = ([], [])
    if outcome not in ("TIMEOUT", "ERROR"):
        senior_text = " ".join(t["text"] for t in transcript if t["role"] == "user")
        violations, warnings = check_goodbye(final_text, outcome, senior_spoke, senior_text)
        warnings += check_reason(final_text, scenario.get("category", ""))
    return {
        "scenario_id": scenario["id"],
        "category": scenario.get("category", ""),
        "run": run_idx,
        "expected": expected,
        "outcome": outcome,
        "outcome_ok": outcome_ok,
        "goodbye": final_text,
        "goodbye_ok": outcome not in ("TIMEOUT", "ERROR") and not violations,
        "violations": violations,
        "warnings": warnings,
        "passed": outcome_ok and outcome not in ("TIMEOUT", "ERROR") and not violations,
        "latencies_ms": latencies,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "transcript": transcript,
    }


def pct(values, q):
    if not values:
        return 0
    s = sorted(values)
    return s[min(len(s) - 1, int(round(q / 100 * (len(s) - 1))))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True, help="file under data/prompts")
    ap.add_argument("--inputs", default="inputs_ks831.json", help="file under data/inputs")
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--temperature", type=float, default=None, help="omit to match production")
    ap.add_argument("--reasoning-effort", default=None)
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-turns", type=int, default=10)
    ap.add_argument("--extra-silence", type=int, default=2)
    ap.add_argument("--only", default=None, help="comma-separated scenario ids")
    ap.add_argument("--label", required=True)
    ap.add_argument("--dry-run", action="store_true", help="no API call: count conversations, estimate cost")
    ap.add_argument("--key-fingerprint", default=None, help="must match the fingerprint of the key in .env")
    ap.add_argument("--language", default="en", choices=sorted(LANGS), help="which words the goodbye checker uses")
    args = ap.parse_args()
    set_language(args.language)

    template = (ROOT / "data/prompts" / args.prompt).read_text(encoding="utf-8")
    assert "@@HISTORY@@" in template, "prompt must be rendered with the @@HISTORY@@ placeholder"
    scenarios = json.loads((ROOT / "data/inputs" / args.inputs).read_text(encoding="utf-8"))["scenarios"]
    if args.only:
        keep = set(args.only.split(","))
        scenarios = [s for s in scenarios if s["id"] in keep]

    jobs = [(s, i) for s in scenarios for i in range(args.runs)]
    print(f"{args.label}: {len(scenarios)} scenarios x {args.runs} runs = {len(jobs)} conversations "
          f"({args.model}, temperature={args.temperature}, prompt={args.prompt})")
    print(f"Estimated cost: ~${estimate_cost(template, scenarios, args):.2f} "
          f"(list price, ~4 chars/token, assistant turns = senior turns + 1)")
    if args.dry_run:
        return
    client = openai.OpenAI(api_key=dev_key(args.key_fingerprint))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda j: run_one(client, args, template, *j), jobs))

    out_dir = ROOT / "experiments" / "ks831" / args.label
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"label": args.label, "date": datetime.now().isoformat(timespec="seconds"),
            "model": args.model, "temperature": args.temperature,
            "reasoning_effort": args.reasoning_effort, "prompt": args.prompt,
            "inputs": args.inputs, "runs": args.runs, "language": args.language}
    (out_dir / "results.json").write_text(json.dumps({"meta": meta, "results": results}, indent=1,
                                                     ensure_ascii=False), encoding="utf-8")
    write_summary(out_dir, meta, results)


def fingerprint(key):
    return hashlib.sha256(key.encode()).hexdigest()[:10]


def dev_key(expected_fp):
    """The dev key, or exit. Never prints the key itself."""
    load_dotenv(ROOT / ".env")
    var = "OPENAI_DEV_API_KEY" if os.environ.get("OPENAI_DEV_API_KEY") else "OPENAI_API_KEY"
    key = os.environ.get(var, "").strip().strip('"')
    if not key:
        sys.exit("No OPENAI_DEV_API_KEY / OPENAI_API_KEY in .env")
    fp = fingerprint(key)
    if fp in BLOCKED_KEY_FINGERPRINTS:
        sys.exit(f"REFUSED: {var} in .env is the {BLOCKED_KEY_FINGERPRINTS[fp]} ({fp}), not the dev key.")
    if expected_fp != fp:
        sys.exit(f"{var} in .env has fingerprint {fp}. If that is your dev key, re-run with "
                 f"--key-fingerprint {fp}")
    print(f"Using {var} (fingerprint {fp})")
    return key


def estimate_cost(template, scenarios, args):
    price_in, price_out = PRICES.get(args.model, PRICES["gpt-4o"])
    prompt_tokens = len(template) / 4
    total = 0.0
    for s in scenarios:
        calls = min(len(s["user_turns"]) + 1, args.max_turns)
        # each call re-sends the prompt plus the history so far (~40 tokens per exchange)
        tokens_in = sum(prompt_tokens + 40 * i for i in range(calls))
        total += (tokens_in * price_in + calls * 60 * price_out) / 1e6
    return total * args.runs


def cost_of(results, model):
    price_in, price_out = PRICES.get(model, PRICES["gpt-4o"])
    return sum(r["tokens_in"] * price_in + r["tokens_out"] * price_out for r in results) / 1e6


def write_summary(out_dir, meta, results):
    lat = [ms for r in results for ms in r["latencies_ms"]]
    n = len(results)
    lines = [f"# KS-831 eval: {meta['label']}", "",
             f"{meta['date']} | {meta['model']} | temperature={meta['temperature']} | "
             f"prompt={meta['prompt']} | inputs={meta['inputs']} | runs={meta['runs']}", "",
             "| Pass (both) | Outcome | Goodbye | p50 ms | p95 ms | Errors | Cost |", "|---|---|---|---|---|---|---|",
             f"| {sum(r['passed'] for r in results)}/{n} ({100 * sum(r['passed'] for r in results) / n:.0f}%) "
             f"| {100 * sum(r['outcome_ok'] for r in results) / n:.0f}% "
             f"| {100 * sum(r['goodbye_ok'] for r in results) / n:.0f}% "
             f"| {pct(lat, 50):.0f} | {pct(lat, 95):.0f} "
             f"| {sum(r['outcome'] == 'ERROR' for r in results)} | ${cost_of(results, meta['model']):.2f} |", "",
             "## By scenario", "", "| Scenario | Pass | Outcome ok | Goodbye ok | Outcomes seen |",
             "|---|---|---|---|---|"]
    by = {}
    for r in results:
        by.setdefault(r["scenario_id"], []).append(r)
    for sid, rs in by.items():
        seen = {}
        for r in rs:
            seen[r["outcome"]] = seen.get(r["outcome"], 0) + 1
        lines.append(f"| {sid} | {sum(r['passed'] for r in rs)}/{len(rs)} | "
                     f"{sum(r['outcome_ok'] for r in rs)}/{len(rs)} | {sum(r['goodbye_ok'] for r in rs)}/{len(rs)} | "
                     + ", ".join(f"{k} x{v}" for k, v in seen.items()) + " |")
    viol = {}
    for r in results:
        for v in r["violations"]:
            key = v.split(":")[0] if v.startswith(("invites", "promise")) else re.sub(r"^\d+ ", "N ", v)
            viol[key] = viol.get(key, 0) + 1
    lines += ["", "## Goodbye violations", ""] + [f"- {k}: {v}" for k, v in
                                                  sorted(viol.items(), key=lambda x: -x[1])]
    warns = sum(len(r["warnings"]) for r in results)
    wcount = {}
    for r in results:
        for w in r["warnings"]:
            wcount[w] = wcount.get(w, 0) + 1
    lines += ["", f"## Warnings ({warns})", ""] + [f"- {k}: {v}" for k, v in sorted(wcount.items(), key=lambda x: -x[1])]
    lines += ["",
              "## Failing goodbyes", ""]
    for r in results:
        if not r["passed"]:
            lines.append(f"- `{r['scenario_id']}#{r['run']}` [{r['outcome']}] {r['goodbye']!r} "
                         f"-> {'; '.join(r['violations']) or 'wrong outcome'}")
    lines += ["", "## Sample passing goodbyes", ""]
    shown = set()
    for r in results:
        if r["passed"] and r["scenario_id"] not in shown:
            shown.add(r["scenario_id"])
            lines.append(f"- `{r['scenario_id']}` [{r['outcome']}] {r['goodbye']!r}")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:6 + 2]))
    print(f"Summary: {out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
