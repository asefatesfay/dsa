"""
Two Heaps Pattern
=================
Maintain two heaps (max-heap for lower half, min-heap for upper half) to track medians or balance partitions.
"""

import heapq


class MedianFinder:
    """
    Streaming Median via Two Heaps
    ------------------------------
    Maintains two heaps:
    - `lower` (max-heap simulated with negatives) holds the smaller half
    - `upper` (min-heap) holds the larger half

    Invariants:
    - len(lower) == len(upper) or len(lower) == len(upper) + 1
    - max(lower) <= min(upper)
    """

    def __init__(self):
        self.lower = []
        self.upper = []

    def addNum(self, num):
        # STEP 1: Place num into appropriate heap
        if not self.lower or num <= -self.lower[0]:
            heapq.heappush(self.lower, -num)
        else:
            heapq.heappush(self.upper, num)
        # STEP 2: Rebalance sizes
        if len(self.lower) > len(self.upper) + 1:
            heapq.heappush(self.upper, -heapq.heappop(self.lower))
        elif len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def findMedian(self):
        # STEP 3: Read median from heap tops
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0


def sliding_window_median(nums, k):
    """
    Sliding Window Median (Reference Implementation)
    ===============================================
    Goal: For each window of size k, compute the median.

    Production approach: two-heaps with lazy deletion in O(n log k).
    Here, we present a simpler, correct reference using a sorted list
    (O(n · k log k)) to keep focus on the median logic.

    Steps per element:
    1) Insert new element in sorted order (bisect.insort)
    2) Remove element that slid out (bisect_left + pop)
    3) Read median from middle(s)
    """
    import bisect
    if k == 0:
        return []
    window = []
    res = []
    for i, x in enumerate(nums):
        bisect.insort(window, x)
        if i >= k:
            idx = bisect.bisect_left(window, nums[i - k])
            window.pop(idx)
        if i >= k - 1:
            mid = k // 2
            if k % 2:
                res.append(float(window[mid]))
            else:
                res.append((window[mid - 1] + window[mid]) / 2.0)
    return res


if __name__ == "__main__":
    mf = MedianFinder()
    for x in [1,2,3,4]:
        mf.addNum(x)
    print("median:", mf.findMedian())  # 2.5
    print(sliding_window_median([1,3,-1,-3,5,3,6,7], 3))

# =====================
# Additional Two Heaps Problems
# =====================

def ipo_max_capital(k, w, profits, capital):
    """
    IPO: Maximize Capital with Two Heaps
    ------------------------------------
    Steps:
    1) Sort projects by capital requirement
    2) Repeat k times:
       - Push affordable projects' profits into max-heap
       - Pop largest profit and add to capital
    """
    import heapq
    projects = sorted(zip(capital, profits))
    i = 0
    maxp = []
    for _ in range(k):
        # STEP 1: Add all newly-affordable projects
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(maxp, -projects[i][1])
            i += 1
        # STEP 2: Take best profit if available
        if not maxp:
            break
        w -= heapq.heappop(maxp)
    return w


def k_closest_points(points, k):
    """
    K Closest Points to Origin (Max-Heap of Size k)
    -----------------------------------------------
    Maintain a bounded max-heap storing k closest points by squared distance.
    """
    import heapq
    h = []
    for x, y in points:
        d2 = x * x + y * y
        if len(h) < k:
            heapq.heappush(h, (-d2, (x, y)))
        else:
            if -d2 > h[0][0]:
                heapq.heapreplace(h, (-d2, (x, y)))
    return [p for _, p in h]


if __name__ == "__main__":
    print("IPO:", ipo_max_capital(2, 0, [1,2,3], [0,1,1]))  # 4
    print("k closest:", k_closest_points([(1,3),(-2,2),(2,-2)], 2))
