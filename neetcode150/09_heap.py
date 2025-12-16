"""
NeetCode 150 - Heap / Priority Queue
=====================================
Min/Max heap problems (7 problems).
"""

import heapq
from collections import defaultdict, Counter


# PATTERN: Min Heap
class KthLargest:
    """
    Kth Largest Element in a Stream.
    
    Pattern: Min heap of size k
    
    Algorithm Steps:
    1. Maintain min heap of k largest elements
    2. Top of heap is kth largest
    3. Add new element: if larger than top, push and pop
    
    Time: O(log k) per add, Space: O(k)
    """
    
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        
        # Keep only k largest
        while len(self.heap) > k:
            heapq.heappop(self.heap)
    
    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


# PATTERN: Max Heap (Negation)
def last_stone_weight(stones):
    """
    Last Stone Weight - smash two heaviest stones.
    
    Pattern: Max heap (negate values for Python min heap)
    
    Time: O(n log n), Space: O(n)
    """
    heap = [-stone for stone in stones]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))
    
    return -heap[0] if heap else 0


# PATTERN: Min Heap with Custom Key
def k_closest(points, k):
    """
    K Closest Points to Origin.
    
    Pattern: Min heap with distance
    
    Time: O(n log k) with size-k heap, Space: O(k)
    """
    heap = []
    
    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(heap, (dist, x, y))
    
    result = []
    for _ in range(k):
        dist, x, y = heapq.heappop(heap)
        result.append([x, y])
    
    return result


# PATTERN: Quick Select (Alternative to Heap)
def find_kth_largest(nums, k):
    """
    Kth Largest Element in an Array.
    
    Pattern: Quick select (or max heap)
    
    Time: O(n) average, O(n^2) worst, Space: O(1)
    """
    k = len(nums) - k  # Convert to kth smallest
    
    def quick_select(left, right):
        pivot = nums[right]
        p = left
        
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1
        
        nums[p], nums[right] = nums[right], nums[p]
        
        if p < k:
            return quick_select(p + 1, right)
        elif p > k:
            return quick_select(left, p - 1)
        else:
            return nums[p]
    
    return quick_select(0, len(nums) - 1)


# PATTERN: Greedy + Sorting
def least_interval(tasks, n):
    """
    Task Scheduler - minimize idle time between same tasks.
    
    Pattern: Max heap + cooling tracking
    
    Algorithm Steps:
    1. Count task frequencies
    2. Process most frequent task first
    3. Track cooling period for each task
    4. Use max heap for available tasks
    
    Time: O(m) where m = total intervals, Space: O(26)
    """
    from collections import deque
    
    count = Counter(tasks)
    max_heap = [-cnt for cnt in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    queue = deque()  # (count, idle_time)
    
    while max_heap or queue:
        time += 1
        
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)  # Process task
            if cnt:
                queue.append((cnt, time + n))
        
        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])
    
    return time


# PATTERN: Multiple Data Structures
class Twitter:
    """
    Design Twitter - post tweets and get news feed.
    
    Pattern: Hash map + min heap
    
    Operations:
    - postTweet: O(1)
    - getNewsFeed: O(k log k) where k = followees
    - follow: O(1)
    - unfollow: O(1)
    """
    
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)  # user -> [(time, tweetId)]
        self.following = defaultdict(set)  # user -> set of followees
    
    def post_tweet(self, user_id, tweet_id):
        self.tweets[user_id].append((self.time, tweet_id))
        self.time -= 1  # Negative for max heap
    
    def get_news_feed(self, user_id):
        """Get 10 most recent tweets from user and followees."""
        heap = []
        
        # Add user's own tweets
        if user_id in self.tweets:
            index = len(self.tweets[user_id]) - 1
            time, tweet_id = self.tweets[user_id][index]
            heapq.heappush(heap, (time, tweet_id, user_id, index))
        
        # Add followees' tweets
        for followee_id in self.following[user_id]:
            if followee_id in self.tweets:
                index = len(self.tweets[followee_id]) - 1
                time, tweet_id = self.tweets[followee_id][index]
                heapq.heappush(heap, (time, tweet_id, followee_id, index))
        
        result = []
        while heap and len(result) < 10:
            time, tweet_id, uid, index = heapq.heappop(heap)
            result.append(tweet_id)
            
            if index > 0:
                index -= 1
                time, tweet_id = self.tweets[uid][index]
                heapq.heappush(heap, (time, tweet_id, uid, index))
        
        return result
    
    def follow(self, follower_id, followee_id):
        if follower_id != followee_id:
            self.following[follower_id].add(followee_id)
    
    def unfollow(self, follower_id, followee_id):
        self.following[follower_id].discard(followee_id)


# PATTERN: Two Heaps
class MedianFinder:
    """
    Find Median from Data Stream.
    
    Pattern: Two heaps (max heap for small half, min heap for large half)
    
    Algorithm Steps:
    1. Max heap stores smaller half (negated values)
    2. Min heap stores larger half
    3. Keep heaps balanced (size diff <= 1)
    4. Median is top of larger heap or average of both tops
    
    Operations:
    - addNum: O(log n)
    - findMedian: O(1)
    Space: O(n)
    """
    
    def __init__(self):
        self.small = []  # Max heap (negated)
        self.large = []  # Min heap
    
    def add_num(self, num):
        # Add to max heap (small half)
        heapq.heappush(self.small, -num)
        
        # Move largest from small to large
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2


if __name__ == "__main__":
    print("=== NeetCode 150 - Heap / Priority Queue ===\n")
    
    # Test KthLargest
    print("Test 1: Kth Largest Element in Stream")
    kth_largest = KthLargest(3, [4, 5, 8, 2])
    print(f"Add 3: {kth_largest.add(3)}")
    print(f"Add 5: {kth_largest.add(5)}")
    print(f"Add 10: {kth_largest.add(10)}")
    print(f"Add 9: {kth_largest.add(9)}")
    
    # Test last_stone_weight
    print("\nTest 2: Last Stone Weight")
    print(f"Stones [2,7,4,1,8,1]: {last_stone_weight([2, 7, 4, 1, 8, 1])}")
    
    # Test k_closest
    print("\nTest 3: K Closest Points")
    points = [[1, 3], [-2, 2], [5, 8], [0, 1]]
    print(f"3 closest to origin: {k_closest(points, 3)}")
    
    # Test find_kth_largest
    print("\nTest 4: Kth Largest Element")
    print(f"2nd largest in [3,2,1,5,6,4]: {find_kth_largest([3, 2, 1, 5, 6, 4], 2)}")
    
    # Test least_interval
    print("\nTest 5: Task Scheduler")
    print(f"Tasks ['A','A','A','B','B','B'], n=2: {least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 2)}")
    
    # Test MedianFinder
    print("\nTest 6: Find Median from Data Stream")
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    print(f"Median after [1,2]: {mf.find_median()}")
    mf.add_num(3)
    print(f"Median after [1,2,3]: {mf.find_median()}")
