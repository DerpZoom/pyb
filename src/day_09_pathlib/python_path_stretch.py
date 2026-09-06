"""Day 9 — learn by example path from pathlib and file I/O: atomic safe writes and globbing. Stretch version."""

import os
from pathlib import Path

# Folder for today's logs, anchored next to THIS file (not the cwd).
# Same anchor as python_path.py: __file__ is where the code LIVES, so this
# resolves the same way whether you run it from the repo root, from home, or
# from a scheduler with an arbitrary working directory.
LOG_DIR = Path(__file__).resolve().parent / "logs"

# Sensor readings to persist, as (tag, value) pairs. In a real system these
# would come from a sensor API.
READINGS = [
    ("PT-101", 4.2),
    ("PT-102", 12.7),
    ("FT-200", 8.9),
]


def safe_write(path: Path, text: str) -> None:
    """Write text to path atomically: fill a temp file, then swap it in.

    Crash-proof against a partial temp file: the bytes are forced to disk
    with flush() + fsync() before the swap, so a power loss can't leave a
    renamed-but-empty file behind.
    """
    path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
    tmp = path.with_suffix(path.suffix + ".tmp")    # sibling temp file
    try:
        # 'with' flushes and closes the file even if the write raises partway.
        with tmp.open("w", encoding="utf-8") as f:  # always name an encoding
            f.write(text)                           # write into the TEMP file
            f.flush()                               # push Python's buffer to the OS
            os.fsync(f.fileno())                    # force the OS to write bytes to disk
        # The swap is the point: an OS-level rename on one filesystem is atomic,
        # so readers see the whole old file or the whole new one, never a torn write.
        tmp.replace(path)                           # atomically replace path
    except Exception:
        tmp.unlink(missing_ok=True)                 # don't leave a stray temp on failure
        raise


def build_report() -> str:
    """Turn the readings into one newline-terminated block of text."""
    rows = [f"{tag},{value}" for tag, value in READINGS]  # simple CSV-ish rows
    return "\n".join(rows) + "\n"                  # trailing newline = POSIX-clean


def main() -> None:
    log_file = LOG_DIR / "readings.log"       # / joins path parts safely
    safe_write(log_file, build_report())      # persist atomically

    # glob finds files by pattern; sorted() makes the order reproducible,
    # since glob itself returns them in arbitrary filesystem order.
    for found in sorted(LOG_DIR.glob("*.log")):
        contents = found.read_text(encoding="utf-8")
        # splitlines() counts an unterminated final line and understands
        # \r\n and bare \r; contents.count("\n") gets both of those wrong.
        print(f"{found.name}: {len(contents.splitlines())} readings")

    # --- housekeeping self-check: warn about any stray temp files ---
    # The try/except above deletes the temp on a failed write, but a hard kill
    # (SIGKILL, power cut) skips it entirely. This turns that silent leftover
    # into something actionable rather than a fix — it only reports.
    leftovers = sorted(LOG_DIR.glob("*.tmp"))
    if leftovers:
        print(f"WARNING: {len(leftovers)} leftover temp file(s) in {LOG_DIR}:")
        for stray in leftovers:
            print(f"  - {stray.name}")
    else:
        print("Housekeeping OK: no leftover temp files.")


if __name__ == "__main__":
    main()
