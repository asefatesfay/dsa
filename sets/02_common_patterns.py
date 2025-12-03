"""
Sets - Common Patterns
======================
Essential patterns and algorithms using sets.
"""

from typing import List, Set
from collections import defaultdict


# Pattern 1: Two Sum (Set approach)
def two_sum_set(nums: List[int], target: int) -> List[int]:
    """
    Find two numbers that add up to target.
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [2,7,11,15], target = 9
        Output: [0,1]
        Explanation: nums[0] + nums[1] = 2 + 7 = 9
    """
    seen = set()  # Track numbers we've seen
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # Check if complement exists in set
        if complement in seen:
            # Find index of complement
            for j, n in enumerate(nums):
                if n == complement and j != i:
                    return [j, i]
        
        seen.add(num)
    
    return []

print("=" * 60)
print("Pattern 1: Two Sum (Set Approach)")
print("=" * 60)
print("Problem: Find indices of two numbers that sum to target")
print("\nHow it works:")
print("  1. Use set to track numbers we've seen")
print("  2. For each number, calculate complement (target - num)")
print("  3. Check if complement exists in set (O(1) lookup)")
print("  4. If found: return indices")
print("  5. If not: add current number to set")
print("\nExample:")
nums = [2, 7, 11, 15]
target = 9
print(f"  Input: nums = {nums}, target = {target}")
result = two_sum_set(nums, target)
print(f"  Output: {result}")
print(f"  Explanation: nums[{result[0]}] + nums[{result[1]}] = {nums[result[0]]} + {nums[result[1]]} = {target}")
print()


# Pattern 2: Contains Duplicate
def contains_duplicate(nums: List[int]) -> bool:
    """
    Check if array contains duplicates.
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [1,2,3,1]
        Output: True
        Explanation: 1 appears twice
    """
    seen = set()
    
    for num in nums:
        if num in seen:
            return True  # Found duplicate
        seen.add(num)
    
    return False

print("=" * 60)
print("Pattern 2: Contains Duplicate")
print("=" * 60)
print("Problem: Check if any value appears at least twice")
print("\nHow it works:")
print("  1. Use set to track seen numbers")
print("  2. For each number:")
print("     - If already in set: found duplicate, return True")
print("     - If not: add to set")
print("  3. If we finish loop: no duplicates, return False")
print("\nExample:")
nums = [1, 2, 3, 1]
print(f"  Input: nums = {nums}")
result = contains_duplicate(nums)
print(f"  Output: {result}")
print(f"  Explanation: 1 appears at index 0 and 3")
print()


# Pattern 3: Intersection of Two Arrays
def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Find intersection of two arrays.
    Time: O(n + m), Space: O(n)
    
    Example:
        Input: nums1 = [1,2,2,1], nums2 = [2,2]
        Output: [2]
        Explanation: 2 appears in both arrays
    """
    # Convert to sets and find intersection
    set1 = set(nums1)
    set2 = set(nums2)
    
    return list(set1 & set2)

print("=" * 60)
print("Pattern 3: Intersection of Two Arrays")
print("=" * 60)
print("Problem: Find elements that appear in both arrays")
print("\nHow it works:")
print("  1. Convert both arrays to sets (removes duplicates)")
print("  2. Use set intersection operator (&)")
print("  3. Result contains elements present in both")
print("  4. Convert back to list")
print("\nExample:")
nums1 = [1, 2, 2, 1]
nums2 = [2, 2]
print(f"  Input: nums1 = {nums1}, nums2 = {nums2}")
result = intersection(nums1, nums2)
print(f"  Output: {result}")
print(f"  Explanation: 2 is the only common element")
print()


# Pattern 4: Happy Number
def is_happy(n: int) -> bool:
    """
    Determine if number is happy.
    Happy: repeatedly sum squares of digits until reaching 1.
    Time: O(log n), Space: O(log n)
    
    Example:
        Input: n = 19
        Output: True
        Explanation: 1² + 9² = 82
                     8² + 2² = 68
                     6² + 8² = 100
                     1² + 0² + 0² = 1
    """
    def get_next(num):
        """Sum of squares of digits"""
        total = 0
        while num > 0:
            digit = num % 10
            total += digit ** 2
            num //= 10
        return total
    
    seen = set()  # Track numbers we've seen
    
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)
    
    return n == 1

print("=" * 60)
print("Pattern 4: Happy Number")
print("=" * 60)
print("Problem: Check if repeatedly summing squares of digits reaches 1")
print("\nHow it works:")
print("  1. Calculate sum of squares of digits")
print("  2. Use set to detect cycles (if we see same number twice)")
print("  3. Keep going until:")
print("     - We reach 1 (happy number)")
print("     - We see a repeated number (cycle, not happy)")
print("\nExample:")
n = 19
print(f"  Input: n = {n}")
result = is_happy(n)
print(f"  Output: {result}")
print(f"  Steps: 19 → 82 → 68 → 100 → 1")
print()


# Pattern 5: Longest Consecutive Sequence
def longest_consecutive(nums: List[int]) -> int:
    """
    Find length of longest consecutive sequence.
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [100,4,200,1,3,2]
        Output: 4
        Explanation: Longest is [1,2,3,4]
    """
    if not nums:
        return 0
    
    num_set = set(nums)  # O(1) lookup
    max_length = 0
    
    for num in num_set:
        # Only start sequence if num is the beginning
        # (num-1 not in set means it's a start)
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # Count consecutive numbers
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            max_length = max(max_length, current_length)
    
    return max_length

print("=" * 60)
print("Pattern 5: Longest Consecutive Sequence")
print("=" * 60)
print("Problem: Find longest sequence of consecutive integers")
print("\nHow it works:")
print("  1. Put all numbers in set for O(1) lookup")
print("  2. For each number:")
print("     - Only start counting if it's sequence start (num-1 not in set)")
print("     - Count how many consecutive numbers exist")
print("  3. This ensures each number visited only once")
print("  4. Track maximum length found")
print("\nExample:")
nums = [100, 4, 200, 1, 3, 2]
print(f"  Input: nums = {nums}")
result = longest_consecutive(nums)
print(f"  Output: {result}")
print(f"  Explanation: Longest consecutive sequence is [1,2,3,4]")
print()


# Pattern 6: Valid Sudoku
def is_valid_sudoku(board: List[List[str]]) -> bool:
    """
    Check if Sudoku board is valid.
    Time: O(1) - fixed 9x9 board, Space: O(1)
    
    Example:
        Input: 9x9 board with some filled cells
        Output: True/False based on Sudoku rules
    """
    # Use sets to track seen numbers in rows, columns, boxes
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                continue
            
            num = board[r][c]
            box_idx = (r // 3) * 3 + (c // 3)
            
            # Check if number already seen
            if num in rows[r] or num in cols[c] or num in boxes[box_idx]:
                return False
            
            # Add to sets
            rows[r].add(num)
            cols[c].add(num)
            boxes[box_idx].add(num)
    
    return True

print("=" * 60)
print("Pattern 6: Valid Sudoku")
print("=" * 60)
print("Problem: Check if partially filled Sudoku board is valid")
print("\nHow it works:")
print("  1. Create sets for each row, column, and 3x3 box")
print("  2. For each filled cell:")
print("     - Check if number already in its row/col/box set")
print("     - If yes: invalid")
print("     - If no: add to all three sets")
print("  3. Box index: (row//3)*3 + (col//3)")
print("\nExample:")
board = [
    ['5','3','.','.','7','.','.','.','.'],
    ['6','.','.','1','9','5','.','.','.'],
    ['.','9','8','.','.','.','.','6','.'],
    ['8','.','.','.','6','.','.','.','3'],
    ['4','.','.','8','.','3','.','.','1'],
    ['7','.','.','.','2','.','.','.','6'],
    ['.','6','.','.','.','.','2','8','.'],
    ['.','.','.','4','1','9','.','.','5'],
    ['.','.','.','.','8','.','.','7','9']
]
print(f"  Input: 9x9 Sudoku board")
result = is_valid_sudoku(board)
print(f"  Output: {result}")
print(f"  Explanation: No duplicates in any row, column, or 3x3 box")
print()


# Pattern 7: Group Anagrams
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams.
    Time: O(n * k log k) where k is max string length
    Space: O(n * k)
    
    Example:
        Input: strs = ["eat","tea","tan","ate","nat","bat"]
        Output: [["eat","tea","ate"],["tan","nat"],["bat"]]
    """
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        # Anagrams will have same sorted key
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())

print("=" * 60)
print("Pattern 7: Group Anagrams")
print("=" * 60)
print("Problem: Group strings that are anagrams of each other")
print("\nHow it works:")
print("  1. Use sorted string as key (anagrams have same sorted form)")
print("  2. Use dictionary to group words by sorted key")
print("  3. 'eat', 'tea', 'ate' all sort to 'aet'")
print("  4. Words with same key are anagrams")
print("\nExample:")
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(f"  Input: {strs}")
result = group_anagrams(strs)
print(f"  Output: {result}")
print(f"  Explanation: 'eat'/'tea'/'ate' are anagrams, 'tan'/'nat' are anagrams")
print()


# Pattern 8: Word Pattern
def word_pattern(pattern: str, s: str) -> bool:
    """
    Check if string follows a pattern.
    Time: O(n), Space: O(n)
    
    Example:
        Input: pattern = "abba", s = "dog cat cat dog"
        Output: True
        Explanation: 'a'→dog, 'b'→cat pattern matches
    """
    words = s.split()
    
    if len(pattern) != len(words):
        return False
    
    char_to_word = {}  # Map pattern char to word
    word_to_char = {}  # Map word to pattern char (bijection)
    
    for char, word in zip(pattern, words):
        # Check char mapping
        if char in char_to_word:
            if char_to_word[char] != word:
                return False
        else:
            char_to_word[char] = word
        
        # Check word mapping (ensure one-to-one)
        if word in word_to_char:
            if word_to_char[word] != char:
                return False
        else:
            word_to_char[word] = char
    
    return True

print("=" * 60)
print("Pattern 8: Word Pattern")
print("=" * 60)
print("Problem: Check if string follows a character pattern")
print("\nHow it works:")
print("  1. Use two dictionaries for bijective mapping")
print("  2. char_to_word: maps pattern char to word")
print("  3. word_to_char: maps word to pattern char")
print("  4. Both mappings must be consistent")
print("  5. Example: 'a'→'dog' and 'dog'→'a' (one-to-one)")
print("\nExample:")
pattern = "abba"
s = "dog cat cat dog"
print(f"  Input: pattern = '{pattern}', s = '{s}'")
result = word_pattern(pattern, s)
print(f"  Output: {result}")
print(f"  Explanation: a→dog, b→cat, b→cat, a→dog (consistent)")
print()


# Pattern 9: Find All Numbers Disappeared in Array
def find_disappeared_numbers(nums: List[int]) -> List[int]:
    """
    Find all numbers from 1 to n that don't appear in array.
    Time: O(n), Space: O(n)
    
    Example:
        Input: nums = [4,3,2,7,8,2,3,1]
        Output: [5,6]
        Explanation: Numbers 5 and 6 are missing
    """
    n = len(nums)
    num_set = set(nums)
    
    missing = []
    for i in range(1, n + 1):
        if i not in num_set:
            missing.append(i)
    
    return missing

print("=" * 60)
print("Pattern 9: Find All Disappeared Numbers")
print("=" * 60)
print("Problem: Find numbers from 1 to n missing from array")
print("\nHow it works:")
print("  1. Convert array to set for O(1) lookup")
print("  2. Check each number from 1 to n")
print("  3. If number not in set: add to result")
print("  4. Set makes membership test very fast")
print("\nExample:")
nums = [4, 3, 2, 7, 8, 2, 3, 1]
print(f"  Input: nums = {nums} (n = {len(nums)})")
result = find_disappeared_numbers(nums)
print(f"  Output: {result}")
print(f"  Explanation: Numbers 1-8, missing 5 and 6")
print()


# Pattern 10: Unique Email Addresses
def num_unique_emails(emails: List[str]) -> int:
    """
    Count unique email addresses.
    Rules: 
      - Ignore dots (.) in local name
      - Ignore everything after plus (+) in local name
      - Domain name unchanged
    Time: O(n * m) where m is avg email length
    Space: O(n * m)
    
    Example:
        Input: ["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com"]
        Output: 2
    """
    unique = set()
    
    for email in emails:
        local, domain = email.split('@')
        
        # Remove dots
        local = local.replace('.', '')
        
        # Remove everything after +
        if '+' in local:
            local = local[:local.index('+')]
        
        # Add normalized email to set
        unique.add(local + '@' + domain)
    
    return len(unique)

print("=" * 60)
print("Pattern 10: Unique Email Addresses")
print("=" * 60)
print("Problem: Count unique emails after applying rules")
print("\nHow it works:")
print("  1. For each email, normalize it:")
print("     - Split into local@domain")
print("     - Remove dots from local part")
print("     - Remove '+' and everything after it")
print("  2. Add normalized email to set")
print("  3. Set automatically handles duplicates")
print("  4. Return size of set")
print("\nExample:")
emails = ["test.email+alex@leetcode.com", "test.e.mail+bob.cathy@leetcode.com", "testemail@leetcode.com"]
print(f"  Input: {len(emails)} emails")
for email in emails:
    print(f"    {email}")
result = num_unique_emails(emails)
print(f"  Output: {result}")
print(f"  Explanation: All normalize to 'testemail@leetcode.com'")
print()
