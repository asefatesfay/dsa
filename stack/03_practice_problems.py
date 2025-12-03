"""
Stack - Practice Problems
==========================
Common interview questions and LeetCode-style problems.
"""

from typing import List, Optional


# Problem 1: Valid Parentheses (LeetCode #20)
def is_valid_parentheses(s: str) -> bool:
    """
    Determine if input string has valid parentheses.
    Time: O(n), Space: O(n)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    
    return not stack

print("Problem 1: Valid Parentheses")
test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
for test in test_cases:
    print(f"'{test}': {is_valid_parentheses(test)}")
print()


# Problem 2: Min Stack (LeetCode #155)
class MinStack:
    """
    Stack with constant time getMin operation.
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        self.stack.pop()
    
    def top(self) -> int:
        return self.stack[-1]
    
    def get_min(self) -> int:
        return self.min_stack[-1]

print("Problem 2: Min Stack")
min_stack = MinStack()
operations = [("push", -2), ("push", 0), ("push", -3), ("getMin", None), 
              ("pop", None), ("top", None), ("getMin", None)]
for op, val in operations:
    if op == "push":
        min_stack.push(val)
        print(f"Push {val}")
    elif op == "pop":
        min_stack.pop()
        print("Pop")
    elif op == "top":
        print(f"Top: {min_stack.top()}")
    elif op == "getMin":
        print(f"Min: {min_stack.get_min()}")
print()


# Problem 3: Daily Temperatures (LeetCode #739)
def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Find number of days until warmer temperature.
    Time: O(n), Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        stack.append(i)
    
    return result

print("Problem 3: Daily Temperatures")
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(f"Temperatures: {temps}")
print(f"Days to wait: {daily_temperatures(temps)}")
print()


# Problem 4: Evaluate Reverse Polish Notation (LeetCode #150)
def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluate arithmetic expression in Reverse Polish Notation.
    Time: O(n), Space: O(n)
    """
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(int(a / b))  # Truncate toward zero
        else:
            stack.append(int(token))
    
    return stack[0]

print("Problem 4: Evaluate RPN")
rpn1 = ["2", "1", "+", "3", "*"]
rpn2 = ["4", "13", "5", "/", "+"]
print(f"{rpn1} = {eval_rpn(rpn1)}")
print(f"{rpn2} = {eval_rpn(rpn2)}")
print()


# Problem 5: Decode String (LeetCode #394)
def decode_string(s: str) -> str:
    """
    Decode encoded string. Example: "3[a]2[bc]" -> "aaabcbc"
    Time: O(n), Space: O(n)
    """
    stack = []
    current_string = ""
    current_num = 0
    
    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0
        elif char == ']':
            prev_string, num = stack.pop()
            current_string = prev_string + current_string * num
        else:
            current_string += char
    
    return current_string

print("Problem 5: Decode String")
print(f"'3[a]2[bc]': {decode_string('3[a]2[bc]')}")
print(f"'3[a2[c]]': {decode_string('3[a2[c]]')}")
print(f"'2[abc]3[cd]ef': {decode_string('2[abc]3[cd]ef')}")
print()


# Problem 6: Remove All Adjacent Duplicates (LeetCode #1047)
def remove_duplicates(s: str) -> str:
    """
    Remove all adjacent duplicate characters.
    Time: O(n), Space: O(n)
    """
    stack = []
    
    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)
    
    return ''.join(stack)

print("Problem 6: Remove Adjacent Duplicates")
print(f"'abbaca': {remove_duplicates('abbaca')}")
print(f"'azxxzy': {remove_duplicates('azxxzy')}")
print()


# Problem 7: Largest Rectangle in Histogram (LeetCode #84)
def largest_rectangle_area(heights: List[int]) -> int:
    """
    Find largest rectangle area in histogram.
    Time: O(n), Space: O(n)
    """
    stack = []
    max_area = 0
    heights.append(0)  # Add sentinel
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height_index = stack.pop()
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, heights[height_index] * width)
        stack.append(i)
    
    heights.pop()  # Remove sentinel
    return max_area

print("Problem 7: Largest Rectangle in Histogram")
hist = [2, 1, 5, 6, 2, 3]
print(f"Heights: {hist}")
print(f"Max area: {largest_rectangle_area(hist)}")
print()


# Problem 8: Simplify Path (LeetCode #71)
def simplify_path(path: str) -> str:
    """
    Simplify Unix-style file path.
    Time: O(n), Space: O(n)
    """
    stack = []
    parts = path.split('/')
    
    for part in parts:
        if part == '..' and stack:
            stack.pop()
        elif part and part != '.' and part != '..':
            stack.append(part)
    
    return '/' + '/'.join(stack)

print("Problem 8: Simplify Path")
paths = ["/home/", "/a/./b/../../c/", "/a//b////c/d//././/.."]
for p in paths:
    print(f"'{p}' -> '{simplify_path(p)}'")
print()


# Problem 9: Asteroid Collision (LeetCode #735)
def asteroid_collision(asteroids: List[int]) -> List[int]:
    """
    Simulate asteroid collisions.
    Positive = moving right, Negative = moving left
    Time: O(n), Space: O(n)
    """
    stack = []
    
    for asteroid in asteroids:
        while stack and asteroid < 0 < stack[-1]:
            if stack[-1] < -asteroid:
                stack.pop()
                continue
            elif stack[-1] == -asteroid:
                stack.pop()
            break
        else:
            stack.append(asteroid)
    
    return stack

print("Problem 9: Asteroid Collision")
print(f"[5, 10, -5]: {asteroid_collision([5, 10, -5])}")
print(f"[8, -8]: {asteroid_collision([8, -8])}")
print(f"[10, 2, -5]: {asteroid_collision([10, 2, -5])}")
print()


# Problem 10: Basic Calculator II (LeetCode #227)
def calculate(s: str) -> int:
    """
    Implement basic calculator for +, -, *, /.
    Time: O(n), Space: O(n)
    """
    if not s:
        return 0
    
    stack = []
    num = 0
    operation = '+'
    
    for i, char in enumerate(s):
        if char.isdigit():
            num = num * 10 + int(char)
        
        if char in '+-*/' or i == len(s) - 1:
            if operation == '+':
                stack.append(num)
            elif operation == '-':
                stack.append(-num)
            elif operation == '*':
                stack.append(stack.pop() * num)
            elif operation == '/':
                stack.append(int(stack.pop() / num))
            
            if char in '+-*/':
                operation = char
            num = 0
    
    return sum(stack)

print("Problem 10: Basic Calculator II")
print(f"'3+2*2': {calculate('3+2*2')}")
print(f"' 3/2 ': {calculate(' 3/2 ')}")
print(f"' 3+5 / 2 ': {calculate(' 3+5 / 2 ')}")
print()


# Problem 11: Trapping Rain Water (LeetCode #42) - Using Stack
def trap_rain_water(height: List[int]) -> int:
    """
    Calculate how much rain water can be trapped.
    Time: O(n), Space: O(n)
    """
    if not height:
        return 0
    
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            
            distance = i - stack[-1] - 1
            bounded_height = min(height[stack[-1]], h) - height[bottom]
            water += distance * bounded_height
        
        stack.append(i)
    
    return water

print("Problem 11: Trapping Rain Water")
elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(f"Elevation: {elevation}")
print(f"Water trapped: {trap_rain_water(elevation)} units")
