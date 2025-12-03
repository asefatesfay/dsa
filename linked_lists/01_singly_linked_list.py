"""
Linked List - Basic Implementation
===================================

A linked list is a linear data structure where elements are stored in nodes.
Each node contains data and a reference (link) to the next node.
"""

class Node:
    """
    Node class - Building block of linked list
    
    How it works:
      1. Each node stores data (value)
      2. Each node has reference to next node
      3. Last node points to None (end of list)
    """
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """
    Singly Linked List Implementation
    
    Structure:
      head → [1|●] → [2|●] → [3|●] → [4|None]
             data next
    
    Operations:
      - append: Add to end
      - prepend: Add to beginning
      - insert: Add at specific position
      - delete: Remove node
      - search: Find node with value
    """
    
    def __init__(self):
        """Initialize empty linked list"""
        self.head = None
        self.size = 0
    
    def is_empty(self):
        """Check if list is empty"""
        return self.head is None
    
    def __len__(self):
        """Return size of list"""
        return self.size
    
    def append(self, data):
        """
        Add node to end of list
        
        How it works:
          1. Create new node with data
          2. If list empty: new node becomes head
          3. If not empty: traverse to last node
          4. Set last node's next to new node
        
        Time: O(n) - need to traverse to end
        """
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Find last node
                current = current.next
            current.next = new_node
        
        self.size += 1
        print(f"Appended {data} to end")
    
    def prepend(self, data):
        """
        Add node to beginning of list
        
        How it works:
          1. Create new node
          2. New node's next points to current head
          3. Update head to new node
        
        Time: O(1) - no traversal needed
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        print(f"Prepended {data} to beginning")
    
    def insert(self, data, position):
        """
        Insert node at specific position (0-indexed)
        
        How it works:
          1. If position 0: same as prepend
          2. Traverse to position-1
          3. New node's next = current's next
          4. Current's next = new node
        
        Example:
          Insert 5 at position 2 in [1→2→3→4]
          1. Traverse to position 1 (node with 2)
          2. new.next = node(3)
          3. node(2).next = new
          Result: [1→2→5→3→4]
        
        Time: O(n) - traverse to position
        """
        if position < 0 or position > self.size:
            print(f"Invalid position {position}")
            return
        
        if position == 0:
            self.prepend(data)
            return
        
        new_node = Node(data)
        current = self.head
        
        # Traverse to position-1
        for _ in range(position - 1):
            current = current.next
        
        # Insert new node
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        print(f"Inserted {data} at position {position}")
    
    def delete(self, data):
        """
        Delete first node with matching data
        
        How it works:
          1. If head matches: update head to next node
          2. Otherwise: traverse to find node
          3. Keep track of previous node
          4. Set previous.next = current.next (bypass node)
        
        Example:
          Delete 3 from [1→2→3→4]
          1. Find node(3), previous is node(2)
          2. node(2).next = node(4)
          Result: [1→2→4]
        
        Time: O(n) - may need to traverse entire list
        """
        if self.is_empty():
            print("List is empty")
            return False
        
        # If head node matches
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            print(f"Deleted {data} from beginning")
            return True
        
        # Search for node
        current = self.head
        prev = None
        
        while current and current.data != data:
            prev = current
            current = current.next
        
        # Node not found
        if current is None:
            print(f"Data {data} not found")
            return False
        
        # Delete node
        prev.next = current.next
        self.size -= 1
        print(f"Deleted {data}")
        return True
    
    def search(self, data):
        """
        Search for node with given data
        
        How it works:
          1. Start at head
          2. Check each node's data
          3. Return True if found, False if reach end
        
        Time: O(n) - may need to check all nodes
        """
        current = self.head
        position = 0
        
        while current:
            if current.data == data:
                print(f"Found {data} at position {position}")
                return True
            current = current.next
            position += 1
        
        print(f"Data {data} not found")
        return False
    
    def get(self, position):
        """
        Get data at specific position
        
        Time: O(n) - traverse to position
        """
        if position < 0 or position >= self.size:
            print(f"Invalid position {position}")
            return None
        
        current = self.head
        for _ in range(position):
            current = current.next
        
        return current.data
    
    def reverse(self):
        """
        Reverse the linked list in-place
        
        How it works:
          1. Use three pointers: prev, current, next
          2. For each node: reverse the next pointer
          3. Update head to last node
        
        Example:
          Original: [1→2→3→4→None]
          Step 1: None←1  2→3→4→None
          Step 2: None←1←2  3→4→None
          Step 3: None←1←2←3  4→None
          Step 4: None←1←2←3←4
          Result: [4→3→2→1→None]
        
        Time: O(n) - single pass through list
        Space: O(1) - only use three pointers
        """
        prev = None
        current = self.head
        
        while current:
            next_node = current.next  # Save next
            current.next = prev       # Reverse pointer
            prev = current            # Move prev forward
            current = next_node       # Move current forward
        
        self.head = prev
        print("List reversed")
    
    def display(self):
        """Display list contents"""
        if self.is_empty():
            print("List is empty")
            return
        
        current = self.head
        elements = []
        
        while current:
            elements.append(str(current.data))
            current = current.next
        
        print(" → ".join(elements) + " → None")
    
    def to_list(self):
        """Convert to Python list"""
        result = []
        current = self.head
        
        while current:
            result.append(current.data)
            current = current.next
        
        return result
    
    def __str__(self):
        """String representation"""
        return str(self.to_list())


# Demonstration
print("=" * 60)
print("Linked List Basic Operations")
print("=" * 60)

# Create linked list
ll = LinkedList()
print(f"\nCreated empty list: {ll}")
print(f"Is empty? {ll.is_empty()}")
print(f"Size: {len(ll)}")

# Append elements
print("\n--- Appending Elements ---")
ll.append(1)
ll.append(2)
ll.append(3)
ll.append(4)
ll.display()

# Prepend element
print("\n--- Prepending Element ---")
ll.prepend(0)
ll.display()

# Insert at position
print("\n--- Inserting Elements ---")
ll.insert(99, 2)  # Insert 99 at position 2
ll.display()

# Search
print("\n--- Searching ---")
ll.search(3)
ll.search(99)
ll.search(100)

# Get by position
print("\n--- Get by Position ---")
print(f"Element at position 0: {ll.get(0)}")
print(f"Element at position 3: {ll.get(3)}")

# Delete
print("\n--- Deleting Elements ---")
ll.delete(99)
ll.display()
ll.delete(0)
ll.display()
ll.delete(4)
ll.display()

# Reverse
print("\n--- Reversing List ---")
ll.display()
ll.reverse()
ll.display()

# Visualizing the structure
print("\n" + "=" * 60)
print("Visualizing Linked List Structure")
print("=" * 60)
print("""
Python List (Array):
  [1, 2, 3, 4]
  - Stored contiguously in memory
  - Direct access by index: O(1)
  - Insert/delete at beginning: O(n) - need to shift elements

Linked List:
  head → [1|●] → [2|●] → [3|●] → [4|None]
         data next
  
  - Nodes scattered in memory
  - Access by index: O(n) - must traverse
  - Insert/delete at beginning: O(1) - just change pointers
  
Each box represents a Node:
  - Left part: data (the value)
  - Right part: next (reference to next node)
  - ● means pointer to next node
  - None means end of list
""")

# Time complexity summary
print("\n" + "=" * 60)
print("Time Complexity Summary")
print("=" * 60)
print("""
Operation         | Array/List | Linked List
------------------+------------+------------
Access by index   | O(1)       | O(n)
Search            | O(n)       | O(n)
Insert beginning  | O(n)       | O(1)
Insert end        | O(1)*      | O(n)**
Insert middle     | O(n)       | O(n)
Delete beginning  | O(n)       | O(1)
Delete end        | O(1)*      | O(n)**
Delete middle     | O(n)       | O(n)

* Amortized time for dynamic array
** O(1) if we maintain tail pointer
""")

# When to use linked lists
print("\n" + "=" * 60)
print("When to Use Linked Lists")
print("=" * 60)
print("""
Use Linked List when:
  ✓ Frequent insertions/deletions at beginning
  ✓ Don't need random access by index
  ✓ Size changes frequently
  ✓ Implementing stack, queue, or other ADTs
  
Use Array/List when:
  ✓ Need fast random access
  ✓ Know size in advance
  ✓ Cache performance matters
  ✓ Mostly read operations
  
Example Use Cases:
  - Undo functionality (doubly linked list)
  - Browser history (doubly linked list)
  - Music playlist
  - Implementing hash table chaining
  - LRU cache (doubly linked list + hash map)
""")

# Common mistakes
print("\n" + "=" * 60)
print("Common Mistakes and Tips")
print("=" * 60)
print("""
1. Forgetting to update head:
   ❌ node.next = head  # Forgot: head = node
   ✓ node.next = head; head = node

2. Losing reference to next node:
   ❌ current.next = current.next.next  # Lost reference!
   ✓ temp = current.next; current.next = temp.next

3. Not handling empty list:
   ❌ current = head; current.next = ...  # What if head is None?
   ✓ if not head: return

4. Off-by-one in traversal:
   ❌ while current.next:  # Stops before last node
   ✓ while current:  # Includes last node

5. Not updating size:
   ❌ Forget to increment/decrement size counter
   ✓ Always update self.size
""")
