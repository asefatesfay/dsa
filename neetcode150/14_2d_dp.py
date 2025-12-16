"""
NeetCode 150 - 2-D Dynamic Programming
=======================================
Grid and matrix DP (11 problems).
"""


# PATTERN: Grid DP
def unique_paths(m, n):
    """
    Unique Paths - paths from top-left to bottom-right.
    
    Pattern: 2D DP (can optimize to 1D)
    
    Time: O(m * n), Space: O(n)
    """
    row = [1] * n
    
    for _ in range(m - 1):
        new_row = [1] * n
        for j in range(n - 2, -1, -1):
            new_row[j] = new_row[j + 1] + row[j]
        row = new_row
    
    return row[0]


# PATTERN: Grid DP with Obstacles
def longest_common_subsequence(text1, text2):
    """
    Longest Common Subsequence.
    
    Pattern: 2D DP table
    
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


# PATTERN: Stock DP
def max_profit(prices):
    """
    Best Time to Buy and Sell Stock with Cooldown.
    
    Pattern: State machine DP (buying, selling, cooldown)
    
    Time: O(n), Space: O(1)
    """
    sold, held, reset = float('-inf'), float('-inf'), 0
    
    for price in prices:
        prev_sold = sold
        sold = held + price
        held = max(held, reset - price)
        reset = max(reset, prev_sold)
    
    return max(sold, reset)


# PATTERN: Unbounded Knapsack
def change(amount, coins):
    """
    Coin Change II - number of combinations to make amount.
    
    Pattern: Unbounded knapsack
    
    Time: O(amount * len(coins)), Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    
    return dp[amount]


# PATTERN: 0/1 Knapsack
def find_target_sum_ways(nums, target):
    """
    Target Sum - count ways to assign +/- to reach target.
    
    Pattern: DP with offset (handle negatives)
    
    Time: O(n * sum), Space: O(sum)
    """
    total = sum(nums)
    if abs(target) > total or (target + total) % 2 != 0:
        return 0
    
    # Transform to subset sum problem
    subset_sum = (target + total) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1
    
    for num in nums:
        for s in range(subset_sum, num - 1, -1):
            dp[s] += dp[s - num]
    
    return dp[subset_sum]


# PATTERN: String Matching DP
def is_interleave(s1, s2, s3):
    """
    Interleaving String.
    
    Pattern: 2D DP matching
    
    Time: O(m * n), Space: O(n)
    """
    if len(s1) + len(s2) != len(s3):
        return False
    
    dp = [False] * (len(s2) + 1)
    dp[0] = True
    
    for j in range(1, len(s2) + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
    
    for i in range(1, len(s1) + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        
        for j in range(1, len(s2) + 1):
            dp[j] = ((dp[j] and s1[i - 1] == s3[i + j - 1]) or
                     (dp[j - 1] and s2[j - 1] == s3[i + j - 1]))
    
    return dp[len(s2)]


# PATTERN: DP with Optimization
def longest_increasing_path(matrix):
    """
    Longest Increasing Path in a Matrix.
    
    Pattern: DFS + memoization
    
    Time: O(m * n), Space: O(m * n)
    """
    if not matrix:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    memo = {}
    
    def dfs(r, c):
        if (r, c) in memo:
            return memo[(r, c)]
        
        max_path = 1
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                max_path = max(max_path, 1 + dfs(nr, nc))
        
        memo[(r, c)] = max_path
        return max_path
    
    result = 0
    for r in range(rows):
        for c in range(cols):
            result = max(result, dfs(r, c))
    
    return result


# PATTERN: Distinct Subsequences DP
def num_distinct(s, t):
    """
    Distinct Subsequences - count distinct subsequences.
    
    Pattern: 2D DP counting
    
    Time: O(m * n), Space: O(n)
    """
    n = len(t)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for char_s in s:
        for j in range(n, 0, -1):
            if char_s == t[j - 1]:
                dp[j] += dp[j - 1]
    
    return dp[n]


# PATTERN: String Edit DP
def min_distance(word1, word2):
    """
    Edit Distance - minimum operations to convert word1 to word2.
    
    Pattern: 2D DP (insert, delete, replace)
    
    Time: O(m * n), Space: O(n)
    """
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))
    
    for i in range(1, m + 1):
        curr = [i]
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr.append(prev[j - 1])
            else:
                curr.append(1 + min(prev[j], curr[j - 1], prev[j - 1]))
        prev = curr
    
    return prev[n]


# PATTERN: Burst Balloons DP
def max_coins(nums):
    """
    Burst Balloons - maximize coins from bursting balloons.
    
    Pattern: Interval DP (burst last)
    
    Time: O(n^3), Space: O(n^2)
    """
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n):
        for left in range(n - length):
            right = left + length
            for i in range(left + 1, right):
                coins = nums[left] * nums[i] * nums[right]
                dp[left][right] = max(dp[left][right], 
                                      dp[left][i] + coins + dp[i][right])
    
    return dp[0][n - 1]


# PATTERN: Regex DP
def is_match(s, p):
    """
    Regular Expression Matching - '.' and '*'.
    
    Pattern: 2D DP with pattern matching
    
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, etc. that match empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Don't use * (0 occurrences)
                dp[i][j] = dp[i][j - 2]
                
                # Use * (1+ occurrences)
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]


if __name__ == "__main__":
    print("=== NeetCode 150 - 2-D Dynamic Programming ===\n")
    
    print(f"Unique Paths (3x7): {unique_paths(3, 7)}")
    print(f"LCS 'abcde', 'ace': {longest_common_subsequence('abcde', 'ace')}")
    print(f"Max Profit with Cooldown [1,2,3,0,2]: {max_profit([1, 2, 3, 0, 2])}")
    print(f"Coin Change II (amount=5, coins=[1,2,5]): {change(5, [1, 2, 5])}")
    print(f"Target Sum [1,1,1,1,1], target=3: {find_target_sum_ways([1, 1, 1, 1, 1], 3)}")
    print(f"Interleaving String 'aabcc', 'dbbca', 'aadbbcbcac': {is_interleave('aabcc', 'dbbca', 'aadbbcbcac')}")
    
    matrix = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
    print(f"Longest Increasing Path: {longest_increasing_path(matrix)}")
    
    print(f"Distinct Subsequences 'rabbbit', 'rabbit': {num_distinct('rabbbit', 'rabbit')}")
    print(f"Edit Distance 'horse', 'ros': {min_distance('horse', 'ros')}")
    print(f"Max Coins [3,1,5,8]: {max_coins([3, 1, 5, 8])}")
    print(f"Regex Match 'aa', 'a*': {is_match('aa', 'a*')}")
