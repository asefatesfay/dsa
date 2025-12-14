# Blind 75 LeetCode Problems

A curated collection of 75 essential LeetCode problems for mastering technical interviews. These problems cover the most important patterns and data structures asked in FAANG and top tech company interviews.

## Why Blind 75?

This list was curated by a Facebook engineer and has become the gold standard for interview preparation. It focuses on:
- **High-frequency problems** asked in real interviews
- **Core patterns** that appear repeatedly across different problems
- **Optimal time complexity** solutions with detailed explanations
- **Comprehensive coverage** of data structures and algorithms

## How to Use This Repository

1. **Start with a category** that matches your current focus area
2. **Read the problem description** and attempt to solve it yourself first
3. **Study the solution** with step-by-step comments explaining the algorithm
4. **Run the examples** to verify your understanding
5. **Practice variations** and edge cases

## Problem Categories

### Array (10 problems)
**Master essential array manipulation techniques and two-pointer patterns**

1. **Two Sum** - Hash map for O(n) complement search
2. **Best Time to Buy and Sell Stock** - Single pass tracking min/max
3. **Contains Duplicate** - Set-based duplicate detection
4. **Product of Array Except Self** - Prefix/suffix products without division
5. **Maximum Subarray** - Kadane's algorithm for optimal subarray sum
6. **Maximum Product Subarray** - Track both max and min products (handle negatives)
7. **Find Minimum in Rotated Sorted Array** - Binary search in rotated array
8. **Search in Rotated Sorted Array** - Modified binary search with pivot
9. **3Sum** - Two pointers with sorted array for triplet finding
10. **Container With Most Water** - Two pointers for area maximization

### Binary (5 problems)
**Understand bit manipulation and mathematical tricks**

1. **Sum of Two Integers** - Bitwise addition using XOR and AND
2. **Number of 1 Bits** - Hamming weight with n & (n-1) optimization
3. **Counting Bits** - DP pattern: dp[i] = dp[i & (i-1)] + 1
4. **Missing Number** - XOR all elements and indices
5. **Reverse Bits** - Build reversed number bit by bit

### Dynamic Programming (11 problems)
**Learn classical DP patterns: Fibonacci, knapsack, subsequences**

1. **Climbing Stairs** - Fibonacci pattern (ways to reach step n)
2. **Coin Change** - Unbounded knapsack (min coins for amount)
3. **Longest Increasing Subsequence** - O(n²) DP or O(n log n) binary search
4. **Longest Common Subsequence** - 2D DP for string matching
5. **Word Break** - DP with dictionary lookup
6. **Combination Sum IV** - Permutation-counting unbounded knapsack
7. **House Robber** - DP with non-adjacent constraint
8. **House Robber II** - Circular array variation
9. **Decode Ways** - String decoding with 1-digit/2-digit choices
10. **Unique Paths** - Grid path counting with combinatorics
11. **Jump Game** - Greedy approach tracking max reachable index

### Graph (6 problems)
**Master DFS, BFS, cycle detection, and topological sort**

1. **Clone Graph** - Deep copy with hash map tracking
2. **Course Schedule** - Cycle detection in directed graph (topological sort)
3. **Pacific Atlantic Water Flow** - Multi-source DFS from borders
4. **Number of Islands** - Connected components via DFS/BFS
5. **Longest Consecutive Sequence** - Hash set for O(n) sequence finding
6. **Graph Valid Tree** - Verify connected acyclic graph (n-1 edges)

### Interval (2 problems)
**Handle interval merging and insertion**

1. **Insert Interval** - Three-phase interval insertion with merging
2. **Merge Intervals** - Sort and merge overlapping intervals

### Linked List (6 problems)
**In-place manipulation with fast/slow pointers**

1. **Reverse Linked List** - Iterative pointer reversal
2. **Detect Cycle in Linked List** - Floyd's cycle detection (fast/slow)
3. **Merge Two Sorted Lists** - Two-pointer merge
4. **Merge K Sorted Lists** - Heap-based merging of multiple lists
5. **Remove Nth Node From End of List** - Two-pointer with gap
6. **Reorder List** - Find middle + reverse + interleave

### Matrix (2 problems)
**2D array traversal patterns**

1. **Set Matrix Zeroes** - In-place marking with first row/col
2. **Spiral Matrix** - Layer-by-layer boundary traversal

### String (9 problems)
**Sliding window, two pointers, and pattern matching**

1. **Longest Substring Without Repeating Characters** - Sliding window with hash map
2. **Longest Repeating Character Replacement** - Sliding window with character frequency
3. **Minimum Window Substring** - Template for substring problems
4. **Valid Anagram** - Character frequency comparison
5. **Group Anagrams** - Hash map with sorted string keys
6. **Valid Parentheses** - Stack-based matching
7. **Valid Palindrome** - Two pointers ignoring non-alphanumeric
8. **Longest Palindromic Substring** - Expand around center
9. **Palindromic Substrings** - Count palindromes with expansion

### Tree (15 problems)
**Binary tree traversal, BST properties, and recursion**

1. **Maximum Depth of Binary Tree** - Recursive depth calculation
2. **Same Tree** - Recursive structure and value comparison
3. **Invert Binary Tree** - Swap left/right children recursively
4. **Binary Tree Maximum Path Sum** - Post-order with global max
5. **Binary Tree Level Order Traversal** - BFS with queue
6. **Serialize and Deserialize Binary Tree** - Tree encoding/decoding
7. **Subtree of Another Tree** - Recursive subtree matching
8. **Construct Binary Tree from Preorder and Inorder** - Recursive construction
9. **Validate Binary Search Tree** - In-order traversal or range checking
10. **Kth Smallest Element in BST** - In-order traversal
11. **Lowest Common Ancestor of BST** - BST property exploitation
12. **Implement Trie (Prefix Tree)** - Prefix tree for word storage
13. **Add and Search Word** - Trie with wildcard DFS
14. **Word Search II** - Trie + backtracking on board
15. **Maximum Depth of N-ary Tree** - Generalized depth calculation

### Heap (3 problems)
**Priority queue patterns**

1. **Merge K Sorted Lists** - Min heap for efficient merging
2. **Top K Frequent Elements** - Heap or bucket sort
3. **Find Median from Data Stream** - Two heaps (max heap + min heap)

---

## File Organization

- **01_array.py** - All 10 array problems with optimized solutions
- **02_binary.py** - Bit manipulation techniques and tricks
- **03_dynamic_programming.py** - Classical DP patterns and optimizations
- **04_graph.py** - Graph traversal, cycle detection, and topological sort
- **05_mixed.py** - String, Interval, Linked List, Matrix, Tree, and Heap problems

Each file contains:
- ✅ **Problem statements** in docstrings
- ✅ **Step-by-step algorithm explanations** with comments
- ✅ **Approach and intuition** for solving each problem
- ✅ **Time and space complexity** analysis
- ✅ **Working examples** with input/output demonstrations
- ✅ **Edge cases** handled in implementations

## Study Tips

### For Beginners
1. Start with **Array** and **String** problems
2. Master **two-pointers** and **sliding window** patterns
3. Move to **Linked List** and **Tree** traversals
4. Build up to **Graph** and **DP** problems

### For Interview Prep
1. **Time yourself** - aim for 25-35 minutes per problem
2. **Code without IDE** first, then verify
3. **Explain out loud** as if in an interview
4. **Analyze complexity** before and after coding
5. **Practice follow-up questions** and variations

### Common Patterns to Master
- **Two Pointers**: Array, String problems
- **Sliding Window**: Substring problems
- **Fast & Slow Pointers**: Linked List cycles
- **DFS/BFS**: Graph and Tree traversal
- **Binary Search**: Sorted array problems
- **DP**: Optimization and counting problems
- **Heap**: Top K and streaming problems
- **Backtracking**: Combinatorial problems

## Practice Schedule

**Week 1-2**: Array, String, Two Pointers (warm-up fundamentals)  
**Week 3**: Linked List, Binary, Matrix (pointer manipulation)  
**Week 4-5**: Tree, Graph (recursion and traversal)  
**Week 6-7**: Dynamic Programming (pattern recognition)  
**Week 8**: Heap, Interval, Review (advanced topics)

---
