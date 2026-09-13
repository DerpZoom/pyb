"""Day 11 -- OOP audit I: when classes earn their keep."""

# Short version: it tells Python "don't actually evaluate the type hints in this file — just store them as text."
# After this line, Python stops evaluating annotations. It just keeps them as plain strings: "int" instead of the actual int object. Nothing looks anything up.
# Why you'd want that: it lets you reference types before the class body finishes.
# For example, if you have a class that references itself in a type hint, Python would normally throw an error because the class isn't fully defined yet.
# But with this future import, you can reference the class in its own type hints without any issues.
# class Node:
#    def next_node(self) -> Node:   # NameError! Node isn't finished being defined yet
from __future__ import annotations  # lets us reference types before the class body finishes
 
from dataclasses import dataclass
from datetime import datetime, timezone

class SensorReading:
    """A single reading from a field sensor -- this earns a class because it
    bundles related state (tag, value, unit, timestamp) with behavior that
    operates on that state (staleness checks)."""
 
    def __init__(self, tag: str, value: float, unit: str, timestamp: datetime) -> None:
        self.tag = tag              # e.g. "FT-101" -- the instrument tag
        self.value = value          # the measured value
        self.unit = unit            # e.g. "L/min"
        self.timestamp = timestamp  # when the reading was taken (UTC)

    # !r is a conversion flag inside an f-string. It says "don't use the friendly version of this value, use the debugging version."
    # The two ways Python turns things into text
    # Every Python object has two possible text forms:
    # 1 -> str() — the readable one, meant for humans reading output
    # 2 -> repr() — the precise one, meant for programmers debugging
    # repr keeps the quotes. That's the whole point — it shows you what you'd type to recreate the value.
 
    def __repr__(self) -> str:
        # __repr__ should be unambiguous -- ideally something you could
        # paste back into Python to recreate the object. This is for
        # developers, not operators, so show every field with !r.
        return (
            #f"Sensor(tag={self.tag}, value={self.value}, unit={self.unit}, timestamp={self.timestamp})"
            f"Sensor(tag={self.tag!r}, value={self.value!r}, unit={self.unit!r}, timestamp={self.timestamp!r})"
        )

    def is_stale(self, now: datetime, max_age_seconds: float) -> bool:
        # a reading is stale if more time than max_age_seconds has passed
        age = (now - self.timestamp).total_seconds()
        return age > max_age_seconds
 

# --- Preview: the @dataclass shortcut ---
# Everything above -- __init__ and a default __repr__ -- can be generated
# automatically if all you need are plain data fields. Compare:
 
@dataclass
class SensorReadingPreview:
    tag: str
    value: float
    unit: str
    timestamp: datetime
    # @dataclass writes __init__ and __repr__ for you from these type
    # annotations. It does NOT write is_stale -- custom behavior still
    # needs a real method, so dataclasses shine for data-holders, not
    # for objects carrying rich logic.
 
 
def main() -> None:
    now = datetime.now(timezone.utc)
    reading = SensorReading(tag="FT-101", value=42.7, unit="L/min", timestamp=now)
    print(reading)  # exercises __repr__
    print(reading.is_stale(now, max_age_seconds=60))  # False, just taken
 
    preview = SensorReadingPreview(tag="PT-200", value=101.3, unit="kPa",timestamp=now)
    print(preview)  # dataclass's auto-generated __repr__
 
 
if __name__ == "__main__":
    main()
    