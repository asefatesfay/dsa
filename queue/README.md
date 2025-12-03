# Python Queue - Data Structures and Algorithms

This folder contains comprehensive learning materials for Queue data structure in Python.

## 📚 Files Overview

1. **01_basics.py** - Queue implementations (list, deque, linked list, circular queue)
2. **02_common_operations.py** - Common patterns (BFS, sliding window, multi-source BFS, etc.)
3. **03_practice_problems.py** - LeetCode-style problems with solutions
4. **04_real_world_problems.py** - Real-world applications (print queue, call center, etc.)
5. **05_exercises.py** - Practice exercises for you to solve

## 🎯 Learning Path

1. Start with `01_basics.py` to understand queue fundamentals and implementations
2. Study `02_common_operations.py` for essential patterns (especially BFS!)
3. Review `03_practice_problems.py` to see solutions to common interview questions
4. Explore `04_real_world_problems.py` to see practical applications
5. Practice with `05_exercises.py` to test your understanding

## ⏱️ Time Complexities

| Operation | List | Deque (Recommended) | Linked List | Circular |
|-----------|------|---------------------|-------------|----------|
| Enqueue | O(1) | O(1) | O(1) | O(1) |
| Dequeue | O(n) ⚠️ | O(1) ✅ | O(1) | O(1) |
| Front/Peek | O(1) | O(1) | O(1) | O(1) |
| isEmpty | O(1) | O(1) | O(1) | O(1) |
| Size | O(1) | O(1) | O(1) | O(1) |

**Recommendation:** Use `collections.deque` for best performance!

## 💡 Key Concepts

- **FIFO**: First In, First Out - oldest element is removed first
- **Two main operations**: Enqueue (add to rear), Dequeue (remove from front)
- **Applications**: BFS, task scheduling, buffering, request handling
- **Best Implementation**: `collections.deque` for O(1) operations

## 🔥 Common Patterns

1. **Breadth-First Search (BFS)**: Level-order tree/graph traversal
2. **Sliding Window Maximum**: Using monotonic deque
3. **Multi-source BFS**: Multiple starting points (rotting oranges)
4. **Level Order Traversal**: Process tree/graph level by level
5. **Shortest Path**: Finding shortest path in unweighted graphs
6. **Task Scheduling**: Round-robin scheduling with time quantum
7. **Binary Number Generation**: Generate sequences efficiently
8. **Stream Processing**: First non-repeating character

## 🚀 Running the Code

```bash
# Run any file to see examples
python3 queue/01_basics.py
python3 queue/02_common_operations.py

# Practice exercises
python3 queue/05_exercises.py
```

## 📖 Queue vs Other Data Structures

| Feature | Queue | Stack | Deque | Priority Queue |
|---------|-------|-------|-------|----------------|
| Access Pattern | FIFO | LIFO | Both ends | By priority |
| Primary Ops | Enqueue/Dequeue | Push/Pop | Add/Remove both ends | Insert/DeleteMin |
| Use Case | BFS, Scheduling | DFS, Undo | Sliding window | Dijkstra, scheduling |
| Time (Insert) | O(1) | O(1) | O(1) | O(log n) |
| Time (Delete) | O(1) | O(1) | O(1) | O(log n) |

## 🌍 Real-World Applications

### Implemented in this folder:
1. **Print Queue** - Office printer job management
2. **Call Center** - Customer service call routing
3. **Task Scheduler** - CPU process scheduling (Round Robin)
4. **Web Server** - HTTP request handling with rate limiting
5. **Message Queue** - Microservices communication (like RabbitMQ)
6. **File System Search** - BFS through directory trees
7. **LRU Cache** - Least Recently Used cache eviction
8. **Restaurant Queue** - Customer waiting line simulation

### Other uses:
- **Operating Systems**: Process scheduling, I/O buffering
- **Networking**: Packet routing, request queues
- **Gaming**: Turn-based game logic, action queues
- **Media**: Video/audio buffering and streaming
- **E-commerce**: Order processing, inventory management
- **Transportation**: Traffic simulation, ride-sharing
- **Real-time Systems**: Event handling, message passing

## 🎓 Tips

- Use `collections.deque` for queue implementation (not list!)
- Queue is essential for BFS traversal (breadth-first)
- Consider queue when you need FIFO order or level-by-level processing
- For priority-based processing, use `heapq` (priority queue)
- Circular queue is great for fixed-size buffers
- Double-ended queue (deque) provides O(1) operations at both ends

## 📝 Common Interview Problems

### Easy:
- Implement Queue using Stacks
- Design Circular Queue
- Recent Counter
- Generate Binary Numbers

### Medium:
- Binary Tree Level Order Traversal
- Rotting Oranges
- Perfect Squares
- Walls and Gates
- Open the Lock

### Hard:
- Shortest Path with Obstacles Elimination
- Word Ladder II
- Bus Routes
- Sliding Window Maximum

## 📊 BFS Algorithm Pattern

```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}
    
    while queue:
        node = queue.popleft()
        
        # Process node
        for neighbor in get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

## 🔗 Related Concepts

- **BFS**: Breadth-First Search uses queue
- **Level Order**: Tree traversal level by level
- **Shortest Path**: In unweighted graphs using BFS
- **Topological Sort**: Using queue (Kahn's algorithm)
- **Producer-Consumer**: Classic queue problem

## 📝 Next Steps

After mastering queues, you can move on to:
- **Priority Queue (Heap)** - Priority-based processing
- **Deque** - Double-ended queue (already covered!)
- **Trees** - Using queue for level-order traversal
- **Graphs** - Using queue for BFS traversal
- **Dynamic Programming** - Some problems optimize with queues

## 🆚 Stack vs Queue

| Aspect | Stack | Queue |
|--------|-------|-------|
| Order | LIFO | FIFO |
| Main Ops | Push/Pop | Enqueue/Dequeue |
| Use | DFS, Recursion, Backtracking | BFS, Scheduling, Buffering |
| Example | Undo/Redo, Call Stack | Print Queue, Task Queue |

Happy Learning! 📚🚀
