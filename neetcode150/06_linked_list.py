"""
NeetCode 150 - Linked List
===========================
Linked list manipulation and patterns.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# PATTERN: In-place Reversal
def reverse_list(head):
    """
    Reverse Linked List.
    
    Pattern: Three-pointer reversal
    
    Algorithm Steps:
    1. prev = None, curr = head
    2. Save next: next_temp = curr.next
    3. Reverse: curr.next = prev
    4. Move pointers: prev = curr, curr = next_temp
    
    Time: O(n), Space: O(1)
    """
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    return prev


# PATTERN: Two Pointers (Merge)
def merge_two_lists(l1, l2):
    """
    Merge Two Sorted Lists.
    
    Pattern: Dummy node + two pointers
    
    Time: O(m + n), Space: O(1)
    """
    dummy = ListNode()
    curr = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    curr.next = l1 or l2
    return dummy.next


# PATTERN: Fast/Slow Pointers + Reversal
def reorder_list(head):
    """
    Reorder List - L0→L1→...→Ln-1→Ln to L0→Ln→L1→Ln-1→L2→Ln-2...
    
    Pattern: Find middle + Reverse second half + Merge
    
    Algorithm Steps:
    1. Find middle using slow/fast pointers
    2. Reverse second half
    3. Merge two halves alternately
    
    Example: 1→2→3→4→5
    - Split: 1→2→3 and 4→5
    - Reverse: 1→2→3 and 5→4
    - Merge: 1→5→2→4→3
    
    Time: O(n), Space: O(1)
    """
    if not head or not head.next:
        return
    
    # Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    second = slow.next
    slow.next = None
    prev = None
    while second:
        next_temp = second.next
        second.next = prev
        prev = second
        second = next_temp
    
    # Merge
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2


# PATTERN: Fast/Slow Pointers (Remove Nth)
def remove_nth_from_end(head, n):
    """
    Remove Nth Node From End of List.
    
    Pattern: Two pointers with n gap
    
    Algorithm Steps:
    1. Create dummy node before head
    2. Move fast pointer n+1 steps ahead
    3. Move both pointers until fast reaches end
    4. Remove node: slow.next = slow.next.next
    
    Time: O(n), Space: O(1)
    """
    dummy = ListNode(0, head)
    slow = fast = dummy
    
    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        slow = slow.next
        fast = fast.next
    
    # Remove node
    slow.next = slow.next.next
    return dummy.next


# PATTERN: Hash Map
def copy_random_list(head):
    """
    Copy List with Random Pointer.
    
    Pattern: Hash map old → new nodes
    
    Algorithm Steps:
    1. First pass: create all nodes, store in map
    2. Second pass: connect next and random pointers
    
    Time: O(n), Space: O(n)
    """
    if not head:
        return None
    
    old_to_new = {}
    
    # First pass: create nodes
    curr = head
    while curr:
        old_to_new[curr] = ListNode(curr.val)
        curr = curr.next
    
    # Second pass: connect pointers
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next
    
    return old_to_new[head]


# PATTERN: Elementary Math with Carry
def add_two_numbers(l1, l2):
    """
    Add Two Numbers - linked lists represent reversed numbers.
    
    Pattern: Elementary addition with carry
    
    Example: 342 + 465 = 807
    - Lists: 2→4→3 + 5→6→4
    - Result: 7→0→8
    
    Time: O(max(m,n)), Space: O(max(m,n))
    """
    dummy = ListNode()
    curr = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        
        curr = curr.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next


# PATTERN: Fast/Slow Pointers (Floyd's Cycle Detection)
def has_cycle(head):
    """
    Linked List Cycle.
    
    Pattern: Floyd's cycle detection (tortoise and hare)
    
    Algorithm Steps:
    1. Slow moves 1 step, fast moves 2 steps
    2. If they meet, cycle exists
    
    Time: O(n), Space: O(1)
    """
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False


# PATTERN: Floyd's Cycle Detection (Modified)
def find_duplicate(nums):
    """
    Find the Duplicate Number.
    
    Pattern: Floyd's cycle detection on array
    
    Algorithm Steps:
    1. Treat array as linked list where nums[i] points to nums[nums[i]]
    2. Find cycle using slow/fast pointers
    3. Find cycle entrance (duplicate)
    
    Time: O(n), Space: O(1)
    """
    slow = fast = nums[0]
    
    # Find intersection point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # Find entrance to cycle (duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow


# PATTERN: Hash Map + Doubly Linked List
class LRUCache:
    """
    LRU Cache - Least Recently Used cache.
    
    Pattern: Hash map + Doubly linked list
    
    Design:
    - Hash map: key → node for O(1) access
    - DLL: maintain LRU order (most recent at tail)
    """
    
    class Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = self.Node()  # Dummy head
        self.tail = self.Node()  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_tail(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = self.Node(key, value)
        self.cache[key] = node
        self._add_to_tail(node)
        
        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]


# PATTERN: Heap (Min Heap)
def merge_k_lists(lists):
    """
    Merge K Sorted Lists.
    
    Pattern: Min heap
    
    Time: O(n log k) where n = total nodes, Space: O(k)
    """
    import heapq
    
    heap = []
    dummy = ListNode()
    curr = dummy
    
    # Add first node of each list to heap
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    # Extract min and add next node from same list
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next


# PATTERN: Iterative Reversal in Groups
def reverse_k_group(head, k):
    """
    Reverse Nodes in k-Group.
    
    Pattern: Iterative reversal in k-sized groups
    
    Time: O(n), Space: O(1)
    """
    def get_length(node):
        length = 0
        while node:
            length += 1
            node = node.next
        return length
    
    def reverse_group(start, k):
        prev, curr = None, start
        for _ in range(k):
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev, start, curr
    
    length = get_length(head)
    dummy = ListNode(0, head)
    prev_group_end = dummy
    
    while length >= k:
        group_start = prev_group_end.next
        new_group_start, new_group_end, next_group_start = reverse_group(group_start, k)
        
        prev_group_end.next = new_group_start
        new_group_end.next = next_group_start
        prev_group_end = new_group_end
        length -= k
    
    return dummy.next


if __name__ == "__main__":
    print("=== NeetCode 150 - Linked List ===\n")
    
    # Helper to create list
    def create_list(vals):
        dummy = ListNode()
        curr = dummy
        for val in vals:
            curr.next = ListNode(val)
            curr = curr.next
        return dummy.next
    
    # Helper to print list
    def print_list(head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        return vals
    
    # Reverse List
    head = create_list([1, 2, 3, 4, 5])
    print(f"Reverse List [1,2,3,4,5]: {print_list(reverse_list(head))}")
    
    # Merge Two Lists
    l1 = create_list([1, 2, 4])
    l2 = create_list([1, 3, 4])
    print(f"Merge Two Lists: {print_list(merge_two_lists(l1, l2))}")
    
    # LRU Cache
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(f"LRU get(1): {lru.get(1)}")
    lru.put(3, 3)
    print(f"LRU get(2): {lru.get(2)}")
    
    # Find Duplicate
    print(f"Find Duplicate [1,3,4,2,2]: {find_duplicate([1, 3, 4, 2, 2])}")
