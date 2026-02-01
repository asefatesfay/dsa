"""
Matrix - Traversal Patterns
===========================
Common matrix traversal patterns for interviews.
"""

from collections import deque
from typing import List


print("=" * 60)
print("Pattern 1: Spiral Traversal")
print("=" * 60)
print()

def spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    Traverse matrix in spiral order (clockwise from outside).
    
    Time: O(m*n), Space: O(1)
    """
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Move right along top row
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # Move down along right column
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        # Move left along bottom row (if exists)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        # Move up along left column (if exists)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print(f"Spiral order: {spiral_order(matrix)}")
print()


print("=" * 60)
print("Pattern 2: Zigzag (Snake) Traversal")
print("=" * 60)
print()

def zigzag_traversal(matrix: List[List[int]]) -> List[int]:
    """
    Traverse matrix in zigzag pattern.
    Row 0: left to right
    Row 1: right to left
    Row 2: left to right, etc.
    
    Time: O(m*n), Space: O(1)
    """
    result = []
    for i, row in enumerate(matrix):
        if i % 2 == 0:
            result.extend(row)
        else:
            result.extend(row[::-1])
    return result

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print(f"Zigzag order: {zigzag_traversal(matrix)}")
print()


print("=" * 60)
print("Pattern 3: Diagonal Traversal")
print("=" * 60)
print()

def diagonal_order(matrix: List[List[int]]) -> List[int]:
    """
    Traverse matrix diagonally (anti-diagonals).
    
    Time: O(m*n), Space: O(1)
    """
    if not matrix:
        return []
    
    m, n = len(matrix), len(matrix[0])
    result = []
    
    # Process each diagonal
    for d in range(m + n - 1):
        intermediate = []
        
        # Determine starting point
        row = 0 if d < n else d - n + 1
        col = d if d < n else n - 1
        
        # Collect diagonal elements
        while row < m and col >= 0:
            intermediate.append(matrix[row][col])
            row += 1
            col -= 1
        
        # Reverse every other diagonal
        if d % 2 == 0:
            result.extend(intermediate[::-1])
        else:
            result.extend(intermediate)
    
    return result

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print(f"Diagonal order: {diagonal_order(matrix)}")
print()


print("=" * 60)
print("Pattern 4: Layer-by-Layer Traversal")
print("=" * 60)
print()

def layer_traversal(matrix: List[List[int]]) -> List[List[int]]:
    """
    Extract elements layer by layer (like onion layers).
    
    Time: O(m*n), Space: O(1)
    """
    if not matrix:
        return []
    
    layers = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        layer = []
        
        # Top row
        for col in range(left, right + 1):
            layer.append(matrix[top][col])
        top += 1
        
        # Right column
        for row in range(top, bottom + 1):
            layer.append(matrix[row][right])
        right -= 1
        
        # Bottom row
        if top <= bottom:
            for col in range(right, left - 1, -1):
                layer.append(matrix[bottom][col])
            bottom -= 1
        
        # Left column
        if left <= right:
            for row in range(bottom, top - 1, -1):
                layer.append(matrix[row][left])
            left += 1
        
        layers.append(layer)
    
    return layers

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print("Layers:")
for i, layer in enumerate(layer_traversal(matrix)):
    print(f"  Layer {i}: {layer}")
print()


print("=" * 60)
print("Pattern 5: DFS on Grid")
print("=" * 60)
print()

def dfs_grid(matrix: List[List[int]], start_i: int, start_j: int) -> List[int]:
    """
    DFS traversal starting from (start_i, start_j).
    Visits all reachable cells.
    
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(matrix), len(matrix[0])
    visited = [[False] * n for _ in range(m)]
    result = []
    
    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n) or visited[i][j]:
            return
        
        visited[i][j] = True
        result.append(matrix[i][j])
        
        # Visit 4 neighbors
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for di, dj in directions:
            dfs(i + di, j + dj)
    
    dfs(start_i, start_j)
    return result

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print(f"DFS from (0,0): {dfs_grid(matrix, 0, 0)}")
print()


print("=" * 60)
print("Pattern 6: BFS on Grid")
print("=" * 60)
print()

def bfs_grid(matrix: List[List[int]], start_i: int, start_j: int) -> List[int]:
    """
    BFS traversal starting from (start_i, start_j).
    Visits cells level by level.
    
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(matrix), len(matrix[0])
    visited = [[False] * n for _ in range(m)]
    result = []
    
    queue = deque([(start_i, start_j)])
    visited[start_i][start_j] = True
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        i, j = queue.popleft()
        result.append(matrix[i][j])
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj]:
                visited[ni][nj] = True
                queue.append((ni, nj))
    
    return result

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print(f"BFS from (1,1): {bfs_grid(matrix, 1, 1)}")
print()


print("=" * 60)
print("Pattern 7: All Paths (Backtracking)")
print("=" * 60)
print()

def find_all_paths(matrix: List[List[int]]) -> List[List[int]]:
    """
    Find all paths from top-left to bottom-right.
    Can only move right or down.
    
    Time: O(2^(m+n)), Space: O(m+n)
    """
    if not matrix:
        return []
    
    m, n = len(matrix), len(matrix[0])
    paths = []
    
    def backtrack(i, j, path):
        if i == m - 1 and j == n - 1:
            paths.append(path + [matrix[i][j]])
            return
        
        if i >= m or j >= n:
            return
        
        # Move right
        backtrack(i, j + 1, path + [matrix[i][j]])
        # Move down
        backtrack(i + 1, j, path + [matrix[i][j]])
    
    backtrack(0, 0, [])
    return paths

matrix = [
    [1, 2],
    [3, 4]
]
print("Matrix:")
for row in matrix:
    print(f"  {row}")
print("All paths (top-left to bottom-right):")
for i, path in enumerate(find_all_paths(matrix)):
    print(f"  Path {i+1}: {path}")
print()


print("=" * 60)
print("Summary of Traversal Patterns")
print("=" * 60)
print()
print("1. Spiral: Clockwise from outside to inside")
print("2. Zigzag: Alternate row directions")
print("3. Diagonal: Process anti-diagonals")
print("4. Layer-by-Layer: Onion-like peeling")
print("5. DFS: Depth-first recursive/stack")
print("6. BFS: Level-order with queue")
print("7. Backtracking: Find all paths")
print()
print("When to use:")
print("  • Spiral: Display/print problems")
print("  • DFS: Connected components, flood fill")
print("  • BFS: Shortest path, level-order")
print("  • Backtracking: All solutions, paths")
