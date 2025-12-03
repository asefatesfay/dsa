"""
Lists - Practice Problems
=========================
Common interview questions and practice problems.
"""

# Problem 1: Two Sum
def two_sum(nums, target):
    """
    Find two numbers that add up to target.
    Time: O(n), Space: O(n)
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print("Problem 1: Two Sum")
nums = [2, 7, 11, 15]
target = 9
print(f"Input: {nums}, target: {target}")
print(f"Indices: {two_sum(nums, target)}")
print()

# Problem 2: Best Time to Buy and Sell Stock
def max_profit(prices):
    """
    Find maximum profit from buying and selling stock once.
    Time: O(n), Space: O(1)
    """
    if not prices:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        profit = price - min_price
        max_profit = max(max_profit, profit)
        min_price = min(min_price, price)
    
    return max_profit

print("Problem 2: Best Time to Buy and Sell Stock")
prices = [7, 1, 5, 3, 6, 4]
print(f"Prices: {prices}")
print(f"Max profit: {max_profit(prices)}")
print()

# Problem 3: Move Zeroes
def move_zeroes(nums):
    """
    Move all zeros to end while maintaining relative order.
    Time: O(n), Space: O(1)
    """
    left = 0
    for right in range(len(nums)):
        if nums[right] != 0:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
    return nums

print("Problem 3: Move Zeroes")
nums = [0, 1, 0, 3, 12]
print(f"Before: {nums}")
print(f"After: {move_zeroes(nums[:])}")
print()

# Problem 4: Contains Duplicate
def contains_duplicate(nums):
    """
    Check if array contains duplicates.
    Time: O(n), Space: O(n)
    """
    return len(nums) != len(set(nums))

print("Problem 4: Contains Duplicate")
nums1 = [1, 2, 3, 1]
nums2 = [1, 2, 3, 4]
print(f"{nums1}: {contains_duplicate(nums1)}")
print(f"{nums2}: {contains_duplicate(nums2)}")
print()

# Problem 5: Rotate Array
def rotate_array(nums, k):
    """
    Rotate array to the right by k steps.
    Time: O(n), Space: O(1)
    """
    k = k % len(nums)
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
    return nums

print("Problem 5: Rotate Array")
nums = [1, 2, 3, 4, 5, 6, 7]
k = 3
print(f"Original: {nums}")
print(f"Rotated by {k}: {rotate_array(nums[:], k)}")
print()

# Problem 6: Product of Array Except Self
def product_except_self(nums):
    """
    Return array where each element is product of all others.
    Time: O(n), Space: O(1) excluding output
    """
    n = len(nums)
    result = [1] * n
    
    # Left pass
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    
    # Right pass
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    
    return result

print("Problem 6: Product of Array Except Self")
nums = [1, 2, 3, 4]
print(f"Input: {nums}")
print(f"Output: {product_except_self(nums)}")
print()

# Problem 7: Maximum Product Subarray
def max_product_subarray(nums):
    """
    Find maximum product of contiguous subarray.
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    max_prod = min_prod = result = nums[0]
    
    for num in nums[1:]:
        temp = max_prod
        max_prod = max(num, max_prod * num, min_prod * num)
        min_prod = min(num, temp * num, min_prod * num)
        result = max(result, max_prod)
    
    return result

print("Problem 7: Maximum Product Subarray")
nums = [2, 3, -2, 4]
print(f"Input: {nums}")
print(f"Max product: {max_product_subarray(nums)}")
