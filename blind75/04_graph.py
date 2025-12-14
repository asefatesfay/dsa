"""
Blind 75 - Graph Problems
==========================
Essential graph traversal and algorithm problems.
"""

from collections import deque, defaultdict


# 1. Clone Graph
# PATTERN: DFS with Hash Map
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node):
    """
    Deep copy of undirected graph.
    
    Pattern: DFS/BFS with hash map to track clones
    Approach: DFS/BFS with hash map old_node -> new_node
    Steps:
    1. Use hash map to track cloned nodes
    2. For each node, create clone if not exists
    3. Recursively clone all neighbors
    
    Time: O(V+E), Space: O(V)
    """
    if not node:
        return None
    
    clones = {}
    
    def dfs(n):
        if n in clones:
            return clones[n]
        
        clone = Node(n.val)
        clones[n] = clone
        
        for neighbor in n.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)


# 2. Course Schedule
# PATTERN: Cycle Detection / Topological Sort (DFS)
def can_finish(num_courses, prerequisites):
    """
    Check if can finish all courses given prerequisites (detect cycle in DAG).
    
    Pattern: 3-state DFS for cycle detection in directed graph
    Problem: Check if it's possible to finish all courses given prerequisite pairs.
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: True
    Explanation: Take course 0, then course 1
    
    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output: False
    Explanation: Circular dependency - impossible
    
    Approach: Cycle Detection in Directed Graph using DFS
    
    Algorithm Steps:
    1. Build adjacency list from prerequisites
       - For [course, prereq]: course requires prereq to be taken first
       - Graph edge: course -> prereq
    
    2. Use 3 states for each node:
       - 0 (WHITE): Unvisited
       - 1 (GRAY): Currently visiting (in DFS path)
       - 2 (BLACK): Fully visited (all descendants explored)
    
    3. For each unvisited course, run DFS:
       a. Mark as GRAY (visiting)
       b. Visit all prerequisites
       c. If we encounter a GRAY node → CYCLE DETECTED
       d. Mark as BLACK (visited) when done
    
    4. If no cycle found → all courses can be completed
    
    Why this works:
    - A cycle means circular dependency (A needs B, B needs A)
    - GRAY nodes are in current DFS path
    - If we reach a GRAY node again, we've found a cycle
    - This is essentially topological sort cycle detection
    
    Example walkthrough [[1,0],[2,1],[2,0]]:
    Graph: 1→0, 2→1, 2→0
    DFS from 0: mark BLACK ✓
    DFS from 1: visit 0 (BLACK), mark 1 BLACK ✓
    DFS from 2: visit 1 (BLACK), visit 0 (BLACK), mark 2 BLACK ✓
    No cycles found → return True
    
    Time: O(V + E) - visit each vertex and edge once
    Space: O(V + E) - adjacency list and state array
    """
    # STEP 1: Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    # STEP 2: Initialize states (0=unvisited, 1=visiting, 2=visited)
    state = [0] * num_courses
    
    # STEP 3: DFS with cycle detection
    def has_cycle(course):
        if state[course] == 1:  # GRAY - visiting (cycle!)
            return True
        if state[course] == 2:  # BLACK - already processed
            return False
        
        # Mark as visiting (GRAY)
        state[course] = 1
        
        # Visit all prerequisites
        for prereq in graph[course]:
            if has_cycle(prereq):
                return True
        
        # Mark as visited (BLACK)
        state[course] = 2
        return False
    
    # STEP 4: Check all courses
    for course in range(num_courses):
        if has_cycle(course):
            return False
    
    return True


# 3. Pacific Atlantic Water Flow
# PATTERN: Multi-source DFS/BFS
def pacific_atlantic(heights):
    """
    Find cells where water can flow to both Pacific and Atlantic oceans.
    
    Pattern: Multi-source DFS from borders
    Approach: Multi-source DFS/BFS from ocean borders
    Steps:
    1. DFS from Pacific borders (top, left)
    2. DFS from Atlantic borders (bottom, right)
    3. Return intersection of reachable cells
    
    Time: O(m*n), Space: O(m*n)
    """
    if not heights or not heights[0]:
        return []
    
    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    
    def dfs(r, c, ocean):
        ocean.add((r, c))
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n and 
                (nr, nc) not in ocean and 
                heights[nr][nc] >= heights[r][c]):
                dfs(nr, nc, ocean)
    
    # Pacific: top and left borders
    for i in range(m):
        dfs(i, 0, pacific)
    for j in range(n):
        dfs(0, j, pacific)
    
    # Atlantic: bottom and right borders
    for i in range(m):
        dfs(i, n - 1, atlantic)
    for j in range(n):
        dfs(m - 1, j, atlantic)
    
    return list(pacific & atlantic)


# 4. Number of Islands
# PATTERN: DFS/BFS (Connected Components)
def num_islands(grid):
    """
    Count connected components of '1's in grid.
    
    Pattern: DFS/BFS to find connected components
    Approach: DFS/BFS to mark connected regions
    Steps:
    1. For each unvisited '1', start DFS/BFS
    2. Mark all connected '1's as visited
    3. Increment island count
    
    Time: O(m*n), Space: O(m*n)
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
        grid[r][c] = '#'  # Mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    
    return count


# 5. Longest Consecutive Sequence
def longest_consecutive(nums):
    """
    Find length of longest consecutive sequence.
    
    Problem: Find the length of the longest consecutive elements sequence.
    Input: nums = [100,4,200,1,3,2]
    Output: 4
    Explanation: Longest consecutive sequence is [1,2,3,4], length = 4
    
    Approach: Hash Set for O(1) lookup + Smart Iteration
    
    Algorithm Steps:
    1. Put all numbers in a hash set for O(1) lookups
    2. For each number in the set:
       a. Check if it's the START of a sequence
          - Start if (num - 1) is NOT in set
          - This prevents redundant counting
       b. If it's a start, count consecutive numbers:
          - While (num + 1) exists, increment counter
       c. Track maximum length found
    3. Return maximum length
    
    Why this works:
    - Hash set provides O(1) lookup
    - Only start counting from sequence beginnings
    - This ensures each number is visited at most twice:
      * Once when checking if it's a start
      * Once when it's part of a sequence
    - Skipping non-starts prevents redundant work
    
    Example walkthrough [100,4,200,1,3,2]:
    Set: {100, 4, 200, 1, 3, 2}
    
    num=100: 99 not in set → START
      - Check 101, 102... not found
      - Sequence length: 1
    
    num=4: 3 in set → NOT START (skip)
    
    num=200: 199 not in set → START
      - Check 201, 202... not found
      - Sequence length: 1
    
    num=1: 0 not in set → START
      - Check 2 ✓, 3 ✓, 4 ✓, 5 ✗
      - Sequence [1,2,3,4] length: 4 ← maximum!
    
    Time: O(n) - each number visited at most twice
    Space: O(n) - hash set storage
    """
    if not nums:
        return 0
    
    # STEP 1: Create hash set for O(1) lookups
    num_set = set(nums)
    max_length = 0
    
    # STEP 2: Check each number
    for num in num_set:
        # STEP 3: Only start counting if this is sequence beginning
        if num - 1 not in num_set:  # Is this a start?
            current = num
            length = 1
            
            # STEP 4: Count consecutive numbers
            while current + 1 in num_set:
                current += 1
                length += 1
            
            # STEP 5: Update maximum
            max_length = max(max_length, length)
    
    return max_length


# 6. Graph Valid Tree
# PATTERN: Union Find / DFS Cycle Detection
def valid_tree(n, edges):
    """
    Check if undirected graph forms valid tree.
    
    Pattern: Union Find or DFS with cycle detection
    Tree conditions:
    1. n nodes and n-1 edges
    2. All nodes connected (no separate components)
    3. No cycles
    
    Approach: Union-Find or DFS
    Steps (DFS):
    1. Check edge count == n-1
    2. DFS to verify all nodes reachable and no cycles
    
    Time: O(V+E), Space: O(V+E)
    """
    if len(edges) != n - 1:
        return False
    
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                return False  # Cycle detected
            if not dfs(neighbor, node):
                return False
        return True
    
    # Check if all nodes are reachable and no cycle
    return dfs(0, -1) and len(visited) == n


if __name__ == "__main__":
    print("=" * 60)
    print("BLIND 75 - GRAPH PROBLEMS")
    print("=" * 60)
    print()
    
    # Clone Graph - skipping demo (needs graph construction)
    print("1. CLONE GRAPH")
    print("-" * 60)
    print("Implementation: Deep copy with DFS and hash map")
    print("Status: ✓ Complete (requires Node class instantiation for demo)")
    print()
    
    # Course Schedule
    print("2. COURSE SCHEDULE (Cycle Detection)")
    print("-" * 60)
    print("Example 1:")
    prereqs1 = [[1, 0]]
    print(f"Input: numCourses = 2, prerequisites = {prereqs1}")
    print(f"Output: {can_finish(2, prereqs1)}")
    print("Explanation: Take course 0 first, then course 1")
    print()
    print("Example 2:")
    prereqs2 = [[1, 0], [0, 1]]
    print(f"Input: numCourses = 2, prerequisites = {prereqs2}")
    print(f"Output: {can_finish(2, prereqs2)}")
    print("Explanation: Circular dependency detected - impossible")
    print()
    
    # Pacific Atlantic - complex output
    print("3. PACIFIC ATLANTIC WATER FLOW")
    print("-" * 60)
    heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    result = pacific_atlantic(heights)
    print(f"Input: heights = 5x5 matrix")
    print(f"Output: {len(result)} cells can flow to both oceans")
    print("Explanation: Multi-source DFS from borders")
    print()
    
    # Number of Islands
    print("4. NUMBER OF ISLANDS")
    print("-" * 60)
    grid = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1']
    ]
    print("Input: 4x5 grid with '1's (land) and '0's (water)")
    print(f"Output: {num_islands(grid)} islands")
    print("Explanation: Count connected components of '1's")
    print()
    
    # Longest Consecutive Sequence
    print("5. LONGEST CONSECUTIVE SEQUENCE")
    print("-" * 60)
    nums = [100, 4, 200, 1, 3, 2]
    print(f"Input: nums = {nums}")
    print(f"Output: {longest_consecutive(nums)}")
    print("Explanation: Longest sequence is [1,2,3,4] with length 4")
    print()
    
    # Graph Valid Tree
    print("6. GRAPH VALID TREE")
    print("-" * 60)
    print("Example 1:")
    edges1 = [[0, 1], [0, 2], [0, 3], [1, 4]]
    print(f"Input: n = 5, edges = {edges1}")
    print(f"Output: {valid_tree(5, edges1)}")
    print("Explanation: Connected acyclic graph with n-1 edges")
    print()
    print("Example 2:")
    edges2 = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
    print(f"Input: n = 5, edges = {edges2}")
    print(f"Output: {valid_tree(5, edges2)}")
    print("Explanation: Has cycle (1-2-3-1), not a valid tree")
    print()
    print("=" * 60)
