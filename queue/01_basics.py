"""
Queue - Basics and Implementations
===================================
Queue is a FIFO (First In First Out) data structure.
Operations: enqueue (add), dequeue (remove), front (peek), isEmpty
Time Complexity: All operations O(1)
Space Complexity: O(n)
"""

from collections import deque


# Implementation 1: Using Python List (Simple but not efficient)
class QueueList:
    """Queue implementation using Python list - O(n) dequeue"""
    
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self.items) == 0
    
    def enqueue(self, item):
        """Add item to rear of queue - O(1)"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item - O(n) due to list shift"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop(0)
    
    def front(self):
        """Return front item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def size(self):
        """Return number of items - O(1)"""
        return len(self.items)
    
    def __str__(self):
        """String representation"""
        return f"Queue({self.items})"


# Implementation 2: Using collections.deque (Most Efficient)
class QueueDeque:
    """Queue implementation using collections.deque - O(1) all operations"""
    
    def __init__(self):
        self.items = deque()
    
    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self.items) == 0
    
    def enqueue(self, item):
        """Add item to rear of queue - O(1)"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()
    
    def front(self):
        """Return front item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def size(self):
        """Return number of items - O(1)"""
        return len(self.items)
    
    def __str__(self):
        """String representation"""
        return f"Queue({list(self.items)})"


# Implementation 3: Using Linked List
class Node:
    """Node for linked list implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None

class QueueLinkedList:
    """Queue implementation using linked list - O(1) all operations"""
    
    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0
    
    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return self.front_node is None
    
    def enqueue(self, data):
        """Add item to rear of queue - O(1)"""
        new_node = Node(data)
        
        if self.rear_node is None:
            self.front_node = self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        
        self._size += 1
    
    def dequeue(self):
        """Remove and return front item - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        data = self.front_node.data
        self.front_node = self.front_node.next
        
        if self.front_node is None:
            self.rear_node = None
        
        self._size -= 1
        return data
    
    def front(self):
        """Return front item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front_node.data
    
    def size(self):
        """Return number of items - O(1)"""
        return self._size
    
    def __str__(self):
        """String representation"""
        items = []
        current = self.front_node
        while current:
            items.append(current.data)
            current = current.next
        return f"Queue({items})"


# Implementation 4: Circular Queue (Fixed Size)
class CircularQueue:
    """Circular queue with fixed size"""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front_idx = 0
        self.rear_idx = -1
        self._size = 0
    
    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return self._size == 0
    
    def is_full(self):
        """Check if queue is full - O(1)"""
        return self._size == self.capacity
    
    def enqueue(self, item):
        """Add item to rear of queue - O(1)"""
        if self.is_full():
            raise OverflowError("Queue is full")
        
        self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.items[self.rear_idx] = item
        self._size += 1
    
    def dequeue(self):
        """Remove and return front item - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self.items[self.front_idx]
        self.items[self.front_idx] = None
        self.front_idx = (self.front_idx + 1) % self.capacity
        self._size -= 1
        return item
    
    def front(self):
        """Return front item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[self.front_idx]
    
    def size(self):
        """Return number of items - O(1)"""
        return self._size
    
    def __str__(self):
        """String representation"""
        if self.is_empty():
            return "Queue([])"
        
        result = []
        idx = self.front_idx
        for _ in range(self._size):
            result.append(self.items[idx])
            idx = (idx + 1) % self.capacity
        return f"Queue({result})"


# Demonstration
print("=== Queue Using List (Simple but O(n) dequeue) ===")
queue1 = QueueList()
for i in [1, 2, 3, 4, 5]:
    queue1.enqueue(i)
    print(f"Enqueued {i}: {queue1}")

print(f"Front: {queue1.front()}")
print(f"Size: {queue1.size()}")

while not queue1.is_empty():
    print(f"Dequeued: {queue1.dequeue()}, Queue: {queue1}")

print()

print("=== Queue Using Deque (Recommended - O(1) all ops) ===")
queue2 = QueueDeque()
for char in ['A', 'B', 'C', 'D']:
    queue2.enqueue(char)
    print(f"Enqueued {char}: {queue2}")

print(f"Front: {queue2.front()}")
for _ in range(2):
    print(f"Dequeued: {queue2.dequeue()}, Queue: {queue2}")

print()

print("=== Queue Using Linked List ===")
queue3 = QueueLinkedList()
for i in [10, 20, 30]:
    queue3.enqueue(i)
    print(f"Enqueued {i}: {queue3}")

print(f"Front: {queue3.front()}")
print(f"Dequeued: {queue3.dequeue()}, Queue: {queue3}")

print()

print("=== Circular Queue (Fixed Size) ===")
queue4 = CircularQueue(3)
for i in [1, 2, 3]:
    queue4.enqueue(i)
    print(f"Enqueued {i}: {queue4}")

print(f"Is full: {queue4.is_full()}")
print(f"Dequeued: {queue4.dequeue()}")
queue4.enqueue(4)
print(f"After dequeue and enqueue 4: {queue4}")

print()

# Comparison of implementations
print("=== Implementation Comparison ===")
print("\n1. List Implementation:")
print("   Pros: Simple, easy to understand")
print("   Cons: O(n) dequeue operation (inefficient)")
print()
print("2. Deque Implementation (RECOMMENDED):")
print("   Pros: O(1) for all operations, built-in, optimized")
print("   Cons: None (best choice for most cases)")
print()
print("3. Linked List Implementation:")
print("   Pros: O(1) all operations, no resize needed")
print("   Cons: Extra memory for pointers, more complex")
print()
print("4. Circular Queue:")
print("   Pros: Fixed memory, cache-friendly, O(1) operations")
print("   Cons: Fixed size, can overflow")

print()
print("=== When to Use Queue ===")
print("1. Task scheduling and job processing")
print("2. BFS (Breadth-First Search) traversal")
print("3. Request handling in servers")
print("4. Print job management")
print("5. Message queues and event handling")
print("6. Call center systems")
