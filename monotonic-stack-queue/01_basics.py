"""
Monotonic Stack and Queue - Basics
===================================
Fundamental operations and patterns.
"""

from collections import deque
from typing import List


print("=" * 70)
print("Pattern 1: Monotonic Increasing Stack")
print("=" * 70)
print()

def monotonic_increasing_stack(arr: List[int]) -> None:
    """
    Stack maintains increasing order from bottom to top.
    Pop elements >= current before pushing.
    
    Time: O(n), Space: O(n)
    """
    stack = []
    
    print(f"Array: {arr}")
    print("\nProcessing:")
    
    for num in arr:
        # Pop elements that violate increasing order
        while stack and stack[-1] >= num:
            popped = stack.pop()
            print(f"  Pop {popped} (>= {num})")
        
        stack.append(num)
        print(f"  Push {num}, stack: {stack}")
    
    print(f"\nFinal stack (bottom→top): {stack}")

monotonic_increasing_stack([3, 1, 4, 1, 5, 9, 2, 6])
print()


print("=" * 70)
print("Pattern 2: Monotonic Decreasing Stack")
print("=" * 70)
print()

def monotonic_decreasing_stack(arr: List[int]) -> None:
    """
    Stack maintains decreasing order from bottom to top.
    Pop elements <= current before pushing.
    
    Time: O(n), Space: O(n)
    """
    stack = []
    
    print(f"Array: {arr}")
    print("\nProcessing:")
    
    for num in arr:
        # Pop elements that violate decreasing order
        while stack and stack[-1] <= num:
            popped = stack.pop()
            print(f"  Pop {popped} (<= {num})")
        
        stack.append(num)
        print(f"  Push {num}, stack: {stack}")
    
    print(f"\nFinal stack (bottom→top): {stack}")

monotonic_decreasing_stack([3, 1, 4, 1, 5, 9, 2, 6])
print()


print("=" * 70)
print("Pattern 3: Next Greater Element")
print("=" * 70)
print()

def next_greater_element(arr: List[int]) -> List[int]:
    """
    Find next greater element for each element.
    Use decreasing stack, store indices.
    
    Time: O(n), Space: O(n)
    """
    n = len(arr)
    result = [-1] * n
    stack = []  # Indices of elements waiting for next greater
    
    for i in range(n):
        # Current element is greater than stack top elements
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            result[idx] = arr[i]
        
        stack.append(i)
    
    return result

arr = [4, 5, 2, 10, 8]
result = next_greater_element(arr)
print(f"Array:        {arr}")
print(f"Next Greater: {result}")
print()


print("=" * 70)
print("Pattern 4: Previous Smaller Element")
print("=" * 70)
print()

def previous_smaller_element(arr: List[int]) -> List[int]:
    """
    Find previous smaller element for each element.
    Use increasing stack, process left-to-right.
    
    Time: O(n), Space: O(n)
    """
    n = len(arr)
    result = [-1] * n
    stack = []  # Indices maintaining increasing values
    
    for i in range(n):
        # Pop elements >= current
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        
        # Top of stack is previous smaller
        if stack:
            result[i] = arr[stack[-1]]
        
        stack.append(i)
    
    return result

arr = [4, 5, 2, 10, 8]
result = previous_smaller_element(arr)
print(f"Array:            {arr}")
print(f"Previous Smaller: {result}")
print()


print("=" * 70)
print("Pattern 5: Monotonic Queue (Sliding Window Maximum)")
print("=" * 70)
print()

def sliding_window_max(arr: List[int], k: int) -> List[int]:
    """
    Find maximum in each sliding window of size k.
    Use decreasing deque, store indices.
    
    Time: O(n), Space: O(k)
    """
    dq = deque()  # Indices in decreasing order of values
    result = []
    
    for i in range(len(arr)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Maintain decreasing order
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add max when window is full
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = sliding_window_max(arr, k)
print(f"Array: {arr}")
print(f"Window size: {k}")
print(f"Sliding max: {result}")
print()


print("=" * 70)
print("Pattern 6: Monotonic Queue (Sliding Window Minimum)")
print("=" * 70)
print()

def sliding_window_min(arr: List[int], k: int) -> List[int]:
    """
    Find minimum in each sliding window of size k.
    Use increasing deque, store indices.
    
    Time: O(n), Space: O(k)
    """
    dq = deque()  # Indices in increasing order of values
    result = []
    
    for i in range(len(arr)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Maintain increasing order
        while dq and arr[dq[-1]] > arr[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add min when window is full
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = sliding_window_min(arr, k)
print(f"Array: {arr}")
print(f"Window size: {k}")
print(f"Sliding min: {result}")
print()


print("=" * 70)
print("Pattern 7: Stock Span Problem")
print("=" * 70)
print()

def stock_span(prices: List[int]) -> List[int]:
    """
    Calculate span (consecutive days with price <= current).
    Use decreasing stack with indices.
    
    Time: O(n), Space: O(n)
    """
    n = len(prices)
    span = [1] * n
    stack = []  # Indices of prices in decreasing order
    
    for i in range(n):
        # Pop smaller or equal prices
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        
        # Span is distance to previous greater price
        span[i] = i + 1 if not stack else i - stack[-1]
        
        stack.append(i)
    
    return span

prices = [100, 80, 60, 70, 60, 75, 85]
span = stock_span(prices)
print(f"Prices: {prices}")
print(f"Span:   {span}")
print("\nInterpretation:")
for i, (p, s) in enumerate(zip(prices, span)):
    print(f"  Day {i}: Price {p}, Span {s} days")
print()


print("=" * 70)
print("Pattern 8: Largest Rectangle in Histogram")
print("=" * 70)
print()

def largest_rectangle_area(heights: List[int]) -> int:
    """
    Find largest rectangle in histogram.
    Use increasing stack with indices.
    
    Time: O(n), Space: O(n)
    """
    stack = []  # Indices of heights in increasing order
    max_area = 0
    heights = heights + [0]  # Sentinel to flush stack
    
    for i, h in enumerate(heights):
        # Pop taller bars and calculate their areas
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    return max_area

heights = [2, 1, 5, 6, 2, 3]
area = largest_rectangle_area(heights)
print(f"Heights: {heights}")
print(f"Largest rectangle area: {area}")
print()


print("=" * 70)
print("Summary")
print("=" * 70)
print()
print("Monotonic Stack Types:")
print("  • Increasing: Pop elements >= current")
print("  • Decreasing: Pop elements <= current")
print()
print("Common Patterns:")
print("  1. Next Greater: Decreasing stack, process left→right")
print("  2. Previous Smaller: Increasing stack, check top before push")
print("  3. Stock Span: Decreasing stack, calculate distance")
print("  4. Histogram: Increasing stack, calculate area on pop")
print()
print("Monotonic Queue:")
print("  • Sliding Max: Decreasing deque")
print("  • Sliding Min: Increasing deque")
print("  • Remove expired indices from front")
print()
print("Time Complexity: O(n) - each element pushed and popped once")
print("Space Complexity: O(n) - worst case all elements in stack/queue")
