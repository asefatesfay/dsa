"""
Heap - Common Patterns
======================
Essential patterns and algorithms using heaps.
"""

import heapq
from typing import List, Optional
from collections import Counter


# Pattern 1: Kth Largest Element
def find_kth_largest(nums: List[int], k: int) -> int:
    """
    Find the kth largest element in array.
    Time: O(n log k), Space: O(k)
    
    Example:
        Input: nums = [3,2,1,5,6,4], k = 2
        Output: 5
        Explanation: 2nd largest is 5 (largest is 6)
    """
    # Keep min heap of size k
    # Smallest in heap will be kth largest overall
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        # If heap exceeds k, remove smallest
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    
    # Root of min heap is kth largest
    return min_heap[0]

print("=" * 60)
print("Pattern 1: Kth Largest Element")
print("=" * 60)
print("Problem: Find the kth largest element in unsorted array")
print("\nHow it works:")
print("  1. Maintain a min heap of size k")
print("  2. Add each element to heap")
print("  3. If heap size exceeds k, remove smallest")
print("  4. After processing all: heap contains k largest elements")
print("  5. Root (smallest in heap) is the kth largest overall")
print("  6. Why? We kept removing smaller elements until k remain")
print("\nExample:")
nums = [3, 2, 1, 5, 6, 4]
k = 2
print(f"  Input: nums = {nums}, k = {k}")
result = find_kth_largest(nums, k)
print(f"  Output: {result}")
print(f"  Explanation: Largest elements are [6, 5], 2nd largest = 5")
print()


# Pattern 2: Merge K Sorted Lists
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_sorted_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists.
    Time: O(n log k) where n=total nodes, k=num lists
    Space: O(k)
    
    Example:
        Input: [[1,4,5], [1,3,4], [2,6]]
        Output: [1,1,2,3,4,4,5,6]
    """
    # Min heap: (value, list_index, node)
    min_heap = []
    
    # Add first node from each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(min_heap, (node.val, i, node))
    
    dummy = ListNode(0)  # Dummy head for result
    current = dummy
    
    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        
        # Add to result
        current.next = node
        current = current.next
        
        # Add next node from same list
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))
    
    return dummy.next

print("=" * 60)
print("Pattern 2: Merge K Sorted Lists")
print("=" * 60)
print("Problem: Merge k sorted linked lists into one sorted list")
print("\nHow it works:")
print("  1. Use min heap to track smallest element from each list")
print("  2. Initially: add first node from all k lists to heap")
print("  3. Repeatedly: pop smallest from heap, add to result")
print("  4. When we pop a node: add its next node to heap")
print("  5. This ensures we always pick globally smallest available")
print("  6. Heap size ≤ k, so each operation is O(log k)")
print("\nExample:")
print("  Input lists: [1→4→5], [1→3→4], [2→6]")
print("  Output: 1→1→2→3→4→4→5→6")
print("  Process:")
print("    Heap: [(1,0), (1,1), (2,2)] → pick 1 from list 0")
print("    Heap: [(1,1), (2,2), (4,0)] → pick 1 from list 1")
print("    Heap: [(2,2), (3,1), (4,0)] → pick 2 from list 2")
print("    ... and so on")
print()


# Pattern 3: Top K Frequent Elements
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Find k most frequent elements.
    Time: O(n log k), Space: O(n)
    
    Example:
        Input: nums = [1,1,1,2,2,3], k = 2
        Output: [1, 2]
        Explanation: 1 appears 3 times, 2 appears 2 times
    """
    # Count frequencies
    freq_map = Counter(nums)
    
    # Use min heap of size k
    # Store (frequency, number) tuples
    min_heap = []
    
    for num, freq in freq_map.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    
    # Extract numbers from heap
    return [num for freq, num in min_heap]

print("=" * 60)
print("Pattern 3: Top K Frequent Elements")
print("=" * 60)
print("Problem: Find k most frequently occurring elements")
print("\nHow it works:")
print("  1. Count frequency of each element (hash map)")
print("  2. Use min heap to keep k most frequent")
print("  3. Store (frequency, number) pairs in heap")
print("  4. If heap size exceeds k, remove least frequent")
print("  5. Final heap contains k most frequent elements")
print("\nExample:")
nums = [1, 1, 1, 2, 2, 3]
k = 2
print(f"  Input: nums = {nums}, k = {k}")
result = top_k_frequent(nums, k)
print(f"  Output: {result}")
print(f"  Frequencies: 1 appears 3x, 2 appears 2x, 3 appears 1x")
print(f"  Top 2 frequent: [1, 2]")
print()


# Pattern 4: K Closest Points to Origin
def k_closest_points(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Find k closest points to origin (0,0).
    Time: O(n log k), Space: O(k)
    
    Example:
        Input: points = [[1,3],[-2,2],[5,8]], k = 2
        Output: [[-2,2],[1,3]]
        Explanation: Distances are sqrt(10), sqrt(8), sqrt(89)
    """
    # Max heap: store negative distances to simulate max heap
    # Pair: (-distance, point)
    max_heap = []
    
    for x, y in points:
        # Calculate squared distance (no need for sqrt, just for comparison)
        dist = -(x*x + y*y)  # Negative for max heap
        
        if len(max_heap) < k:
            heapq.heappush(max_heap, (dist, [x, y]))
        else:
            # If this point is closer than farthest in heap
            if dist > max_heap[0][0]:
                heapq.heapreplace(max_heap, (dist, [x, y]))
    
    return [point for dist, point in max_heap]

print("=" * 60)
print("Pattern 4: K Closest Points to Origin")
print("=" * 60)
print("Problem: Find k points closest to origin (0, 0)")
print("\nHow it works:")
print("  1. Use max heap to track k closest points")
print("  2. Store negative distances (Python has min heap)")
print("  3. For each point: calculate distance to origin")
print("  4. If heap has space: add point")
print("  5. If heap full and point closer: replace farthest")
print("  6. Final heap has k closest points")
print("\nExample:")
points = [[1, 3], [-2, 2], [5, 8]]
k = 2
print(f"  Input: points = {points}, k = {k}")
result = k_closest_points(points, k)
print(f"  Output: {result}")
print(f"  Distances: [1,3]=√10, [-2,2]=√8, [5,8]=√89")
print(f"  Closest 2: [-2,2] and [1,3]")
print()


# Pattern 5: Find Median from Data Stream
class MedianFinder:
    """
    Find median from stream of numbers.
    Time: O(log n) per add, O(1) for median
    Space: O(n)
    
    Example:
        addNum(1) → median = 1
        addNum(2) → median = 1.5
        addNum(3) → median = 2
    """
    def __init__(self):
        # Two heaps: max heap for smaller half, min heap for larger half
        self.small = []  # Max heap (negate values)
        self.large = []  # Min heap
    
    def addNum(self, num: int) -> None:
        """Add number to data structure"""
        # Always add to small first (max heap)
        heapq.heappush(self.small, -num)
        
        # Balance: move largest from small to large
        heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # If large is bigger, move one back to small
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def findMedian(self) -> float:
        """Return median of all numbers"""
        if len(self.small) > len(self.large):
            return -self.small[0]  # Odd count: middle element
        else:
            return (-self.small[0] + self.large[0]) / 2  # Even: average of two middle

print("=" * 60)
print("Pattern 5: Find Median from Data Stream")
print("=" * 60)
print("Problem: Maintain median as numbers arrive one by one")
print("\nHow it works:")
print("  1. Use TWO heaps to split numbers in half")
print("  2. Max heap 'small': stores smaller half (largest at top)")
print("  3. Min heap 'large': stores larger half (smallest at top)")
print("  4. Invariant: len(small) == len(large) or len(small) = len(large)+1")
print("  5. Median: if odd count, top of small; if even, average of both tops")
print("  6. Adding number: balance heaps to maintain invariant")
print("\nExample:")
mf = MedianFinder()
operations = [
    (1, "addNum(1)"),
    (None, "findMedian"),
    (2, "addNum(2)"),
    (None, "findMedian"),
    (3, "addNum(3)"),
    (None, "findMedian")
]
print("  Operations:")
for val, op in operations:
    if val is not None:
        mf.addNum(val)
        print(f"    {op}")
    else:
        median = mf.findMedian()
        print(f"    {op} = {median}")
print()


# Pattern 6: Task Scheduler (different approach using heap)
def least_interval_heap(tasks: List[str], n: int) -> int:
    """
    Minimum intervals to complete tasks with cooldown.
    Time: O(m) where m is total intervals, Space: O(1)
    
    Example:
        Input: tasks = ['A','A','A','B','B','B'], n = 2
        Output: 8
    """
    freq_map = Counter(tasks)
    max_heap = [-freq for freq in freq_map.values()]
    heapq.heapify(max_heap)
    
    time = 0
    
    while max_heap:
        temp = []  # Tasks we process this cycle
        
        # Process up to n+1 tasks (one cycle)
        for _ in range(n + 1):
            if max_heap:
                freq = heapq.heappop(max_heap)
                if freq < -1:  # Still has remaining instances
                    temp.append(freq + 1)
            time += 1
            
            # If no more tasks and no pending, we're done
            if not max_heap and not temp:
                break
        
        # Add back tasks that still have instances
        for freq in temp:
            heapq.heappush(max_heap, freq)
    
    return time

print("=" * 60)
print("Pattern 6: Task Scheduler (Heap Approach)")
print("=" * 60)
print("Problem: Schedule tasks with cooldown between same tasks")
print("\nHow it works:")
print("  1. Count task frequencies, add to max heap")
print("  2. Process in cycles of (n+1) intervals")
print("  3. Each cycle: pick most frequent available tasks")
print("  4. After cycle: add back tasks with remaining instances")
print("  5. Continue until all tasks completed")
print("\nExample:")
tasks = ['A', 'A', 'A', 'B', 'B', 'B']
n = 2
print(f"  Input: tasks = {tasks}, cooldown = {n}")
result = least_interval_heap(tasks, n)
print(f"  Output: {result} intervals")
print(f"  Schedule: A → B → idle → A → B → idle → A → B")
print()


# Pattern 7: Reorganize String
def reorganize_string(s: str) -> str:
    """
    Rearrange string so no adjacent characters are same.
    Time: O(n log k) where k is unique chars, Space: O(k)
    
    Example:
        Input: s = "aab"
        Output: "aba"
        Explanation: "baa" would have adjacent 'a's
    """
    # Count frequencies
    freq_map = Counter(s)
    
    # Max heap: (-frequency, character)
    max_heap = [(-freq, char) for char, freq in freq_map.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev_freq, prev_char = 0, ''
    
    while max_heap:
        # Get most frequent character
        freq, char = heapq.heappop(max_heap)
        result.append(char)
        
        # Add back previous character (now it can be used)
        if prev_freq < 0:
            heapq.heappush(max_heap, (prev_freq, prev_char))
        
        # Update previous (this char can't be used next)
        prev_freq, prev_char = freq + 1, char
    
    # Check if successful
    result_str = ''.join(result)
    return result_str if len(result_str) == len(s) else ""

print("=" * 60)
print("Pattern 7: Reorganize String")
print("=" * 60)
print("Problem: Rearrange string so no two adjacent chars are same")
print("\nHow it works:")
print("  1. Count character frequencies")
print("  2. Use max heap to always pick most frequent char")
print("  3. Pick char, add to result, temporarily exclude it")
print("  4. Add back previous char (now separated by one position)")
print("  5. If we can't place all chars, return empty string")
print("\nExample:")
s = "aab"
print(f"  Input: '{s}'")
result = reorganize_string(s)
print(f"  Output: '{result}'")
print(f"  Process: Pick 'a', then 'a', then 'b' → rearrange → 'aba'")
print()


# Pattern 8: Kth Smallest Element in Sorted Matrix
def kth_smallest_in_matrix(matrix: List[List[int]], k: int) -> int:
    """
    Find kth smallest in row and column sorted matrix.
    Time: O(k log n) where n is matrix dimension
    Space: O(n)
    
    Example:
        Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
        Output: 13
    """
    n = len(matrix)
    
    # Min heap: (value, row, col)
    min_heap = []
    
    # Add first element from each row
    for r in range(min(n, k)):  # Only need to add k rows max
        heapq.heappush(min_heap, (matrix[r][0], r, 0))
    
    count = 0
    result = 0
    
    while min_heap:
        val, r, c = heapq.heappop(min_heap)
        count += 1
        
        if count == k:
            result = val
            break
        
        # Add next element from same row
        if c + 1 < n:
            heapq.heappush(min_heap, (matrix[r][c + 1], r, c + 1))
    
    return result

print("=" * 60)
print("Pattern 8: Kth Smallest in Sorted Matrix")
print("=" * 60)
print("Problem: Find kth smallest in row-column sorted matrix")
print("\nHow it works:")
print("  1. Matrix is sorted: rows left→right, columns top→bottom")
print("  2. Use min heap, start with first element of each row")
print("  3. Pop smallest k times")
print("  4. When popping (r,c), add next element from same row (r,c+1)")
print("  5. kth popped element is the answer")
print("\nExample:")
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
k = 8
print(f"  Input matrix:")
for row in matrix:
    print(f"    {row}")
print(f"  k = {k}")
result = kth_smallest_in_matrix(matrix, k)
print(f"  Output: {result}")
print(f"  Sorted order: 1,5,9,10,11,12,13,13,15")
print(f"  8th smallest: 13")
print()
