"""
Stack - Basics and Implementations
===================================
Stack is a LIFO (Last In First Out) data structure.
Operations: push (add), pop (remove), peek (view top), isEmpty
Time Complexity: All operations O(1)
Space Complexity: O(n)
"""

# Implementation 1: Using Python List (Most Common)
class StackList:
    """Stack implementation using Python list"""
    
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return len(self.items) == 0
    
    def push(self, item):
        """Add item to top of stack - O(1)"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Return top item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def size(self):
        """Return number of items - O(1)"""
        return len(self.items)
    
    def __str__(self):
        """String representation"""
        return f"Stack({self.items})"


# Implementation 2: Using Linked List
class Node:
    """Node for linked list implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None

class StackLinkedList:
    """Stack implementation using linked list"""
    
    def __init__(self):
        self.head = None
        self._size = 0
    
    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return self.head is None
    
    def push(self, data):
        """Add item to top of stack - O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def pop(self):
        """Remove and return top item - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data
    
    def peek(self):
        """Return top item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.head.data
    
    def size(self):
        """Return number of items - O(1)"""
        return self._size
    
    def __str__(self):
        """String representation"""
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return f"Stack({items})"


# Demonstration
print("=== Stack Using List ===")
stack1 = StackList()
print(f"Is empty: {stack1.is_empty()}")

# Push elements
for i in [1, 2, 3, 4, 5]:
    stack1.push(i)
    print(f"Pushed {i}: {stack1}")

print(f"Size: {stack1.size()}")
print(f"Peek: {stack1.peek()}")

# Pop elements
while not stack1.is_empty():
    print(f"Popped: {stack1.pop()}, Stack: {stack1}")

print()

print("=== Stack Using Linked List ===")
stack2 = StackLinkedList()

# Push elements
for char in ['A', 'B', 'C', 'D']:
    stack2.push(char)
    print(f"Pushed {char}: {stack2}")

print(f"Size: {stack2.size()}")
print(f"Peek: {stack2.peek()}")

# Pop elements
for _ in range(2):
    print(f"Popped: {stack2.pop()}, Stack: {stack2}")

print()

# Comparison of implementations
print("=== Implementation Comparison ===")
print("List Implementation:")
print("  Pros: Simple, built-in operations, dynamic sizing")
print("  Cons: May have occasional O(n) resize operations")
print()
print("Linked List Implementation:")
print("  Pros: No resize operations, truly O(1) for all ops")
print("  Cons: Extra memory for node pointers, more complex")
print()

# When to use which?
print("=== When to Use Stack ===")
print("1. Function call management (call stack)")
print("2. Undo/Redo functionality")
print("3. Expression evaluation and syntax parsing")
print("4. Backtracking algorithms (DFS, maze solving)")
print("5. Browser history (back button)")
print("6. Parentheses/bracket matching")
