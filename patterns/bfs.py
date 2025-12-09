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

# --- Number of Islands ---
def num_islands(grid):
    """
    Count connected components of '1's in a grid using BFS.

    Steps:
    - Traverse all cells; when hitting an unvisited '1', start a BFS to mark its region.
    - BFS uses a queue and explores 4-direction neighbors.
    - Increment islands count per BFS start.
    """
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    visited = [[False]*C for _ in range(R)]
    from collections import deque
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1' and not visited[r][c]:
                count += 1
                q = deque([(r,c)])
                visited[r][c] = True
                while q:
                    x,y = q.popleft()
                    for dx,dy in dirs:
                        nx,ny = x+dx, y+dy
                        if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == '1' and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx,ny))
    return count

# --- Shortest Path in Binary Matrix ---
def shortest_path_in_binary_matrix(grid):
    """
    Find shortest path from (0,0) to (R-1,C-1) moving in 8 directions through 0-cells.
    Uses BFS with distance levels.
    """
    if not grid or not grid[0]:
        return -1
    R, C = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[R-1][C-1] == 1:
        return -1
    from collections import deque
    q = deque([(0,0,1)])
    grid[0][0] = 1  # mark visited by setting to 1
    dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    while q:
        x,y,d = q.popleft()
        if x == R-1 and y == C-1:
            return d
        for dx,dy in dirs:
            nx,ny = x+dx, y+dy
            if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == 0:
                grid[nx][ny] = 1
                q.append((nx,ny,d+1))
    return -1

# --- Rotting Oranges ---
def rotting_oranges(grid):
    """
    Multi-source BFS: each minute, fresh oranges adjacent to rotten become rotten.
    Return minutes needed to rot all, or -1 if impossible.
    """
    from collections import deque
    R = len(grid)
    C = len(grid[0]) if R else 0
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r,c,0))
            elif grid[r][c] == 1:
                fresh += 1
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    minutes = 0
    while q:
        x,y,t = q.popleft()
        minutes = max(minutes, t)
        for dx,dy in dirs:
            nx,ny = x+dx, y+dy
            if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == 1:
                grid[nx][ny] = 2
                fresh -= 1
                q.append((nx,ny,t+1))
    return minutes if fresh == 0 else -1

if __name__ == "__main__":
    grid_islands = [
        ['1','1','0','0'],
        ['1','0','0','1'],
        ['0','0','1','1'],
        ['0','0','0','0'],
    ]
    print("num_islands:", num_islands(grid_islands))

    grid_sp = [
        [0,1,0],
        [0,0,0],
        [1,0,0],
    ]
    print("shortest_path_in_binary_matrix:", shortest_path_in_binary_matrix([row[:] for row in grid_sp]))

    oranges = [
        [2,1,1],
        [1,1,0],
        [0,1,1],
    ]
    print("rotting_oranges:", rotting_oranges(oranges))
