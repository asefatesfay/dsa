"""
Selection Sort
==============
Select smallest element and put it at the front.
"""


def selection_sort(arr):
    """
    Sorts the array in-place using selection sort.
    Time: O(n^2)  Space: O(1)
    """
    n = len(arr)
    # STEP 1: Move boundary of sorted/unsorted
    for i in range(n):
        min_idx = i
        # STEP 2: Find smallest in unsorted part
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # STEP 3: Swap into position i
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


if __name__ == "__main__":
    data = [64, 25, 12, 22, 11]
    print("Before:", data)
    print("After:", selection_sort(data))
