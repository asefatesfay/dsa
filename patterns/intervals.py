"""
Interval Patterns
=================
Sorting intervals and merging/inserting to handle overlaps.
"""


def merge_intervals(intervals):
    """
    Merge overlapping intervals.
    Input: list of [start, end]
    """
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    res = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)
        else:
            res.append([s, e])
    return res


def insert_interval(intervals, newI):
    """
    Insert interval and merge overlaps.
    """
    res = []
    i = 0
    n = len(intervals)
    # add all before
    while i < n and intervals[i][1] < newI[0]:
        res.append(intervals[i]); i += 1
    # merge overlaps
    s, e = newI
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    res.append([s, e])
    # add remaining
    res.extend(intervals[i:])
    return res


def has_overlap(a, b):
    """
    Check if two intervals [a1,a2] and [b1,b2] overlap.
    """
    return not (a[1] < b[0] or b[1] < a[0])


if __name__ == "__main__":
    print(merge_intervals([[1,3],[2,6],[8,10],[15,18]]))
    print(insert_interval([[1,3],[6,9]], [2,5]))
    print(has_overlap([1,3],[4,6]))
