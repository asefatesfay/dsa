"""
Advanced Graph Patterns
========================
Complex graph algorithms and advanced problem-solving patterns.
"""

from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple
import heapq


print("=" * 60)
print("Advanced Graph Patterns")
print("=" * 60)
print()


# Pattern 1: Dijkstra's Shortest Path (Weighted Graphs)
print("=" * 60)
print("Pattern 1: Dijkstra's Shortest Path Algorithm")
print("=" * 60)
print()
print("Find shortest path in weighted graph with non-negative weights.")
print()
print("Example graph:")
print()
print("       7")
print("   0 ----- 1")
print("   |    /  |")
print(" 5 |  2    | 3")
print("   | /     |")
print("   2 ----- 3")
print("      4")
print()


def dijkstra(graph, start, end=None):
    """
    Dijkstra's algorithm for shortest path.
    
    How it works:
    1. Start with distance 0 to source, infinity to others
    2. Use min-heap to always process nearest unvisited node
    3. For each neighbor, update distance if shorter path found
    4. Continue until all nodes processed or target reached
    
    Step-by-step example:
    Graph: 0--(7)--1--(3)--3
           |      /      |
          (5)   (2)     (4)
           |   /        |
           2-----------3
    
    Find shortest path from 0 to 3:
    
    Step 1: Start at 0
      distances = {0: 0}
      heap = [(0, 0)]
    
    Step 2: Process 0, update neighbors
      Visit 0 (dist=0)
      Update 1: 0 + 7 = 7
      Update 2: 0 + 5 = 5
      distances = {0: 0, 1: 7, 2: 5}
      heap = [(5, 2), (7, 1)]
    
    Step 3: Process 2 (smallest distance)
      Visit 2 (dist=5)
      Update 1: 5 + 2 = 7 (same, no update)
      Update 3: 5 + 4 = 9
      distances = {0: 0, 1: 7, 2: 5, 3: 9}
      heap = [(7, 1), (9, 3)]
    
    Step 4: Process 1
      Visit 1 (dist=7)
      Update 3: 7 + 3 = 10 (worse than 9, no update)
      heap = [(9, 3)]
    
    Step 5: Process 3
      Visit 3 (dist=9) - DONE!
      Path: 0 → 2 → 3, Total distance: 9
    
    Time: O((V + E) log V) with min-heap
    Space: O(V)
    
    Args:
        graph: dict of {node: [(neighbor, weight), ...]}
        start: Starting node
        end: Optional ending node (if None, find distances to all)
    
    Returns: (distances dict, parent dict for path reconstruction)
    """
    # STEP 1: Initialize data structures
    # distances: shortest known distance from start to each node
    distances = {start: 0}
    
    # parent: track path for reconstruction (parent[node] = previous node in shortest path)
    parent = {start: None}
    
    # STEP 2: Initialize min-heap with start node
    # Heap stores (distance, node) tuples
    # Min-heap ensures we always process closest unvisited node next
    heap = [(0, start)]  # (distance, node)
    
    # STEP 3: Track visited nodes to avoid reprocessing
    visited = set()
    
    # STEP 4: Main loop - process nodes until heap is empty
    while heap:
        # STEP 5: Pop node with minimum distance
        # This is the "greedy" part - always pick nearest unvisited node
        current_dist, node = heapq.heappop(heap)
        
        # STEP 6: Skip if already visited
        # Heap may contain duplicate entries with different distances
        # Only process a node once (with its best distance)
        if node in visited:
            continue
        
        # STEP 7: Mark as visited
        visited.add(node)
        
        # STEP 8: Early exit optimization if target reached
        if end and node == end:
            break
        
        # STEP 9: Relax all edges from current node
        # "Relax" means: check if going through current node gives shorter path
        for neighbor, weight in graph.get(node, []):
            # STEP 10: Calculate new distance through current node
            new_dist = current_dist + weight
            
            # STEP 11: Update if this path is shorter
            # Either: neighbor not yet reached, OR new path is better
            if neighbor not in distances or new_dist < distances[neighbor]:
                # STEP 12: Update best known distance
                distances[neighbor] = new_dist
                
                # STEP 13: Record parent for path reconstruction
                parent[neighbor] = node
                
                # STEP 14: Add to heap for future processing
                # Note: We don't remove old (worse) entries from heap
                # They'll be skipped in step 6 when popped
                heapq.heappush(heap, (new_dist, neighbor))
    
    # STEP 15: Return results
    return distances, parent


def reconstruct_path(parent, start, end):
    """Reconstruct path from parent pointers"""
    if end not in parent:
        return None
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    
    return path[::-1]


# Demo Dijkstra
graph = {
    0: [(1, 7), (2, 5)],
    1: [(0, 7), (2, 2), (3, 3)],
    2: [(0, 5), (1, 2), (3, 4)],
    3: [(1, 3), (2, 4)]
}

print("Graph: 0--(7)--1--(3)--3")
print("       |      /      |")
print("      (5)   (2)     (4)")
print("       |   /        |")
print("       2 ---------- 3")
print()

distances, parent = dijkstra(graph, 0, 3)
path = reconstruct_path(parent, 0, 3)
print(f"Shortest distance from 0 to 3: {distances[3]}")
print(f"Path: {' → '.join(map(str, path))}")
print()


# Pattern 2: Bellman-Ford (Handles Negative Weights)
print("=" * 60)
print("Pattern 2: Bellman-Ford Algorithm")
print("=" * 60)
print()
print("Shortest path with negative edge weights (detects negative cycles).")
print()


def bellman_ford(vertices, edges, start):
    """
    Bellman-Ford algorithm for shortest paths.
    
    How it works:
    1. Initialize distances: 0 to start, infinity to others
    2. Relax all edges V-1 times
    3. Check for negative cycles (if distance can still improve)
    
    Step-by-step example:
    Vertices: [0, 1, 2, 3]
    Edges: (0,1,4), (0,2,5), (1,2,-3), (1,3,6), (2,3,2)
    Start: 0
    
    Initial:
      distances = {0: 0, 1: ∞, 2: ∞, 3: ∞}
    
    Iteration 1 (relax all edges):
      Edge (0,1,4): distances[1] = 0 + 4 = 4
      Edge (0,2,5): distances[2] = 0 + 5 = 5
      Edge (1,2,-3): distances[2] = 4 + (-3) = 1 (improved!)
      Edge (1,3,6): distances[3] = 4 + 6 = 10
      Edge (2,3,2): distances[3] = 1 + 2 = 3 (improved!)
      Result: {0: 0, 1: 4, 2: 1, 3: 3}
    
    Iteration 2:
      Edge (1,2,-3): distances[2] = 4 + (-3) = 1 (no change)
      Edge (2,3,2): distances[3] = 1 + 2 = 3 (no change)
      Result: {0: 0, 1: 4, 2: 1, 3: 3} - converged!
    
    Iteration 3:
      No changes (early convergence)
    
    Negative cycle check:
      Try relaxing all edges again
      If any distance improves, negative cycle exists
      In this example: No improvement → No negative cycle
    
    Why V-1 iterations?
      Longest simple path has at most V-1 edges
      Each iteration finds shortest path with one more edge
    
    Time: O(V × E)
    Space: O(V)
    
    Args:
        vertices: List of all vertices
        edges: List of (u, v, weight) tuples
        start: Starting vertex
    
    Returns: (distances dict, has_negative_cycle bool)
    """
    # STEP 1: Initialize distances to infinity (except start)
    distances = {v: float('inf') for v in vertices}
    distances[start] = 0
    
    # STEP 2: Initialize parent tracking for path reconstruction
    parent = {v: None for v in vertices}
    
    # STEP 3: Main loop - relax all edges V-1 times
    # Why V-1? Longest simple path has at most V-1 edges
    # After k iterations, we have shortest paths using at most k edges
    for iteration in range(len(vertices) - 1):
        # STEP 4: Try to improve distance through each edge
        for u, v, weight in edges:
            # STEP 5: Check if we can reach u (not infinity)
            if distances[u] != float('inf'):
                # STEP 6: Calculate potential new distance to v through u
                new_dist = distances[u] + weight
                
                # STEP 7: Update if this path is shorter
                # This is "relaxing" the edge
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    parent[v] = u
    
    # STEP 8: Check for negative weight cycles
    # If we can still improve distances after V-1 iterations,
    # there must be a negative cycle (allows infinite improvement)
    has_negative_cycle = False
    for u, v, weight in edges:
        # STEP 9: Try to relax edges one more time
        if distances[u] != float('inf'):
            if distances[u] + weight < distances[v]:
                # STEP 10: Found improvement after V-1 iterations = negative cycle!
                has_negative_cycle = True
                break
    
    # STEP 11: Return results
    return distances, has_negative_cycle, parent


# Demo Bellman-Ford
vertices = [0, 1, 2, 3]
edges = [
    (0, 1, 4),
    (0, 2, 5),
    (1, 2, -3),  # Negative weight
    (1, 3, 6),
    (2, 3, 2)
]

print("Graph with negative edge (1→2 weight -3):")
distances, has_cycle, parent = bellman_ford(vertices, edges, 0)
print(f"Has negative cycle? {has_cycle}")
print(f"Distances from 0: {distances}")
print()


# Pattern 3: Floyd-Warshall (All-Pairs Shortest Path)
print("=" * 60)
print("Pattern 3: Floyd-Warshall Algorithm")
print("=" * 60)
print()
print("Find shortest paths between all pairs of vertices.")
print()


def floyd_warshall(vertices, edges):
    """
    Floyd-Warshall all-pairs shortest path.
    
    How it works:
    1. Initialize distance matrix
    2. For each intermediate vertex k:
       Try using k as intermediate in path i→j
    3. Update distance if shorter path found
    
    Time: O(V³)
    Space: O(V²)
    
    Returns: Distance matrix (2D dict)
    """
    # Initialize distances
    dist = defaultdict(lambda: defaultdict(lambda: float('inf')))
    
    # Distance to self is 0
    for v in vertices:
        dist[v][v] = 0
    
    # Set edge weights
    for u, v, weight in edges:
        dist[u][v] = weight
    
    # Try all intermediate vertices
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


# Demo Floyd-Warshall
vertices = [0, 1, 2, 3]
edges = [(0, 1, 3), (0, 2, 6), (1, 2, 1), (1, 3, 4), (2, 3, 2)]

print("Computing all-pairs shortest paths:")
all_distances = floyd_warshall(vertices, edges)
print("\nDistance matrix:")
print("     0    1    2    3")
for i in vertices:
    print(f"{i}: ", end="")
    for j in vertices:
        d = all_distances[i][j]
        if d == float('inf'):
            print("  ∞ ", end=" ")
        else:
            print(f"{d:3} ", end=" ")
    print()
print()


# Pattern 4: Minimum Spanning Tree - Kruskal's Algorithm
print("=" * 60)
print("Pattern 4: Kruskal's MST Algorithm")
print("=" * 60)
print()
print("Find minimum spanning tree (connects all vertices with minimum total weight).")
print()


class UnionFind:
    """Union-Find (Disjoint Set Union) for cycle detection"""
    
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, v):
        """Find root with path compression"""
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]
    
    def union(self, u, v):
        """Union by rank"""
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u == root_v:
            return False  # Already in same set
        
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
        
        return True


def kruskal_mst(vertices, edges):
    """
    Kruskal's algorithm for MST.
    
    How it works:
    1. Sort edges by weight
    2. For each edge (u, v):
       - If u and v not connected, add edge to MST
       - Use Union-Find to track connectivity
    3. Continue until V-1 edges added
    
    Step-by-step example:
    Vertices: [0, 1, 2, 3]
    Edges: (0,1,10), (0,2,6), (0,3,5), (1,3,15), (2,3,4)
    
    Goal: Connect all vertices with minimum total weight
    
    Step 1: Sort edges by weight
      (2,3,4), (0,3,5), (0,2,6), (0,1,10), (1,3,15)
    
    Step 2: Process edges one by one
    
    Edge (2,3,4):
      Sets: {0}, {1}, {2}, {3}
      2 and 3 not connected → ADD edge
      MST: [(2,3,4)], weight: 4
      Sets: {0}, {1}, {2,3}
    
    Edge (0,3,5):
      Sets: {0}, {1}, {2,3}
      0 and 3 not connected → ADD edge
      MST: [(2,3,4), (0,3,5)], weight: 9
      Sets: {0,2,3}, {1}
    
    Edge (0,2,6):
      Sets: {0,2,3}, {1}
      0 and 2 already connected → SKIP (would create cycle)
      MST: [(2,3,4), (0,3,5)], weight: 9
    
    Edge (0,1,10):
      Sets: {0,2,3}, {1}
      0 and 1 not connected → ADD edge
      MST: [(2,3,4), (0,3,5), (0,1,10)], weight: 19
      Sets: {0,1,2,3}
    
    Stop: Have V-1 = 3 edges (all vertices connected)
    
    Final MST:
         0
        /|\\
       1 | 5
         |  \\
         10  3
         |    \\
         1     2
              (4)
    
    Total weight: 19
    
    Union-Find prevents cycles:
      - find(u) returns set representative
      - union(u,v) merges sets
      - If find(u) == find(v), already in same set (cycle!)
    
    Time: O(E log E) for sorting
    Space: O(V)
    
    Returns: (MST edges, total weight)
    """
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])
    
    uf = UnionFind(vertices)
    mst = []
    total_weight = 0
    
    for u, v, weight in sorted_edges:
        if uf.union(u, v):  # No cycle created
            mst.append((u, v, weight))
            total_weight += weight
            
            if len(mst) == len(vertices) - 1:
                break  # MST complete
    
    return mst, total_weight


# Demo Kruskal's
vertices = [0, 1, 2, 3]
edges = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]

print("Finding MST:")
mst, total = kruskal_mst(vertices, edges)
print(f"\nMST edges:")
for u, v, w in mst:
    print(f"  {u} -- {v} (weight: {w})")
print(f"Total weight: {total}")
print()


# Pattern 5: Prim's MST Algorithm
print("=" * 60)
print("Pattern 5: Prim's MST Algorithm")
print("=" * 60)
print()
print("Alternative MST algorithm - grows tree from starting vertex.")
print()


def prim_mst(graph, start):
    """
    Prim's algorithm for MST.
    
    How it works:
    1. Start with arbitrary vertex
    2. Use min-heap for edges from tree to non-tree vertices
    3. Add minimum weight edge that connects to new vertex
    4. Continue until all vertices included
    
    Time: O((V + E) log V)
    Space: O(V)
    
    Returns: (MST edges, total weight)
    """
    mst = []
    visited = {start}
    total_weight = 0
    
    # Add all edges from start
    edges = [(weight, start, neighbor) for neighbor, weight in graph[start]]
    heapq.heapify(edges)
    
    while edges and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges)
        
        if v in visited:
            continue
        
        visited.add(v)
        mst.append((u, v, weight))
        total_weight += weight
        
        # Add edges from newly added vertex
        for neighbor, edge_weight in graph[v]:
            if neighbor not in visited:
                heapq.heappush(edges, (edge_weight, v, neighbor))
    
    return mst, total_weight


# Demo Prim's
graph = {
    0: [(1, 10), (2, 6), (3, 5)],
    1: [(0, 10), (3, 15)],
    2: [(0, 6), (3, 4)],
    3: [(0, 5), (1, 15), (2, 4)]
}

print("Finding MST with Prim's:")
mst, total = prim_mst(graph, 0)
print(f"\nMST edges:")
for u, v, w in mst:
    print(f"  {u} -- {v} (weight: {w})")
print(f"Total weight: {total}")
print()


# Pattern 6: Strongly Connected Components (Kosaraju's Algorithm)
print("=" * 60)
print("Pattern 6: Strongly Connected Components")
print("=" * 60)
print()
print("Find maximal sets where every vertex reaches every other vertex.")
print()
print("Example:")
print("  0 → 1 → 2")
print("  ↑       ↓")
print("  4 ← 3 ← 2")
print()
print("SCCs: {0,1,2}, {3,4} if there are edges forming cycles")
print()


def kosaraju_scc(graph, vertices):
    """
    Kosaraju's algorithm for strongly connected components.
    
    How it works:
    1. DFS on original graph, record finish times
    2. Transpose graph (reverse all edges)
    3. DFS on transposed graph in decreasing finish time order
    4. Each DFS tree is one SCC
    
    Step-by-step example:
    Graph: 0→1→2→0 (cycle) and 3→4→5→3 (cycle) with 2→3
    
         0 → 1
         ↑   ↓
         └── 2 → 3 → 4
                 ↑   ↓
                 └── 5
    
    Step 1: First DFS - Record finish times
      Start at 0:
        Visit 0 → 1 → 2 → 3 → 4 → 5
        Finish order (reverse): 5, 4, 3, 2, 1, 0
      
      finish_order = [5, 4, 3, 2, 1, 0]
    
    Step 2: Transpose graph (reverse all edges)
      Original: 0→1, 1→2, 2→0, 2→3, 3→4, 4→5, 5→3
      Transposed: 1→0, 2→1, 0→2, 3→2, 4→3, 5→4, 3→5
      
         0 ← 1
         ↓   ↑
         2 ← 3 ← 4
                 ↓   ↑
                     5
    
    Step 3: Second DFS on transposed in reverse finish order
      Process 5 (highest finish time):
        DFS from 5: 5 → 4 → 3
        SCC 1: [5, 4, 3]
      
      Process 2 (next unvisited):
        DFS from 2: 2 → 1 → 0
        SCC 2: [2, 1, 0]
    
    Result: Two SCCs
      SCC 1: {3, 4, 5} - all can reach each other
      SCC 2: {0, 1, 2} - all can reach each other
    
    Why this works:
      - First DFS finds "exit points" from SCCs
      - Transpose reverses edge directions
      - Second DFS in reverse order ensures we process
        one complete SCC at a time
      - Cannot jump between SCCs in transposed graph
    
    Time: O(V + E)
    Space: O(V)
    
    Returns: List of SCCs (each SCC is a list of vertices)
    """
    # Step 1: DFS to get finish order
    visited = set()
    finish_order = []
    
    def dfs1(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs1(neighbor)
        finish_order.append(node)
    
    for v in vertices:
        if v not in visited:
            dfs1(v)
    
    # Step 2: Transpose graph
    transposed = defaultdict(list)
    for u in graph:
        for v in graph[u]:
            transposed[v].append(u)
    
    # Step 3: DFS on transposed in reverse finish order
    visited = set()
    sccs = []
    
    def dfs2(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in transposed.get(node, []):
            if neighbor not in visited:
                dfs2(neighbor, component)
    
    for node in reversed(finish_order):
        if node not in visited:
            component = []
            dfs2(node, component)
            sccs.append(component)
    
    return sccs


# Demo Kosaraju's
directed_graph = {
    0: [1],
    1: [2],
    2: [0, 3],
    3: [4],
    4: [5],
    5: [3]
}
vertices = [0, 1, 2, 3, 4, 5]

print("Finding SCCs:")
sccs = kosaraju_scc(directed_graph, vertices)
print(f"\nStrongly Connected Components:")
for i, scc in enumerate(sccs, 1):
    print(f"  SCC {i}: {scc}")
print()


# Pattern 7: Articulation Points (Cut Vertices)
print("=" * 60)
print("Pattern 7: Articulation Points")
print("=" * 60)
print()
print("Vertices whose removal disconnects the graph.")
print()


def find_articulation_points(graph, vertices):
    """
    Find articulation points using Tarjan's algorithm.
    
    How it works:
    1. DFS with discovery time and low-link value
    2. low[v] = min(disc[v], disc[u] for backedge v→u, low[child])
    3. Vertex u is articulation point if:
       - Root with 2+ children, OR
       - Non-root with child v where low[v] >= disc[u]
    
    Step-by-step example:
    Graph:
         0 --- 1 --- 2
               |     |
               3 --- 4
    
    DFS traversal from 0:
    
    Visit 0 (time=0):
      disc[0] = 0, low[0] = 0
      
    Visit 1 (time=1):
      disc[1] = 1, low[1] = 1
      
    Visit 2 (time=2):
      disc[2] = 2, low[2] = 2
      
    Visit 4 (time=3):
      disc[4] = 3, low[4] = 3
      
    Visit 3 (time=4):
      disc[3] = 4, low[3] = 4
      Back edge to 1: low[3] = min(4, disc[1]) = 1
      
    Backtrack to 4:
      low[4] = min(low[4], low[3]) = min(3, 1) = 1
      
    Backtrack to 2:
      low[2] = min(low[2], low[4]) = min(2, 1) = 1
      Check: low[4]=1 < disc[2]=2 (no articulation point)
      
    Backtrack to 1:
      low[1] = min(low[1], low[2]) = min(1, 1) = 1
      Check: low[2]=1 >= disc[1]=1 → 1 is articulation point!
      Check: low[3]=1 >= disc[1]=1 → 1 is articulation point!
      
    Backtrack to 0:
      low[0] = min(low[0], low[1]) = 0
      Root with 1 child → not articulation point
    
    Result: Vertex 1 is articulation point
      Removing 1 disconnects {0} from {2,3,4}
    
    Key concepts:
      disc[v] = discovery time (when first visited)
      low[v] = lowest disc reachable from v's subtree
      
      If low[child] >= disc[u]:
        child cannot reach above u without going through u
        → u is articulation point (cut vertex)
    
    Time: O(V + E)
    Space: O(V)
    """
    discovery = {}
    low = {}
    parent = {}
    articulation_points = set()
    time = [0]
    
    def dfs(u):
        children = 0
        discovery[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph.get(u, []):
            if v not in discovery:
                children += 1
                parent[v] = u
                dfs(v)
                
                low[u] = min(low[u], low[v])
                
                # Check if u is articulation point
                if parent.get(u) is None and children > 1:
                    articulation_points.add(u)  # Root with 2+ children
                
                if parent.get(u) is not None and low[v] >= discovery[u]:
                    articulation_points.add(u)  # Non-root condition
            
            elif v != parent.get(u):
                low[u] = min(low[u], discovery[v])  # Back edge
    
    for v in vertices:
        if v not in discovery:
            parent[v] = None
            dfs(v)
    
    return list(articulation_points)


# Demo Articulation Points
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2, 4],
    4: [3]
}
vertices = [0, 1, 2, 3, 4]

print("Graph: 0-1-2-3-4 (with 0-1-2 forming triangle)")
print("Finding articulation points:")
aps = find_articulation_points(graph, vertices)
print(f"Articulation points: {aps}")
print("(Removing vertex 2 or 3 would disconnect the graph)")
print()


# Pattern 8: Bridges (Cut Edges)
print("=" * 60)
print("Pattern 8: Bridges (Cut Edges)")
print("=" * 60)
print()
print("Edges whose removal disconnects the graph.")
print()


def find_bridges(graph, vertices):
    """
    Find bridges using Tarjan's algorithm.
    
    How it works:
    1. Similar to articulation points
    2. Edge u-v is bridge if low[v] > disc[u]
       (no back edge from v's subtree to u's ancestors)
    
    Time: O(V + E)
    Space: O(V)
    """
    discovery = {}
    low = {}
    parent = {}
    bridges = []
    time = [0]
    
    def dfs(u):
        discovery[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph.get(u, []):
            if v not in discovery:
                parent[v] = u
                dfs(v)
                
                low[u] = min(low[u], low[v])
                
                # Check if u-v is bridge
                if low[v] > discovery[u]:
                    bridges.append((u, v))
            
            elif v != parent.get(u):
                low[u] = min(low[u], discovery[v])
    
    for v in vertices:
        if v not in discovery:
            parent[v] = None
            dfs(v)
    
    return bridges


# Demo Bridges
print("Finding bridges:")
bridges = find_bridges(graph, vertices)
print(f"Bridges: {bridges}")
print("(Removing edge 2-3 or 3-4 would disconnect the graph)")
print()


# Pattern 9: Eulerian Path/Circuit
print("=" * 60)
print("Pattern 9: Eulerian Path and Circuit")
print("=" * 60)
print()
print("Eulerian Path: Visit every edge exactly once")
print("Eulerian Circuit: Eulerian path that starts and ends at same vertex")
print()


def has_eulerian_path_circuit(graph, vertices):
    """
    Check if graph has Eulerian path or circuit.
    
    Conditions:
    - Eulerian Circuit: All vertices have even degree
    - Eulerian Path: Exactly 0 or 2 vertices have odd degree
    
    Time: O(V + E)
    """
    degree = {v: 0 for v in vertices}
    
    for u in graph:
        for v in graph[u]:
            degree[u] += 1
    
    odd_degree_vertices = [v for v in vertices if degree[v] % 2 == 1]
    
    if len(odd_degree_vertices) == 0:
        return "Eulerian Circuit", True
    elif len(odd_degree_vertices) == 2:
        return "Eulerian Path", True
    else:
        return "None", False


def find_eulerian_path(graph, start):
    """
    Find Eulerian path using Hierholzer's algorithm.
    
    How it works:
    1. Start DFS from any vertex with odd degree (or any vertex)
    2. Follow edges, removing them as visited
    3. Backtrack when stuck, adding to path
    4. Reverse final path
    
    Time: O(E)
    """
    # Create adjacency list copy (will modify)
    adj = defaultdict(list)
    for u in graph:
        adj[u] = list(graph[u])
    
    path = []
    stack = [start]
    
    while stack:
        u = stack[-1]
        
        if adj[u]:
            v = adj[u].pop()
            # Remove reverse edge (for undirected)
            if u in adj[v]:
                adj[v].remove(u)
            stack.append(v)
        else:
            path.append(stack.pop())
    
    return path[::-1]


# Demo Eulerian
test_graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1]
}
vertices = [0, 1, 2]

print("Triangle graph (all vertices degree 2):")
result, exists = has_eulerian_path_circuit(test_graph, vertices)
print(f"Has {result}: {exists}")
print()


# Pattern 10: Traveling Salesman Problem (TSP) - DP Solution
print("=" * 60)
print("Pattern 10: Traveling Salesman Problem")
print("=" * 60)
print()
print("Visit all cities exactly once and return to start (minimize cost).")
print()


def tsp_dp(dist, n):
    """
    TSP using dynamic programming with bitmask.
    
    How it works:
    1. dp[mask][i] = min cost to visit cities in mask, ending at i
    2. Try all possible last cities
    3. Reconstruct path from DP table
    
    Step-by-step example (4 cities):
    Distance matrix:
         0   1   2   3
      0 [0, 10, 15, 20]
      1 [10, 0, 35, 25]
      2 [15, 35, 0, 30]
      3 [20, 25, 30, 0]
    
    Bitmask representation:
      0001 (1) = visited {0}
      0011 (3) = visited {0, 1}
      0111 (7) = visited {0, 1, 2}
      1111 (15) = visited all
    
    Step 1: Initialize
      dp[0001][0] = 0 (start at city 0)
      All other states = ∞
    
    Step 2: Build up subsets
      mask = 0001 (only city 0):
        Add city 1: dp[0011][1] = 0 + 10 = 10
        Add city 2: dp[0101][2] = 0 + 15 = 15
        Add city 3: dp[1001][3] = 0 + 20 = 20
      
      mask = 0011 (cities 0,1):
        From city 1, add city 2:
          dp[0111][2] = min(∞, 10 + 35) = 45
        From city 1, add city 3:
          dp[1011][3] = min(∞, 10 + 25) = 35
      
      mask = 0101 (cities 0,2):
        From city 2, add city 1:
          dp[0111][1] = min(∞, 15 + 35) = 50
        From city 2, add city 3:
          dp[1101][3] = min(∞, 15 + 30) = 45
      
      ... continue for all subsets ...
    
    Step 3: Find minimum for visiting all cities
      mask = 1111 (all cities visited)
      Try ending at each city and return to 0:
        End at 1: dp[1111][1] + dist[1][0]
        End at 2: dp[1111][2] + dist[2][0]
        End at 3: dp[1111][3] + dist[3][0]
      
      Choose minimum = optimal tour cost
    
    Example tour: 0 → 1 → 3 → 2 → 0
      Cost: 10 + 25 + 30 + 15 = 80
    
    Why bitmask?
      Efficiently represent which cities visited
      Can check in O(1): if (mask & (1 << i)) then city i visited
      Can add city: new_mask = mask | (1 << i)
    
    Time: O(n² × 2ⁿ)
    Space: O(n × 2ⁿ)
    
    Args:
        dist: 2D distance matrix
        n: Number of cities
    
    Returns: min cost
    """
    # dp[mask][i] = min cost visiting cities in mask, ending at city i
    dp = [[float('inf')] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    
    # Start at city 0
    dp[1][0] = 0
    
    # Try all subsets
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            
            # Try adding each city
            for next_city in range(n):
                if mask & (1 << next_city):
                    continue
                
                new_mask = mask | (1 << next_city)
                new_cost = dp[mask][last] + dist[last][next_city]
                
                if new_cost < dp[new_mask][next_city]:
                    dp[new_mask][next_city] = new_cost
                    parent[new_mask][next_city] = last
    
    # Find minimum cost to visit all and return to start
    full_mask = (1 << n) - 1
    min_cost = float('inf')
    last_city = -1
    
    for i in range(n):
        cost = dp[full_mask][i] + dist[i][0]
        if cost < min_cost:
            min_cost = cost
            last_city = i
    
    return min_cost


# Demo TSP (small example)
dist_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

print("Distance matrix (4 cities):")
for row in dist_matrix:
    print(f"  {row}")
print()

min_cost = tsp_dp(dist_matrix, 4)
print(f"Minimum TSP cost: {min_cost}")
print("(Visit all cities once and return to start)")
print()


# Summary
print("=" * 60)
print("Summary of Advanced Patterns")
print("=" * 60)
print()
print("Shortest Path Algorithms:")
print("  • Dijkstra: Non-negative weights, O((V+E) log V)")
print("  • Bellman-Ford: Handles negative weights, O(VE)")
print("  • Floyd-Warshall: All-pairs, O(V³)")
print()
print("Minimum Spanning Tree:")
print("  • Kruskal: Sort edges, Union-Find, O(E log E)")
print("  • Prim: Grow tree, min-heap, O((V+E) log V)")
print()
print("Graph Structure:")
print("  • Strongly Connected Components: Kosaraju's, O(V+E)")
print("  • Articulation Points: Tarjan's, O(V+E)")
print("  • Bridges: Similar to articulation points")
print()
print("Special Paths:")
print("  • Eulerian Path: Visit every edge once")
print("  • Hamiltonian Path: Visit every vertex once (NP-hard)")
print("  • TSP: Hamiltonian cycle with min cost, O(n² × 2ⁿ)")
print()
print("When to Use:")
print("  • Single-source shortest path: Dijkstra (positive) or Bellman-Ford")
print("  • All-pairs shortest: Floyd-Warshall (small graphs)")
print("  • Connect all vertices min cost: MST (Kruskal/Prim)")
print("  • Find critical vertices/edges: Articulation points/Bridges")
print("  • Directed graph cycles: SCC")
print()
