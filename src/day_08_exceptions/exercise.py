"""Day 8 - Exceptions done right.
Validate a batch of raw sensor readings, turning bad data into a
custom exception so the caller can decide what to do with it.
"""
 
class SensorRangeError(ValueError):
    """Raised when a reading is unparseable or outside its valid range."""
    # Subclass ValueError so old `except ValueError` handlers still catch it,
    # while new code can catch SensorRangeError specifically when it cares.
    def __init__(self, tag: str, value: float, low: float, high: float):
        self.tag = tag          # stash context ON the exception object...
        self.value = value      # ...so a handler can log it without re-parsing
        super().__init__(f"{tag}={value} outside [{low}, {high}]")
 
 
def validate(tag: str, raw: str, low: float, high: float) -> float:
    """Parse and range-check one reading; raise on bad, return on good."""
    try:
        value = float(raw)              # may raise ValueError on junk text
    except ValueError as exc:
        # Re-raise as OUR type, chaining the original with `from` for the trace.
        raise SensorRangeError(tag, float("nan"), low, high) from exc
    else:
        # `else` runs only when the try block did NOT raise (parse succeeded).
        if not (low <= value <= high):
            raise SensorRangeError(tag, value, low, high)
        return value
    finally:
        # `finally` ALWAYS runs: success, handled error, or exception in flight.
        print(f"checked {tag}")


def main() -> None:
    readings = [("PT-101", "4.2"), ("PT-102", "999"), ("PT-103", "oops")]
    good, bad = [], []
    for tag, raw in readings:
        try:
            good.append((tag, validate(tag, raw, 0.0, 20.0)))
        except SensorRangeError as exc:      # catch ONLY our error; let real bugs crash loud
            bad.append((tag, str(exc)))
    print("good:", good)
    print(  "bad:", bad)
 

if __name__ == "__main__":
    main()
