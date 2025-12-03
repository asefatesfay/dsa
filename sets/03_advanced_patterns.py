"""
Sets - Advanced Patterns
========================
Complex problems using sets with multiple techniques.
"""

from typing import List, Set
from collections import defaultdict, Counter


# Pattern 1: Longest Substring Without Repeating Characters
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    Time: O(n), Space: O(min(n, m)) where m is charset size
    
    Example:
        Input: s = "abcabcbb"
        Output: 3
        Explanation: "abc" is longest without repeats
    """
    char_set = set()  # Track characters in current window
    left = 0  # Left pointer of sliding window
    max_length = 0
    
    for right in range(len(s)):
        # If character already in window, shrink from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character
        char_set.add(s[right])
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length

print("=" * 60)
print("Pattern 1: Longest Substring Without Repeating Characters")
print("=" * 60)
print("Problem: Find longest substring with all unique characters")
print("\nHow it works:")
print("  1. Use sliding window with two pointers")
print("  2. Use set to track characters in current window")
print("  3. Expand right pointer, add character to set")
print("  4. If duplicate found: shrink from left until duplicate removed")
print("  5. Track maximum window size seen")
print("\nExample:")
s = "abcabcbb"
print(f"  Input: s = '{s}'")
result = length_of_longest_substring(s)
print(f"  Output: {result}")
print(f"  Explanation: 'abc' is longest (length 3)")
print()


# Pattern 2: Contains Duplicate II (within k distance)
def contains_nearby_duplicate(nums: List[int], k: int) -> bool:
    """
    Check if duplicate exists within k distance.
    Time: O(n), Space: O(min(n, k))
    
    Example:
        Input: nums = [1,2,3,1], k = 3
        Output: True
        Explanation: nums[0] = nums[3] = 1, distance = 3
    """
    window = set()  # Sliding window of size k
    
    for i, num in enumerate(nums):
        # Check if duplicate in current window
        if num in window:
            return True
        
        # Add to window
        window.add(num)
        
        # Maintain window size k
        if len(window) > k:
            window.remove(nums[i - k])
    
    return False

print("=" * 60)
print("Pattern 2: Contains Nearby Duplicate")
print("=" * 60)
print("Problem: Check if duplicate exists within k indices")
print("\nHow it works:")
print("  1. Use set as sliding window of size k")
print("  2. For each number:")
print("     - Check if already in window (duplicate within k)")
print("     - Add number to window")
print("     - Remove oldest if window exceeds size k")
print("  3. Set provides O(1) lookup and removal")
print("\nExample:")
nums = [1, 2, 3, 1]
k = 3
print(f"  Input: nums = {nums}, k = {k}")
result = contains_nearby_duplicate(nums, k)
print(f"  Output: {result}")
print(f"  Explanation: 1 at index 0 and 3, distance = 3 ≤ k")
print()


# Pattern 3: Longest Substring with At Most K Distinct Characters
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Find longest substring with at most k distinct characters.
    Time: O(n), Space: O(k)
    
    Example:
        Input: s = "eceba", k = 2
        Output: 3
        Explanation: "ece" has 2 distinct chars
    """
    if k == 0:
        return 0
    
    char_count = {}  # Track character counts in window
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Add character to window
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if too many distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

print("=" * 60)
print("Pattern 3: Longest Substring with K Distinct Characters")
print("=" * 60)
print("Problem: Find longest substring with at most k distinct characters")
print("\nHow it works:")
print("  1. Use sliding window with character count map")
print("  2. Expand right: add character, update count")
print("  3. If distinct chars > k: shrink from left")
print("     - Decrease count, remove if count becomes 0")
print("  4. Track maximum valid window size")
print("\nExample:")
s = "eceba"
k = 2
print(f"  Input: s = '{s}', k = {k}")
result = length_of_longest_substring_k_distinct(s, k)
print(f"  Output: {result}")
print(f"  Explanation: 'ece' has 2 distinct characters (e, c)")
print()


# Pattern 4: Subarray Sum Equals K (using set)
def subarray_sum_with_set(nums: List[int], k: int) -> bool:
    """
    Check if there's a subarray with sum equal to k.
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [1,2,3,4,5], k = 9
        Output: True
        Explanation: [2,3,4] sums to 9
    """
    # Use prefix sum with set
    prefix_sum = 0
    sum_set = {0}  # Include 0 for subarrays starting at index 0
    
    for num in nums:
        prefix_sum += num
        
        # Check if (prefix_sum - k) exists
        # If yes: there's a subarray with sum k
        if prefix_sum - k in sum_set:
            return True
        
        sum_set.add(prefix_sum)
    
    return False

print("=" * 60)
print("Pattern 4: Subarray Sum Equals K")
print("=" * 60)
print("Problem: Check if any contiguous subarray sums to k")
print("\nHow it works:")
print("  1. Use prefix sum: sum of elements from start to current")
print("  2. Store all prefix sums in set")
print("  3. For current prefix_sum:")
print("     - If (prefix_sum - k) in set: found subarray!")
print("     - Why? Because sum[i..j] = prefix[j] - prefix[i-1]")
print("  4. Add current prefix sum to set")
print("\nExample:")
nums = [1, 2, 3, 4, 5]
k = 9
print(f"  Input: nums = {nums}, k = {k}")
result = subarray_sum_with_set(nums, k)
print(f"  Output: {result}")
print(f"  Explanation: Subarray [2,3,4] has sum = 9")
print()


# Pattern 5: Distribute Candies (maximize types)
def distribute_candies(candy_type: List[int]) -> int:
    """
    Find maximum candy types Alice can eat (can eat n/2 candies).
    Time: O(n), Space: O(n)
    
    Example:
        Input: candy_type = [1,1,2,2,3,3]
        Output: 3
        Explanation: Can eat 3 candies, 3 types available
    """
    # Count unique types
    unique_types = len(set(candy_type))
    
    # Can eat at most n/2 candies
    max_eat = len(candy_type) // 2
    
    # Return minimum of unique types and max can eat
    return min(unique_types, max_eat)

print("=" * 60)
print("Pattern 5: Distribute Candies")
print("=" * 60)
print("Problem: Maximize candy types when eating n/2 candies")
print("\nHow it works:")
print("  1. Count unique candy types using set")
print("  2. Calculate max candies can eat: n/2")
print("  3. Answer is min(unique_types, n/2)")
print("     - If more types than slots: eat n/2 different types")
print("     - If fewer types: eat all unique types")
print("\nExample:")
candy_type = [1, 1, 2, 2, 3, 3]
print(f"  Input: candy_type = {candy_type}")
result = distribute_candies(candy_type)
print(f"  Output: {result}")
print(f"  Explanation: Can eat 3 candies, 3 types exist, eat 1 of each")
print()


# Pattern 6: Jewels and Stones
def num_jewels_in_stones(jewels: str, stones: str) -> int:
    """
    Count how many stones are jewels.
    Time: O(j + s), Space: O(j)
    
    Example:
        Input: jewels = "aA", stones = "aAAbbbb"
        Output: 3
        Explanation: 'a' and two 'A's are jewels
    """
    jewel_set = set(jewels)  # O(1) lookup
    
    count = 0
    for stone in stones:
        if stone in jewel_set:
            count += 1
    
    return count

print("=" * 60)
print("Pattern 6: Jewels and Stones")
print("=" * 60)
print("Problem: Count stones that are jewels (case-sensitive)")
print("\nHow it works:")
print("  1. Convert jewels to set for O(1) lookup")
print("  2. For each stone: check if it's a jewel")
print("  3. Count matches")
print("  4. Set makes checking much faster than scanning jewels string")
print("\nExample:")
jewels = "aA"
stones = "aAAbbbb"
print(f"  Input: jewels = '{jewels}', stones = '{stones}'")
result = num_jewels_in_stones(jewels, stones)
print(f"  Output: {result}")
print(f"  Explanation: 'a' (1x) and 'A' (2x) are jewels")
print()


# Pattern 7: Find All Duplicates in Array
def find_duplicates(nums: List[int]) -> List[int]:
    """
    Find all numbers that appear twice.
    Numbers in range [1, n] where n = len(nums)
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [4,3,2,7,8,2,3,1]
        Output: [2,3]
    """
    seen = set()
    duplicates = set()
    
    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)

print("=" * 60)
print("Pattern 7: Find All Duplicates")
print("=" * 60)
print("Problem: Find all numbers that appear twice")
print("\nHow it works:")
print("  1. Use two sets:")
print("     - seen: tracks numbers we've encountered")
print("     - duplicates: tracks numbers seen twice")
print("  2. For each number:")
print("     - If in seen: add to duplicates")
print("     - If not: add to seen")
print("  3. Using set for duplicates prevents counting same number multiple times")
print("\nExample:")
nums = [4, 3, 2, 7, 8, 2, 3, 1]
print(f"  Input: nums = {nums}")
result = find_duplicates(nums)
print(f"  Output: {result}")
print(f"  Explanation: 2 and 3 each appear twice")
print()


# Pattern 8: Bulls and Cows
def get_hint(secret: str, guess: str) -> str:
    """
    Compare secret and guess to find bulls and cows.
    Bulls: correct digit in correct position
    Cows: correct digit in wrong position
    Time: O(n), Space: O(1) - limited to 10 digits
    
    Example:
        Input: secret = "1807", guess = "7810"
        Output: "1A3B"
        Explanation: 1 bull (8), 3 cows (1,7,0)
    """
    bulls = 0
    secret_counts = Counter()
    guess_counts = Counter()
    
    # First pass: count bulls
    for i in range(len(secret)):
        if secret[i] == guess[i]:
            bulls += 1
        else:
            # Track non-bull digits
            secret_counts[secret[i]] += 1
            guess_counts[guess[i]] += 1
    
    # Second pass: count cows (intersection of remaining digits)
    cows = 0
    for digit in guess_counts:
        # Min of counts in secret and guess
        cows += min(secret_counts[digit], guess_counts[digit])
    
    return f"{bulls}A{cows}B"

print("=" * 60)
print("Pattern 8: Bulls and Cows")
print("=" * 60)
print("Problem: Count bulls (correct position) and cows (wrong position)")
print("\nHow it works:")
print("  1. First pass: count exact matches (bulls)")
print("  2. Track non-matching digits from both strings")
print("  3. Second pass: count cows")
print("     - For each digit: min(secret_count, guess_count)")
print("     - This gives correct digit in wrong position")
print("\nExample:")
secret = "1807"
guess = "7810"
print(f"  Input: secret = '{secret}', guess = '{guess}'")
result = get_hint(secret, guess)
print(f"  Output: '{result}'")
print(f"  Explanation: 1 bull (8 at position 1), 3 cows (1,7,0)")
print()


# Pattern 9: Max Number of K-Sum Pairs
def max_operations(nums: List[int], k: int) -> int:
    """
    Find max pairs that sum to k (each number used once).
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [1,2,3,4], k = 5
        Output: 2
        Explanation: Pairs (1,4) and (2,3)
    """
    num_count = Counter(nums)  # Count occurrences
    operations = 0
    
    for num in num_count:
        complement = k - num
        
        if complement in num_count:
            if num == complement:
                # Special case: need pairs of same number
                operations += num_count[num] // 2
            else:
                # Take minimum of both counts
                operations += min(num_count[num], num_count[complement])
    
    # Divide by 2 since we count each pair twice (except for num == complement)
    # Actually, we need to be more careful
    return operations // 2 if operations > 0 else 0

def max_operations_correct(nums: List[int], k: int) -> int:
    """Correct implementation"""
    num_count = Counter(nums)
    operations = 0
    
    for num in list(num_count.keys()):
        if num_count[num] == 0:
            continue
            
        complement = k - num
        
        if complement == num:
            # Pair same numbers: can make count//2 pairs
            operations += num_count[num] // 2
            num_count[num] = 0
        elif complement in num_count:
            # Pair different numbers: take min count
            pairs = min(num_count[num], num_count[complement])
            operations += pairs
            num_count[num] = 0
            num_count[complement] = 0
    
    return operations

print("=" * 60)
print("Pattern 9: Max Number of K-Sum Pairs")
print("=" * 60)
print("Problem: Maximum pairs that sum to k (use each number once)")
print("\nHow it works:")
print("  1. Count frequency of each number")
print("  2. For each unique number:")
print("     - Calculate complement (k - num)")
print("     - If complement exists:")
print("       * Same number: pairs = count // 2")
print("       * Different: pairs = min(count_num, count_complement)")
print("  3. Mark used numbers to avoid double counting")
print("\nExample:")
nums = [1, 2, 3, 4]
k = 5
print(f"  Input: nums = {nums}, k = {k}")
result = max_operations_correct(nums, k)
print(f"  Output: {result}")
print(f"  Explanation: Pairs (1,4) and (2,3) both sum to 5")
print()


# Pattern 10: Powerful Integers
def powerful_integers(x: int, y: int, bound: int) -> List[int]:
    """
    Find all unique x^i + y^j <= bound.
    Time: O(log(bound)^2), Space: O(log(bound)^2)
    
    Example:
        Input: x = 2, y = 3, bound = 10
        Output: [2,3,4,5,7,9,10]
    """
    result = set()  # Use set to avoid duplicates
    
    # Try all combinations of powers
    x_power = 1
    for i in range(20):  # log2(bound) should be enough
        if x_power > bound:
            break
            
        y_power = 1
        for j in range(20):
            value = x_power + y_power
            
            if value <= bound:
                result.add(value)
            
            if y_power > bound:
                break
            
            # Handle y = 1 case (infinite loop prevention)
            if y == 1:
                break
            y_power *= y
        
        # Handle x = 1 case
        if x == 1:
            break
        x_power *= x
    
    return sorted(result)

print("=" * 60)
print("Pattern 10: Powerful Integers")
print("=" * 60)
print("Problem: Find all unique sums x^i + y^j <= bound")
print("\nHow it works:")
print("  1. Try all combinations of powers i and j")
print("  2. Use set to automatically handle duplicates")
print("     - Important when x=1 or y=1 (1^i = 1 for all i)")
print("  3. Stop when power exceeds bound")
print("  4. Return sorted unique values")
print("\nExample:")
x, y, bound = 2, 3, 10
print(f"  Input: x = {x}, y = {y}, bound = {bound}")
result = powerful_integers(x, y, bound)
print(f"  Output: {result}")
print(f"  Explanation: 2^0+3^0=2, 2^1+3^0=3, 2^0+3^1=4, 2^2+3^0=5, etc.")
print()
