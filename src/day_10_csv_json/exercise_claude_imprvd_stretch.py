"""Day 10 — Claude improved version of CSV and JSON fluency — DictReader, json round-trips, and config files. Stretch goal"""

import csv                          # CSV reading — DictReader gives one dict per row
import json                         # JSON serialization
import logging                      # Structured, level-based output to stderr
import os                           # os.fdopen / os.replace / os.fsync for the atomic write
import tempfile                     # mkstemp — safe temp file for the atomic write
from pathlib import Path            # Filesystem paths
from collections import defaultdict # Grouping readings by tag

log = logging.getLogger(__name__)

# Folder this script lives in, so we can find the CSV and JSON files relative to it.
# __file__ resolves against the SCRIPT, not the current working directory, so this works
# whether you run `python script.py`, `python subdir/script.py`, or from a scheduler with
# an arbitrary CWD. A bare "readings.csv" would break in the last two cases.
HERE = Path(__file__).parent

CSV_PATH = HERE / "readings.csv"    # CSV file is in the same folder as this script
JSON_PATH = HERE / "summary.json"   # JSON file will be created in the same folder as this script
CONFIG_PATH = HERE / "config.json"  # Editable settings — behaviour without code changes

def load_good_readings(path: Path) -> list[dict]:
    """Parse the CSV, keep only GOOD rows with a usable numeric value."""

    # [] is a list display — literal syntax that constructs a new list object. Empty, length zero.
    # Identical in effect to list(), though [] is marginally faster since it's a single BUILD_LIST
    # opcode rather than a name lookup and call. Use [].
    # It has to be created before the loop, and outside it: initialise inside and you reset on every
    # iteration. It also guarantees we return a list even when nothing matches, instead of raising
    # UnboundLocalError on an empty file.
    rows = []

    # newline="" disables Python's universal-newline translation and hands raw bytes to the csv
    # parser. The csv module tracks quote state itself, so it knows a newline inside a quoted field
    # is data, not a record separator — but only if the file layer hasn't already rewritten \r\n
    # to \n behind its back. Always pass this when opening a file for csv.
    #
    # utf-8-sig (not plain utf-8) because we did NOT create this file. Anything exported from Excel
    # or a historian may carry a UTF-8 BOM, which would glue \ufeff onto the first header name and
    # make the column check below fail against a header that looks correct in an editor.
    # utf-8-sig strips a BOM if present and behaves identically if not.
    with path.open(newline="", encoding="utf-8-sig") as f:

        # DictReader consumes the first row as field names and yields one dict per data row instead
        # of a positional list. Note it never raises on a malformed row: a short row gets None for
        # the missing fields, a long row dumps the extras into a list under key None. A broken CSV
        # parses "successfully" and the problem surfaces somewhere downstream.
        reader = csv.DictReader(f)

        # Fail fast on a header mismatch. Without this, a renamed or misspelled column produces
        # KeyError: 'quality' from inside the loop, which tells you the key is missing but not that
        # the header said "Quality". Set difference gives us exactly which ones are absent.
        # `or []` guards the empty-file case, where fieldnames is None.
        # 
        missing = {"tag", "quality", "value"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path.name}: missing columns {sorted(missing)}")

        for row in reader:

            # Guard clause: continue jumps to the top of this for loop and pulls the next row,
            # skipping the rest of the body. Rejecting early keeps the real work at one indent
            # level instead of nesting it three deep inside an if.
            #
            # .strip().upper() because exports are inconsistent — "Good", "GOOD", trailing spaces.
            # Exact-match on "GOOD" alone silently drops every row when the source changes format,
            # and because the condition REJECTS on mismatch, that failure is quiet: you get an empty
            # summary rather than an error. `or ""` handles the None that DictReader supplies for a
            # short row, which would otherwise blow up on .strip().
            if (row["quality"] or "").strip().upper() != "GOOD":
                continue

            # Same None guard, plus strip. A whitespace-only cell is empty for our purposes, and
            # catching it here means it never reaches float() and never logs a warning — a blank
            # cell isn't an anomaly worth a log line, an unparseable one is.
            raw = (row["value"] or "").strip()
            if not raw:
                continue

            # float() raises ValueError on everything a real export throws at you: "N/A", "---",
            # "#VALUE!", "1,750.5" with a thousands separator, "12.5 psi" with units. Without this
            # try, one bad cell in row 4000 kills the entire run with a traceback that doesn't say
            # which row. reader.line_num is the physical line in the file (header included), which
            # is what you need to actually go and look at it. %r shows quotes and escapes so you can
            # tell "  " from "" from "N/A" — %s would render whitespace as an invisible gap.
            try:
                value = float(raw)
            except ValueError:
                log.warning("%s:%d unparseable value %r", path.name, reader.line_num, raw)
                continue

            # float() happily accepts the literal strings "nan" and "inf" — they parse without
            # error. NaN is not valid JSON, and json.dump(allow_nan=False) downstream would abort
            # the whole write. Catching it here means we know the line number and can drop one row
            # instead of losing the run. `value != value` is true only for NaN, by IEEE 754.
            if value != value:
                log.warning("%s:%d NaN value", path.name, reader.line_num)
                continue

            # Build a fresh dict rather than mutating and appending `row`. Mutating is safe —
            # DictReader creates a new dict each iteration, so there's no aliasing — but `row`
            # carries every column in the file, including `quality` (now always "GOOD", so dead
            # weight) and whatever else the historian decided to add this month. An explicit dict
            # states the contract: downstream code gets tag and value, nothing else.
            rows.append({"tag": row["tag"], "value": value})

    return rows


def summarise(rows: list[dict]) -> dict[str, dict]:
    """Group readings by tag and compute per-tag statistics."""

    # defaultdict(list) calls list() automatically the first time a key is touched, so
    # buckets[tag].append(...) works without an `if tag not in buckets` dance. The factory only
    # fires on a genuine miss — an existing key behaves exactly like a normal dict.
    buckets = defaultdict(list)
    for row in rows:
        buckets[row["tag"]].append(row["value"])

    summary = {}
    for tag, values in buckets.items():

        # No ZeroDivisionError guard is needed: a bucket only comes into existence because
        # something was appended to it, so len(values) >= 1 always. That's a property of
        # defaultdict, not luck, but it isn't obvious to someone reading this cold.
        #
        # count is the field that makes the rest meaningful — a mean over 2 samples and a mean
        # over 4000 are not the same claim, and without it you can't distinguish "this tag is
        # healthy" from "this tag was almost entirely filtered out as BAD upstream".
        #
        # round() is round-half-to-EVEN (round(0.5) is 0, round(1.5) is 2) and operates on the
        # binary float, so round(2.675, 2) gives 2.67. Fine for a monitoring average; reach for
        # Decimal instead if a number ever has to be exact.
        #
        # min/max stay unrounded on purpose — those are actual observed readings, and rounding
        # them would misreport the extreme. They're what tells you whether the mean is hiding
        # a spike.
        summary[tag] = {
            "count": len(values),
            "mean": round(sum(values) / len(values), 2),
            "min": min(values),
            "max": max(values),
        }

    # Returning `summary` (a plain dict) rather than `buckets` matters for the round-trip: a
    # defaultdict serialises to JSON fine but comes back as a plain dict, so the factory is
    # silently lost. Building a new dict keeps the declared return type honest.
    log.info("summarised %d readings across %d tags", len(rows), len(summary))
    return summary


def write_json_atomic(path: Path, obj) -> None:
    """Write obj as JSON to path. Readers never see a partial file."""
    # dir=path.parent puts the temp file on the SAME filesystem as the target.
    # os.replace is only atomic within one filesystem; across a mount boundary
    # it degrades to copy-then-delete and the guarantee is gone.
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        # mkstemp returns a raw OS descriptor; fdopen wraps it so json.dump
        # can use it and it gets closed properly. Don't open(tmp) instead —
        # that leaks this descriptor.
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            # allow_nan=False: bare NaN/Infinity are NOT valid JSON. Python
            # would write and re-read them happily, so the assert in main()
            # would pass while the file broke every non-Python consumer.
            json.dump(obj, f, indent=2, sort_keys=True, allow_nan=False)
            f.write("\n")
            f.flush()          # out of Python's buffer
            os.fsync(f.fileno())   # out of the OS cache, onto disk
        os.replace(tmp, path)  # atomic on POSIX and Windows; unlike os.rename,
                               # doesn't fail when the destination exists
    except BaseException:
        # BaseException, not Exception, so Ctrl-C also cleans up the temp file.
        Path(tmp).unlink(missing_ok=True)
        raise


def load_config(path: Path) -> dict:
    """Load runtime settings from JSON, falling back to defaults if absent."""

    # Defaults live in code so the script runs on a fresh checkout with no config file.
    # The config file overrides them; it doesn't replace them. That means adding a new
    # setting later won't KeyError on someone's older config.
    defaults = {"warn_above": 50.0}

    if not path.exists():
        log.info("%s not found — using defaults %r", path.name, defaults)
        return defaults

    # No BOM handling here: unlike readings.csv, we own this file. If a BOM ever did
    # appear (someone edited it in Notepad), json.load raises rather than silently
    # mangling it, which is the failure we want.
    try:
        with path.open(encoding="utf-8") as f:
            user = json.load(f)
    except json.JSONDecodeError as e:
        # A typo in the config is a config error, not a crash with a raw traceback.
        # e.lineno/e.colno point at the offending character so it's actually fixable.
        raise ValueError(f"{path.name}:{e.lineno}:{e.colno}: invalid JSON — {e.msg}") from e

    # A JSON file whose top level is a list or a number parses fine but isn't a config.
    if not isinstance(user, dict):
        raise ValueError(f"{path.name}: expected a JSON object, got {type(user).__name__}")

    # Merge, don't replace. Unknown keys are kept and warned about rather than dropped —
    # a typo'd "warn_abov" should be visible, not silently ignored.
    unknown = set(user) - set(defaults)
    if unknown:
        log.warning("%s: unrecognised settings %s", path.name, sorted(unknown))

    config = {**defaults, **user}

    # Validate the type here, once, rather than letting a string threshold blow up
    # mid-comparison later with "'>' not supported between str and float".
    if not isinstance(config["warn_above"], (int, float)) or isinstance(config["warn_above"], bool):
        raise ValueError(
            f"{path.name}: warn_above must be a number, got {config['warn_above']!r}"
        )

    return config

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Load config first, before doing any work. If it's malformed we want to fail
    # immediately rather than after parsing 4000 CSV rows.
    config = load_config(CONFIG_PATH)
    warn_above = config["warn_above"]

    rows = load_good_readings(CSV_PATH)
    if not rows:
        log.warning("%s: no good readings found", CSV_PATH.name)
    summary = summarise(rows)

    write_json_atomic(JSON_PATH, summary)

    # Threshold check. sorted() so the warnings come out in a stable order between runs —
    # dict order follows insertion (i.e. CSV order), which changes when the source changes.
    for tag, stats in sorted(summary.items()):
        if stats["mean"] > warn_above:
            log.warning(
                "%s mean %.2f exceeds warn_above %.2f (n=%d, max=%.2f)",
                tag, stats["mean"], warn_above, stats["count"], stats["max"],
            )

    with JSON_PATH.open(encoding="utf-8") as f:
        reloaded = json.load(f)

    assert reloaded == summary, "round-trip changed the data!"
    print("Round-trip OK")
    print(json.dumps(summary, indent=2, sort_keys=True))
    

if __name__ == "__main__":
    main()