"""
Heap - Advanced Patterns
========================
Complex problems and advanced techniques using heaps.
"""

import heapq
from typing import List, Tuple
from collections import defaultdict


# Pattern 1: Sliding Window Median
class SlidingWindowMedian:
    """
    Find median in each sliding window of size k.
    Time: O(n log k), Space: O(k)
    
    Example:
        Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
        Output: [1, -1, -1, 3, 5, 6]
    """
    def __init__(self):
        self.small = []  # Max heap for smaller half
        self.large = []  # Min heap for larger half
    
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        """Find median for each window"""
        result = []
        
        # Helper to add number
        def add_num(num):
            heapq.heappush(self.small, -num)
            heapq.heappush(self.large, -heapq.heappop(self.small))
            if len(self.large) > len(self.small):
                heapq.heappush(self.small, -heapq.heappop(self.large))
        
        # Helper to remove number
        def remove_num(num):
            # Find and remove from appropriate heap
            if num <= -self.small[0]:
                self.small.remove(-num)
                heapq.heapify(self.small)
            else:
                self.large.remove(num)
                heapq.heapify(self.large)
        
        # Helper to get median
        def get_median():
            if len(self.small) > len(self.large):
                return float(-self.small[0])
            else:
                return (-self.small[0] + self.large[0]) / 2.0
        
        # Build first window
        for i in range(k):
            add_num(nums[i])
        result.append(get_median())
        
        # Slide window
        for i in range(k, len(nums)):
            remove_num(nums[i - k])  # Remove leaving element
            add_num(nums[i])  # Add new element
            result.append(get_median())
        
        return result

print("=" * 60)
print("Pattern 1: Sliding Window Median")
print("=" * 60)
print("Problem: Find median in each sliding window")
print("\nHow it works:")
print("  1. Use two heaps (like median finder)")
print("  2. Add k elements to build first window")
print("  3. For each slide: remove leaving element, add new one")
print("  4. Maintain balance between heaps")
print("  5. Calculate median from heap tops")
print("\nExample:")
swm = SlidingWindowMedian()
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(f"  Input: nums = {nums}, k = {k}")
result = swm.medianSlidingWindow(nums, k)
print(f"  Output: {result}")
print(f"  Windows: [1,3,-1]→1, [3,-1,-3]→-1, [-1,-3,5]→-1, etc.")
print()


# Pattern 2: IPO (Maximum Capital)
def findMaximizedCapital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    """
    Maximize capital by selecting up to k projects.
    Time: O(n log n), Space: O(n)
    
    Example:
        Input: k=2, w=0, profits=[1,2,3], capital=[0,1,1]
        Output: 4
        Explanation: Start with w=0, pick project 0 (profit=1, w=1),
                     then pick project 1 or 2 (profit=2, w=3),
                     best is project 2 (profit=3, final w=4)
    """
    # Min heap for available projects by capital requirement
    min_capital = [(c, p) for c, p in zip(capital, profits)]
    heapq.heapify(min_capital)
    
    # Max heap for available projects (we can afford)
    max_profit = []
    
    for _ in range(k):
        # Move all affordable projects to max profit heap
        while min_capital and min_capital[0][0] <= w:
            c, p = heapq.heappop(min_capital)
            heapq.heappush(max_profit, -p)  # Max heap with negation
        
        # If no projects available, stop
        if not max_profit:
            break
        
        # Pick most profitable project
        w += -heapq.heappop(max_profit)
    
    return w

print("=" * 60)
print("Pattern 2: IPO (Maximize Capital)")
print("=" * 60)
print("Problem: Pick up to k projects to maximize capital")
print("        Each project has capital requirement and profit")
print("\nHow it works:")
print("  1. Use two heaps:")
print("     - Min heap: projects sorted by capital requirement")
print("     - Max heap: projects we can currently afford")
print("  2. For each of k iterations:")
print("     - Move all affordable projects to max heap")
print("     - Pick most profitable project")
print("     - Update capital")
print("  3. Greedy: always pick best available option")
print("\nExample:")
k = 2
w = 0
profits = [1, 2, 3]
capital = [0, 1, 1]
print(f"  Input: k={k}, w={w}, profits={profits}, capital={capital}")
result = findMaximizedCapital(k, w, profits, capital)
print(f"  Output: {result}")
print(f"  Step 1: Can afford project 0 (capital=0), pick it, profit=1, w=1")
print(f"  Step 2: Can afford projects 1,2 (capital=1), pick 2, profit=3, w=4")
print()


# Pattern 3: Meeting Rooms II
def minMeetingRooms(intervals: List[List[int]]) -> int:
    """
    Find minimum meeting rooms needed.
    Time: O(n log n), Space: O(n)
    
    Example:
        Input: [[0,30],[5,10],[15,20]]
        Output: 2
        Explanation: [0,30] and [5,10] overlap, need 2 rooms
    """
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap: tracks end times of ongoing meetings
    min_heap = []
    
    for start, end in intervals:
        # If earliest meeting has ended, remove it
        if min_heap and min_heap[0] <= start:
            heapq.heappop(min_heap)
        
        # Add current meeting's end time
        heapq.heappush(min_heap, end)
    
    # Heap size = concurrent meetings = rooms needed
    return len(min_heap)

print("=" * 60)
print("Pattern 3: Meeting Rooms II")
print("=" * 60)
print("Problem: Find minimum meeting rooms needed for all meetings")
print("\nHow it works:")
print("  1. Sort meetings by start time")
print("  2. Use min heap to track end times of active meetings")
print("  3. For each meeting:")
print("     - If earliest meeting ended: remove from heap (free room)")
print("     - Add current meeting to heap (occupy room)")
print("  4. Heap size = concurrent meetings = rooms needed")
print("\nExample:")
intervals = [[0, 30], [5, 10], [15, 20]]
print(f"  Input: {intervals}")
result = minMeetingRooms(intervals)
print(f"  Output: {result} rooms")
print(f"  Timeline:")
print(f"    0-30: Room 1 occupied")
print(f"    5-10: Room 2 occupied (overlaps with Room 1)")
print(f"    15-20: Room 2 reused (10 < 15, room freed)")
print()


# Pattern 4: Merge K Sorted Arrays
def merge_k_sorted_arrays(arrays: List[List[int]]) -> List[int]:
    """
    Merge k sorted arrays into one sorted array.
    Time: O(n log k) where n=total elements, k=num arrays
    Space: O(k)
    
    Example:
        Input: [[1,4,7],[2,5,8],[3,6,9]]
        Output: [1,2,3,4,5,6,7,8,9]
    """
    # Min heap: (value, array_index, element_index)
    min_heap = []
    
    # Add first element from each array
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))
    
    result = []
    
    while min_heap:
        val, arr_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        
        # Add next element from same array
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))
    
    return result

print("=" * 60)
print("Pattern 4: Merge K Sorted Arrays")
print("=" * 60)
print("Problem: Merge k sorted arrays into one sorted array")
print("\nHow it works:")
print("  1. Use min heap to track smallest available element")
print("  2. Initially: add first element from each array")
print("  3. Repeatedly:")
print("     - Pop smallest element from heap")
print("     - Add to result")
print("     - Add next element from same array to heap")
print("  4. Similar to merging k sorted lists")
print("\nExample:")
arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
print(f"  Input: {arrays}")
result = merge_k_sorted_arrays(arrays)
print(f"  Output: {result}")
print()


# Pattern 5: Find K Pairs with Smallest Sums
def kSmallestPairs(nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
    """
    Find k pairs with smallest sums from two arrays.
    Time: O(k log k), Space: O(k)
    
    Example:
        Input: nums1=[1,7,11], nums2=[2,4,6], k=3
        Output: [[1,2],[1,4],[1,6]]
        Explanation: Sums are 3,5,7 (smallest 3)
    """
    if not nums1 or not nums2:
        return []
    
    # Min heap: (sum, index1, index2)
    min_heap = []
    
    # Start with pairs using first element of nums1
    for j in range(min(k, len(nums2))):
        heapq.heappush(min_heap, (nums1[0] + nums2[j], 0, j))
    
    result = []
    
    while min_heap and len(result) < k:
        _, i, j = heapq.heappop(min_heap)
        result.append([nums1[i], nums2[j]])
        
        # Add next pair using next element from nums1
        if i + 1 < len(nums1):
            heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))
    
    return result

print("=" * 60)
print("Pattern 5: K Pairs with Smallest Sums")
print("=" * 60)
print("Problem: Find k pairs (one from each array) with smallest sums")
print("\nHow it works:")
print("  1. Both arrays are sorted")
print("  2. Start with pairs: (nums1[0], nums2[0..k-1])")
print("  3. Use min heap to track pairs by sum")
print("  4. For each pair (i,j) popped:")
print("     - Add to result")
print("     - Add next pair (i+1, j) to heap")
print("  5. This explores pairs in increasing sum order")
print("\nExample:")
nums1 = [1, 7, 11]
nums2 = [2, 4, 6]
k = 3
print(f"  Input: nums1={nums1}, nums2={nums2}, k={k}")
result = kSmallestPairs(nums1, nums2, k)
print(f"  Output: {result}")
print(f"  Sums: [1,2]=3, [1,4]=5, [1,6]=7")
print()


# Pattern 6: Trapping Rain Water II (3D version)
def trapRainWater(heightMap: List[List[int]]) -> int:
    """
    Calculate trapped rain water in 3D elevation map.
    Time: O(mn log(mn)), Space: O(mn)
    
    Example:
        Input: [[1,4,3,1,3,2],
                [3,2,1,3,2,4],
                [2,3,3,2,3,1]]
        Output: 4
    """
    if not heightMap or not heightMap[0]:
        return 0
    
    m, n = len(heightMap), len(heightMap[0])
    visited = [[False] * n for _ in range(m)]
    
    # Min heap: (height, row, col)
    min_heap = []
    
    # Add all border cells to heap
    for i in range(m):
        for j in range(n):
            if i == 0 or i == m-1 or j == 0 or j == n-1:
                heapq.heappush(min_heap, (heightMap[i][j], i, j))
                visited[i][j] = True
    
    water = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Process from outside to inside
    while min_heap:
        h, r, c = heapq.heappop(min_heap)
        
        # Check neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                # Water level is determined by minimum surrounding height
                water += max(0, h - heightMap[nr][nc])
                
                # Add neighbor with max of its height and current water level
                heapq.heappush(min_heap, (max(h, heightMap[nr][nc]), nr, nc))
                visited[nr][nc] = True
    
    return water

print("=" * 60)
print("Pattern 6: Trapping Rain Water II (3D)")
print("=" * 60)
print("Problem: Calculate trapped water in 3D elevation map")
print("\nHow it works:")
print("  1. Water flows from outside to inside")
print("  2. Start with all border cells in min heap")
print("  3. Process cells from lowest to highest")
print("  4. For each cell: water level = min surrounding height")
print("  5. If cell lower than water level: trap water")
print("  6. Add neighbors to heap with updated water level")
print("\nExample:")
heightMap = [
    [1, 4, 3, 1, 3, 2],
    [3, 2, 1, 3, 2, 4],
    [2, 3, 3, 2, 3, 1]
]
print(f"  Input elevation map:")
for row in heightMap:
    print(f"    {row}")
result = trapRainWater(heightMap)
print(f"  Output: {result} units of water")
print()


# Pattern 7: Smallest Range Covering K Lists
def smallestRange(nums: List[List[int]]) -> List[int]:
    """
    Find smallest range that includes at least one from each list.
    Time: O(n log k) where n=total elements, k=num lists
    Space: O(k)
    
    Example:
        Input: [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
        Output: [20,24]
        Explanation: Range contains 24 from list1, 20 from list2, 22 from list3
    """
    # Min heap: (value, list_index, element_index)
    min_heap = []
    current_max = float('-inf')
    
    # Add first element from each list
    for i, lst in enumerate(nums):
        heapq.heappush(min_heap, (lst[0], i, 0))
        current_max = max(current_max, lst[0])
    
    # Track best range
    range_start, range_end = 0, float('inf')
    
    while min_heap:
        current_min, list_idx, elem_idx = heapq.heappop(min_heap)
        
        # Update best range if current is smaller
        if current_max - current_min < range_end - range_start:
            range_start, range_end = current_min, current_max
        
        # If we can't add more from this list, done
        if elem_idx + 1 == len(nums[list_idx]):
            break
        
        # Add next element from same list
        next_val = nums[list_idx][elem_idx + 1]
        heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
        current_max = max(current_max, next_val)
    
    return [range_start, range_end]

print("=" * 60)
print("Pattern 7: Smallest Range Covering K Lists")
print("=" * 60)
print("Problem: Find smallest range with at least one element from each list")
print("\nHow it works:")
print("  1. Start with first element from each list")
print("  2. Track current min (heap top) and current max")
print("  3. Current range = [min, max]")
print("  4. Try to shrink range by advancing smallest element")
print("  5. Pop min, add next from same list, update max")
print("  6. Continue until one list exhausted")
print("\nExample:")
nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
print(f"  Input: {nums}")
result = smallestRange(nums)
print(f"  Output: {result}")
print(f"  Range [20,24] contains: 24 from list1, 20 from list2, 22 from list3")
print()
