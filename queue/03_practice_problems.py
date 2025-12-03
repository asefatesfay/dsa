"""
Queue - Practice Problems
==========================
Common interview questions and LeetCode-style problems.
"""

from collections import deque
from typing import List, Optional
import heapq


# Problem 1: Implement Queue using Stacks (LeetCode #232)
class MyQueue:
    """
    Implement queue using two stacks.
    Push: O(1), Pop: O(1) amortized
    """
    def __init__(self):
        self.stack_in = []
        self.stack_out = []
    
    def push(self, x: int) -> None:
        """Push element to back of queue"""
        self.stack_in.append(x)
    
    def pop(self) -> int:
        """Remove element from front of queue"""
        self._move_elements()
        return self.stack_out.pop()
    
    def peek(self) -> int:
        """Get front element"""
        self._move_elements()
        return self.stack_out[-1]
    
    def empty(self) -> bool:
        """Check if empty"""
        return not self.stack_in and not self.stack_out
    
    def _move_elements(self):
        """Move elements from in to out stack if needed"""
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())

print("Problem 1: Queue using Stacks")
queue = MyQueue()
for val in [1, 2, 3]:
    queue.push(val)
    print(f"Pushed {val}")
print(f"Front: {queue.peek()}")
print(f"Popped: {queue.pop()}")
print(f"Front now: {queue.peek()}")
print()


# Problem 2: Number of Recent Calls (LeetCode #933)
class RecentCounter:
    """
    Count requests in last 3000ms.
    Time: O(1) amortized, Space: O(W) where W is window size
    """
    def __init__(self):
        self.queue = deque()
    
    def ping(self, t: int) -> int:
        """Add request at time t, return count in [t-3000, t]"""
        self.queue.append(t)
        
        # Remove requests outside window
        while self.queue and self.queue[0] < t - 3000:
            self.queue.popleft()
        
        return len(self.queue)

print("Problem 2: Recent Counter")
counter = RecentCounter()
for time in [1, 100, 3001, 3002]:
    count = counter.ping(time)
    print(f"Ping at {time}ms: {count} recent calls")
print()


# Problem 3: Design Circular Queue (LeetCode #622)
class MyCircularQueue:
    """
    Design circular queue with fixed size.
    All operations O(1)
    """
    def __init__(self, k: int):
        self.capacity = k
        self.data = [0] * k
        self.front = 0
        self.size = 0
    
    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        idx = (self.front + self.size) % self.capacity
        self.data[idx] = value
        self.size += 1
        return True
    
    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True
    
    def Front(self) -> int:
        return -1 if self.isEmpty() else self.data[self.front]
    
    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        idx = (self.front + self.size - 1) % self.capacity
        return self.data[idx]
    
    def isEmpty(self) -> bool:
        return self.size == 0
    
    def isFull(self) -> bool:
        return self.size == self.capacity

print("Problem 3: Circular Queue")
cq = MyCircularQueue(3)
print(f"Enqueue 1: {cq.enQueue(1)}")
print(f"Enqueue 2: {cq.enQueue(2)}")
print(f"Enqueue 3: {cq.enQueue(3)}")
print(f"Enqueue 4: {cq.enQueue(4)}")  # Should fail
print(f"Front: {cq.Front()}, Rear: {cq.Rear()}")
print(f"Dequeue: {cq.deQueue()}")
print(f"Enqueue 4: {cq.enQueue(4)}")
print(f"Rear: {cq.Rear()}")
print()


# Problem 4: Binary Tree Level Order Traversal (LeetCode #102)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Level order traversal of binary tree.
    Time: O(n), Space: O(w) where w is max width
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result

print("Problem 4: Binary Tree Level Order Traversal")
root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
print(f"Level order: {level_order(root)}")
print()


# Problem 5: Rotting Oranges (LeetCode #994)
def oranges_rotting(grid: List[List[int]]) -> int:
    """
    Time for all oranges to rot.
    Time: O(m*n), Space: O(m*n)
    """
    if not grid:
        return -1
    
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh_count += 1
    
    if fresh_count == 0:
        return 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    max_time = 0
    
    while queue:
        r, c, time = queue.popleft()
        max_time = max(max_time, time)
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh_count -= 1
                queue.append((nr, nc, time + 1))
    
    return max_time if fresh_count == 0 else -1

print("Problem 5: Rotting Oranges")
grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
print(f"Time: {oranges_rotting(grid)} minutes")
print()


# Problem 6: Perfect Squares (LeetCode #279)
def num_squares(n: int) -> int:
    """
    Find least number of perfect squares that sum to n.
    Time: O(n*sqrt(n)), Space: O(n)
    """
    if n < 2:
        return n
    
    squares = [i * i for i in range(1, int(n**0.5) + 1)]
    queue = deque([(n, 0)])
    visited = {n}
    
    while queue:
        remainder, steps = queue.popleft()
        
        for square in squares:
            if square > remainder:
                break
            
            if square == remainder:
                return steps + 1
            
            next_remainder = remainder - square
            if next_remainder not in visited:
                visited.add(next_remainder)
                queue.append((next_remainder, steps + 1))
    
    return -1

print("Problem 6: Perfect Squares")
for num in [12, 13]:
    print(f"Least squares for {num}: {num_squares(num)}")
print()


# Problem 7: Walls and Gates (LeetCode #286)
def walls_and_gates(rooms: List[List[int]]) -> None:
    """
    Fill each empty room with distance to nearest gate.
    Time: O(m*n), Space: O(m*n)
    """
    if not rooms:
        return
    
    rows, cols = len(rooms), len(rooms[0])
    INF = 2147483647
    queue = deque()
    
    # Find all gates
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))

print("Problem 7: Walls and Gates")
INF = 2147483647
rooms = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
walls_and_gates(rooms)
print("Distances:")
for row in rooms:
    print(row)
print()


# Problem 8: Shortest Bridge (LeetCode #934)
def shortest_bridge(grid: List[List[int]]) -> int:
    """
    Find shortest bridge between two islands.
    Time: O(n^2), Space: O(n^2)
    """
    n = len(grid)
    
    def dfs(r, c, queue):
        """Mark first island and add to queue"""
        if r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1:
            return
        
        grid[r][c] = 2
        queue.append((r, c, 0))
        
        dfs(r+1, c, queue)
        dfs(r-1, c, queue)
        dfs(r, c+1, queue)
        dfs(r, c-1, queue)
    
    # Find first island
    queue = deque()
    found = False
    for r in range(n):
        if found:
            break
        for c in range(n):
            if grid[r][c] == 1:
                dfs(r, c, queue)
                found = True
                break
    
    # BFS to second island
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while queue:
        r, c, dist = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == 1:
                    return dist
                if grid[nr][nc] == 0:
                    grid[nr][nc] = 2
                    queue.append((nr, nc, dist + 1))
    
    return -1

print("Problem 8: Shortest Bridge")
grid = [[0, 1], [1, 0]]
print(f"Shortest bridge: {shortest_bridge(grid)}")
print()


# Problem 9: Open the Lock (LeetCode #752)
def open_lock(deadends: List[str], target: str) -> int:
    """
    Find minimum turns to open lock avoiding deadends.
    Time: O(10^4), Space: O(10^4)
    """
    dead = set(deadends)
    if "0000" in dead:
        return -1
    
    queue = deque([("0000", 0)])
    visited = {"0000"}
    
    def neighbors(code):
        """Generate all possible next codes"""
        result = []
        for i in range(4):
            digit = int(code[i])
            for move in [-1, 1]:
                new_digit = (digit + move) % 10
                new_code = code[:i] + str(new_digit) + code[i+1:]
                result.append(new_code)
        return result
    
    while queue:
        code, turns = queue.popleft()
        
        if code == target:
            return turns
        
        for next_code in neighbors(code):
            if next_code not in visited and next_code not in dead:
                visited.add(next_code)
                queue.append((next_code, turns + 1))
    
    return -1

print("Problem 9: Open the Lock")
deadends = ["0201", "0101", "0102", "1212", "2002"]
target = "0202"
print(f"Minimum turns: {open_lock(deadends, target)}")
print()


# Problem 10: Jump Game IV (LeetCode #1345)
def min_jumps(arr: List[int]) -> int:
    """
    Minimum jumps to reach last index.
    Time: O(n), Space: O(n)
    """
    if len(arr) <= 1:
        return 0
    
    n = len(arr)
    graph = {}
    for i, val in enumerate(arr):
        graph.setdefault(val, []).append(i)
    
    queue = deque([(0, 0)])  # (index, steps)
    visited = {0}
    
    while queue:
        idx, steps = queue.popleft()
        
        if idx == n - 1:
            return steps
        
        # Check all positions with same value
        for next_idx in graph[arr[idx]]:
            if next_idx not in visited:
                visited.add(next_idx)
                queue.append((next_idx, steps + 1))
        
        # Clear to avoid revisiting
        graph[arr[idx]].clear()
        
        # Check adjacent positions
        for next_idx in [idx - 1, idx + 1]:
            if 0 <= next_idx < n and next_idx not in visited:
                visited.add(next_idx)
                queue.append((next_idx, steps + 1))
    
    return -1

print("Problem 10: Jump Game IV")
arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
print(f"Array: {arr}")
print(f"Minimum jumps: {min_jumps(arr)}")
