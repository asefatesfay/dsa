"""
Matrix - LeetCode Problems
==========================
Essential matrix problems for interviews.
"""

from typing import List
from collections import deque


print("=" * 70)
print("Problem 1: Spiral Matrix (LC 54)")
print("=" * 70)
print()

def spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    Return elements in spiral order (clockwise from outside).
    
    Approach: Track boundaries, move right→down→left→up, shrink bounds.
    Time: O(m*n), Space: O(1) excluding output
    """
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # Down
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        # Left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        # Up
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Matrix: {matrix}")
print(f"Spiral: {spiral_order(matrix)}")
print()


print("=" * 70)
print("Problem 2: Rotate Image (LC 48)")
print("=" * 70)
print()

def rotate(matrix: List[List[int]]) -> None:
    """
    Rotate matrix 90° clockwise in-place.
    
    Approach: Transpose + Reverse each row
    Time: O(n²), Space: O(1)
    """
    n = len(matrix)
    
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for row in matrix:
        row.reverse()

matrix = [[1,2,3],[4,5,6],[7,8,9]]
print(f"Before: {matrix}")
rotate(matrix)
print(f"After:  {matrix}")
print()


print("=" * 70)
print("Problem 3: Set Matrix Zeroes (LC 73)")
print("=" * 70)
print()

def set_zeroes(matrix: List[List[int]]) -> None:
    """
    Set entire row/col to 0 if element is 0.
    
    Approach: Use first row/col as markers
    Time: O(m*n), Space: O(1)
    """
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # Mark zeros in first row/col
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # Set zeros
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # Handle first row/col
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0

matrix = [[1,1,1],[1,0,1],[1,1,1]]
print(f"Before: {matrix}")
set_zeroes(matrix)
print(f"After:  {matrix}")
print()


print("=" * 70)
print("Problem 4: Search 2D Matrix (LC 74)")
print("=" * 70)
print()

def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Search in row/col sorted matrix.
    
    Approach: Treat as 1D sorted array, binary search
    Time: O(log(m*n)), Space: O(1)
    """
    if not matrix:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = (left + right) // 2
        val = matrix[mid // n][mid % n]
        
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False

matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
print(f"Matrix: {matrix}")
print(f"Search 3: {search_matrix(matrix, 3)}")
print(f"Search 13: {search_matrix(matrix, 13)}")
print()


print("=" * 70)
print("Problem 5: Search 2D Matrix II (LC 240)")
print("=" * 70)
print()

def search_matrix_ii(matrix: List[List[int]], target: int) -> bool:
    """
    Search in row-sorted and col-sorted matrix.
    
    Approach: Start top-right, move left or down
    Time: O(m+n), Space: O(1)
    """
    if not matrix:
        return False
    
    row, col = 0, len(matrix[0]) - 1
    
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1
    
    return False

matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22]]
print(f"Matrix: {matrix}")
print(f"Search 5: {search_matrix_ii(matrix, 5)}")
print(f"Search 20: {search_matrix_ii(matrix, 20)}")
print()


print("=" * 70)
print("Problem 6: Number of Islands (LC 200)")
print("=" * 70)
print()

def num_islands(grid: List[List[str]]) -> int:
    """
    Count islands (connected '1's).
    
    Approach: DFS to mark visited islands
    Time: O(m*n), Space: O(m*n) for recursion
    """
    if not grid:
        return 0
    
    def dfs(i, j):
        if (i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or 
            grid[i][j] != '1'):
            return
        
        grid[i][j] = '0'  # Mark visited
        dfs(i+1, j)
        dfs(i-1, j)
        dfs(i, j+1)
        dfs(i, j-1)
    
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    
    return count

grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
]
print(f"Grid has {num_islands([row[:] for row in grid])} islands")
print()


print("=" * 70)
print("Problem 7: Max Area of Island (LC 695)")
print("=" * 70)
print()

def max_area_of_island(grid: List[List[int]]) -> int:
    """
    Find maximum island area.
    
    Approach: DFS to calculate each island's area
    Time: O(m*n), Space: O(m*n)
    """
    if not grid:
        return 0
    
    def dfs(i, j):
        if (i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or 
            grid[i][j] != 1):
            return 0
        
        grid[i][j] = 0
        return 1 + dfs(i+1, j) + dfs(i-1, j) + dfs(i, j+1) + dfs(i, j-1)
    
    max_area = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                max_area = max(max_area, dfs(i, j))
    
    return max_area

grid = [
    [0,0,1,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1,1],
    [0,1,1,0,1,0,0,0,1],
    [0,1,0,0,1,1,0,0,1]
]
print(f"Max island area: {max_area_of_island([row[:] for row in grid])}")
print()


print("=" * 70)
print("Problem 8: Pacific Atlantic Water Flow (LC 417)")
print("=" * 70)
print()

def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    Find cells that can flow to both oceans.
    
    Approach: Reverse flow from oceans using DFS
    Time: O(m*n), Space: O(m*n)
    """
    if not heights:
        return []
    
    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    
    def dfs(i, j, visited):
        visited.add((i, j))
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            ni, nj = i + di, j + dj
            if (0 <= ni < m and 0 <= nj < n and 
                (ni, nj) not in visited and
                heights[ni][nj] >= heights[i][j]):
                dfs(ni, nj, visited)
    
    # Pacific: top row and left col
    for i in range(m):
        dfs(i, 0, pacific)
    for j in range(n):
        dfs(0, j, pacific)
    
    # Atlantic: bottom row and right col
    for i in range(m):
        dfs(i, n-1, atlantic)
    for j in range(n):
        dfs(m-1, j, atlantic)
    
    return list(pacific & atlantic)

heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
result = pacific_atlantic(heights)
print(f"Cells flowing to both oceans: {sorted(result)[:5]}...")
print()


print("=" * 70)
print("Problem 9: Word Search (LC 79)")
print("=" * 70)
print()

def exist(board: List[List[str]], word: str) -> bool:
    """
    Find if word exists in grid (DFS with backtracking).
    
    Time: O(m*n*4^L) where L is word length
    Space: O(L) for recursion
    """
    if not board:
        return False
    
    m, n = len(board), len(board[0])
    
    def dfs(i, j, k):
        if k == len(word):
            return True
        if (i < 0 or i >= m or j < 0 or j >= n or 
            board[i][j] != word[k]):
            return False
        
        temp = board[i][j]
        board[i][j] = '#'  # Mark visited
        
        found = (dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or
                 dfs(i, j+1, k+1) or dfs(i, j-1, k+1))
        
        board[i][j] = temp  # Backtrack
        return found
    
    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False

board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]
print(f"Board: {board}")
print(f"'ABCCED' exists: {exist([row[:] for row in board], 'ABCCED')}")
print(f"'SEE' exists: {exist([row[:] for row in board], 'SEE')}")
print(f"'ABCB' exists: {exist([row[:] for row in board], 'ABCB')}")
print()


print("=" * 70)
print("Problem 10: Unique Paths (LC 62)")
print("=" * 70)
print()

def unique_paths(m: int, n: int) -> int:
    """
    Count paths from top-left to bottom-right (only right/down).
    
    Approach: DP, dp[i][j] = dp[i-1][j] + dp[i][j-1]
    Time: O(m*n), Space: O(n) with rolling array
    """
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    
    return dp[-1]

print(f"Paths in 3x7 grid: {unique_paths(3, 7)}")
print(f"Paths in 3x2 grid: {unique_paths(3, 2)}")
print()


print("=" * 70)
print("Problem 11: Minimum Path Sum (LC 64)")
print("=" * 70)
print()

def min_path_sum(grid: List[List[int]]) -> int:
    """
    Find minimum path sum from top-left to bottom-right.
    
    Approach: DP, modify grid in-place
    Time: O(m*n), Space: O(1)
    """
    m, n = len(grid), len(grid[0])
    
    for i in range(1, m):
        grid[i][0] += grid[i-1][0]
    for j in range(1, n):
        grid[0][j] += grid[0][j-1]
    
    for i in range(1, m):
        for j in range(1, n):
            grid[i][j] += min(grid[i-1][j], grid[i][j-1])
    
    return grid[-1][-1]

grid = [[1,3,1],[1,5,1],[4,2,1]]
print(f"Grid: {grid}")
print(f"Min path sum: {min_path_sum([row[:] for row in grid])}")
print()


print("=" * 70)
print("Problem 12: Surrounded Regions (LC 130)")
print("=" * 70)
print()

def solve(board: List[List[str]]) -> None:
    """
    Capture surrounded regions (flip 'O' to 'X').
    
    Approach: DFS from borders to mark safe 'O's
    Time: O(m*n), Space: O(m*n)
    """
    if not board:
        return
    
    m, n = len(board), len(board[0])
    
    def dfs(i, j):
        if (i < 0 or i >= m or j < 0 or j >= n or 
            board[i][j] != 'O'):
            return
        board[i][j] = 'S'  # Mark safe
        dfs(i+1, j)
        dfs(i-1, j)
        dfs(i, j+1)
        dfs(i, j-1)
    
    # Mark border-connected 'O's
    for i in range(m):
        dfs(i, 0)
        dfs(i, n-1)
    for j in range(n):
        dfs(0, j)
        dfs(m-1, j)
    
    # Flip remaining 'O's to 'X', restore 'S' to 'O'
    for i in range(m):
        for j in range(n):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == 'S':
                board[i][j] = 'O'

board = [['X','X','X','X'],['X','O','O','X'],['X','X','O','X'],['X','O','X','X']]
print(f"Before: {board}")
solve(board)
print(f"After:  {board}")
print()


print("=" * 70)
print("Summary")
print("=" * 70)
print()
print("Key Patterns:")
print("  • Spiral: Track 4 boundaries, shrink after each layer")
print("  • Rotation: Transpose + Reverse rows (90° CW)")
print("  • Set Zeroes: Use first row/col as O(1) space markers")
print("  • Binary Search: Treat 2D as 1D array (index = row*n + col)")
print("  • Islands: DFS/BFS to mark connected components")
print("  • Flow: Reverse flow from destinations (oceans)")
print("  • Word Search: DFS with backtracking")
print("  • Path Counting: DP, dp[i][j] = dp[i-1][j] + dp[i][j-1]")
print()
print("Time Complexities:")
print("  • Most matrix problems: O(m*n)")
print("  • Binary search on matrix: O(log(m*n))")
print("  • DFS/BFS: O(m*n)")
print("  • Backtracking: O(m*n*4^L) worst case")
print()
print("Interview Tips:")
print("  ✓ Clarify if in-place modification allowed")
print("  ✓ Check for edge cases (empty, single element)")
print("  ✓ Consider space optimization with first row/col")
print("  ✓ Use visited set or modify grid to track visited")
print("  ✓ For flow problems, think backwards from destination")
