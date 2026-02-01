"""
Matrix - Transformations
========================
Matrix transformation operations.
"""

from typing import List


print("=" * 60)
print("Transformation 1: Rotate 90° Clockwise")
print("=" * 60)
print()

def rotate_90_clockwise(matrix: List[List[int]]) -> None:
    """
    Rotate matrix 90° clockwise in-place.
    Algorithm: Transpose + Reverse each row
    
    Time: O(n²), Space: O(1)
    """
    n = len(matrix)
    
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()

def print_matrix(matrix, name=""):
    if name:
        print(f"{name}:")
    for row in matrix:
        print(f"  {row}")
    print()

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print_matrix(matrix, "Original")
rotate_90_clockwise(matrix)
print_matrix(matrix, "Rotated 90° Clockwise")


print("=" * 60)
print("Transformation 2: Rotate 90° Counter-Clockwise")
print("=" * 60)
print()

def rotate_90_counter_clockwise(matrix: List[List[int]]) -> None:
    """
    Rotate matrix 90° counter-clockwise in-place.
    Algorithm: Reverse each row + Transpose
    
    Time: O(n²), Space: O(1)
    """
    n = len(matrix)
    
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
    
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print_matrix(matrix, "Original")
rotate_90_counter_clockwise(matrix)
print_matrix(matrix, "Rotated 90° Counter-Clockwise")


print("=" * 60)
print("Transformation 3: Rotate 180°")
print("=" * 60)
print()

def rotate_180(matrix: List[List[int]]) -> None:
    """
    Rotate matrix 180° in-place.
    Algorithm: Reverse matrix + Reverse each row
    
    Time: O(n²), Space: O(1)
    """
    matrix.reverse()
    for row in matrix:
        row.reverse()

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print_matrix(matrix, "Original")
rotate_180(matrix)
print_matrix(matrix, "Rotated 180°")


print("=" * 60)
print("Transformation 4: Transpose")
print("=" * 60)
print()

def transpose(matrix: List[List[int]]) -> List[List[int]]:
    """
    Transpose matrix (rows become columns).
    
    Time: O(m*n), Space: O(m*n) for new matrix
    """
    m, n = len(matrix), len(matrix[0])
    return [[matrix[i][j] for i in range(m)] for j in range(n)]

def transpose_in_place(matrix: List[List[int]]) -> None:
    """
    Transpose square matrix in-place.
    
    Time: O(n²), Space: O(1)
    """
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
print_matrix(matrix, "Original (2x3)")
transposed = transpose(matrix)
print_matrix(transposed, "Transposed (3x2)")

square_matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print_matrix(square_matrix, "Square Matrix")
transpose_in_place(square_matrix)
print_matrix(square_matrix, "Transposed In-Place")


print("=" * 60)
print("Transformation 5: Flip Horizontal/Vertical")
print("=" * 60)
print()

def flip_horizontal(matrix: List[List[int]]) -> None:
    """Flip matrix horizontally (mirror left-right)."""
    for row in matrix:
        row.reverse()

def flip_vertical(matrix: List[List[int]]) -> None:
    """Flip matrix vertically (mirror top-bottom)."""
    matrix.reverse()

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print_matrix(matrix, "Original")

matrix_h = [row[:] for row in matrix]
flip_horizontal(matrix_h)
print_matrix(matrix_h, "Flipped Horizontal")

matrix_v = [row[:] for row in matrix]
flip_vertical(matrix_v)
print_matrix(matrix_v, "Flipped Vertical")


print("=" * 60)
print("Transformation 6: Set Matrix Zeroes")
print("=" * 60)
print()

def set_zeroes(matrix: List[List[int]]) -> None:
    """
    Set entire row and column to 0 if element is 0.
    Use first row/column as markers for O(1) space.
    
    Time: O(m*n), Space: O(1)
    """
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # Use first row/column as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # Set zeros based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # Handle first row
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    
    # Handle first column
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0

matrix = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]
print_matrix(matrix, "Original")
set_zeroes(matrix)
print_matrix(matrix, "After Set Zeroes")


print("=" * 60)
print("Transformation 7: Matrix Multiplication")
print("=" * 60)
print()

def multiply_matrices(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Multiply two matrices A (m x n) and B (n x p) = C (m x p).
    
    Time: O(m*n*p), Space: O(m*p)
    """
    m, n = len(A), len(A[0])
    p = len(B[0])
    
    C = [[0] * p for _ in range(m)]
    
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

A = [
    [1, 2],
    [3, 4]
]
B = [
    [5, 6],
    [7, 8]
]
print_matrix(A, "Matrix A (2x2)")
print_matrix(B, "Matrix B (2x2)")
C = multiply_matrices(A, B)
print_matrix(C, "A × B")


print("=" * 60)
print("Transformation 8: Submatrix Sum")
print("=" * 60)
print()

def sum_region(matrix: List[List[int]], r1: int, c1: int, r2: int, c2: int) -> int:
    """
    Sum of rectangle from (r1,c1) to (r2,c2).
    
    Time: O((r2-r1)*(c2-c1)), Space: O(1)
    """
    total = 0
    for i in range(r1, r2 + 1):
        for j in range(c1, c2 + 1):
            total += matrix[i][j]
    return total

matrix = [
    [3, 0, 1, 4, 2],
    [5, 6, 3, 2, 1],
    [1, 2, 0, 1, 5],
    [4, 1, 0, 1, 7],
    [1, 0, 3, 0, 5]
]
print_matrix(matrix, "Matrix")
print(f"Sum of region (2,1) to (4,3): {sum_region(matrix, 2, 1, 4, 3)}")
print()


print("=" * 60)
print("Transformation 9: Prefix Sum (2D)")
print("=" * 60)
print()

class NumMatrix:
    """
    2D prefix sum for efficient range sum queries.
    
    Time: Init O(m*n), Query O(1)
    Space: O(m*n)
    """
    
    def __init__(self, matrix: List[List[int]]):
        if not matrix:
            return
        
        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                self.prefix[i][j] = (matrix[i-1][j-1] + 
                                     self.prefix[i-1][j] + 
                                     self.prefix[i][j-1] - 
                                     self.prefix[i-1][j-1])
    
    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """O(1) range sum query."""
        return (self.prefix[r2+1][c2+1] - 
                self.prefix[r1][c2+1] - 
                self.prefix[r2+1][c1] + 
                self.prefix[r1][c1])

matrix = [
    [3, 0, 1, 4, 2],
    [5, 6, 3, 2, 1],
    [1, 2, 0, 1, 5]
]
print_matrix(matrix, "Matrix")
nm = NumMatrix(matrix)
print("Using 2D Prefix Sum (O(1) queries):")
print(f"  Sum (0,0) to (1,2): {nm.sum_region(0, 0, 1, 2)}")
print(f"  Sum (1,1) to (2,3): {nm.sum_region(1, 1, 2, 3)}")
print()


print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Common Transformations:")
print("  1. Rotate 90° CW: Transpose + Reverse rows")
print("  2. Rotate 90° CCW: Reverse rows + Transpose")
print("  3. Rotate 180°: Reverse matrix + Reverse rows")
print("  4. Transpose: Swap matrix[i][j] with matrix[j][i]")
print("  5. Flip H/V: Reverse rows / Reverse matrix")
print("  6. Set Zeroes: Use first row/col as markers")
print("  7. Multiply: C[i][j] = Σ A[i][k] * B[k][j]")
print("  8. Prefix Sum: O(1) range queries")
print()
print("Space Optimization:")
print("  • Use first row/column as markers")
print("  • In-place transformations for square matrices")
print("  • Prefix sums for multiple queries")
