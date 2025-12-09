"""
Top K / Heap Patterns
=====================
Use heaps to efficiently track extrema or frequencies.
"""

import heapq
from collections import Counter


def kth_largest(nums, k):
    """
    Return the k-th largest element using a min-heap of size k.
    Time: O(n log k) Space: O(k)
    """
    h = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        else:
            if x > h[0]:
                heapq.heapreplace(h, x)
    return h[0]


def top_k_frequent(nums, k):
    """
    Return top-k frequent elements.
    """
    freq = Counter(nums)
    # Build max-heap by negative count
    h = [(-c, x) for x, c in freq.items()]
    heapq.heapify(h)
    res = []
    for _ in range(min(k, len(h))):
        c, x = heapq.heappop(h)
        res.append(x)
    return res


if __name__ == "__main__":
    print("kth largest:", kth_largest([3,2,1,5,6,4], 2))
    print("top-k:", top_k_frequent([1,1,1,2,2,3], 2))
