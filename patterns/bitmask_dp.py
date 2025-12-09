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

def smallest_sufficient_team(skills, people):
            """
            Problem: Given required `skills` (list of strings) and `people` where each person has a list
            of skills, return indices of the smallest team covering all required skills.

            Technique: Bitmask DP over the set of skills.

            Mapping:
            - Map each skill to a bit position [0..m-1], m = len(skills)
            - For each person, compress their skills into a bitmask `pmask`.

            DP State:
            - dp[mask] = list of people indices forming a minimal team that covers `mask` skills
            - Start with dp[0] = [] and iteratively try to add each person to improve coverage.

            Steps:
            1) Build skill->bit mapping and compute every person's `pmask`.
            2) Initialize `dp` with `None` for all masks except `dp[0] = []`.
            3) For each person i with `pmask`, for each `mask` where `dp[mask]` is known, compute `new_mask = mask | pmask`.
               - If `dp[new_mask]` is None or longer than `dp[mask] + [i]`, update it.
            4) Return `dp[all_mask]` where `all_mask = (1<<m) - 1`.

            Correctness:
            - We perform a relaxation over subsets of skills. Each transition either keeps or adds a person,
              monotonically increasing covered skills. We always keep the shortest team found for each mask.

            Complexity:
            - Let m = number of skills, n = number of people.
            - Time ~ O(n * 2^m) in the worst case; Space ~ O(2^m * m) for storing teams.
            """
            m = len(skills)
            skill_to_bit = {s: idx for idx, s in enumerate(skills)}

            people_masks = []
            for plist in people:
                pmask = 0
                for s in plist:
                    if s in skill_to_bit:
                        pmask |= 1 << skill_to_bit[s]
                people_masks.append(pmask)

            all_mask = (1 << m) - 1
            dp = [None] * (1 << m)
            dp[0] = []

            for i, pmask in enumerate(people_masks):
                if pmask == 0:
                    continue
                # iterate on a snapshot to avoid chaining within same person iteration
                prev_dp = dp[:]
                for mask in range(1 << m):
                    team = prev_dp[mask]
                    if team is None:
                        continue
                    new_mask = mask | pmask
                    new_team = team + [i]
                    if dp[new_mask] is None or len(dp[new_mask]) > len(new_team):
                        dp[new_mask] = new_team

            return dp[all_mask] if dp[all_mask] is not None else []

# --- Can Partition to K Equal Sum Subsets (Bitmask + Memo) ---
def can_partition_k_subsets(nums, k):
            """
            Problem: Partition `nums` into `k` subsets with equal sum.

            Technique: Backtracking with memoization keyed by (used_mask, current_bucket_sum, buckets_left).

            Key Ideas:
            - target = total_sum / k; if not divisible, return False.
            - Sort nums descending to prune faster.
            - Use bitmask `used` to mark which indices are already placed.
            - Fill one bucket to `target` before moving to next; when a bucket is exactly `target`, reset current sum to 0 and decrement k.

            Steps:
            1) Validate divisibility and compute target. Sort nums descending.
            2) DFS(used_mask, curr_sum, buckets_left):
               - If buckets_left == 1: remaining nums must form last bucket ⇒ True.
               - If curr_sum == target: start new bucket ⇒ DFS(used_mask, 0, buckets_left-1).
               - Try each unused index i; if curr_sum + nums[i] <= target, mark used and recurse.
               - Memoize results by (used_mask, curr_sum, buckets_left).

            Correctness:
            - Each item is assigned to exactly one bucket; sum constraints ensure equal partition.
            - Memoization avoids recomputation of states, guaranteeing termination on feasible inputs.

            Complexity:
            - Exponential in worst-case, but pruning + memo significantly reduces search.
            """
            total = sum(nums)
            if total % k != 0:
                return False
            target = total // k
            nums.sort(reverse=True)
            if nums[0] > target:
                return False

            from functools import lru_cache

            n = len(nums)

            @lru_cache(maxsize=None)
            def dfs(used_mask, curr_sum, buckets_left):
                if buckets_left == 1:
                    return True
                if curr_sum == target:
                    return dfs(used_mask, 0, buckets_left - 1)

                # try placing next item
                for i in range(n):
                    if (used_mask >> i) & 1:
                        continue
                    val = nums[i]
                    if curr_sum + val > target:
                        continue
                    # choose
                    if dfs(used_mask | (1 << i), curr_sum + val, buckets_left):
                        return True
                return False

            return dfs(0, 0, k)

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
    # demos for newly added functions
    skills = ["java", "nodejs", "react"]
    people = [["java"], ["nodejs"], ["nodejs", "react"]]
    print("Smallest sufficient team:", smallest_sufficient_team(skills, people))
    print("Can partition into k subsets:", can_partition_k_subsets([4,3,2,3,5,2,1], 4))
