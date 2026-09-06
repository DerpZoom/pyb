"""Day 10 — CSV and JSON fluency — DictReader, json round-trips, and config files."""

import csv
import json
from pathlib import Path
from collections import defaultdict

# Folder this script lives in, so we can find the CSV and JSON files relative to it 
HERE = Path(__file__).parent

CSV_PATH = HERE / "readings.csv"    # CSV file is in the same folder as this script
JSON_PATH = HERE / "summary.json"   # JSON file will be created in the same folder as this script



def load_good_readings(path: Path) -> list[dict]:

    # [] is a list display — literal syntax that constructs a new list object. Empty, length zero.
    # Identical in effect to list(), though [] is marginally faster since it's a single BUILD_LIST opcode rather than a name lookup and call.
    # Use [].
    rows = []

    # newline="" lets the csv module handle line endings itself
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)        # first line becomes the keys
        for row in reader:  # # <-- continue jumps back HERE
            # skip bad quality or empty value cells
            if row["quality"] != "GOOD" or not row["value"]:
                continue    # <-- skips the two lines below
            row["value"] = float(row["value"])   # CSV gives strings
            rows.append(row)
    return rows


def summarise(rows: list[dict]) -> dict[str, float]:
    buckets = defaultdict(list)
    for row in rows:
        buckets[row["tag"]].append(row["value"])
    # average each tag's readings, rounded to 2 dp
    return {tag: round(sum(v) / len(v), 2) for tag, v in buckets.items()}


def main() -> None:
    summary = summarise(load_good_readings(CSV_PATH))

    # write pretty, indented JSON so a human can read the file
    # 1 ->  Path.open() is just a wrapper around builtin open().
    #       Mode "w" truncates the file to zero length first, so this is a full rewrite each run, not an append.
    # 2 ->  json.dump() serializes the dict to JSON and writes it to the file.  
    #       The indent=2 argument makes the JSON human-readable with 2-space indentation.
    #       json.dump (no s) writes directly to the file object rather than building the whole string in memory.
    #       indent=2 triggers pretty-printing: newlines between elements, two spaces of nesting per level.
    #       Without it you get one long line.
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    
    # read it straight back to prove the round-trip is lossless
    with JSON_PATH.open(encoding="utf-8") as f:
        reloaded = json.loads(f.read())          # <-- deserialize the JSON file here
 
    assert reloaded == summary, "round-trip changed the data!"
    print("Round-trip OK")
    print(summary)


if __name__ == "__main__":
    main()
