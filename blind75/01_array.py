"""
Blind 75 - Array Problems
==========================
Essential array manipulation and algorithm problems for technical interviews.
"""


# 1. Two Sum
# PATTERN: Hash Map
def two_sum(nums, target):
    """
    Find indices of two numbers that add up to target.
    
    Problem: Given array of integers, return indices of two numbers that sum to target.
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1] (because nums[0] + nums[1] = 2 + 7 = 9)
    
    Pattern: Hash Map for O(1) complement lookup
    Approach: Hash map to store value -> index
    
    Algorithm Steps:
    1. Create empty hash map to store {value: index}
    2. For each number at index i:
       a. Calculate complement = target - current_number
       b. Check if complement exists in hash map
       c. If yes: return [hash_map[complement], i]
       d. If no: store current_number -> i in hash map
    3. Continue until pair found
    
    Why this works:
    - For each num, we check if (target - num) was seen before
    - Hash map provides O(1) lookup time
    - We only need one pass through the array
    
    Time: O(n) - single pass through array
    Space: O(n) - hash map stores up to n elements
    """
    seen = {}  # {value: index}
    
    for i, num in enumerate(nums):
        complement = target - num  # What number do we need?
        
        if complement in seen:  # Found the pair!
            return [seen[complement], i]
        
        seen[num] = i  # Store current number for future lookups
    
    return []  # No solution found


# 2. Best Time to Buy and Sell Stock
# PATTERN: Greedy / Single Pass
def max_profit(prices):
    """
    Maximum profit from one buy and one sell transaction.
    
    Problem: Find max profit from buying on one day and selling on a later day.
    Input: prices = [7,1,5,3,6,4]
    Output: 5 (buy at 1, sell at 6, profit = 6-1 = 5)
    
    Pattern: Greedy - track running min and max profit
    Approach: Track minimum price seen so far and max profit
    
    Algorithm Steps:
    1. Initialize min_price = infinity (haven't seen any price yet)
    2. Initialize max_profit = 0 (no transaction = no profit)
    3. For each price in the array:
       a. Calculate potential profit = current_price - min_price
       b. Update max_profit if this profit is larger
       c. Update min_price if current price is smaller
    4. Return max_profit
    
    Why this works:
    - We want to buy low and sell high
    - For each price, check: what if we sell today?
    - Profit would be: today's price - cheapest price seen so far
    - Track the maximum such profit
    
    Time: O(n) - single pass
    Space: O(1) - only two variables
    """
    if not prices:
        return 0
    
    min_price = float('inf')  # Cheapest price seen so far
    max_profit = 0  # Best profit found so far
    
    for price in prices:
        # If we sell at this price, what's our profit?
        profit = price - min_price
        
        # Update our best profit if this is better
        if profit > max_profit:
            max_profit = profit
        
        # Update minimum price if this is cheaper
        if price < min_price:
            min_price = price
    
    return max_profit


# 3. Contains Duplicate
# PATTERN: Hash Set
def contains_duplicate(nums):
    """
    Check if array contains any duplicates.
    
    Pattern: Hash Set for O(1) lookup
    Approach: Use set to track seen elements
    Time: O(n), Space: O(n)
    """
    return len(nums) != len(set(nums))


# 4. Product of Array Except Self
# PATTERN: Prefix/Suffix Products
def product_except_self(nums):
    """
    Return array where output[i] = product of all elements except nums[i].
    Constraint: No division allowed, must be O(n).
    
    Problem: For each position, calculate product of all other elements.
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]
    
    Pattern: Prefix/Suffix products in two passes
    Explanation: 
    - output[0] = 2*3*4 = 24
    - output[1] = 1*3*4 = 12
    - output[2] = 1*2*4 = 8
    - output[3] = 1*2*3 = 6
    
    Approach: Two-pass with prefix and suffix products
    
    Algorithm Steps:
    1. PASS 1 (Left to Right) - Prefix Products:
       - result[0] = 1 (no elements to the left)
       - result[1] = nums[0]
       - result[2] = nums[0] * nums[1]
       - result[i] = product of all elements before i
    
    2. PASS 2 (Right to Left) - Suffix Products:
       - Multiply result[i] by product of all elements after i
       - Build suffix product on the fly
    
    Example walkthrough for [1,2,3,4]:
    After pass 1: [1, 1, 2, 6]  (prefix products)
    After pass 2: [24, 12, 8, 6]  (multiply by suffix products)
    
    Why this works:
    - result[i] needs product of elements before i AND after i
    - Prefix pass: captures all elements to the left
    - Suffix pass: multiplies by all elements to the right
    - Together: gives product of all except i
    
    Time: O(n) - two passes
    Space: O(1) - excluding output array (which doesn't count per problem)
    """
    n = len(nums)
    result = [1] * n
    
    # PASS 1: Build prefix products (left to right)
    prefix = 1
    for i in range(n):
        result[i] = prefix  # Product of all elements before i
        prefix *= nums[i]  # Include current element for next iteration
    
    # PASS 2: Multiply by suffix products (right to left)
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix  # Multiply by product of all elements after i
        suffix *= nums[i]  # Include current element for next iteration
    
    return result


# 5. Maximum Subarray (Kadane's Algorithm)
# PATTERN: Dynamic Programming / Kadane's Algorithm
def max_subarray(nums):
    """
    Find contiguous subarray with largest sum.
    
    Problem: Find the contiguous subarray with the maximum sum.
    Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
    Output: 6 (subarray [4,-1,2,1] has the largest sum)
    
    Pattern: Dynamic Programming (Kadane's Algorithm)
    Approach: Kadane's Algorithm - Dynamic Programming
    
    Algorithm Steps:
    1. Initialize current_sum = nums[0] (best sum ending at position 0)
    2. Initialize max_sum = nums[0] (overall best sum found)
    3. For each element from index 1 to n-1:
       a. Decide: extend current subarray OR start fresh from current element
       b. current_sum = max(current_element, current_sum + current_element)
       c. Update max_sum if current_sum is larger
    4. Return max_sum
    
    Key Insight:
    - At each position, we ask: "Should I extend the previous subarray or start new?"
    - Extend if: previous_sum + current > current (previous contribution is positive)
    - Start new if: current > previous_sum + current (previous drags us down)
    
    Example walkthrough [-2,1,-3,4,-1,2,1,-5,4]:
    i=0: current=-2, max=-2
    i=1: current=max(1, -2+1)=1, max=1  (start fresh)
    i=2: current=max(-3, 1-3)=-2, max=1  (extend but negative)
    i=3: current=max(4, -2+4)=4, max=4  (start fresh)
    i=4: current=max(-1, 4-1)=3, max=4  (extend)
    i=5: current=max(2, 3+2)=5, max=5  (extend)
    i=6: current=max(1, 5+1)=6, max=6  (extend)
    i=7: current=max(-5, 6-5)=1, max=6  (extend)
    i=8: current=max(4, 1+4)=5, max=6  (extend)
    
    Time: O(n) - single pass
    Space: O(1) - only two variables
    """
    if not nums:
        return 0
    
    current_sum = max_sum = nums[0]
    
    for num in nums[1:]:
        # Extend current subarray or start new one?
        current_sum = max(num, current_sum + num)
        
        # Update global maximum
        max_sum = max(max_sum, current_sum)
    
    return max_sum


# 6. Maximum Product Subarray
# PATTERN: Dynamic Programming (Track Max/Min)
def max_product(nums):
    """
    Find contiguous subarray with largest product.
    
    Pattern: Dynamic Programming with state tracking (max and min)
    Approach: Track both max and min products (negatives can flip)
    Steps:
    1. Maintain max_prod and min_prod ending at current position
    2. For each num, compute candidates: num, num*max_prod, num*min_prod
    3. Update max_prod = max(candidates), min_prod = min(candidates)
    4. Track global maximum
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        candidates = (num, num * max_prod, num * min_prod)
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    return result


# 7. Find Minimum in Rotated Sorted Array
# PATTERN: Binary Search (Modified)
def find_min(nums):
    """
    Find minimum in rotated sorted array (no duplicates).
    
    Pattern: Modified Binary Search on rotated array
    Approach: Binary search
    Steps:
    1. If nums[left] < nums[right], array not rotated, return nums[left]
    2. Binary search: compare mid with right
    3. If nums[mid] > nums[right], min is in right half
    4. Otherwise, min is in left half (including mid)
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] < nums[right]:
            return nums[left]
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]


# 8. Search in Rotated Sorted Array
# PATTERN: Binary Search (Modified)
def search(nums, target):
    """
    Search target in rotated sorted array, return index or -1.
    
    Pattern: Modified Binary Search with pivot detection
    Approach: Modified binary search
    Steps:
    1. Find which half is properly sorted
    2. Check if target lies in sorted half
    3. Adjust left/right pointers accordingly
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


# 9. 3Sum
# PATTERN: Two Pointers
def three_sum(nums):
    """
    Find all unique triplets that sum to zero.
    
    Problem: Find all unique triplets [nums[i], nums[j], nums[k]] where i≠j≠k and sum = 0.
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2], [-1,0,1]]
    
    Pattern: Two Pointers (after sorting)
    Approach: Sort + Two Pointers
    
    Algorithm Steps:
    1. Sort the array (enables two-pointer technique and duplicate skipping)
    2. For each element at index i (first element of triplet):
       a. Skip duplicates for i (if nums[i] == nums[i-1])
       b. Use two pointers: left = i+1, right = n-1
       c. While left < right:
          - Calculate sum = nums[i] + nums[left] + nums[right]
          - If sum == 0: found a triplet!
            * Add to result
            * Skip duplicates for left and right
            * Move both pointers inward
          - If sum < 0: need larger sum → move left pointer right
          - If sum > 0: need smaller sum → move right pointer left
    3. Return all found triplets
    
    Why this works:
    - Sorting allows us to use two pointers efficiently
    - For each fixed first element, problem reduces to Two Sum
    - Skip duplicates to ensure unique triplets
    - Two pointers converge from both ends based on sum comparison
    
    Example walkthrough [-1,0,1,2,-1,-4]:
    After sort: [-4,-1,-1,0,1,2]
    i=0 (val=-4): left=-1, right=2, sum=-1 (skip, too small)
    i=1 (val=-1): 
      - left=-1, right=2, sum=0 ✓ Found [-1,-1,2]
      - left=0, right=1, sum=0 ✓ Found [-1,0,1]
    
    Time: O(n²) - O(n log n) sort + O(n) for each of n elements
    Space: O(1) - excluding output (sorting in-place)
    """
    nums.sort()  # STEP 1: Sort to enable two-pointer technique
    result = []
    n = len(nums)
    
    # STEP 2: Fix first element, find two others
    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two pointers for remaining elements
        left, right = i + 1, n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                # Found a valid triplet!
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for left pointer
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                
                # Skip duplicates for right pointer
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                # Move both pointers
                left += 1
                right -= 1
                
            elif total < 0:
                # Sum too small, need larger left value
                left += 1
            else:
                # Sum too large, need smaller right value
                right -= 1
    
    return result


# 10. Container With Most Water
# PATTERN: Two Pointers
def max_area(height):
    """
    Find two lines that form container with most water.
    
    Pattern: Two Pointers (converging from ends)
    Approach: Two pointers from both ends
    Steps:
    1. Start with widest container (left=0, right=n-1)
    2. Calculate area = min(height[left], height[right]) * (right - left)
    3. Move pointer with smaller height inward (potential for taller line)
    4. Track maximum area
    
    Intuition: Width decreases, so need taller lines to improve area
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        water = min(height[left], height[right]) * width
        max_water = max(max_water, water)
        
        # Move pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water


if __name__ == "__main__":
    print("=" * 60)
    print("BLIND 75 - ARRAY PROBLEMS")
    print("=" * 60)
    print()
    
    # Two Sum
    print("1. TWO SUM")
    print("-" * 60)
    test_nums = [2, 7, 11, 15]
    test_target = 9
    print(f"Input: nums = {test_nums}, target = {test_target}")
    print(f"Output: {two_sum(test_nums, test_target)}")
    print(f"Explanation: nums[0] + nums[1] = {test_nums[0]} + {test_nums[1]} = {test_target}")
    print()
    
    # Best Time to Buy and Sell Stock
    print("2. BEST TIME TO BUY AND SELL STOCK")
    print("-" * 60)
    prices = [7, 1, 5, 3, 6, 4]
    print(f"Input: prices = {prices}")
    print(f"Output: {max_profit(prices)}")
    print("Explanation: Buy on day 2 (price=1) and sell on day 5 (price=6), profit = 6-1 = 5")
    print()
    
    # Contains Duplicate
    print("3. CONTAINS DUPLICATE")
    print("-" * 60)
    test_array = [1, 2, 3, 1]
    print(f"Input: nums = {test_array}")
    print(f"Output: {contains_duplicate(test_array)}")
    print("Explanation: Element 1 appears twice")
    print()
    
    # Product of Array Except Self
    print("4. PRODUCT OF ARRAY EXCEPT SELF")
    print("-" * 60)
    test_nums = [1, 2, 3, 4]
    print(f"Input: nums = {test_nums}")
    print(f"Output: {product_except_self(test_nums)}")
    print("Explanation: [2×3×4, 1×3×4, 1×2×4, 1×2×3] = [24, 12, 8, 6]")
    print()
    
    # Maximum Subarray
    print("5. MAXIMUM SUBARRAY (Kadane's Algorithm)")
    print("-" * 60)
    test_nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Input: nums = {test_nums}")
    print(f"Output: {max_subarray(test_nums)}")
    print("Explanation: Subarray [4,-1,2,1] has the largest sum = 6")
    print()
    
    # Maximum Product Subarray
    print("6. MAXIMUM PRODUCT SUBARRAY")
    print("-" * 60)
    test_nums = [2, 3, -2, 4]
    print(f"Input: nums = {test_nums}")
    print(f"Output: {max_product(test_nums)}")
    print("Explanation: Subarray [2,3] has the largest product = 6")
    print()
    
    # Find Minimum in Rotated Sorted Array
    print("7. FIND MINIMUM IN ROTATED SORTED ARRAY")
    print("-" * 60)
    test_nums = [3, 4, 5, 1, 2]
    print(f"Input: nums = {test_nums}")
    print(f"Output: {find_min(test_nums)}")
    print("Explanation: Original array [1,2,3,4,5] was rotated 3 times")
    print()
    
    # Search in Rotated Sorted Array
    print("8. SEARCH IN ROTATED SORTED ARRAY")
    print("-" * 60)
    test_nums = [4, 5, 6, 7, 0, 1, 2]
    test_target = 0
    print(f"Input: nums = {test_nums}, target = {test_target}")
    print(f"Output: {search(test_nums, test_target)}")
    print(f"Explanation: Target {test_target} is at index 4")
    print()
    
    # 3Sum
    print("9. 3SUM")
    print("-" * 60)
    test_nums = [-1, 0, 1, 2, -1, -4]
    print(f"Input: nums = {test_nums}")
    print(f"Output: {three_sum(test_nums)}")
    print("Explanation: Found triplets that sum to 0")
    print()
    
    # Container With Most Water
    print("10. CONTAINER WITH MOST WATER")
    print("-" * 60)
    test_heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Input: height = {test_heights}")
    print(f"Output: {max_area(test_heights)}")
    print("Explanation: Max area between lines at index 1 and 8: min(8,7) × (8-1) = 49")
    print()
    print("=" * 60)
