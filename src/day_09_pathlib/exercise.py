"""Day 9 — pathlib and file I/O: atomic safe writes and globbing."""
 
from pathlib import Path            # modern, OS-agnostic filesystem API
 
# Folder for today's logs, anchored next to THIS file (not the cwd).
# resolve() makes it absolute so the script works from any directory.
LOG_DIR = Path(__file__).resolve().parent / "logs" # LOG_DIR ends up as Path("/home/jon/project/logs").
 
READINGS = [                       # (tag, value) pairs to persist
    ("PT-101", 4.2),
    ("PT-102", 12.7),
    ("FT-200", 8.9),
]

def safe_write(path: Path, text: str) -> None:
    """Write text to path atomically: fill a temp file, then swap it in."""
    path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
    tmp = path.with_suffix(path.suffix + ".tmp")    # sibling temp file
    # 'with' flushes and closes the file even if the write raises partway.
    with tmp.open("w", encoding="utf-8") as f:      # always name an encoding
        f.write(text)                               # write into the TEMP file
    # The swap is the point: an OS-level rename on one filesystem is atomic,
    # so readers see the whole old file or the whole new one, never a torn write.
    tmp.replace(path)                                   # atomically replace path
 
 
def build_report() -> str:
    """Turn the readings into one newline-terminated block of text."""
    rows = [f"{tag},{value}" for tag, value in READINGS]  # simple CSV-ish rows
    return "\n".join(rows) + "\n"                  # trailing newline = POSIX-clean
 
 
def main() -> None:
    log_file = LOG_DIR / "readings.log"             # / joins path parts safely
    safe_write(log_file, build_report())            # persist atomically
    # glob finds files by pattern; here every .log in the folder.
    for found in sorted(LOG_DIR.glob("*.log")):
        # read_text is a one-liner for open-read-all-close.
        contents = found.read_text(encoding="utf-8")
        print(f"{found.name}: {len(contents.splitlines())} readings")
 

if __name__ == "__main__":
    main()