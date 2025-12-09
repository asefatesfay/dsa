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

# --- Combination Sum ---
def combination_sum(candidates, target):
    """
    Generate all combinations where numbers can be used unlimited times to sum to target.
    Backtracking with index and running sum.
    """
    candidates.sort()
    res = []
    cur = []
    def dfs(i, total):
        if total == target:
            res.append(cur[:])
            return
        if total > target or i == len(candidates):
            return
        # choose i
        cur.append(candidates[i])
        dfs(i, total + candidates[i])
        cur.pop()
        # skip i
        dfs(i + 1, total)
    dfs(0, 0)
    return res

# --- N-Queens ---
def n_queens(n):
    """
    Place n queens so none attack each other; return board configurations.
    Track used columns and diagonals with sets.
    """
    res = []
    cols = set()
    d1 = set()  # r-c
    d2 = set()  # r+c
    board = [['.']*n for _ in range(n)]
    def dfs(r):
        if r == n:
            res.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r-c) in d1 or (r+c) in d2:
                continue
            cols.add(c); d1.add(r-c); d2.add(r+c)
            board[r][c] = 'Q'
            dfs(r+1)
            board[r][c] = '.'
            cols.remove(c); d1.remove(r-c); d2.remove(r+c)
    dfs(0)
    return res

# --- Word Search ---
def word_search(board, word):
    """
    Determine if `word` exists in the grid via 4-dir DFS visiting each cell at most once per path.
    """
    R = len(board)
    C = len(board[0]) if R else 0
    visited = [[False]*C for _ in range(R)]
    def dfs(r,c,idx):
        if idx == len(word):
            return True
        if r<0 or r>=R or c<0 or c>=C or visited[r][c] or board[r][c] != word[idx]:
            return False
        visited[r][c] = True
        res = dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1)
        visited[r][c] = False
        return res
    for r in range(R):
        for c in range(C):
            if dfs(r,c,0):
                return True
    return False

if __name__ == "__main__":
    print("combination_sum:", combination_sum([2,3,6,7], 7))
    for line in n_queens(4):
        print(line)
    board = [
        ['A','B','C','E'],
        ['S','F','C','S'],
        ['A','D','E','E']
    ]
    print("word_search(ABCCED):", word_search(board, "ABCCED"))
