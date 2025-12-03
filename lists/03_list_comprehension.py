"""
Lists - List Comprehension
==========================
Elegant and concise way to create lists based on existing lists or iterables.
Syntax: [expression for item in iterable if condition]
"""

# Basic list comprehension
squares = [x**2 for x in range(1, 6)]
print(f"Squares: {squares}")

# With condition
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"Even squares: {even_squares}")

# String manipulation
words = ["hello", "world", "python"]
uppercase = [word.upper() for word in words]
print(f"Uppercase: {uppercase}")

# Filtering
numbers = [1, -2, 3, -4, 5, -6]
positive = [n for n in numbers if n > 0]
print(f"Positive numbers: {positive}")
print()

# Nested list comprehension
matrix = [[i + j for j in range(3)] for i in range(3)]
print("Matrix:")
for row in matrix:
    print(row)
print()

# Flattening a list
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]
print(f"Flattened: {flat}")

# With if-else
numbers = [1, 2, 3, 4, 5]
labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
print(f"Labels: {labels}")
print()

# Practical examples
# 1. Filter strings by length
words = ["a", "ab", "abc", "abcd", "abcde"]
long_words = [w for w in words if len(w) >= 3]
print(f"Words with 3+ chars: {long_words}")

# 2. Create tuples
pairs = [(x, x**2) for x in range(5)]
print(f"Number-square pairs: {pairs}")

# 3. Remove vowels
text = "hello world"
no_vowels = [char for char in text if char not in "aeiou"]
print(f"Without vowels: {''.join(no_vowels)}")
