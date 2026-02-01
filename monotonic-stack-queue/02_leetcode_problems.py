"""
Monotonic Stack/Queue - LeetCode Problems
==========================================
Essential problems using monotonic data structures.
"""

from typing import List
from collections import deque


print("=" * 70)
print("Problem 1: Next Greater Element I (LC 496)")
print("=" * 70)
print()

def next_greater_element(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Find next greater element for each element in nums1.
    
    Approach: Monotonic decreasing stack on nums2
    Time: O(n), Space: O(n)
    """
    next_greater = {}
    stack = []
    
    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)
    
    return [next_greater.get(num, -1) for num in nums1]

nums1 = [4, 1, 2]
nums2 = [1, 3, 4, 2]
print(f"nums1: {nums1}, nums2: {nums2}")
print(f"Next greater: {next_greater_element(nums1, nums2)}")
print()


print("=" * 70)
print("Problem 2: Daily Temperatures (LC 739)")
print("=" * 70)
print()

def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Days until warmer temperature.
    
    Approach: Monotonic decreasing stack with indices
    Time: O(n), Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Store indices
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_i = stack.pop()
            result[prev_i] = i - prev_i
        stack.append(i)
    
    return result

temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(f"Temperatures: {temps}")
print(f"Days to wait: {daily_temperatures(temps)}")
print()


print("=" * 70)
print("Problem 3: Largest Rectangle in Histogram (LC 84)")
print("=" * 70)
print()

def largest_rectangle_area(heights: List[int]) -> int:
    """
    Find largest rectangle in histogram.
    
    Approach: Monotonic increasing stack
    Time: O(n), Space: O(n)
    """
    stack = []
    max_area = 0
    heights.append(0)  # Sentinel to flush stack
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    heights.pop()  # Remove sentinel
    return max_area

heights = [2, 1, 5, 6, 2, 3]
print(f"Heights: {heights}")
print(f"Largest rectangle: {largest_rectangle_area(heights)}")
print()


print("=" * 70)
print("Problem 4: Trapping Rain Water (LC 42)")
print("=" * 70)
print()

def trap(height: List[int]) -> int:
    """
    Calculate trapped rainwater.
    
    Approach: Monotonic decreasing stack
    Time: O(n), Space: O(n)
    """
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bounded_height = min(height[left], h) - height[bottom]
            water += width * bounded_height
        stack.append(i)
    
    return water

height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(f"Height: {height}")
print(f"Water trapped: {trap(height)}")
print()


print("=" * 70)
print("Problem 5: Sliding Window Maximum (LC 239)")
print("=" * 70)
print()

def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Max value in each sliding window of size k.
    
    Approach: Monotonic decreasing deque
    Time: O(n), Space: O(k)
    """
    dq = deque()  # Store indices
    result = []
    
    for i, num in enumerate(nums):
        # Remove out of window
        if dq and dq[0] <= i - k:
            dq.popleft()
        
        # Maintain decreasing order
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is full
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(f"Nums: {nums}, k={k}")
print(f"Max in windows: {max_sliding_window(nums, k)}")
print()


print("=" * 70)
print("Problem 6: Remove K Digits (LC 402)")
print("=" * 70)
print()

def remove_k_digits(num: str, k: int) -> str:
    """
    Remove k digits to get smallest number.
    
    Approach: Monotonic increasing stack
    Time: O(n), Space: O(n)
    """
    stack = []
    
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    
    # Remove remaining k digits from end
    stack = stack[:len(stack) - k] if k > 0 else stack
    
    # Remove leading zeros
    result = ''.join(stack).lstrip('0')
    return result if result else '0'

num = "1432219"
k = 3
print(f"Number: {num}, k={k}")
print(f"Smallest: {remove_k_digits(num, k)}")
print()


print("=" * 70)
print("Problem 7: Next Greater Element II (LC 503)")
print("=" * 70)
print()

def next_greater_elements(nums: List[int]) -> List[int]:
    """
    Next greater element in circular array.
    
    Approach: Monotonic decreasing stack, traverse twice
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]
        if i < n:
            stack.append(idx)
    
    return result

nums = [1, 2, 1]
print(f"Circular array: {nums}")
print(f"Next greater: {next_greater_elements(nums)}")
print()


print("=" * 70)
print("Problem 8: Car Fleet (LC 853)")
print("=" * 70)
print()

def car_fleet(target: int, position: List[int], speed: List[int]) -> int:
    """
    Count car fleets reaching destination.
    
    Approach: Sort by position, monotonic stack of times
    Time: O(n log n), Space: O(n)
    """
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    
    for pos, spd in cars:
        time = (target - pos) / spd
        if not stack or time > stack[-1]:
            stack.append(time)
    
    return len(stack)

target = 12
position = [10, 8, 0, 5, 3]
speed = [2, 4, 1, 1, 3]
print(f"Target: {target}")
print(f"Position: {position}, Speed: {speed}")
print(f"Car fleets: {car_fleet(target, position, speed)}")
print()


print("=" * 70)
print("Problem 9: Online Stock Span (LC 901)")
print("=" * 70)
print()

class StockSpanner:
    """
    Calculate stock price span.
    
    Approach: Monotonic decreasing stack with (price, span)
    """
    
    def __init__(self):
        self.stack = []
    
    def next(self, price: int) -> int:
        """Time: O(1) amortized"""
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span

spanner = StockSpanner()
prices = [100, 80, 60, 70, 60, 75, 85]
print("Stock prices and spans:")
for p in prices:
    print(f"  Price {p}: span = {spanner.next(p)}")
print()


print("=" * 70)
print("Problem 10: Sum of Subarray Minimums (LC 907)")
print("=" * 70)
print()

def sum_subarray_mins(arr: List[int]) -> int:
    """
    Sum of minimums of all subarrays.
    
    Approach: Monotonic increasing stack, find left/right boundaries
    Time: O(n), Space: O(n)
    """
    MOD = 10**9 + 7
    n = len(arr)
    stack = []
    result = 0
    
    for i in range(n + 1):
        while stack and (i == n or arr[stack[-1]] > arr[i]):
            mid = stack.pop()
            left = stack[-1] if stack else -1
            right = i
            count = (mid - left) * (right - mid)
            result = (result + arr[mid] * count) % MOD
        stack.append(i)
    
    return result

arr = [3, 1, 2, 4]
print(f"Array: {arr}")
print(f"Sum of subarray mins: {sum_subarray_mins(arr)}")
print()


print("=" * 70)
print("Problem 11: Shortest Subarray with Sum >= K (LC 862)")
print("=" * 70)
print()

def shortest_subarray(nums: List[int], k: int) -> int:
    """
    Find shortest subarray with sum >= k.
    
    Approach: Prefix sum + monotonic increasing deque
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    
    dq = deque()
    min_len = n + 1
    
    for i in range(n + 1):
        # Check if we can form valid subarray
        while dq and prefix[i] - prefix[dq[0]] >= k:
            min_len = min(min_len, i - dq.popleft())
        
        # Maintain increasing order
        while dq and prefix[i] <= prefix[dq[-1]]:
            dq.pop()
        
        dq.append(i)
    
    return min_len if min_len <= n else -1

nums = [2, -1, 2]
k = 3
print(f"Nums: {nums}, k={k}")
print(f"Shortest subarray: {shortest_subarray(nums, k)}")
print()


print("=" * 70)
print("Problem 12: Constrained Subsequence Sum (LC 1425)")
print("=" * 70)
print()

def constrained_subset_sum(nums: List[int], k: int) -> int:
    """
    Max sum of subsequence with max gap k.
    
    Approach: DP + monotonic decreasing deque
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    dp = nums[:]
    dq = deque()
    
    for i in range(n):
        # Remove out of range
        if dq and dq[0] < i - k:
            dq.popleft()
        
        # Update dp
        if dq:
            dp[i] = max(dp[i], nums[i] + dp[dq[0]])
        
        # Maintain decreasing order
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        
        dq.append(i)
    
    return max(dp)

nums = [10, 2, -10, 5, 20]
k = 2
print(f"Nums: {nums}, k={k}")
print(f"Max constrained sum: {constrained_subset_sum(nums, k)}")
print()


print("=" * 70)
print("Summary")
print("=" * 70)
print()
print("Key Patterns:")
print("  • Next Greater: Monotonic decreasing stack")
print("  • Histogram: Monotonic increasing stack")
print("  • Sliding Window Max: Monotonic decreasing deque")
print("  • Remove K Digits: Monotonic increasing stack")
print("  • Stock Span: Monotonic decreasing stack with counts")
print("  • Subarray Problems: Prefix sum + monotonic deque")
print()
print("Stack vs Deque:")
print("  • Stack: One-directional problems (next greater/smaller)")
print("  • Deque: Sliding window problems (need both ends)")
print()
print("Time Complexity:")
print("  • All monotonic problems: O(n) amortized")
print("  • Each element pushed/popped at most once")
print()
print("Interview Tips:")
print("  ✓ Identify if you need next greater/smaller")
print("  ✓ Choose increasing/decreasing based on problem")
print("  ✓ Store indices when you need positions")
print("  ✓ Use deque for sliding window optimizations")
print("  ✓ Combine with prefix sum for subarray problems")
