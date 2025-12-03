class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None
        self.size = 0
    def is_empty(self):
        return self.size == 0
    
    def push(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
        
        self.head = new_node
        self.size += 1