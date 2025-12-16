"""
NeetCode 150 - Intervals
=========================
Interval manipulation (6 problems).
"""


# PATTERN: Sorting + Merging
def insert(intervals, newInterval):
    """
    Insert Interval - insert and merge if needed.
    
    Pattern: Three-phase merge
    
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    
    # Add all intervals before newInterval
    while i < len(intervals) and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < len(intervals) and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    
    result.append(newInterval)
    
    # Add remaining intervals
    while i < len(intervals):
        result.append(intervals[i])
        i += 1
    
    return result


# PATTERN: Sorting + Greedy
def merge(intervals):
    """
    Merge Intervals - merge all overlapping intervals.
    
    Pattern: Sort by start, merge overlapping
    
    Time: O(n log n), Space: O(n)
    """
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged


# PATTERN: Interval Counting
def erase_overlap_intervals(intervals):
    """
    Non-overlapping Intervals - minimum removals to make non-overlapping.
    
    Pattern: Sort by end, greedy selection
    
    Time: O(n log n), Space: O(1)
    """
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    end = float('-inf')
    
    for start, interval_end in intervals:
        if start >= end:
            end = interval_end
        else:
            count += 1
    
    return count


# PATTERN: Interval Scheduling
def can_attend_meetings(intervals):
    """
    Meeting Rooms - can attend all meetings.
    
    Pattern: Sort and check overlaps
    
    Time: O(n log n), Space: O(1)
    """
    intervals.sort()
    
    for i in range(len(intervals) - 1):
        if intervals[i][1] > intervals[i + 1][0]:
            return False
    
    return True


# PATTERN: Min Heap
def min_meeting_rooms(intervals):
    """
    Meeting Rooms II - minimum meeting rooms required.
    
    Pattern: Min heap of end times
    
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0
    
    import heapq
    
    intervals.sort(key=lambda x: x[0])
    heap = [intervals[0][1]]
    
    for start, end in intervals[1:]:
        if start >= heap[0]:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    
    return len(heap)


# PATTERN: Sweep Line Algorithm
def min_interval(intervals, queries):
    """
    Minimum Interval to Include Each Query.
    
    Pattern: Sort + min heap + sweep line
    
    Algorithm Steps:
    1. Sort intervals by start time
    2. Sort queries (keep original indices)
    3. For each query, add all valid intervals to heap
    4. Remove expired intervals
    5. Top of heap is smallest valid interval
    
    Time: O(n log n + q log q), Space: O(n + q)
    """
    import heapq
    
    intervals.sort()
    sorted_queries = sorted((q, i) for i, q in enumerate(queries))
    
    result = [-1] * len(queries)
    heap = []
    i = 0
    
    for q, idx in sorted_queries:
        # Add all intervals that start before or at query
        while i < len(intervals) and intervals[i][0] <= q:
            start, end = intervals[i]
            if end >= q:  # Valid interval
                heapq.heappush(heap, (end - start + 1, end))
            i += 1
        
        # Remove expired intervals
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        
        # Answer query
        if heap:
            result[idx] = heap[0][0]
    
    return result


if __name__ == "__main__":
    print("=== NeetCode 150 - Intervals ===\n")
    
    print("Test 1: Insert Interval")
    intervals = [[1, 3], [6, 9]]
    newInterval = [2, 5]
    print(f"Insert {newInterval} into {intervals}: {insert(intervals, newInterval)}")
    
    print("\nTest 2: Merge Intervals")
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(f"Merge {intervals}: {merge(intervals)}")
    
    print("\nTest 3: Non-overlapping Intervals")
    intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
    print(f"Min removals for {intervals}: {erase_overlap_intervals(intervals)}")
    
    print("\nTest 4: Meeting Rooms")
    intervals = [[0, 30], [5, 10], [15, 20]]
    print(f"Can attend {intervals}: {can_attend_meetings(intervals)}")
    
    print("\nTest 5: Meeting Rooms II")
    intervals = [[0, 30], [5, 10], [15, 20]]
    print(f"Min rooms for {intervals}: {min_meeting_rooms(intervals)}")
    
    print("\nTest 6: Minimum Interval to Include Query")
    intervals = [[1, 4], [2, 4], [3, 6], [4, 4]]
    queries = [2, 3, 4, 5]
    print(f"Intervals {intervals}, Queries {queries}: {min_interval(intervals, queries)}")
