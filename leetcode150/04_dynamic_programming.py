"""
LeetCode 150 - Dynamic Programming (1D)
========================================
Essential 1D DP problems.
"""


# PATTERN: Dynamic Programming (Fibonacci)
def climb_stairs(n):
    """
    Climbing Stairs - ways to climb n stairs (1 or 2 steps).
    
    Pattern: Fibonacci-like DP
    
    Time: O(n), Space: O(1)
    """
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1


# PATTERN: Dynamic Programming
def rob(nums):
    """
    House Robber - max money without robbing adjacent houses.
    
    Pattern: DP with state transition
    
    Algorithm Steps:
    1. dp[i] = max money robbing up to house i
    2. dp[i] = max(rob i + dp[i-2], skip i = dp[i-1])
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2, prev1 = 0, 0
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2, prev1 = prev1, current
    
    return prev1


# PATTERN: Dynamic Programming (Circular Array)
def rob_ii(nums):
    """
    House Robber II - houses arranged in circle.
    
    Pattern: DP with circular constraint
    
    Algorithm Steps:
    1. Either rob first house (exclude last)
    2. Or don't rob first house (include last)
    3. Return max of both scenarios
    
    Time: O(n), Space: O(1)
    """
    if len(nums) == 1:
        return nums[0]
    
    def rob_linear(houses):
        prev2, prev1 = 0, 0
        for num in houses:
            current = max(prev1, prev2 + num)
            prev2, prev1 = prev1, current
        return prev1
    
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


# PATTERN: Dynamic Programming (String Segmentation)
def word_break(s, word_dict):
    """
    Word Break - check if string can be segmented into dictionary words.
    
    Pattern: DP for string segmentation
    
    Algorithm Steps:
    1. dp[i] = True if s[:i] can be segmented
    2. For each position i, check all possible last words
    3. dp[i] = True if dp[j] and s[j:i] in wordDict
    
    Time: O(n² * m) where m = avg word length, Space: O(n)
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[n]


# PATTERN: Dynamic Programming (Unbounded Knapsack)
def coin_change(coins, amount):
    """
    Coin Change - minimum coins to make amount.
    
    Pattern: Unbounded knapsack DP
    
    Algorithm Steps:
    1. dp[i] = min coins to make amount i
    2. dp[0] = 0 (0 coins for 0 amount)
    3. For each amount, try each coin
    4. dp[i] = min(dp[i], dp[i - coin] + 1)
    
    Time: O(amount * coins), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# PATTERN: Dynamic Programming (Subsequence)
def length_of_lis(nums):
    """
    Longest Increasing Subsequence.
    
    Pattern: DP for subsequence
    
    Time: O(n²), Space: O(n)
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


# PATTERN: Dynamic Programming (Grid Path)
def min_path_sum(grid):
    """
    Minimum Path Sum - top-left to bottom-right with min sum.
    
    Pattern: Grid DP
    
    Time: O(m*n), Space: O(1) in-place
    """
    m, n = len(grid), len(grid[0])
    
    # First row
    for j in range(1, n):
        grid[0][j] += grid[0][j - 1]
    
    # First column
    for i in range(1, m):
        grid[i][0] += grid[i - 1][0]
    
    # Rest of grid
    for i in range(1, m):
        for j in range(1, n):
            grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
    
    return grid[m - 1][n - 1]


# PATTERN: Dynamic Programming (Grid Path)
def unique_paths(m, n):
    """
    Unique Paths - grid paths from top-left to bottom-right.
    
    Pattern: Grid DP or combinatorics
    
    Time: O(m*n), Space: O(n)
    """
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    
    return dp[n - 1]


# PATTERN: Dynamic Programming (Grid Path with Obstacles)
def unique_paths_with_obstacles(obstacle_grid):
    """
    Unique Paths II - with obstacles.
    
    Pattern: Grid DP with obstacle checking
    
    Time: O(m*n), Space: O(n)
    """
    if not obstacle_grid or obstacle_grid[0][0] == 1:
        return 0
    
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [0] * n
    dp[0] = 1
    
    for i in range(m):
        for j in range(n):
            if obstacle_grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    
    return dp[n - 1]


# PATTERN: Dynamic Programming (String DP)
def longest_palindrome_substring(s):
    """
    Longest Palindromic Substring.
    
    Pattern: Expand around center
    
    Time: O(n²), Space: O(1)
    """
    if not s:
        return ""
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    start = end = 0
    
    for i in range(len(s)):
        # Odd length palindrome
        len1 = expand_around_center(i, i)
        # Even length palindrome
        len2 = expand_around_center(i, i + 1)
        max_len = max(len1, len2)
        
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    
    return s[start:end + 1]


# PATTERN: Dynamic Programming (2D String DP)
def is_interleave(s1, s2, s3):
    """
    Interleaving String - check if s3 is interleaving of s1 and s2.
    
    Pattern: 2D DP
    
    Time: O(m*n), Space: O(m*n)
    """
    m, n, l = len(s1), len(s2), len(s3)
    
    if m + n != l:
        return False
    
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # First row
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    
    # First column
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    
    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or \
                       (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
    
    return dp[m][n]


# PATTERN: Dynamic Programming (2D String DP)
def min_distance(word1, word2):
    """
    Edit Distance - minimum operations to convert word1 to word2.
    
    Pattern: 2D DP (Levenshtein distance)
    
    Operations: insert, delete, replace
    
    Algorithm Steps:
    1. dp[i][j] = min operations to convert word1[:i] to word2[:j]
    2. If chars match: dp[i][j] = dp[i-1][j-1]
    3. Else: min of insert, delete, replace
    
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]


if __name__ == "__main__":
    print("=== LeetCode 150 - Dynamic Programming (1D) ===\n")
    
    print(f"Climb Stairs (n=5): {climb_stairs(5)}")
    print(f"House Robber [1,2,3,1]: {rob([1, 2, 3, 1])}")
    print(f"House Robber II [2,3,2]: {rob_ii([2, 3, 2])}")
    print(f"Word Break 'leetcode' ['leet','code']: {word_break('leetcode', ['leet', 'code'])}")
    print(f"Coin Change [1,2,5] amount=11: {coin_change([1, 2, 5], 11)}")
    print(f"Longest Increasing Subsequence [10,9,2,5,3,7,101,18]: {length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])}")
    print(f"Min Path Sum [[1,3,1],[1,5,1],[4,2,1]]: {min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])}")
    print(f"Unique Paths (3x7): {unique_paths(3, 7)}")
    print(f"Longest Palindrome 'babad': '{longest_palindrome_substring('babad')}'")
    print(f"Edit Distance 'horse' -> 'ros': {min_distance('horse', 'ros')}")
