"""
NeetCode 150 - Graphs
=====================
Graph traversal and algorithms (13 problems).
"""

from collections import deque, defaultdict


# PATTERN: DFS (Grid)
def num_islands(grid):
    """
    Number of Islands - count connected components of 1s.
    
    Pattern: DFS to mark visited cells
    
    Time: O(m * n), Space: O(m * n) for recursion
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # Mark as visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    
    return count


# PATTERN: DFS with Hash Map
def clone_graph(node):
    """
    Clone Graph - deep copy of undirected graph.
    
    Pattern: DFS with hash map (old -> new)
    
    Time: O(V + E), Space: O(V)
    """
    if not node:
        return None
    
    class Node:
        def __init__(self, val=0, neighbors=None):
            self.val = val
            self.neighbors = neighbors if neighbors else []
    
    old_to_new = {}
    
    def dfs(node):
        if node in old_to_new:
            return old_to_new[node]
        
        copy = Node(node.val)
        old_to_new[node] = copy
        
        for neighbor in node.neighbors:
            copy.neighbors.append(dfs(neighbor))
        
        return copy
    
    return dfs(node)


# PATTERN: DFS (Grid)
def max_area_of_island(grid):
    """
    Max Area of Island - largest connected component.
    
    Pattern: DFS with area counting
    
    Time: O(m * n), Space: O(m * n)
    """
    rows, cols = len(grid), len(grid[0])
    max_area = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
    
    return max_area


# PATTERN: Multi-source DFS
def pacific_atlantic(heights):
    """
    Pacific Atlantic Water Flow - cells that reach both oceans.
    
    Pattern: DFS from ocean borders inward
    
    Time: O(m * n), Space: O(m * n)
    """
    rows, cols = len(heights), len(heights[0])
    pacific, atlantic = set(), set()
    
    def dfs(r, c, visited, prev_height):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or heights[r][c] < prev_height):
            return
        
        visited.add((r, c))
        dfs(r + 1, c, visited, heights[r][c])
        dfs(r - 1, c, visited, heights[r][c])
        dfs(r, c + 1, visited, heights[r][c])
        dfs(r, c - 1, visited, heights[r][c])
    
    # DFS from Pacific (top and left)
    for c in range(cols):
        dfs(0, c, pacific, heights[0][c])
        dfs(rows - 1, c, atlantic, heights[rows - 1][c])
    
    for r in range(rows):
        dfs(r, 0, pacific, heights[r][0])
        dfs(r, cols - 1, atlantic, heights[r][cols - 1])
    
    return list(pacific & atlantic)


# PATTERN: DFS (Grid Capture)
def solve(board):
    """
    Surrounded Regions - capture 'O' surrounded by 'X'.
    
    Pattern: Mark border-connected regions, then flip rest
    
    Time: O(m * n), Space: O(m * n)
    """
    if not board:
        return
    
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'T'  # Temporary mark
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    # Mark border-connected 'O's
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)
    
    # Flip remaining 'O's to 'X', restore 'T's to 'O'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'T':
                board[r][c] = 'O'


# PATTERN: Multi-source BFS
def oranges_rotting(grid):
    """
    Rotting Oranges - time for all oranges to rot.
    
    Pattern: BFS from all rotten oranges simultaneously
    
    Time: O(m * n), Space: O(m * n)
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    
    # Find all rotten oranges and count fresh
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    
    if fresh == 0:
        return 0
    
    minutes = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        
        minutes += 1
    
    return minutes - 1 if fresh == 0 else -1


# PATTERN: BFS (Shortest Path)
def walls_and_gates(rooms):
    """
    Walls and Gates - distance from each room to nearest gate.
    
    Pattern: Multi-source BFS from all gates
    
    Time: O(m * n), Space: O(m * n)
    """
    if not rooms:
        return
    
    rows, cols = len(rooms), len(rooms[0])
    queue = deque()
    INF = 2147483647
    
    # Find all gates
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))


# PATTERN: Topological Sort (Cycle Detection)
def can_finish(numCourses, prerequisites):
    """
    Course Schedule - detect cycle in directed graph.
    
    Pattern: DFS cycle detection (white-gray-black)
    
    Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    # 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * numCourses
    
    def has_cycle(course):
        if state[course] == 1:  # Visiting (gray)
            return True
        if state[course] == 2:  # Visited (black)
            return False
        
        state[course] = 1
        for prereq in graph[course]:
            if has_cycle(prereq):
                return True
        state[course] = 2
        
        return False
    
    for course in range(numCourses):
        if has_cycle(course):
            return False
    
    return True


# PATTERN: Topological Sort (DFS)
def find_order(numCourses, prerequisites):
    """
    Course Schedule II - return valid course order.
    
    Pattern: DFS topological sort
    
    Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    state = [0] * numCourses
    order = []
    
    def dfs(course):
        if state[course] == 1:
            return False
        if state[course] == 2:
            return True
        
        state[course] = 1
        for prereq in graph[course]:
            if not dfs(prereq):
                return False
        state[course] = 2
        order.append(course)
        
        return True
    
    for course in range(numCourses):
        if not dfs(course):
            return []
    
    return order


# PATTERN: Union Find (Cycle Detection)
def find_redundant_connection(edges):
    """
    Redundant Connection - find edge that creates cycle.
    
    Pattern: Union-Find
    
    Time: O(E * α(V)), Space: O(V)
    """
    parent = list(range(len(edges) + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        parent[root_x] = root_y
        return True
    
    for u, v in edges:
        if not union(u, v):
            return [u, v]


# PATTERN: Union Find (Connected Components)
def count_components(n, edges):
    """
    Number of Connected Components in Undirected Graph.
    
    Pattern: Union-Find
    
    Time: O(E * α(V)), Space: O(V)
    """
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            parent[root_x] = root_y
            return True
        return False
    
    components = n
    for u, v in edges:
        if union(u, v):
            components -= 1
    
    return components


# PATTERN: Union Find (Cycle Detection)
def valid_tree(n, edges):
    """
    Graph Valid Tree - connected graph with no cycles.
    
    Pattern: Union-Find (n-1 edges, no cycles)
    
    Time: O(E * α(V)), Space: O(V)
    """
    if len(edges) != n - 1:
        return False
    
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return False
        parent[root_u] = root_v
    
    return True


# PATTERN: BFS (Shortest Path)
def ladder_length(beginWord, endWord, wordList):
    """
    Word Ladder - shortest transformation sequence.
    
    Pattern: BFS on word graph
    
    Time: O(M^2 * N) where M = word length, N = wordList size
    Space: O(M^2 * N)
    """
    if endWord not in wordList:
        return 0
    
    wordList = set(wordList)
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    
    while queue:
        word, length = queue.popleft()
        
        if word == endWord:
            return length
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i + 1:]
                if next_word in wordList and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))
    
    return 0


if __name__ == "__main__":
    print("=== NeetCode 150 - Graphs ===\n")
    
    print("Test 1: Number of Islands")
    grid1 = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1']
    ]
    print(f"Islands: {num_islands(grid1)}")
    
    print("\nTest 2: Course Schedule")
    print(f"Can finish [[1,0]]: {can_finish(2, [[1, 0]])}")
    print(f"Can finish [[1,0],[0,1]]: {can_finish(2, [[1, 0], [0, 1]])}")
    
    print("\nTest 3: Course Schedule II")
    print(f"Order for [[1,0],[2,0],[3,1],[3,2]]: {find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])}")
