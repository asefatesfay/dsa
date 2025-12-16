"""
NeetCode 150 - Stack
====================
Stack-based problem solving.
"""


# PATTERN: Stack (Bracket Matching)
def is_valid(s):
    """
    Valid Parentheses - check if brackets are properly closed.
    
    Pattern: Stack for matching pairs
    
    Algorithm Steps:
    1. Push opening brackets onto stack
    2. For closing bracket, check if matches top of stack
    3. Stack should be empty at end
    
    Time: O(n), Space: O(n)
    """
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in pairs:
            stack.append(char)
        elif not stack or pairs[stack.pop()] != char:
            return False
    
    return len(stack) == 0


# PATTERN: Stack with Auxiliary Structure
class MinStack:
    """
    Min Stack - stack with O(1) min operation.
    
    Pattern: Two stacks (main + min tracking)
    
    Design:
    - Main stack: stores all values
    - Min stack: stores minimum at each level
    
    Example: push 3,5,2,1
    - Main: [3,5,2,1]
    - Min:  [3,3,2,1]
    """
    
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))
    
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()
    
    def top(self):
        return self.stack[-1]
    
    def getMin(self):
        return self.min_stack[-1]


# PATTERN: Stack (Expression Evaluation)
def eval_rpn(tokens):
    """
    Evaluate Reverse Polish Notation.
    
    Pattern: Stack for operands
    
    Algorithm Steps:
    1. Push numbers onto stack
    2. For operator, pop two operands, compute, push result
    
    Example: ["2","1","+","3","*"]
    - Push 2, push 1
    - '+': pop 1,2, compute 2+1=3, push 3
    - Push 3
    - '*': pop 3,3, compute 3*3=9, push 9
    
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
            else:
                stack.append(int(a / b))  # Truncate toward zero
        else:
            stack.append(int(token))
    
    return stack[0]


# PATTERN: Backtracking with Stack
def generate_parenthesis(n):
    """
    Generate Parentheses - all combinations of n pairs.
    
    Pattern: Backtracking with validity rules
    
    Algorithm Steps:
    1. Add '(' if open_count < n
    2. Add ')' if close_count < open_count
    3. Backtrack when complete
    
    Example: n=3
    - Start: ""
    - Add '(': "("
    - Add '(': "(("
    - Add '(': "((("
    - Add ')': "((())"
    - Backtrack and try other combinations
    
    Time: O(4^n / sqrt(n)) - Catalan number, Space: O(n)
    """
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result


# PATTERN: Monotonic Stack
def daily_temperatures(temperatures):
    """
    Daily Temperatures - days until warmer temperature.
    
    Pattern: Monotonic decreasing stack
    
    Algorithm Steps:
    1. Stack stores indices of temperatures
    2. For each temp, pop all smaller temps from stack
    3. For popped indices, current index - popped index = days to wait
    
    Why it works: We only care about next warmer day, so can discard
    smaller temperatures once we find a warmer one
    
    Example: [73,74,75,71,69,72,76,73]
    - Day 0 (73): stack=[0], result=[0,...]
    - Day 1 (74): 74>73, pop 0, result=[1,0,...], stack=[1]
    - Day 2 (75): 75>74, pop 1, result=[1,1,0,...], stack=[2]
    
    Time: O(n), Space: O(n)
    """
    result = [0] * len(temperatures)
    stack = []  # Stack of indices
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
        stack.append(i)
    
    return result


# PATTERN: Monotonic Stack with Sorting
def car_fleet(target, position, speed):
    """
    Car Fleet - number of car fleets arriving at target.
    
    Pattern: Sort + Stack (or just track time)
    
    Algorithm Steps:
    1. Sort cars by starting position (descending)
    2. Calculate time to reach target for each car
    3. If car catches up to one ahead, they form fleet
    
    Why it works: Cars behind can't pass, so if slower car is ahead,
    faster car forms fleet with it
    
    Example: target=12, pos=[10,8,0,5,3], speed=[2,4,1,1,3]
    - Car at 10: time = 2/2 = 1
    - Car at 8: time = 4/4 = 1 (forms fleet with car at 10)
    - Car at 5: time = 7/1 = 7
    - Car at 3: time = 9/3 = 3 (catches car at 5)
    - Car at 0: time = 12/1 = 12
    - Fleets: 3
    
    Time: O(n log n), Space: O(n)
    """
    cars = sorted(zip(position, speed), reverse=True)
    fleets = 0
    prev_time = 0
    
    for pos, spd in cars:
        time = (target - pos) / spd
        if time > prev_time:
            fleets += 1
            prev_time = time
    
    return fleets


# PATTERN: Monotonic Stack
def largest_rectangle_area(heights):
    """
    Largest Rectangle in Histogram.
    
    Pattern: Monotonic increasing stack
    
    Algorithm Steps:
    1. Stack stores indices of increasing heights
    2. When smaller height found, calculate areas of previous rectangles
    3. Height = heights[stack.pop()]
    4. Width = current_index - stack[-1] - 1 (or current_index if stack empty)
    
    Why it works: For each bar, we find how far left and right it can extend
    
    Example: [2,1,5,6,2,3]
    - At index 1 (h=1): Pop 2, area = 2*1 = 2
    - At index 4 (h=2): Pop 6, area = 6*1 = 6; Pop 5, area = 5*2 = 10
    
    Time: O(n), Space: O(n)
    """
    stack = []
    max_area = 0
    
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
    
    # Process remaining bars
    for i, h in stack:
        max_area = max(max_area, h * (len(heights) - i))
    
    return max_area


if __name__ == "__main__":
    print("=== NeetCode 150 - Stack ===\n")
    
    # Valid Parentheses
    print(f"Valid Parentheses '()[]{{}}': {is_valid('()[]{}')}") 
    print(f"Valid Parentheses '(]': {is_valid('(]')}")
    
    # Min Stack
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    print(f"MinStack getMin: {min_stack.getMin()}")
    min_stack.pop()
    print(f"MinStack top: {min_stack.top()}")
    print(f"MinStack getMin: {min_stack.getMin()}")
    
    # Evaluate RPN
    print(f"Eval RPN ['2','1','+','3','*']: {eval_rpn(['2', '1', '+', '3', '*'])}")
    
    # Generate Parentheses
    print(f"Generate Parentheses n=3: {generate_parenthesis(3)}")
    
    # Daily Temperatures
    print(f"Daily Temperatures [73,74,75,71,69,72,76,73]: {daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])}")
    
    # Car Fleet
    print(f"Car Fleet target=12, pos=[10,8,0,5,3], speed=[2,4,1,1,3]: {car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3])}")
    
    # Largest Rectangle
    print(f"Largest Rectangle [2,1,5,6,2,3]: {largest_rectangle_area([2, 1, 5, 6, 2, 3])}")
