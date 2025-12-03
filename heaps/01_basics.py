"""
Heap (Priority Queue) - Basics
===============================
Understanding heaps and Python's heapq module.
"""

import heapq
from typing import List


print("=" * 60)
print("What is a Heap?")
print("=" * 60)
print("A heap is a special tree-based data structure that satisfies")
print("the heap property:")
print()
print("Min Heap: Parent node ≤ all children (smallest at root)")
print("Max Heap: Parent node ≥ all children (largest at root)")
print()
print("Python's heapq implements a MIN HEAP")
print()
print("Key Properties:")
print("  - Always maintains heap property after operations")
print("  - Smallest element is always at index 0")
print("  - Insert: O(log n)")
print("  - Remove min: O(log n)")
print("  - Peek min: O(1)")
print()
print("Common Use Cases:")
print("  - Finding k smallest/largest elements")
print("  - Merge k sorted lists")
print("  - Task scheduling by priority")
print("  - Dijkstra's shortest path algorithm")
print("  - Median finding in a stream")
print()


# Basic Operations
print("=" * 60)
print("Basic Heap Operations")
print("=" * 60)

# 1. Creating a heap
print("\n1. Creating a heap:")
heap = []  # Start with empty list
print(f"   Empty heap: {heap}")

# 2. Adding elements (heappush)
print("\n2. Adding elements with heappush:")
heapq.heappush(heap, 5)
print(f"   After push(5): {heap}")
heapq.heappush(heap, 3)
print(f"   After push(3): {heap}")
heapq.heappush(heap, 7)
print(f"   After push(7): {heap}")
heapq.heappush(heap, 1)
print(f"   After push(1): {heap}")
print(f"   Note: Smallest (1) is at index 0")

# 3. Converting list to heap (heapify)
print("\n3. Converting existing list to heap:")
numbers = [5, 2, 8, 1, 9, 3]
print(f"   Original list: {numbers}")
heapq.heapify(numbers)
print(f"   After heapify: {numbers}")
print(f"   Time: O(n) - more efficient than n pushes!")

# 4. Removing smallest element (heappop)
print("\n4. Removing smallest element:")
heap = [1, 3, 5, 7]
print(f"   Heap before: {heap}")
smallest = heapq.heappop(heap)
print(f"   Popped: {smallest}")
print(f"   Heap after: {heap}")

# 5. Push and pop in one operation
print("\n5. Push then pop (heappushpop):")
heap = [1, 3, 5, 7]
print(f"   Heap: {heap}")
result = heapq.heappushpop(heap, 2)
print(f"   heappushpop(2) returns: {result}")
print(f"   Heap after: {heap}")
print(f"   Explanation: Pushes 2, then pops smallest (1)")

# 6. Pop then push (heapreplace)
print("\n6. Pop then push (heapreplace):")
heap = [1, 3, 5, 7]
print(f"   Heap: {heap}")
result = heapq.heapreplace(heap, 2)
print(f"   heapreplace(2) returns: {result}")
print(f"   Heap after: {heap}")
print(f"   Explanation: Pops smallest (1), then pushes 2")

# 7. Peek at smallest without removing
print("\n7. Peek at smallest element:")
heap = [1, 3, 5, 7]
print(f"   Heap: {heap}")
print(f"   Smallest (heap[0]): {heap[0]}")
print(f"   Heap unchanged: {heap}")

print()


# Finding k smallest/largest elements
print("=" * 60)
print("Finding K Smallest/Largest Elements")
print("=" * 60)

numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]
k = 3

print(f"\nGiven: {numbers}")
print(f"Find: {k} smallest and {k} largest")

# K smallest
smallest = heapq.nsmallest(k, numbers)
print(f"\n{k} smallest: {smallest}")
print(f"How it works: Maintains max heap of size k")

# K largest
largest = heapq.nlargest(k, numbers)
print(f"{k} largest: {largest}")
print(f"How it works: Maintains min heap of size k")

# With custom key
print("\nWith custom objects:")
students = [
    ('Alice', 85),
    ('Bob', 92),
    ('Charlie', 78),
    ('David', 95),
    ('Eve', 88)
]
print(f"Students: {students}")

# Top 3 by score
top_students = heapq.nlargest(3, students, key=lambda x: x[1])
print(f"\nTop 3 by score:")
for name, score in top_students:
    print(f"  {name}: {score}")

print()


# Max Heap Simulation
print("=" * 60)
print("Simulating Max Heap (Python only has Min Heap)")
print("=" * 60)
print("\nTrick: Negate all values!")
print("Example: [5, 2, 8] → push -5, -2, -8")
print("         Min heap: [-8, -5, -2]")
print("         Pop: -8 → negate back → 8 (the max!)")

print("\nDemo:")
max_heap = []
values = [5, 2, 8, 1, 9]
print(f"Values to insert: {values}")

# Insert with negation
for val in values:
    heapq.heappush(max_heap, -val)
print(f"Max heap (negated): {max_heap}")

# Extract max
print("\nExtracting maximums:")
while max_heap:
    max_val = -heapq.heappop(max_heap)  # Negate back to get actual max
    print(f"  Popped: {max_val}, Heap: {[-x for x in max_heap]}")

print()


# Merging Sorted Lists
print("=" * 60)
print("Merging Multiple Sorted Lists")
print("=" * 60)

list1 = [1, 4, 7]
list2 = [2, 5, 8]
list3 = [3, 6, 9]

print(f"\nList 1: {list1}")
print(f"List 2: {list2}")
print(f"List 3: {list3}")

# heapq.merge returns iterator
merged = list(heapq.merge(list1, list2, list3))
print(f"\nMerged: {merged}")
print(f"\nHow it works:")
print(f"  - Uses heap to track smallest element from each list")
print(f"  - Time: O(n log k) where n=total elements, k=num lists")
print(f"  - Space: O(k) for heap")

print()


# Heap Invariant
print("=" * 60)
print("Understanding Heap Structure")
print("=" * 60)

heap = [1, 3, 5, 7, 9, 8, 6]
print(f"\nHeap: {heap}")
print(f"\nTree representation:")
print(f"           1           (index 0)")
print(f"         /   \\")
print(f"        3     5        (indices 1, 2)")
print(f"       / \\   / \\")
print(f"      7   9 8   6      (indices 3, 4, 5, 6)")
print()
print(f"Parent-Child relationship:")
print(f"  - Parent of index i: (i - 1) // 2")
print(f"  - Left child of i: 2*i + 1")
print(f"  - Right child of i: 2*i + 2")
print()
print(f"Heap property: parent ≤ both children")
print(f"  - 1 ≤ 3 and 1 ≤ 5 ✓")
print(f"  - 3 ≤ 7 and 3 ≤ 9 ✓")
print(f"  - 5 ≤ 8 and 5 ≤ 6 ✓")

print()
