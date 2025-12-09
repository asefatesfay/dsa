"""
Topological Sort / DAG DP
=========================
Dynamic programming on DAGs by processing nodes in topological order.
"""

from collections import deque, defaultdict


def topo_order(n, edges):
    """
    Return a topological ordering for DAG with n nodes [0..n-1].
    """
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != n:
        raise ValueError("Graph is not a DAG")
    return order


def longest_path_dag(n, edges, weights=None):
    """
    Longest path length in DAG (unweighted -> max edges; weighted -> max sum).
    If weights is None, counts edges; else weights[u] is node weight or edge weight via dict.
    """
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    order = topo_order(n, edges)
    dp = [-10**9] * n
    for i in range(n):
        if indeg[i] == 0:
            dp[i] = 0 if weights is None else (weights[i] if isinstance(weights, list) else 0)
    for u in order:
        for v in adj[u]:
            gain = 1 if weights is None else (weights[v] if isinstance(weights, list) else weights.get((u,v), 0))
            dp[v] = max(dp[v], dp[u] + gain)
    return max(dp)


def task_schedule_min_time(n, edges, duration):
    """
    Each task i takes duration[i], edges are prerequisites (u -> v means u before v).
    Compute earliest finish time using DAG DP.
    """
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    order = topo_order(n, edges)
    finish = [0] * n
    for u in order:
        start_u = finish[u]  # already includes its duration if sources set below
        for v in adj[u]:
            finish[v] = max(finish[v], finish[u])
        if indeg[u] == 0:
            finish[u] = duration[u]
        else:
            finish[u] += duration[u]
    return max(finish)


if __name__ == "__main__":
    print("topo:", topo_order(4, [(0,1),(0,2),(1,3),(2,3)]))
    print("longest path (edges):", longest_path_dag(4, [(0,1),(0,2),(1,3),(2,3)]))
    dur = [3,2,4,1]
    print("schedule time:", task_schedule_min_time(4, [(0,1),(0,2),(1,3),(2,3)], dur))

# =====================
# Additional DAG / Toposort DP Problems
# =====================

def course_schedule_order(n, prerequisites):
    """
    Return one valid order to finish all courses or [] if impossible.
    """
    try:
        order = topo_order(n, prerequisites)
        return order
    except ValueError:
        return []


def count_paths_dag(n, edges, start, end):
    """
    Count number of distinct paths from start to end in DAG via DP in topo order.
    """
    from collections import defaultdict
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
    order = topo_order(n, edges)
    ways = [0] * n
    ways[start] = 1
    for u in order:
        for v in adj[u]:
            ways[v] += ways[u]
    return ways[end]


if __name__ == "__main__":
    print("course order:", course_schedule_order(4, [(0,1),(0,2),(1,3),(2,3)]))
    print("path count:", count_paths_dag(4, [(0,1),(0,2),(1,3),(2,3)], 0, 3))  # 2 paths
