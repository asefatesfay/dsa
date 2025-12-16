"""
NeetCode 150 - Backtracking
============================
Explore all possible solutions (9 problems).
"""


# PATTERN: Backtracking (Decision Tree)
def subsets(nums):
    """
    Subsets - all possible subsets.
    
    Pattern: Decision tree (include/exclude each element)
    
    Time: O(2^n), Space: O(n) for recursion
    """
    result = []
    
    def backtrack(index, current):
        if index == len(nums):
            result.append(current[:])
            return
        
        # Include nums[index]
        current.append(nums[index])
        backtrack(index + 1, current)
        current.pop()
        
        # Exclude nums[index]
        backtrack(index + 1, current)
    
    backtrack(0, [])
    return result


# PATTERN: Backtracking with Pruning
def combination_sum(candidates, target):
    """
    Combination Sum - combinations that sum to target (can reuse elements).
    
    Pattern: Backtracking with remaining sum tracking
    
    Time: O(2^target), Space: O(target)
    """
    result = []
    
    def backtrack(index, current, total):
        if total == target:
            result.append(current[:])
            return
        if total > target or index == len(candidates):
            return
        
        # Include candidates[index] (can reuse)
        current.append(candidates[index])
        backtrack(index, current, total + candidates[index])
        current.pop()
        
        # Skip candidates[index]
        backtrack(index + 1, current, total)
    
    backtrack(0, [], 0)
    return result


# PATTERN: Backtracking with Swapping
def permute(nums):
    """
    Permutations - all possible arrangements.
    
    Pattern: Backtracking with swapping
    
    Time: O(n! * n), Space: O(n)
    """
    result = []
    
    def backtrack(index):
        if index == len(nums):
            result.append(nums[:])
            return
        
        for i in range(index, len(nums)):
            nums[index], nums[i] = nums[i], nums[index]
            backtrack(index + 1)
            nums[index], nums[i] = nums[i], nums[index]  # Backtrack
    
    backtrack(0)
    return result


# PATTERN: Backtracking with Duplicate Handling
def subsets_with_dup(nums):
    """
    Subsets II - subsets with duplicate elements (no duplicate subsets).
    
    Pattern: Sort + skip duplicates at same level
    
    Time: O(2^n), Space: O(n)
    """
    nums.sort()
    result = []
    
    def backtrack(index, current):
        result.append(current[:])
        
        for i in range(index, len(nums)):
            # Skip duplicates at same recursion level
            if i > index and nums[i] == nums[i - 1]:
                continue
            
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result


# PATTERN: Backtracking with Duplicate Handling
def combination_sum2(candidates, target):
    """
    Combination Sum II - combinations that sum to target (each element used once).
    
    Pattern: Sort + skip duplicates + no reuse
    
    Time: O(2^n), Space: O(n)
    """
    candidates.sort()
    result = []
    
    def backtrack(index, current, total):
        if total == target:
            result.append(current[:])
            return
        if total > target:
            return
        
        for i in range(index, len(candidates)):
            if i > index and candidates[i] == candidates[i - 1]:
                continue
            
            current.append(candidates[i])
            backtrack(i + 1, current, total + candidates[i])
            current.pop()
    
    backtrack(0, [], 0)
    return result


# PATTERN: Backtracking on 2D Grid
def exist(board, word):
    """
    Word Search - find word in 2D board.
    
    Pattern: DFS backtracking with visited marking
    
    Time: O(m * n * 4^L) where L = word length
    Space: O(L) for recursion
    """
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c, index):
        if index == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[index]:
            return False
        
        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'
        
        # Try all 4 directions
        found = (dfs(r + 1, c, index + 1) or
                 dfs(r - 1, c, index + 1) or
                 dfs(r, c + 1, index + 1) or
                 dfs(r, c - 1, index + 1))
        
        # Backtrack
        board[r][c] = temp
        
        return found
    
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    
    return False


# PATTERN: Backtracking with Validation
def partition(s):
    """
    Palindrome Partitioning - all ways to partition into palindromes.
    
    Pattern: Backtracking with substring validation
    
    Time: O(n * 2^n), Space: O(n)
    """
    result = []
    
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    def backtrack(index, current):
        if index == len(s):
            result.append(current[:])
            return
        
        for i in range(index, len(s)):
            substring = s[index:i + 1]
            if is_palindrome(substring):
                current.append(substring)
                backtrack(i + 1, current)
                current.pop()
    
    backtrack(0, [])
    return result


# PATTERN: Backtracking with Mapping
def letter_combinations(digits):
    """
    Letter Combinations of a Phone Number.
    
    Pattern: Backtracking with digit-to-letter mapping
    
    Time: O(4^n), Space: O(n)
    """
    if not digits:
        return []
    
    mapping = {
        '2': 'abc', '3': 'def', '4': 'ghi',
        '5': 'jkl', '6': 'mno', '7': 'pqrs',
        '8': 'tuv', '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current):
        if index == len(digits):
            result.append(''.join(current))
            return
        
        for letter in mapping[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result


# PATTERN: Backtracking with Constraints
def solve_n_queens(n):
    """
    N-Queens - place N queens on N×N board.
    
    Pattern: Backtracking with conflict checking
    
    Algorithm Steps:
    1. Place one queen per row
    2. Check column and diagonal conflicts
    3. Track used columns and diagonals with sets
    
    Time: O(n!), Space: O(n^2)
    """
    result = []
    cols = set()
    pos_diag = set()  # r + c
    neg_diag = set()  # r - c
    
    board = [['.'] * n for _ in range(n)]
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            
            # Place queen
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = 'Q'
            
            backtrack(row + 1)
            
            # Backtrack
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)
            board[row][col] = '.'
    
    backtrack(0)
    return result


if __name__ == "__main__":
    print("=== NeetCode 150 - Backtracking ===\n")
    
    print("Test 1: Subsets")
    print(f"Subsets of [1,2,3]: {subsets([1, 2, 3])}")
    
    print("\nTest 2: Combination Sum")
    print(f"Combinations summing to 7 from [2,3,6,7]: {combination_sum([2, 3, 6, 7], 7)}")
    
    print("\nTest 3: Permutations")
    print(f"Permutations of [1,2,3]: {permute([1, 2, 3])}")
    
    print("\nTest 4: Subsets with Duplicates")
    print(f"Subsets of [1,2,2]: {subsets_with_dup([1, 2, 2])}")
    
    print("\nTest 5: Word Search")
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    print(f"Board contains 'ABCCED': {exist(board, 'ABCCED')}")
    print(f"Board contains 'SEE': {exist(board, 'SEE')}")
    
    print("\nTest 6: Palindrome Partitioning")
    print(f"Palindrome partitions of 'aab': {partition('aab')}")
    
    print("\nTest 7: Letter Combinations")
    print(f"Letter combinations of '23': {letter_combinations('23')}")
    
    print("\nTest 8: N-Queens (n=4)")
    solutions = solve_n_queens(4)
    print(f"Number of solutions: {len(solutions)}")
    print("First solution:")
    for row in solutions[0]:
        print(row)
