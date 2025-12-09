"""
Bitmasking / Bit DP
===================
Use bitmasks to represent subsets efficiently. Great for TSP, subset DP, assignment.
"""

# Example 1: Traveling Salesman Problem (TSP) on small graphs
# State: (mask, last) where mask marks visited, last is last city.
def tsp_brutish(dist):
    """
    dist: NxN matrix of distances. Start at 0, visit all, return to 0.
    DP[mask][i] = minimum cost to reach i having visited 'mask'.
    Time: O(n^2·2^n)
    """
    n = len(dist)
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # only city 0 visited, at 0
    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            cost = dp[mask][i]
            if cost == INF:
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                nxt = mask | (1 << j)
                dp[nxt][j] = min(dp[nxt][j], cost + dist[i][j])
    full = (1 << n) - 1
    ans = min(dp[full][i] + dist[i][0] for i in range(n))
    return ans


# Example 2: Count subsets with sum = target (bit tricks are optional but included)
def count_subsets_sum(nums, target):
    """
    DP over sums; bitset acceleration (if small target) demonstrates bitmask.
    Time: O(n·target)
    """
    dp = 1  # bitset where bit s is reachable sum s; start with sum 0
    for x in nums:
        dp |= dp << x
    return (dp >> target) & 1  # 1 if reachable, else 0


# Example 3: Assignment problem (min cost) using DP over subsets
def assignment_min_cost(cost):
    """
    cost: NxN matrix cost[i][j] assigning worker i to job j.
    State: dp[mask] = min cost when first popcount(mask) workers assigned to jobs in 'mask'.
    Time: O(n·2^n)
    """
    n = len(cost)
    INF = 10**9
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count("1")  # next worker index
        if i >= n:
            continue
        for j in range(n):
            if not (mask & (1 << j)):
                dp[mask | (1 << j)] = min(dp[mask | (1 << j)], dp[mask] + cost[i][j])
    return dp[(1 << n) - 1]


if __name__ == "__main__":
    d = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
    print("tsp:", tsp_brutish(d))
    print("subset sum reachable:", count_subsets_sum([2,3,7], 5))
    c = [[9,2,7],[6,4,3],[5,8,1]]
    print("assign:", assignment_min_cost(c))

# =====================
# Additional Bitmask DP Problems
# =====================

def min_xor_pair(nums):
    """
    Find minimal XOR of any pair. Sorting + linear scan.
    Time: O(n log n)
    """
    nums = sorted(nums)
    best = 10**9
    for i in range(1, len(nums)):
        best = min(best, nums[i] ^ nums[i - 1])
    return best


def max_compatibility_score(students, mentors):
    """
    Maximize sum of compatibility scores by assignment using DP over subsets.
    score(i,j) = number of equal answers.
    Time: O(n·2^n·m) where m = answers length
    """
    n = len(students)
    def score(s, m):
        return sum(int(a == b) for a, b in zip(s, m))
    scores = [[score(students[i], mentors[j]) for j in range(n)] for i in range(n)]
    dp = [-1] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count('1')  # next student index
        if i >= n:
            continue
        for j in range(n):
            if not (mask & (1 << j)):
                nxt = mask | (1 << j)
                dp[nxt] = max(dp[nxt], dp[mask] + scores[i][j])
    return dp[(1 << n) - 1]


if __name__ == "__main__":
    print("min xor pair:", min_xor_pair([0,2,5,7]))  # likely 2
    print("compat score:", max_compatibility_score([[1,1,0],[1,0,1],[0,0,1]], [[1,0,0],[0,0,1],[1,1,0]]))
