"""
LeetCode 150 - Sliding Window
==============================
Problems using sliding window technique.
"""


# PATTERN: Sliding Window
def min_sub_array_len(target, nums):
    """
    Minimum Size Subarray Sum - smallest subarray with sum >= target.
    
    Pattern: Sliding window with variable size
    
    Algorithm Steps:
    1. Expand window by moving right pointer
    2. When sum >= target, try to shrink from left
    3. Track minimum length found
    
    Time: O(n), Space: O(1)
    """
    n = len(nums)
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += nums[right]
        
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0


# PATTERN: Sliding Window with Hash Map
def length_of_longest_substring(s):
    """
    Longest Substring Without Repeating Characters.
    
    Pattern: Sliding window with hash map
    
    Algorithm Steps:
    1. Use hash map to track last seen index of each character
    2. When duplicate found, move left pointer past previous occurrence
    3. Track maximum length
    
    Time: O(n), Space: O(min(n, alphabet_size))
    """
    char_index = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # If char seen and within current window
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


# PATTERN: Sliding Window with Hash Map
def find_substring(s, words):
    """
    Substring with Concatenation of All Words.
    
    Pattern: Sliding window with word counting
    
    Algorithm Steps:
    1. Calculate total length needed (word_len * word_count)
    2. Slide window of that size through string
    3. Check if window contains exact concatenation of all words
    
    Time: O(n * m) where m = word length, Space: O(k) where k = word count
    """
    if not s or not words:
        return []
    
    word_len = len(words[0])
    word_count = len(words)
    total_len = word_len * word_count
    word_freq = {}
    
    # Count word frequencies
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    result = []
    
    # Try starting from each position within first word_len positions
    for i in range(word_len):
        left = i
        seen = {}
        count = 0
        
        for right in range(i, len(s) - word_len + 1, word_len):
            word = s[right:right + word_len]
            
            if word in word_freq:
                seen[word] = seen.get(word, 0) + 1
                count += 1
                
                # If word appears too many times, shrink window
                while seen[word] > word_freq[word]:
                    left_word = s[left:left + word_len]
                    seen[left_word] -= 1
                    count -= 1
                    left += word_len
                
                # Check if we found a valid concatenation
                if count == word_count:
                    result.append(left)
                    # Shrink for next iteration
                    left_word = s[left:left + word_len]
                    seen[left_word] -= 1
                    count -= 1
                    left += word_len
            else:
                # Reset window
                seen.clear()
                count = 0
                left = right + word_len
    
    return result


# PATTERN: Sliding Window with Hash Map
def min_window(s, t):
    """
    Minimum Window Substring - smallest substring containing all chars of t.
    
    Pattern: Sliding window with character counting
    
    Algorithm Steps:
    1. Count characters needed from t
    2. Expand window until all characters found
    3. Contract window while maintaining all characters
    4. Track minimum window
    
    Time: O(m + n), Space: O(k) where k = unique chars
    """
    if not s or not t:
        return ""
    
    # Count characters in t
    need = {}
    for char in t:
        need[char] = need.get(char, 0) + 1
    
    required = len(need)  # Unique characters needed
    formed = 0  # Unique characters satisfied in current window
    
    window_counts = {}
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if current character satisfied
        if char in need and window_counts[char] == need[char]:
            formed += 1
        
        # Try to contract window
        while formed == required and left <= right:
            # Update result
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Remove leftmost character
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in need and window_counts[left_char] < need[left_char]:
                formed -= 1
            
            left += 1
    
    return s[min_left:min_left + min_len] if min_len != float('inf') else ""


if __name__ == "__main__":
    print("=== LeetCode 150 - Sliding Window ===\n")
    
    # Minimum Size Subarray Sum
    print(f"Min Subarray Len (target=7, [2,3,1,2,4,3]): {min_sub_array_len(7, [2, 3, 1, 2, 4, 3])}")
    
    # Longest Substring Without Repeating Characters
    print(f"Longest Substring Without Repeating 'abcabcbb': {length_of_longest_substring('abcabcbb')}")
    print(f"Longest Substring Without Repeating 'bbbbb': {length_of_longest_substring('bbbbb')}")
    print(f"Longest Substring Without Repeating 'pwwkew': {length_of_longest_substring('pwwkew')}")
    
    # Substring with Concatenation of All Words
    print(f"Find Substring 'barfoothefoobarman' words=['foo','bar']: {find_substring('barfoothefoobarman', ['foo', 'bar'])}")
    
    # Minimum Window Substring
    print(f"Min Window 'ADOBECODEBANC' t='ABC': '{min_window('ADOBECODEBANC', 'ABC')}'")
    print(f"Min Window 'a' t='a': '{min_window('a', 'a')}'")
    print(f"Min Window 'a' t='aa': '{min_window('a', 'aa')}'")
