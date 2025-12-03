"""
Doubly Linked List Implementation
==================================

Each node has references to both next AND previous nodes.
Allows traversal in both directions.
"""

class DNode:
    """
    Doubly Linked Node
    
    Structure:
      prev ← [data] → next
    """
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
    
    def __repr__(self):
        return f"DNode({self.data})"


class DoublyLinkedList:
    """
    Doubly Linked List
    
    Structure:
      None ← [1] ↔ [2] ↔ [3] ↔ [4] → None
      
    Advantages over singly linked:
      - Can traverse backwards
      - Delete node in O(1) if we have node reference
      - Better for certain algorithms (LRU cache)
    
    Disadvantages:
      - More memory (extra pointer per node)
      - More complex pointer updates
    """
    
    def __init__(self):
        self.head = None
        self.tail = None  # Track tail for O(1) append
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def append(self, data):
        """
        Add to end of list
        
        How it works:
          1. Create new node
          2. If empty: head and tail both point to new node
          3. Otherwise:
             - New node's prev = current tail
             - Tail's next = new node
             - Update tail to new node
        
        Time: O(1) - we have tail pointer!
        """
        new_node = DNode(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        print(f"Appended {data}")
    
    def prepend(self, data):
        """
        Add to beginning
        
        How it works:
          1. Create new node
          2. If empty: head and tail both point to new node
          3. Otherwise:
             - New node's next = current head
             - Head's prev = new node
             - Update head to new node
        
        Time: O(1)
        """
        new_node = DNode(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.size += 1
        print(f"Prepended {data}")
    
    def insert_after(self, target_data, new_data):
        """
        Insert after node with target_data
        
        How it works:
          1. Find node with target_data
          2. Create new node
          3. Update four pointers:
             - new.next = current.next
             - new.prev = current
             - current.next.prev = new (if not tail)
             - current.next = new
        
        Example:
          Insert 5 after 2 in [1↔2↔3]
          Step 1: Find node(2)
          Step 2: new.next = node(3), new.prev = node(2)
          Step 3: node(3).prev = new, node(2).next = new
          Result: [1↔2↔5↔3]
        
        Time: O(n) - search for target
        """
        current = self.head
        
        while current:
            if current.data == target_data:
                new_node = DNode(new_data)
                new_node.next = current.next
                new_node.prev = current
                
                if current.next:  # Not inserting after tail
                    current.next.prev = new_node
                else:  # Inserting after tail
                    self.tail = new_node
                
                current.next = new_node
                self.size += 1
                print(f"Inserted {new_data} after {target_data}")
                return True
            current = current.next
        
        print(f"Target {target_data} not found")
        return False
    
    def delete(self, data):
        """
        Delete node with given data
        
        How it works:
          1. Find node to delete
          2. Update surrounding nodes' pointers:
             - prev.next = current.next
             - next.prev = current.prev
          3. Handle special cases (head, tail, only node)
        
        Example:
          Delete 2 from [1↔2↔3]
          node(1).next = node(3)
          node(3).prev = node(1)
          Result: [1↔3]
        
        Time: O(n) - search for node
        
        Note: If we already have node reference, deletion is O(1)!
        """
        if self.is_empty():
            print("List is empty")
            return False
        
        current = self.head
        
        while current:
            if current.data == data:
                # Update previous node
                if current.prev:
                    current.prev.next = current.next
                else:  # Deleting head
                    self.head = current.next
                
                # Update next node
                if current.next:
                    current.next.prev = current.prev
                else:  # Deleting tail
                    self.tail = current.prev
                
                self.size -= 1
                print(f"Deleted {data}")
                return True
            
            current = current.next
        
        print(f"Data {data} not found")
        return False
    
    def delete_node(self, node):
        """
        Delete specific node (when we have reference)
        
        How it works:
          1. We already have the node reference
          2. Just update surrounding pointers
          3. No searching needed!
        
        Time: O(1) - this is the advantage of doubly linked!
        """
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        
        self.size -= 1
    
    def reverse(self):
        """
        Reverse the list
        
        How it works:
          1. Swap prev and next pointers for each node
          2. Swap head and tail
        
        Time: O(n)
        """
        current = self.head
        
        while current:
            # Swap prev and next
            current.prev, current.next = current.next, current.prev
            current = current.prev  # Move to next (which is now prev)
        
        # Swap head and tail
        self.head, self.tail = self.tail, self.head
        print("List reversed")
    
    def display_forward(self):
        """Display from head to tail"""
        if self.is_empty():
            print("List is empty")
            return
        
        current = self.head
        elements = []
        
        while current:
            elements.append(str(current.data))
            current = current.next
        
        print("Forward: None ← " + " ↔ ".join(elements) + " → None")
    
    def display_backward(self):
        """Display from tail to head"""
        if self.is_empty():
            print("List is empty")
            return
        
        current = self.tail
        elements = []
        
        while current:
            elements.append(str(current.data))
            current = current.prev
        
        print("Backward: None ← " + " ↔ ".join(elements) + " → None")
    
    def to_list(self):
        """Convert to Python list"""
        result = []
        current = self.head
        
        while current:
            result.append(current.data)
            current = current.next
        
        return result


# Demonstration
print("=" * 60)
print("Doubly Linked List Operations")
print("=" * 60)

dll = DoublyLinkedList()

# Append elements
print("\n--- Appending Elements ---")
dll.append(1)
dll.append(2)
dll.append(3)
dll.append(4)
dll.display_forward()

# Prepend element
print("\n--- Prepending Element ---")
dll.prepend(0)
dll.display_forward()

# Insert after
print("\n--- Inserting After Node ---")
dll.insert_after(2, 99)
dll.display_forward()

# Bidirectional traversal
print("\n--- Bidirectional Traversal ---")
dll.display_forward()
dll.display_backward()

# Delete
print("\n--- Deleting Elements ---")
dll.delete(99)
dll.display_forward()
dll.delete(0)
dll.display_forward()

# Reverse
print("\n--- Reversing List ---")
dll.reverse()
dll.display_forward()
dll.display_backward()

# Visualizing structure
print("\n" + "=" * 60)
print("Doubly Linked List Structure")
print("=" * 60)
print("""
Singly Linked:
  head → [1]→[2]→[3]→[4]→None
  Can only go forward →

Doubly Linked:
  head                           tail
    ↓                             ↓
  None←[1]↔[2]↔[3]↔[4]→None
  
  Can go both ways ← →
  
Each node has:
  - data: the value
  - next: pointer to next node
  - prev: pointer to previous node

Example of node [2]:
  prev: points to node [1]
  data: 2
  next: points to node [3]
""")

# Comparison
print("\n" + "=" * 60)
print("Singly vs Doubly Linked List")
print("=" * 60)
print("""
                    | Singly  | Doubly
--------------------+---------+--------
Memory per node     | 2 words | 3 words
Append (with tail)  | O(1)    | O(1)
Prepend             | O(1)    | O(1)
Delete (with ref)   | O(n)*   | O(1)
Traverse backward   | ✗       | ✓
Implementation      | Simpler | Complex

* Need previous node to delete, must traverse
  Doubly linked can delete node directly!

Use Doubly Linked when:
  ✓ Need bidirectional traversal
  ✓ Implementing LRU cache
  ✓ Browser history (back/forward)
  ✓ Undo/Redo functionality
  ✓ Delete node given reference only

Use Singly Linked when:
  ✓ Memory is constrained
  ✓ Only need forward traversal
  ✓ Simpler implementation preferred
""")
