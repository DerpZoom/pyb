"""Day 9 — learn by example path from pathlib and file I/O: atomic safe writes and globbing."""

from pathlib import Path  # import "Path" class

# Folder for today's logs, anchored next to THIS file (not the cwd).
# 1 ->  Path(__file__) : (typecast) wraps the running script's filepath (the string in __file__) into a Path object, so you can use pathlib's methods on it.
#       __file__ : the module-level variable Python automatically sets to the path of the current .py file
# 2 ->  .resolve() : turns a path into its canonical absolute form — it makes the path absolute and eliminates any indirection (., .., symlinks),
#       giving you the one true path to the actual location on disk.

LOG_DIR = Path(__file__).resolve().parent / "logs"  # LOG_DIR ends up as Path("/home/jon/project/logs").

print(f"__file__\t\t= {__file__}")
print (f"Type(__file__)\t\t= {type(__file__)}")
print("-"*150)
print(f"Path(__file__)\t\t= {Path(__file__)}")
print(f"Type(Path(__file__))\t= {type(Path(__file__))}")
print("-"*150)
print(f"Path(__file__).resolve()= {Path(__file__).resolve()}")
print(f"Type(Path(__file__).resolve())= {type(Path(__file__).resolve())}")
print("-"*150)
print(f"LOG_DIR\t\t\t= {LOG_DIR}")
print(f"Type(LOG_DIR)\t\t= {type(LOG_DIR)}")
print("-"*150)

# Sensor readings to persist, as (tag, value) pairs.  In a real system these would come from a sensor API.
READINGS = [
    ("PT-101", 4.2),
    ("PT-102", 12.7),
    ("FT-200", 8.9),
]

print("/n")
print("-"*150)
print(f"READINGS\t\t= {READINGS}")
print(f"Type(READINGS)\t\t= {type(READINGS)}")
print("-"*150)
print(f"READINGS[0]\t\t= {READINGS[0]}")
print(f"Type(READINGS[0])\t= {type(READINGS[0])}") 
print("-"*150)
print(f"READINGS[0][0]\t\t= {READINGS[0][0]}")
print(f"Type(READINGS[0][0])\t= {type(READINGS[0][0])}") 
print("-"*150) 
print(f"READINGS[0][1]\t\t= {READINGS[0][1]}")
print(f"Type(READINGS[0][1])\t= {type(READINGS[0][1])}") 
print("-"*150)
print(f"READINGS[1][0]\t\t= {READINGS[1][0]}")
print(f"Type(READINGS[1][0])\t= {type(READINGS[1][0])}") 
print("-"*150) 
print(f"READINGS[1][1]\t\t= {READINGS[1][1]}")
print(f"Type(READINGS[1][1])\t= {type(READINGS[1][1])}") 
print("-"*150)

def safe_write(path: Path, text: str) -> None:
    """Write text to path atomically: fill a temp file, then swap it in."""


    # path = log_file = Path("/home/jon/project/logs/readings.log")
    # 1 ->  path.parent — the directory holding the file, not the file itself:
    # 2 ->  path.parent.mkdir(...) — creates that directory.
    # 3 ->  parents=True — create any missing intermediate directories too. If /home/jon/project exists but logs doesn't, that's fine.
    #       If none of project/logs exist, it builds the whole chain.
    # 4 ->  exist_ok=True — don't complain if the directory already exists. Without it, mkdir raises FileExistsError when the folder is already there.
    # 5     With it, an existing directory is silently accepted.
    path.parent.mkdir(parents=True, exist_ok=True)

    # This computes a temporary filename right next to the target file, by taking the original path and tacking .tmp onto its extension.
    # 1 ->  path.suffix — the file's extension, including the dot.
    # 2 ->  path.suffix + ".tmp" — the original extension plus .tmp, e.g. ".log.tmp".
    # 3 ->  path.with_suffix(...) — replace the original extension with the new one,
    #       so readings.log becomes readings.log.tmp, and readings.txt becomes readings.txt.tmp.
    tmp = path.with_suffix(path.suffix + ".tmp")    # sibling temp file


    # 1 ->  This is the "fill the temp file" half of the atomic-write pattern,
    #       done with a with block so the file is properly closed no matter what.
    #       Otherwise you would have to use try/finally to ensure the file is closed even if an exception occurs.
    # 2 ->  Path.open() is pathlib's version of the built-in open() — it opens the file and returns a file object you can write to.
    # 3 ->  "w" — write mode: creates the file if it doesn't exist, and truncates (empties) it if it does. That's fine here since tmp is a throwaway.
    # 4 ->  encoding="utf-8" — always name an encoding when writing text files, so you don't get platform-dependent behavior. 
    # 5 ->  with ... as f: This is a context manager.
    #       The with block guarantees the file is flushed and closed when the block exits — whether it exits normally or because an exception was raised inside it. 
    # --- build phase: path is untouched, still the old version ---
    with tmp.open("w", encoding="utf-8") as f:      # always name an encoding
        f.write(text)                               # write into the TEMP file
        # tmp is now complete and closed

    # This is the atomic swap — the final step that makes the temp file become the target file, in one indivisible operation.
    # What it does: tmp (the fully-written temporary file) is renamed over path (the target).
    # After this line, path contains the new content and tmp no longer exists — it is path now.
    # An atomic swap (more precisely, an atomic operation) is an operation that, from the perspective of any observer, either happens completely or not at all
    # — there is no observable in-between state where it's "half done."
    # "Atomic" comes from the Greek atomos, "indivisible." 
    # The operation can't be split or caught mid-execution: at any instant you look, you see the state before it or the state after it, never a partial blend of the two.
    # --- swap phase: instant, atomic ---
    tmp.replace(path)


def build_report() -> str:
    """Turn the readings into one newline-terminated block of text."""

    # List comprehension: for each (tag, value) pair in READINGS, make a string "tag,value" and collect them all into a list.
    # list comprehension —> a compact syntax for building a list by transforming or filtering an existing iterable, all in one expression.
    rows = [f"{tag},{value}" for tag, value in READINGS]
    
    print(f"rows\t\t\t= {rows}")
    print(f"Type(rows)\t\t= {type(rows)}")
    print("-"*150)
    print(f"rows[0]\t\t\t= {rows[0]}")
    print(f"Type(rows[0])\t\t= {type(rows[0])}")
    print("-"*150)
    print(f"rows[1]\t\t\t= {rows[1]}")
    print(f"Type(rows[1])\t\t= {type(rows[1])}")
    print("-"*150)  
    return "\n".join(rows) + "\n"                  # trailing newline = POSIX-clean


def main() -> None:
    log_file = LOG_DIR / "readings.log"       # / joins path parts safely, log_file ends up as Path("/home/jon/project/logs/readings.log")
    safe_write(log_file, build_report())      # persist atomically


    # This loops over every .log file in LOG_DIR, reads each one, and prints its name alongside how many lines it contains.
    # Going through it:
    # LOG_DIR.glob("*.log") — finds all files ending in .log directly inside LOG_DIR (not recursive — that'd be rglob). Returns a generator of Path objects.
    # sorted(...) — glob returns files in arbitrary, filesystem-dependent order, so sorted() wraps it to give a stable, predictable sequence.
    # for found in ... — each iteration, found is one Path pointing at a log file.
    for found in sorted(LOG_DIR.glob("*.log")):
        # found.read_text(encoding="utf-8") — reads the entire file into a single string and closes it, all in one call.
        # The comment is exactly right: this is shorthand for the full with open(...) as f: f.read() dance. i.e. open("app.log", "r", encoding="utf-8")
        # Naming encoding="utf-8" here is the same good habit as before — it makes decoding consistent across platforms rather than relying on a system default.
        contents = found.read_text(encoding="utf-8")
        # Why splitlines() rather than contents.count("\n")? splitlines() is more robust: it handles a final line that has no trailing newline (counts it anyway),
        # and it recognizes \r\n and \r line endings too — so a file written on Windows counts correctly.
        # count("\n") would miss an unterminated last line and mishandle \r-only endings.
        print(f"{found.name}: {len(contents.splitlines())} readings")


if __name__ == "__main__":
    main()