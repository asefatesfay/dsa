"""
NeetCode 150 - Advanced Graphs
===============================
MST, shortest paths, advanced algorithms (6 problems).
"""

import heapq
from collections import defaultdict


# PATTERN: Prim's Algorithm (MST)
def min_cost_connect_points(points):
    """
    Min Cost to Connect All Points - Minimum Spanning Tree.
    
    Pattern: Prim's algorithm with min heap
    
    Algorithm Steps:
    1. Start from any point
    2. Use min heap to track edges to unvisited points
    3. Greedily add minimum edge that connects new point
    4. Continue until all points connected
    
    Time: O(n^2 log n), Space: O(n^2)
    """
    n = len(points)
    visited = set()
    min_heap = [(0, 0)]  # (cost, point_index)
    total_cost = 0
    
    while len(visited) < n:
        cost, i = heapq.heappop(min_heap)
        
        if i in visited:
            continue
        
        visited.add(i)
        total_cost += cost
        
        # Add edges to unvisited neighbors
        for j in range(n):
            if j not in visited:
                dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                heapq.heappush(min_heap, (dist, j))
    
    return total_cost


# PATTERN: Dijkstra's Algorithm
def network_delay_time(times, n, k):
    """
    Network Delay Time - shortest path to all nodes.
    
    Pattern: Dijkstra's algorithm
    
    Time: O(E log V), Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    min_heap = [(0, k)]  # (time, node)
    visited = set()
    max_time = 0
    
    while min_heap:
        time, node = heapq.heappop(min_heap)
        
        if node in visited:
            continue
        
        visited.add(node)
        max_time = max(max_time, time)
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (time + weight, neighbor))
    
    return max_time if len(visited) == n else -1


# PATTERN: Bellman-Ford (Negative Weights)
def cheapest_flights_within_k_stops(n, flights, src, dst, k):
    """
    Cheapest Flights Within K Stops.
    
    Pattern: Modified Bellman-Ford / BFS with K layers
    
    Time: O(K * E), Space: O(V)
    """
    prices = [float('inf')] * n
    prices[src] = 0
    
    for _ in range(k + 1):
        temp_prices = prices[:]
        
        for u, v, price in flights:
            if prices[u] != float('inf'):
                temp_prices[v] = min(temp_prices[v], prices[u] + price)
        
        prices = temp_prices
    
    return prices[dst] if prices[dst] != float('inf') else -1


# PATTERN: Tarjan's Algorithm (Strongly Connected Components)
def min_vertices_to_reach_all(n, edges):
    """
    Minimum Number of Vertices to Reach All Nodes.
    
    Pattern: Find nodes with no incoming edges
    
    Time: O(V + E), Space: O(V)
    """
    has_incoming = set()
    for u, v in edges:
        has_incoming.add(v)
    
    return [i for i in range(n) if i not in has_incoming]


# PATTERN: Topological Sort + DP
def min_height_trees(n, edges):
    """
    Minimum Height Trees - find tree centers.
    
    Pattern: Trim leaves layer by layer (like topological sort)
    
    Algorithm Steps:
    1. Start from leaf nodes (degree 1)
    2. Remove leaves layer by layer
    3. Last remaining nodes are centers
    
    Time: O(V), Space: O(V)
    """
    if n <= 2:
        return list(range(n))
    
    from collections import deque
    
    # Build adjacency list
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    
    # Find initial leaves
    leaves = deque([i for i in range(n) if len(graph[i]) == 1])
    
    remaining = n
    while remaining > 2:
        leaf_count = len(leaves)
        remaining -= leaf_count
        
        for _ in range(leaf_count):
            leaf = leaves.popleft()
            neighbor = graph[leaf].pop()
            graph[neighbor].remove(leaf)
            
            if len(graph[neighbor]) == 1:
                leaves.append(neighbor)
    
    return list(leaves)


# PATTERN: Union Find with Path Compression
def accounts_merge(accounts):
    """
    Accounts Merge - merge accounts with common emails.
    
    Pattern: Union-Find on emails
    
    Time: O(N * K * α(N)) where K = max emails per account
    Space: O(N * K)
    """
    from collections import defaultdict
    
    email_to_name = {}
    parent = {}
    
    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Build union-find
    for account in accounts:
        name = account[0]
        first_email = account[1]
        
        for email in account[1:]:
            email_to_name[email] = name
            union(email, first_email)
    
    # Group emails by root
    groups = defaultdict(list)
    for email in email_to_name:
        groups[find(email)].append(email)
    
    # Build result
    result = []
    for emails in groups.values():
        result.append([email_to_name[emails[0]]] + sorted(emails))
    
    return result


if __name__ == "__main__":
    print("=== NeetCode 150 - Advanced Graphs ===\n")
    
    print("Test 1: Min Cost to Connect Points")
    points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
    print(f"Min cost: {min_cost_connect_points(points)}")
    
    print("\nTest 2: Network Delay Time")
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    print(f"Network delay: {network_delay_time(times, 4, 2)}")
    
    print("\nTest 3: Cheapest Flights Within K Stops")
    flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    print(f"Cheapest price: {cheapest_flights_within_k_stops(3, flights, 0, 2, 1)}")
    
    print("\nTest 4: Minimum Height Trees")
    edges = [[1, 0], [1, 2], [1, 3]]
    print(f"MHT roots: {min_height_trees(4, edges)}")
