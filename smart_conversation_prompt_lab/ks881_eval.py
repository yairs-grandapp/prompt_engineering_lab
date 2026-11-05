#!/usr/bin/env python3
"""
KS-881: score the fall prompt against the KS-881 functional requirements (FR v3) and technical
requirements, turn by turn.

What it checks on every run, on top of the KS-831 goodbye rules (ks831_eval.check_goodbye):
  - the final outcome (confirmed fall / assistance requested / unable to verify / no response / no fall);
  - WHEN the call closes: the closing must come right after senior answer number `close_after`.
    Closing earlier means Vega skipped its one re-ask or the confirming question; closing later means
    it asked again when it should have acted. This is the check the KS-831 runner could not make;
  - speech during a no-fall goodbye (`after_close`): the senior's words are added after the goodbye
    and the turn is evaluated again, as the server does (KS-739). Help asked there must raise the alert.

Pass rate (KS-881 TR v3): every wording of every scenario runs --runs times (5) and must pass every
run. Scenarios marked `pending` (behaviour owned by another ticket) are reported but do not gate.

Inputs: data/inputs/inputs_ks881_<lang>.json, built by tools/ks881/build_inputs.py.
Prompts: data/prompts/prompt_ks881_<label>_<lang>[_unknown].txt, from tools/ks881/render_ks881.py.

KEY SAFETY and cost: as ks831_eval (dev key only, --key-fingerprint must match, --dry-run is free).

    python ks881_eval.py --prompt-label v2 --language en --runs 5 --label v2_en_r5 --dry-run
    python ks881_eval.py --prompt-label v2 --language en --runs 5 --label v2_en_r5 --key-fingerprint <fp>
"""
import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import openai

import ks831_eval as k

ROOT = Path(__file__).parent
ASSISTANCE = "distress_assistance_requested"
UNABLE = "distress_unable_to_verify"
OUTCOMES = {k.FALL_CONFIRMED, ASSISTANCE, UNABLE, k.NO_RESPONSE_OUTCOME, k.NO_FALL}
# The goodbye checker requires the alert phrase on every alerting outcome; KS-881 adds two.
k.ALERT_OUTCOMES.update({ASSISTANCE, UNABLE})
# The goodbye may say "I'm sorry you fell" to a senior who said it in other words; KS-831 only knew
# "fell". The lists are the KS-881 prompt's own fall wordings (WHICH ALERT).
k.LANGS["en"]["senior_fell"] = re.compile(
    r"\b(fell|fall|fallen|tumble|went down|slipped|slip|tripped|on the floor|off the floor|collapsed|rolled off"
    r"|up by myself|myself up|got back up|get back up)\b")
k.LANGS["pt"]["senior_fell"] = re.compile(r"ca[ií]|queda|\bqi\b|\bti\b|k í|kí|escorreg|no chão")
k.LANGS["he"]["senior_fell"] = re.compile(r"נפל|החלק|על הרצפה")
# ks831_eval.check_reason's categories, by expected outcome.
REASON_CATEGORY = {UNABLE: "unclear", k.FALL_CONFIRMED: "fell", ASSISTANCE: "help"}

# KS-876 (delivered by KS-881): Portuguese closings end word for word on their agreed sentences
# (PortuguesePack.closingSentences), so the KS-831 "Adeus" / alert-phrase checks do not apply in pt.
PT_ALERT = ("Estou a enviar um alerta a quem lhe pode prestar ajuda. Vou terminar a chamada agora para dar "
            "seguimento ao alerta. Obrigada por falar comigo.")
PT_ENDINGS = {
    k.FALL_CONFIRMED: [PT_ALERT],
    ASSISTANCE: [PT_ALERT],
    UNABLE: ["Desculpe, não consegui perceber o que disse. A sua segurança é a minha prioridade, por isso "
             "estou a enviar um alerta a quem lhe pode prestar ajuda. Vou terminar a chamada agora para dar "
             "seguimento ao alerta. Obrigada por falar comigo."],
    k.NO_RESPONSE_OUTCOME: ["Não tive resposta sua e a sua segurança é a minha prioridade, por isso estou a "
                            "enviar um alerta no sistema SeniorMatics. Até breve."],
    # RenderKs881 renders with currentTime 18:39, so FAREWELL NOW names the afternoon farewell.
    k.NO_FALL: ["Tenha uma boa tarde. Até breve!",
                "Obrigada por partilhar comigo como se sente. Quando quiser, podemos voltar a conversar."],
}


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def check_pt_closing(text, outcome):
    """KS-876: the closing ends on an agreed sentence, asks nothing and is at most 4 sentences."""
    violations = []
    if not any(_norm(text).endswith(_norm(e)) for e in PT_ENDINGS.get(outcome, [])):
        violations.append("does not end on the agreed Portuguese closing")
    if "?" in text:
        violations.append("question")
    if len(k.sentences(k.normalise(text))) > 4:
        violations.append("more than 4 sentences")
    if k.LANG["could_not_reach"].search(_norm(text)):
        violations.append("could-not-reach")
    return violations, []


def check_closing(text, outcome, senior_spoke, senior_text, language):
    if language == "pt":
        return check_pt_closing(text, outcome)
    return k.check_goodbye(text, outcome, senior_spoke, senior_text)


def cost_of(results, model):
    """List-price cost, with cached input at the cached price."""
    price_in, price_out = k.PRICES.get(model, k.PRICES["gpt-4o"])
    price_cached = CACHED_PRICE.get(model, price_in)
    total = 0.0
    for r in results:
        cached = r.get("tokens_cached", 0)
        total += (r["tokens_in"] - cached) * price_in + cached * price_cached + r["tokens_out"] * price_out
    return total / 1e6


def load_jobs(inputs, only, include_pending, wordings=None):
    jobs = []
    for s in inputs["scenarios"]:
        if only and s["id"] not in only:
            continue
        if s.get("pending") and not include_pending:
            continue
        for i, p in enumerate(s["phrasings"]):
            if wordings and f"{s['id']}/{p.get('id', f'p{i + 1}')}" not in wordings:
                continue
            jobs.append({
                "scenario": s["id"],
                "phrasing": p.get("id", f"p{i + 1}"),
                "situation": s.get("situation", ""),
                "prompt": s.get("prompt", "named"),
                "turns": p["turns"],
                "expected": p.get("expected_outcome", s["expected_outcome"]),
                "also_accepted": p.get("also_accepted", s.get("also_accepted", [])),
                "close_after": p.get("close_after", s.get("close_after")),
                "after_close": p.get("after_close", s.get("after_close")),
                "pending": s.get("pending"),
                "assistance_flag": p.get("assistance_flag", s.get("assistance_flag", False)),
                "no_flag": s.get("no_flag", False),
                "source": p.get("source", ""),
            })
    return jobs


# Cached input (a repeated prompt prefix of 1024+ tokens) is billed at half the input price for gpt-4o.
CACHED_PRICE = {"gpt-4o": 1.25, "gpt-5.4-mini": 0.075, "gpt-5.4-nano": 0.02, "gpt-6-sol": 0.20, "gpt-5.6-terra": 0.20,
                "gpt-6.1-terra": 0.05}


SPLIT = "@@SPLIT@@"


def messages_for(model, prompt):
    """KS-881 caching: the messages production sends. A prompt rendered with @@SPLIT@@ goes as the fixed
    instructions (a developer message; system for gpt-4/3 models, as OpenAiApiRequest.instructionsRole) and
    then the input; an older single-part prompt as one user message."""
    if SPLIT not in prompt:
        return [{"role": "user", "content": prompt}]
    instructions, user = (x.strip() for x in prompt.split(SPLIT, 1))
    role = "system" if model.startswith(("gpt-4", "gpt-3")) else "developer"
    return [{"role": role, "content": instructions}, {"role": "user", "content": user}]


def call_llm(client, model, prompt, temperature, reasoning_effort):
    """The request ks831_eval.call_llm sends (production's shape), plus the cached-token count, and a
    longer wait on the per-minute token limit: the first KS-881 run lost 22 of 211 conversations to
    429s after ks831_eval's 2 / 4 / 8 s retries. Returns (parsed, ms, tokens_in, tokens_out, cached)."""
    kwargs = dict(model=model, messages=messages_for(model, prompt),
                  response_format={"type": "json_object"})
    if temperature is not None:
        kwargs["temperature"] = temperature
    if reasoning_effort:
        kwargs["reasoning_effort"] = reasoning_effort
    for attempt in range(6):
        start = time.perf_counter()
        try:
            r = client.chat.completions.create(**kwargs)
            break
        except openai.RateLimitError as e:
            # An empty account also answers 429; retrying it only stalls the run.
            if attempt == 5 or "insufficient_quota" in str(e) or "no credits" in str(e):
                raise
            # 2026-11-02: a run sat silent for 50 minutes; every wait is now visible.
            print(f"  429 rate limit, waiting {20 * (attempt + 1)} s ({str(e)[:120]})", flush=True)
            time.sleep(20 * (attempt + 1))
        except (openai.APIConnectionError, openai.APITimeoutError, openai.InternalServerError) as e:
            if attempt == 5:
                raise
            print(f"  {type(e).__name__}, retrying in {2 ** attempt * 2} s", flush=True)
            time.sleep(2 ** attempt * 2)
    ms = (time.perf_counter() - start) * 1000
    details = getattr(r.usage, "prompt_tokens_details", None)
    cached = (getattr(details, "cached_tokens", 0) or 0) if details else 0
    return (json.loads(r.choices[0].message.content), ms, r.usage.prompt_tokens, r.usage.completion_tokens,
            cached)


LANG_CODES = {"en": "en-US", "pt": "pt-PT", "he": "he-IL"}


def server_check(checks, history, out):
    """KS-881 (2026-11-03): what the server's ContextDistressFallDetected.enforceTurnLimit does to a reply, with
    the stop turn and closings read from the real method (server_checks_ks881_<label>.json). Returns
    (outcome, text, reason) when the server would replace the reply, else None."""
    if not checks:
        return None
    senior = [h for h in history if h.startswith(k.USER_PREFIX)]
    spoke = any(h != k.USER_PREFIX + k.NO_RESPONSE for h in senior)
    if out == k.NO_RESPONSE_OUTCOME and spoke:
        return (checks["noResponseAfterSpeechBecomes"], checks["noResponseAfterSpeechClosing"],
                "no response although the senior spoke")
    if out == k.IN_PROGRESS and len(senior) >= checks["hardStopSeniorTurns"]:
        return ((checks["outcomeSpoke"], checks["closingSpoke"], "hard stop") if spoke
                else (checks["outcomeSilent"], checks["closingSilent"], "hard stop"))
    return None


def converse(client, args, template, history, transcript, turns, start_ui, totals):
    """Runs the conversation from `history` until a terminal outcome. Returns (outcome, text, answers)."""
    ui = start_ui
    silences_after = 0
    for _ in range(args.max_turns):
        prompt = template.replace("@@HISTORY@@", "\n".join(history)).strip()
        try:
            parsed, ms, ti, to, cached = call_llm(client, args.model, prompt, args.temperature,
                                                  args.reasoning_effort)
        except Exception as e:  # noqa: BLE001 - recorded, not fatal to the batch
            transcript.append({"role": "error", "text": str(e)})
            return "ERROR", "", ui
        totals["latencies"].append(ms)
        totals["in"] += ti
        totals["out"] += to
        totals["cached"] += cached
        text = parsed.get("text", "")
        out = str(parsed.get("conversationOutcome", k.IN_PROGRESS)).strip().lower()
        override = server_check(args.server_checks, history, out)
        if override:
            model_said = {"outcome": out, "text": text}
            out, text, why = override
        history.append(k.ASSISTANT_PREFIX + text)
        # KS-881: the server reads the flag only as true (a boolean or the string "true").
        flag = str(parsed.get("assistanceRequested", "")).strip().lower() == "true"
        transcript.append({"role": "assistant", "text": text, "outcome": out, "after_answers": ui,
                           "assistance_requested": flag})
        if override:
            transcript[-1]["server_override"] = why
            transcript[-1]["model_said"] = model_said
        if out != k.IN_PROGRESS:
            return out, text, ui
        if ui < len(turns):
            user = turns[ui]
            ui += 1
        else:
            # The script ran out: the senior goes quiet. Counted as answers, so a call that keeps
            # asking shows up as closing late rather than as a timeout.
            user = ""
            ui += 1
            silences_after += 1
            if silences_after > args.extra_silence:
                return "TIMEOUT", "", ui
        history.append(k.USER_PREFIX + (user if user.strip() else k.NO_RESPONSE))
        transcript.append({"role": "user", "text": user or "(silence)"})
    return "TIMEOUT", "", ui


def run_one(client, args, templates, job, run_idx):
    template = templates[job["prompt"]]
    history, transcript = [], []
    totals = {"latencies": [], "in": 0, "out": 0, "cached": 0}
    turns = job["turns"]
    outcome, final_text, answers = converse(client, args, template, history, transcript, turns, 0, totals)

    violations, warnings = [], []
    accepted = {job["expected"], *job["also_accepted"]}
    outcome_ok = outcome in accepted
    if not outcome_ok:
        violations.append(f"outcome {outcome}, expected {job['expected']}")
    allowed = job["close_after"] if isinstance(job["close_after"], list) else [job["close_after"]]
    if job["close_after"] is not None and outcome not in ("ERROR", "TIMEOUT") and answers not in allowed:
        violations.append(
            f"closed after {answers} answer(s), expected {job['close_after']}"
            + (" (closed early: skipped the re-ask or the confirming question)" if answers < min(allowed)
               else " (asked again instead of closing)"))
    if outcome in OUTCOMES:
        senior_text = " ".join(t["text"] for t in transcript if t["role"] == "user")
        senior_spoke = any(t.strip() for t in turns[:answers])
        v, w = check_closing(final_text, outcome, senior_spoke, senior_text, args.language)
        # KS-881 v7 (P3): a misheard fall word ("I well down") IS the senior saying they fell, so "I'm sorry
        # you fell" is right when the scenario is a fall; the KS-831 check only knows the literal words.
        if outcome == job["expected"] == k.FALL_CONFIRMED:
            v = [x for x in v if "never said so" not in x]
        violations += [f"goodbye: {x}" for x in v]
        warnings += w
        if outcome == job["expected"] and outcome in REASON_CATEGORY and args.language != "pt":
            warnings += k.check_reason(final_text, REASON_CATEGORY[outcome])
        # KS-881 (NUN-1626, yuvalo 45082): a fall with a help request carries assistanceRequested.
        last = next((t for t in reversed(transcript) if t["role"] == "assistant"), {})
        if outcome == k.FALL_CONFIRMED and job["assistance_flag"] and not last.get("assistance_requested"):
            violations.append("assistanceRequested missing on a fall with a help request")
        # 2 Nov v7 review (B3): a fall with no help signal must not carry the flag either.
        if outcome == k.FALL_CONFIRMED and job.get("no_flag") and last.get("assistance_requested"):
            violations.append("assistanceRequested set on a fall with no help signal")
    elif outcome not in ("ERROR", "TIMEOUT"):
        violations.append(f"unknown outcome '{outcome}'")

    # KS-739 / KS-881: the senior speaks over a no-fall goodbye. The server re-evaluates the turn
    # with their words after the goodbye; an alert must follow if they asked for help.
    after = job["after_close"]
    re_outcome = None
    if after and outcome == k.NO_FALL and not violations:
        history.append(k.USER_PREFIX + after["text"])
        transcript.append({"role": "user", "text": after["text"], "during_goodbye": True})
        re_outcome, re_text, _ = converse(client, args, template, history, transcript, [], 0, totals)
        if re_outcome != after["expected_outcome"]:
            violations.append(f"speech during the goodbye: outcome {re_outcome}, expected {after['expected_outcome']}")
        elif re_outcome in OUTCOMES:
            v, w = check_closing(re_text, re_outcome, True, after["text"], args.language)
            violations += [f"re-evaluated goodbye: {x}" for x in v]
            warnings += w

    return {**{key: job[key] for key in ("scenario", "phrasing", "situation", "prompt", "expected",
                                          "close_after", "pending", "source")},
            "run": run_idx, "outcome": outcome, "answers_before_close": answers, "re_outcome": re_outcome,
            "passed": not violations, "violations": violations, "warnings": warnings,
            "goodbye": final_text, "latencies_ms": totals["latencies"],
            "tokens_in": totals["in"], "tokens_out": totals["out"], "tokens_cached": totals["cached"],
            "transcript": transcript}


def estimate_cost(templates, jobs, args):
    price_in, price_out = k.PRICES.get(args.model, k.PRICES["gpt-4o"])
    total = 0.0
    for j in jobs:
        prompt_tokens = len(templates[j["prompt"]]) / 4
        close = max(j["close_after"]) if isinstance(j["close_after"], list) else j["close_after"]
        calls = min((close or len(j["turns"])) + 1, args.max_turns) + (2 if j["after_close"] else 0)
        tokens_in = sum(prompt_tokens + 40 * i for i in range(calls))
        total += (tokens_in * price_in + calls * 60 * price_out) / 1e6
    return total * args.runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-label", required=True, help="the render_ks881.py label, e.g. v2")
    ap.add_argument("--language", default="en", choices=["en", "he", "pt"])
    ap.add_argument("--inputs", default=None, help="file under data/inputs (default inputs_ks881_<lang>.json)")
    ap.add_argument("--model", default="gpt-4o")
    # João, 2026-11-02: the KS-881 tests run at temperature 0. Production sends no temperature today
    # (OpenAI's default, 1.0), so pass --temperature -1 to test the production setting instead.
    ap.add_argument("--temperature", type=float, default=0.0,
                    help="default 0 (KS-881 tests); -1 = send none, as production does today")
    ap.add_argument("--reasoning-effort", default=None)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-turns", type=int, default=8)
    ap.add_argument("--extra-silence", type=int, default=2)
    ap.add_argument("--only", default=None, help="comma-separated scenario ids")
    ap.add_argument("--wordings-file", default=None,
                    help="file with one scenario/wording per line (e.g. still_unclear/w4): run only those")
    ap.add_argument("--include-pending", action="store_true", help="also run scenarios owned by another ticket")
    ap.add_argument("--label", required=True)
    ap.add_argument("--dry-run", action="store_true", help="no API call: count conversations, estimate cost")
    ap.add_argument("--key-fingerprint", default=None)
    ap.add_argument("--no-server-checks", action="store_true",
                    help="do not apply the server's hard stop and no-response override (KS-881)")
    args = ap.parse_args()
    if args.temperature is not None and args.temperature < 0:
        args.temperature = None
    k.set_language(args.language)

    templates = {}
    for kind, suffix in (("named", ""), ("unknown", "_unknown")):
        path = ROOT / "data/prompts" / f"prompt_ks881_{args.prompt_label}_{args.language}{suffix}.txt"
        templates[kind] = path.read_text(encoding="utf-8")
        assert "@@HISTORY@@" in templates[kind], f"{path.name} must be rendered with @@HISTORY@@"
    # KS-881 (2026-11-03): apply the server's own checks, as production does, unless --no-server-checks.
    args.server_checks = None
    if not args.no_server_checks:
        checks_path = ROOT / "data/prompts" / f"server_checks_ks881_{args.prompt_label}.json"
        assert checks_path.exists(), f"{checks_path.name} missing: re-render the label, or pass --no-server-checks"
        args.server_checks = json.loads(checks_path.read_text(encoding="utf-8"))[LANG_CODES[args.language]]
    inputs_name = args.inputs or f"inputs_ks881_{args.language}.json"
    inputs = json.loads((ROOT / "data/inputs" / inputs_name).read_text(encoding="utf-8"))
    only = set(args.only.split(",")) if args.only else None
    wordings = None
    if args.wordings_file:
        wordings = {ln.strip() for ln in Path(args.wordings_file).read_text(encoding="utf-8").splitlines()
                    if ln.strip() and not ln.startswith("#")}
    jobs = load_jobs(inputs, only, args.include_pending, wordings)
    if wordings:
        found = {f"{j['scenario']}/{j['phrasing']}" for j in jobs}
        assert found == wordings, f"not in the inputs: {sorted(wordings - found)}"
    runs = [(j, i) for j in jobs for i in range(args.runs)]
    n_scen = len({j["scenario"] for j in jobs})
    print(f"{args.label}: {n_scen} scenarios, {len(jobs)} wordings x {args.runs} runs = {len(runs)} conversations "
          f"({args.model}, temperature={args.temperature}, prompt={args.prompt_label}, {inputs_name}, "
          f"server checks {'on' if args.server_checks else 'off'})")
    print(f"Estimated cost: ~${estimate_cost(templates, jobs, args):.2f} (list price, ~4 chars/token)")
    if args.dry_run:
        return
    # A hung request fails after 60 s instead of the client's 10-minute default; retries are ours.
    client = openai.OpenAI(api_key=k.dev_key(args.key_fingerprint), timeout=60, max_retries=0)
    out_dir = ROOT / "experiments" / "ks881" / args.label
    out_dir.mkdir(parents=True, exist_ok=True)
    # Each conversation is saved as it finishes, so a stopped run keeps what it paid for.
    partial = out_dir / "results.partial.jsonl"
    results = []
    started = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool, partial.open("w", encoding="utf-8") as sink:
        futures = [pool.submit(run_one, client, args, templates, *r) for r in runs]
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            sink.write(json.dumps(r, ensure_ascii=False) + "\n")
            sink.flush()
            print(f"[{len(results)}/{len(runs)} {time.time() - started:.0f}s] {r['scenario']}/{r['phrasing']}"
                  f"#{r['run']}: {'PASS' if r['passed'] else 'FAIL'} {r['outcome']}@{r['answers_before_close']}",
                  flush=True)

    meta = {"label": args.label, "date": datetime.now().isoformat(timespec="seconds"), "model": args.model,
            "temperature": args.temperature, "reasoning_effort": args.reasoning_effort,
            "server_checks": bool(args.server_checks),
            "prompt_label": args.prompt_label, "language": args.language, "inputs": inputs_name, "runs": args.runs}
    (out_dir / "results.json").write_text(json.dumps({"meta": meta, "results": results}, indent=1,
                                                     ensure_ascii=False), encoding="utf-8")
    write_summary(out_dir, meta, results)


def write_summary(out_dir, meta, results):
    gating = [r for r in results if not r["pending"]]
    by_wording = {}
    for r in results:
        by_wording.setdefault((r["scenario"], r["phrasing"]), []).append(r)
    gate_words = {key: rs for key, rs in by_wording.items() if not rs[0]["pending"]}
    words_ok = sum(all(r["passed"] for r in rs) for rs in gate_words.values())
    lat = [ms for r in results for ms in r["latencies_ms"]]
    verdict = "PASS" if words_ok == len(gate_words) else "FAIL"
    lines = [f"# KS-881 eval: {meta['label']} — {verdict}", "",
             f"{meta['date']} | {meta['model']} | temperature={meta['temperature']} | prompt={meta['prompt_label']} "
             f"| {meta['language']} | {meta['inputs']} | runs={meta['runs']}", "",
             "Pass rule (KS-881 TR v3): every wording passes every run.", "",
             "| Wordings passing every run | Runs passed | p50 ms | p95 ms | Errors | Cost |",
             "|---|---|---|---|---|---|",
             f"| {words_ok}/{len(gate_words)} | {sum(r['passed'] for r in gating)}/{len(gating)} "
             f"| {k.pct(lat, 50):.0f} | {k.pct(lat, 95):.0f} | {sum(r['outcome'] == 'ERROR' for r in results)} "
             f"| ${cost_of(results, meta['model']):.2f} |", "",
             f"Cost: list price, cached input at the cached price "
             f"({sum(r.get('tokens_cached', 0) for r in results)} of {sum(r['tokens_in'] for r in results)} "
             f"input tokens cached).", "",
             "## By scenario", "", "| Scenario | Situation | Expected | Wordings passing | Runs passed | Outcomes seen |",
             "|---|---|---|---|---|---|"]
    by_scen = {}
    for (sid, _), rs in by_wording.items():
        by_scen.setdefault(sid, []).append(rs)
    for sid, groups in by_scen.items():
        flat = [r for g in groups for r in g]
        seen = {}
        for r in flat:
            key = f"{r['outcome']}@{r['answers_before_close']}"
            seen[key] = seen.get(key, 0) + 1
        tag = f" (pending {flat[0]['pending']})" if flat[0]["pending"] else ""
        lines.append(f"| {sid}{tag} | {flat[0]['situation']} | {flat[0]['expected']}@{flat[0]['close_after']} "
                     f"| {sum(all(r['passed'] for r in g) for g in groups)}/{len(groups)} "
                     f"| {sum(r['passed'] for r in flat)}/{len(flat)} | "
                     + ", ".join(f"{key} x{v}" for key, v in sorted(seen.items())) + " |")
    lines += ["", "`outcome@N` = the outcome and the number of senior answers before the call closed.", "",
              "## Failures", ""]
    for r in results:
        if not r["passed"]:
            said = " / ".join(t["text"] for t in r["transcript"] if t["role"] == "assistant")
            lines.append(f"- `{r['scenario']}/{r['phrasing']}#{r['run']}`{' (pending)' if r['pending'] else ''}: "
                         f"{'; '.join(r['violations'])} — Vega: {said!r}")
    warns = {}
    for r in results:
        for w in r["warnings"]:
            warns[w] = warns.get(w, 0) + 1
    lines += ["", "## Warnings", ""] + [f"- {w}: {n}" for w, n in sorted(warns.items(), key=lambda x: -x[1])]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:9]))
    print(f"Summary: {out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
