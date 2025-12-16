"""
NeetCode 150 - Arrays & Hashing
================================
Core array and hash map problems.
"""


# PATTERN: Hash Set
def contains_duplicate(nums):
    """
    Contains Duplicate - check if any value appears twice.
    
    Pattern: Hash set for O(1) lookups
    
    Time: O(n), Space: O(n)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


# PATTERN: Hash Map (Frequency Counter)
def is_anagram(s, t):
    """
    Valid Anagram - check if two strings are anagrams.
    
    Pattern: Hash map frequency counting
    
    Time: O(n), Space: O(1) - at most 26 letters
    """
    if len(s) != len(t):
        return False
    
    from collections import Counter
    return Counter(s) == Counter(t)


# PATTERN: Hash Map
def two_sum(nums, target):
    """
    Two Sum - find indices of two numbers that sum to target.
    
    Pattern: Hash map to store complements
    
    Algorithm Steps:
    1. For each number, calculate complement = target - num
    2. Check if complement exists in hash map
    3. If yes, return indices
    4. Otherwise, store current number with its index
    
    Time: O(n), Space: O(n)
    """
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []


# PATTERN: Hash Map (Sorted Key)
def group_anagrams(strs):
    """
    Group Anagrams - group strings that are anagrams.
    
    Pattern: Hash map with sorted string as key
    
    Algorithm Steps:
    1. Use sorted string as key
    2. Group all anagrams together
    
    Time: O(n * k log k) where k = max string length
    Space: O(n * k)
    """
    from collections import defaultdict
    
    anagram_map = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    
    return list(anagram_map.values())


# PATTERN: Heap / Bucket Sort
def top_k_frequent(nums, k):
    """
    Top K Frequent Elements.
    
    Pattern: Hash map + Bucket sort or Heap
    
    Algorithm Steps:
    1. Count frequencies with hash map
    2. Use bucket sort: index = frequency, value = numbers
    3. Collect from highest frequency bucket
    
    Time: O(n), Space: O(n)
    """
    from collections import Counter
    
    # Count frequencies
    count = Counter(nums)
    
    # Bucket sort: buckets[i] contains all numbers with frequency i
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Collect from highest frequency
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result


# PATTERN: Prefix/Suffix Products
def product_except_self(nums):
    """
    Product of Array Except Self (no division allowed).
    
    Pattern: Prefix and suffix products
    
    Algorithm Steps:
    1. First pass: result[i] = product of all elements to left
    2. Second pass: multiply by product of all elements to right
    
    Time: O(n), Space: O(1) excluding output
    """
    n = len(nums)
    result = [1] * n
    
    # Left pass
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # Right pass
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result


# PATTERN: Hash Set (Multiple)
def is_valid_sudoku(board):
    """
    Valid Sudoku - check if partially filled 9x9 sudoku is valid.
    
    Pattern: Hash sets for rows, columns, and boxes
    
    Algorithm Steps:
    1. Use 9 sets for rows, 9 for columns, 9 for 3x3 boxes
    2. For each cell, check if number already exists in its row/col/box
    3. Box index = (row // 3) * 3 + (col // 3)
    
    Time: O(81) = O(1), Space: O(81) = O(1)
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                continue
            
            num = board[r][c]
            box_idx = (r // 3) * 3 + (c // 3)
            
            if num in rows[r] or num in cols[c] or num in boxes[box_idx]:
                return False
            
            rows[r].add(num)
            cols[c].add(num)
            boxes[box_idx].add(num)
    
    return True


# PATTERN: String Encoding
def encode(strs):
    """
    Encode list of strings to single string.
    
    Pattern: Length prefix encoding
    
    Format: "4#word5#hello" for ["word", "hello"]
    
    Time: O(n), Space: O(1)
    """
    result = []
    for s in strs:
        result.append(f"{len(s)}#{s}")
    return ''.join(result)


def decode(s):
    """
    Decode string back to list of strings.
    
    Pattern: Parse length prefix
    
    Time: O(n), Space: O(1)
    """
    result = []
    i = 0
    
    while i < len(s):
        # Find delimiter '#'
        j = i
        while s[j] != '#':
            j += 1
        
        # Extract length
        length = int(s[i:j])
        # Extract string
        result.append(s[j + 1:j + 1 + length])
        # Move to next encoded string
        i = j + 1 + length
    
    return result


# PATTERN: Hash Set
def longest_consecutive(nums):
    """
    Longest Consecutive Sequence.
    
    Pattern: Hash set with smart iteration
    
    Algorithm Steps:
    1. Put all numbers in set
    2. For each number, check if it's start of sequence (num-1 not in set)
    3. If start, count consecutive numbers
    
    Why it works: Only counting from sequence starts prevents redundant work
    
    Time: O(n), Space: O(n)
    """
    if not nums:
        return 0
    
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        # Only start counting from sequence beginning
        if num - 1 not in num_set:
            current = num
            length = 1
            
            while current + 1 in num_set:
                current += 1
                length += 1
            
            max_length = max(max_length, length)
    
    return max_length


if __name__ == "__main__":
    print("=== NeetCode 150 - Arrays & Hashing ===\n")
    
    # Contains Duplicate
    print(f"Contains Duplicate [1,2,3,1]: {contains_duplicate([1, 2, 3, 1])}")
    print(f"Contains Duplicate [1,2,3,4]: {contains_duplicate([1, 2, 3, 4])}")
    
    # Valid Anagram
    print(f"Is Anagram 'anagram', 'nagaram': {is_anagram('anagram', 'nagaram')}")
    
    # Two Sum
    print(f"Two Sum [2,7,11,15] target=9: {two_sum([2, 7, 11, 15], 9)}")
    
    # Group Anagrams
    print(f"Group Anagrams ['eat','tea','tan','ate','nat','bat']: {group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])}")
    
    # Top K Frequent
    print(f"Top K Frequent [1,1,1,2,2,3] k=2: {top_k_frequent([1, 1, 1, 2, 2, 3], 2)}")
    
    # Product Except Self
    print(f"Product Except Self [1,2,3,4]: {product_except_self([1, 2, 3, 4])}")
    
    # Valid Sudoku
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    print(f"Valid Sudoku: {is_valid_sudoku(board)}")
    
    # Encode/Decode
    strs = ["hello", "world"]
    encoded = encode(strs)
    print(f"Encode {strs}: '{encoded}'")
    print(f"Decode '{encoded}': {decode(encoded)}")
    
    # Longest Consecutive Sequence
    print(f"Longest Consecutive [100,4,200,1,3,2]: {longest_consecutive([100, 4, 200, 1, 3, 2])}")
