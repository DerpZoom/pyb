"""Day 9 — learn by example path from pathlib and file I/O: atomic safe writes and globbing. Strectch version."""

import os
from pathlib import Path


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



    def main() -> None:
    # ... your existing main() body: writing logs, reading them back, etc. ...

    # --- housekeeping self-check: warn about any stray temp files ---
    leftovers = sorted(LOG_DIR.glob("*.tmp"))
    if leftovers:
        print(f"WARNING: {len(leftovers)} leftover temp file(s) in {LOG_DIR}:")
        for stray in leftovers:
            print(f"  - {stray.name}")
    else:
        print("Housekeeping OK: no leftover temp files.")