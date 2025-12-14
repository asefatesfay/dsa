"""
Blind 75 - Dynamic Programming Problems
========================================
Core DP patterns for technical interviews.
"""


# 1. Climbing Stairs
# PATTERN: Dynamic Programming (Fibonacci)
def climb_stairs(n):
    """
    Number of ways to climb n stairs (1 or 2 steps at a time).
    
    Pattern: DP - Fibonacci sequence
    Approach: DP - Fibonacci pattern
    Steps:
    1. Base: ways[1]=1, ways[2]=2
    2. ways[i] = ways[i-1] + ways[i-2]
    3. Can optimize to O(1) space with two variables
    
    Time: O(n), Space: O(1)
    """
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1


# 2. Coin Change
def coin_change(coins, amount):
    """
    Minimum coins to make amount, or -1 if impossible.
    
    Problem: Given coins of different denominations and total amount, find minimum
    number of coins needed to make that amount.
    Input: coins = [1,2,5], amount = 11
    Output: 3 (11 = 5 + 5 + 1)
    
    Approach: Dynamic Programming (Unbounded Knapsack)
    
    Algorithm Steps:
    1. Create DP array: dp[i] = minimum coins needed for amount i
    2. Initialize:
       - dp[0] = 0 (0 coins needed for amount 0)
       - dp[i] = infinity for all other amounts (impossible initially)
    3. For each amount from 1 to target:
       - Try each coin denomination
       - If coin <= amount: dp[amount] = min(dp[amount], dp[amount-coin] + 1)
    4. Return dp[amount] if possible, else -1
    
    Why this works:
    - To make amount i, we can use any coin c and need dp[i-c] more coins
    - dp[i-c] + 1 means: use one coin c, plus minimum coins for remaining amount
    - Try all coins and pick the minimum
    - This is "unbounded" because we can use each coin multiple times
    
    Example walkthrough coins=[1,2,5], amount=11:
    dp[0] = 0
    dp[1] = dp[0]+1 = 1 (use coin 1)
    dp[2] = min(dp[1]+1, dp[0]+1) = 1 (use coin 2)
    dp[5] = min(dp[4]+1, dp[3]+1, dp[0]+1) = 1 (use coin 5)
    dp[11] = min(dp[10]+1, dp[9]+1, dp[6]+1) = 3 (5+5+1)
    
    Time: O(amount × len(coins)) - for each amount, try all coins
    Space: O(amount) - DP array
    """
    # Initialize DP array
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0
    
    # Fill DP table for each amount
    for i in range(1, amount + 1):
        # Try each coin
        for coin in coins:
            if i >= coin:  # Can use this coin
                # Use coin + solve for remaining amount
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # Return result (or -1 if impossible)
    return dp[amount] if dp[amount] != float('inf') else -1


# 3. Longest Increasing Subsequence
# PATTERN: Dynamic Programming (Subsequence)
def length_of_lis(nums):
    """
    Length of longest strictly increasing subsequence.
    
    Pattern: DP for subsequence problems
    Approach 1: DP O(n²)
    - dp[i] = length of LIS ending at i
    - dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]
    
    Approach 2: Binary Search O(n log n)
    - Maintain array of smallest tail elements for each length
    
    Time: O(n²) or O(n log n), Space: O(n)
    """
    if not nums:
        return 0
    
    # DP approach
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# 4. Longest Common Subsequence
# PATTERN: Dynamic Programming (2D DP)
def longest_common_subsequence(text1, text2):
    """
    Length of LCS between two strings.
    
    Pattern: 2D DP for string matching
    Approach: 2D DP
    Steps:
    1. dp[i][j] = LCS length of text1[0:i] and text2[0:j]
    2. If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    3. Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


# 5. Word Break
# PATTERN: Dynamic Programming (String Segmentation)
def word_break(s, word_dict):
    """
    Check if string can be segmented into words from dictionary.
    
    Pattern: DP for string segmentation
    Approach: DP
    Steps:
    1. dp[i] = True if s[0:i] can be segmented
    2. dp[0] = True (empty string)
    3. For each i, check all j < i:
       if dp[j] and s[j:i] in word_dict: dp[i] = True
    
    Time: O(n² * m) where m=average word length, Space: O(n)
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[len(s)]


# 6. Combination Sum IV
# PATTERN: Dynamic Programming (Unbounded Knapsack)
def combination_sum4(nums, target):
    """
    Number of combinations that sum to target (order matters).
    
    Pattern: Unbounded Knapsack with permutations
    Approach: DP - unbounded knapsack with permutations
    Steps:
    1. dp[i] = number of ways to make sum i
    2. dp[0] = 1
    3. For each sum i, try all nums:
       dp[i] += dp[i-num]
    
    Time: O(target * len(nums)), Space: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
    
    return dp[target]


# 7. House Robber
def rob(nums):
    """
    Maximum money robbing houses without alerting police (no adjacent).
    
    Problem: Rob houses to maximize money, but can't rob two adjacent houses.
    Input: nums = [2,7,9,3,1]
    Output: 12 (rob houses 0, 2, 4: 2+9+1=12)
    
    Approach: Dynamic Programming with space optimization
    
    Algorithm Steps:
    1. dp[i] = max money robbing up to house i
    2. At each house, we have two choices:
       a. Rob current house: get nums[i] + dp[i-2] (skip previous house)
       b. Skip current house: get dp[i-1] (keep previous maximum)
    3. dp[i] = max(rob current, skip current)
    4. Optimize space: only need previous two values
    
    Why this works:
    - If we rob house i, we can't rob house i-1 (adjacent)
    - So we get: current_value + best_from_(i-2)
    - If we skip house i, we keep: best_from_(i-1)
    - Choose the maximum of these two options
    
    Example walkthrough [2,7,9,3,1]:
    House 0: rob=2 (only option)
    House 1: rob=max(7, 2)=7 (rob this house or keep previous)
    House 2: rob=max(7, 2+9)=11 (skip house 1, rob 0 and 2)
    House 3: rob=max(11, 7+3)=11 (keep previous best)
    House 4: rob=max(11, 11+1)=12 (rob houses 0,2,4)
    
    State transition:
    prev2, prev1 = money_before_previous, money_at_previous
    current = max(prev1, prev2 + current_house)
    
    Time: O(n) - single pass
    Space: O(1) - only two variables
    """
    if not nums:
        return 0
    if len(nums) <= 2:
        return max(nums)
    
    # prev2 = best up to house i-2
    # prev1 = best up to house i-1
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        # Current choice: rob this house + prev2, or skip (keep prev1)
        curr = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, curr  # Shift window
    
    return prev1


# 8. House Robber II
# PATTERN: Dynamic Programming (Circular Array)
def rob2(nums):
    """
    Houses arranged in circle (first and last are adjacent).
    
    Pattern: DP with circular constraint
    Approach: Run rob() twice
    Steps:
    1. Case 1: Rob houses 0 to n-2 (exclude last)
    2. Case 2: Rob houses 1 to n-1 (exclude first)
    3. Return max of both cases
    
    Time: O(n), Space: O(1)
    """
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[:-1]), rob(nums[1:]))


# 9. Decode Ways
# PATTERN: Dynamic Programming (Fibonacci-like)
def num_decodings(s):
    """
    Number of ways to decode string where 'A'=1, 'B'=2, ..., 'Z'=26.
    
    Pattern: DP with multiple transition choices
    Approach: DP
    Steps:
    1. dp[i] = ways to decode s[0:i]
    2. Single digit: if s[i-1] != '0', add dp[i-1]
    3. Two digits: if 10 <= int(s[i-2:i]) <= 26, add dp[i-2]
    
    Time: O(n), Space: O(1)
    """
    if not s or s[0] == '0':
        return 0
    
    n = len(s)
    prev2, prev1 = 1, 1
    
    for i in range(1, n):
        curr = 0
        # Single digit
        if s[i] != '0':
            curr += prev1
        # Two digits
        two_digit = int(s[i-1:i+1])
        if 10 <= two_digit <= 26:
            curr += prev2
        
        prev2, prev1 = prev1, curr
    
    return prev1


# 10. Unique Paths
# PATTERN: Dynamic Programming (Grid DP)
def unique_paths(m, n):
    """
    Number of paths from top-left to bottom-right in m×n grid (only right/down).
    
    Pattern: Grid DP / Combinatorics
    Approach: DP or combinatorics
    DP Steps:
    1. dp[i][j] = paths to cell (i,j)
    2. dp[i][j] = dp[i-1][j] + dp[i][j-1]
    3. Can optimize to O(n) space
    
    Time: O(m*n), Space: O(n)
    """
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[n - 1]


# 11. Jump Game
# PATTERN: Greedy
def can_jump(nums):
    """
    Check if can reach last index from first (each element is max jump length).
    
    Pattern: Greedy - track maximum reachable position
    Approach: Greedy - track farthest reachable
    Steps:
    1. Track max_reach = 0
    2. For each i <= max_reach:
       max_reach = max(max_reach, i + nums[i])
    3. Return True if max_reach >= last index
    
    Time: O(n), Space: O(1)
    """
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
        if max_reach >= len(nums) - 1:
            return True
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("BLIND 75 - DYNAMIC PROGRAMMING PROBLEMS")
    print("=" * 60)
    print()
    
    print("1. CLIMBING STAIRS")
    print("-" * 60)
    n = 5
    print(f"Input: n = {n}")
    print(f"Output: {climb_stairs(n)}")
    print(f"Explanation: {n} ways to climb {n} stairs (1 or 2 steps at a time)")
    print()
    
    print("2. COIN CHANGE")
    print("-" * 60)
    coins, amount = [1, 2, 5], 11
    print(f"Input: coins = {coins}, amount = {amount}")
    print(f"Output: {coin_change(coins, amount)}")
    print(f"Explanation: {amount} = 5 + 5 + 1 (minimum 3 coins)")
    print()
    
    print("3. LONGEST INCREASING SUBSEQUENCE")
    print("-" * 60)
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Input: nums = {nums}")
    print(f"Output: {length_of_lis(nums)}")
    print("Explanation: LIS is [2,3,7,101] with length 4")
    print()
    
    print("4. LONGEST COMMON SUBSEQUENCE")
    print("-" * 60)
    text1, text2 = "abcde", "ace"
    print(f"Input: text1 = '{text1}', text2 = '{text2}'")
    print(f"Output: {longest_common_subsequence(text1, text2)}")
    print("Explanation: LCS is 'ace' with length 3")
    print()
    
    print("5. WORD BREAK")
    print("-" * 60)
    s, wordDict = "leetcode", ["leet", "code"]
    print(f"Input: s = '{s}', wordDict = {wordDict}")
    print(f"Output: {word_break(s, wordDict)}")
    print("Explanation: 'leetcode' can be segmented as 'leet code'")
    print()
    
    print("6. COMBINATION SUM IV")
    print("-" * 60)
    nums, target = [1, 2, 3], 4
    print(f"Input: nums = {nums}, target = {target}")
    print(f"Output: {combination_sum4(nums, target)}")
    print("Explanation: Possible combinations: (1,1,1,1), (1,1,2), (1,2,1), (1,3), (2,1,1), (2,2), (3,1)")
    print()
    
    print("7. HOUSE ROBBER")
    print("-" * 60)
    houses = [2, 7, 9, 3, 1]
    print(f"Input: nums = {houses}")
    print(f"Output: {rob(houses)}")
    print("Explanation: Rob houses 0, 2, 4: 2 + 9 + 1 = 12")
    print()
    
    print("8. HOUSE ROBBER II (Circular)")
    print("-" * 60)
    houses = [2, 3, 2]
    print(f"Input: nums = {houses}")
    print(f"Output: {rob2(houses)}")
    print("Explanation: Cannot rob houses 0 and 2 (adjacent in circle)")
    print()
    
    print("9. DECODE WAYS")
    print("-" * 60)
    s = "226"
    print(f"Input: s = '{s}'")
    print(f"Output: {num_decodings(s)}")
    print("Explanation: '226' can be decoded as 'BZ'(2 26), 'VF'(22 6), 'BBF'(2 2 6)")
    print()
    
    print("10. UNIQUE PATHS")
    print("-" * 60)
    m, n = 3, 7
    print(f"Input: m = {m}, n = {n}")
    print(f"Output: {unique_paths(m, n)}")
    print(f"Explanation: {unique_paths(m, n)} unique paths in {m}×{n} grid")
    print()
    
    print("11. JUMP GAME")
    print("-" * 60)
    nums = [2, 3, 1, 1, 4]
    print(f"Input: nums = {nums}")
    print(f"Output: {can_jump(nums)}")
    print("Explanation: Jump 1 step to index 1, then 3 steps to last index")
    print()
    print("=" * 60)
