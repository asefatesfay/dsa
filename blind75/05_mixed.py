"""
Blind 75 - String, Interval, Linked List, Matrix, Tree, Heap Problems
=======================================================================
Remaining categories from Blind 75.
"""

from collections import Counter, defaultdict, deque
import heapq


# ============================================
# STRING PROBLEMS
# ============================================

# PATTERN: Sliding Window
def length_of_longest_substring(s):
    """
    Longest substring without repeating characters.
    
    Pattern: Sliding window with hash map
    Approach: Sliding window with hash map
    Time: O(n), Space: O(min(n, alphabet_size))
    """
    char_index = {}
    max_len = start = 0
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = end
        max_len = max(max_len, end - start + 1)
    
    return max_len


# PATTERN: Hash Map
def is_anagram(s, t):
    """Check if two strings are anagrams.
    
    Pattern: Hash Map / Frequency Counter
    """
    return Counter(s) == Counter(t)


# PATTERN: Hash Map (Sorted Key)
def group_anagrams(strs):
    """Group anagrams together.
    
    Pattern: Hash map with sorted string as key
    """
    anagram_map = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    return list(anagram_map.values())


# PATTERN: Stack
def is_valid_parentheses(s):
    """Check if parentheses are valid.
    
    Pattern: Stack for matching pairs
    """
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    for char in s:
        if char in pairs:
            stack.append(char)
        elif not stack or pairs[stack.pop()] != char:
            return False
    return not stack


# PATTERN: Two Pointers
def is_palindrome(s):
    """Check if string is valid palindrome (alphanumeric only)."""
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# ============================================
# INTERVAL PROBLEMS
# ============================================

# PATTERN: Sort + Merge
def merge_intervals(intervals):
    """
    Merge overlapping intervals.
    
    Pattern: Sort by start, then merge overlapping
    Approach: Sort by start, then merge
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged


# PATTERN: Interval Merging
def insert_interval(intervals, new_interval):
    """
    Insert new interval and merge if needed.
    
    Pattern: Three-phase insertion (before, merge, after)
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result


# ============================================
# LINKED LIST PROBLEMS
# ============================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# PATTERN: In-place Reversal
def reverse_list(head):
    """Reverse linked list iteratively.
    
    Pattern: Three-pointer in-place reversal
    """
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev


# PATTERN: Fast and Slow Pointers (Floyd's Cycle Detection)
def has_cycle(head):
    """Detect cycle using fast/slow pointers.
    
    Pattern: Floyd's cycle detection (tortoise and hare)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


# PATTERN: Two Pointers (Merge)
def merge_two_lists(l1, l2):
    """Merge two sorted lists.
    
    Pattern: Two-pointer merge with dummy node
    """
    dummy = ListNode()
    curr = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    curr.next = l1 or l2
    return dummy.next


# ============================================
# MATRIX PROBLEMS
# ============================================

# PATTERN: In-place Modification
def set_zeroes(matrix):
    """
    Set entire row and column to 0 if element is 0.
    
    Pattern: Use first row/col as markers for O(1) space
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
    
    # Set zeros based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # Handle first row and col
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0


# PATTERN: Layer-by-Layer Traversal
def spiral_order(matrix):
    """Return matrix elements in spiral order.
    
    Pattern: Process outer layer, shrink boundaries
    """
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Right
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        # Down
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        if top <= bottom:
            # Left
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        if left <= right:
            # Up
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result


# ============================================
# TREE PROBLEMS
# ============================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# PATTERN: DFS (Recursion)
def max_depth(root):
    """Maximum depth of binary tree.
    
    Pattern: Recursive DFS
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# PATTERN: DFS (Recursion)
def is_same_tree(p, q):
    """Check if two trees are identical.
    
    Pattern: Recursive pre-order traversal
    """
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


# PATTERN: DFS (Recursion)
def invert_tree(root):
    """Invert binary tree.
    
    Pattern: Recursive DFS with swap
    """
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# ============================================
# HEAP PROBLEMS
# ============================================

# PATTERN: Heap (Min Heap)
def top_k_frequent(nums, k):
    """
    Find k most frequent elements.
    
    Pattern: Min heap of size k or bucket sort
    Approach: Counter + heap or bucket sort
    Time: O(n log k), Space: O(n)
    """
    count = Counter(nums)
    return [item for item, freq in count.most_common(k)]


# PATTERN: Two Heaps (Max Heap + Min Heap)
class MedianFinder:
    """Find median from data stream using two heaps.
    
    Pattern: Two heaps (max heap for small half, min heap for large half)
    """
    
    def __init__(self):
        self.small = []  # Max heap (negated)
        self.large = []  # Min heap
    
    def addNum(self, num):
        heapq.heappush(self.small, -num)
        
        # Balance: ensure small's max <= large's min
        if self.small and self.large and -self.small[0] > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0


if __name__ == "__main__":
    print("=== Blind 75 Additional Problems ===\n")
    
    # String
    print("Longest Substring('abcabcbb'):", length_of_longest_substring('abcabcbb'))
    print("Is Anagram('anagram', 'nagaram'):", is_anagram('anagram', 'nagaram'))
    print("Valid Parentheses('()[]{}'):", is_valid_parentheses('()[]{}'))
    print("Valid Palindrome('A man, a plan, a canal: Panama'):", is_palindrome('A man, a plan, a canal: Panama'))
    
    # Interval
    print("\nMerge Intervals([[1,3],[2,6],[8,10],[15,18]]):", merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))
    
    # Heap
    print("\nTop K Frequent([1,1,1,2,2,3], 2):", top_k_frequent([1, 1, 1, 2, 2, 3], 2))
    
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    print("Median after [1,2]:", mf.findMedian())
    mf.addNum(3)
    print("Median after [1,2,3]:", mf.findMedian())
