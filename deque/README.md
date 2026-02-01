# Deque (Double-Ended Queue)

## Overview
A **deque** (pronounced "deck") is a linear data structure that allows insertion and deletion at both ends (front and back) in O(1) time.

## Operations

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| append(x) | O(1) | Add element to right end |
| appendleft(x) | O(1) | Add element to left end |
| pop() | O(1) | Remove and return rightmost element |
| popleft() | O(1) | Remove and return leftmost element |
| peek() | O(1) | View rightmost element without removing |
| peekleft() | O(1) | View leftmost element without removing |

## Python Implementation
```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)        # [1, 2, 3, 4]
dq.appendleft(0)    # [0, 1, 2, 3, 4]
dq.pop()            # 4, deque: [0, 1, 2, 3]
dq.popleft()        # 0, deque: [1, 2, 3]
```

## Use Cases

### 1. Sliding Window
Maintain elements in a window that slides over an array.
```python
# Maximum in sliding window
def max_sliding_window(nums, k):
    dq = deque()  # Store indices
    result = []
    
    for i, num in enumerate(nums):
        # Remove out of window
        if dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove smaller elements (monotonic decreasing)
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

### 2. BFS (Level-Order Traversal)
Used as a queue for graph/tree traversal.
```python
def bfs(root):
    if not root:
        return []
    
    queue = deque([root])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node.val)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result
```

### 3. Recent Counter
Track events in a time window.
```python
class RecentCounter:
    def __init__(self):
        self.requests = deque()
    
    def ping(self, t):
        self.requests.append(t)
        
        # Remove old requests
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        
        return len(self.requests)
```

### 4. Palindrome Check
Access from both ends to verify symmetry.
```python
def is_palindrome(s):
    dq = deque(s.lower())
    
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    
    return True
```

## Common Patterns

### Pattern 1: Monotonic Deque
Maintain elements in increasing or decreasing order.
- **Sliding Window Maximum**: Monotonic decreasing deque
- **Sliding Window Minimum**: Monotonic increasing deque

### Pattern 2: Two-Pointer with Deque
Process elements from both ends.
- **Palindrome problems**
- **Container With Most Water**

### Pattern 3: Fixed-Size Window
Maintain exactly k elements.
- **Moving Average**
- **Max/Min in Window**

## Deque vs List

| Feature | Deque | List |
|---------|-------|------|
| append() | O(1) | O(1) amortized |
| appendleft() | O(1) | O(n) |
| pop() | O(1) | O(1) |
| popleft() | O(1) | O(n) |
| Access by index | O(n) | O(1) |
| Memory | More efficient for both ends | Better for random access |

**Use deque when**: Frequent operations at both ends
**Use list when**: Need index-based access

## Interview Tips
- ✓ Deque is ideal for sliding window problems
- ✓ Can be used as both stack (append/pop) and queue (append/popleft)
- ✓ Monotonic deque pattern appears frequently
- ✓ Consider deque when you need O(1) operations at both ends
- ✓ Python's `collections.deque` is implemented as doubly-linked list

## Time Complexity Summary
- **All basic operations**: O(1)
- **Search**: O(n) (must iterate)
- **Access by index**: O(n) for deque, O(1) for list

## Common LeetCode Problems
- LC 239: Sliding Window Maximum
- LC 862: Shortest Subarray with Sum at Least K
- LC 933: Number of Recent Calls
- LC 1696: Jump Game VI
- LC 346: Moving Average from Data Stream
