"""
Union-Find - LeetCode Problems
===============================
Common union-find interview problems from LeetCode.
"""

from typing import List
from collections import defaultdict


class UnionFind:
    """Standard Union-Find with path compression and union by rank."""
    
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


print("=" * 60)
print("Problem 1: Number of Connected Components (LeetCode 323)")
print("=" * 60)
print()

def count_components(n: int, edges: List[List[int]]) -> int:
    """
    Count connected components in undirected graph.
    
    Time: O(E * α(n)), Space: O(n)
    """
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count

print("Number of Connected Components:")
test_cases = [
    (5, [[0,1],[1,2],[3,4]], 2),
    (5, [[0,1],[1,2],[2,3],[3,4]], 1)
]
for n, edges, expected in test_cases:
    result = count_components(n, edges)
    status = "✓" if result == expected else "✗"
    print(f"  {status} n={n}, edges={edges} -> {result} components")
print()


print("=" * 60)
print("Problem 2: Graph Valid Tree (LeetCode 261)")
print("=" * 60)
print()

def valid_tree(n: int, edges: List[List[int]]) -> bool:
    """
    Check if edges form a valid tree.
    Valid tree: n-1 edges, no cycles, connected.
    
    Time: O(E * α(n)), Space: O(n)
    """
    if len(edges) != n - 1:
        return False
    
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return False  # Cycle detected
    
    return uf.count == 1  # Must be fully connected

print("Graph Valid Tree:")
test_cases = [
    (5, [[0,1],[0,2],[0,3],[1,4]], True),
    (5, [[0,1],[1,2],[2,3],[1,3],[1,4]], False)  # Has cycle
]
for n, edges, expected in test_cases:
    result = valid_tree(n, edges)
    status = "✓" if result == expected else "✗"
    print(f"  {status} n={n}, {len(edges)} edges -> {result}")
print()


print("=" * 60)
print("Problem 3: Redundant Connection (LeetCode 684)")
print("=" * 60)
print()

def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """
    Find edge that creates cycle (return last one).
    
    Time: O(E * α(n)), Space: O(n)
    """
    uf = UnionFind(len(edges) + 1)
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]  # This edge creates cycle
    
    return []

print("Redundant Connection:")
test_cases = [
    [[1,2],[1,3],[2,3]],
    [[1,2],[2,3],[3,4],[1,4],[1,5]]
]
for edges in test_cases:
    result = find_redundant_connection(edges)
    print(f"  {edges}")
    print(f"  -> Redundant: {result}")
print()


print("=" * 60)
print("Problem 4: Accounts Merge (LeetCode 721)")
print("=" * 60)
print()

def accounts_merge(accounts: List[List[str]]) -> List[List[str]]:
    """
    Merge accounts with common emails.
    
    Time: O(N * K * α(N)) where N=accounts, K=emails
    Space: O(N * K)
    """
    email_to_id = {}
    email_to_name = {}
    uf = UnionFind(len(accounts))
    
    # Map emails to account IDs
    for i, account in enumerate(accounts):
        name = account[0]
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            else:
                email_to_id[email] = i
            email_to_name[email] = name
    
    # Group emails by root account
    components = defaultdict(list)
    for email, acc_id in email_to_id.items():
        root = uf.find(acc_id)
        components[root].append(email)
    
    # Build result
    result = []
    for acc_id, emails in components.items():
        name = accounts[acc_id][0]
        result.append([name] + sorted(emails))
    
    return result

print("Accounts Merge:")
accounts = [
    ["John","johnsmith@mail.com","john_newyork@mail.com"],
    ["John","johnsmith@mail.com","john00@mail.com"],
    ["Mary","mary@mail.com"],
    ["John","johnnybravo@mail.com"]
]
result = accounts_merge(accounts)
for account in result:
    print(f"  {account}")
print()


print("=" * 60)
print("Problem 5: Most Stones Removed (LeetCode 947)")
print("=" * 60)
print()

def remove_stones(stones: List[List[int]]) -> int:
    """
    Maximum stones that can be removed.
    Can remove stone if shares row/column with another.
    
    Time: O(N * α(N)), Space: O(N)
    """
    uf = UnionFind(20002)  # Max coordinates
    
    for x, y in stones:
        uf.union(x, y + 10001)  # Offset y to avoid collision
    
    # Count unique components with stones
    unique_roots = len({uf.find(x) for x, y in stones})
    
    return len(stones) - unique_roots

print("Most Stones Removed:")
test_cases = [
    [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]],
    [[0,0],[0,2],[1,1],[2,0],[2,2]]
]
for stones in test_cases:
    result = remove_stones(stones)
    print(f"  {len(stones)} stones -> can remove {result}")
print()


print("=" * 60)
print("Problem 6: Smallest String With Swaps (LeetCode 1202)")
print("=" * 60)
print()

def smallest_string_with_swaps(s: str, pairs: List[List[int]]) -> str:
    """
    Get lexicographically smallest string after unlimited swaps.
    
    Time: O(N log N + E * α(N)), Space: O(N)
    """
    n = len(s)
    uf = UnionFind(n)
    
    # Union indices that can be swapped
    for a, b in pairs:
        uf.union(a, b)
    
    # Group indices by component
    components = defaultdict(list)
    for i in range(n):
        root = uf.find(i)
        components[root].append(i)
    
    # Sort characters in each component
    result = list(s)
    for indices in components.values():
        chars = sorted([s[i] for i in indices])
        for i, char in zip(sorted(indices), chars):
            result[i] = char
    
    return ''.join(result)

print("Smallest String With Swaps:")
test_cases = [
    ("dcab", [[0,3],[1,2]], "bacd"),
    ("dcab", [[0,3],[1,2],[0,2]], "abcd")
]
for s, pairs, expected in test_cases:
    result = smallest_string_with_swaps(s, pairs)
    status = "✓" if result == expected else "✗"
    print(f"  {status} '{s}' with swaps {pairs}")
    print(f"     -> '{result}'")
print()


print("=" * 60)
print("Problem 7: Satisfiability of Equality Equations (LeetCode 990)")
print("=" * 60)
print()

def equations_possible(equations: List[str]) -> bool:
    """
    Check if equations can be satisfied.
    
    Time: O(N * α(26)), Space: O(1)
    """
    uf = UnionFind(26)  # 26 letters
    
    # Process equality first
    for eq in equations:
        if eq[1] == '=':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            uf.union(x, y)
    
    # Check inequalities
    for eq in equations:
        if eq[1] == '!':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            if uf.connected(x, y):
                return False
    
    return True

print("Satisfiability of Equality Equations:")
test_cases = [
    (["a==b","b!=a"], False),
    (["b==a","a==b"], True),
    (["a==b","b==c","a==c"], True),
    (["a==b","b!=c","c==a"], False)
]
for equations, expected in test_cases:
    result = equations_possible(equations)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {equations} -> {result}")
print()


print("=" * 60)
print("Problem 8: Number of Operations to Make Network Connected (LC 1319)")
print("=" * 60)
print()

def make_connected(n: int, connections: List[List[int]]) -> int:
    """
    Minimum operations to connect network.
    Can remove edge and add elsewhere.
    
    Time: O(E * α(n)), Space: O(n)
    """
    if len(connections) < n - 1:
        return -1  # Not enough cables
    
    uf = UnionFind(n)
    redundant = 0
    
    for u, v in connections:
        if not uf.union(u, v):
            redundant += 1
    
    components = uf.count
    needed = components - 1
    
    return needed if redundant >= needed else -1

print("Operations to Make Network Connected:")
test_cases = [
    (4, [[0,1],[0,2],[1,2]], 1),
    (6, [[0,1],[0,2],[0,3],[1,2],[1,3]], 2),
    (6, [[0,1],[0,2],[0,3],[1,2]], -1)
]
for n, connections, expected in test_cases:
    result = make_connected(n, connections)
    status = "✓" if result == expected else "✗"
    print(f"  {status} n={n}, {len(connections)} connections -> {result} ops")
print()


print("=" * 60)
print("Problem 9: Minimize Malware Spread (LeetCode 924)")
print("=" * 60)
print()

def min_malware_spread(graph: List[List[int]], initial: List[int]) -> int:
    """
    Find node to remove that minimizes malware spread.
    
    Time: O(N²), Space: O(N)
    """
    n = len(graph)
    uf = UnionFind(n)
    
    # Build union-find ignoring initial infected
    for i in range(n):
        if i in initial:
            continue
        for j in range(i + 1, n):
            if j not in initial and graph[i][j] == 1:
                uf.union(i, j)
    
    # Count infected per component
    count = defaultdict(int)
    for node in initial:
        for i in range(n):
            if graph[node][i] == 1 and i not in initial:
                root = uf.find(i)
                count[root] += 1
    
    # Find best node to remove
    best_node = min(initial)
    max_saved = 0
    
    for node in initial:
        saved = 0
        for i in range(n):
            if graph[node][i] == 1 and i not in initial:
                root = uf.find(i)
                if count[root] == 1:  # Only this node infects component
                    saved += uf.count
        
        if saved > max_saved or (saved == max_saved and node < best_node):
            max_saved = saved
            best_node = node
    
    return best_node

print("Minimize Malware Spread:")
graph = [
    [1,1,0],
    [1,1,0],
    [0,0,1]
]
initial = [0, 1]
result = min_malware_spread(graph, initial)
print(f"  Graph: {len(graph)}x{len(graph)}, infected: {initial}")
print(f"  Remove node: {result}")
print()


print("=" * 60)
print("Problem 10: Swim in Rising Water (LeetCode 778)")
print("=" * 60)
print()

def swim_in_water(grid: List[List[int]]) -> int:
    """
    Minimum time to swim from top-left to bottom-right.
    
    Time: O(N² log N²), Space: O(N²)
    """
    n = len(grid)
    # Binary search on answer
    left, right = grid[0][0], n * n - 1
    
    def can_swim(T):
        uf = UnionFind(n * n)
        for i in range(n):
            for j in range(n):
                if grid[i][j] > T:
                    continue
                idx = i * n + j
                # Connect to neighbors
                for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] <= T:
                        uf.union(idx, ni * n + nj)
        
        return uf.connected(0, n * n - 1)
    
    while left < right:
        mid = (left + right) // 2
        if can_swim(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

print("Swim in Rising Water:")
grids = [
    [[0,2],[1,3]],
    [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
]
for grid in grids:
    result = swim_in_water(grid)
    print(f"  {len(grid)}x{len(grid)} grid -> time: {result}")
print()


print("=" * 60)
print("Union-Find Problems Summary")
print("=" * 60)
print()
print("Key Patterns:")
print("  1. Connected Components: Count disjoint sets")
print("  2. Cycle Detection: Check if union fails")
print("  3. Graph Validation: Tree has n-1 edges, no cycles")
print("  4. Grouping: Merge by common property")
print("  5. Network: Connectivity and redundancy")
print()
print("Common Variations:")
print("  • Basic union-find: Standard implementation")
print("  • With size tracking: Know component sizes")
print("  • With mapping: Nodes aren't 0 to n-1")
print("  • Grid problems: Convert 2D to 1D index")
print("  • String problems: Use character/index mapping")
print()
print("Interview Tips:")
print("  • Always use path compression + union by rank")
print("  • Track count for component counting")
print("  • Map non-numeric IDs to indices")
print("  • Consider if problem needs connectivity")
print("  • Union-find doesn't support disconnection")
