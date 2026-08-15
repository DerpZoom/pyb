"""Day 4 — Function audit: args, kwargs, keyword-only, and the mutable-default trap.(Module docstring)(Sandbox)"""


#---------------------------------------------------------------------------------------------------------------------------------------------
#   *args — variable positional arguments. The * in a function signature collects any extra positional arguments into a tuple:
#---------------------------------------------------------------------------------------------------------------------------------------------

def log_readings(sensor_id, *readings):
    print(sensor_id, type(sensor_id), readings, type(readings))
    print("-"*20)

log_readings("TT-101", 72.4, 72.6, 73.0)
# TT-101 <class 'str'> (72.4, 72.6, 73.0) <class 'tuple'>

#---------------------------------------------------------------------------------------------------------------------------------------------
# **kwargs — variable keyword arguments. The ** collects extra keyword arguments into a dict:
#---------------------------------------------------------------------------------------------------------------------------------------------

def configure(tag, **options):
    print(tag, type(tag), options, type(options))
    print("-"*20)

configure("P-201", setpoint=55.0, mode="auto")
# P-201 <class 'str'> {'setpoint': 55.0, 'mode': 'auto'} <class 'dict'>

print("*"*20)

#---------------------------------------------------------------------------------------------------------------------------------------------
# These also work in reverse at the call site — f(*my_tuple, **my_dict) unpacks a sequence into positional args and a dict into keyword args.
# Same ** unpacking idiom you hit with HF tokenizers passing BatchEncoding into a model.
#---------------------------------------------------------------------------------------------------------------------------------------------

def move_axis(axis_id, speed, accel, *, mode="auto"):
    print(f"{axis_id}: speed={speed}, accel={accel}, mode={mode}")
    print("-"*20)
    
# Unpacking a tuple into positional args
params = (72.4, 1.2) # type: tuple
move_axis("X1", *params)
# X1: speed=72.4, accel=1.2, mode=auto

# Unpacking a dict into keyword args
settings = {"speed": 50.0, "accel": 0.8, "mode": "jog"} # type: dict
move_axis("Y1", **settings)
# Y1: speed=50.0, accel=0.8, mode=jog

# Combine both
positional = ("Z1",)    # tuple - trailing comma required to make it a tuple
keywords = {"speed": 10.0, "accel": 0.3} # type: dict
move_axis(*positional, **keywords)
# Z1: speed=10.0, accel=0.3, mode=auto

print("*"*20)

#---------------------------------------------------------------------------------------------------------------------------------------------
# what is the difference between `*` and `*args`
# Both mark "everything after this must be passed by keyword"
# The difference is whether you also want to collect those extra positional arguments or just block them.
# Bare * — no extra positional args allowed at all, it's just a fence:
# *args — same fence, but it also catches the overflow into a tuple you can use:
#
# So: use bare * when you want to force keyword-only args but have no need to accept a variable number of positionals.
# Use *args when you actually want to accept and use a variable number of positionals and force anything after them to be named. 
# Functionally, both do the exact same job of closing off positional matching for what follows
# *args just also gives you a place to put the extras instead of rejecting them.
#---------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------
# No — **kwargs doesn't have a bare-** equivalent, and the reason is that its job is different from *.
# * (or *args) is a fence — it marks a boundary in the parameter list, so anything after it changes how arguments must be passed (keyword-only). 
# That's why a bare * makes sense: you don't need to catch anything, you just need the fence.
#
#**kwargs isn't a fence — it's a catch-all endpoint. There's nothing "after" it that changes behavior, because Python doesn't allow anything 
# to come after **kwargs at all except more keyword-only params before it. 
# So a bare ** would have nothing to mark the start of — it wouldn't make syntactic sense, and Python doesn't allow it:
# ** must always bind to a name and collect into a dict:
#---------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------
# The full signature order is:
# positional-only, /, positional-or-keyword, *args (or bare *), keyword-only, **kwargs
# 
# def raw_write(addr, value, /, *, retries=3):
#
# addr and value must be positional (can't be passed as addr=), retries must be keyword.
# / and * bookend the positional-or-keyword middle section; **kwargs just sits at the very end soaking up whatever's left.
#
# def f(pos_only, /, normal, *, kw_only, **kwargs):
# before / → positional-only (pos_only)
# between / and * → positional-or-keyword, the everyday default (normal)
# after * → keyword-only (kw_only)
# **kwargs → catches whatever named args aren't already declared

# / and * are mirror images: / closes off keyword-calling from the left, * closes off positional-calling from the right. 
# Most everyday functions use neither and just live in the flexible middle zone — 
# you mainly reach for / when writing library-style code where you want to lock down the calling convention, 
# or when mimicking built-ins like len(obj, /), which is itself positional-only.
#---------------------------------------------------------------------------------------------------------------------------------------------