"""
Two Pointers Pattern
====================
Use two indices that move towards each other or in tandem to achieve O(n) on sorted arrays, strings, or when shrinking/expanding ranges.
"""


def pair_sum_sorted(arr, target):
    """
    Find two numbers in a sorted array that sum to target.
    Time: O(n) Space: O(1)
    """
    i, j = 0, len(arr) - 1
    while i < j:
        s = arr[i] + arr[j]
        if s == target:
            return (i, j)
        if s < target:
            i += 1
        else:
            j -= 1
    return None


def remove_duplicates_sorted(arr):
    """
    Remove duplicates in-place from a sorted array and return new length.
    Time: O(n) Space: O(1)
    """
    if not arr:
        return 0
    write = 1
    for read in range(1, len(arr)):
        if arr[read] != arr[read - 1]:
            arr[write] = arr[read]
            write += 1
    return write


if __name__ == "__main__":
    a = [1, 2, 3, 4, 6, 8]
    print("pair_sum_sorted:", pair_sum_sorted(a, 10))
    b = [1,1,2,2,2,3,4,4]
    n = remove_duplicates_sorted(b)
    print("dedup:", b[:n])

# =====================
# Additional Two-Pointers Problems
# =====================

def two_sum_unsorted(arr, target):
    """
    Return indices of two numbers that add to target in an unsorted array.
    Uses hash map (not strictly two-pointers), but include sorted variant below.
    Time: O(n) Space: O(n)
    """
    seen = {}
    for i, x in enumerate(arr):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None


def two_sum_sorted_indices(arr, target):
    """
    Two pointers for sorted array; return 1-based indices like classic problem.
    Time: O(n) Space: O(1)
    """
    i, j = 0, len(arr) - 1
    while i < j:
        s = arr[i] + arr[j]
        if s == target:
            return (i + 1, j + 1)
        if s < target:
            i += 1
        else:
            j -= 1
    return None


def three_sum(nums):
    """
    Find all unique triplets (a,b,c) such that a+b+c=0.
    Sort + fix one + two-pointers.
    Time: O(n^2) Space: O(1) extra (excluding output)
    """
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        target = -nums[i]
        l, r = i + 1, n - 1
        while l < r:
            s = nums[l] + nums[r]
            if s == target:
                res.append([nums[i], nums[l], nums[r]])
                l += 1; r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
            elif s < target:
                l += 1
            else:
                r -= 1
    return res


def container_with_most_water(height):
    """
    Max area formed by two lines; classic two-pointers.
    Move the shorter pointer inward.
    Time: O(n) Space: O(1)
    """
    i, j = 0, len(height) - 1
    best = 0
    while i < j:
        h = min(height[i], height[j])
        best = max(best, h * (j - i))
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
    return best


if __name__ == "__main__":
    print("two sum unsorted:", two_sum_unsorted([3,2,4], 6))  # (1,2)
    print("two sum sorted idx:", two_sum_sorted_indices([2,7,11,15], 9))  # (1,2)
    print("three sum:", three_sum([-1,0,1,2,-1,-4]))
    print("max water:", container_with_most_water([1,8,6,2,5,4,8,3,7]))
