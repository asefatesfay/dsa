# Matrix / 2D Arrays

Matrix manipulation and 2D array algorithms.

## Overview

Matrices (2D arrays) are fundamental data structures used in various algorithmic problems. This module covers traversal patterns, transformations, and search algorithms on 2D grids.

## Contents

### 01_basics.py
- Matrix creation and initialization
- Accessing elements
- Row and column operations
- Matrix traversal (row-major, column-major)
- Diagonal traversal
- Matrix properties

### 02_traversal_patterns.py
- Spiral traversal
- Zigzag (snake) traversal
- Diagonal traversal
- Layer-by-layer traversal
- DFS on grid
- BFS on grid
- Four/eight-directional movement

### 03_transformations.py
- Matrix rotation (90°, 180°, 270°)
- Matrix transpose
- Flip horizontal/vertical
- Set zeros
- Submatrix operations
- Matrix multiplication

### 04_leetcode_problems.py
- Spiral Matrix (LC 54)
- Rotate Image (LC 48)
- Set Matrix Zeroes (LC 73)
- Search 2D Matrix (LC 74, 240)
- Number of Islands (LC 200)
- Max Area of Island (LC 695)
- Pacific Atlantic Water Flow (LC 417)
- Surrounded Regions (LC 130)
- Word Search (LC 79)
- Unique Paths (LC 62)

## Key Concepts

### Matrix Dimensions
- m × n matrix: m rows, n columns
- Access: matrix[row][column] or matrix[i][j]
- Row-major order: traverse rows first
- Column-major order: traverse columns first

### Time Complexity
- Access element: O(1)
- Traverse all elements: O(m × n)
- Row/column operation: O(n) or O(m)
- Search (unsorted): O(m × n)
- Search (sorted rows/cols): O(m + n) or O(log(m×n))

### Space Complexity
- Storage: O(m × n)
- In-place operations: O(1)
- With visited tracking: O(m × n)

## Common Patterns

### 1. Four-Directional Movement
```python
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

for dr, dc in directions:
    new_row, new_col = row + dr, col + dc
    if 0 <= new_row < m and 0 <= new_col < n:
        # Process neighbor
```

### 2. Eight-Directional Movement
```python
directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]
```

### 3. Spiral Traversal
```python
top, bottom = 0, m - 1
left, right = 0, n - 1

while top <= bottom and left <= right:
    # Right, down, left, up
```

### 4. DFS on Grid
```python
def dfs(i, j):
    if not (0 <= i < m and 0 <= j < n) or visited[i][j]:
        return
    
    visited[i][j] = True
    for di, dj in directions:
        dfs(i + di, j + dj)
```

### 5. BFS on Grid
```python
from collections import deque

queue = deque([(start_i, start_j)])
visited = set([(start_i, start_j)])

while queue:
    i, j = queue.popleft()
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if (ni, nj) not in visited:
            queue.append((ni, nj))
            visited.add((ni, nj))
```

### 6. Layer-by-Layer Processing
```python
for layer in range(min(m, n) // 2):
    # Process outer layer
    # Move to inner layer
```

## Common Operations

### Rotation
- 90° clockwise: Transpose + reverse each row
- 90° counter-clockwise: Reverse each row + transpose
- 180°: Reverse rows + reverse each row

### Transpose
```python
# In-place for square matrix
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

### Set Zeros
Use first row/column as markers to achieve O(1) space.

## Problem Categories

### Search Problems
- Binary search in sorted matrix
- Search in row-wise and column-wise sorted matrix
- Find peak element in 2D array

### Graph Problems on Grid
- Number of islands (DFS/BFS/Union-Find)
- Shortest path (BFS)
- Connected components
- Flood fill

### Dynamic Programming
- Unique paths
- Minimum path sum
- Maximal rectangle
- Largest square

### Traversal Problems
- Spiral matrix
- Zigzag traversal
- Diagonal traversal
- Snake pattern

### Transformation Problems
- Rotate image
- Transpose
- Flip matrix
- Set zeros

## Interview Tips

### Boundary Handling
- Always check: `0 <= i < m and 0 <= j < n`
- Watch for empty matrix edge cases
- Consider single row/column matrices

### Space Optimization
- Can you use the matrix itself for tracking?
- Use first row/column as markers
- Bit manipulation for boolean grids

### Common Mistakes
- Confusing row/column indices
- Off-by-one errors in boundaries
- Forgetting to mark cells as visited in DFS/BFS
- Not handling empty or single-element matrices

### Optimization Techniques
- Use visited set/array to avoid re-processing
- For sorted matrices, use binary search
- Consider in-place modifications
- Use proper data structures (deque for BFS)

## Real-World Applications

- **Image Processing**: Convolution, filters, transformations
- **Game Development**: Grid-based games, pathfinding
- **Computer Graphics**: 2D graphics, sprites
- **Data Science**: Data frames, numerical computations
- **Maps/Navigation**: Grid-based maps, tile systems
- **Circuit Design**: Grid layouts
- **Scientific Computing**: Numerical simulations
