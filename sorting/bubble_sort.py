"""
Bubble Sort
===========
Repeatedly swap adjacent out-of-order elements.
"""


def bubble_sort(arr):
    """
    Sorts the array in-place using bubble sort.
    Time: O(n^2)  Space: O(1)
    """
    n = len(arr)
    # STEP 1: Outer pass shrinks unsorted suffix
    for i in range(n - 1):
        swapped = False
        # STEP 2: Bubble the largest to the end of range
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # STEP 3: Early exit if already sorted
        if not swapped:
            break
    return arr


if __name__ == "__main__":
    data = [5, 1, 4, 2, 8]
    print("Before:", data)
    print("After:", bubble_sort(data))
