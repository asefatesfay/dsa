"""
Lists - Basics
==============
Lists are ordered, mutable collections in Python that can store elements of different types.
Time Complexity: Access O(1), Append O(1), Insert O(n), Delete O(n), Search O(n)
Space Complexity: O(n)
"""

# Creating lists
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, [1, 2]]

print("Basic Lists:")
print(f"Empty list: {empty_list}")
print(f"Numbers: {numbers}")
print(f"Mixed types: {mixed}")
print()

# Accessing elements
print("Accessing Elements:")
print(f"First element: {numbers[0]}")
print(f"Last element: {numbers[-1]}")
print(f"Second last: {numbers[-2]}")
print()

# Slicing
print("Slicing:")
print(f"First 3 elements: {numbers[0:3]}")
print(f"Elements from index 2: {numbers[2:]}")
print(f"Last 3 elements: {numbers[-3:]}")
print(f"Every 2nd element: {numbers[::2]}")
print(f"Reverse list: {numbers[::-1]}")
print()

# List length
print(f"Length of list: {len(numbers)}")
print()

# Checking membership
print("Membership:")
print(f"3 in numbers: {3 in numbers}")
print(f"10 in numbers: {10 in numbers}")
