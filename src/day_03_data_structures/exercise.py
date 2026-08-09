"""Day 3 — Data structure audit: pick the right container."""

from collections import Counter
 
# Raw feed from one poll cycle: some tags were re-read, so there are duplicates.

readings = [ # list[tuple[str, float]]
    ("FT101", 12.4), ("PT204", 3.1), ("FT101", 12.9),   # FT101 re-read
    ("TT330", 88.0), ("PT204", 3.4), ("LT415", 61.2),
]

REQUIRED = {"FT101", "PT204", "TT330", "LT415", "FT500"}  # a set(contains unique elements) literal, an empty set is set() not {} which is a dict literal

ALARM_LIMIT = 50.0  # values above this are flagged
 
# 1. Latest value per tag. Dict assignment overwrites, so the LAST
#    reading of a duplicated tag automatically wins — no de-dup logic.
latest = {} # Creates an empty dictionary to hold the latest readings for each tag.
for tag, value in readings:
    latest[tag] = value
 
# 2. Which required tags never appeared? Set difference: REQUIRED minus
#    the tags we actually saw. latest.keys() is a dict view of the seen tags.
missing = REQUIRED - set(latest.keys()) # Creates a set of missing tags by subtracting the set of seen tags from the REQUIRED set.
 
# 3. Keep only tags whose latest value breaches the alarm limit.
#    Dict comprehension: {key: val for ... if condition}.
alarms = {tag: val for tag, val in latest.items() if val > ALARM_LIMIT}

print(f"Latest values : {latest}")
print(f"Missing tags  : {missing}")
print(f"Alarms        : {alarms}")

# 4. Count how many times each tag was read. Counter is a dict subclass
counts = Counter(tag for tag, value in readings)  # Creates a Counter object that counts the occurrences of each reading in the readings list.
print(f"Counts        : {counts}")
print(f"Counts items  : {list(counts.items())}")
print(f"Counts items  : {counts.items()}")

duplicates = {tag: count for tag, count in counts.items() if count > 1}  # Creates a dictionary of tags that have duplicates (count greater than 1).
print(f"Duplicates    : {duplicates}")
