"""
Quick Sort
==========
Divide-and-conquer using partition around a pivot.
"""


def quick_sort(arr):
    """
    Sorts the array using quicksort (in-place, Lomuto partition).
    Average: O(n log n), Worst: O(n^2), Space: O(log n) recursion
    """
    def partition(a, lo, hi):
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        return i
    
    def sort(a, lo, hi):
        if lo < hi:
            p = partition(a, lo, hi)
            sort(a, lo, p - 1)
            sort(a, p + 1, hi)
    
    sort(arr, 0, len(arr) - 1)
    return arr


if __name__ == "__main__":
    data = [10, 7, 8, 9, 1, 5]
    print("Before:", data)
    print("After:", quick_sort(data))
