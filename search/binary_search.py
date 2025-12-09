"""
Binary Search
=============
Efficient search on a sorted array using divide and conquer.
"""


def binary_search(arr, target):
    """
    Return index of target in sorted arr, or -1 if not found.
    Time: O(log n)  Space: O(1)
    Preconditions: arr must be sorted in non-decreasing order.
    """
    left, right = 0, len(arr) - 1
    # STEP 1: While there is a search range
    while left <= right:
        # STEP 2: Pick middle (avoid overflow)
        mid = left + (right - left) // 2
        # STEP 3: Compare middle with target
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            # STEP 4a: Target in right half
            left = mid + 1
        else:
            # STEP 4b: Target in left half
            right = mid - 1
    # STEP 5: Not found
    return -1


if __name__ == "__main__":
    data = [1, 2, 4, 7, 9]
    print("Sorted array:", data)
    for t in [7, 3, 1, 10]:
        idx = binary_search(data, t)
        print(f"Find {t}: index={idx}")
