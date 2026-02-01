"""
Union-Find - Basics
==================
Basic implementation of Union-Find (Disjoint Set Union) data structure.
"""

print("=" * 60)
print("Union-Find Data Structure")
print("=" * 60)
print()


class UnionFind:
    """
    Union-Find with path compression and union by rank.
    
    Operations:
    - find(x): O(α(n)) ≈ O(1)
    - union(x, y): O(α(n)) ≈ O(1)
    - connected(x, y): O(α(n)) ≈ O(1)
    
    Space: O(n)
    """
    
    def __init__(self, n):
        """Initialize n disjoint sets."""
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n           # Rank (approximate tree height)
        self.count = n                # Number of disjoint sets
    
    def find(self, x):
        """
        Find root of set containing x.
        Implements path compression.
        """
        if self.parent[x] != x:
            # Path compression: make x point directly to root
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Merge sets containing x and y.
        Implements union by rank.
        Returns True if merge happened, False if already connected.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            # Equal rank: make one root and increase its rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.count -= 1  # Merged two sets
        return True
    
    def connected(self, x, y):
        """Check if x and y are in same set."""
        return self.find(x) == self.find(y)
    
    def get_count(self):
        """Get number of disjoint sets."""
        return self.count
    
    def get_all_components(self):
        """Get all connected components as dict."""
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        return components


print("Example: Building Connected Components")
print()

# Create 10 nodes (0-9)
uf = UnionFind(10)
print(f"Initial: {uf.count} disjoint sets")
print(f"Parent array: {uf.parent}")
print()

# Connect some nodes
connections = [
    (0, 1),
    (1, 2),
    (3, 4),
    (5, 6),
    (6, 7),
    (8, 9),
    (0, 5)  # Merge two components
]

for x, y in connections:
    if uf.union(x, y):
        print(f"Connected {x} and {y}")
    else:
        print(f"{x} and {y} already connected")
    print(f"  Components: {uf.count}")

print()
print(f"Final: {uf.count} disjoint components")
print(f"Parent array (after path compression): {[uf.find(i) for i in range(10)]}")
print()

# Test connectivity
queries = [(0, 7), (3, 4), (0, 3), (8, 9)]
print("Connectivity queries:")
for x, y in queries:
    print(f"  Are {x} and {y} connected? {uf.connected(x, y)}")
print()

# Show all components
components = uf.get_all_components()
print("All connected components:")
for root, members in components.items():
    print(f"  Component {root}: {members}")
print()


print("=" * 60)
print("Union-Find with Union by Size")
print("=" * 60)
print()


class UnionFindBySize:
    """
    Union-Find with union by size instead of rank.
    Tracks actual size of each component.
    """
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n  # Size of each component
        self.count = n
    
    def find(self, x):
        """Find with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by size."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Attach smaller tree to larger tree
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        
        self.count -= 1
        return True
    
    def get_size(self, x):
        """Get size of component containing x."""
        return self.size[self.find(x)]


print("Example: Tracking Component Sizes")
print()

uf_size = UnionFindBySize(8)

connections = [(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (0, 3)]

for x, y in connections:
    uf_size.union(x, y)
    print(f"Connected {x}-{y}: Size of component = {uf_size.get_size(x)}")

print()
print(f"Component sizes:")
for i in range(8):
    print(f"  Node {i}: component size = {uf_size.get_size(i)}")
print()


print("=" * 60)
print("Application: Cycle Detection")
print("=" * 60)
print()


def has_cycle(n, edges):
    """
    Detect cycle in undirected graph using Union-Find.
    
    Args:
        n: Number of nodes
        edges: List of [u, v] edges
    
    Returns:
        True if graph has cycle, False otherwise
    """
    uf = UnionFind(n)
    
    for u, v in edges:
        if not uf.union(u, v):
            # Already connected, adding this edge creates cycle
            return True
    
    return False


print("Cycle Detection in Graphs:")
print()

# Graph without cycle
edges1 = [[0, 1], [1, 2], [2, 3]]
print(f"Edges: {edges1}")
print(f"Has cycle: {has_cycle(4, edges1)}")
print()

# Graph with cycle
edges2 = [[0, 1], [1, 2], [2, 3], [3, 1]]
print(f"Edges: {edges2}")
print(f"Has cycle: {has_cycle(4, edges2)}")
print()


print("=" * 60)
print("Application: Count Connected Components")
print("=" * 60)
print()


def count_components(n, edges):
    """Count number of connected components in graph."""
    uf = UnionFind(n)
    
    for u, v in edges:
        uf.union(u, v)
    
    return uf.get_count()


print("Count Connected Components:")
print()

test_cases = [
    (5, [[0, 1], [1, 2], [3, 4]]),  # 2 components: {0,1,2} and {3,4}
    (5, [[0, 1], [1, 2], [2, 3], [3, 4]]),  # 1 component
    (6, [[0, 1], [1, 2], [3, 4]])  # 3 components: {0,1,2}, {3,4}, {5}
]

for n, edges in test_cases:
    result = count_components(n, edges)
    print(f"n={n}, edges={edges}")
    print(f"  Components: {result}")
    print()


print("=" * 60)
print("Comparison: With vs Without Optimizations")
print("=" * 60)
print()


class NaiveUnionFind:
    """Union-Find without any optimizations (for comparison)."""
    
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        """Simple find without path compression."""
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        """Simple union without rank."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y


print("Tree depth after operations:")
print()

# Create chain: 0 -> 1 -> 2 -> 3 -> 4
naive_uf = NaiveUnionFind(5)
optimized_uf = UnionFind(5)

for i in range(4):
    naive_uf.union(i, i + 1)
    optimized_uf.union(i, i + 1)

print("Naive (no optimizations):")
print(f"  Parent array: {naive_uf.parent}")

print("Optimized (path compression + union by rank):")
print(f"  Parent array after find(0): ", end="")
optimized_uf.find(0)
print([optimized_uf.find(i) for i in range(5)])

print()
print("Depth comparison:")
print("  Naive: Linear depth O(n)")
print("  Optimized: Nearly constant O(α(n)) ≈ O(1)")
print()


print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Key Points:")
print("  • Union-Find tracks disjoint sets efficiently")
print("  • Path compression flattens trees during find")
print("  • Union by rank/size keeps trees balanced")
print("  • Combined optimizations give O(α(n)) ≈ O(1) per operation")
print("  • Perfect for dynamic connectivity, cycle detection, MST")
print()
print("Operations:")
print("  • find(x): Find root of set containing x")
print("  • union(x, y): Merge sets containing x and y")
print("  • connected(x, y): Check if x and y in same set")
print()
print("Use Cases:")
print("  • Network connectivity")
print("  • Cycle detection in graphs")
print("  • Kruskal's MST algorithm")
print("  • Connected components counting")
print("  • Image segmentation")
