"""
Sliding Window + Prefix Sum
===========================
Maintain a window over the array or string to compute aggregates efficiently.
"""


def max_sum_subarray_fixed(arr, k):
    """
    Fixed-Size Sliding Window: Max Sum
    ----------------------------------
    Invariant: window covers exactly k elements; we maintain its sum.

    Steps:
    1) Initialize `window_sum = sum(arr[:k])` and `max_sum = window_sum`
    2) For each new index i ≥ k:
       - Add entering element arr[i]
       - Remove leaving element arr[i-k]
       - Update `max_sum`

    Correctness: each k-length window is considered exactly once.
    Time: O(n)  Space: O(1)
    """
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum


def longest_substring_k_distinct(s, k):
    """
    Variable-Size Sliding Window: ≤ k Distinct
    ------------------------------------------
    Invariant: window has at most k distinct chars; expand right, shrink left.

    Steps:
    1) Expand right; increment count of s[right]
    2) If distinct > k: move left forward, decrement counts, removing zeros
    3) Track best length as we go

    Time: O(n) (each index enters/exits window once)  Space: O(k)
    """
    from collections import Counter
    left = 0
    counts = Counter()
    distinct = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        if counts[ch] == 1:
            distinct += 1
        while distinct > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                distinct -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def prefix_sums(arr):
    """
    Prefix Sums
    -----------
    Build cumulative sums P for fast range queries.
    P[i] = sum(arr[:i]).  sum(l..r) = P[r+1] - P[l].
    """
    P = [0]
    for x in arr:
        P.append(P[-1] + x)
    return P


if __name__ == "__main__":
    print(max_sum_subarray_fixed([2,1,5,1,3,2], 3))  # 9
    print(longest_substring_k_distinct("eceba", 2))  # 3 ("ece")
    print(prefix_sums([1,2,3,4]))  # [0,1,3,6,10]

# Additional Sliding Window Problem

def min_subarray_len(target, nums):
    """
    Variable Window: Min Length with Sum ≥ target
    --------------------------------------------
    Invariant: maintain window sum; shrink to minimal when sum ≥ target.

    Steps:
    1) Expand right, accumulate sum
    2) While sum ≥ target: update answer, shrink left, subtract nums[left]
    3) If no window meets target → return 0

    Time: O(n) Space: O(1)
    """
    left = 0
    cur = 0
    best = float('inf')
    for right, x in enumerate(nums):
        cur += x
        while cur >= target:
            best = min(best, right - left + 1)
            cur -= nums[left]
            left += 1
    return 0 if best == float('inf') else best


if __name__ == "__main__":
    print(min_subarray_len(7, [2,3,1,2,4,3]))  # 2 (4,3)
