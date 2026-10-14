#!/usr/bin/env python3
"""
KS-831: render the fall prompt from the real Java of a grandappflutter ref, optionally with a
candidate patch applied, so the lab tests exactly what the server would send. Free: no API calls.

    python tools/ks831/render_ks831.py --label baseline
    python tools/ks831/render_ks831.py --label candidate_v1 --patch tools/ks831/candidate_v1.patch --compare-with baseline

Writes every prompt (each ContextType x en-US/he-IL/pt-PT) to experiments/ks831/rendered/<label>/ and
the fall prompts to data/prompts/prompt_ks831_<label>[_he|_pt].txt (the file ks831_eval.py --prompt takes).
--compare-with checks that every OTHER prompt is byte-identical to that label's (Hebrew, Portuguese and
medication must not change in KS-831) and prints which ones differ.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
SRC_DIR = "picmeinserver/DddSmartConversation/src"
PKG = "com/ddd/services/smartconversation"
GSON = "picmeinserver/libs_all/libs/thrdParties/json/gson-2.11.0.jar"
FALL_EN = "DISTRESS_FALL_DETECTED_en-US.txt"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--repo", default=str(Path.home() / "Desktop" / "grandappflutter"))
    ap.add_argument("--ref", default="origin/a475i")
    ap.add_argument("--patch", default=None, help="diff -ruN patch against <ref>'s src/ (a/ b/ prefixes)")
    ap.add_argument("--senior-name", default="Jake")
    ap.add_argument("--compare-with", default=None, help="label rendered earlier")
    ap.add_argument("--expect-changed", default=FALL_EN,
                    help="comma-separated prompt files allowed to differ from --compare-with")
    args = ap.parse_args()

    repo = Path(args.repo)
    commit = git(repo, "rev-parse", "--short", args.ref).decode().strip()
    out = LAB / "experiments" / "ks831" / "rendered" / args.label
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "src"
        files = git(repo, "ls-tree", "-r", "--name-only", args.ref, f"{SRC_DIR}/{PKG}/context").decode().split()
        files += [f"{SRC_DIR}/{PKG}/AssistantResponse.java", f"{SRC_DIR}/{PKG}/ConversationOutcome.java"]
        for f in files:
            dest = src / f[len(SRC_DIR) + 1:]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(git(repo, "show", f"{args.ref}:{f}"))
        if args.patch:
            subprocess.run(["patch", "-p1", "-s", "-d", str(src), "-i", str(Path(args.patch).resolve())], check=True)
        shutil.copy(Path(__file__).parent / "RenderAll.java", src / "RenderAll.java")
        classes = tmp / "classes"
        cp = str(repo / GSON)
        java_files = [str(p) for p in src.rglob("*.java")]
        subprocess.run(["javac", "-nowarn", "-encoding", "UTF-8", "-cp", cp, "-d", str(classes), *java_files], check=True)
        if out.exists():
            shutil.rmtree(out)
        sep = ";" if sys.platform == "win32" else ":"
        # The Java prints a debug line per context; keep it out of the console.
        subprocess.run(["java", "-cp", f"{classes}{sep}{cp}", "RenderAll", str(out), args.senior_name],
                       check=True, stdout=subprocess.DEVNULL)

    (out / "SOURCE.txt").write_text(f"ref={args.ref} ({commit})\npatch={args.patch}\nseniorName={args.senior_name}\n",
                                    encoding="utf-8")
    target = LAB / "data" / "prompts" / f"prompt_ks831_{args.label}.txt"
    shutil.copy(out / FALL_EN, target)
    # KS-831 covers every language: the Hebrew and Portuguese fall prompts go next to the English one.
    for code, suffix in (("he-IL", "he"), ("pt-PT", "pt")):
        shutil.copy(out / f"DISTRESS_FALL_DETECTED_{code}.txt",
                    LAB / "data" / "prompts" / f"prompt_ks831_{args.label}_{suffix}.txt")
    rendered = sorted(p.name for p in out.glob("*.txt") if p.name != "SOURCE.txt")
    print(f"{args.label}: {len(rendered)} prompts from {args.ref} ({commit})"
          f"{' + ' + args.patch if args.patch else ''} -> {out}")
    print(f"Fall prompts -> {target.relative_to(LAB)} (+ _he, _pt)")

    if args.compare_with:
        other = LAB / "experiments" / "ks831" / "rendered" / args.compare_with
        changed = [n for n in rendered if (other / n).read_bytes() != (out / n).read_bytes()]
        missing = [n for n in rendered if not (other / n).exists()]
        print(f"vs {args.compare_with}: changed = {changed or 'none'}" + (f", missing = {missing}" if missing else ""))
        allowed = set(args.expect_changed.split(","))
        unexpected = [n for n in changed if n not in allowed]
        if unexpected:
            print(f"UNEXPECTED: prompts outside --expect-changed changed: {unexpected}")
            sys.exit(1)


if __name__ == "__main__":
    main()
