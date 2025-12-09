"""
Dynamic Programming (DP) Patterns
================================
Core templates and worked problems with detailed algorithm descriptions.
"""

# Template 1: 1D DP (e.g., Fibonacci, climbing stairs)
def climb_stairs(n):
    """
    Problem: Number of ways to climb n stairs taking 1 or 2 steps.
    Recurrence: dp[i] = dp[i-1] + dp[i-2]
    Time: O(n) Space: O(1)
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# Template 2: 0/1 Knapsack
def knapsack_01(weights, values, W):
    """
    Problem: Max value with capacity W, each item can be taken at most once.
    Recurrence: dp[w] = max(dp[w], dp[w-wi] + vi) iterating w descending.
    Time: O(nW) Space: O(W)
    """
    dp = [0] * (W + 1)
    for wi, vi in zip(weights, values):
        for w in range(W, wi - 1, -1):
            dp[w] = max(dp[w], dp[w - wi] + vi)
    return dp[W]


# Template 3: Longest Increasing Subsequence (LIS)
def lis_length(nums):
    """
    Problem: Length of LIS.
    Method: Patience sorting with tails (binary search).
    Time: O(n log n) Space: O(n)
    """
    import bisect
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


# Template 4: Edit Distance (Levenshtein)
def edit_distance(a, b):
    """
    Problem: Min operations to convert string a to b (insert/delete/replace).
    Recurrence: dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    Time: O(nm) Space: O(m)
    """
    n, m = len(a), len(b)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(
                prev[j] + 1,      # delete a[i-1]
                cur[j - 1] + 1,   # insert b[j-1]
                prev[j - 1] + cost  # replace/match
            )
        prev = cur
    return prev[m]


# Problem Set
# 1) House Robber (non-adjacent max sum)
def house_robber(nums):
    """
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    Time: O(n) Space: O(1)
    """
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1


# 2) Coin Change (min coins)
def coin_change(coins, amount):
    """
    dp[x] = min over coins (dp[x-coin] + 1)
    Time: O(n·amount)
    """
    INF = amount + 1
    dp = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if x - c >= 0:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != INF else -1


# 3) Maximum Subarray (Kadane)
def max_subarray(nums):
    """
    dp: best ending at i. Time: O(n) Space: O(1)
    """
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


if __name__ == "__main__":
    print(climb_stairs(5))            # 8
    print(knapsack_01([2,3,4],[4,5,6], 5))  # 9
    print(lis_length([10,9,2,5,3,7,101,18]))  # 4
    print(edit_distance("horse","ros"))  # 3
    print(house_robber([2,7,9,3,1]))  # 12
    print(coin_change([1,2,5], 11))   # 3
    print(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))  # 6

# =====================
# Additional DP Problems
# =====================

def partition_equal_subset_sum(nums):
    """
    Determine if array can be partitioned into two subsets with equal sum.
    Use 1D DP over sums.
    Time: O(n·S) Space: O(S)
    """
    S = sum(nums)
    if S % 2:
        return False
    target = S // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]
    return dp[target]


def min_path_sum(grid):
    """
    Min path sum from top-left to bottom-right (move only right/down).
    Time: O(mn) Space: O(n)
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    dp = [10**9] * n
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[j] = grid[i][j]
            elif i == 0:
                dp[j] = dp[j - 1] + grid[i][j]
            elif j == 0:
                dp[j] = dp[j] + grid[i][j]
            else:
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]
    return dp[-1]


def lcs(a, b):
    """
    Longest Common Subsequence length.
    Time: O(nm) Space: O(m)
    """
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[m]


if __name__ == "__main__":
    print("partition equal:", partition_equal_subset_sum([1,5,11,5]))  # True
    print("min path sum:", min_path_sum([[1,3,1],[1,5,1],[4,2,1]]))  # 7
    print("lcs:", lcs("abcde", "ace"))  # 3
