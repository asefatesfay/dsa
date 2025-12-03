"""
Linked List Common Patterns
============================

Essential patterns and algorithms using linked lists.
Each pattern includes explanation of how it works.
"""

# Setup: Node class for examples
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def create_linked_list(values):
    """Helper to create linked list from list"""
    if not values:
        return None
    head = Node(values[0])
    current = head
    for val in values[1:]:
        current.next = Node(val)
        current = current.next
    return head

def print_list(head):
    """Helper to print linked list"""
    if not head:
        print("Empty list")
        return
    current = head
    elements = []
    while current:
        elements.append(str(current.data))
        current = current.next
    print(" → ".join(elements) + " → None")


# Pattern 1: Reverse Linked List
print("=" * 60)
print("Pattern 1: Reverse Linked List")
print("=" * 60)
print("""
Problem: Reverse a singly linked list in-place.

How it works:
  1. Use three pointers: prev (None), current (head), next
  2. For each node:
     - Save next node (next = current.next)
     - Reverse pointer (current.next = prev)
     - Move prev forward (prev = current)
     - Move current forward (current = next)
  3. When done, prev is new head
  
Example:
  Original: [1→2→3→4→None]
  Step 1: None←1  2→3→4  (reversed first pointer)
  Step 2: None←1←2  3→4  (reversed second pointer)
  Step 3: None←1←2←3  4  (reversed third pointer)
  Step 4: None←1←2←3←4   (done)
  Result: [4→3→2→1→None]

Time: O(n), Space: O(1)
""")

def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next  # Save next
        current.next = prev       # Reverse pointer
        prev = current            # Move prev forward
        current = next_node       # Move current forward
    
    return prev  # New head

head = create_linked_list([1, 2, 3, 4, 5])
print("Original: ", end="")
print_list(head)
head = reverse_list(head)
print("Reversed: ", end="")
print_list(head)


# Pattern 2: Detect Cycle (Floyd's Cycle Detection)
print("\n" + "=" * 60)
print("Pattern 2: Detect Cycle (Floyd's Algorithm)")
print("=" * 60)
print("""
Problem: Detect if linked list has a cycle.

How it works:
  1. Use two pointers: slow (moves 1 step) and fast (moves 2 steps)
  2. If there's a cycle, fast will eventually catch up to slow
  3. Like runners on a circular track - faster catches slower
  4. If fast reaches None, no cycle exists
  
Example with cycle:
  [1→2→3→4→5]
       ↑     ↓
       └─────┘
  
  slow: 1 → 2 → 3 → 4 → 5 → 3 → 4 → 5
  fast: 1 → 3 → 5 → 4 → 3 → 5 → 4
        They meet at node 3 or 4!

Example without cycle:
  [1→2→3→None]
  fast reaches None, no cycle

Time: O(n), Space: O(1)
""")

def has_cycle(head):
    if not head:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
        
        if slow == fast:
            return True  # Cycle detected
    
    return False  # Reached end, no cycle

# Create list without cycle
head = create_linked_list([1, 2, 3, 4, 5])
print("List without cycle: ", end="")
print_list(head)
print(f"Has cycle? {has_cycle(head)}")

# Create list with cycle (manually for demo)
head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
head.next.next.next = Node(4)
head.next.next.next.next = head.next  # Creates cycle
print("\nList with cycle: 1→2→3→4→2...")
print(f"Has cycle? {has_cycle(head)}")


# Pattern 3: Find Middle of List
print("\n" + "=" * 60)
print("Pattern 3: Find Middle Element")
print("=" * 60)
print("""
Problem: Find the middle node of linked list in one pass.

How it works:
  1. Use slow and fast pointers (both start at head)
  2. Slow moves 1 step, fast moves 2 steps
  3. When fast reaches end, slow is at middle
  4. For even length, returns second middle
  
Example:
  List: [1→2→3→4→5]
  Step 1: slow=1, fast=1
  Step 2: slow=2, fast=3
  Step 3: slow=3, fast=5
  Step 4: fast.next=None, stop
  Middle: 3

Time: O(n), Space: O(1)
""")

def find_middle(head):
    if not head:
        return None
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow  # Slow is at middle

head = create_linked_list([1, 2, 3, 4, 5])
print("List: ", end="")
print_list(head)
middle = find_middle(head)
print(f"Middle element: {middle.data}")

head = create_linked_list([1, 2, 3, 4, 5, 6])
print("\nList: ", end="")
print_list(head)
middle = find_middle(head)
print(f"Middle element: {middle.data}")


# Pattern 4: Merge Two Sorted Lists
print("\n" + "=" * 60)
print("Pattern 4: Merge Two Sorted Lists")
print("=" * 60)
print("""
Problem: Merge two sorted linked lists into one sorted list.

How it works:
  1. Use dummy node to simplify edge cases
  2. Compare heads of both lists
  3. Attach smaller node to result
  4. Move pointer in that list forward
  5. Repeat until one list is empty
  6. Attach remaining list
  
Example:
  List1: 1→3→5
  List2: 2→4→6
  
  Step 1: Compare 1 vs 2, take 1: result→1
  Step 2: Compare 3 vs 2, take 2: result→1→2
  Step 3: Compare 3 vs 4, take 3: result→1→2→3
  Step 4: Compare 5 vs 4, take 4: result→1→2→3→4
  Step 5: Compare 5 vs 6, take 5: result→1→2→3→4→5
  Step 6: Attach rest of list2: result→1→2→3→4→5→6

Time: O(n + m), Space: O(1)
""")

def merge_sorted_lists(l1, l2):
    dummy = Node(0)  # Dummy node simplifies code
    current = dummy
    
    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = l1 if l1 else l2
    
    return dummy.next  # Skip dummy node

l1 = create_linked_list([1, 3, 5, 7])
l2 = create_linked_list([2, 4, 6, 8])
print("List 1: ", end="")
print_list(l1)
print("List 2: ", end="")
print_list(l2)
merged = merge_sorted_lists(l1, l2)
print("Merged: ", end="")
print_list(merged)


# Pattern 5: Remove Nth Node From End
print("\n" + "=" * 60)
print("Pattern 5: Remove Nth Node From End")
print("=" * 60)
print("""
Problem: Remove nth node from the end in one pass.

How it works:
  1. Use two pointers with gap of n nodes
  2. Move first pointer n steps ahead
  3. Move both pointers together until first reaches end
  4. Second pointer is now at node before target
  5. Remove target node
  
Example: Remove 2nd from end in [1→2→3→4→5]
  Step 1: Move first 2 steps: first=3
  Step 2: Move both until first reaches end:
          second=3 (before 4), first=None
  Step 3: Remove node after second
  Result: [1→2→3→5]

Time: O(n), Space: O(1)
""")

def remove_nth_from_end(head, n):
    dummy = Node(0)
    dummy.next = head
    first = dummy
    second = dummy
    
    # Move first n+1 steps ahead
    for _ in range(n + 1):
        if not first:
            return head  # n is larger than list length
        first = first.next
    
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    
    # Remove nth node
    second.next = second.next.next
    
    return dummy.next

head = create_linked_list([1, 2, 3, 4, 5])
print("Original: ", end="")
print_list(head)
head = remove_nth_from_end(head, 2)
print("After removing 2nd from end: ", end="")
print_list(head)


# Pattern 6: Palindrome Linked List
print("\n" + "=" * 60)
print("Pattern 6: Check if Palindrome")
print("=" * 60)
print("""
Problem: Check if linked list is a palindrome.

How it works:
  1. Find middle using slow/fast pointers
  2. Reverse second half of list
  3. Compare first half with reversed second half
  4. If all match, it's a palindrome
  
Example:
  List: [1→2→3→2→1]
  Step 1: Find middle (3)
  Step 2: Reverse second half: [1→2→3] and [1→2]
  Step 3: Compare: 1==1, 2==2, all match
  Result: True

Time: O(n), Space: O(1)
""")

def is_palindrome(head):
    if not head or not head.next:
        return True
    
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    while slow:
        next_node = slow.next
        slow.next = prev
        prev = slow
        slow = next_node
    
    # Compare both halves
    left = head
    right = prev
    while right:  # Only need to check second half
        if left.data != right.data:
            return False
        left = left.next
        right = right.next
    
    return True

head = create_linked_list([1, 2, 3, 2, 1])
print("List: ", end="")
print_list(head)
print(f"Is palindrome? {is_palindrome(head)}")

head = create_linked_list([1, 2, 3, 4, 5])
print("\nList: ", end="")
print_list(head)
print(f"Is palindrome? {is_palindrome(head)}")


# Pattern 7: Intersection of Two Lists
print("\n" + "=" * 60)
print("Pattern 7: Find Intersection Point")
print("=" * 60)
print("""
Problem: Find node where two linked lists intersect.

How it works:
  1. Calculate lengths of both lists
  2. Advance pointer in longer list by difference
  3. Move both pointers together
  4. They'll meet at intersection point
  
Example:
  List A: 1→2→3→
                ↘
                 7→8→9
                ↗
  List B: 4→5→6→
  
  Length A = 6, Length B = 6
  Both start together, meet at node 7

Alternative: Two pointers switching lists
  - When pointer reaches end, switch to other list
  - They'll meet at intersection after same distance

Time: O(n + m), Space: O(1)
""")

def get_intersection(headA, headB):
    if not headA or not headB:
        return None
    
    # Two pointers
    pA = headA
    pB = headB
    
    # When pointer reaches end, switch to other list
    # After at most 2 iterations, they meet at intersection
    while pA != pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA
    
    return pA  # Either intersection or None

# Create intersecting lists
intersection = Node(7)
intersection.next = Node(8)
intersection.next.next = Node(9)

listA = Node(1)
listA.next = Node(2)
listA.next.next = intersection

listB = Node(4)
listB.next = Node(5)
listB.next.next = Node(6)
listB.next.next.next = intersection

print("List A: 1→2→7→8→9")
print("List B: 4→5→6→7→8→9")
print("       (intersect at 7)")
inter = get_intersection(listA, listB)
print(f"Intersection at node: {inter.data if inter else 'None'}")


# Key Insights Summary
print("\n" + "=" * 60)
print("Key Insights")
print("=" * 60)
print("""
1. Reverse: Three pointers (prev, current, next)
2. Cycle Detection: Floyd's algorithm (slow/fast pointers)
3. Find Middle: Fast pointer moves 2x speed
4. Merge Sorted: Dummy node simplifies edge cases
5. Nth From End: Two pointers with n gap
6. Palindrome: Find middle + reverse + compare
7. Intersection: Switch lists when reaching end

Common Techniques:
  - Two Pointers (slow/fast, different speeds)
  - Dummy Node (simplifies head edge cases)
  - Runner Technique (one pointer ahead)
  - In-place Reversal
  
Time Complexity: Most patterns are O(n)
Space Complexity: Most patterns are O(1)
""")
