"""
Strings - Common Patterns
==========================
Common string manipulation patterns and techniques.
"""

from collections import Counter, defaultdict


print("=" * 60)
print("Pattern 1: Two Pointers Technique")
print("=" * 60)
print()

def is_palindrome(s):
    """Check if string is palindrome using two pointers."""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print("Is Palindrome:")
test_cases = ["racecar", "hello", "madam", "python"]
for s in test_cases:
    print(f"  '{s}': {is_palindrome(s)}")
print()


def reverse_vowels(s):
    """Reverse only the vowels in a string."""
    vowels = set('aeiouAEIOU')
    chars = list(s)
    left, right = 0, len(s) - 1
    
    while left < right:
        if chars[left] not in vowels:
            left += 1
        elif chars[right] not in vowels:
            right -= 1
        else:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1
    
    return ''.join(chars)

print("Reverse Vowels:")
text = "hello"
print(f"  Original: {text}")
print(f"  Result: {reverse_vowels(text)}")
print()


print("=" * 60)
print("Pattern 2: Sliding Window")
print("=" * 60)
print()

def longest_substring_without_repeating(s):
    """Find length of longest substring without repeating characters."""
    char_index = {}
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length

print("Longest Substring Without Repeating:")
test_cases = ["abcabcbb", "bbbbb", "pwwkew"]
for s in test_cases:
    print(f"  '{s}': {longest_substring_without_repeating(s)}")
print()


def find_all_anagrams(s, p):
    """Find all start indices of p's anagrams in s."""
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = []
    
    if window_count == p_count:
        result.append(0)
    
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
s = "cbaebabacd"
p = "abc"
print(f"  String: {s}")
print(f"  Pattern: {p}")
print(f"  Anagram indices: {find_all_anagrams(s, p)}")
print()


print("=" * 60)
print("Pattern 3: Character Frequency (Hash Map)")
print("=" * 60)
print()

def first_unique_char(s):
    """Find index of first non-repeating character."""
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1

print("First Unique Character:")
test_cases = ["leetcode", "loveleetcode", "aabb"]
for s in test_cases:
    idx = first_unique_char(s)
    result = f"index {idx} ('{s[idx]}')" if idx != -1 else "None"
    print(f"  '{s}': {result}")
print()


def group_anagrams(strs):
    """Group strings that are anagrams of each other."""
    anagram_groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    return list(anagram_groups.values())

print("Group Anagrams:")
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(f"  Input: {words}")
print(f"  Grouped: {group_anagrams(words)}")
print()


print("=" * 60)
print("Pattern 4: String Building")
print("=" * 60)
print()

def compress_string(s):
    """Compress string using counts (e.g., 'aaabb' -> 'a3b2')."""
    if not s:
        return ""
    
    result = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            result.append(s[i-1] + str(count))
            count = 1
    
    # Add last group
    result.append(s[-1] + str(count))
    
    compressed = ''.join(result)
    return compressed if len(compressed) < len(s) else s

print("String Compression:")
test_cases = ["aabcccccaaa", "abc", "aaaa"]
for s in test_cases:
    print(f"  '{s}' -> '{compress_string(s)}'")
print()


def zigzag_conversion(s, num_rows):
    """Convert string to zigzag pattern."""
    if num_rows == 1 or num_rows >= len(s):
        return s
    
    rows = [''] * num_rows
    current_row = 0
    going_down = False
    
    for char in s:
        rows[current_row] += char
        if current_row == 0 or current_row == num_rows - 1:
            going_down = not going_down
        current_row += 1 if going_down else -1
    
    return ''.join(rows)

print("ZigZag Conversion:")
s = "PAYPALISHIRING"
print(f"  String: {s}")
print(f"  3 rows: {zigzag_conversion(s, 3)}")
print(f"  4 rows: {zigzag_conversion(s, 4)}")
print()


print("=" * 60)
print("Pattern 5: Subsequence/Substring Problems")
print("=" * 60)
print()

def is_subsequence(s, t):
    """Check if s is subsequence of t."""
    s_idx = 0
    for char in t:
        if s_idx < len(s) and char == s[s_idx]:
            s_idx += 1
    return s_idx == len(s)

print("Is Subsequence:")
test_cases = [("abc", "ahbgdc"), ("axc", "ahbgdc")]
for s, t in test_cases:
    print(f"  '{s}' in '{t}': {is_subsequence(s, t)}")
print()


def longest_common_prefix(strs):
    """Find longest common prefix among strings."""
    if not strs:
        return ""
    
    # Sort strings - shortest first
    strs.sort(key=len)
    
    for i, char in enumerate(strs[0]):
        for string in strs[1:]:
            if string[i] != char:
                return strs[0][:i]
    
    return strs[0]

print("Longest Common Prefix:")
test_cases = [
    ["flower", "flow", "flight"],
    ["dog", "racecar", "car"]
]
for strs in test_cases:
    print(f"  {strs}")
    print(f"  Prefix: '{longest_common_prefix(strs)}'")
print()


print("=" * 60)
print("Pattern 6: String Reversal")
print("=" * 60)
print()

def reverse_words(s):
    """Reverse words in a string."""
    return ' '.join(s.split()[::-1])

print("Reverse Words:")
sentences = ["the sky is blue", "  hello world  ", "a good   example"]
for sentence in sentences:
    print(f"  Original: '{sentence}'")
    print(f"  Reversed: '{reverse_words(sentence)}'")
print()


def reverse_string_between_parentheses(s):
    """Reverse strings between each pair of parentheses."""
    stack = []
    current = []
    
    for char in s:
        if char == '(':
            stack.append(current)
            current = []
        elif char == ')':
            current = current[::-1]
            if stack:
                current = stack.pop() + current
        else:
            current.append(char)
    
    return ''.join(current)

print("Reverse Between Parentheses:")
test_cases = ["(abcd)", "(u(love)i)", "(ed(et(oc))el)"]
for s in test_cases:
    print(f"  '{s}' -> '{reverse_string_between_parentheses(s)}'")
print()


print("=" * 60)
print("Pattern 7: String Matching/Search")
print("=" * 60)
print()

def str_str(haystack, needle):
    """Find first occurrence of needle in haystack (indexOf)."""
    if not needle:
        return 0
    
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i+len(needle)] == needle:
            return i
    
    return -1

print("String Search (indexOf):")
print(f"  'hello' in 'hello world': index {str_str('hello world', 'hello')}")
print(f"  'world' in 'hello world': index {str_str('hello world', 'world')}")
print(f"  'xyz' in 'hello world': index {str_str('hello world', 'xyz')}")
print()


def is_rotation(s1, s2):
    """Check if s2 is rotation of s1."""
    if len(s1) != len(s2):
        return False
    return s2 in (s1 + s1)

print("String Rotation:")
test_cases = [("waterbottle", "erbottlewat"), ("hello", "world")]
for s1, s2 in test_cases:
    print(f"  '{s2}' is rotation of '{s1}': {is_rotation(s1, s2)}")
print()


print("=" * 60)
print("Pattern 8: Parentheses/Bracket Validation")
print("=" * 60)
print()

def is_valid_parentheses(s):
    """Check if parentheses/brackets are valid."""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    
    return not stack

print("Valid Parentheses:")
test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
for s in test_cases:
    print(f"  '{s}': {is_valid_parentheses(s)}")
print()


print("=" * 60)
print("Common String Patterns Summary")
print("=" * 60)
print()
print("1. Two Pointers: Palindrome, reverse operations")
print("2. Sliding Window: Substrings with conditions")
print("3. Hash Map: Character frequency, anagrams")
print("4. String Building: Compression, transformations")
print("5. Subsequence: Is subsequence, LCS, prefix")
print("6. Reversal: Reverse words, sections")
print("7. Search/Match: Pattern matching, rotation")
print("8. Validation: Parentheses, brackets")
print()
print("Tips:")
print("  • Use Counter for frequency counting")
print("  • Use set for O(1) lookups")
print("  • Convert to list for in-place modifications")
print("  • Use join() for building strings")
print("  • Consider edge cases: empty strings, single char")
