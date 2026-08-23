"""Day 7 — Consolidation I: week-1 integrative exercise.

Folds the week together — f-strings (incl. f"{x=}"), enumerate/zip/
unpacking, comprehensions, dict/set methods, and *args + keyword-only
arguments — into one small commissioning-report tool. No new concepts.
"""

# Parallel data straight off a commissioning sheet: names and readings.
TAG_NAMES = ["TT_101", "PT_102", "FT_103", "LT_104", "TT_105"]
READINGS  = [72.4, 118.9, 55.0, 32.5, 210.7]  # engineering units


def build_reading_map(names, values):
    """Pair each tag name with its reading, using zip + a comprehension."""
    # zip() walks both lists in lockstep; unpacking names each (name, value).
    # Fill the ??? with a dict comprehension mapping name -> value.
    return {name: value for name, value in zip(names, values)}


def flag_out_of_range(reading_map, *, low, high):
    """Return the SET of tag names whose reading is outside [low, high].

    low/high are keyword-only (note the bare * in the signature) so a caller
    can never swap the two bounds by position — a Day-4 habit worth keeping.
    """
    # Set comprehension: dedupes for free and gives O(1) membership later.
    return {name for name, value in reading_map.items()
            if not (low <= value <= high)}


def summarize(reading_map, *labels, low=0.0, high=200.0):
    """Print a numbered commissioning summary.

    *labels soaks up any optional section headers passed positionally; the
    defaults are plain floats, never a list/dict, so we sidestep the
    mutable-default trap from Day 4.
    """
    for header in labels:                 # zero or more optional headers
        print(f"== {header} ==")
    bad = flag_out_of_range(reading_map, low=low, high=high)
    # enumerate() gives a 1-based index for a human-readable list.
    for i, (name, value) in enumerate(reading_map.items(), start=1):
        status = "OUT" if name in bad else "ok"   # set membership, O(1)
        print(f"{i:>2}. {name:<8} {value:>7.1f}  [{status}]")
    # f"{x=}" prints the expression AND its value — the Day-2 debug idiom.
    print(f"{len(bad)=}")


def main():
    readings = build_reading_map(TAG_NAMES, READINGS)
    # assert is plain Python: a wrong ??? fails loudly instead of silently.
    assert readings["PT_102"] == 118.9, "map should pair names to readings"
    summarize(readings, "Week-1 Commissioning Check", low=40.0, high=150.0)


if __name__ == "__main__":
    main()
