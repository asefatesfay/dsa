"""
Breadth-First Search (BFS)
==========================
Level-order traversal using a queue. Great for shortest paths on unweighted graphs.
"""

from collections import deque


def level_order_tree(root):
    """
    Return level order traversal of a binary tree.
    """
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res


def shortest_path_unweighted(adj, start, end):
    """
    BFS to compute shortest path length and path on an unweighted graph.
    Returns (dist, path) or (-1, []).
    """
    q = deque([start])
    parent = {start: None}
    while q:
        v = q.popleft()
        if v == end:
            break
        for nbr in adj.get(v, []):
            if nbr not in parent:
                parent[nbr] = v
                q.append(nbr)
    if end not in parent:
        return -1, []
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return len(path) - 1, path


if __name__ == "__main__":
    adj = {0:[1,2],1:[3],2:[3],3:[]}
    print(shortest_path_unweighted(adj, 0, 3))
