# Intervals

Interval problems involve working with ranges [start, end] and are common in scheduling, meeting room, and calendar applications.

## Common Operations

### 1. Merge Overlapping Intervals
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)
    
    return merged
```
**Time:** O(n log n), **Space:** O(n)

### 2. Insert Interval
```python
def insert(intervals, newInterval):
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result
```
**Time:** O(n), **Space:** O(n)

### 3. Check Overlap
```python
def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]
```

### 4. Meeting Rooms
```python
# Can attend all meetings (no overlap)?
def can_attend_meetings(intervals):
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True

# Minimum meeting rooms needed
def min_meeting_rooms(intervals):
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    rooms = available = 0
    s = e = 0
    
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1
            available = max(available, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    
    return available
```

## Key Patterns

### Pattern 1: Sort + Merge
- **Use case:** Merge overlapping intervals
- **Algorithm:** Sort by start, merge consecutive overlapping intervals
- **Time:** O(n log n)

### Pattern 2: Sort + Two Pointers
- **Use case:** Meeting rooms, interval intersections
- **Algorithm:** Separate start/end times, use two pointers
- **Time:** O(n log n)

### Pattern 3: Sweep Line
- **Use case:** Maximum concurrent intervals
- **Algorithm:** Create events for start/end, process in order
- **Time:** O(n log n)

### Pattern 4: Interval Tree / Segment Tree
- **Use case:** Range queries, dynamic intervals
- **Algorithm:** Build tree structure for O(log n) queries
- **Time:** Build O(n log n), Query O(log n)

## Common Problems

1. **Merge Intervals** (LC 56)
   - Sort by start, merge overlapping

2. **Insert Interval** (LC 57)
   - Add before, merge overlapping, add after

3. **Non-overlapping Intervals** (LC 435)
   - Greedy: remove intervals with latest end time

4. **Meeting Rooms** (LC 252)
   - Sort and check consecutive overlaps

5. **Meeting Rooms II** (LC 253)
   - Two pointers on sorted start/end times

6. **Interval List Intersections** (LC 986)
   - Two pointers, find overlaps

7. **Minimum Number of Arrows** (LC 452)
   - Sort by end, greedy selection

## Time Complexities

| Operation | Time | Space |
|-----------|------|-------|
| Sort intervals | O(n log n) | O(1) |
| Merge overlapping | O(n log n) | O(n) |
| Insert interval | O(n) | O(n) |
| Check overlap | O(1) | O(1) |
| Meeting rooms (can attend) | O(n log n) | O(1) |
| Meeting rooms (min count) | O(n log n) | O(n) |

## Interview Tips

✓ **Always sort first** - Most interval problems require sorting  
✓ **Sort by start time** - Default choice unless problem specifies otherwise  
✓ **Watch for edge cases** - Empty intervals, single interval, all overlapping  
✓ **Clarify closed vs open intervals** - Is [1,3] same as [1,2]?  
✓ **Two pointers for start/end** - Useful for meeting rooms type problems  
✓ **Greedy works well** - Many interval problems have greedy solutions  
✓ **Draw it out** - Visualize intervals on a timeline

## Common Mistakes

- Forgetting to sort intervals first
- Not handling edge cases (empty, single interval)
- Confusing closed [a,b] vs open (a,b) intervals
- Not considering when intervals touch but don't overlap
- Modifying input when not allowed

## Real-World Applications

- **Calendar scheduling** - Meeting rooms, appointment booking
- **Task scheduling** - CPU scheduling, resource allocation
- **Network protocols** - Time slot allocation, bandwidth scheduling
- **Financial systems** - Trading windows, market hours
- **Video streaming** - Buffer management, time ranges
