"""
NeetCode 150 - Sliding Window
==============================
Dynamic window problems for optimization.
"""


# PATTERN: Greedy / Single Pass (Can also be viewed as sliding window of size 1)
def max_profit(prices):
    """
    Best Time to Buy and Sell Stock (single transaction).
    
    Pattern: Track minimum price seen so far
    
    Algorithm Steps:
    1. Track minimum price encountered
    2. For each price, calculate profit if sold today
    3. Track maximum profit
    
    Time: O(n), Space: O(1)
    """
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit


# PATTERN: Sliding Window with Hash Map
def length_of_longest_substring(s):
    """
    Longest Substring Without Repeating Characters.
    
    Pattern: Sliding window with hash map
    
    Algorithm Steps:
    1. Use hash map to track last seen index of each character
    2. When duplicate found, move left pointer past previous occurrence
    3. Track maximum window size
    
    Example: "abcabcbb"
    - 'a': window [0,0], length=1
    - 'ab': window [0,1], length=2
    - 'abc': window [0,2], length=3
    - 'abc|a': duplicate! move left to 1, window [1,3], length=3
    
    Time: O(n), Space: O(min(n, alphabet_size))
    """
    char_index = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # If char in window, move left past its previous occurrence
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


# PATTERN: Sliding Window with Frequency Map
def character_replacement(s, k):
    """
    Longest Repeating Character Replacement.
    
    Pattern: Sliding window with character frequency tracking
    
    Algorithm Steps:
    1. Track frequency of characters in current window
    2. Window is valid if: window_length - max_frequency <= k
    3. If invalid, shrink from left
    
    Why it works: We can replace at most k characters, so we need
    window_length - most_frequent_char <= k
    
    Example: "AABABBA", k=1
    - "AAB": length=3, maxFreq=2, replacements=1 ✓
    - "AABA": length=4, maxFreq=3, replacements=1 ✓
    
    Time: O(n), Space: O(26) = O(1)
    """
    from collections import defaultdict
    
    count = defaultdict(int)
    left = 0
    max_length = 0
    max_freq = 0
    
    for right in range(len(s)):
        count[s[right]] += 1
        max_freq = max(max_freq, count[s[right]])
        
        # If window invalid, shrink from left
        window_length = right - left + 1
        if window_length - max_freq > k:
            count[s[left]] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length


# PATTERN: Sliding Window with Frequency Map
def check_inclusion(s1, s2):
    """
    Permutation in String - check if s2 contains permutation of s1.
    
    Pattern: Sliding window with character matching
    
    Algorithm Steps:
    1. Count characters in s1
    2. Slide fixed-size window (len(s1)) through s2
    3. Compare character counts
    
    Time: O(n), Space: O(26) = O(1)
    """
    from collections import Counter
    
    if len(s1) > len(s2):
        return False
    
    s1_count = Counter(s1)
    window_count = Counter(s2[:len(s1)])
    
    if s1_count == window_count:
        return True
    
    # Slide window
    for i in range(len(s1), len(s2)):
        # Add new character
        window_count[s2[i]] += 1
        # Remove old character
        left_char = s2[i - len(s1)]
        window_count[left_char] -= 1
        if window_count[left_char] == 0:
            del window_count[left_char]
        
        if s1_count == window_count:
            return True
    
    return False


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
    
    Example: s="ADOBECODEBANC", t="ABC"
    - Expand to "ADOBEC": has all chars
    - Contract to "DOBECODEBA": still has all chars
    - Contract to "CODEBA": still has all chars
    - Contract to "ODEBAN": missing 'C'
    - Final answer: "BANC"
    
    Time: O(m + n), Space: O(k) where k = unique chars
    """
    if not s or not t:
        return ""
    
    from collections import Counter
    
    need = Counter(t)
    required = len(need)
    formed = 0
    
    window_counts = {}
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if current character requirement is satisfied
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


# PATTERN: Monotonic Deque
def max_sliding_window(nums, k):
    """
    Sliding Window Maximum.
    
    Pattern: Monotonic decreasing deque
    
    Algorithm Steps:
    1. Use deque to store indices of potential maximums
    2. Maintain decreasing order in deque
    3. Remove indices outside current window
    4. Front of deque is always maximum
    
    Why it works: Only need to track decreasing elements since
    smaller elements after a larger one can't be maximum
    
    Example: nums=[1,3,-1,-3,5,3,6,7], k=3
    - Window [1,3,-1]: deque=[1(3)], max=3
    - Window [3,-1,-3]: deque=[1(3),2(-1),3(-3)], max=3
    - Window [-1,-3,5]: deque=[4(5)], max=5
    
    Time: O(n), Space: O(k)
    """
    from collections import deque
    
    if not nums:
        return []
    
    deq = deque()
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside current window
        while deq and deq[0] < i - k + 1:
            deq.popleft()
        
        # Remove smaller elements (they can't be max)
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()
        
        deq.append(i)
        
        # Add to result if window is full
        if i >= k - 1:
            result.append(nums[deq[0]])
    
    return result


if __name__ == "__main__":
    print("=== NeetCode 150 - Sliding Window ===\n")
    
    # Best Time to Buy and Sell Stock
    print(f"Max Profit [7,1,5,3,6,4]: {max_profit([7, 1, 5, 3, 6, 4])}")
    
    # Longest Substring Without Repeating
    print(f"Longest Substring 'abcabcbb': {length_of_longest_substring('abcabcbb')}")
    print(f"Longest Substring 'bbbbb': {length_of_longest_substring('bbbbb')}")
    print(f"Longest Substring 'pwwkew': {length_of_longest_substring('pwwkew')}")
    
    # Character Replacement
    print(f"Character Replacement 'ABAB' k=2: {character_replacement('ABAB', 2)}")
    print(f"Character Replacement 'AABABBA' k=1: {character_replacement('AABABBA', 1)}")
    
    # Permutation in String
    print(f"Check Inclusion 'ab' in 'eidbaooo': {check_inclusion('ab', 'eidbaooo')}")
    
    # Minimum Window Substring
    print(f"Min Window 'ADOBECODEBANC' t='ABC': '{min_window('ADOBECODEBANC', 'ABC')}'")
    
    # Sliding Window Maximum
    print(f"Max Sliding Window [1,3,-1,-3,5,3,6,7] k=3: {max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)}")
