"""
Binary Search & Variants
========================
Use binary search to find boundaries (first/last), solve monotonic predicate problems, and handle rotated arrays.
"""


def lower_bound(arr, target):
    """
    Lower Bound (first ≥ target)
    ----------------------------
    Invariant: search range [lo, hi) maintains answer ∈ [lo, hi).

    Steps:
    1) While lo < hi:
       - mid = (lo+hi)//2
       - If arr[mid] < target → lo = mid+1 (answer strictly to right)
       - Else → hi = mid (mid is a candidate; shrink left)
    2) Return lo
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(arr, target):
    """
    Upper Bound (first > target)
    ----------------------------
    Same pattern as lower bound, but the predicate is arr[mid] <= target.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search_rotated(arr, target):
    """
    Binary Search in Rotated Array
    ------------------------------
    Invariant: one side of [lo..mid] or [mid..hi] is sorted; decide which.
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[lo] <= arr[mid]:  # left side sorted
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right side sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def peak_element(arr):
    """
    Peak Finding (Binary Search on hills)
    -------------------------------------
    Compare mid to mid+1 and move towards the uphill side.
    """
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    a = [1,2,2,3,5]
    print("lb 3:", lower_bound(a,3), "ub 3:", upper_bound(a,3))
    r = [4,5,6,7,0,1,2]
    print("rot search 0:", search_rotated(r,0))
    p = [1,3,2,1]
    print("peak idx:", peak_element(p))

# Additional Binary Search Problem (Predicate BS)

def first_bad_version(n, is_bad):
    """
    Predicate Binary Search: First True
    -----------------------------------
    Given versions 1..n and a predicate is_bad(v), find first v with is_bad(v)=True.

    Steps:
    1) lo=1, hi=n
    2) While lo<hi:
       - mid=(lo+hi)//2
       - If is_bad(mid): hi=mid (mid could be first bad)
       - Else: lo=mid+1
    3) Return lo
    """
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    def mock_is_bad(v):
        return v >= 5
    print("first bad:", first_bad_version(10, mock_is_bad))  # 5
