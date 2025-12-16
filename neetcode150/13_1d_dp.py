"""
NeetCode 150 - 1-D Dynamic Programming
=======================================
Linear DP problems (12 problems).
"""


# PATTERN: Fibonacci DP
def climb_stairs(n):
    """
    Climbing Stairs - ways to reach top (1 or 2 steps).
    
    Pattern: Fibonacci sequence
    
    Time: O(n), Space: O(1)
    """
    if n <= 2:
        return n
    
    one, two = 1, 2
    for _ in range(n - 2):
        one, two = two, one + two
    
    return two


# PATTERN: Linear DP
def min_cost_climbing_stairs(cost):
    """
    Min Cost Climbing Stairs.
    
    Pattern: DP with choice (take from i or i+1)
    
    Time: O(n), Space: O(1)
    """
    one, two = 0, 0
    
    for i in range(len(cost)):
        temp = cost[i] + min(one, two)
        one, two = two, temp
    
    return min(one, two)


# PATTERN: Fibonacci with Constraint
def rob(nums):
    """
    House Robber - max money without robbing adjacent houses.
    
    Pattern: DP with skip constraint
    
    Time: O(n), Space: O(1)
    """
    rob1, rob2 = 0, 0
    
    for num in nums:
        temp = max(rob1 + num, rob2)
        rob1, rob2 = rob2, temp
    
    return rob2


# PATTERN: Circular Array DP
def rob2(nums):
    """
    House Robber II - houses in circle.
    
    Pattern: Two passes (exclude first or last)
    
    Time: O(n), Space: O(1)
    """
    def rob_linear(houses):
        rob1, rob2 = 0, 0
        for num in houses:
            temp = max(rob1 + num, rob2)
            rob1, rob2 = rob2, temp
        return rob2
    
    if len(nums) == 1:
        return nums[0]
    
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


# PATTERN: Subsequence DP
def longest_palindrome(s):
    """
    Longest Palindromic Substring.
    
    Pattern: Expand around center
    
    Time: O(n^2), Space: O(1)
    """
    result = ""
    
    for i in range(len(s)):
        # Odd length palindromes
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > len(result):
                result = s[l:r + 1]
            l -= 1
            r += 1
        
        # Even length palindromes
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > len(result):
                result = s[l:r + 1]
            l -= 1
            r += 1
    
    return result


# PATTERN: State Machine DP
def count_substrings(s):
    """
    Palindromic Substrings - count all palindromic substrings.
    
    Pattern: Expand around center
    
    Time: O(n^2), Space: O(1)
    """
    count = 0
    
    for i in range(len(s)):
        # Odd length
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
        
        # Even length
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
    
    return count


# PATTERN: String DP
def decode_ways(s):
    """
    Decode Ways - number of ways to decode string.
    
    Pattern: DP with 1-digit and 2-digit choices
    
    Time: O(n), Space: O(1)
    """
    if s[0] == '0':
        return 0
    
    one, two = 1, 1
    
    for i in range(1, len(s)):
        temp = 0
        
        if s[i] != '0':
            temp = one
        
        if 10 <= int(s[i - 1:i + 1]) <= 26:
            temp += two
        
        one, two = temp, one
    
    return one


# PATTERN: Unbounded Knapsack
def coin_change(coins, amount):
    """
    Coin Change - minimum coins to make amount.
    
    Pattern: Unbounded knapsack (can reuse coins)
    
    Time: O(amount * len(coins)), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for coin in coins:
            if a >= coin:
                dp[a] = min(dp[a], 1 + dp[a - coin])
    
    return dp[amount] if dp[amount] != float('inf') else -1


# PATTERN: Bounded Knapsack
def max_product(nums):
    """
    Maximum Product Subarray.
    
    Pattern: Track both max and min (negatives flip signs)
    
    Time: O(n), Space: O(1)
    """
    result = max(nums)
    curr_max, curr_min = 1, 1
    
    for num in nums:
        temp = curr_max * num
        curr_max = max(num, temp, curr_min * num)
        curr_min = min(num, temp, curr_min * num)
        result = max(result, curr_max)
    
    return result


# PATTERN: DP with Comparison
def word_break(s, wordDict):
    """
    Word Break - can segment string into dictionary words.
    
    Pattern: DP with substring checking
    
    Time: O(n^2 * m) where m = avg word length
    Space: O(n)
    """
    dp = [False] * (len(s) + 1)
    dp[0] = True
    word_set = set(wordDict)
    
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[len(s)]


# PATTERN: Subsequence DP (LIS)
def length_of_lis(nums):
    """
    Longest Increasing Subsequence.
    
    Pattern: Binary search + patience sorting
    
    Time: O(n log n), Space: O(n)
    """
    import bisect
    
    sub = []
    
    for num in nums:
        pos = bisect.bisect_left(sub, num)
        if pos == len(sub):
            sub.append(num)
        else:
            sub[pos] = num
    
    return len(sub)


# PATTERN: Partition DP
def can_partition(nums):
    """
    Partition Equal Subset Sum.
    
    Pattern: 0/1 knapsack (target = sum/2)
    
    Time: O(n * sum), Space: O(sum)
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    
    target = total // 2
    dp = set([0])
    
    for num in nums:
        new_dp = set()
        for s in dp:
            if s + num == target:
                return True
            new_dp.add(s)
            new_dp.add(s + num)
        dp = new_dp
    
    return False


if __name__ == "__main__":
    print("=== NeetCode 150 - 1-D Dynamic Programming ===\n")
    
    print(f"Climbing Stairs (n=5): {climb_stairs(5)}")
    print(f"Min Cost Climbing Stairs [10,15,20]: {min_cost_climbing_stairs([10, 15, 20])}")
    print(f"House Robber [1,2,3,1]: {rob([1, 2, 3, 1])}")
    print(f"House Robber II [2,3,2]: {rob2([2, 3, 2])}")
    print(f"Longest Palindrome 'babad': {longest_palindrome('babad')}")
    print(f"Count Palindromic Substrings 'abc': {count_substrings('abc')}")
    print(f"Decode Ways '12': {decode_ways('12')}")
    print(f"Coin Change [1,2,5], 11: {coin_change([1, 2, 5], 11)}")
    print(f"Max Product Subarray [2,3,-2,4]: {max_product([2, 3, -2, 4])}")
    print(f"Word Break 'leetcode', ['leet','code']: {word_break('leetcode', ['leet', 'code'])}")
    print(f"Length of LIS [10,9,2,5,3,7,101,18]: {length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])}")
    print(f"Can Partition [1,5,11,5]: {can_partition([1, 5, 11, 5])}")
