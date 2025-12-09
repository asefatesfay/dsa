"""
Insertion Sort
==============
Build sorted prefix by inserting each element in place.
"""


def insertion_sort(arr):
    """
    Sorts the array in-place using insertion sort.
    Time: O(n^2) average/worst, O(n) best when nearly sorted. Space: O(1)
    """
    # STEP 1: Grow sorted prefix [0..i)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # STEP 2: Shift greater elements right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        # STEP 3: Insert key
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    data = [12, 11, 13, 5, 6]
    print("Before:", data)
    print("After:", insertion_sort(data))
