"""
Lists - Operations
==================
Common operations: append, insert, extend, remove, pop, clear, etc.
"""

# Starting list
fruits = ["apple", "banana", "cherry"]
print(f"Original list: {fruits}")
print()

# Append - adds element at end O(1)
fruits.append("date")
print(f"After append('date'): {fruits}")

# Insert - adds element at specific index O(n)
fruits.insert(1, "apricot")
print(f"After insert(1, 'apricot'): {fruits}")

# Extend - adds multiple elements O(k) where k is number of elements
fruits.extend(["elderberry", "fig"])
print(f"After extend: {fruits}")
print()

# Remove - removes first occurrence O(n)
fruits.remove("banana")
print(f"After remove('banana'): {fruits}")

# Pop - removes and returns element at index (default -1) O(n) or O(1) for last
popped = fruits.pop()
print(f"Popped element: {popped}")
print(f"After pop(): {fruits}")

popped_at_1 = fruits.pop(1)
print(f"Popped at index 1: {popped_at_1}")
print(f"After pop(1): {fruits}")
print()

# Index - finds first occurrence O(n)
print(f"Index of 'cherry': {fruits.index('cherry')}")

# Count - counts occurrences O(n)
numbers = [1, 2, 3, 2, 4, 2, 5]
print(f"Count of 2 in {numbers}: {numbers.count(2)}")
print()

# Sort - sorts in place O(n log n)
numbers.sort()
print(f"Sorted numbers: {numbers}")

numbers.sort(reverse=True)
print(f"Reverse sorted: {numbers}")

# Sorted - returns new sorted list O(n log n)
original = [3, 1, 4, 1, 5]
sorted_list = sorted(original)
print(f"Original: {original}, Sorted copy: {sorted_list}")
print()

# Reverse - reverses in place O(n)
numbers.reverse()
print(f"Reversed: {numbers}")

# Clear - removes all elements O(n)
temp = [1, 2, 3]
temp.clear()
print(f"After clear: {temp}")
