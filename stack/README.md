# Python Stack - Data Structures and Algorithms

This folder contains comprehensive learning materials for Stack data structure in Python.

## 📚 Files Overview

1. **01_basics.py** - Stack implementations (using list and linked list), fundamentals
2. **02_common_operations.py** - Common patterns (balanced parentheses, postfix evaluation, etc.)
3. **03_practice_problems.py** - LeetCode-style problems with solutions
4. **04_real_world_problems.py** - Real-world applications (browser history, undo/redo, etc.)
5. **05_exercises.py** - Practice exercises for you to solve
6. **list_impl.py** - Your basic list implementation
7. **linked_list_impl.py** - Your basic linked list implementation

## 🎯 Learning Path

1. Start with `01_basics.py` to understand stack fundamentals and both implementations
2. Study `02_common_operations.py` for essential patterns used in stack problems
3. Review `03_practice_problems.py` to see solutions to common interview questions
4. Explore `04_real_world_problems.py` to see practical applications
5. Practice with `05_exercises.py` to test your understanding

## ⏱️ Time Complexities

| Operation | Time Complexity |
|-----------|----------------|
| Push | O(1) |
| Pop | O(1) |
| Peek/Top | O(1) |
| isEmpty | O(1) |
| Size | O(1) |
| Search | O(n) |

## 💡 Key Concepts

- **LIFO**: Last In, First Out - most recent element is removed first
- **Two main operations**: Push (add) and Pop (remove)
- **Applications**: Function calls, expression evaluation, backtracking, undo/redo
- **Implementation**: Can use array/list or linked list

## 🔥 Common Patterns

1. **Balanced Parentheses**: Validate brackets/parentheses matching
2. **Next Greater Element**: Find next larger element using monotonic stack
3. **Expression Evaluation**: Infix/postfix/prefix conversion and evaluation
4. **Monotonic Stack**: Maintain elements in increasing/decreasing order
5. **Two Stacks**: Use two stacks to solve specific problems
6. **Min/Max Stack**: Track minimum/maximum in O(1) time

## 🚀 Running the Code

```bash
# Run any file to see examples
python3 stack/01_basics.py
python3 stack/02_common_operations.py

# Practice exercises
python3 stack/05_exercises.py
```

## 📖 Stack vs Other Data Structures

| Feature | Stack | Queue | List |
|---------|-------|-------|------|
| Access Pattern | LIFO | FIFO | Random Access |
| Primary Ops | Push/Pop | Enqueue/Dequeue | Index Access |
| Use Case | Undo/Backtrack | Task Queue | General Purpose |
| Time (Insert) | O(1) | O(1) | O(1) amortized |
| Time (Delete) | O(1) | O(1) | O(n) |

## 🌍 Real-World Applications

### Implemented in this folder:
1. **Browser History** - Back/forward navigation
2. **Text Editor** - Undo/redo functionality
3. **Calculator** - Expression evaluation
4. **Call Stack** - Function call tracking
5. **Syntax Checker** - Code validation
6. **Build System** - Task dependencies
7. **Memory Allocator** - Stack-based allocation
8. **File Navigator** - Path navigation

### Other uses:
- **Compilers**: Syntax parsing, expression evaluation
- **JVM/Runtime**: Method call stack, exception handling
- **Browsers**: Navigation history, page state
- **IDEs**: Syntax validation, auto-completion
- **Games**: Undo moves, state management
- **Algorithms**: DFS traversal, backtracking problems

## 🎓 Tips

- Stack is perfect when you need to reverse something or track nested structures
- Use stack for problems involving pairs/matching (parentheses, tags)
- Monotonic stack is powerful for "next greater/smaller" element problems
- Consider stack when you see keywords: "nearest", "previous", "next", "valid"
- Time complexity is usually O(n) with O(n) space for stack problems

## 📝 Next Steps

After mastering stacks, you can move on to:
- **Queues** (FIFO data structure)
- **Deque** (Double-ended queue)
- **Priority Queue** (Heap-based)
- **Trees** (Using stack for DFS traversal)
- **Graphs** (Using stack for DFS)

## 🔗 Related Concepts

- **Recursion**: Uses implicit call stack
- **DFS**: Depth-First Search uses stack
- **Backtracking**: Relies on stack for state management
- **Dynamic Programming**: Some problems can be optimized with stacks

Happy Learning! 📚🚀
