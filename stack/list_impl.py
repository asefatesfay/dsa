class Stack:
    def __init__(self):
        self.stack = []
    def is_empty(self):
        return len(self.stack) == 0
    
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if self.is_empty():
            return "Stack is empty"
        return self.stack.pop()
    def peek(self):
        if self.is_empty():
            return "Stack is empty"
        return self.stack[-1]
    def size(self):
        return len(self.stack)