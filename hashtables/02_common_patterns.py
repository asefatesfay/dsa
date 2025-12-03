"""
Hash Table Common Patterns
===========================

Essential patterns and algorithms using hash tables.
Each pattern includes explanation of how it works.
"""

# Pattern 1: Two Sum (Find pair that adds to target)
print("=" * 60)
print("Pattern 1: Two Sum")
print("=" * 60)
print("""
Problem: Given array of integers, find indices of two numbers that add up to target.

How it works:
  1. Create empty hash table to store {number: index}
  2. For each number in array:
     - Calculate complement = target - current_number
     - Check if complement exists in hash table
     - If yes: found the pair! Return both indices
     - If no: store current number and its index
  3. Hash table allows O(1) lookup instead of nested loops
  4. Single pass through array is sufficient

Example:
  Input: nums = [2, 7, 11, 15], target = 9
  Step 1: See 2, need 7. Store {2: 0}
  Step 2: See 7, need 2. Found it at index 0! Return [0, 1]
  Output: [0, 1]
""")

def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(f"Input: {nums}, target: {target}")
print(f"Output: {result}")
print(f"Verification: {nums[result[0]]} + {nums[result[1]]} = {target}")

# Pattern 2: First Non-Repeating Character
print("\n" + "=" * 60)
print("Pattern 2: First Non-Repeating Character")
print("=" * 60)
print("""
Problem: Find first character in string that appears only once.

How it works:
  1. First pass: Count frequency of each character using hash table
  2. Iterate through string, incrementing count for each character
  3. Second pass: Go through original string in order
  4. Return first character with count == 1
  5. Hash table preserves counts, string order gives us "first"

Example:
  Input: "leetcode"
  Frequency: {'l':1, 'e':3, 't':1, 'c':1, 'o':1, 'd':1}
  First pass through string: 'l' has count 1
  Output: 'l'
""")

def first_non_repeating(s):
    # Count frequencies
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    
    # Find first with count 1
    for char in s:
        if freq[char] == 1:
            return char
    return None

s = "leetcode"
result = first_non_repeating(s)
print(f"Input: '{s}'")
print(f"Output: '{result}'")

# Pattern 3: Group Anagrams
print("\n" + "=" * 60)
print("Pattern 3: Group Anagrams")
print("=" * 60)
print("""
Problem: Group strings that are anagrams (same letters, different order).

How it works:
  1. Anagrams have identical character frequencies
  2. Create hash table with sorted string as key
  3. Sort each word's characters: "eat" → "aet", "tea" → "aet" (same!)
  4. Use sorted version as key to group anagrams together
  5. Words with same sorted form go in same list
  6. Return all groups as list of lists

Example:
  Input: ["eat", "tea", "tan", "ate", "nat", "bat"]
  "eat" → sorted: "aet" → group["aet"] = ["eat"]
  "tea" → sorted: "aet" → group["aet"] = ["eat", "tea"]
  "tan" → sorted: "ant" → group["ant"] = ["tan"]
  Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
""")

def group_anagrams(strs):
    groups = {}
    for word in strs:
        key = ''.join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
result = group_anagrams(words)
print(f"Input: {words}")
print(f"Output: {result}")

# Pattern 4: Subarray Sum Equals K
print("\n" + "=" * 60)
print("Pattern 4: Subarray Sum Equals K")
print("=" * 60)
print("""
Problem: Count number of subarrays with sum equal to k.

How it works:
  1. Use prefix sum technique with hash table
  2. Track cumulative sum as we go through array
  3. Key insight: if (cumulative_sum - k) exists, we found a subarray!
  4. Store frequency of each prefix sum seen
  5. For each position, check if (current_sum - k) was seen before
  6. That means there's a subarray between those positions with sum = k

Example:
  Input: nums = [1, 2, 3], k = 3
  sum=0: seen={0:1}
  sum=1: need -2? No. seen={0:1, 1:1}
  sum=3: need 0? Yes! count=1. seen={0:1, 1:1, 3:1}
  sum=6: need 3? Yes! count=2. seen={0:1, 1:1, 3:1, 6:1}
  Output: 2 (subarrays [3] and [1,2])
""")

def subarray_sum(nums, k):
    count = 0
    current_sum = 0
    sum_freq = {0: 1}  # Base case: sum of 0 seen once
    
    for num in nums:
        current_sum += num
        # If (current_sum - k) exists, we found subarray(s)
        if current_sum - k in sum_freq:
            count += sum_freq[current_sum - k]
        sum_freq[current_sum] = sum_freq.get(current_sum, 0) + 1
    
    return count

nums = [1, 2, 3]
k = 3
result = subarray_sum(nums, k)
print(f"Input: nums = {nums}, k = {k}")
print(f"Output: {result} subarrays")

# Pattern 5: Longest Consecutive Sequence
print("\n" + "=" * 60)
print("Pattern 5: Longest Consecutive Sequence")
print("=" * 60)
print("""
Problem: Find length of longest consecutive sequence in unsorted array.

How it works:
  1. Put all numbers in a set (hash table) for O(1) lookup
  2. For each number, check if it's the START of a sequence
  3. How? If (num - 1) doesn't exist, num is a sequence start
  4. Count consecutive numbers: num, num+1, num+2, etc.
  5. Keep checking num+1, num+2... until not found in set
  6. Track maximum length found
  7. Skip numbers that aren't sequence starts (optimization!)

Example:
  Input: [100, 4, 200, 1, 3, 2]
  Set: {1, 2, 3, 4, 100, 200}
  1 is start (no 0): count 1→2→3→4 = length 4
  100 is start (no 99): count 100 = length 1
  200 is start (no 199): count 200 = length 1
  Output: 4
""")

def longest_consecutive(nums):
    if not nums:
        return 0
    
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        # Only start counting if this is the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # Count consecutive numbers
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            max_length = max(max_length, current_length)
    
    return max_length

nums = [100, 4, 200, 1, 3, 2]
result = longest_consecutive(nums)
print(f"Input: {nums}")
print(f"Output: {result}")
print(f"Sequence: [1, 2, 3, 4]")

# Pattern 6: Isomorphic Strings
print("\n" + "=" * 60)
print("Pattern 6: Isomorphic Strings")
print("=" * 60)
print("""
Problem: Check if two strings are isomorphic (one-to-one character mapping).

How it works:
  1. Need TWO hash tables for bijection (one-to-one mapping)
  2. First table maps s -> t (each char in s maps to one char in t)
  3. Second table maps t -> s (each char in t maps to one char in s)
  4. For each character pair:
     - Check if mapping exists and is consistent
     - If new mapping, add to both tables
     - If existing mapping conflicts, return False
  5. Both directions must be consistent for isomorphism

Example:
  Input: s = "egg", t = "add"
  'e' → 'a', 'g' → 'd'
  Reverse: 'a' → 'e', 'd' → 'g'
  Both consistent, Output: True
  
  Counter-example: s = "foo", t = "bar"
  'f' → 'b', 'o' → 'a', but 'o' also needs → 'r'
  Conflict! Output: False
""")

def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    
    s_to_t = {}
    t_to_s = {}
    
    for char_s, char_t in zip(s, t):
        # Check s -> t mapping
        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return False
        else:
            s_to_t[char_s] = char_t
        
        # Check t -> s mapping
        if char_t in t_to_s:
            if t_to_s[char_t] != char_s:
                return False
        else:
            t_to_s[char_t] = char_s
    
    return True

s1, t1 = "egg", "add"
s2, t2 = "foo", "bar"
print(f"Input: s = '{s1}', t = '{t1}'")
print(f"Output: {is_isomorphic(s1, t1)}")
print(f"Input: s = '{s2}', t = '{t2}'")
print(f"Output: {is_isomorphic(s2, t2)}")

# Pattern 7: Valid Anagram
print("\n" + "=" * 60)
print("Pattern 7: Valid Anagram")
print("=" * 60)
print("""
Problem: Check if two strings are anagrams (same characters, different order).

How it works:
  1. Anagrams must have identical character frequencies
  2. Count frequency of each character in first string
  3. Decrement count for each character in second string
  4. If all counts reach exactly zero, they're anagrams
  5. Alternative: count both and compare dictionaries

Example:
  Input: s = "anagram", t = "nagaram"
  Frequency s: {'a':3, 'n':1, 'g':1, 'r':1, 'm':1}
  Subtract t:  {'a':0, 'n':0, 'g':0, 'r':0, 'm':0}
  All zero, Output: True
""")

def is_anagram(s, t):
    if len(s) != len(t):
        return False
    
    count = {}
    
    # Count characters in s
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    # Decrement for characters in t
    for char in t:
        if char not in count:
            return False
        count[char] -= 1
        if count[char] < 0:
            return False
    
    return all(c == 0 for c in count.values())

s, t = "anagram", "nagaram"
result = is_anagram(s, t)
print(f"Input: s = '{s}', t = '{t}'")
print(f"Output: {result}")

# Pattern 8: Design Hash Map
print("\n" + "=" * 60)
print("Pattern 8: Design Hash Map (Chaining)")
print("=" * 60)
print("""
Problem: Implement hash map with put, get, remove operations.

How it works:
  1. Use array of buckets (lists) for collision handling
  2. Hash function: key % size determines bucket index
  3. Each bucket stores list of (key, value) pairs (chaining)
  4. Put: hash key → find bucket → update or append
  5. Get: hash key → find bucket → search for key
  6. Remove: hash key → find bucket → remove key if found
  7. Collisions handled by storing multiple pairs per bucket

Example:
  put(1, 100): 1 % 1000 = 1 → buckets[1] = [(1, 100)]
  put(1001, 200): 1001 % 1000 = 1 → buckets[1] = [(1, 100), (1001, 200)]
  get(1): hash to bucket 1, find (1, 100) → return 100
  get(1001): hash to bucket 1, find (1001, 200) → return 200
""")

class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]
    
    def _hash(self, key):
        return key % self.size
    
    def put(self, key, value):
        bucket = self.buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
    
    def get(self, key):
        bucket = self.buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1
    
    def remove(self, key):
        bucket = self.buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return

hashmap = MyHashMap()
hashmap.put(1, 100)
hashmap.put(2, 200)
hashmap.put(1001, 300)  # Collides with key 1
print(f"get(1): {hashmap.get(1)}")
print(f"get(1001): {hashmap.get(1001)}")
hashmap.put(1, 150)  # Update
print(f"get(1) after update: {hashmap.get(1)}")
hashmap.remove(1)
print(f"get(1) after remove: {hashmap.get(1)}")

# Key Insights Summary
print("\n" + "=" * 60)
print("Key Insights")
print("=" * 60)
print("""
1. Two Sum: Store complements as you go, single pass
2. Frequency Counting: First pass count, second pass process
3. Anagrams: Sorted string or frequency map as key
4. Prefix Sum: Store sums seen, check (current - target)
5. Consecutive Sequence: Start from sequence beginning only
6. Isomorphic: Need bidirectional mapping (two hash tables)
7. Collision Handling: Chaining (lists) or open addressing
8. Hash Function: Distribute keys evenly across buckets

Time Complexity: O(1) average for all basic operations
Space Complexity: O(n) where n is number of elements stored
""")
