"""
Queue - Common Operations and Patterns
=======================================
Essential operations and patterns used in queue problems.
"""

from collections import deque
from typing import List, Optional


class Queue:
    """Simple queue implementation using deque for examples"""
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


# Pattern 1: Generate Binary Numbers
def generate_binary_numbers(n: int) -> List[str]:
    """
    Generate binary numbers from 1 to n using queue.
    Time: O(n), Space: O(n)
    
    Example:
        Input: n = 5
        Output: ['1', '10', '11', '100', '101']
        Explanation: First 5 binary numbers are 1, 10, 11, 100, 101
    """
    result = []
    queue = Queue()
    queue.enqueue("1")
    
    for _ in range(n):
        binary = queue.dequeue()
        result.append(binary)
        
        # Generate next numbers by appending 0 and 1
        queue.enqueue(binary + "0")
        queue.enqueue(binary + "1")
    
    return result

print("=" * 60)
print("Pattern 1: Generate Binary Numbers")
print("=" * 60)
print("Problem: Generate first n binary numbers using queue")
print("\nHow it works:")
print("  1. Start with '1' in queue")
print("  2. For each number, dequeue it and add to result")
print("  3. Generate next numbers by appending '0' and '1'")
print("  4. Example: '1' generates '10' and '11'")
print("            '10' generates '100' and '101'")
print("\nExample:")
print(f"  Input: n = 5")
result = generate_binary_numbers(5)
print(f"  Output: {result}")
print(f"  Explanation: Each number creates two children (add 0, add 1)")
print()


# Pattern 2: First Non-Repeating Character in Stream
class FirstNonRepeating:
    """
    Find first non-repeating character in a stream.
    Time: O(1) per character, Space: O(26) = O(1)
    
    Example:
        Stream: a, a, b, c
        Output: a, #, b, b
        After 'a': first non-repeating = 'a'
        After 'a': first non-repeating = '#' (all repeat)
        After 'b': first non-repeating = 'b'
        After 'c': first non-repeating = 'b'
    """
    def __init__(self):
        self.queue = deque()
        self.char_count = {}
    
    def add_char(self, char: str) -> str:
        """Add character and return first non-repeating"""
        # Update count
        self.char_count[char] = self.char_count.get(char, 0) + 1
        self.queue.append(char)
        
        # Remove repeating characters from front
        while self.queue and self.char_count[self.queue[0]] > 1:
            self.queue.popleft()
        
        return self.queue[0] if self.queue else '#'

print("=" * 60)
print("Pattern 2: First Non-Repeating Character in Stream")
print("=" * 60)
print("Problem: Find first non-repeating character as characters arrive")
print("\nHow it works:")
print("  1. Keep a queue of characters in order they arrived")
print("  2. Keep a count of how many times each char appears")
print("  3. When adding new char: update count and add to queue")
print("  4. Remove chars from front of queue if they repeat")
print("  5. Front of queue is always first non-repeating char")
print("\nExample:")
print("  Input stream: 'a', 'a', 'b', 'c', 'c', 'x', 'b'")
print("  Output:")
stream = FirstNonRepeating()
for char in "aabccxb":
    result = stream.add_char(char)
    print(f"    After '{char}': first non-repeating = '{result}'")
print()


# Pattern 3: Implement Stack using Queues
class StackUsingQueues:
    """
    Implement stack using one queue.
    Push: O(n), Pop: O(1)
    
    Example:
        Operations: push(1), push(2), push(3), pop(), top()
        Output: 3, 2
        Explanation: Stack follows LIFO, last pushed (3) is first out
    """
    def __init__(self):
        self.queue = deque()
    
    def push(self, x: int) -> None:
        """Push element (expensive operation)"""
        self.queue.append(x)
        # Rotate queue to make new element front
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())
    
    def pop(self) -> int:
        """Pop element from top"""
        return self.queue.popleft()
    
    def top(self) -> int:
        """Get top element"""
        return self.queue[0]
    
    def empty(self) -> bool:
        """Check if empty"""
        return len(self.queue) == 0

print("=" * 60)
print("Pattern 3: Implement Stack using Queues")
print("=" * 60)
print("Problem: Implement LIFO stack using FIFO queue")
print("\nHow it works:")
print("  1. When pushing: add element to back of queue")
print("  2. Then rotate: move all previous elements to back")
print("  3. Result: newest element is now at front")
print("  4. Example: queue [1,2] + push(3)")
print("            -> [1,2,3] -> rotate -> [3,1,2]")
print("  5. Pop/top operations are now O(1) from front")
print("\nExample:")
print("  Operations: push(1), push(2), push(3), top(), pop(), top()")
stack = StackUsingQueues()
operations = []
for val in [1, 2, 3]:
    stack.push(val)
    operations.append(f"push({val})")
operations.append(f"top() -> {stack.top()}")
operations.append(f"pop() -> {stack.pop()}")
operations.append(f"top() -> {stack.top()}")
print("  Output:", ", ".join(operations))
print()


# Pattern 4: Sliding Window Maximum using Deque
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Find maximum in each sliding window of size k.
    Time: O(n), Space: O(k)
    Uses monotonic decreasing deque
    
    Example:
        Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
        Output: [3,3,5,5,6,7]
        Explanation: 
        Window [1,3,-1] -> max = 3
        Window [3,-1,-3] -> max = 3
        Window [-1,-3,5] -> max = 5
        Window [-3,5,3] -> max = 5
        Window [5,3,6] -> max = 6
        Window [3,6,7] -> max = 7
    """
    if not nums or k == 0:
        return []
    
    result = []
    dq = deque()  # Stores indices
    
    for i in range(len(nums)):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (maintain decreasing order)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result after first window
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

print("=" * 60)
print("Pattern 4: Sliding Window Maximum (Monotonic Deque)")
print("=" * 60)
print("Problem: Find maximum in each window of size k")
print("\nHow it works:")
print("  1. Use deque to store indices (not values)")
print("  2. Keep deque in decreasing order of values")
print("  3. Remove indices outside current window from front")
print("  4. Remove smaller elements from back (they can't be max)")
print("  5. Front of deque always has index of maximum")
print("  6. Why? Larger elements block smaller ones from being max")
print("\nExample:")
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(f"  Input: nums = {nums}, k = {k}")
result = max_sliding_window(nums, k)
print(f"  Output: {result}")
print("  Windows:")
windows = [[1,3,-1], [3,-1,-3], [-1,-3,5], [-3,5,3], [5,3,6], [3,6,7]]
for i, window in enumerate(windows):
    print(f"    {window} -> max = {result[i]}")
print()


# Pattern 5: Level Order Traversal (BFS on Tree)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
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

print("=" * 60)
print("Pattern 5: Level Order Traversal (BFS)")
print("=" * 60)
print("Problem: Traverse binary tree level by level")
print("\nHow it works:")
print("  1. Start with root in queue")
print("  2. For each level: count how many nodes in queue")
print("  3. Process exactly that many nodes (one level)")
print("  4. While processing: add their children to queue")
print("  5. Children go to back, so they're processed in next level")
print("  6. This ensures level-by-level processing")
print("\nExample:")
print("  Input tree:")
print("       1")
print("      / \\")
print("     2   3")
print("    / \\ /")
print("   4  5 6")
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(6)
result = level_order_traversal(root)
print(f"  Output: {result}")
print("  Process: [1] -> [2,3] -> [4,5,6]")
print()


# Pattern 6: Time Taken to Rot Oranges
def oranges_rotting(grid: List[List[int]]) -> int:
    """
    Find time for all oranges to rot (multi-source BFS).
    Time: O(m*n), Space: O(m*n)
    0 = empty, 1 = fresh, 2 = rotten
    
    Example:
        Input: [[2,1,1],
                [1,1,0],
                [0,1,1]]
        Output: 4
        Explanation:
        Minute 0: [[2,1,1],    Minute 1: [[2,2,1],
                   [1,1,0],              [2,1,0],
                   [0,1,1]]              [0,1,1]]
        Minute 2: [[2,2,2],    Minute 3: [[2,2,2],
                   [2,2,0],              [2,2,0],
                   [0,1,1]]              [0,2,1]]
        Minute 4: All rotten
    """
    if not grid:
        return -1
    
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0
    
    # Find all rotten oranges and count fresh
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:
                fresh_count += 1
    
    if fresh_count == 0:
        return 0
    
    # 4 directions: right, down, left, up (row_delta, col_delta)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    max_time = 0
    
    while queue:
        r, c, time = queue.popleft()  # Current rotten orange position and time
        max_time = max(max_time, time)  # Track maximum time taken
        
        # Check all 4 adjacent cells
        for dr, dc in directions:
            nr, nc = r + dr, c + dc  # nr = new row, nc = new column (neighbor position)
            
            # If neighbor is within bounds and is a fresh orange
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2  # Mark as rotten
                fresh_count -= 1  # Decrement fresh orange count
                queue.append((nr, nc, time + 1))  # Add to queue with incremented time
    
    return max_time if fresh_count == 0 else -1

print("=" * 60)
print("Pattern 6: Rotting Oranges (Multi-source BFS)")
print("=" * 60)
print("Problem: Find time for all fresh oranges to rot")
print("\nHow it works:")
print("  1. Add ALL rotten oranges to queue initially (multi-source)")
print("  2. Count all fresh oranges")
print("  3. Process queue level by level (each level = 1 minute)")
print("  4. Each rotten orange spreads to 4 adjacent cells")
print("  5. Mark newly rotten oranges and add to queue")
print("  6. Track time as we process levels")
print("  7. If fresh oranges remain, return -1 (impossible)")
print("\nExample:")
print("  Input grid (2=rotten, 1=fresh, 0=empty):")
grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
for row in grid:
    print(f"    {row}")
result = oranges_rotting([row[:] for row in grid])
print(f"  Output: {result} minutes")
print("  Key: All rotten oranges spread simultaneously each minute")
print()


# Pattern 7: Task Scheduler with Cooldown
def least_interval(tasks: List[str], n: int) -> int:
    """
    Schedule tasks with cooldown period.
    Time: O(m) where m is total intervals, Space: O(1)
    
    Example:
        Input: tasks = ['A','A','A','B','B','B'], n = 2
        Output: 8
        Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
        Tasks must have n intervals between same task
    """
    from collections import Counter
    import heapq
    
    # Count how many of each task we have
    # Example: {'A': 3, 'B': 3} means 3 A's and 3 B's
    task_counts = Counter(tasks)
    
    # Create max heap (Python has min heap, so use negative values)
    # Example: [3, 3] becomes [-3, -3] so most frequent is at top
    max_heap = [-count for count in task_counts.values()]
    heapq.heapify(max_heap)  # Convert list to heap structure
    
    # Track current time (starts at 0, increments each interval)
    time = 0
    
    # Queue stores tasks in cooldown: (remaining_count, time_when_available)
    # Example: (-2, 5) means 2 tasks remaining, available at time 5
    queue = deque()
    
    # Continue while there are tasks to process or tasks in cooldown
    while max_heap or queue:
        time += 1  # Increment time for each interval
        
        # Process a task if any are available
        if max_heap:
            # Get most frequent task (negative, so closest to 0)
            count = heapq.heappop(max_heap)
            count += 1  # Decrement actual count (since it's negative: -3 + 1 = -2)
            
            # If still have more of this task, put it in cooldown queue
            if count < 0:  # -2 < 0 means still 2 tasks left
                # Task will be available at: current_time + cooldown_period
                queue.append((count, time + n))
        # else: No tasks available, CPU sits idle this interval
        
        # Check if any task in cooldown is now available
        if queue and queue[0][1] == time:
            # Front of queue has reached its available time
            count, _ = queue.popleft()  # Remove from cooldown
            heapq.heappush(max_heap, count)  # Put back in available tasks
    
    return time  # Total intervals needed

print("=" * 60)
print("Pattern 7: Task Scheduler with Cooldown")
print("=" * 60)
print("Problem: You have a CPU that needs to execute tasks, but same tasks")
print("        need a cooldown period between executions.")
print()
print("Real-world analogy:")
print("  Imagine you're washing dishes (task A) and drying dishes (task B).")
print("  After washing a dish, your hands are wet and you need to wait")
print("  n=2 time units before washing another dish (cooldown).")
print("  During cooldown, you can either:")
print("    - Do a different task (dry dishes)")
print("    - Stay idle (wait)")
print()
print("The Problem:")
print("  - You have tasks: ['A', 'A', 'A', 'B', 'B', 'B']")
print("  - Cooldown n = 2 (must wait 2 intervals before repeating same task)")
print("  - Each task takes 1 time unit to execute")
print("  - Question: What's the minimum total time to finish all tasks?")
print()
print("Why can't we just do: A A A B B B? (6 time units)")
print("  Because: After executing A, you must wait 2 intervals before next A")
print("  So: A -> ? -> ? -> A is the earliest you can do another A")
print()
print("Valid Schedule (8 time units):")
print("  Time 0: Execute A   (first A)")
print("  Time 1: Execute B   (first B, A is in cooldown)")
print("  Time 2: idle        (both A and B in cooldown)")
print("  Time 3: Execute A   (second A, cooldown satisfied)")
print("  Time 4: Execute B   (second B)")
print("  Time 5: idle        (both in cooldown)")
print("  Time 6: Execute A   (third A)")
print("  Time 7: Execute B   (third B)")
print("  Total: 8 intervals")
print()
print("Key Rule: After executing task X at time t,")
print("         next X can't execute until time t + n + 1")
print("         (need n intervals gap)")
print()
print("\nHow the algorithm works:")
print("  1. Use max heap to always process most frequent task")
print("     (finish high-frequency tasks early to avoid bottlenecks)")
print("  2. Use queue to track when tasks become available again")
print("     (store task and the time when cooldown expires)")
print("  3. Execute most frequent task, then put in cooldown queue")
print("  4. Each time unit: check if any task cooldown is over")
print("  5. Move completed cooldown tasks back to max heap")
print("  6. If no tasks available, CPU sits idle (still counts time)")
print()
print("Example walkthrough:")
tasks = ['A', 'A', 'A', 'B', 'B', 'B']
n = 2
print(f"  Input: tasks = {tasks}, cooldown = {n}")
result = least_interval(tasks, n)
print(f"  Output: {result} intervals")
print()
print("  Step-by-step execution:")
print("    Interval 1: Run A (heap has A:3, B:3 → pick A)")
print("               A cooldown until time 4 (1+2+1)")
print("    Interval 2: Run B (heap has B:3)")
print("               B cooldown until time 5")
print("    Interval 3: idle (both A and B in cooldown)")
print("    Interval 4: Run A (A available again, still have 2 A's left)")
print("               A cooldown until time 7")
print("    Interval 5: Run B (B available again, still have 2 B's left)")
print("               B cooldown until time 8")
print("    Interval 6: idle (both in cooldown)")
print("    Interval 7: Run A (last A)")
print("    Interval 8: Run B (last B)")
print()
print("  Visual timeline: A -> B -> idle -> A -> B -> idle -> A -> B")
print("  Total: 8 intervals (not 6, because of cooldown constraints)")
print()


# Pattern 8: Number of Islands (BFS)
def num_islands_bfs(grid: List[List[str]]) -> int:
    """
    Count number of islands using BFS.
    Time: O(m*n), Space: O(min(m,n))
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = '0'
        
        while queue:
            row, col = queue.popleft()
            # 4 directions: right, down, left, up (row_delta, col_delta)
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                bfs(r, c)
                count += 1
    
    return count

print("=" * 60)
print("Pattern 8: Number of Islands (BFS)")
print("=" * 60)
print("Problem: Count number of islands (connected 1s)")
print("\nHow it works:")
print("  1. Scan grid for any land cell ('1')")
print("  2. When found: start BFS to explore entire island")
print("  3. BFS: use queue to visit all connected land cells")
print("  4. Mark visited cells as '0' to avoid recounting")
print("  5. Check 4 directions (up, down, left, right)")
print("  6. Each complete BFS = one island, increment counter")
print("\nExample:")
print("  Input grid (1=land, 0=water):")
grid = [
    ['1', '1', '0', '0', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '1', '0', '0'],
    ['0', '0', '0', '1', '1']
]
for row in grid:
    print(f"    {row}")
result = num_islands_bfs([row[:] for row in grid])
print(f"  Output: {result} islands")
print("  Found: top-left 2x2, center single, bottom-right 1x2")
print()


# Pattern 9: Shortest Path in Binary Matrix
def shortest_path_binary_matrix(grid: List[List[int]]) -> int:
    """
    Find shortest path from top-left to bottom-right.
    Time: O(n^2), Space: O(n^2)
    """
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    
    if n == 1:
        return 1
    
    queue = deque([(0, 0, 1)])  # (row, col, distance)
    grid[0][0] = 1  # Mark visited
    
    # 8 directions: right, down, left, up, diagonal-right-down, diagonal-right-up, diagonal-left-up, diagonal-left-down
    directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    
    while queue:
        r, c, dist = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if nr == n-1 and nc == n-1:
                return dist + 1
            
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                queue.append((nr, nc, dist + 1))
    
    return -1

print("=" * 60)
print("Pattern 9: Shortest Path in Binary Matrix")
print("=" * 60)
print("Problem: Find shortest path from top-left to bottom-right")
print("\nHow it works:")
print("  1. Start BFS from (0,0) with distance 1")
print("  2. Can move in 8 directions (including diagonals)")
print("  3. Track distance as we explore")
print("  4. Mark cells as visited (change 0 to 1)")
print("  5. BFS guarantees first path found is shortest")
print("  6. Return distance when we reach bottom-right")
print("\nExample:")
print("  Input grid (0=clear, 1=blocked):")
grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
for row in grid:
    print(f"    {row}")
result = shortest_path_binary_matrix([row[:] for row in grid])
print(f"  Output: {result} steps")
print("  Path: (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)")
print("  Key: BFS explores nearest cells first = shortest path")
