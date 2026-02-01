"""
Strings - LeetCode Problems
===========================
Common string interview problems from LeetCode.
"""

from collections import Counter, defaultdict
from typing import List


print("=" * 60)
print("Problem 1: Valid Anagram (LeetCode 242)")
print("=" * 60)
print()

def is_anagram(s: str, t: str) -> bool:
    """
    Check if two strings are anagrams.
    
    Time: O(n), Space: O(1) - fixed alphabet size
    """
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)

print("Valid Anagram:")
test_cases = [
    ("anagram", "nagaram", True),
    ("rat", "car", False),
    ("listen", "silent", True)
]
for s, t, expected in test_cases:
    result = is_anagram(s, t)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' and '{t}': {result}")
print()


print("=" * 60)
print("Problem 2: Group Anagrams (LeetCode 49)")
print("=" * 60)
print()

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams of each other.
    
    Time: O(n * k log k) where k is max string length
    Space: O(n * k)
    """
    anagram_map = defaultdict(list)
    for s in strs:
        # Use sorted string as key
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    return list(anagram_map.values())

print("Group Anagrams:")
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
result = group_anagrams(strs)
print(f"  Input: {strs}")
print(f"  Output: {result}")
print()


print("=" * 60)
print("Problem 3: Longest Palindromic Substring (LeetCode 5)")
print("=" * 60)
print()

def longest_palindrome(s: str) -> str:
    """
    Find longest palindromic substring.
    
    Time: O(n²), Space: O(1)
    """
    if not s:
        return ""
    
    def expand_around_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    result = ""
    for i in range(len(s)):
        # Odd length palindrome
        palindrome1 = expand_around_center(i, i)
        # Even length palindrome
        palindrome2 = expand_around_center(i, i + 1)
        
        # Keep the longest
        result = max([result, palindrome1, palindrome2], key=len)
    
    return result

print("Longest Palindromic Substring:")
test_cases = ["babad", "cbbd", "racecar", "a", "ac"]
for s in test_cases:
    result = longest_palindrome(s)
    print(f"  '{s}' -> '{result}'")
print()


print("=" * 60)
print("Problem 4: Palindromic Substrings (LeetCode 647)")
print("=" * 60)
print()

def count_substrings(s: str) -> int:
    """
    Count all palindromic substrings.
    
    Time: O(n²), Space: O(1)
    """
    count = 0
    
    for i in range(len(s)):
        # Odd length palindromes
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
        
        # Even length palindromes
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
    
    return count

print("Count Palindromic Substrings:")
test_cases = ["abc", "aaa", "racecar"]
for s in test_cases:
    result = count_substrings(s)
    print(f"  '{s}': {result} palindromes")
print()


print("=" * 60)
print("Problem 5: Encode and Decode Strings (LeetCode 271)")
print("=" * 60)
print()

class Codec:
    """
    Encode/decode list of strings to/from a single string.
    Handles special characters and empty strings.
    """
    
    def encode(self, strs: List[str]) -> str:
        """Encode list to string: length#string"""
        result = []
        for s in strs:
            result.append(f"{len(s)}#{s}")
        return ''.join(result)
    
    def decode(self, s: str) -> List[str]:
        """Decode string back to list"""
        result = []
        i = 0
        
        while i < len(s):
            # Find the delimiter
            j = s.find('#', i)
            length = int(s[i:j])
            # Extract string of that length
            result.append(s[j + 1:j + 1 + length])
            i = j + 1 + length
        
        return result

codec = Codec()
test_cases = [
    ["hello", "world"],
    ["", ""],
    ["a#b", "c#d"],
    ["we", "say", ":", "yes"]
]
print("Encode/Decode:")
for strs in test_cases:
    encoded = codec.encode(strs)
    decoded = codec.decode(encoded)
    status = "✓" if decoded == strs else "✗"
    print(f"  {status} {strs}")
    print(f"     Encoded: '{encoded}'")
    print(f"     Decoded: {decoded}")
print()


print("=" * 60)
print("Problem 6: Longest Repeating Character Replacement (LeetCode 424)")
print("=" * 60)
print()

def character_replacement(s: str, k: int) -> int:
    """
    Longest substring with same letter after k replacements.
    
    Time: O(n), Space: O(1) - fixed alphabet
    """
    char_count = {}
    max_length = 0
    max_freq = 0
    left = 0
    
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        max_freq = max(max_freq, char_count[s[right]])
        
        # If we need more than k replacements, shrink window
        if (right - left + 1) - max_freq > k:
            char_count[s[left]] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

print("Longest Repeating Character Replacement:")
test_cases = [
    ("ABAB", 2, 4),
    ("AABABBA", 1, 4),
    ("AAAA", 0, 4)
]
for s, k, expected in test_cases:
    result = character_replacement(s, k)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' with k={k}: {result}")
print()


print("=" * 60)
print("Problem 7: Minimum Window Substring (LeetCode 76)")
print("=" * 60)
print()

def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s containing all characters from t.
    
    Time: O(|s| + |t|), Space: O(|t|)
    """
    if not s or not t:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    
    window_counts = {}
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        # Try to contract window
        while left <= right and formed == required:
            # Update result
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Remove from left
            char = s[left]
            window_counts[char] -= 1
            if char in t_count and window_counts[char] < t_count[char]:
                formed -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]

print("Minimum Window Substring:")
test_cases = [
    ("ADOBECODEBANC", "ABC", "BANC"),
    ("a", "a", "a"),
    ("a", "aa", "")
]
for s, t, expected in test_cases:
    result = min_window(s, t)
    status = "✓" if result == expected else "✗"
    print(f"  {status} s='{s}', t='{t}' -> '{result}'")
print()


print("=" * 60)
print("Problem 8: Valid Palindrome II (LeetCode 680)")
print("=" * 60)
print()

def valid_palindrome(s: str) -> bool:
    """
    Check if string can be palindrome after deleting at most one character.
    
    Time: O(n), Space: O(1)
    """
    def is_palindrome_range(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
    
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            # Try deleting either left or right character
            return (is_palindrome_range(left + 1, right) or 
                    is_palindrome_range(left, right - 1))
        left += 1
        right -= 1
    
    return True

print("Valid Palindrome II (delete at most 1 char):")
test_cases = [
    ("aba", True),
    ("abca", True),  # Remove 'b' or 'c'
    ("abc", False),
    ("racecar", True)
]
for s, expected in test_cases:
    result = valid_palindrome(s)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}': {result}")
print()


print("=" * 60)
print("Problem 9: Longest Common Prefix (LeetCode 14)")
print("=" * 60)
print()

def longest_common_prefix(strs: List[str]) -> str:
    """
    Find longest common prefix among strings.
    
    Time: O(S) where S = sum of all characters
    Space: O(1)
    """
    if not strs:
        return ""
    
    # Use first string as reference
    for i in range(len(strs[0])):
        char = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != char:
                return strs[0][:i]
    
    return strs[0]

print("Longest Common Prefix:")
test_cases = [
    (["flower", "flow", "flight"], "fl"),
    (["dog", "racecar", "car"], ""),
    (["interspecies", "interstellar", "interstate"], "inters")
]
for strs, expected in test_cases:
    result = longest_common_prefix(strs)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {strs}")
    print(f"     Result: '{result}'")
print()


print("=" * 60)
print("Problem 10: String to Integer (atoi) (LeetCode 8)")
print("=" * 60)
print()

def my_atoi(s: str) -> int:
    """
    Convert string to integer with specific rules.
    
    Time: O(n), Space: O(1)
    """
    s = s.lstrip()  # Remove leading whitespace
    if not s:
        return 0
    
    sign = 1
    index = 0
    
    # Check for sign
    if s[0] in ['+', '-']:
        if s[0] == '-':
            sign = -1
        index += 1
    
    # Read digits
    result = 0
    while index < len(s) and s[index].isdigit():
        result = result * 10 + int(s[index])
        index += 1
    
    result *= sign
    
    # Clamp to 32-bit integer range
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    
    if result > INT_MAX:
        return INT_MAX
    if result < INT_MIN:
        return INT_MIN
    
    return result

print("String to Integer (atoi):")
test_cases = [
    ("42", 42),
    ("   -42", -42),
    ("4193 with words", 4193),
    ("words and 987", 0),
    ("-91283472332", -2147483648)  # INT_MIN
]
for s, expected in test_cases:
    result = my_atoi(s)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' -> {result}")
print()


print("=" * 60)
print("Problem 11: Find All Anagrams (LeetCode 438)")
print("=" * 60)
print()

def find_anagrams(s: str, p: str) -> List[int]:
    """
    Find all start indices of p's anagrams in s.
    
    Time: O(n), Space: O(1) - fixed alphabet
    """
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = []
    
    if window_count == p_count:
        result.append(0)
    
    # Slide the window
    for i in range(len(p), len(s)):
        # Add new character
        window_count[s[i]] += 1
        # Remove old character
        old_char = s[i - len(p)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        if window_count == p_count:
            result.append(i - len(p) + 1)
    
    return result

print("Find All Anagrams:")
test_cases = [
    ("cbaebabacd", "abc", [0, 6]),
    ("abab", "ab", [0, 1, 2])
]
for s, p, expected in test_cases:
    result = find_anagrams(s, p)
    status = "✓" if result == expected else "✗"
    print(f"  {status} s='{s}', p='{p}'")
    print(f"     Result: {result}")
print()


print("=" * 60)
print("Problem 12: Longest Substring with At Most K Distinct (LeetCode 340)")
print("=" * 60)
print()

def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Longest substring with at most k distinct characters.
    
    Time: O(n), Space: O(k)
    """
    if k == 0:
        return 0
    
    char_count = {}
    max_length = 0
    left = 0
    
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if too many distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

print("Longest Substring with At Most K Distinct:")
test_cases = [
    ("eceba", 2, 3),  # "ece"
    ("aa", 1, 2),     # "aa"
    ("abc", 2, 2)     # "ab" or "bc"
]
for s, k, expected in test_cases:
    result = length_of_longest_substring_k_distinct(s, k)
    status = "✓" if result == expected else "✗"
    print(f"  {status} s='{s}', k={k} -> {result}")
print()


print("=" * 60)
print("Problem 13: Reverse Words in a String (LeetCode 151)")
print("=" * 60)
print()

def reverse_words(s: str) -> str:
    """
    Reverse the order of words in a string.
    
    Time: O(n), Space: O(n)
    """
    return ' '.join(reversed(s.split()))

print("Reverse Words:")
test_cases = [
    ("the sky is blue", "blue is sky the"),
    ("  hello world  ", "world hello"),
    ("a good   example", "example good a")
]
for s, expected in test_cases:
    result = reverse_words(s)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}'")
    print(f"     -> '{result}'")
print()


print("=" * 60)
print("Problem 14: Implement strStr() (LeetCode 28)")
print("=" * 60)
print()

def str_str(haystack: str, needle: str) -> int:
    """
    Find first occurrence of needle in haystack.
    
    Time: O(n*m), Space: O(1)
    """
    if not needle:
        return 0
    
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return i
    
    return -1

print("Implement strStr():")
test_cases = [
    ("hello", "ll", 2),
    ("aaaaa", "bba", -1),
    ("", "", 0),
    ("abc", "c", 2)
]
for haystack, needle, expected in test_cases:
    result = str_str(haystack, needle)
    status = "✓" if result == expected else "✗"
    print(f"  {status} haystack='{haystack}', needle='{needle}' -> {result}")
print()


print("=" * 60)
print("Problem 15: Zigzag Conversion (LeetCode 6)")
print("=" * 60)
print()

def convert_zigzag(s: str, num_rows: int) -> str:
    """
    Convert string to zigzag pattern and read line by line.
    
    Time: O(n), Space: O(n)
    """
    if num_rows == 1 or num_rows >= len(s):
        return s
    
    rows = [''] * num_rows
    current_row = 0
    going_down = False
    
    for char in s:
        rows[current_row] += char
        
        # Change direction at top or bottom
        if current_row == 0 or current_row == num_rows - 1:
            going_down = not going_down
        
        current_row += 1 if going_down else -1
    
    return ''.join(rows)

print("Zigzag Conversion:")
test_cases = [
    ("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"),
    ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"),
    ("A", 1, "A")
]
for s, num_rows, expected in test_cases:
    result = convert_zigzag(s, num_rows)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' rows={num_rows}")
    print(f"     -> '{result}'")
print()


print("=" * 60)
print("String Problems Summary")
print("=" * 60)
print()
print("Key Patterns:")
print("  1. Hash Map: Anagrams, character frequency")
print("  2. Two Pointers: Palindromes, partitioning")
print("  3. Sliding Window: Substrings with constraints")
print("  4. Expand Around Center: Palindrome detection")
print("  5. String Building: Encoding, transformations")
print()
print("Time Complexity Tips:")
print("  • Character frequency: O(n) with hash map")
print("  • Palindrome check: O(n) with two pointers")
print("  • Longest palindrome: O(n²) expand around center")
print("  • Sliding window: O(n) for most substring problems")
print()
print("Space Optimization:")
print("  • Use Counter for frequency analysis")
print("  • Sliding window often uses O(1) or O(k) space")
print("  • String building: use list + join() instead of +=")
