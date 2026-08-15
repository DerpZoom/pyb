"""Day 4 — Function audit: args, kwargs, keyword-only, and the mutable-default trap.(Module docstring)"""
 
# A reading collector. Each call appends ONE reading to a log and returns it.
# The default value of `log` is the bug we are fixing — see the placeholder line.
def collect_reading(tag, value, *, unit="raw", log=None):
    # Everything after the bare * is keyword-only: callers must name unit/log.
    # A mutable default like []  is evaluated ONCE at definition time, so every
    # call that omits `log` would share the same list and leak readings across
    # unrelated calls. The sentinel + fresh-list-inside pattern prevents that.
    if log is None:            # sentinel check: caller passed no log
        log = []               # build a NEW list per call — no shared state
    log.append((tag, value, unit))   # record this reading as a tuple
    return log
 
# *tags gathers extra positional args into a TUPLE; **options gathers extra
# named args into a DICT. scan_ms is an ordinary keyword arg with a default.
def poll(*tags, scan_ms=500, **options):
    print(f"Polling {len(tags)} tags every {scan_ms} ms; options={options}")
    return tags
 
alarm_count = 0                # module-level (global) counter
def bump_alarm():
    global alarm_count         # without this, the line below makes a LOCAL
    alarm_count += 1           # and the module-level counter never changes
    return alarm_count

# --- exercise driver ---
first = collect_reading("FT101", 12.4)     # no log passed -> should be fresh
second = collect_reading("PT204", 3.1)     # MUST also be a fresh, separate list
print(f"first  : {first}")
print(f"second : {second}")   # one item each if the fix is correct, not two
poll("FT101", "PT204", "TT330", scan_ms=250, deadband=0.5)
print(f"alarms : {bump_alarm()}, {bump_alarm()}")
