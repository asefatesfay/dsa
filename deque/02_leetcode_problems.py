"""
Deque - LeetCode Problems
=========================
Essential deque problems for interviews.
"""

from collections import deque
from typing import List


print("=" * 70)
print("Problem 1: Sliding Window Maximum (LC 239)")
print("=" * 70)
print()

def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Find maximum in each sliding window of size k.
    
    Approach: Monotonic decreasing deque (store indices)
    Time: O(n), Space: O(k)
    """
    result = []
    dq = deque()  # Store indices
    
    for i, num in enumerate(nums):
        # Remove indices outside window
        if dq and dq[0] <= i - k:
            dq.popleft()
        
        # Maintain decreasing order (remove smaller)
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        # Add to result once window is full
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

nums = [1,3,-1,-3,5,3,6,7]
k = 3
print(f"Array: {nums}, k={k}")
print(f"Max in each window: {max_sliding_window(nums, k)}")
print()


print("=" * 70)
print("Problem 2: Sliding Window Median (LC 480)")
print("=" * 70)
print()

from sortedcontainers import SortedList

def median_sliding_window(nums: List[int], k: int) -> List[float]:
    """
    Find median in each sliding window.
    
    Approach: Maintain sorted window with SortedList
    Time: O(n*log k), Space: O(k)
    """
    window = SortedList(nums[:k])
    result = []
    
    def get_median():
        mid = k // 2
        if k % 2 == 1:
            return float(window[mid])
        return (window[mid-1] + window[mid]) / 2.0
    
    result.append(get_median())
    
    for i in range(k, len(nums)):
        window.remove(nums[i-k])
        window.add(nums[i])
        result.append(get_median())
    
    return result

# Note: Requires sortedcontainers library
print("Median Sliding Window:")
print("  nums=[1,3,-1,-3,5,3,6,7], k=3")
print("  Result: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]")
print()


print("=" * 70)
print("Problem 3: Shortest Subarray with Sum at Least K (LC 862)")
print("=" * 70)
print()

def shortest_subarray(nums: List[int], k: int) -> int:
    """
    Find shortest subarray with sum >= k.
    
    Approach: Prefix sum + monotonic increasing deque
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    
    dq = deque()
    result = float('inf')
    
    for i in range(n + 1):
        # Check if we can form valid subarray
        while dq and prefix[i] - prefix[dq[0]] >= k:
            result = min(result, i - dq.popleft())
        
        # Maintain increasing order
        while dq and prefix[i] <= prefix[dq[-1]]:
            dq.pop()
        
        dq.append(i)
    
    return result if result != float('inf') else -1

nums = [2, -1, 2]
k = 3
print(f"Array: {nums}, k={k}")
print(f"Shortest subarray length: {shortest_subarray(nums, k)}")
print()


print("=" * 70)
print("Problem 4: Number of Recent Calls (LC 933)")
print("=" * 70)
print()

class RecentCounter:
    """
    Count requests in last 3000ms window.
    
    Time: O(1) amortized per ping
    Space: O(w) where w is window size
    """
    
    def __init__(self):
        self.requests = deque()
    
    def ping(self, t: int) -> int:
        self.requests.append(t)
        
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        
        return len(self.requests)

counter = RecentCounter()
pings = [1, 100, 3001, 3002]
print("Recent Calls (3000ms window):")
for t in pings:
    print(f"  Ping({t}): {counter.ping(t)} requests")
print()


print("=" * 70)
print("Problem 5: Jump Game VI (LC 1696)")
print("=" * 70)
print()

def max_result(nums: List[int], k: int) -> int:
    """
    Max score jumping at most k steps (DP + deque optimization).
    
    Approach: Monotonic decreasing deque for max in window
    Time: O(n), Space: O(k)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])
    
    for i in range(1, n):
        # Remove indices outside window
        while dq and dq[0] < i - k:
            dq.popleft()
        
        # Best score reaching i
        dp[i] = nums[i] + dp[dq[0]]
        
        # Maintain decreasing order
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        
        dq.append(i)
    
    return dp[-1]

nums = [1,-1,-2,4,-7,3]
k = 2
print(f"Array: {nums}, k={k}")
print(f"Max result: {max_result(nums, k)}")
print()


print("=" * 70)
print("Problem 6: Moving Average from Data Stream (LC 346)")
print("=" * 70)
print()

class MovingAverage:
    """
    Calculate moving average of last size values.
    
    Time: O(1) per operation
    Space: O(size)
    """
    
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.total = 0
    
    def next(self, val: int) -> float:
        self.queue.append(val)
        self.total += val
        
        if len(self.queue) > self.size:
            self.total -= self.queue.popleft()
        
        return self.total / len(self.queue)

ma = MovingAverage(3)
values = [1, 10, 3, 5]
print("Moving Average (size=3):")
for val in values:
    print(f"  next({val}): {ma.next(val):.2f}")
print()


print("=" * 70)
print("Problem 7: Constrained Subsequence Sum (LC 1425)")
print("=" * 70)
print()

def constrained_subset_sum(nums: List[int], k: int) -> int:
    """
    Max sum of non-empty subsequence with constraint: gap <= k.
    
    Approach: DP + monotonic decreasing deque
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])
    result = dp[0]
    
    for i in range(1, n):
        # Remove indices outside window
        while dq and dq[0] < i - k:
            dq.popleft()
        
        # Take current or extend previous
        dp[i] = max(nums[i], nums[i] + dp[dq[0]])
        result = max(result, dp[i])
        
        # Maintain decreasing order
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        
        dq.append(i)
    
    return result

nums = [10,2,-10,5,20]
k = 2
print(f"Array: {nums}, k={k}")
print(f"Max constrained sum: {constrained_subset_sum(nums, k)}")
print()


print("=" * 70)
print("Problem 8: Reveal Cards In Increasing Order (LC 950)")
print("=" * 70)
print()

def deck_revealed_increasing(deck: List[int]) -> List[int]:
    """
    Arrange deck so revealing alternately gives sorted order.
    
    Approach: Simulate process backwards using deque
    Time: O(n log n), Space: O(n)
    """
    deck.sort()
    dq = deque()
    
    # Build result backwards
    for card in reversed(deck):
        if dq:
            dq.appendleft(dq.pop())  # Move last to first
        dq.appendleft(card)
    
    return list(dq)

deck = [17,13,11,2,3,5,7]
print(f"Deck: {deck}")
print(f"Arrangement: {deck_revealed_increasing(deck)}")
print()


print("=" * 70)
print("Problem 9: Design Circular Queue (LC 622)")
print("=" * 70)
print()

class MyCircularQueue:
    """
    Implement circular queue with fixed size.
    
    Time: O(1) for all operations
    Space: O(k)
    """
    
    def __init__(self, k: int):
        self.queue = deque(maxlen=k)
        self.size = k
    
    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.queue.append(value)
        return True
    
    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.queue.popleft()
        return True
    
    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[0]
    
    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.queue[-1]
    
    def isEmpty(self) -> bool:
        return len(self.queue) == 0
    
    def isFull(self) -> bool:
        return len(self.queue) == self.size

cq = MyCircularQueue(3)
print("Circular Queue (size=3):")
print(f"  enQueue(1): {cq.enQueue(1)}")
print(f"  enQueue(2): {cq.enQueue(2)}")
print(f"  enQueue(3): {cq.enQueue(3)}")
print(f"  enQueue(4): {cq.enQueue(4)} (full)")
print(f"  Front: {cq.Front()}")
print(f"  isFull: {cq.isFull()}")
print()


print("=" * 70)
print("Problem 10: Longest Continuous Subarray (LC 1438)")
print("=" * 70)
print()

def longest_subarray(nums: List[int], limit: int) -> int:
    """
    Longest subarray where |max - min| <= limit.
    
    Approach: Two deques (max and min) + sliding window
    Time: O(n), Space: O(n)
    """
    max_dq = deque()  # Decreasing
    min_dq = deque()  # Increasing
    left = 0
    result = 0
    
    for right, num in enumerate(nums):
        # Maintain max deque (decreasing)
        while max_dq and max_dq[-1] < num:
            max_dq.pop()
        max_dq.append(num)
        
        # Maintain min deque (increasing)
        while min_dq and min_dq[-1] > num:
            min_dq.pop()
        min_dq.append(num)
        
        # Shrink window if constraint violated
        while max_dq[0] - min_dq[0] > limit:
            if max_dq[0] == nums[left]:
                max_dq.popleft()
            if min_dq[0] == nums[left]:
                min_dq.popleft()
            left += 1
        
        result = max(result, right - left + 1)
    
    return result

nums = [8,2,4,7]
limit = 4
print(f"Array: {nums}, limit={limit}")
print(f"Longest subarray: {longest_subarray(nums, limit)}")
print()


print("=" * 70)
print("Summary")
print("=" * 70)
print()
print("Key Patterns:")
print("  • Sliding Window Max/Min: Monotonic deque")
print("  • Recent Events: Deque with time-based filtering")
print("  • DP Optimization: Deque for range max/min queries")
print("  • Simulation: Use deque for flexible operations")
print()
print("Monotonic Deque:")
print("  • Decreasing: Track maximum in window")
print("  • Increasing: Track minimum in window")
print("  • Remove elements that can't be answer")
print()
print("Time Complexities:")
print("  • All basic ops: O(1)")
print("  • Sliding window: O(n) with monotonic deque")
print("  • vs naive O(n*k): Huge improvement!")
print()
print("Interview Tips:")
print("  ✓ Deque ideal for sliding window with max/min")
print("  ✓ Store indices (not values) for position tracking")
print("  ✓ Monotonic deque: remove useless elements")
print("  ✓ Consider deque when need both-end access")
