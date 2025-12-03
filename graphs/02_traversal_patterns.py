"""
Graph Traversal - BFS and DFS Patterns
=======================================
Common graph traversal patterns and their applications.
"""

from collections import deque, defaultdict
from typing import List, Set, Dict


print("=" * 60)
print("Graph Traversal Overview")
print("=" * 60)
print()
print("Two main traversal methods:")
print()
print("1. BFS (Breadth-First Search):")
print("   • Explores level by level")
print("   • Uses Queue (FIFO)")
print("   • Finds shortest path in unweighted graphs")
print("   • Good for: nearest neighbor, shortest path")
print()
print("2. DFS (Depth-First Search):")
print("   • Explores as deep as possible first")
print("   • Uses Stack (or recursion)")
print("   • Good for: cycle detection, pathfinding, topological sort")
print()


class Graph:
    """Graph using adjacency list"""
    
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)
    
    def get_vertices(self):
        return list(self.graph.keys())


# Pattern 1: BFS Traversal
print("=" * 60)
print("Pattern 1: BFS (Breadth-First Search)")
print("=" * 60)
print()
print("How BFS works:")
print("1. Start from source node, mark as visited")
print("2. Add to queue")
print("3. While queue not empty:")
print("   a. Dequeue node")
print("   b. Process node")
print("   c. Enqueue all unvisited neighbors")
print()
print("Visual Example:")
print()
print("     1 ---- 2")
print("     |      |")
print("     3 ---- 4")
print()
print("BFS from 1: 1 → 2, 3 → 4")
print("(Level 0: 1, Level 1: 2,3, Level 2: 4)")
print()


def bfs(graph, start):
    """
    Basic BFS traversal.
    
    Time: O(V + E)
    Space: O(V) for queue and visited set
    """
    # STEP 1: Initialize visited set to track explored nodes
    # Using set for O(1) lookup to avoid revisiting nodes
    visited = set()
    
    # STEP 2: Initialize queue with starting node
    # Queue ensures FIFO order - processes nodes level by level
    queue = deque([start])
    
    # STEP 3: Mark start as visited immediately (before processing)
    # This prevents adding it to queue multiple times
    visited.add(start)
    
    # STEP 4: Track result in order of visit
    result = []
    
    # STEP 5: Process nodes until queue is empty
    while queue:
        # STEP 6: Remove node from front of queue (FIFO)
        node = queue.popleft()
        
        # STEP 7: Process current node
        result.append(node)
        
        # STEP 8: Explore all neighbors of current node
        for neighbor in graph.graph[node]:
            # STEP 9: Only process unvisited neighbors
            if neighbor not in visited:
                # STEP 10: Mark as visited and add to queue
                # IMPORTANT: Mark as visited NOW (not when dequeued)
                # This prevents adding same node multiple times
                visited.add(neighbor)
                queue.append(neighbor)
    
    # STEP 11: Return nodes in BFS order
    return result


def bfs_with_levels(graph, start):
    """
    BFS tracking levels (distance from start).
    
    Returns: List of (node, level) tuples
    Time: O(V + E)
    """
    visited = set()
    queue = deque([(start, 0)])
    visited.add(start)
    result = []
    
    while queue:
        node, level = queue.popleft()
        result.append((node, level))
        
        for neighbor in graph.graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
    
    return result


# Demo BFS
g = Graph()
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)
g.add_edge(3, 4)

print("Graph edges: (1,2), (1,3), (2,4), (3,4)")
print(f"BFS from 1: {bfs(g, 1)}")
print(f"BFS with levels: {bfs_with_levels(g, 1)}")
print()


# Pattern 2: DFS Traversal
print("=" * 60)
print("Pattern 2: DFS (Depth-First Search)")
print("=" * 60)
print()
print("How DFS works:")
print("1. Start from source, mark visited")
print("2. Recursively visit unvisited neighbors")
print("3. Backtrack when no unvisited neighbors")
print()
print("Visual Example:")
print()
print("     1 ---- 2")
print("     |      |")
print("     3 ---- 4")
print()
print("DFS from 1: 1 → 2 → 4 → 3")
print("(Goes deep first: 1→2→4, then backtracks to 3)")
print()


def dfs_recursive(graph, start, visited=None):
    """
    DFS using recursion.
    
    Time: O(V + E)
    Space: O(V) for recursion stack
    """
    # STEP 1: Initialize visited set on first call
    # visited is shared across all recursive calls
    if visited is None:
        visited = set()
    
    # STEP 2: Mark current node as visited
    # Do this BEFORE exploring neighbors to avoid infinite loops
    visited.add(start)
    
    # STEP 3: Add current node to result
    result = [start]
    
    # STEP 4: Recursively explore each unvisited neighbor
    for neighbor in graph.graph[start]:
        # STEP 5: Check if neighbor has been visited
        if neighbor not in visited:
            # STEP 6: Recursively DFS from neighbor
            # Goes DEEP before exploring other neighbors at this level
            # This is the key difference from BFS!
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    # STEP 7: Return path including this node and all descendants
    return result


def dfs_iterative(graph, start):
    """
    DFS using explicit stack.
    
    Time: O(V + E)
    Space: O(V)
    """
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            result.append(node)
            
            # Add neighbors in reverse for same order as recursive
            for neighbor in reversed(graph.graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result


print("Graph edges: (1,2), (1,3), (2,4), (3,4)")
print(f"DFS recursive from 1: {dfs_recursive(g, 1)}")
print(f"DFS iterative from 1: {dfs_iterative(g, 1)}")
print()


# Pattern 3: Shortest Path (BFS)
print("=" * 60)
print("Pattern 3: Shortest Path (Unweighted)")
print("=" * 60)
print()
print("BFS finds shortest path in unweighted graphs.")
print()


def shortest_path(graph, start, end):
    """
    Find shortest path from start to end.
    
    How it works:
    1. BFS from start
    2. Track parent of each node
    3. Reconstruct path from end to start
    
    Time: O(V + E)
    Returns: path or None if no path exists
    """
    # STEP 1: Handle trivial case
    if start == end:
        return [start]
    
    # STEP 2: Initialize BFS data structures
    visited = {start}
    queue = deque([start])
    
    # STEP 3: Track parent of each node for path reconstruction
    # parent[node] = the node we came from to reach 'node'
    # This lets us work backwards from end to start
    parent = {start: None}
    
    # STEP 4: BFS exploration
    while queue:
        # STEP 5: Get next node to explore
        node = queue.popleft()
        
        # STEP 6: Check if we reached the target
        if node == end:
            # STEP 7: Reconstruct path by following parent pointers backwards
            path = []
            current = end
            # Work backwards from end to start
            while current is not None:
                path.append(current)
                current = parent[current]  # Move to parent
            
            # STEP 8: Reverse path (we built it backwards)
            return path[::-1]
        
        # STEP 9: Explore neighbors
        for neighbor in graph.graph[node]:
            if neighbor not in visited:
                # STEP 10: Mark as visited
                visited.add(neighbor)
                
                # STEP 11: Record how we reached this neighbor
                parent[neighbor] = node
                
                # STEP 12: Add to queue for later exploration
                queue.append(neighbor)
    
    # STEP 13: Queue empty without finding end - no path exists
    return None


def shortest_distance(graph, start, end):
    """
    Find shortest distance (number of edges).
    
    Time: O(V + E)
    Returns: distance or -1 if unreachable
    """
    if start == end:
        return 0
    
    visited = {start}
    queue = deque([(start, 0)])
    
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in graph.graph[node]:
            if neighbor == end:
                return dist + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # Unreachable


print("Find shortest path from 1 to 4:")
path = shortest_path(g, 1, 4)
print(f"Path: {path}")
print(f"Distance: {shortest_distance(g, 1, 4)}")
print()


# Pattern 4: Connected Components
print("=" * 60)
print("Pattern 4: Connected Components")
print("=" * 60)
print()
print("Find all disconnected parts of a graph.")
print()
print("Example graph with 2 components:")
print()
print("  Component 1:    Component 2:")
print("   1 --- 2         5 --- 6")
print("   |     |")
print("   3 --- 4")
print()


def count_connected_components(graph):
    """
    Count number of connected components.
    
    How it works:
    1. For each unvisited vertex, start DFS
    2. Each DFS finds one component
    3. Count number of DFS calls
    
    Time: O(V + E)
    """
    visited = set()
    count = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    for vertex in graph.graph:
        if vertex not in visited:
            dfs(vertex)
            count += 1
    
    return count


def find_all_components(graph):
    """
    Find all connected components.
    
    Returns: List of components (each component is a list of vertices)
    Time: O(V + E)
    """
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph.graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for vertex in graph.graph:
        if vertex not in visited:
            component = []
            dfs(vertex, component)
            components.append(component)
    
    return components


# Demo connected components
g2 = Graph()
g2.add_edge(1, 2)
g2.add_edge(1, 3)
g2.add_edge(2, 4)
g2.add_edge(3, 4)
g2.add_edge(5, 6)

print("Graph: (1,2), (1,3), (2,4), (3,4), (5,6)")
print(f"Number of components: {count_connected_components(g2)}")
print(f"Components: {find_all_components(g2)}")
print()


# Pattern 5: Cycle Detection
print("=" * 60)
print("Pattern 5: Cycle Detection")
print("=" * 60)
print()
print("Detect if graph contains a cycle.")
print()


def has_cycle_undirected(graph):
    """
    Detect cycle in undirected graph.
    
    How it works:
    1. DFS from each unvisited vertex
    2. Track parent to avoid false positives
    3. If visit a visited node (not parent), cycle found
    
    Time: O(V + E)
    """
    visited = set()
    
    def dfs(node, parent):
        # STEP 1: Mark current node as visited
        visited.add(node)
        
        # STEP 2: Explore all neighbors
        for neighbor in graph.graph[node]:
            # STEP 3: Check if neighbor has been visited
            if neighbor not in visited:
                # STEP 4: Neighbor unvisited - recursively explore
                # Pass current node as parent for next call
                if dfs(neighbor, node):
                    return True  # Cycle found in subtree
            
            # STEP 5: Neighbor is visited - potential cycle!
            # BUT: In undirected graph, edge goes both ways
            # If neighbor is our parent, that's just the edge we came from
            # Example: A---B, when at B, we see A but that's not a cycle
            elif neighbor != parent:
                # STEP 6: Visited neighbor that's NOT our parent = CYCLE!
                # We found a back edge to an ancestor
                return True
        
        # STEP 7: No cycle found from this node
        return False
    
    for vertex in graph.graph:
        if vertex not in visited:
            if dfs(vertex, None):
                return True
    
    return False


def has_cycle_directed(graph):
    """
    Detect cycle in directed graph.
    
    How it works:
    1. Track nodes in current recursion stack
    2. If revisit a node in stack, cycle found
    3. Three states: unvisited, in-stack, visited
    
    Time: O(V + E)
    """
    WHITE, GRAY, BLACK = 0, 1, 2  # unvisited, in-stack, visited
    color = defaultdict(lambda: WHITE)
    
    def dfs(node):
        color[node] = GRAY  # Mark as in-stack
        
        for neighbor in graph.graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge = cycle
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        
        color[node] = BLACK  # Mark as visited
        return False
    
    for vertex in graph.graph:
        if color[vertex] == WHITE:
            if dfs(vertex):
                return True
    
    return False


print("Undirected graph with cycle:")
print(f"Has cycle? {has_cycle_undirected(g)}")
print()


# Pattern 6: Bipartite Check
print("=" * 60)
print("Pattern 6: Bipartite Graph Check")
print("=" * 60)
print()
print("Check if graph can be 2-colored.")
print()
print("Bipartite graph example:")
print()
print("  Set A    Set B")
print("    1 ---- 3")
print("    |  \\ / |")
print("    |   X  |")
print("    |  / \\ |")
print("    2 ---- 4")
print()
print("Can color with 2 colors: A={1,2}, B={3,4}")
print()


def is_bipartite_bfs(graph):
    """
    Check if graph is bipartite using BFS.
    
    How it works:
    1. Try to color graph with 2 colors (0 and 1)
    2. Adjacent nodes must have different colors
    3. If conflict found, not bipartite
    
    Time: O(V + E)
    """
    color = {}
    
    def bfs(start):
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            
            for neighbor in graph.graph[node]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False  # Adjacent nodes same color
        
        return True
    
    for vertex in graph.graph:
        if vertex not in color:
            if not bfs(vertex):
                return False
    
    return True


def is_bipartite_dfs(graph):
    """
    Check if graph is bipartite using DFS.
    
    Time: O(V + E)
    """
    color = {}
    
    def dfs(node, c):
        color[node] = c
        
        for neighbor in graph.graph[node]:
            if neighbor not in color:
                if not dfs(neighbor, 1 - c):
                    return False
            elif color[neighbor] == c:
                return False
        
        return True
    
    for vertex in graph.graph:
        if vertex not in color:
            if not dfs(vertex, 0):
                return False
    
    return True


# Create bipartite graph
g3 = Graph()
g3.add_edge(1, 3)
g3.add_edge(1, 4)
g3.add_edge(2, 3)
g3.add_edge(2, 4)

print("Bipartite graph: (1,3), (1,4), (2,3), (2,4)")
print(f"Is bipartite (BFS)? {is_bipartite_bfs(g3)}")
print(f"Is bipartite (DFS)? {is_bipartite_dfs(g3)}")
print()


# Pattern 7: All Paths Between Two Nodes
print("=" * 60)
print("Pattern 7: Find All Paths")
print("=" * 60)
print()
print("Find all possible paths from source to destination.")
print()


def all_paths(graph, start, end):
    """
    Find all paths from start to end.
    
    How it works:
    1. DFS with backtracking
    2. Track current path
    3. When reach end, save path
    4. Backtrack and try other paths
    
    Time: O(V! × V) worst case
    """
    paths = []
    
    def dfs(node, path, visited):
        path.append(node)
        visited.add(node)
        
        if node == end:
            paths.append(path[:])
        else:
            for neighbor in graph.graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, path, visited)
        
        # Backtrack
        path.pop()
        visited.remove(node)
    
    dfs(start, [], set())
    return paths


print("Find all paths from 1 to 4:")
all_paths_result = all_paths(g, 1, 4)
for i, path in enumerate(all_paths_result, 1):
    print(f"  Path {i}: {' → '.join(map(str, path))}")
print()


# Pattern 8: Island Count (Grid BFS/DFS)
print("=" * 60)
print("Pattern 8: Island Count (Grid as Graph)")
print("=" * 60)
print()
print("Treat 2D grid as graph, count connected components.")
print()
print("Example grid (1=land, 0=water):")
print()
print("  1 1 0 0")
print("  1 0 0 1")
print("  0 0 1 1")
print()
print("Islands: 3 (top-left, middle-right, bottom-right)")
print()


def count_islands(grid):
    """
    Count number of islands in grid.
    
    How it works:
    1. For each land cell (1), start BFS/DFS
    2. Mark all connected land as visited
    3. Each BFS/DFS finds one island
    
    Time: O(rows × cols)
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0
    
    def bfs(r, c):
        queue = deque([(r, c)])
        visited.add((r, c))
        
        while queue:
            row, col = queue.popleft()
            
            # Check 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = row + dr, col + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited and grid[nr][nc] == 1):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                bfs(r, c)
                count += 1
    
    return count


grid = [
    [1, 1, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 1]
]

print(f"Number of islands: {count_islands(grid)}")
print()


# Pattern 9: Topological Sort
print("=" * 60)
print("Pattern 9: Topological Sort (DAG)")
print("=" * 60)
print()
print("Order vertices such that for edge u→v, u comes before v.")
print()
print("Example - Course prerequisites:")
print()
print("  Course 0 → Course 1 → Course 3")
print("            ↓")
print("         Course 2")
print()
print("Valid order: [0, 1, 2, 3] or [0, 2, 1, 3]")
print()


def topological_sort_dfs(graph):
    """
    Topological sort using DFS.
    
    How it works:
    1. DFS from each unvisited vertex
    2. Add vertex to result after visiting all neighbors
    3. Reverse result
    
    Time: O(V + E)
    Works only on DAG (Directed Acyclic Graph)
    """
    # STEP 1: Track visited nodes
    visited = set()
    
    # STEP 2: Result stack (will be reversed at end)
    # Key insight: nodes added to result in "finish time" order
    result = []
    
    def dfs(node):
        # STEP 3: Mark as visited
        visited.add(node)
        
        # STEP 4: Visit all neighbors first (go deep)
        for neighbor in graph.graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        
        # STEP 5: Add to result AFTER visiting all neighbors
        # This is the key! Ensures dependencies come before dependents
        # Example: if A→B, we visit B first, add B to result, then add A
        # So A comes before B in reversed result
        result.append(node)
    
    # STEP 6: DFS from each unvisited vertex
    # Needed because graph might be disconnected
    for vertex in graph.graph:
        if vertex not in visited:
            dfs(vertex)
    
    # STEP 7: Reverse to get correct topological order
    # Nodes with no outgoing edges were added first
    # Reversing puts them at the end (where they belong)
    return result[::-1]


def topological_sort_bfs(graph, vertices):
    """
    Topological sort using BFS (Kahn's algorithm).
    
    How it works:
    1. Calculate in-degree for each vertex
    2. Start with vertices having in-degree 0
    3. Process and reduce in-degree of neighbors
    4. Add neighbors with in-degree 0 to queue
    
    Time: O(V + E)
    """
    # STEP 1: Initialize in-degree counter for each vertex
    # in-degree = number of incoming edges
    in_degree = {v: 0 for v in vertices}
    
    # STEP 2: Calculate in-degrees by counting incoming edges
    # For each edge u→v, increment in_degree[v]
    for u in graph.graph:
        for v in graph.graph[u]:
            in_degree[v] += 1
    
    # STEP 3: Find all vertices with no incoming edges (in-degree = 0)
    # These can be processed first (no dependencies)
    queue = deque([v for v in vertices if in_degree[v] == 0])
    
    # STEP 4: Result list (will contain topological order)
    result = []
    
    # STEP 5: Process vertices in BFS order
    while queue:
        # STEP 6: Remove a vertex with no incoming edges
        node = queue.popleft()
        
        # STEP 7: Add to result (safe to process now)
        result.append(node)
        
        # STEP 8: Process all outgoing edges from this node
        for neighbor in graph.graph[node]:
            # STEP 9: Remove this edge by decreasing in-degree
            # Conceptually: we've "processed" the dependency
            in_degree[neighbor] -= 1
            
            # STEP 10: If neighbor now has no dependencies, it's ready!
            # Add to queue for processing
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # STEP 11: Check for cycles
    # If result doesn't contain all vertices, there's a cycle
    # (some vertices never reached in-degree 0 due to cycle)
    return result if len(result) == len(vertices) else []


# Demo topological sort
dag = Graph(directed=True)
dag.add_edge(0, 1)
dag.add_edge(0, 2)
dag.add_edge(1, 3)
dag.add_edge(2, 3)

vertices = [0, 1, 2, 3]
print("DAG edges: 0→1, 0→2, 1→3, 2→3")
print(f"Topological order (DFS): {topological_sort_dfs(dag)}")
print(f"Topological order (BFS): {topological_sort_bfs(dag, vertices)}")
print()


# Pattern 10: Course Schedule (Cycle Detection in DAG)
print("=" * 60)
print("Pattern 10: Course Schedule Problem")
print("=" * 60)
print()
print("Can complete all courses given prerequisites?")
print("(Check if DAG - no cycles)")
print()


def can_finish_courses(num_courses, prerequisites):
    """
    Determine if can finish all courses.
    
    How it works:
    1. Build directed graph from prerequisites
    2. Check for cycles using DFS
    3. If cycle exists, cannot finish
    
    Time: O(V + E)
    
    Example:
      Input: numCourses=4, prerequisites=[[1,0],[2,1],[3,2]]
      Output: True (can take in order: 0→1→2→3)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_courses
    
    def has_cycle(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Cycle detected
            if color[neighbor] == WHITE:
                if has_cycle(neighbor):
                    return True
        
        color[node] = BLACK
        return False
    
    for course in range(num_courses):
        if color[course] == WHITE:
            if has_cycle(course):
                return False
    
    return True


def find_course_order(num_courses, prerequisites):
    """
    Find valid course order (topological sort).
    
    Returns: Valid order or [] if impossible
    Time: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    result = []
    
    while queue:
        course = queue.popleft()
        result.append(course)
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return result if len(result) == num_courses else []


prerequisites = [[1, 0], [2, 1], [3, 2]]
print(f"Prerequisites: {prerequisites}")
print(f"Can finish? {can_finish_courses(4, prerequisites)}")
print(f"Course order: {find_course_order(4, prerequisites)}")
print()


# Summary
print("=" * 60)
print("Summary of Patterns")
print("=" * 60)
print()
print("BFS Patterns:")
print("  • Shortest path (unweighted)")
print("  • Level-order traversal")
print("  • Connected components")
print("  • Bipartite check")
print()
print("DFS Patterns:")
print("  • Path finding")
print("  • Cycle detection")
print("  • Topological sort")
print("  • Connected components")
print("  • Backtracking (all paths)")
print()
print("Time Complexity:")
print("  • Most operations: O(V + E)")
print("  • All paths: O(V! × V) worst case")
print()
print("Space Complexity:")
print("  • Visited set: O(V)")
print("  • Queue/Stack: O(V)")
print("  • Recursion: O(V) stack depth")
print()
