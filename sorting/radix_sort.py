"""
Radix Sort (LSD)
================
Sort integers by digits using stable counting sort per digit.
"""


def radix_sort(arr):
    """
    Returns a new sorted list using LSD radix sort (base-10).
    Assumes non-negative integers. Time: O(d·(n + b)), Space: O(n + b)
    """
    if not arr:
        return []
    if any(x < 0 for x in arr):
        raise ValueError("radix_sort expects non-negative integers")
    
    def counting_by_digit(a, exp, base=10):
        count = [0] * base
        out = [0] * len(a)
        # STEP 1: Count digit occurrences
        for x in a:
            d = (x // exp) % base
            count[d] += 1
        # STEP 2: Prefix sums
        for i in range(1, base):
            count[i] += count[i - 1]
        # STEP 3: Build output stably
        for x in reversed(a):
            d = (x // exp) % base
            count[d] -= 1
            out[count[d]] = x
        return out
    
    max_val = max(arr)
    exp = 1
    result = arr[:]
    while max_val // exp > 0:
        result = counting_by_digit(result, exp)
        exp *= 10
    return result


if __name__ == "__main__":
    data = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Before:", data)
    print("After:", radix_sort(data))
