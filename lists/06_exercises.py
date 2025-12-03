"""
Lists - Exercises
=================
Practice exercises to test your understanding.
Try solving these before looking at the solutions!
"""

# Exercise 1: Find Missing Number
def find_missing_number(nums):
    """
    Given array of n-1 integers in range [0, n], find missing number.
    Example: [3, 0, 1] -> 2
    
    TODO: Implement this function
    Hint: Use sum formula or XOR
    """
    pass

# Exercise 2: Find All Numbers Disappeared
def find_disappeared_numbers(nums):
    """
    Given array of n integers [1, n], find all numbers that don't appear.
    Example: [4,3,2,7,8,2,3,1] -> [5,6]
    
    TODO: Implement this function
    Hint: Mark visited indices by negating values
    """
    pass

# Exercise 3: Merge Sorted Arrays
def merge_sorted_arrays(nums1, m, nums2, n):
    """
    Merge nums2 into nums1 (which has size m+n).
    Example: nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3
    Result: [1,2,2,3,5,6]
    
    TODO: Implement this function
    Hint: Start from the end
    """
    pass

# Exercise 4: Remove Element
def remove_element(nums, val):
    """
    Remove all occurrences of val in-place, return new length.
    Example: nums=[3,2,2,3], val=3 -> 2, nums=[2,2,_,_]
    
    TODO: Implement this function
    Hint: Two pointers
    """
    pass

# Exercise 5: Plus One
def plus_one(digits):
    """
    Given array representing a number, increment by one.
    Example: [1,2,3] -> [1,2,4]
    Example: [9,9,9] -> [1,0,0,0]
    
    TODO: Implement this function
    Hint: Handle carry
    """
    pass

# Exercise 6: Find Peak Element
def find_peak_element(nums):
    """
    Find index where nums[i] > nums[i-1] and nums[i] > nums[i+1].
    Example: [1,2,3,1] -> 2 (index of 3)
    
    TODO: Implement this function
    Hint: Binary search or linear scan
    """
    pass

# Exercise 7: Search in Rotated Sorted Array
def search_rotated(nums, target):
    """
    Search target in rotated sorted array.
    Example: nums=[4,5,6,7,0,1,2], target=0 -> 4
    
    TODO: Implement this function
    Hint: Modified binary search
    """
    pass

# Exercise 8: Find First and Last Position
def search_range(nums, target):
    """
    Find starting and ending position of target in sorted array.
    Example: nums=[5,7,7,8,8,10], target=8 -> [3,4]
    
    TODO: Implement this function
    Hint: Two binary searches
    """
    pass

# Exercise 9: Spiral Matrix
def spiral_order(matrix):
    """
    Return all elements in spiral order.
    Example: [[1,2,3],[4,5,6],[7,8,9]] -> [1,2,3,6,9,8,7,4,5]
    
    TODO: Implement this function
    Hint: Track boundaries
    """
    pass

# Exercise 10: Subarray Sum Equals K
def subarray_sum(nums, k):
    """
    Count number of continuous subarrays that sum to k.
    Example: nums=[1,1,1], k=2 -> 2
    
    TODO: Implement this function
    Hint: Prefix sum + hashmap
    """
    pass


# Test your solutions
if __name__ == "__main__":
    print("Test your implementations here!")
    print("Uncomment the tests as you complete each exercise.\n")
    
    # Test Exercise 1
    # print(f"Missing number in [3,0,1]: {find_missing_number([3,0,1])}")
    
    # Test Exercise 2
    # print(f"Disappeared numbers: {find_disappeared_numbers([4,3,2,7,8,2,3,1])}")
    
    # Test Exercise 5
    # print(f"Plus one [1,2,3]: {plus_one([1,2,3])}")
    # print(f"Plus one [9,9,9]: {plus_one([9,9,9])}")
