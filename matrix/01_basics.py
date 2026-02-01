"""
Matrix - Basics
==============
Fundamental matrix operations and concepts.
"""

print("=" * 60)
print("Matrix Creation and Initialization")
print("=" * 60)
print()

# Create matrix
rows, cols = 3, 4

# Method 1: List comprehension
matrix1 = [[0 for _ in range(cols)] for _ in range(rows)]
print("Zero matrix (3x4):")
for row in matrix1:
    print(f"  {row}")
print()

# Method 2: Initialize with values
matrix2 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
print("Matrix with values:")
for row in matrix2:
    print(f"  {row}")
print()

# Method 3: Identity matrix
n = 4
identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
print(f"Identity matrix ({n}x{n}):")
for row in identity:
    print(f"  {row}")
print()

# WARNING: Don't do this! (all rows reference same list)
wrong_matrix = [[0] * cols] * rows
wrong_matrix[0][0] = 1
print("WRONG way (shared reference):")
for row in wrong_matrix:
    print(f"  {row}")  # All rows affected!
print()


print("=" * 60)
print("Accessing Elements")
print("=" * 60)
print()

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Matrix:")
for row in matrix:
    print(f"  {row}")
print()

print("Accessing elements:")
print(f"  matrix[0][0] = {matrix[0][0]} (top-left)")
print(f"  matrix[1][1] = {matrix[1][1]} (center)")
print(f"  matrix[2][2] = {matrix[2][2]} (bottom-right)")
print(f"  matrix[-1][-1] = {matrix[-1][-1]} (bottom-right using negative)")
print()

# Get dimensions
m = len(matrix)  # number of rows
n = len(matrix[0]) if m > 0 else 0  # number of columns
print(f"Dimensions: {m} x {n}")
print()


print("=" * 60)
print("Row and Column Operations")
print("=" * 60)
print()

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

# Get specific row
row_1 = matrix[1]
print(f"Row 1: {row_1}")

# Get specific column
col_2 = [row[2] for row in matrix]
print(f"Column 2: {col_2}")
print()

# Sum of row
row_sum = sum(matrix[0])
print(f"Sum of row 0: {row_sum}")

# Sum of column
col_sum = sum(row[1] for row in matrix)
print(f"Sum of column 1: {col_sum}")

# Sum of all elements
total_sum = sum(sum(row) for row in matrix)
print(f"Sum of all elements: {total_sum}")
print()


print("=" * 60)
print("Matrix Traversal Patterns")
print("=" * 60)
print()

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Row-major order (default)
print("Row-major traversal:")
elements = []
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        elements.append(matrix[i][j])
print(f"  {elements}")
print()

# Column-major order
print("Column-major traversal:")
elements = []
for j in range(len(matrix[0])):
    for i in range(len(matrix)):
        elements.append(matrix[i][j])
print(f"  {elements}")
print()

# Diagonal (main diagonal)
print("Main diagonal:")
diagonal = [matrix[i][i] for i in range(min(len(matrix), len(matrix[0])))]
print(f"  {diagonal}")
print()

# Anti-diagonal
print("Anti-diagonal:")
n = len(matrix)
anti_diagonal = [matrix[i][n-1-i] for i in range(n)]
print(f"  {anti_diagonal}")
print()


print("=" * 60)
print("Four Directional Movement")
print("=" * 60)
print()

def get_neighbors(i, j, m, n):
    """Get all valid neighbors in 4 directions."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    neighbors = []
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n:
            neighbors.append((ni, nj))
    
    return neighbors

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
m, n = len(matrix), len(matrix[0])

print("4-directional neighbors:")
for i in range(m):
    for j in range(n):
        neighbors = get_neighbors(i, j, m, n)
        values = [matrix[ni][nj] for ni, nj in neighbors]
        print(f"  ({i},{j}) value={matrix[i][j]}: neighbors = {values}")
print()


print("=" * 60)
print("Eight Directional Movement")
print("=" * 60)
print()

def get_neighbors_8(i, j, m, n):
    """Get all valid neighbors in 8 directions."""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    neighbors = []
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n:
            neighbors.append((ni, nj))
    
    return neighbors

print("8-directional neighbors for center cell (1,1):")
neighbors = get_neighbors_8(1, 1, m, n)
values = [matrix[ni][nj] for ni, nj in neighbors]
print(f"  Center value: {matrix[1][1]}")
print(f"  All neighbors: {values}")
print()


print("=" * 60)
print("Matrix Properties")
print("=" * 60)
print()

def is_square(matrix):
    """Check if matrix is square."""
    return len(matrix) == len(matrix[0]) if matrix else True

def is_symmetric(matrix):
    """Check if matrix is symmetric."""
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def is_diagonal(matrix):
    """Check if matrix is diagonal."""
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] != 0:
                return False
    return True

matrices = {
    "Square": [[1, 2], [3, 4]],
    "Symmetric": [[1, 2, 3], [2, 5, 6], [3, 6, 9]],
    "Diagonal": [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
    "Identity": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
}

for name, mat in matrices.items():
    print(f"{name} matrix:")
    for row in mat:
        print(f"  {row}")
    print(f"  Square: {is_square(mat)}")
    print(f"  Symmetric: {is_symmetric(mat)}")
    print(f"  Diagonal: {is_diagonal(mat)}")
    print()


print("=" * 60)
print("Common Matrix Operations")
print("=" * 60)
print()

def print_matrix(matrix, name="Matrix"):
    """Helper to print matrix."""
    print(f"{name}:")
    for row in matrix:
        print(f"  {row}")
    print()

# Transpose
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
print_matrix(matrix, "Original (2x3)")

transposed = [[matrix[j][i] for j in range(len(matrix))] 
              for i in range(len(matrix[0]))]
print_matrix(transposed, "Transposed (3x2)")

# Flip horizontal (reverse each row)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print_matrix(matrix, "Original")

flipped_h = [row[::-1] for row in matrix]
print_matrix(flipped_h, "Flipped Horizontal")

# Flip vertical (reverse row order)
flipped_v = matrix[::-1]
print_matrix(flipped_v, "Flipped Vertical")

# Find min/max
matrix = [
    [3, 1, 4],
    [1, 5, 9],
    [2, 6, 5]
]
min_val = min(min(row) for row in matrix)
max_val = max(max(row) for row in matrix)
print(f"Matrix: {matrix}")
print(f"Min value: {min_val}")
print(f"Max value: {max_val}")
print()


print("=" * 60)
print("Submatrix Operations")
print("=" * 60)
print()

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

print_matrix(matrix, "Original 4x4")

# Extract submatrix
def get_submatrix(matrix, r1, c1, r2, c2):
    """Extract submatrix from (r1,c1) to (r2,c2) inclusive."""
    return [row[c1:c2+1] for row in matrix[r1:r2+1]]

submatrix = get_submatrix(matrix, 1, 1, 2, 2)
print_matrix(submatrix, "Submatrix [1:2, 1:2]")


print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Key Points:")
print("  • Create matrix: [[0] * cols for _ in range(rows)]")
print("  • Access: matrix[row][col]")
print("  • Dimensions: m = len(matrix), n = len(matrix[0])")
print("  • Row-major: iterate rows first")
print("  • Column-major: iterate columns first")
print("  • 4-directions: [(0,1), (1,0), (0,-1), (-1,0)]")
print("  • 8-directions: add diagonals")
print("  • Always check boundaries: 0 <= i < m and 0 <= j < n")
