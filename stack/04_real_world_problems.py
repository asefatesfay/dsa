"""
Stack - Real World Applications
================================
Practical problems and use cases in real systems.
"""

from typing import List, Optional
from collections import deque


# Problem 1: Browser History
class BrowserHistory:
    """
    Implement browser back/forward navigation.
    Real-world use: Web browsers (Chrome, Firefox, Safari)
    """
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.current = 0
    
    def visit(self, url: str) -> None:
        """Visit a new URL"""
        # Remove all forward history
        self.history = self.history[:self.current + 1]
        self.history.append(url)
        self.current += 1
    
    def back(self, steps: int) -> str:
        """Go back in history"""
        self.current = max(0, self.current - steps)
        return self.history[self.current]
    
    def forward(self, steps: int) -> str:
        """Go forward in history"""
        self.current = min(len(self.history) - 1, self.current + steps)
        return self.history[self.current]
    
    def get_current(self) -> str:
        """Get current URL"""
        return self.history[self.current]

print("Problem 1: Browser History")
browser = BrowserHistory("google.com")
browser.visit("youtube.com")
browser.visit("facebook.com")
print(f"Current: {browser.get_current()}")
print(f"Back 1: {browser.back(1)}")
print(f"Back 1: {browser.back(1)}")
print(f"Forward 1: {browser.forward(1)}")
browser.visit("linkedin.com")
print(f"After new visit: {browser.get_current()}")
print(f"Forward 1: {browser.forward(1)}")
print()


# Problem 2: Undo/Redo Text Editor
class TextEditor:
    """
    Text editor with undo/redo functionality.
    Real-world use: Google Docs, Microsoft Word, VS Code
    """
    def __init__(self):
        self.text = ""
        self.undo_stack = []
        self.redo_stack = []
    
    def write(self, text: str) -> None:
        """Add text"""
        self.undo_stack.append(self.text)
        self.text += text
        self.redo_stack.clear()  # Clear redo on new action
    
    def delete(self, length: int) -> None:
        """Delete last 'length' characters"""
        self.undo_stack.append(self.text)
        self.text = self.text[:-length] if length <= len(self.text) else ""
        self.redo_stack.clear()
    
    def undo(self) -> str:
        """Undo last operation"""
        if self.undo_stack:
            self.redo_stack.append(self.text)
            self.text = self.undo_stack.pop()
        return self.text
    
    def redo(self) -> str:
        """Redo last undone operation"""
        if self.redo_stack:
            self.undo_stack.append(self.text)
            self.text = self.redo_stack.pop()
        return self.text
    
    def get_text(self) -> str:
        """Get current text"""
        return self.text

print("Problem 2: Text Editor with Undo/Redo")
editor = TextEditor()
editor.write("Hello ")
editor.write("World")
print(f"Text: '{editor.get_text()}'")
editor.delete(5)
print(f"After delete 5: '{editor.get_text()}'")
editor.undo()
print(f"After undo: '{editor.get_text()}'")
editor.redo()
print(f"After redo: '{editor.get_text()}'")
print()


# Problem 3: Expression Evaluator (Calculator)
class Calculator:
    """
    Basic calculator for arithmetic expressions.
    Real-world use: Calculator apps, spreadsheet formulas
    """
    def __init__(self):
        self.operators = {'+', '-', '*', '/', '(', ')'}
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def evaluate(self, expression: str) -> float:
        """Evaluate arithmetic expression"""
        # Convert to postfix
        postfix = self._infix_to_postfix(expression)
        # Evaluate postfix
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self, expression: str) -> List[str]:
        """Convert infix to postfix notation"""
        output = []
        stack = []
        i = 0
        
        while i < len(expression):
            if expression[i].isspace():
                i += 1
                continue
            
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                output.append(expression[i:j])
                i = j
            elif expression[i] == '(':
                stack.append(expression[i])
                i += 1
            elif expression[i] == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
                i += 1
            elif expression[i] in self.operators:
                while (stack and stack[-1] != '(' and 
                       stack[-1] in self.precedence and
                       self.precedence[stack[-1]] >= self.precedence[expression[i]]):
                    output.append(stack.pop())
                stack.append(expression[i])
                i += 1
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """Evaluate postfix expression"""
        stack = []
        
        for token in tokens:
            if token not in self.operators:
                stack.append(float(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
        
        return stack[0] if stack else 0

print("Problem 3: Calculator")
calc = Calculator()
expressions = ["2 + 3", "2 + 3 * 4", "(2 + 3) * 4", "10 / 2 - 3"]
for expr in expressions:
    print(f"'{expr}' = {calc.evaluate(expr)}")
print()


# Problem 4: Function Call Stack Simulator
class CallStack:
    """
    Simulate function call stack for debugging.
    Real-world use: Debuggers, profilers, error trackers
    """
    def __init__(self):
        self.stack = []
        self.call_count = {}
    
    def call_function(self, func_name: str, args: List = None) -> None:
        """Push function call onto stack"""
        self.stack.append({'name': func_name, 'args': args or []})
        self.call_count[func_name] = self.call_count.get(func_name, 0) + 1
    
    def return_function(self) -> Optional[str]:
        """Pop function from stack (return)"""
        if self.stack:
            return self.stack.pop()['name']
        return None
    
    def get_stack_trace(self) -> List[str]:
        """Get current stack trace"""
        return [f"{frame['name']}({', '.join(map(str, frame['args']))})" 
                for frame in self.stack]
    
    def get_depth(self) -> int:
        """Get current stack depth"""
        return len(self.stack)
    
    def get_statistics(self) -> dict:
        """Get call statistics"""
        return {
            'current_depth': self.get_depth(),
            'max_function': max(self.call_count.items(), key=lambda x: x[1]) if self.call_count else None,
            'total_calls': sum(self.call_count.values())
        }

print("Problem 4: Function Call Stack")
call_stack = CallStack()
call_stack.call_function("main", [])
call_stack.call_function("process_data", [10, 20])
call_stack.call_function("validate", ["input"])
print(f"Stack trace: {call_stack.get_stack_trace()}")
print(f"Depth: {call_stack.get_depth()}")
call_stack.return_function()
print(f"After return: {call_stack.get_stack_trace()}")
print()


# Problem 5: Syntax Checker (Code Validator)
class SyntaxChecker:
    """
    Check syntax for balanced brackets/parentheses.
    Real-world use: IDEs, code editors, compilers
    """
    def check_syntax(self, code: str) -> dict:
        """Check code for syntax errors"""
        stack = []
        pairs = {'(': ')', '{': '}', '[': ']', '<': '>'}
        errors = []
        line_num = 1
        
        for i, char in enumerate(code):
            if char == '\n':
                line_num += 1
            
            if char in pairs:
                stack.append((char, line_num, i))
            elif char in pairs.values():
                if not stack:
                    errors.append(f"Line {line_num}: Unexpected closing '{char}'")
                else:
                    open_char, open_line, open_pos = stack.pop()
                    if pairs[open_char] != char:
                        errors.append(f"Line {line_num}: Mismatched brackets - expected '{pairs[open_char]}', got '{char}'")
        
        # Check for unclosed brackets
        for open_char, line, pos in stack:
            errors.append(f"Line {line}: Unclosed '{open_char}'")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'bracket_pairs': len(code) - len(stack)
        }

print("Problem 5: Syntax Checker")
checker = SyntaxChecker()
code_samples = [
    "if (x > 0) { return true; }",
    "if (x > 0 { return true; }",
    "array[0] = value);",
]
for code in code_samples:
    result = checker.check_syntax(code)
    print(f"Code: '{code}'")
    print(f"Valid: {result['valid']}")
    if result['errors']:
        for error in result['errors']:
            print(f"  Error: {error}")
print()


# Problem 6: Task Execution Order (Build System)
class BuildSystem:
    """
    Manage build task dependencies and execution order.
    Real-world use: Make, Gradle, npm scripts, CI/CD pipelines
    """
    def __init__(self):
        self.tasks = {}
        self.execution_order = []
    
    def add_task(self, name: str, dependencies: List[str] = None) -> None:
        """Add a build task with dependencies"""
        self.tasks[name] = dependencies or []
    
    def get_execution_order(self) -> List[str]:
        """Get topological order of task execution using DFS"""
        visited = set()
        stack = []
        
        def dfs(task):
            if task in visited:
                return
            visited.add(task)
            
            for dep in self.tasks.get(task, []):
                dfs(dep)
            
            stack.append(task)
        
        for task in self.tasks:
            dfs(task)
        
        return stack
    
    def detect_circular_dependency(self) -> Optional[List[str]]:
        """Detect circular dependencies"""
        visiting = set()
        visited = set()
        
        def has_cycle(task, path):
            if task in visiting:
                return path + [task]
            if task in visited:
                return None
            
            visiting.add(task)
            path.append(task)
            
            for dep in self.tasks.get(task, []):
                cycle = has_cycle(dep, path[:])
                if cycle:
                    return cycle
            
            visiting.remove(task)
            visited.add(task)
            return None
        
        for task in self.tasks:
            cycle = has_cycle(task, [])
            if cycle:
                return cycle
        
        return None

print("Problem 6: Build System")
build = BuildSystem()
build.add_task("compile", ["clean"])
build.add_task("test", ["compile"])
build.add_task("package", ["test"])
build.add_task("clean", [])
print(f"Execution order: {build.get_execution_order()}")
print(f"Circular dependency: {build.detect_circular_dependency()}")
print()


# Problem 7: Memory Management (Stack vs Heap)
class MemoryAllocator:
    """
    Simulate stack-based memory allocation.
    Real-world use: Compilers, runtime environments, memory profilers
    """
    def __init__(self, size: int):
        self.size = size
        self.used = 0
        self.stack = []
    
    def allocate(self, name: str, size: int) -> bool:
        """Allocate memory on stack"""
        if self.used + size > self.size:
            return False
        
        self.stack.append({'name': name, 'size': size})
        self.used += size
        return True
    
    def deallocate(self) -> Optional[dict]:
        """Deallocate top of stack (LIFO)"""
        if self.stack:
            block = self.stack.pop()
            self.used -= block['size']
            return block
        return None
    
    def get_usage(self) -> dict:
        """Get memory usage statistics"""
        return {
            'total': self.size,
            'used': self.used,
            'free': self.size - self.used,
            'usage_percent': (self.used / self.size) * 100
        }

print("Problem 7: Memory Allocator")
memory = MemoryAllocator(1024)
memory.allocate("int_array", 100)
memory.allocate("string", 50)
memory.allocate("object", 200)
usage = memory.get_usage()
print(f"Used: {usage['used']}/{usage['total']} bytes ({usage['usage_percent']:.1f}%)")
freed = memory.deallocate()
print(f"Freed: {freed['name']} ({freed['size']} bytes)")
print()


# Problem 8: Path Navigation (File System)
class FileNavigator:
    """
    Navigate file system paths with cd command.
    Real-world use: Terminal/shell, file managers
    """
    def __init__(self):
        self.path_stack = ["/"]
        self.history = []
    
    def cd(self, path: str) -> str:
        """Change directory"""
        if path == "/":
            self.path_stack = ["/"]
        elif path == "..":
            if len(self.path_stack) > 1:
                self.path_stack.pop()
        elif path == ".":
            pass  # Stay in current directory
        else:
            self.path_stack.append(path)
        
        current = self.get_current_path()
        self.history.append(current)
        return current
    
    def get_current_path(self) -> str:
        """Get current path"""
        if len(self.path_stack) == 1:
            return "/"
        return "/".join(self.path_stack)
    
    def pwd(self) -> str:
        """Print working directory"""
        return self.get_current_path()
    
    def get_history(self) -> List[str]:
        """Get navigation history"""
        return self.history[-5:]  # Last 5

print("Problem 8: File Navigator")
nav = FileNavigator()
print(f"Current: {nav.pwd()}")
nav.cd("home")
nav.cd("user")
print(f"After cd home/user: {nav.pwd()}")
nav.cd("..")
print(f"After cd ..: {nav.pwd()}")
nav.cd("documents")
print(f"After cd documents: {nav.pwd()}")
print(f"History: {nav.get_history()}")
