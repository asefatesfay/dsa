"""
Hash Tables (Dictionaries) - Basic Operations
==============================================

Hash tables provide O(1) average time complexity for insert, delete, and lookup operations.
In Python, dictionaries and sets are implemented as hash tables.
"""

# Creating hash tables
print("=" * 60)
print("1. Creating Hash Tables")
print("=" * 60)

# Empty dictionary
hash_table = {}
print(f"Empty dictionary: {hash_table}")

# Dictionary with initial values
student_grades = {"Alice": 95, "Bob": 87, "Charlie": 92}
print(f"Student grades: {student_grades}")

# Using dict() constructor
colors = dict(red="#FF0000", green="#00FF00", blue="#0000FF")
print(f"Colors: {colors}")

# Dictionary comprehension
squares = {x: x**2 for x in range(1, 6)}
print(f"Squares: {squares}")

# Basic Operations
print("\n" + "=" * 60)
print("2. Basic Operations")
print("=" * 60)

# Insert/Update
hash_table["name"] = "John"
hash_table["age"] = 30
print(f"After insert: {hash_table}")

# Access
name = hash_table["name"]
print(f"Access by key: {name}")

# Safe access with get()
age = hash_table.get("age", 0)
missing = hash_table.get("missing", "default")
print(f"Using get(): age={age}, missing={missing}")

# Check if key exists
if "name" in hash_table:
    print(f"'name' exists in hash_table")

# Delete
del hash_table["age"]
print(f"After delete: {hash_table}")

# Pop (remove and return)
value = hash_table.pop("name", None)
print(f"Popped value: {value}, remaining: {hash_table}")

# Iteration
print("\n" + "=" * 60)
print("3. Iteration Methods")
print("=" * 60)

data = {"a": 1, "b": 2, "c": 3}

# Iterate over keys
print("Keys:", end=" ")
for key in data:
    print(key, end=" ")
print()

# Iterate over values
print("Values:", end=" ")
for value in data.values():
    print(value, end=" ")
print()

# Iterate over key-value pairs
print("Key-value pairs:")
for key, value in data.items():
    print(f"  {key}: {value}")

# Common Methods
print("\n" + "=" * 60)
print("4. Common Methods")
print("=" * 60)

d = {"x": 10, "y": 20}

# keys(), values(), items()
print(f"Keys: {list(d.keys())}")
print(f"Values: {list(d.values())}")
print(f"Items: {list(d.items())}")

# update() - merge dictionaries
d.update({"z": 30, "x": 15})
print(f"After update: {d}")

# clear()
d_copy = d.copy()
d_copy.clear()
print(f"After clear: {d_copy}, original: {d}")

# setdefault() - get or set default
count = d.setdefault("count", 0)
print(f"Setdefault: {count}, dict: {d}")

# Sets (Hash Sets)
print("\n" + "=" * 60)
print("5. Sets - Hash-based Collection")
print("=" * 60)

# Creating sets
s1 = {1, 2, 3, 4, 5}
s2 = set([3, 4, 5, 6, 7])
print(f"Set 1: {s1}")
print(f"Set 2: {s2}")

# Set operations
print(f"Union: {s1 | s2}")
print(f"Intersection: {s1 & s2}")
print(f"Difference: {s1 - s2}")
print(f"Symmetric difference: {s1 ^ s2}")

# Set methods
s1.add(6)
print(f"After add(6): {s1}")

s1.discard(2)  # Safe remove (no error if missing)
print(f"After discard(2): {s1}")

# Time Complexity Summary
print("\n" + "=" * 60)
print("Time Complexity")
print("=" * 60)
print("Insert/Update: O(1) average")
print("Lookup:        O(1) average")
print("Delete:        O(1) average")
print("Space:         O(n)")
