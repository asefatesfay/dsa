# Union-Find (Disjoint Set Union)

Union-Find data structure for tracking disjoint sets and connectivity.

## Overview

Union-Find (also called Disjoint Set Union or DSU) is a data structure that efficiently tracks elements partitioned into disjoint (non-overlapping) sets. It's essential for graph connectivity, cycle detection, and dynamic connectivity problems.

## Contents

### 01_basics.py
- Basic union-find implementation
- Find operation (with path compression)
- Union operation (with union by rank/size)
- Connected components tracking
- Basic operations and complexity

### 02_common_patterns.py
- Cycle detection in graphs
- Connected components
- Minimum spanning tree (Kruskal's)
- Dynamic connectivity
- Union-find with rollback
- Weighted union-find

### 03_leetcode_problems.py
- Number of Connected Components (LC 323)
- Graph Valid Tree (LC 261)
- Redundant Connection (LC 684)
- Redundant Connection II (LC 685)
- Accounts Merge (LC 721)
- Most Stones Removed (LC 947)
- Smallest String With Swaps (LC 1202)
- Satisfiability of Equality Equations (LC 990)
- Number of Operations to Make Network Connected (LC 1319)
- Minimize Malware Spread (LC 924)

## Key Concepts

### Operations
- **Find(x)**: Find which set x belongs to
- **Union(x, y)**: Merge the sets containing x and y
- **Connected(x, y)**: Check if x and y are in same set

### Time Complexity
- Without optimization: O(n) per operation
- With path compression: O(log n) per operation
- With path compression + union by rank: O(α(n)) ≈ O(1)
  - α(n) is inverse Ackermann function (effectively constant)

### Space Complexity
- O(n) where n is number of elements

## Optimizations

### 1. Path Compression
During find, make nodes point directly to root.

```python
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])  # Path compression
    return self.parent[x]
```

### 2. Union by Rank
Attach smaller tree under root of larger tree.

```python
def union(self, x, y):
    root_x, root_y = self.find(x), self.find(y)
    if root_x == root_y:
        return False
    
    if self.rank[root_x] < self.rank[root_y]:
        self.parent[root_x] = root_y
    elif self.rank[root_x] > self.rank[root_y]:
        self.parent[root_y] = root_x
    else:
        self.parent[root_y] = root_x
        self.rank[root_x] += 1
    return True
```

### 3. Union by Size
Similar to union by rank, but track actual tree size.

## Common Use Cases

1. **Dynamic Connectivity**: Check if two nodes are connected
2. **Cycle Detection**: Detect cycles in undirected graphs
3. **MST**: Kruskal's algorithm for minimum spanning tree
4. **Connected Components**: Count disjoint components
5. **Network Connectivity**: Track network connections
6. **Image Processing**: Find connected regions
7. **Social Networks**: Friend circles, group detection

## Implementation Patterns

### Basic Template
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.count -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

## Common Problems

### Detect Cycle
If union returns False (already connected), there's a cycle.

### Count Components
Track `count` variable, decrement on successful union.

### Minimum Spanning Tree
Sort edges by weight, use union-find to avoid cycles (Kruskal's).

### Dynamic Graph
Add edges dynamically, query connectivity in O(α(n)).

## Interview Tips

- Always implement path compression
- Choose union by rank or size (both work)
- Track component count if needed
- For graphs, nodes often need mapping to [0, n-1]
- Can extend with weights for weighted union-find
- Consider if problem needs connectivity queries
- Union-find doesn't support disconnection (use timestamps/versions)

## Real-World Applications

- **Network Connectivity**: Check if servers are connected
- **Percolation Theory**: Does water flow through?
- **Image Segmentation**: Find connected pixels
- **Social Networks**: Friend recommendations
- **Compiler Optimization**: Register allocation
- **Game Development**: Terrain generation, region detection
