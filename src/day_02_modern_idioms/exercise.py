"""Day 02 — Modern idiom audit: f-strings, enumerate, zip, unpacking.
 
Run:  uv run python src/day_02_modern_idioms/exercise.py
"""
 
# A short commissioning snapshot: four analog tags and their live readings.
tags = ["TT-101", "PT-204", "FT-330", "LT-410"]   # tag names: temp, pressure, flow, level
readings = [72.4, 3.15, 128.7, 41.9]              # matching live process values
units = ["degC", "barg", "m3h", "pct"]            # engineering units, one per tag
 
 
def build_report() -> list[str]:
    """Return one formatted line per tag, e.g. '01  TT-101 = 72.4 degC'."""
    lines: list[str] = []   # list[str] : a type hint saying lines should be a list containing strings.
                            # Helps people and tools understand the intended contents, "[]" means emptylist
 
    # enumerate gives (index, item) pairs; start=1 so channels read 1..N.
    # We need the three parallel lists walked in lockstep as (tag, value, unit).
    for channel, (tag, value, unit) in enumerate(zip(tags, readings, units), start=1):
        # ':02d' zero-pads the channel number to two digits (01, 02, ...).
        lines.append(f"{channel:02d}  {tag} = {value} {unit}")
 
    return lines
 
 
def sanity_check() -> None:
    """Self-documenting f-string: f'{expr=}' prints the expression AND its value."""
    total = sum(readings)      # quick smoke test: add up the raw readings
    print(f"{total=}")         # prints  total=246.15  — name and value together
 
 
if __name__ == "__main__":
    for line in build_report():
        print(line)
    sanity_check()
