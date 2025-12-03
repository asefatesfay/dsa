"""
Stack - Common Operations and Patterns
=======================================
Essential operations and patterns used in stack problems.
"""

from typing import List, Optional


class Stack:
    """Simple stack implementation for examples"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


# Pattern 1: Reversing a sequence
def reverse_string(s: str) -> str:
    """
    Reverse a string using stack.
    Time: O(n), Space: O(n)
    
    Example:
        Input: "HELLO"
        Output: "OLLEH"
        Explanation: Push all chars, then pop in reverse order
    """
    stack = Stack()
    
    # Push all characters
    for char in s:
        stack.push(char)
    
    # Pop all characters
    result = ""
    while not stack.is_empty():
        result += stack.pop()
    
    return result

print("=" * 60)
print("Pattern 1: Reversing a Sequence")
print("=" * 60)
print("Problem: Reverse a string using LIFO property of stack")
print("\nHow it works:")
print("  1. Push all characters onto stack one by one")
print("  2. Stack stores them in order: bottom to top")
print("  3. Pop all characters: LIFO gives reverse order")
print("  4. Example: 'ABC' -> push A, B, C -> pop C, B, A")
print("\nExample:")
print(f"  Input: 'HELLO'")
print(f"  Output: '{reverse_string('HELLO')}'")
print(f"  Process: H->E->L->L->O (push) | O->L->L->E->H (pop)")
print()


# Pattern 2: Balanced Parentheses
def is_balanced(expression: str) -> bool:
    """
    Check if parentheses/brackets are balanced.
    Time: O(n), Space: O(n)
    
    Example:
        Input: "([{}])"
        Output: True
        Explanation: Each opening bracket has matching closing bracket
        
        Input: "([)]"
        Output: False
        Explanation: Brackets are interleaved incorrectly
    """
    stack = Stack()
    opening = "({["
    closing = ")}]"
    pairs = {'(': ')', '{': '}', '[': ']'}
    
    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty():
                return False
            top = stack.pop()
            if pairs[top] != char:
                return False
    
    return stack.is_empty()

print("=" * 60)
print("Pattern 2: Balanced Parentheses/Brackets")
print("=" * 60)
print("Problem: Check if brackets are properly balanced and nested")
print("\nHow it works:")
print("  1. Push every opening bracket onto stack")
print("  2. When closing bracket found: check stack top")
print("  3. Stack top must be matching opening bracket")
print("  4. Pop the matching opening bracket")
print("  5. At end: stack should be empty (all matched)")
print("  6. Why stack? Last opened must be first closed (LIFO)")
print("\nExamples:")
test_cases = ['(())', '[]{}', '([)]', '((())']
for expr in test_cases:
    result = is_balanced(expr)
    status = "✓ Valid" if result else "✗ Invalid"
    print(f"  '{expr}' -> {status}")
print()


# Pattern 3: Next Greater Element
def next_greater_element(arr: List[int]) -> List[int]:
    """
    Find next greater element for each element.
    Time: O(n), Space: O(n)
    
    Example:
        Input: [4, 5, 2, 25, 7, 8]
        Output: [5, 25, 25, -1, 8, -1]
        Explanation:
        4 -> 5 (next greater)
        5 -> 25 (skip 2, find 25)
        2 -> 25
        25 -> -1 (no greater element)
        7 -> 8
        8 -> -1 (no greater element)
    """
    n = len(arr)
    result = [-1] * n
    stack = Stack()
    
    # Traverse from right to left
    for i in range(n - 1, -1, -1):
        # Pop elements smaller than current
        while not stack.is_empty() and stack.peek() <= arr[i]:
            stack.pop()
        
        # Top of stack is next greater element
        if not stack.is_empty():
            result[i] = stack.peek()
        
        # Push current element
        stack.push(arr[i])
    
    return result

print("=" * 60)
print("Pattern 3: Next Greater Element")
print("=" * 60)
print("Problem: Find the first element to the right that is greater")
print("\nHow it works:")
print("  1. Traverse array from RIGHT to LEFT")
print("  2. Stack stores potential 'next greater' candidates")
print("  3. For each element: pop smaller elements (can't be answer)")
print("  4. Stack top is next greater (or stack is empty = -1)")
print("  5. Push current element (might be answer for left elements)")
print("  6. Stack stays in decreasing order")
print("\nExample:")
arr = [4, 5, 2, 25, 7, 8]
result = next_greater_element(arr)
print(f"  Input: {arr}")
print(f"  Output: {result}")
for i in range(len(arr)):
    nge = result[i] if result[i] != -1 else "none"
    print(f"    {arr[i]} -> {nge}")
print()


# Pattern 4: Stock Span Problem
def calculate_span(prices: List[int]) -> List[int]:
    """
    Calculate span of stock prices.
    Span = number of consecutive days before current day with price <= current price
    Time: O(n), Space: O(n)
    
    Example:
        Input: [100, 80, 60, 70, 60, 75, 85]
        Output: [1, 1, 1, 2, 1, 4, 6]
        Explanation:
        Day 0 (100): span = 1 (only itself)
        Day 1 (80): span = 1 (80 < 100)
        Day 2 (60): span = 1 (60 < 80)
        Day 3 (70): span = 2 (70 > 60, 70 < 80)
        Day 4 (60): span = 1 (60 < 70)
        Day 5 (75): span = 4 (75 > 60,70,60,75)
        Day 6 (85): span = 6 (85 > all previous except 100)
    """
    n = len(prices)
    spans = [1] * n
    stack = Stack()
    
    for i in range(n):
        # Pop while current price is greater
        while not stack.is_empty() and prices[stack.peek()] <= prices[i]:
            stack.pop()
        
        # Calculate span
        if stack.is_empty():
            spans[i] = i + 1
        else:
            spans[i] = i - stack.peek()
        
        stack.push(i)
    
    return spans

print("=" * 60)
print("Pattern 4: Stock Span Problem")
print("=" * 60)
print("Problem: Calculate consecutive days with price <= current price")
print("\nHow it works:")
print("  1. Stack stores indices of days")
print("  2. For each day: pop days with lower/equal prices")
print("  3. These popped days can't affect future spans")
print("  4. Span = current day - index at top of stack")
print("  5. If stack empty: span = all days so far")
print("  6. Push current day index to stack")
print("\nExample:")
prices = [100, 80, 60, 70, 60, 75, 85]
spans = calculate_span(prices)
print(f"  Input: {prices}")
print(f"  Output: {spans}")
for i in range(len(prices)):
    print(f"    Day {i}: price={prices[i]} -> span={spans[i]}")
print()


# Pattern 5: Evaluate Postfix Expression
def evaluate_postfix(expression: str) -> int:
    """
    Evaluate postfix (RPN) expression.
    Example: "23+" = 2 + 3 = 5
    Time: O(n), Space: O(n)
    
    Example:
        Input: "23*5+"
        Output: 11
        Explanation:
        Step 1: Push 2
        Step 2: Push 3
        Step 3: Operator *, pop 3 and 2, push 2*3=6
        Step 4: Push 5
        Step 5: Operator +, pop 5 and 6, push 6+5=11
    """
    stack = Stack()
    operators = {'+', '-', '*', '/'}
    
    for char in expression:
        if char.isdigit():
            stack.push(int(char))
        elif char in operators:
            b = stack.pop()
            a = stack.pop()
            
            if char == '+':
                stack.push(a + b)
            elif char == '-':
                stack.push(a - b)
            elif char == '*':
                stack.push(a * b)
            elif char == '/':
                stack.push(a // b)
    
    return stack.pop()

print("=" * 60)
print("Pattern 5: Evaluate Postfix Expression (RPN)")
print("=" * 60)
print("Problem: Evaluate postfix notation expressions")
print("\nHow it works:")
print("  1. Scan expression left to right")
print("  2. If operand (number): push to stack")
print("  3. If operator: pop two operands")
print("  4. Apply operator: second_popped operator first_popped")
print("  5. Push result back to stack")
print("  6. Final stack value is the answer")
print("  7. Example '23+': push 2, push 3, pop both, push 2+3=5")
print("\nExamples:")
examples = [('23+', '(2 + 3)'), ('23*5+', '(2 * 3) + 5'), ('52/3*', '(5 / 2) * 3')]
for postfix, infix in examples:
    result = evaluate_postfix(postfix)
    print(f"  '{postfix}' = {infix} = {result}")
print()


# Pattern 6: Infix to Postfix Conversion
def infix_to_postfix(expression: str) -> str:
    """
    Convert infix expression to postfix.
    Time: O(n), Space: O(n)
    
    Example:
        Input: "(A+B)*C"
        Output: "AB+C*"
        Explanation:
        - Process (A+B) first, gives AB+
        - Then multiply by C, gives AB+C*
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = Stack()
    result = []
    
    for char in expression:
        if char.isalnum():
            result.append(char)
        elif char == '(':
            stack.push(char)
        elif char == ')':
            while not stack.is_empty() and stack.peek() != '(':
                result.append(stack.pop())
            stack.pop()  # Remove '('
        else:  # Operator
            while (not stack.is_empty() and 
                   stack.peek() != '(' and
                   precedence.get(stack.peek(), 0) >= precedence.get(char, 0)):
                result.append(stack.pop())
            stack.push(char)
    
    while not stack.is_empty():
        result.append(stack.pop())
    
    return ''.join(result)

print("=" * 60)
print("Pattern 6: Infix to Postfix Conversion")
print("=" * 60)
print("Problem: Convert standard notation to postfix notation")
print("\nHow it works:")
print("  1. Operands: add directly to output")
print("  2. '(': push to stack (marks start of subexpression)")
print("  3. ')': pop until '(' (end of subexpression)")
print("  4. Operator: pop higher/equal precedence operators first")
print("     Then push current operator")
print("  5. At end: pop all remaining operators")
print("  6. Stack ensures precedence and left-to-right order")
print("\nExamples:")
examples = ['A+B', 'A+B*C', '(A+B)*C', 'A+B*C-D']
for infix in examples:
    postfix = infix_to_postfix(infix)
    print(f"  '{infix}' -> '{postfix}'")
print()


# Pattern 7: Min Stack (Stack with getMin operation)
class MinStack:
    """
    Stack that supports getMin() in O(1) time.
    
    Example:
        Operations: push(5), push(2), push(8), push(1), getMin()
        Output: 1
        Explanation: Maintains auxiliary stack tracking minimums
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> int:
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        return self.stack.pop()
    
    def top(self) -> int:
        return self.stack[-1]
    
    def get_min(self) -> int:
        return self.min_stack[-1]

print("=" * 60)
print("Pattern 7: Min Stack (O(1) getMin)")
print("=" * 60)
print("Problem: Stack with constant-time minimum retrieval")
print("\nHow it works:")
print("  1. Use TWO stacks: main stack + min stack")
print("  2. Main stack: stores all values normally")
print("  3. Min stack: stores minimum at each level")
print("  4. When pushing: if value <= current min, push to min stack")
print("  5. When popping: if popped value is min, pop from min stack too")
print("  6. getMin(): just return top of min stack (O(1))")
print("\nExample:")
print("  Operations: push(5), push(2), push(8), push(1), push(3)")
min_stack = MinStack()
for val in [5, 2, 8, 1, 3]:
    min_stack.push(val)
    print(f"    Push {val} -> min: {min_stack.get_min()}")
print("\n  Pop operations:")
for _ in range(2):
    popped = min_stack.pop()
    print(f"    Pop {popped} -> min: {min_stack.get_min()}")
print()


# Pattern 8: Remove Adjacent Duplicates
def remove_duplicates(s: str) -> str:
    """
    Remove adjacent duplicate characters.
    Time: O(n), Space: O(n)
    
    Example:
        Input: "abbaca"
        Output: "ca"
        Explanation:
        - Remove 'bb' -> "aaca"
        - Remove 'aa' -> "ca"
    """
    stack = []
    
    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)
    
    return ''.join(stack)

print("=" * 60)
print("Pattern 8: Remove Adjacent Duplicates")
print("=" * 60)
print("Problem: Remove all adjacent duplicate characters")
print("\nHow it works:")
print("  1. Process string character by character")
print("  2. If stack top matches current char: POP (remove duplicate)")
print("  3. Otherwise: PUSH current char to stack")
print("  4. Stack automatically handles cascade removals")
print("  5. Example: 'abbaca' -> 'a' then 'bb' removed")
print("     -> 'aaca' -> 'aa' removed -> 'ca'")
print("\nExamples:")
examples = ['abbaca', 'azxxzy', 'aabbcc']
for s in examples:
    result = remove_duplicates(s)
    print(f"  '{s}' -> '{result}'")
print()


# Pattern 9: Valid Palindrome after Character Removal
def is_valid_palindrome_stack(s: str) -> bool:
    """
    Check if string can become palindrome by removing at most one character.
    Using stack approach.
    Time: O(n), Space: O(n)
    """
    def is_palindrome(text):
        return text == text[::-1]
    
    # Try removing each character
    for i in range(len(s)):
        modified = s[:i] + s[i+1:]
        if is_palindrome(modified):
            return True
    
    return is_palindrome(s)

print("Pattern 9: Valid Palindrome")
print(f"'aba': {is_valid_palindrome_stack('aba')}")
print(f"'abca': {is_valid_palindrome_stack('abca')}")
print(f"'abc': {is_valid_palindrome_stack('abc')}")
