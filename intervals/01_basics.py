"""
Intervals - Basics
==================
Fundamental operations on intervals.
"""

from typing import List


print("=" * 60)
print("Basic 1: Interval Representation")
print("=" * 60)
print()

# Intervals as lists
interval1 = [1, 3]  # [start, end]
print(f"List interval: {interval1}")

# Intervals as tuples (immutable)
interval2 = (5, 7)
print(f"Tuple interval: {interval2}")

# Intervals as custom class
class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"[{self.start}, {self.end}]"

interval3 = Interval(10, 15)
print(f"Class interval: {interval3}")
print()


print("=" * 60)
print("Basic 2: Check Overlap")
print("=" * 60)
print()

def overlaps(a: List[int], b: List[int]) -> bool:
    """
    Check if two intervals overlap.
    Intervals overlap if: a.start <= b.end AND b.start <= a.end
    
    Time: O(1), Space: O(1)
    """
    return a[0] <= b[1] and b[0] <= a[1]

intervals = [
    ([1, 3], [2, 4]),
    ([1, 3], [4, 6]),
    ([1, 5], [2, 3]),
    ([1, 3], [3, 5])
]

for a, b in intervals:
    print(f"{a} and {b}: {'Overlap' if overlaps(a, b) else 'No overlap'}")
print()


print("=" * 60)
print("Basic 3: Merge Two Intervals")
print("=" * 60)
print()

def merge_two(a: List[int], b: List[int]) -> List[int]:
    """
    Merge two overlapping intervals.
    
    Time: O(1), Space: O(1)
    """
    if not overlaps(a, b):
        return None
    return [min(a[0], b[0]), max(a[1], b[1])]

a = [1, 4]
b = [2, 6]
merged = merge_two(a, b)
print(f"Merge {a} and {b}: {merged}")

a = [1, 3]
b = [5, 7]
merged = merge_two(a, b)
print(f"Merge {a} and {b}: {merged}")
print()


print("=" * 60)
print("Basic 4: Sort Intervals")
print("=" * 60)
print()

intervals = [[5, 7], [1, 3], [8, 10], [2, 4]]
print(f"Original: {intervals}")

# Sort by start time
sorted_by_start = sorted(intervals, key=lambda x: x[0])
print(f"Sorted by start: {sorted_by_start}")

# Sort by end time
sorted_by_end = sorted(intervals, key=lambda x: x[1])
print(f"Sorted by end: {sorted_by_end}")

# Sort by duration (end - start)
sorted_by_duration = sorted(intervals, key=lambda x: x[1] - x[0])
print(f"Sorted by duration: {sorted_by_duration}")
print()


print("=" * 60)
print("Basic 5: Merge All Overlapping Intervals")
print("=" * 60)
print()

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge all overlapping intervals.
    
    Approach: Sort by start, then merge consecutive overlapping intervals.
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            # Overlapping, merge
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            # Non-overlapping, add new interval
            merged.append(current)
    
    return merged

intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
print(f"Original: {intervals}")
print(f"Merged: {merge_intervals(intervals)}")

intervals = [[1, 4], [4, 5]]
print(f"\nOriginal: {intervals}")
print(f"Merged: {merge_intervals(intervals)}")
print()


print("=" * 60)
print("Basic 6: Insert Interval")
print("=" * 60)
print()

def insert_interval(intervals: List[List[int]], new: List[int]) -> List[List[int]]:
    """
    Insert new interval and merge if necessary.
    
    Approach: Add before, merge overlapping, add after.
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals that come before new interval
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result

intervals = [[1, 3], [6, 9]]
new = [2, 5]
print(f"Intervals: {intervals}")
print(f"Insert {new}: {insert_interval(intervals, new)}")

intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
new = [4, 8]
print(f"\nIntervals: {intervals}")
print(f"Insert {new}: {insert_interval(intervals, new)}")
print()


print("=" * 60)
print("Basic 7: Find Gaps")
print("=" * 60)
print()

def find_gaps(intervals: List[List[int]], start: int, end: int) -> List[List[int]]:
    """
    Find gaps between intervals within [start, end] range.
    
    Time: O(n log n), Space: O(n)
    """
    intervals.sort(key=lambda x: x[0])
    gaps = []
    current = start
    
    for interval in intervals:
        if interval[0] > current:
            gaps.append([current, interval[0]])
        current = max(current, interval[1])
    
    if current < end:
        gaps.append([current, end])
    
    return gaps

intervals = [[1, 3], [5, 7], [10, 12]]
start, end = 0, 15
print(f"Intervals: {intervals}")
print(f"Gaps in [{start}, {end}]: {find_gaps(intervals, start, end)}")
print()


print("=" * 60)
print("Basic 8: Interval Intersection")
print("=" * 60)
print()

def intersection(a: List[int], b: List[int]) -> List[int]:
    """
    Find intersection of two intervals.
    
    Time: O(1), Space: O(1)
    """
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    
    if start <= end:
        return [start, end]
    return None

a = [1, 5]
b = [3, 7]
print(f"Intersection of {a} and {b}: {intersection(a, b)}")

a = [1, 3]
b = [5, 7]
print(f"Intersection of {a} and {b}: {intersection(a, b)}")
print()


print("=" * 60)
print("Basic 9: Interval Properties")
print("=" * 60)
print()

def interval_length(interval: List[int]) -> int:
    """Calculate length/duration of interval."""
    return interval[1] - interval[0]

def is_point(interval: List[int]) -> bool:
    """Check if interval is a single point."""
    return interval[0] == interval[1]

def contains_point(interval: List[int], point: int) -> bool:
    """Check if interval contains a point."""
    return interval[0] <= point <= interval[1]

def contains_interval(outer: List[int], inner: List[int]) -> bool:
    """Check if outer interval contains inner interval."""
    return outer[0] <= inner[0] and inner[1] <= outer[1]

interval = [3, 8]
print(f"Interval: {interval}")
print(f"  Length: {interval_length(interval)}")
print(f"  Is point: {is_point(interval)}")
print(f"  Contains 5: {contains_point(interval, 5)}")
print(f"  Contains 10: {contains_point(interval, 10)}")
print(f"  Contains [4, 6]: {contains_interval(interval, [4, 6])}")
print()


print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Key Operations:")
print("  1. Check overlap: a.start <= b.end AND b.start <= a.end")
print("  2. Merge two: [min(starts), max(ends)]")
print("  3. Merge all: Sort + linear scan")
print("  4. Insert: Add before + merge + add after")
print("  5. Intersection: [max(starts), min(ends)]")
print()
print("Common Patterns:")
print("  • Always sort intervals first (usually by start)")
print("  • Use greedy approach for merging")
print("  • Track current interval while scanning")
print("  • Handle edge cases: empty, single, touching")
print()
print("Time Complexity:")
print("  • Overlap check: O(1)")
print("  • Merge all: O(n log n) due to sorting")
print("  • Insert: O(n) with sorted input")
