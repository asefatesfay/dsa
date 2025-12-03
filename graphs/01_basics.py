"""
Graphs - Basics
===============
Understanding graph data structures and representations.
"""

from collections import defaultdict, deque


print("=" * 60)
print("What is a Graph?")
print("=" * 60)
print()
print("A graph is a collection of nodes (vertices) connected by edges.")
print()
print("Key Terminology:")
print("  • Vertex (Node): A point in the graph")
print("  • Edge: Connection between two vertices")
print("  • Directed: Edges have direction (A → B)")
print("  • Undirected: Edges have no direction (A ↔ B)")
print("  • Weighted: Edges have values/costs")
print("  • Unweighted: All edges equal (or weight = 1)")
print()
print("Graph Types:")
print("  • Directed Graph (Digraph): Edges have direction")
print("  • Undirected Graph: Edges are bidirectional")
print("  • Weighted Graph: Edges have weights")
print("  • Cyclic: Contains cycles")
print("  • Acyclic: No cycles (DAG = Directed Acyclic Graph)")
print("  • Connected: Path exists between all vertices")
print("  • Disconnected: Some vertices unreachable")
print()
print("Example - Undirected Graph:")
print()
print("     1 ---- 2")
print("     |      |")
print("     |      |")
print("     3 ---- 4")
print()
print("Edges: (1,2), (1,3), (2,4), (3,4)")
print()
print("Example - Directed Graph:")
print()
print("     1 → 2")
print("     ↓   ↓")
print("     3 → 4")
print()
print("Edges: 1→2, 1→3, 2→4, 3→4")
print()


# Graph Representation 1: Adjacency Matrix
print("=" * 60)
print("Graph Representation 1: Adjacency Matrix")
print("=" * 60)
print()
print("Use 2D array where matrix[i][j] = 1 if edge exists.")
print()
print("Example graph:")
print("     0 ---- 1")
print("     |      |")
print("     2 ---- 3")
print()
print("Adjacency Matrix:")
print("     0  1  2  3")
print("  0 [0, 1, 1, 0]")
print("  1 [1, 0, 0, 1]")
print("  2 [1, 0, 0, 1]")
print("  3 [0, 1, 1, 0]")
print()
print("Advantages:")
print("  ✓ O(1) edge lookup")
print("  ✓ Simple implementation")
print("  ✓ Good for dense graphs")
print()
print("Disadvantages:")
print("  ✗ O(V²) space")
print("  ✗ Slow to iterate neighbors O(V)")
print("  ✗ Wastes space for sparse graphs")
print()


class GraphMatrix:
    """Graph using adjacency matrix"""
    
    def __init__(self, num_vertices, directed=False):
        """
        Initialize graph with V vertices.
        
        Time: O(V²), Space: O(V²)
        """
        self.V = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]
    
    def add_edge(self, u, v, weight=1):
        """
        Add edge between u and v.
        
        Time: O(1)
        """
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight
    
    def remove_edge(self, u, v):
        """Remove edge. Time: O(1)"""
        self.matrix[u][v] = 0
        if not self.directed:
            self.matrix[v][u] = 0
    
    def has_edge(self, u, v):
        """Check if edge exists. Time: O(1)"""
        return self.matrix[u][v] != 0
    
    def get_neighbors(self, v):
        """
        Get all neighbors of v.
        
        Time: O(V)
        """
        neighbors = []
        for i in range(self.V):
            if self.matrix[v][i] != 0:
                neighbors.append(i)
        return neighbors
    
    def print_graph(self):
        """Display adjacency matrix"""
        print("\nAdjacency Matrix:")
        for row in self.matrix:
            print("  ", row)


# Graph Representation 2: Adjacency List
print("=" * 60)
print("Graph Representation 2: Adjacency List")
print("=" * 60)
print()
print("Use dictionary/array where list[i] = neighbors of vertex i.")
print()
print("Example graph:")
print("     0 ---- 1")
print("     |      |")
print("     2 ---- 3")
print()
print("Adjacency List:")
print("  0 → [1, 2]")
print("  1 → [0, 3]")
print("  2 → [0, 3]")
print("  3 → [1, 2]")
print()
print("Advantages:")
print("  ✓ O(V + E) space (space efficient)")
print("  ✓ Fast neighbor iteration O(degree)")
print("  ✓ Good for sparse graphs")
print()
print("Disadvantages:")
print("  ✗ O(degree) edge lookup")
print("  ✗ Slightly more complex")
print()


class Graph:
    """Graph using adjacency list (most common)"""
    
    def __init__(self, directed=False):
        """
        Initialize empty graph.
        
        Time: O(1), Space: O(1)
        """
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v, weight=None):
        """
        Add edge between u and v.
        
        Time: O(1) average
        """
        if weight is not None:
            self.graph[u].append((v, weight))
            if not self.directed:
                self.graph[v].append((u, weight))
        else:
            self.graph[u].append(v)
            if not self.directed:
                self.graph[v].append(u)
    
    def remove_edge(self, u, v):
        """Remove edge. Time: O(degree)"""
        if v in self.graph[u]:
            self.graph[u].remove(v)
        if not self.directed and u in self.graph[v]:
            self.graph[v].remove(u)
    
    def get_neighbors(self, v):
        """Get neighbors. Time: O(1)"""
        return self.graph[v]
    
    def get_vertices(self):
        """Get all vertices. Time: O(1)"""
        return list(self.graph.keys())
    
    def print_graph(self):
        """Display adjacency list"""
        print("\nAdjacency List:")
        for vertex in sorted(self.graph.keys()):
            print(f"  {vertex} → {self.graph[vertex]}")


print("=" * 60)
print("Graph Implementations Demo")
print("=" * 60)
print()

# Adjacency Matrix example
print("Adjacency Matrix Implementation:")
gm = GraphMatrix(4, directed=False)
gm.add_edge(0, 1)
gm.add_edge(0, 2)
gm.add_edge(1, 3)
gm.add_edge(2, 3)
gm.print_graph()

print()

# Adjacency List example
print("Adjacency List Implementation:")
g = Graph(directed=False)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(2, 3)
g.print_graph()

print()


# Edge List Representation
print("=" * 60)
print("Graph Representation 3: Edge List")
print("=" * 60)
print()
print("Store list of all edges: [(u, v, weight), ...]")
print()
print("Example:")
print("  Edges = [(0,1), (0,2), (1,3), (2,3)]")
print()
print("Advantages:")
print("  ✓ Simple for some algorithms (Kruskal's MST)")
print("  ✓ Easy to sort by weight")
print()
print("Disadvantages:")
print("  ✗ Slow neighbor lookup O(E)")
print("  ✗ Slow edge lookup O(E)")
print()


class EdgeListGraph:
    """Graph using edge list"""
    
    def __init__(self, directed=False):
        self.edges = []
        self.directed = directed
        self.vertices = set()
    
    def add_edge(self, u, v, weight=1):
        """Add edge. Time: O(1)"""
        self.edges.append((u, v, weight))
        self.vertices.add(u)
        self.vertices.add(v)
        
        if not self.directed:
            self.edges.append((v, u, weight))
    
    def print_graph(self):
        """Display edge list"""
        print("\nEdge List:")
        for u, v, w in self.edges:
            print(f"  {u} → {v} (weight: {w})")


# Weighted Graph Example
print("=" * 60)
print("Weighted Graph Example")
print("=" * 60)
print()
print("Graph with edge weights:")
print()
print("       2")
print("   0 ---- 1")
print("   |      |")
print(" 5 |      | 3")
print("   |      |")
print("   2 ---- 3")
print("       4")
print()

weighted_g = Graph(directed=False)
weighted_g.add_edge(0, 1, 2)
weighted_g.add_edge(0, 2, 5)
weighted_g.add_edge(1, 3, 3)
weighted_g.add_edge(2, 3, 4)
weighted_g.print_graph()

print()


# Graph Properties
def count_vertices(graph):
    """Count number of vertices"""
    return len(graph.graph)


def count_edges(graph):
    """
    Count number of edges.
    For undirected graph, each edge counted twice.
    """
    total = sum(len(neighbors) for neighbors in graph.graph.values())
    return total if graph.directed else total // 2


def get_degree(graph, vertex):
    """
    Get degree of vertex (number of edges).
    
    Directed graph:
      • In-degree: incoming edges
      • Out-degree: outgoing edges
    """
    return len(graph.graph[vertex])


def is_connected_undirected(graph):
    """
    Check if undirected graph is connected.
    
    How it works:
    1. Start DFS from any vertex
    2. Count reachable vertices
    3. If all reachable, graph is connected
    
    Time: O(V + E)
    """
    if not graph.graph:
        return True
    
    visited = set()
    start = next(iter(graph.graph.keys()))
    
    def dfs(v):
        visited.add(v)
        for neighbor in graph.graph[v]:
            if neighbor not in visited:
                dfs(neighbor)
    
    dfs(start)
    return len(visited) == len(graph.graph)


print("=" * 60)
print("Graph Properties")
print("=" * 60)
print()

print(f"Number of vertices: {count_vertices(g)}")
print(f"Number of edges: {count_edges(g)}")
print(f"Degree of vertex 0: {get_degree(g, 0)}")
print(f"Is connected? {is_connected_undirected(g)}")

print()


# Special Graph Types
print("=" * 60)
print("Special Types of Graphs")
print("=" * 60)
print()

print("1. Complete Graph (Kₙ):")
print("   Every vertex connected to every other vertex")
print("   Edges = n(n-1)/2")
print()
print("   K₄:")
print("     1 ---- 2")
print("     |\\    /|")
print("     | \\  / |")
print("     |  \\/  |")
print("     |  /\\  |")
print("     | /  \\ |")
print("     |/    \\|")
print("     3 ---- 4")
print()

print("2. Tree:")
print("   Connected acyclic graph")
print("   V vertices, V-1 edges")
print("   Exactly one path between any two vertices")
print()
print("     1")
print("    / \\")
print("   2   3")
print("  / \\")
print(" 4   5")
print()

print("3. Bipartite Graph:")
print("   Vertices split into two sets")
print("   Edges only between sets, not within")
print()
print("   Set A    Set B")
print("     1 ---- 4")
print("     |  \\ / |")
print("     |   X  |")
print("     |  / \\ |")
print("     2 ---- 5")
print("     |      |")
print("     3 ---- 6")
print()

print("4. Cyclic Graph:")
print("   Contains at least one cycle")
print()
print("     1 → 2")
print("     ↑   ↓")
print("     4 ← 3")
print()

print("5. DAG (Directed Acyclic Graph):")
print("   Directed with no cycles")
print("   Used in: task scheduling, dependency resolution")
print()
print("     1 → 2")
print("     ↓   ↓")
print("     3 → 4")
print()


# Graph vs Tree
print("=" * 60)
print("Graph vs Tree")
print("=" * 60)
print()
print("                Graph           Tree")
print("-" * 60)
print("Edges           Any             V-1")
print("Cycles          May have        None")
print("Root            None            Has root")
print("Parent          Multiple        One")
print("Connection      May be unconnected  Connected")
print("Direction       Any             Parent → Child")
print()
print("Relationship:")
print("  • Tree is a special case of graph")
print("  • Tree = Connected Acyclic Undirected Graph")
print()


# Representation Comparison
print("=" * 60)
print("Choosing Graph Representation")
print("=" * 60)
print()
print("                Matrix      List        Edge List")
print("-" * 60)
print("Space           O(V²)       O(V+E)      O(E)")
print("Add edge        O(1)        O(1)        O(1)")
print("Remove edge     O(1)        O(V)        O(E)")
print("Check edge      O(1)        O(V)        O(E)")
print("Get neighbors   O(V)        O(1)        O(E)")
print()
print("Use Adjacency Matrix when:")
print("  • Dense graph (many edges)")
print("  • Need fast edge lookup")
print("  • Graph is small")
print()
print("Use Adjacency List when:")
print("  • Sparse graph (few edges) - MOST COMMON")
print("  • Need to iterate neighbors")
print("  • Memory is concern")
print()
print("Use Edge List when:")
print("  • Need to process all edges")
print("  • Algorithms like Kruskal's MST")
print("  • Simple storage")
print()


# Real-world applications
print("=" * 60)
print("Real-World Applications of Graphs")
print("=" * 60)
print()
print("1. Social Networks:")
print("   • Vertices = people")
print("   • Edges = friendships/connections")
print("   • Facebook, LinkedIn, Twitter")
print()
print("2. Maps and Navigation:")
print("   • Vertices = locations")
print("   • Edges = roads/paths")
print("   • Google Maps, GPS routing")
print()
print("3. Web Pages:")
print("   • Vertices = web pages")
print("   • Edges = hyperlinks")
print("   • PageRank algorithm")
print()
print("4. Computer Networks:")
print("   • Vertices = computers/routers")
print("   • Edges = network connections")
print("   • Internet routing")
print()
print("5. Dependencies:")
print("   • Vertices = tasks/packages")
print("   • Edges = dependencies")
print("   • Build systems, package managers")
print()
print("6. Recommendation Systems:")
print("   • Vertices = users/items")
print("   • Edges = ratings/purchases")
print("   • Amazon, Netflix recommendations")
print()
print("7. Biology:")
print("   • Vertices = proteins/genes")
print("   • Edges = interactions")
print("   • Protein interaction networks")
print()
print("8. Circuits:")
print("   • Vertices = components")
print("   • Edges = wires/connections")
print("   • Circuit design")
print()


# Building graphs from different inputs
print("=" * 60)
print("Building Graphs from Different Inputs")
print("=" * 60)
print()


def build_from_edges(edges, directed=False):
    """
    Build graph from edge list.
    
    Input: [(u, v), (u, v), ...]
    Time: O(E)
    """
    graph = Graph(directed)
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def build_from_matrix(matrix, directed=False):
    """
    Build graph from adjacency matrix.
    
    Time: O(V²)
    """
    graph = Graph(directed)
    n = len(matrix)
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                graph.add_edge(i, j)
    
    return graph


print("Example: Build from edge list")
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
g_from_edges = build_from_edges(edges)
g_from_edges.print_graph()

print()


# Graph operations
print("=" * 60)
print("Basic Graph Operations")
print("=" * 60)
print()


def reverse_graph(graph):
    """
    Reverse all edges (for directed graphs).
    
    Time: O(V + E)
    """
    reversed_g = Graph(directed=True)
    
    for u in graph.graph:
        for v in graph.graph[u]:
            reversed_g.add_edge(v, u)
    
    return reversed_g


def get_all_paths(graph, start, end):
    """
    Find all paths from start to end.
    
    How it works:
    1. DFS with backtracking
    2. Track current path
    3. When reach end, save path
    
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
        
        path.pop()
        visited.remove(node)
    
    dfs(start, [], set())
    return paths


print("Example: Find all paths from 0 to 3")
all_paths = get_all_paths(g, 0, 3)
print(f"Paths from 0 to 3:")
for i, path in enumerate(all_paths, 1):
    print(f"  Path {i}: {path}")

print()


# Common graph checks
print("=" * 60)
print("Common Graph Checks")
print("=" * 60)
print()


def has_cycle_undirected(graph):
    """
    Check if undirected graph has cycle.
    
    How it works:
    1. DFS from each unvisited vertex
    2. If visit a visited vertex (not parent), cycle exists
    
    Time: O(V + E)
    """
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph.graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # Found cycle
        
        return False
    
    for vertex in graph.graph:
        if vertex not in visited:
            if dfs(vertex, None):
                return True
    
    return False


def is_bipartite(graph):
    """
    Check if graph is bipartite (2-colorable).
    
    How it works:
    1. Try to color graph with 2 colors
    2. Adjacent nodes must have different colors
    3. If successful, graph is bipartite
    
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
                    return False  # Same color as neighbor
        
        return True
    
    for vertex in graph.graph:
        if vertex not in color:
            if not bfs(vertex):
                return False
    
    return True


print(f"Does graph have cycle? {has_cycle_undirected(g)}")
print(f"Is graph bipartite? {is_bipartite(g)}")

print()


# Summary
print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Key Concepts:")
print("  • Graph = vertices + edges")
print("  • Can be directed/undirected, weighted/unweighted")
print("  • Three main representations:")
print("    1. Adjacency Matrix - O(V²) space, O(1) lookup")
print("    2. Adjacency List - O(V+E) space, fast iteration")
print("    3. Edge List - O(E) space, simple")
print()
print("Common Operations:")
print("  • Add/remove vertices and edges")
print("  • Check connectivity")
print("  • Find paths")
print("  • Detect cycles")
print("  • Check bipartiteness")
print()
print("Next: Graph traversal algorithms (BFS, DFS)")
print()
