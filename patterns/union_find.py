"""
Union-Find (Disjoint Set Union)
================================
Data structure to track connectivity with near-constant time unions/finds.
"""


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # connected components

    def find(self, x):
        """Path compression find"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        """Union by rank"""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        self.count -= 1
        return True


def count_components(n, edges):
    """
    Count connected components in an undirected graph with n nodes.
    """
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count


def kruskal_mst(n, edges):
    """
    Kruskal's algorithm using DSU.
    edges: list of (w, u, v)
    Returns total weight of MST.
    """
    dsu = DSU(n)
    total = 0
    for w, u, v in sorted(edges):
        if dsu.union(u, v):
            total += w
    # If graph isn't connected, this returns a forest weight.
    return total


if __name__ == "__main__":
    print("components:", count_components(5, [(0,1),(1,2),(3,4)]))  # 2
    print("mst:", kruskal_mst(4, [(1,0,1),(4,1,2),(3,2,3),(2,0,2)]))
