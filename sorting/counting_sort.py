"""
Counting Sort
=============
Stable linear-time sort for integers in a known small range.
"""


def counting_sort(arr, max_value=None):
    """
    Returns a new sorted list using counting sort.
    Assumes non-negative integers. Time: O(n + k) Space: O(n + k)
    """
    if not arr:
        return []
    if max_value is None:
        max_value = max(arr)
    count = [0] * (max_value + 1)
    # STEP 1: Count occurrences
    for x in arr:
        if x < 0:
            raise ValueError("counting_sort expects non-negative integers")
        count[x] += 1
    # STEP 2: Prefix sums for positions
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    # STEP 3: Build output stably (iterate original right-to-left)
    out = [0] * len(arr)
    for x in reversed(arr):
        count[x] -= 1
        out[count[x]] = x
    return out


if __name__ == "__main__":
    data = [4, 2, 2, 8, 3, 3, 1]
    print("Before:", data)
    print("After:", counting_sort(data))
