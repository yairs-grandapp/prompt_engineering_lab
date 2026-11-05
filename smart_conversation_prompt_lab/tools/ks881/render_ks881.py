#!/usr/bin/env python3
"""
KS-881: render the fall prompts from the real Java, so the lab tests exactly what the server sends.
Free: no API calls.

    python tools/ks881/render_ks881.py --label base --ref origin/a475i      # a git ref of grandappflutter
    python tools/ks881/render_ks881.py --label v2 --worktree                # the working tree (uncommitted)

Writes experiments/ks881/rendered/<label>/ and data/prompts/prompt_ks881_<label>_<lang>[_unknown].txt,
lang = en / he / pt; _unknown is the prompt for a call where nobody is identified (NUN-1592).
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
LANGS = {"en-US": "en", "he-IL": "he", "pt-PT": "pt"}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--family", default="FULL", choices=["FULL", "COMPACT"],
                    help="KS-881: the prompt family to render (COMPACT = gpt-6.1-terra)")
    ap.add_argument("--repo", default=str(Path.home() / "Desktop" / "grandappflutter"))
    src_group = ap.add_mutually_exclusive_group(required=True)
    src_group.add_argument("--ref", help="git ref of the repo, e.g. origin/a475i")
    src_group.add_argument("--worktree", action="store_true", help="the repo's working tree as it is now")
    args = ap.parse_args()

    repo = Path(args.repo)
    files = git(repo, "ls-files", f"{SRC_DIR}/{PKG}/context").decode().split()
    if args.worktree:
        # KS-881: new classes (FarewellMoment, ClosingSentences) are not committed yet.
        files += git(repo, "ls-files", "--others", "--exclude-standard", f"{SRC_DIR}/{PKG}/context").decode().split()
    files += [f"{SRC_DIR}/{PKG}/AssistantResponse.java", f"{SRC_DIR}/{PKG}/ConversationOutcome.java"]
    out = LAB / "experiments" / "ks881" / "rendered" / args.label
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "src"
        for f in files:
            dest = src / f[len(SRC_DIR) + 1:]
            dest.parent.mkdir(parents=True, exist_ok=True)
            if args.worktree:
                dest.write_bytes((repo / f).read_bytes())
            else:
                dest.write_bytes(git(repo, "show", f"{args.ref}:{f}"))
        shutil.copy(Path(__file__).parent / "RenderKs881.java", src / "RenderKs881.java")
        classes = tmp / "classes"
        cp = str(repo / GSON)
        java_files = [str(p) for p in src.rglob("*.java")]
        subprocess.run(["javac", "-nowarn", "-encoding", "UTF-8", "-cp", cp, "-d", str(classes), *java_files], check=True)
        if out.exists():
            shutil.rmtree(out)
        sep = ";" if sys.platform == "win32" else ":"
        subprocess.run(["java", "-cp", f"{classes}{sep}{cp}", "RenderKs881", str(out), args.family], check=True,
                       stdout=subprocess.DEVNULL)

    source = "worktree" if args.worktree else f"{args.ref} ({git(repo, 'rev-parse', '--short', args.ref).decode().strip()})"
    (out / "SOURCE.txt").write_text(f"source={source}\n", encoding="utf-8")
    for code, short in LANGS.items():
        for suffix in ("", "_unknown"):
            shutil.copy(out / f"DISTRESS_FALL_DETECTED_{code}{suffix}.txt",
                        LAB / "data" / "prompts" / f"prompt_ks881_{args.label}_{short}{suffix}.txt")
    # KS-881 (2026-11-03): the server's own checks, read from enforceTurnLimit, for ks881_eval.
    shutil.copy(out / "SERVER_CHECKS.json", LAB / "data" / "prompts" / f"server_checks_ks881_{args.label}.json")
    print(f"{args.label}: 6 fall prompts from {source} -> data/prompts/prompt_ks881_{args.label}_<en|he|pt>[_unknown].txt")


if __name__ == "__main__":
    main()
