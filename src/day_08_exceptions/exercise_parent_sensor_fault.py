"""Day 8 - Exceptions done right.
Validate a batch of raw sensor readings, turning bad data into a
custom exception so the caller can decide what to do with it.
"""


class SensorError(ValueError):
    """Base class for any sensor problem.

    Subclasses ValueError so old `except ValueError` handlers still catch it.
    Catch SensorError to handle ANY sensor issue; catch a subclass to be
    more specific. Both subclasses share the same context attributes and
    message format, so that lives here in the parent.
    """
    def __init__(self, tag: str, value: float, low: float, high: float):
        self.tag = tag          # stash context ON the exception object...
        self.value = value      # ...so a handler can log it without re-parsing
        super().__init__(f"{tag}={value} outside [{low}, {high}]")


class SensorRangeError(SensorError):
    """Raised when a reading parsed fine but is outside its valid range."""


class SensorParseError(SensorError):
    """Raised when a reading can't even be parsed into a number.

    A sibling of SensorRangeError, not a child of it - a value that never
    parsed doesn't really have a range. value is NaN here.
    """


def validate(tag: str, raw: str, low: float, high: float) -> float:
    """Parse and range-check one reading; raise on bad, return on good."""
    try:
        value = float(raw)              # may raise ValueError on junk text
    except ValueError as exc:
        # Parse-failure branch: re-raise as OUR parse type, chaining the
        # original with `from` for the traceback.
        raise SensorParseError(tag, float("nan"), low, high) from exc
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
    parse_failures = range_failures = 0
    for tag, raw in readings:
        try:
            good.append((tag, validate(tag, raw, 0.0, 20.0)))
        except SensorParseError as exc:      # specific sibling - check first
            parse_failures += 1
            bad.append((tag, str(exc)))
        except SensorRangeError as exc:      # the other specific sibling
            range_failures += 1
            bad.append((tag, str(exc)))
        # A caller that didn't care could replace both blocks above with a
        # single `except SensorError as exc:` and catch either one.
    print("good:", good)
    print(  "bad:", bad)
    print(f"parse failures: {parse_failures}, range failures: {range_failures}")

 
if __name__ == "__main__":
    main()