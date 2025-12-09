"""
DFS / Backtracking
==================
Explore all possibilities via depth-first search, backtracking on dead ends.
"""


def subsets(nums):
    """
    Generate all subsets of nums.
    Time: O(n·2^n) Space: O(n)
    """
    res = []
    cur = []
    def backtrack(i):
        if i == len(nums):
            res.append(cur[:])
            return
        # choose
        cur.append(nums[i])
        backtrack(i + 1)
        # unchoose
        cur.pop()
        backtrack(i + 1)
    backtrack(0)
    return res


def permutations(nums):
    """
    Generate all permutations of nums.
    Time: O(n·n!)
    """
    res = []
    used = [False] * len(nums)
    cur = []
    def backtrack():
        if len(cur) == len(nums):
            res.append(cur[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            cur.append(nums[i])
            backtrack()
            cur.pop()
            used[i] = False
    backtrack()
    return res


def path_exists(graph, start, end):
    """
    DFS on adjacency list to find path existence.
    Time: O(V+E)
    """
    visited = set()
    def dfs(v):
        if v == end:
            return True
        visited.add(v)
        for nbr in graph.get(v, []):
            if nbr not in visited and dfs(nbr):
                return True
        return False
    return dfs(start)


if __name__ == "__main__":
    print("subsets:", subsets([1,2]))
    print("perms:", permutations([1,2,3]))
    g = {0:[1],1:[2],2:[3],3:[]}
    print("path 0->3:", path_exists(g,0,3))
