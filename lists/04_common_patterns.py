"""
Lists - Common Patterns and Algorithms
======================================
Frequently used patterns when working with lists in DSA problems.
"""

# Pattern 1: Two Pointers
def two_pointer_example(arr):
    """
    Remove duplicates from sorted array.
    Time: O(n), Space: O(1)
    
    Example:
        Input: [1, 1, 2, 2, 3, 4, 4]
        Output: [1, 2, 3, 4]
        Explanation: Use two pointers to track unique elements
    """
    if not arr:
        return 0
    
    left = 0
    for right in range(1, len(arr)):
        if arr[right] != arr[left]:
            left += 1
            arr[left] = arr[right]
    
    return left + 1

print("=" * 60)
print("Pattern 1: Two Pointers - Remove Duplicates")
print("=" * 60)
print("Problem: Remove duplicates from sorted array in-place")
print("\nHow it works:")
print("  1. Use two pointers: 'left' tracks unique position")
print("  2. 'right' scans through array")
print("  3. When different element found: move left, copy element")
print("  4. Result: unique elements packed at start of array")
print("  5. Works because array is SORTED")
print("\nExample:")
arr = [1, 1, 2, 2, 3, 4, 4]
print(f"  Input: {arr}")
length = two_pointer_example(arr)
print(f"  Output: {arr[:length]}")
print("  Process: Left marks boundary, right finds new unique values")
print()

# Pattern 2: Sliding Window
def max_sum_subarray(arr, k):
    """
    Maximum sum of subarray of size k.
    Time: O(n), Space: O(1)
    
    Example:
        Input: arr = [1, 4, 2, 10, 23, 3, 1, 0, 20], k = 4
        Output: 39
        Explanation: Subarray [10, 23, 3, 1] has max sum 39
    """
    if len(arr) < k:
        return None
    
    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
    
print("=" * 60)
print("Pattern 2: Sliding Window - Maximum Sum Subarray")
print("=" * 60)
print("Problem: Find maximum sum of k consecutive elements")
print("\nHow it works:")
print("  1. Calculate sum of first k elements (initial window)")
print("  2. Slide window: remove leftmost, add new rightmost")
print("  3. Formula: new_sum = old_sum - arr[left] + arr[right]")
print("  4. Track maximum sum seen")
print("  5. Efficient: O(n) instead of O(n*k)")
print("  6. Avoids recalculating entire window each time")
print("\nExample:")
arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
k = 4
result = max_sum_subarray(arr, k)
print(f"  Input: arr = {arr}, k = {k}")
print(f"  Output: {result}")
print("  Best window: [10,23,3,1] = 37 (or similar)")
print()

# Pattern 3: Kadane's Algorithm - Maximum Subarray Sum
def max_subarray_sum(arr):
    """
    Find maximum sum of contiguous subarray.
    Time: O(n), Space: O(1)
    
    Example:
        Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        Output: 6
        Explanation: Subarray [4, -1, 2, 1] has sum 6
    """
    max_sum = current_sum = arr[0]
    
    for num in arr[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum

print("=" * 60)
print("Pattern 3: Kadane's Algorithm - Maximum Subarray Sum")
print("=" * 60)
print("Problem: Find maximum sum of any contiguous subarray")
print("\nHow it works:")
print("  1. Track current_sum: sum ending at current position")
print("  2. At each element: decide to extend or start fresh")
print("  3. Extend if current_sum + num > num")
print("  4. Start fresh if num alone is better")
print("  5. Key insight: negative sum? Drop it, start over")
print("  6. Track maximum sum seen across all positions")
print("\nExample:")
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
result = max_subarray_sum(arr)
print(f"  Input: {arr}")
print(f"  Output: {result}")
print("  Best subarray: [4,-1,2,1] = 6")
print()

# Pattern 4: Prefix Sum
def prefix_sum_example(arr):
    """
    Calculate prefix sum array.
    Time: O(n), Space: O(n)
    
    Example:
        Input: [1, 2, 3, 4, 5]
        Output: [1, 3, 6, 10, 15]
        Explanation: Each element is sum of all previous + current
        prefix[i] = arr[0] + arr[1] + ... + arr[i]
    """
    prefix = [0] * len(arr)
    prefix[0] = arr[0]
    
    for i in range(1, len(arr)):
        prefix[i] = prefix[i - 1] + arr[i]
    
    return prefix

print("=" * 60)
print("Pattern 4: Prefix Sum")
print("=" * 60)
print("Problem: Calculate cumulative sum for range queries")
print("\nHow it works:")
print("  1. prefix[i] = sum of all elements from 0 to i")
print("  2. Build: prefix[i] = prefix[i-1] + arr[i]")
print("  3. Use: range sum(L,R) = prefix[R] - prefix[L-1]")
print("  4. Benefit: O(1) range sum queries after O(n) preprocessing")
print("  5. Without prefix: each range query needs O(n)")
print("\nExample:")
arr = [1, 2, 3, 4, 5]
result = prefix_sum_example(arr)
print(f"  Input: {arr}")
print(f"  Output: {result}")
print(f"  Use: sum[1:3] = prefix[3]-prefix[0] = 10-1 = 9")
print(f"       (elements 2+3+4 = 9)")
print()

# Pattern 5: Finding Duplicates
def find_duplicates(arr):
    """
    Find all duplicate elements.
    Time: O(n), Space: O(n)
    
    Example:
        Input: [1, 2, 3, 2, 4, 3, 5]
        Output: [2, 3]
        Explanation: 2 and 3 appear more than once
    """
    seen = set()
    duplicates = set()
    
    for num in arr:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)

print("=" * 60)
print("Pattern 5: Finding Duplicates")
print("=" * 60)
print("Problem: Identify all elements that appear more than once")
print("\nHow it works:")
print("  1. Use 'seen' set to track elements we've encountered")
print("  2. Use 'duplicates' set to store duplicates found")
print("  3. For each element: check if already in 'seen'")
print("  4. If yes: it's a duplicate, add to duplicates set")
print("  5. If no: first time seeing it, add to seen set")
print("  6. Sets give O(1) lookup, total O(n) time")
print("\nExample:")
arr = [1, 2, 3, 2, 4, 3, 5]
result = find_duplicates(arr)
print(f"  Input: {arr}")
print(f"  Output: {result}")
print("  Found: 2 and 3 appear multiple times")
print()

# Pattern 6: Reversing Portions
def reverse_portion(arr, start, end):
    """
    Reverse elements from start to end index.
    Time: O(n), Space: O(1)
    
    Example:
        Input: arr = [1, 2, 3, 4, 5, 6], start = 1, end = 4
        Output: [1, 5, 4, 3, 2, 6]
        Explanation: Reverse elements from index 1 to 4
    """
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1
    return arr

print("=" * 60)
print("Pattern 6: Reversing Portions")
print("=" * 60)
print("Problem: Reverse a subarray in-place")
print("\nHow it works:")
print("  1. Two pointers: start at beginning and end of range")
print("  2. Swap elements at both pointers")
print("  3. Move start forward, end backward")
print("  4. Continue until pointers meet")
print("  5. In-place reversal: O(1) space")
print("\nExample:")
arr = [1, 2, 3, 4, 5, 6]
print(f"  Input: {arr}, reverse indices 1 to 4")
result = reverse_portion(arr[:], 1, 4)
print(f"  Output: {result}")
print("  Process: swap(2,5), swap(3,4) -> [1,5,4,3,2,6]")
