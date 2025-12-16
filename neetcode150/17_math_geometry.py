"""
NeetCode 150 - Math & Geometry
===============================
Mathematical and geometric problems (8 problems).
"""

import math


# PATTERN: Simulation
def rotate(matrix):
    """
    Rotate Image - rotate matrix 90 degrees clockwise in-place.
    
    Pattern: Transpose + reverse rows
    
    Time: O(n^2), Space: O(1)
    """
    n = len(matrix)
    
    # Transpose
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()


# PATTERN: Matrix Traversal
def spiral_order(matrix):
    """
    Spiral Matrix - return elements in spiral order.
    
    Pattern: Four-pointer boundary tracking
    
    Time: O(m * n), Space: O(1)
    """
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
        
        if top <= bottom:
            # Left
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        if left <= right:
            # Up
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result


# PATTERN: Matrix State Update
def set_zeroes(matrix):
    """
    Set Matrix Zeroes - set row and column to 0 if element is 0.
    
    Pattern: Use first row/col as markers
    
    Time: O(m * n), Space: O(1)
    """
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = False
    
    # Use first row and col as markers
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 0:
                matrix[0][c] = 0
                if r == 0:
                    first_row_zero = True
                else:
                    matrix[r][0] = 0
    
    # Set zeros based on markers (skip first row/col)
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[0][c] == 0 or matrix[r][0] == 0:
                matrix[r][c] = 0
    
    # Handle first column
    if matrix[0][0] == 0:
        for r in range(rows):
            matrix[r][0] = 0
    
    # Handle first row
    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0


# PATTERN: Happy Number Detection
def is_happy(n):
    """
    Happy Number - repeatedly replace with sum of squares of digits.
    
    Pattern: Cycle detection with set
    
    Time: O(log n), Space: O(log n)
    """
    seen = set()
    
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    
    return n == 1


# PATTERN: String Addition
def plus_one(digits):
    """
    Plus One - increment integer represented as array.
    
    Pattern: Carry propagation
    
    Time: O(n), Space: O(1)
    """
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    
    return [1] + digits


# PATTERN: Math (Exponentiation)
def my_pow(x, n):
    """
    Pow(x, n) - calculate x raised to power n.
    
    Pattern: Fast exponentiation (divide and conquer)
    
    Time: O(log n), Space: O(log n)
    """
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n
    
    def helper(x, n):
        if n == 0:
            return 1
        
        half = helper(x, n // 2)
        
        if n % 2 == 0:
            return half * half
        else:
            return half * half * x
    
    return helper(x, n)


# PATTERN: String Multiplication
def multiply(num1, num2):
    """
    Multiply Strings - multiply two non-negative integers as strings.
    
    Pattern: Elementary multiplication with position tracking
    
    Time: O(m * n), Space: O(m + n)
    """
    if num1 == "0" or num2 == "0":
        return "0"
    
    m, n = len(num1), len(num2)
    result = [0] * (m + n)
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            digit1 = int(num1[i])
            digit2 = int(num2[j])
            
            mul = digit1 * digit2
            pos1 = i + j
            pos2 = i + j + 1
            
            sum_val = mul + result[pos2]
            result[pos2] = sum_val % 10
            result[pos1] += sum_val // 10
    
    # Skip leading zeros
    start = 0
    while start < len(result) and result[start] == 0:
        start += 1
    
    return ''.join(map(str, result[start:]))


# PATTERN: Geometry
def detect_squares(self):
    """
    Detect Squares - count axis-aligned squares with 3 other points.
    
    Pattern: Hash map of point counts
    
    This is a class-based problem. See implementation below.
    """
    pass


class DetectSquares:
    """
    Detect Squares - count axis-aligned squares.
    
    Pattern: Hash map (x, y) -> count
    
    Operations:
    - add: O(1)
    - count: O(n) where n = points with same x-coordinate
    """
    
    def __init__(self):
        from collections import defaultdict
        self.points = defaultdict(int)
    
    def add(self, point):
        """Add a point."""
        self.points[tuple(point)] += 1
    
    def count(self, point):
        """
        Count squares where point is one corner.
        
        Algorithm Steps:
        1. Fix point as one corner
        2. For each other point with same x-coordinate
        3. Calculate side length
        4. Check if two other corners exist
        """
        x1, y1 = point
        total = 0
        
        for (x2, y2), count2 in self.points.items():
            if x1 == x2 or abs(x1 - x2) != abs(y1 - y2):
                continue
            
            # Potential diagonal point
            side = abs(x1 - x2)
            
            # Check other two corners
            count3 = self.points[(x1, y2)]
            count4 = self.points[(x2, y1)]
            
            total += count2 * count3 * count4
        
        return total


if __name__ == "__main__":
    print("=== NeetCode 150 - Math & Geometry ===\n")
    
    print("Test 1: Rotate Image")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"Before: {matrix}")
    rotate(matrix)
    print(f"After 90° rotation: {matrix}")
    
    print("\nTest 2: Spiral Matrix")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"Spiral order: {spiral_order(matrix)}")
    
    print("\nTest 3: Set Matrix Zeroes")
    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    print(f"Before: {matrix}")
    set_zeroes(matrix)
    print(f"After: {matrix}")
    
    print("\nTest 4: Happy Number")
    print(f"Is 19 happy: {is_happy(19)}")
    print(f"Is 2 happy: {is_happy(2)}")
    
    print("\nTest 5: Plus One")
    print(f"[1,2,3] + 1 = {plus_one([1, 2, 3])}")
    print(f"[9,9,9] + 1 = {plus_one([9, 9, 9])}")
    
    print("\nTest 6: Power")
    print(f"2^10 = {my_pow(2, 10)}")
    print(f"2^-2 = {my_pow(2, -2)}")
    
    print("\nTest 7: Multiply Strings")
    print(f"'123' * '456' = {multiply('123', '456')}")
    
    print("\nTest 8: Detect Squares")
    ds = DetectSquares()
    ds.add([3, 10])
    ds.add([11, 2])
    ds.add([3, 2])
    print(f"Count squares with [11, 10]: {ds.count([11, 10])}")
    ds.add([11, 10])
    print(f"Count after adding [11, 10]: {ds.count([11, 10])}")
