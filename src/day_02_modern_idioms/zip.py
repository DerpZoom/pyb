"""
Day 02 — Explore zip() 
 
Run:  uv run python src/day_02_modern_idioms/zip.py
"""

# Python’s zip() combines multiple iterables item-by-item.

names = ["Ana", "Ben", "Cal"]   # A list of three strings, each a name.
scores = [90, 85, 92]           # A list of three integers, each a score.   
pairs = zip(names, scores)

print("names =", names)     # names = ['Ana', 'Ben', 'Cal']
print("scores =", scores)   # scores = [90, 85, 92]
print("-"*20)  

print("type(pairs) =", type(pairs))     # <class 'zip'>
print("list(pairs) =", list(pairs))     # [('Ana', 90), ('Ben', 85), ('Cal', 92)]  — zip() returns an iterator,
                                        # so we convert it to a list(typecast) to see its contents as a list.
#print("list(pairs) =", list(pairs))     # list(pairs) consumes the zip iterator and converts its items into a list.
#print("type(list(pairs)) =", type(list(pairs)))     # <class 'list'>                                      
print("-"*20)

# A common use is looping over related values:
for name, score in zip(names, scores):
    print(f"{name}: {score}")
print("-"*20)

"""
Important details:
zip() stops when the shortest iterable runs out.
It returns an iterator, so it’s consumed after one pass.
Use list(zip(...)) if you need a reusable list.
It can combine more than two iterables.
"""

pairs1 = zip(names, scores, [True, True, True])
for name, score, passed in pairs1:
    print(name, score, passed)
print(list(pairs1))  # prints [] because the zip iterator was consumed in the for loop above.
print("-"*20)

pairs2 = list(zip(names, scores, [True, True, True]))  # recreate the zip iterator
for name, score, passed in pairs2:
    print(name, score, passed)
print(pairs2)  # prints the list of tuples because it's a list, not an iterator.
print("-"*20)   