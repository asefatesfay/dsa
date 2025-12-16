"""
NeetCode 150 - Binary Search
=============================
Search optimization techniques.
"""


# PATTERN: Binary Search (Basic)
def binary_search(nums, target):
    """
    Binary Search - find target in sorted array.
    
    Pattern: Classic binary search
    
    Algorithm Steps:
    1. Set left=0, right=n-1
    2. While left <= right:
       - mid = (left + right) // 2
       - If nums[mid] == target, return mid
       - If nums[mid] < target, search right half
       - Else search left half
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


# PATTERN: Binary Search (2D)
def search_matrix(matrix, target):
    """
    Search a 2D Matrix - matrix sorted row-wise and column-wise.
    
    Pattern: Treat 2D as 1D array for binary search
    
    Algorithm Steps:
    1. Treat m×n matrix as array of length m*n
    2. Convert index to (row, col): row = idx // n, col = idx % n
    3. Binary search on virtual 1D array
    
    Time: O(log(m*n)), Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = (left + right) // 2
        row, col = mid // n, mid % n
        mid_val = matrix[row][col]
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# PATTERN: Binary Search on Answer
def min_eating_speed(piles, h):
    """
    Koko Eating Bananas - minimum speed to eat all bananas in h hours.
    
    Pattern: Binary search on answer space
    
    Algorithm Steps:
    1. Search space: [1, max(piles)]
    2. For each speed k, calculate hours needed
    3. Binary search to find minimum valid k
    
    Why it works: If speed k works, any speed > k also works (monotonic)
    
    Example: piles=[3,6,7,11], h=8
    - Try k=6: hours = 1+1+2+2 = 6 ✓
    - Try k=4: hours = 1+2+2+3 = 8 ✓
    - Try k=3: hours = 1+2+3+4 = 10 ✗
    - Answer: 4
    
    Time: O(n log m) where m = max(piles), Space: O(1)
    """
    def can_eat_all(k):
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k  # Ceiling division
        return hours <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        if can_eat_all(mid):
            right = mid
        else:
            left = mid + 1
    
    return left


# PATTERN: Binary Search (Modified)
def find_min(nums):
    """
    Find Minimum in Rotated Sorted Array.
    
    Pattern: Binary search with rotation handling
    
    Algorithm Steps:
    1. If nums[mid] > nums[right], minimum is in right half
    2. Otherwise, minimum is in left half (including mid)
    
    Example: [4,5,6,7,0,1,2]
    - mid=7 > right=2, search right
    - mid=0 < right=2, search left
    - Found minimum: 0
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if nums[mid] > nums[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid
    
    return nums[left]


# PATTERN: Binary Search (Modified)
def search(nums, target):
    """
    Search in Rotated Sorted Array.
    
    Pattern: Binary search with rotation detection
    
    Algorithm Steps:
    1. Find which half is sorted
    2. Check if target is in sorted half
    3. Search appropriate half
    
    Example: [4,5,6,7,0,1,2], target=0
    - mid=7, left half [4,5,6,7] is sorted
    - target not in [4,7], search right
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Check which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


# PATTERN: Binary Search (Time-based)
class TimeMap:
    """
    Time Based Key-Value Store.
    
    Pattern: Hash map + Binary search on timestamps
    
    Design:
    - Store list of (timestamp, value) pairs for each key
    - Use binary search to find largest timestamp <= given timestamp
    """
    
    def __init__(self):
        self.store = {}
    
    def set(self, key, value, timestamp):
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))
    
    def get(self, key, timestamp):
        if key not in self.store:
            return ""
        
        values = self.store[key]
        left, right = 0, len(values) - 1
        result = ""
        
        # Binary search for largest timestamp <= given timestamp
        while left <= right:
            mid = (left + right) // 2
            if values[mid][0] <= timestamp:
                result = values[mid][1]
                left = mid + 1
            else:
                right = mid - 1
        
        return result


# PATTERN: Binary Search (Hard)
def find_median_sorted_arrays(nums1, nums2):
    """
    Median of Two Sorted Arrays.
    
    Pattern: Binary search for partition
    
    Algorithm Steps:
    1. Binary search on smaller array
    2. Partition both arrays so left halves have (m+n+1)//2 elements
    3. Ensure max(left1) <= min(right2) and max(left2) <= min(right1)
    
    Time: O(log(min(m,n))), Space: O(1)
    """
    # Ensure nums1 is smaller
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found correct partition
            if (m + n) % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
            else:
                return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return 0.0


if __name__ == "__main__":
    print("=== NeetCode 150 - Binary Search ===\n")
    
    # Binary Search
    print(f"Binary Search [-1,0,3,5,9,12] target=9: {binary_search([-1, 0, 3, 5, 9, 12], 9)}")
    
    # Search 2D Matrix
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    print(f"Search Matrix target=3: {search_matrix(matrix, 3)}")
    
    # Koko Eating Bananas
    print(f"Min Eating Speed [3,6,7,11] h=8: {min_eating_speed([3, 6, 7, 11], 8)}")
    
    # Find Minimum in Rotated Array
    print(f"Find Min [3,4,5,1,2]: {find_min([3, 4, 5, 1, 2])}")
    
    # Search in Rotated Array
    print(f"Search Rotated [4,5,6,7,0,1,2] target=0: {search([4, 5, 6, 7, 0, 1, 2], 0)}")
    
    # Time Based Key-Value Store
    time_map = TimeMap()
    time_map.set("foo", "bar", 1)
    print(f"TimeMap get('foo', 1): {time_map.get('foo', 1)}")
    print(f"TimeMap get('foo', 3): {time_map.get('foo', 3)}")
    time_map.set("foo", "bar2", 4)
    print(f"TimeMap get('foo', 4): {time_map.get('foo', 4)}")
    print(f"TimeMap get('foo', 5): {time_map.get('foo', 5)}")
    
    # Median of Two Sorted Arrays
    print(f"Median [1,3] [2]: {find_median_sorted_arrays([1, 3], [2])}")
    print(f"Median [1,2] [3,4]: {find_median_sorted_arrays([1, 2], [3, 4])}")
