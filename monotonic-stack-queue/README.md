# Monotonic Stack and Queue

## Overview

Monotonic data structures maintain elements in a specific order (increasing or decreasing) which enables efficient solving of range-based problems.

## Monotonic Stack

A stack that maintains elements in monotonic order by popping elements that violate the order before pushing new ones.

### Types

**Monotonic Increasing Stack:**
- Elements increase from bottom to top
- Pop smaller elements when pushing larger ones
- Use: Find next greater element

**Monotonic Decreasing Stack:**
- Elements decrease from bottom to top
- Pop larger elements when pushing smaller ones
- Use: Find next smaller element

### Template

```python
def monotonic_increasing_stack(arr):
    stack = []
    result = []
    
    for i, num in enumerate(arr):
        # Pop elements that violate increasing order
        while stack and arr[stack[-1]] >= num:
            stack.pop()
        
        # Process with top of stack
        if stack:
            result.append(arr[stack[-1]])
        
        stack.append(i)
    
    return result
```

### Common Patterns

1. **Next Greater Element**: Use decreasing stack, store indices
2. **Previous Smaller Element**: Use increasing stack, process left-to-right
3. **Largest Rectangle**: Use increasing stack for histogram heights
4. **Stock Span**: Use decreasing stack to count consecutive smaller elements

### Time Complexity

- Each element pushed once: O(n)
- Each element popped at most once: O(n)
- **Total: O(n)**

## Monotonic Queue

A deque that maintains elements in monotonic order, typically used for sliding window problems.

### Template

```python
from collections import deque

def sliding_window_maximum(arr, k):
    dq = deque()  # Store indices
    result = []
    
    for i, num in enumerate(arr):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Maintain decreasing order
        while dq and arr[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is full
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result
```

### Common Patterns

1. **Sliding Window Maximum**: Use decreasing queue
2. **Sliding Window Minimum**: Use increasing queue
3. **Jump Game VI**: DP with monotonic queue optimization
4. **Constrained Subsequence Sum**: Track best options in window

## When to Use

### Monotonic Stack
- Finding next/previous greater/smaller elements
- Range queries (max/min in ranges)
- Histogram problems
- Trapping water problems

### Monotonic Queue
- Sliding window maximum/minimum
- DP optimization with range constraints
- Moving average with constraints

## Key Insights

1. **Amortized O(n)**: Each element processed exactly twice (push + pop)
2. **Space O(n)**: Worst case when all elements maintain order
3. **Store Indices**: Usually store indices instead of values for position info
4. **Window Maintenance**: For queues, remove expired elements from front

## Common Mistakes

1. Not removing expired window elements
2. Confusing when to use increasing vs decreasing
3. Forgetting to check if stack/queue is empty
4. Processing elements before adding to structure

## Interview Tips

- Clarify if asking for next/previous greater/smaller
- Consider if you need indices or just values
- Watch for circular arrays (process array twice)
- For sliding windows, consider monotonic queue
- Time complexity is always O(n) when properly implemented
