"""
Day 02 — Explore enumerate()  
 
Run:  uv run python src/day_02_modern_idioms/enumerate.py
"""



"""
enumerate() lets you loop over a sequence while getting both:
the item’s index
the item itself
"""

fruits = ["apple", "banana", "cherry"] # Python list containing three strings.

print("-"*20)
for index, fruit in enumerate(fruits):
    print(index, fruit)
print("-"*20)

# Avoid this, Tenumerate() is cleaner than maintaining a counter manually:
number = 1
for ass in fruits:
    print(number, ass)
    number += 1
print("-"*20)

# To start at a different index, use the start= keyword argument:
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)
print("-"*20)

# To start at a different index, use the start= keyword argument:
# For each index print the corresponding list item, starting at 10 instead of 0.
for peanut, butter in enumerate(fruits, start=10):
    print(peanut, butter)
print("-"*20)


"""
Notes on list items: Python lists are zero-indexed, meaning the first item is at index 0.

The square brackets make it a list:

fruits = ["apple", "banana", "cherry"]
         ^                           ^
Inside the brackets, commas separate the list’s items:
["apple", "banana", "cherry"]

[] → defines a list

"apple" etc. → string values

, → separates the values

fruits → variable referring to the list

You can verify its type:
print(type(fruits))
"""

print("print(type(fruits))")
print(type(fruits))