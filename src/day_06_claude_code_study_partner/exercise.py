"""Day 6 — Claude Code as study partner.
 
Scans the pyb repo for completed day folders and prints a ready-to-paste
prompt you can hand to Claude Code to quiz yourself on the week's material.
"""
from pathlib import Path                       # pathlib gives clean, OS-safe paths
 
# Resolve src/ relative to THIS file, not the shell's working directory,
# so the script works no matter where you launch it from.
SRC = Path(__file__).resolve().parents[1]      # .../pyb/src
 
def completed_days() -> list[str]:
    """Return sorted topic slugs for every day_NN_* folder under src/."""
    # glob() returns paths in arbitrary OS order, so we sort for a stable list.
    folders = sorted(SRC.glob("day_[0-9][0-9]_*"))  # match only day folders, e.g. day_04_function_audit
    # folder.name is like "day_04_function_audit"; keep the whole slug.
    return [f.name for f in folders if f.is_dir()]
 
def build_quiz_prompt(days: list[str]) -> str:
    """Assemble a single Claude Code prompt from the day slugs."""
    topics = "\n".join(f"  - {slug}" for slug in days)   # one bullet per day
    return (
        "You are my Python study partner. Quiz me on these completed "
        "lessons, one question at a time, waiting for my answer before "
        f"revealing the next:\n{topics}"
    )
 
def main() -> None:
    days = completed_days()
    print(f"Found {len(days)} completed day folder(s).")
    print("-" * 60)
    print(build_quiz_prompt(days))             # paste this into Claude Code
 
if __name__ == "__main__":
    main()
