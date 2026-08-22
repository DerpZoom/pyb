"""Day 6 — Claude Code as study partner.

Scans the pyb repo for completed day folders and prints a ready-to-paste
prompt you can hand to Claude Code to quiz yourself on the week's material.
"""
import argparse                                # stdlib CLI parser (previewed before Day 17)
from pathlib import Path                       # pathlib gives clean, OS-safe paths

# Resolve src/ relative to THIS file, not the shell's working directory,
# so the script works no matter where you launch it from.
SRC = Path(__file__).resolve().parents[1]      # .../pyb/src

def completed_days(topic: str | None = None) -> list[str]:
    """Return sorted topic slugs for every day_NN_* folder under src/.

    If `topic` is given, keep only slugs containing that keyword
    (case-insensitive substring match).
    """
    # glob() returns paths in arbitrary OS order, so we sort for a stable list.
    folders = sorted(SRC.glob("day_[0-9][0-9]_*"))  # match only day folders, e.g. day_04_function_audit
    slugs = [f.name for f in folders if f.is_dir()]
    if topic:
        key = topic.lower()
        slugs = [s for s in slugs if key in s.lower()]
    return slugs

def build_quiz_prompt(days: list[str]) -> str:
    """Assemble a single Claude Code prompt from the day slugs."""
    topics = "\n".join(f"  - {slug}" for slug in days)   # one bullet per day
    return (
        "You are my Python study partner. Quiz me on these completed "
        "lessons, one question at a time, waiting for my answer before "
        f"revealing the next:\n{topics}"
    )

def parse_args() -> argparse.Namespace:
    """Parse command-line flags."""
    parser = argparse.ArgumentParser(
        description="Generate a Claude Code quiz prompt from completed day folders."
    )
    parser.add_argument(
        "--topic",
        help="Only include day slugs containing this keyword (e.g. 'git').",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    days = completed_days(args.topic)
    if args.topic:
        print(f"Found {len(days)} completed day folder(s) matching {args.topic!r}.")
    else:
        print(f"Found {len(days)} completed day folder(s).")
    print(f"Expecting Claude Code to ask {len(days)} question(s).")
    print("-" * 60)
    print(build_quiz_prompt(days))             # paste this into Claude Code

if __name__ == "__main__":
    main()