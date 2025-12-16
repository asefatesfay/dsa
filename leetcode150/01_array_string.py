"""
LeetCode 150 - Array/String Problems
====================================
Essential array and string manipulation problems.
"""


# PATTERN: Two Pointers
def merge_sorted_array(nums1, m, nums2, n):
    """
    Merge nums2 into nums1 (nums1 has size m+n).
    
    Pattern: Two pointers from end (reverse merge)
    
    Problem: Merge two sorted arrays in-place
    Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
    Output: [1,2,2,3,5,6]
    
    Algorithm Steps:
    1. Start from the end of both arrays
    2. Compare elements and place larger one at end of nums1
    3. Move pointers backward
    4. Copy remaining nums2 elements if any
    
    Time: O(m+n), Space: O(1)
    """
    i, j, k = m - 1, n - 1, m + n - 1
    
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    
    # Copy remaining nums2 elements
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1


# PATTERN: Two Pointers
def remove_element(nums, val):
    """
    Remove all occurrences of val in-place.
    
    Pattern: Two pointers (fast/slow)
    
    Algorithm Steps:
    1. Use slow pointer for next position to write
    2. Use fast pointer to scan array
    3. Copy non-val elements to slow position
    
    Time: O(n), Space: O(1)
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow


# PATTERN: Two Pointers
def remove_duplicates(nums):
    """
    Remove duplicates from sorted array, return new length.
    
    Pattern: Two pointers (slow writes unique, fast scans)
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


# PATTERN: Two Pointers
def remove_duplicates_ii(nums):
    """
    Allow at most 2 duplicates in sorted array.
    
    Pattern: Two pointers with count tracking
    
    Algorithm Steps:
    1. Keep first two elements as-is
    2. For remaining elements, check if different from nums[slow-1]
    3. If different, safe to add (won't exceed 2 duplicates)
    
    Time: O(n), Space: O(1)
    """
    if len(nums) <= 2:
        return len(nums)
    
    slow = 2
    for fast in range(2, len(nums)):
        if nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1
    return slow


# PATTERN: Hash Map / Boyer-Moore Voting
def majority_element(nums):
    """
    Find element appearing more than n/2 times.
    
    Pattern: Boyer-Moore Voting Algorithm
    
    Algorithm Steps:
    1. Maintain candidate and count
    2. If count == 0, set current element as candidate
    3. Increment count if same, decrement if different
    4. Majority element will survive
    
    Why it works: Majority element appears > n/2 times,
    so even if all other elements cancel it out, it remains.
    
    Time: O(n), Space: O(1)
    """
    candidate, count = None, 0
    
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    
    return candidate


# PATTERN: Array Rotation / Reversal
def rotate_array(nums, k):
    """
    Rotate array to right by k steps.
    
    Pattern: Three reversals
    
    Algorithm Steps:
    1. Reverse entire array
    2. Reverse first k elements
    3. Reverse remaining elements
    
    Example: [1,2,3,4,5,6,7], k=3
    - After reverse all: [7,6,5,4,3,2,1]
    - After reverse [:3]: [5,6,7,4,3,2,1]
    - After reverse [3:]: [5,6,7,1,2,3,4]
    
    Time: O(n), Space: O(1)
    """
    n = len(nums)
    k = k % n  # Handle k > n
    
    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
    
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


# PATTERN: Greedy
def max_profit(prices):
    """
    Best Time to Buy and Sell Stock (single transaction).
    
    Pattern: Greedy - track minimum price
    
    Time: O(n), Space: O(1)
    """
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit


# PATTERN: Greedy
def max_profit_ii(prices):
    """
    Best Time to Buy and Sell Stock II (multiple transactions).
    
    Pattern: Greedy - capture every upward movement
    
    Algorithm Steps:
    1. Add up all positive differences
    2. Each upward price change = profit opportunity
    
    Time: O(n), Space: O(1)
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit


# PATTERN: Dynamic Programming (State Machine)
def max_profit_iii(prices):
    """
    Best Time to Buy and Sell Stock III (at most 2 transactions).
    
    Pattern: DP with states (buy1, sell1, buy2, sell2)
    
    Algorithm Steps:
    1. Track best profit after each state
    2. buy1: min cost of first purchase
    3. sell1: max profit after first sale
    4. buy2: max profit after second purchase (using sell1 profit)
    5. sell2: max profit after second sale
    
    Time: O(n), Space: O(1)
    """
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0
    
    for price in prices:
        buy1 = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2 = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)
    
    return sell2


# PATTERN: Greedy / Dynamic Programming
def can_jump(nums):
    """
    Jump Game - check if can reach last index.
    
    Pattern: Greedy - track farthest reachable
    
    Time: O(n), Space: O(1)
    """
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True


# PATTERN: Greedy
def jump(nums):
    """
    Jump Game II - minimum jumps to reach end.
    
    Pattern: Greedy BFS-like approach
    
    Algorithm Steps:
    1. Track current jump's end and farthest reach
    2. When reach current end, must make a jump
    3. Update end to farthest reachable
    
    Time: O(n), Space: O(1)
    """
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    
    return jumps


# PATTERN: Sorting / Counting
def h_index(citations):
    """
    H-Index: researcher has h papers with >= h citations each.
    
    Pattern: Sorting or counting
    
    Algorithm Steps:
    1. Sort citations in descending order
    2. Find largest h where citations[h-1] >= h
    
    Time: O(n log n), Space: O(1)
    """
    citations.sort(reverse=True)
    h = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h = i + 1
        else:
            break
    return h


# PATTERN: Hash Map + Random
class RandomizedSet:
    """
    Insert, Delete, GetRandom O(1).
    
    Pattern: Hash map + Dynamic array
    
    Design:
    - Hash map: val -> index in array
    - Array: stores values for O(1) random access
    - Delete: swap with last element, then pop
    """
    
    def __init__(self):
        self.val_to_idx = {}
        self.vals = []
    
    def insert(self, val):
        if val in self.val_to_idx:
            return False
        self.val_to_idx[val] = len(self.vals)
        self.vals.append(val)
        return True
    
    def remove(self, val):
        if val not in self.val_to_idx:
            return False
        # Swap with last element
        idx = self.val_to_idx[val]
        last_val = self.vals[-1]
        self.vals[idx] = last_val
        self.val_to_idx[last_val] = idx
        # Remove last
        self.vals.pop()
        del self.val_to_idx[val]
        return True
    
    def getRandom(self):
        import random
        return random.choice(self.vals)


# PATTERN: Prefix/Suffix Products
def product_except_self(nums):
    """
    Product of array except self (no division allowed).
    
    Pattern: Prefix and suffix products
    
    Time: O(n), Space: O(1) excluding output
    """
    n = len(nums)
    result = [1] * n
    
    # Left pass: result[i] = product of all elements to left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # Right pass: multiply by product of all elements to right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result


# PATTERN: Greedy
def can_complete_circuit(gas, cost):
    """
    Gas Station - find starting station to complete circuit.
    
    Pattern: Greedy with total balance check
    
    Algorithm Steps:
    1. If total gas < total cost, impossible
    2. Track current tank and starting position
    3. If tank negative, can't start from any previous position
    4. Reset start position to next station
    
    Time: O(n), Space: O(1)
    """
    if sum(gas) < sum(cost):
        return -1
    
    tank = 0
    start = 0
    
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            tank = 0
            start = i + 1
    
    return start


# PATTERN: Greedy
def candy(ratings):
    """
    Candy - minimum candies (higher rating gets more than neighbors).
    
    Pattern: Two-pass greedy
    
    Algorithm Steps:
    1. Left pass: if rating[i] > rating[i-1], candy[i] = candy[i-1] + 1
    2. Right pass: if rating[i] > rating[i+1], candy[i] = max(candy[i], candy[i+1] + 1)
    
    Time: O(n), Space: O(n)
    """
    n = len(ratings)
    candies = [1] * n
    
    # Left to right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    
    # Right to left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    
    return sum(candies)


# PATTERN: Two Pointers / Stack
def trap(height):
    """
    Trapping Rain Water.
    
    Pattern: Two pointers with max heights
    
    Algorithm Steps:
    1. Use two pointers from both ends
    2. Track left_max and right_max
    3. Water at position = min(left_max, right_max) - height
    4. Move pointer with smaller max
    
    Time: O(n), Space: O(1)
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water


# PATTERN: Hash Map
def roman_to_int(s):
    """
    Roman to Integer conversion.
    
    Pattern: Hash map with subtraction rule
    
    Algorithm Steps:
    1. Map symbols to values
    2. If current < next, subtract (e.g., IV = 4)
    3. Otherwise, add
    
    Time: O(n), Space: O(1)
    """
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    
    for i in range(len(s)):
        if i + 1 < len(s) and roman[s[i]] < roman[s[i + 1]]:
            result -= roman[s[i]]
        else:
            result += roman[s[i]]
    
    return result


# PATTERN: Greedy
def int_to_roman(num):
    """
    Integer to Roman conversion.
    
    Pattern: Greedy with value-symbol pairs
    
    Time: O(1), Space: O(1)
    """
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = []
    for i, value in enumerate(values):
        count = num // value
        if count:
            result.append(symbols[i] * count)
            num -= value * count
    
    return ''.join(result)


# PATTERN: String Traversal
def length_of_last_word(s):
    """
    Length of last word in string.
    
    Pattern: Traverse from end, skip spaces
    
    Time: O(n), Space: O(1)
    """
    i = len(s) - 1
    # Skip trailing spaces
    while i >= 0 and s[i] == ' ':
        i -= 1
    # Count word length
    length = 0
    while i >= 0 and s[i] != ' ':
        length += 1
        i -= 1
    return length


# PATTERN: String Comparison
def longest_common_prefix(strs):
    """
    Longest common prefix among strings.
    
    Pattern: Vertical scanning
    
    Time: O(S) where S = sum of all characters, Space: O(1)
    """
    if not strs:
        return ""
    
    for i in range(len(strs[0])):
        char = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != char:
                return strs[0][:i]
    
    return strs[0]


# PATTERN: Two Pointers
def reverse_words(s):
    """
    Reverse words in a string.
    
    Pattern: Split, reverse, join
    
    Time: O(n), Space: O(n)
    """
    return ' '.join(reversed(s.split()))


if __name__ == "__main__":
    print("=== LeetCode 150 - Array/String Problems ===\n")
    
    # Merge Sorted Array
    nums1 = [1, 2, 3, 0, 0, 0]
    merge_sorted_array(nums1, 3, [2, 5, 6], 3)
    print(f"Merge Sorted Array: {nums1}")
    
    # Remove Element
    nums = [3, 2, 2, 3]
    print(f"Remove Element (val=3): length={remove_element(nums, 3)}, array={nums[:2]}")
    
    # Majority Element
    print(f"Majority Element [2,2,1,1,1,2,2]: {majority_element([2, 2, 1, 1, 1, 2, 2])}")
    
    # Rotate Array
    nums = [1, 2, 3, 4, 5, 6, 7]
    rotate_array(nums, 3)
    print(f"Rotate Array (k=3): {nums}")
    
    # Product Except Self
    print(f"Product Except Self [1,2,3,4]: {product_except_self([1, 2, 3, 4])}")
    
    # Trapping Rain Water
    print(f"Trap Rain Water [0,1,0,2,1,0,1,3,2,1,2,1]: {trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])}")
    
    # Roman/Integer
    print(f"Roman to Int 'MCMXCIV': {roman_to_int('MCMXCIV')}")
    print(f"Int to Roman 1994: {int_to_roman(1994)}")
    
    # String operations
    print(f"Length of Last Word 'Hello World': {length_of_last_word('Hello World')}")
    print(f"Longest Common Prefix ['flower','flow','flight']: {longest_common_prefix(['flower', 'flow', 'flight'])}")
    print(f"Reverse Words 'the sky is blue': '{reverse_words('the sky is blue')}'")
