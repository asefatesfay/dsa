"""
Deque - Basics
==============
Double-ended queue implementation and operations.
"""

from collections import deque


print("=" * 60)
print("Basic Deque Operations")
print("=" * 60)
print()

# Create deque
dq = deque([1, 2, 3])
print(f"Initial deque: {dq}")

# Add to right
dq.append(4)
print(f"After append(4): {dq}")

# Add to left
dq.appendleft(0)
print(f"After appendleft(0): {dq}")

# Remove from right
right = dq.pop()
print(f"Popped from right: {right}, deque: {dq}")

# Remove from left
left = dq.popleft()
print(f"Popped from left: {left}, deque: {dq}")

# Peek (access without removing)
print(f"Peek right: {dq[-1]}")
print(f"Peek left: {dq[0]}")
print()


print("=" * 60)
print("Deque as Stack (LIFO)")
print("=" * 60)
print()

stack = deque()
print("Push 1, 2, 3:")
stack.append(1)
stack.append(2)
stack.append(3)
print(f"Stack: {stack}")

print("Pop operations:")
print(f"  Pop: {stack.pop()}")
print(f"  Pop: {stack.pop()}")
print(f"  Stack: {stack}")
print()


print("=" * 60)
print("Deque as Queue (FIFO)")
print("=" * 60)
print()

queue = deque()
print("Enqueue 1, 2, 3:")
queue.append(1)
queue.append(2)
queue.append(3)
print(f"Queue: {queue}")

print("Dequeue operations:")
print(f"  Dequeue: {queue.popleft()}")
print(f"  Dequeue: {queue.popleft()}")
print(f"  Queue: {queue}")
print()


print("=" * 60)
print("Deque with Max Size (Circular Buffer)")
print("=" * 60)
print()

# Fixed-size deque (automatically removes from left when full)
circular = deque(maxlen=3)
print(f"Max size: 3")

for i in range(5):
    circular.append(i)
    print(f"  Append {i}: {circular}")
print()


print("=" * 60)
print("Rotation Operations")
print("=" * 60)
print()

dq = deque([1, 2, 3, 4, 5])
print(f"Original: {dq}")

dq.rotate(2)  # Rotate right by 2
print(f"Rotate right by 2: {dq}")

dq.rotate(-3)  # Rotate left by 3
print(f"Rotate left by 3: {dq}")
print()


print("=" * 60)
print("Extend Operations")
print("=" * 60)
print()

dq = deque([1, 2, 3])
print(f"Original: {dq}")

dq.extend([4, 5])  # Add multiple to right
print(f"Extend right [4, 5]: {dq}")

dq.extendleft([0, -1])  # Add multiple to left (reversed!)
print(f"Extend left [0, -1]: {dq}")
print("Note: extendleft adds in reverse order!")
print()


print("=" * 60)
print("Other Useful Operations")
print("=" * 60)
print()

dq = deque([1, 2, 3, 2, 4])
print(f"Deque: {dq}")

# Count occurrences
print(f"Count of 2: {dq.count(2)}")

# Remove first occurrence
dq.remove(2)
print(f"After remove(2): {dq}")

# Reverse
dq.reverse()
print(f"After reverse(): {dq}")

# Clear
dq.clear()
print(f"After clear(): {dq}")
print()


print("=" * 60)
print("Example: Palindrome Checker")
print("=" * 60)
print()

def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome using deque.
    
    Time: O(n), Space: O(n)
    """
    s = ''.join(c.lower() for c in s if c.isalnum())
    dq = deque(s)
    
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    
    return True

test_strings = ["racecar", "hello", "A man a plan a canal Panama"]
for s in test_strings:
    print(f"'{s}' is palindrome: {is_palindrome(s)}")
print()


print("=" * 60)
print("Example: Recent Counter (Time Window)")
print("=" * 60)
print()

class RecentCounter:
    """
    Count requests in last 3000ms.
    
    Time: O(1) amortized per ping
    Space: O(w) where w is window size
    """
    
    def __init__(self):
        self.requests = deque()
    
    def ping(self, t: int) -> int:
        self.requests.append(t)
        
        # Remove requests older than 3000ms
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        
        return len(self.requests)

counter = RecentCounter()
pings = [1, 100, 3001, 3002]
print("Ping timestamps and counts (3000ms window):")
for t in pings:
    count = counter.ping(t)
    print(f"  Ping at {t}: {count} requests in window")
print()


print("=" * 60)
print("Example: Moving Average")
print("=" * 60)
print()

class MovingAverage:
    """
    Calculate average of last k elements.
    
    Time: O(1) per operation
    Space: O(k)
    """
    
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.sum = 0
    
    def next(self, val: int) -> float:
        self.queue.append(val)
        self.sum += val
        
        if len(self.queue) > self.size:
            self.sum -= self.queue.popleft()
        
        return self.sum / len(self.queue)

ma = MovingAverage(3)
values = [1, 10, 3, 5]
print("Moving average of last 3 elements:")
for val in values:
    avg = ma.next(val)
    print(f"  Add {val}: avg = {avg:.2f}")
print()


print("=" * 60)
print("Example: BFS with Deque")
print("=" * 60)
print()

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root: TreeNode) -> list:
    """
    Level-order traversal using deque as queue.
    
    Time: O(n), Space: O(w) where w is max width
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result

# Build tree: [3,9,20,null,null,15,7]
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print("Tree level-order traversal:")
for i, level in enumerate(level_order(root)):
    print(f"  Level {i}: {level}")
print()


print("=" * 60)
print("Performance Comparison: Deque vs List")
print("=" * 60)
print()

import time

def benchmark_left_operations(n=10000):
    # Deque
    start = time.time()
    dq = deque()
    for i in range(n):
        dq.appendleft(i)
    for i in range(n):
        dq.popleft()
    deque_time = time.time() - start
    
    # List
    start = time.time()
    lst = []
    for i in range(n):
        lst.insert(0, i)
    for i in range(n):
        lst.pop(0)
    list_time = time.time() - start
    
    return deque_time, list_time

dq_time, lst_time = benchmark_left_operations()
print(f"Operations on left end ({10000} ops):")
print(f"  Deque: {dq_time:.4f}s")
print(f"  List:  {lst_time:.4f}s")
print(f"  Speedup: {lst_time/dq_time:.1f}x faster with deque")
print()


print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Key Operations (all O(1)):")
print("  • append(x)      - Add to right")
print("  • appendleft(x)  - Add to left")
print("  • pop()          - Remove from right")
print("  • popleft()      - Remove from left")
print("  • rotate(n)      - Rotate elements")
print()
print("Common Use Cases:")
print("  • Sliding window problems")
print("  • BFS/level-order traversal")
print("  • Recent events tracking")
print("  • Palindrome checking")
print("  • Moving average/statistics")
print()
print("When to Use:")
print("  ✓ Need O(1) operations at both ends")
print("  ✓ Implementing queue or stack")
print("  ✓ Sliding window algorithms")
print("  ✗ Need random access by index (use list)")
