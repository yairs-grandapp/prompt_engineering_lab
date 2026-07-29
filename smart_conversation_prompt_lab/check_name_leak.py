#!/usr/bin/env python3
"""
Check whether the assistant spoke a name it was not supposed to speak.

For shared or common-area devices there is no single senior, and the caller
supplies a placeholder such as "Shared Activity Resident". The assistant must
address the senior without any name at all — it must neither read the
placeholder aloud nor invent a name of its own.

This reads an experiment's generated transcripts and classifies every assistant
turn:

  exact     the forbidden name appears verbatim
  partial   a distinctive word from the forbidden name appears on its own
  invented  the assistant addressed the senior by some other name

Usage:
    python check_name_leak.py experiments/exp_012_shared_activity_no_name \\
        --forbidden-name "Shared Activity Resident"

Exits non-zero if any leak is found, so it can gate a run.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

OUTPUTS_SUBDIR = "outputs"
ASSISTANT_ROLE = "assistant"

# Function words carry no identifying force, so a hit on one of them is not
# evidence that the placeholder leaked. Everything else in the forbidden name
# is distinctive: "Resident" on its own still tells the senior they are being
# addressed by a label rather than a name.
GENERIC_NAME_WORDS: Set[str] = {
    "a", "an", "the", "of", "for", "and", "to", "in",
}

# Vocative forms: an address term followed by the name the assistant chose to
# use. Anything captured here is a name the assistant put in the senior's face.
#
# The greeting alternation is case-insensitive via a scoped (?i:...) group, NOT
# via re.IGNORECASE on the whole pattern. Real assistant text capitalises
# greetings ("Hello Margaret"), so a case-sensitive alternation never fires and
# the check silently passes everything. But a global IGNORECASE would also make
# the [A-Z] capture match lowercase, turning "Hello, this is your care
# assistant" into a reported invented name. Only the greeting may vary in case;
# the captured name must stay capitalised.
VOCATIVE_PATTERN = re.compile(
    r"\b(?i:hello|hi|hey|dear|greetings|good\s+morning|good\s+afternoon|good\s+evening)"
    r"[\s,]+"
    r"([A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*)",
)

# Capitalised words that routinely follow a greeting without being a name.
NON_NAME_CAPITALISED: Set[str] = {
    "I", "I'm", "It", "It's", "This", "There", "Are", "Can", "Please",
    "How", "Is", "We", "You", "Your", "Just", "And", "If", "Help", "Stay",
    "The", "My", "Sorry", "Oh", "So", "That", "What", "Do", "Did", "Have",
}


def distinctive_words(name: str) -> List[str]:
    """Words from the forbidden name that would identify it on their own."""
    return [
        word for word in re.findall(r"[A-Za-z']+", name)
        if word.lower() not in GENERIC_NAME_WORDS
    ]


def find_exact(text: str, name: str) -> bool:
    """True if the forbidden name appears verbatim, ignoring case and spacing."""
    pattern = r"\s+".join(re.escape(part) for part in name.split())
    return re.search(pattern, text, re.IGNORECASE) is not None


def find_partial(text: str, name: str) -> List[str]:
    """Distinctive words from the forbidden name that appear on their own."""
    hits = []
    for word in distinctive_words(name):
        if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
            hits.append(word)
    return hits


def find_invented(text: str, allowed: Set[str]) -> List[str]:
    """Names the assistant used in a vocative position that it was not given."""
    hits = []
    for match in VOCATIVE_PATTERN.finditer(text):
        candidate = match.group(1).strip()
        first = candidate.split()[0]
        if first in NON_NAME_CAPITALISED:
            continue
        if candidate.lower() in allowed or first.lower() in allowed:
            continue
        hits.append(candidate)
    return hits


def assistant_turns(output: Dict[str, Any]) -> Iterator[Tuple[str, int, str]]:
    """Yield (model_name, turn_number, text) for every assistant turn."""
    for model_name, result in output.get("model_results", {}).items():
        for entry in result.get("transcript", []):
            if entry.get("role") == ASSISTANT_ROLE:
                text = entry.get("text") or ""
                if text.strip():
                    yield model_name, entry.get("turn", 0), text


def load_outputs(experiment_dir: Path) -> List[Dict[str, Any]]:
    outputs_dir = experiment_dir / OUTPUTS_SUBDIR
    if not outputs_dir.is_dir():
        raise SystemExit(f"No outputs directory at {outputs_dir}")
    paths = sorted(outputs_dir.glob("*.json"))
    if not paths:
        raise SystemExit(f"No transcripts found in {outputs_dir}")
    return [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def known_name_words(*names: Optional[str]) -> Set[str]:
    """
    Every word already accounted for by another category.

    Used to keep the invented-name check honest: a vocative hit on the permitted
    name is correct behaviour, and a hit on the forbidden name is already counted
    as an exact leak. Only a name from neither source is genuinely invented.
    """
    words: Set[str] = set()
    for name in names:
        if not name:
            continue
        words.add(name.lower())
        words.update(word.lower() for word in re.findall(r"[A-Za-z']+", name))
    return words


def analyse(
    outputs: List[Dict[str, Any]],
    forbidden_name: str,
    expected_name: Optional[str],
) -> Tuple[List[Dict[str, Any]], Counter]:
    allowed = known_name_words(expected_name, forbidden_name)
    rows = []
    totals: Counter = Counter()

    for output in outputs:
        exact_turns, partial_hits, invented_hits = [], [], []
        spoke_expected = False
        for _model, turn, text in assistant_turns(output):
            if find_exact(text, forbidden_name):
                exact_turns.append(turn)
            partial_hits.extend(find_partial(text, forbidden_name))
            invented_hits.extend(find_invented(text, allowed))
            if expected_name and find_exact(text, expected_name):
                spoke_expected = True

        rows.append({
            "scenario_id": output.get("scenario_id", "?"),
            "scenario_name": output.get("scenario_name", ""),
            "exact": len(exact_turns),
            "partial": sorted(set(partial_hits)),
            "invented": sorted(set(invented_hits)),
            "spoke_expected": spoke_expected,
        })
        totals["exact"] += len(exact_turns)
        totals["partial"] += len(partial_hits)
        totals["invented"] += len(invented_hits)
        totals["spoke_expected"] += int(spoke_expected)
        if exact_turns or partial_hits or invented_hits:
            totals["scenarios_leaking"] += 1

    return rows, totals


def report(rows: List[Dict[str, Any]], totals: Counter, args: argparse.Namespace) -> None:
    print(f"\nExperiment:      {args.experiment_dir}")
    print(f"Forbidden name:  {args.forbidden_name!r}")
    if args.expected_name:
        print(f"Permitted name:  {args.expected_name!r}")
    print(f"Scenarios:       {len(rows)}\n")

    name_column = f" {'said name':<10}" if args.expected_name else ""
    header = f"{'scenario':<16} {'exact':>6} {'partial':<24} {'invented':<24}{name_column}"
    print(header)
    print("-" * len(header))
    for row in rows:
        partial = ", ".join(row["partial"]) or "-"
        invented = ", ".join(row["invented"]) or "-"
        said = f" {'yes' if row['spoke_expected'] else 'NO':<10}" if args.expected_name else ""
        print(f"{row['scenario_id']:<16} {row['exact']:>6} {partial:<24} {invented:<24}{said}")

    print()
    print(f"TOTAL exact hits:        {totals['exact']}")
    print(f"TOTAL partial hits:      {totals['partial']}")
    print(f"TOTAL invented names:    {totals['invented']}")
    print(f"Scenarios with any leak: {totals['scenarios_leaking']}/{len(rows)}")
    if args.expected_name:
        print(f"Spoke {args.expected_name!r}:          "
              f"{totals['spoke_expected']}/{len(rows)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("experiment_dir", type=Path,
                        help="experiment directory containing outputs/")
    parser.add_argument("--forbidden-name", required=True,
                        help="the name the assistant must never speak")
    parser.add_argument("--expected-name", default=None,
                        help="a name the assistant IS allowed to use, if any "
                             "(suppresses invented-name hits for it)")
    args = parser.parse_args()

    outputs = load_outputs(args.experiment_dir)
    rows, totals = analyse(outputs, args.forbidden_name, args.expected_name)
    report(rows, totals, args)

    leaked = totals["exact"] + totals["partial"] + totals["invented"]
    print(f"\nRESULT: {'LEAK DETECTED' if leaked else 'CLEAN'}")
    return 1 if leaked else 0


if __name__ == "__main__":
    sys.exit(main())
