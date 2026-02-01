"""
Intervals - LeetCode Problems
==============================
Essential interval problems for interviews.
"""

from typing import List
import heapq


print("=" * 70)
print("Problem 1: Merge Intervals (LC 56)")
print("=" * 70)
print()

def merge(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge all overlapping intervals.
    
    Approach: Sort by start, merge consecutive overlapping
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)
    
    return merged

intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
print(f"Intervals: {intervals}")
print(f"Merged: {merge(intervals)}")
print()


print("=" * 70)
print("Problem 2: Insert Interval (LC 57)")
print("=" * 70)
print()

def insert(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    """
    Insert and merge new interval.
    
    Approach: Add before, merge overlapping, add after
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    n = len(intervals)
    
    # Add all before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)
    
    # Add remaining
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result

intervals = [[1, 3], [6, 9]]
newInterval = [2, 5]
print(f"Intervals: {intervals}, New: {newInterval}")
print(f"After insert: {insert(intervals, newInterval)}")
print()


print("=" * 70)
print("Problem 3: Non-overlapping Intervals (LC 435)")
print("=" * 70)
print()

def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    """
    Min intervals to remove to make non-overlapping.
    
    Approach: Sort by end, greedy keep earliest ending
    Time: O(n log n), Space: O(1)
    """
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])
    count = 0
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1  # Remove current interval
        else:
            end = intervals[i][1]
    
    return count

intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
print(f"Intervals: {intervals}")
print(f"Remove count: {erase_overlap_intervals(intervals)}")
print()


print("=" * 70)
print("Problem 4: Meeting Rooms (LC 252)")
print("=" * 70)
print()

def can_attend_meetings(intervals: List[List[int]]) -> bool:
    """
    Can attend all meetings (no overlap)?
    
    Approach: Sort and check consecutive
    Time: O(n log n), Space: O(1)
    """
    intervals.sort()
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    
    return True

intervals = [[0, 30], [5, 10], [15, 20]]
print(f"Meetings: {intervals}")
print(f"Can attend all: {can_attend_meetings(intervals)}")

intervals = [[7, 10], [2, 4]]
print(f"\nMeetings: {intervals}")
print(f"Can attend all: {can_attend_meetings(intervals)}")
print()


print("=" * 70)
print("Problem 5: Meeting Rooms II (LC 253)")
print("=" * 70)
print()

def min_meeting_rooms(intervals: List[List[int]]) -> int:
    """
    Min meeting rooms needed.
    
    Approach: Separate start/end times, two pointers
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0
    
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = max_rooms = 0
    s = e = 0
    
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    
    return max_rooms

intervals = [[0, 30], [5, 10], [15, 20]]
print(f"Meetings: {intervals}")
print(f"Min rooms: {min_meeting_rooms(intervals)}")
print()


print("=" * 70)
print("Problem 6: Interval List Intersections (LC 986)")
print("=" * 70)
print()

def interval_intersection(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Find intersections of two interval lists.
    
    Approach: Two pointers, find overlaps
    Time: O(m + n), Space: O(min(m, n))
    """
    result = []
    i = j = 0
    
    while i < len(A) and j < len(B):
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])
        
        if start <= end:
            result.append([start, end])
        
        # Move pointer with earlier end
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1
    
    return result

A = [[0, 2], [5, 10], [13, 23], [24, 25]]
B = [[1, 5], [8, 12], [15, 24], [25, 26]]
print(f"A: {A}")
print(f"B: {B}")
print(f"Intersections: {interval_intersection(A, B)}")
print()


print("=" * 70)
print("Problem 7: Minimum Arrows to Burst Balloons (LC 452)")
print("=" * 70)
print()

def find_min_arrow_shots(points: List[List[int]]) -> int:
    """
    Min arrows to burst all balloons.
    
    Approach: Sort by end, greedy shoot at earliest end
    Time: O(n log n), Space: O(1)
    """
    if not points:
        return 0
    
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    
    for i in range(1, len(points)):
        if points[i][0] > end:
            arrows += 1
            end = points[i][1]
    
    return arrows

points = [[10, 16], [2, 8], [1, 6], [7, 12]]
print(f"Balloons: {points}")
print(f"Min arrows: {find_min_arrow_shots(points)}")
print()


print("=" * 70)
print("Problem 8: Employee Free Time (LC 759)")
print("=" * 70)
print()

def employee_free_time(schedule: List[List[List[int]]]) -> List[List[int]]:
    """
    Find common free time intervals.
    
    Approach: Flatten, merge, find gaps
    Time: O(n log n), Space: O(n)
    """
    # Flatten all intervals
    intervals = []
    for employee in schedule:
        intervals.extend(employee)
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Merge overlapping
    merged = [intervals[0]]
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)
    
    # Find gaps
    gaps = []
    for i in range(1, len(merged)):
        gaps.append([merged[i-1][1], merged[i][0]])
    
    return gaps

schedule = [[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]
print(f"Schedule: {schedule}")
print(f"Free time: {employee_free_time(schedule)}")
print()


print("=" * 70)
print("Problem 9: My Calendar I (LC 729)")
print("=" * 70)
print()

class MyCalendar:
    """
    Book events without double booking.
    
    Approach: Maintain sorted list, check overlaps
    """
    
    def __init__(self):
        self.events = []
    
    def book(self, start: int, end: int) -> bool:
        """Time: O(n)"""
        for s, e in self.events:
            if start < e and s < end:
                return False
        self.events.append((start, end))
        return True

calendar = MyCalendar()
bookings = [(10, 20), (15, 25), (20, 30)]
print("Booking events:")
for start, end in bookings:
    result = calendar.book(start, end)
    print(f"  [{start}, {end}): {result}")
print()


print("=" * 70)
print("Problem 10: Car Pooling (LC 1094)")
print("=" * 70)
print()

def car_pooling(trips: List[List[int]], capacity: int) -> bool:
    """
    Check if car can handle all trips.
    
    Approach: Timeline events (pickup/dropoff)
    Time: O(n log n), Space: O(n)
    """
    events = []
    for passengers, start, end in trips:
        events.append((start, passengers))
        events.append((end, -passengers))
    
    events.sort()
    current = 0
    
    for _, change in events:
        current += change
        if current > capacity:
            return False
    
    return True

trips = [[2, 1, 5], [3, 3, 7]]
capacity = 4
print(f"Trips: {trips}, Capacity: {capacity}")
print(f"Can pool: {car_pooling(trips, capacity)}")

trips = [[2, 1, 5], [3, 3, 7]]
capacity = 5
print(f"\nTrips: {trips}, Capacity: {capacity}")
print(f"Can pool: {car_pooling(trips, capacity)}")
print()


print("=" * 70)
print("Problem 11: Data Stream as Disjoint Intervals (LC 352)")
print("=" * 70)
print()

class SummaryRanges:
    """
    Track disjoint intervals from data stream.
    
    Approach: Maintain sorted intervals, merge on add
    """
    
    def __init__(self):
        self.intervals = []
    
    def addNum(self, value: int) -> None:
        """Time: O(n)"""
        new = [value, value]
        result = []
        i = 0
        
        # Add all before new
        while i < len(self.intervals) and self.intervals[i][1] < new[0] - 1:
            result.append(self.intervals[i])
            i += 1
        
        # Merge overlapping
        while i < len(self.intervals) and self.intervals[i][0] <= new[1] + 1:
            new[0] = min(new[0], self.intervals[i][0])
            new[1] = max(new[1], self.intervals[i][1])
            i += 1
        result.append(new)
        
        # Add remaining
        while i < len(self.intervals):
            result.append(self.intervals[i])
            i += 1
        
        self.intervals = result
    
    def getIntervals(self) -> List[List[int]]:
        """Time: O(1)"""
        return self.intervals

sr = SummaryRanges()
nums = [1, 3, 7, 2, 6]
print("Adding numbers and tracking intervals:")
for num in nums:
    sr.addNum(num)
    print(f"  Add {num}: {sr.getIntervals()}")
print()


print("=" * 70)
print("Summary")
print("=" * 70)
print()
print("Key Patterns:")
print("  • Merge: Sort by start, merge consecutive")
print("  • Insert: Add before + merge + add after")
print("  • Non-overlap: Sort by end, greedy keep earliest")
print("  • Meeting Rooms I: Check consecutive overlaps")
print("  • Meeting Rooms II: Separate start/end, two pointers")
print("  • Intersections: Two pointers on both lists")
print("  • Min Arrows: Sort by end, shoot at earliest")
print("  • Timeline: Create events, process sorted")
print()
print("Time Complexities:")
print("  • Most problems: O(n log n) due to sorting")
print("  • Merge/Insert: O(n log n)")
print("  • Two pointers: O(m + n)")
print()
print("Interview Tips:")
print("  ✓ Always ask: overlapping or touching?")
print("  ✓ Sort by start time (default) or end time (greedy)")
print("  ✓ Use events for timeline problems")
print("  ✓ Two pointers for two lists")
print("  ✓ Greedy works for many interval problems")
