"""
Merge Sort
==========
Divide array into halves, sort each, and merge.
"""


def merge_sort(arr):
    """
    Returns a new sorted list using merge sort.
    Time: O(n log n)  Space: O(n)
    """
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # Merge two sorted lists
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]
    print("Before:", data)
    print("After:", merge_sort(data))
