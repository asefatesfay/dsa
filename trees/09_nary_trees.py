"""
N-ary Trees (General Trees with Multiple Children)
===================================================
Understanding trees where nodes can have any number of children.
"""

from collections import deque
from typing import List, Optional


class Node:
    """N-ary tree node"""
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children if children else []


print("=" * 60)
print("What is an N-ary Tree?")
print("=" * 60)
print()
print("An N-ary tree (also called general tree) is a tree where")
print("each node can have any number of children (0 to n).")
print()
print("Key Properties:")
print("  • Each node can have 0, 1, 2, 3, ... children")
print("  • No limit on number of children")
print("  • More flexible than binary trees")
print("  • Children stored in list/array")
print()
print("Common Types:")
print("  • Binary tree: max 2 children (special case)")
print("  • Ternary tree: max 3 children")
print("  • K-ary tree: max k children")
print("  • General N-ary: unlimited children")
print()
print("Example N-ary Tree:")
print()
print("            1")
print("         /  |  \\")
print("        2   3   4")
print("       /|   |   |\\")
print("      5 6   7   8 9")
print("        |      /|\\")
print("        10   11 12 13")
print()
print("Node 1 has 3 children: [2, 3, 4]")
print("Node 2 has 2 children: [5, 6]")
print("Node 4 has 2 children: [8, 9]")
print("Node 8 has 3 children: [11, 12, 13]")
print()


# Basic N-ary tree operations
def preorder_recursive(root):
    """
    Preorder traversal: Visit node, then all children.
    
    How it works:
    1. Process current node
    2. Recursively visit each child (left to right)
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return []
    
    result = [root.val]
    for child in root.children:
        result.extend(preorder_recursive(child))
    
    return result


def preorder_iterative(root):
    """
    Iterative preorder using stack.
    
    How it works:
    1. Use stack (LIFO)
    2. Push children in reverse order
    3. Process nodes as they're popped
    
    Time: O(n), Space: O(n)
    """
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Add children in reverse order
        # (so leftmost is processed first)
        for child in reversed(node.children):
            stack.append(child)
    
    return result


def postorder_recursive(root):
    """
    Postorder traversal: Visit children, then node.
    
    How it works:
    1. Recursively visit all children first
    2. Then process current node
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return []
    
    result = []
    for child in root.children:
        result.extend(postorder_recursive(child))
    
    result.append(root.val)
    return result


def postorder_iterative(root):
    """
    Iterative postorder using two stacks.
    
    How it works:
    1. First stack: reverse preorder
    2. Second stack: reverse result
    
    Time: O(n), Space: O(n)
    """
    if not root:
        return []
    
    stack1 = [root]
    stack2 = []
    
    while stack1:
        node = stack1.pop()
        stack2.append(node.val)
        
        # Add children (left to right)
        for child in node.children:
            stack1.append(child)
    
    # Reverse to get postorder
    return stack2[::-1]


def level_order(root):
    """
    Level order traversal (BFS).
    
    How it works:
    1. Use queue for BFS
    2. Process nodes level by level
    3. Add all children of current level
    
    Time: O(n), Space: O(w) where w = max width
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            # Add all children
            for child in node.children:
                queue.append(child)
        
        result.append(level)
    
    return result


print("=" * 60)
print("N-ary Tree Traversals Demo")
print("=" * 60)
print()

# Build example tree
#        1
#      / | \
#     3  2  4
#    / \
#   5   6

root = Node(1)
root.children = [Node(3), Node(2), Node(4)]
root.children[0].children = [Node(5), Node(6)]

print("Tree structure:")
print("       1")
print("     / | \\")
print("    3  2  4")
print("   / \\")
print("  5   6")
print()

print("Traversals:")
print(f"  Preorder (recursive):  {preorder_recursive(root)}")
print(f"  Preorder (iterative):  {preorder_iterative(root)}")
print(f"  Postorder (recursive): {postorder_recursive(root)}")
print(f"  Postorder (iterative): {postorder_iterative(root)}")
print(f"  Level order:           {level_order(root)}")

print()


# N-ary tree properties
def max_depth(root):
    """
    Find maximum depth (height).
    
    How it works:
    1. If no node, depth = 0
    2. Find max depth among all children
    3. Add 1 for current level
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0
    
    if not root.children:
        return 1
    
    max_child_depth = max(max_depth(child) for child in root.children)
    return 1 + max_child_depth


def count_nodes(root):
    """
    Count total number of nodes.
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0
    
    total = 1  # Current node
    for child in root.children:
        total += count_nodes(child)
    
    return total


def count_leaves(root):
    """
    Count leaf nodes (nodes with no children).
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0
    
    if not root.children:
        return 1  # This is a leaf
    
    total = 0
    for child in root.children:
        total += count_leaves(child)
    
    return total


def diameter(root):
    """
    Find diameter (longest path between any two nodes).
    
    How it works:
    1. For each node, find two deepest children
    2. Diameter might pass through this node
    3. Track maximum seen
    
    Time: O(n²) naive, can optimize to O(n)
    """
    max_diameter = [0]
    
    def height(node):
        if not node:
            return 0
        
        if not node.children:
            return 1
        
        # Get heights of all children
        heights = [height(child) for child in node.children]
        
        # Diameter through this node =
        # sum of two largest child heights
        if len(heights) >= 2:
            heights.sort(reverse=True)
            path_through_node = heights[0] + heights[1]
            max_diameter[0] = max(max_diameter[0], path_through_node)
        elif len(heights) == 1:
            max_diameter[0] = max(max_diameter[0], heights[0])
        
        return 1 + max(heights)
    
    height(root)
    return max_diameter[0]


print("=" * 60)
print("N-ary Tree Properties")
print("=" * 60)
print()

# Build larger tree
#            1
#         /  |  \
#        2   3   4
#       /|   |   |\
#      5 6   7   8 9

root2 = Node(1)
root2.children = [Node(2), Node(3), Node(4)]
root2.children[0].children = [Node(5), Node(6)]
root2.children[1].children = [Node(7)]
root2.children[2].children = [Node(8), Node(9)]

print("Tree:")
print("           1")
print("        /  |  \\")
print("       2   3   4")
print("      /|   |   |\\")
print("     5 6   7   8 9")
print()

print(f"Max depth:    {max_depth(root2)}")
print(f"Node count:   {count_nodes(root2)}")
print(f"Leaf count:   {count_leaves(root2)}")
print(f"Diameter:     {diameter(root2)}")

print()


# Serialize and Deserialize
def serialize(root):
    """
    Convert N-ary tree to string.
    
    Format: value [children_count] child1 child2 ...
    
    How it works:
    1. Preorder traversal
    2. Store value and number of children
    3. Recursively serialize children
    
    Time: O(n), Space: O(n)
    """
    if not root:
        return ""
    
    result = []
    
    def helper(node):
        if not node:
            return
        
        result.append(str(node.val))
        result.append(str(len(node.children)))
        
        for child in node.children:
            helper(child)
    
    helper(root)
    return " ".join(result)


def deserialize(data):
    """
    Convert string back to N-ary tree.
    
    How it works:
    1. Split string into tokens
    2. Recursively build tree
    3. First token = value, second = children count
    4. Build that many children
    
    Time: O(n), Space: O(n)
    """
    if not data:
        return None
    
    tokens = data.split()
    index = [0]  # Use list to modify in nested function
    
    def helper():
        if index[0] >= len(tokens):
            return None
        
        # Read value and children count
        val = int(tokens[index[0]])
        index[0] += 1
        
        children_count = int(tokens[index[0]])
        index[0] += 1
        
        # Create node
        node = Node(val)
        
        # Build children
        for _ in range(children_count):
            child = helper()
            if child:
                node.children.append(child)
        
        return node
    
    return helper()


print("=" * 60)
print("Serialize and Deserialize")
print("=" * 60)
print()

serialized = serialize(root2)
print(f"Serialized: {serialized}")

deserialized = deserialize(serialized)
print(f"Deserialized (level order): {level_order(deserialized)}")
print("Trees match!")

print()


# Lowest Common Ancestor
def lowest_common_ancestor(root, p, q):
    """
    Find lowest common ancestor of two nodes.
    
    How it works:
    1. If current node is p or q, return it
    2. Search in all children
    3. If two+ children return non-null, this is LCA
    4. Otherwise return the one non-null child
    
    Time: O(n), Space: O(h)
    """
    if not root or root.val == p or root.val == q:
        return root
    
    # Search all children
    found = []
    for child in root.children:
        result = lowest_common_ancestor(child, p, q)
        if result:
            found.append(result)
    
    # If found in 2+ subtrees, this is LCA
    if len(found) > 1:
        return root
    
    # Otherwise, return the one found (or None)
    return found[0] if found else None


print("=" * 60)
print("Lowest Common Ancestor")
print("=" * 60)
print()

print("Tree:")
print("           1")
print("        /  |  \\")
print("       2   3   4")
print("      /|   |   |\\")
print("     5 6   7   8 9")
print()

lca1 = lowest_common_ancestor(root2, 5, 6)
print(f"LCA(5, 6) = {lca1.val if lca1 else None}")

lca2 = lowest_common_ancestor(root2, 5, 7)
print(f"LCA(5, 7) = {lca2.val if lca2 else None}")

lca3 = lowest_common_ancestor(root2, 8, 9)
print(f"LCA(8, 9) = {lca3.val if lca3 else None}")

print()


# Clone N-ary tree
def clone_tree(root):
    """
    Create deep copy of N-ary tree.
    
    How it works:
    1. Create new node with same value
    2. Recursively clone all children
    3. Add cloned children to new node
    
    Time: O(n), Space: O(n)
    """
    if not root:
        return None
    
    new_node = Node(root.val)
    
    for child in root.children:
        new_child = clone_tree(child)
        new_node.children.append(new_child)
    
    return new_node


print("=" * 60)
print("Clone Tree")
print("=" * 60)
print()

cloned = clone_tree(root2)
print(f"Original (level order):  {level_order(root2)}")
print(f"Cloned (level order):    {level_order(cloned)}")
print(f"Are different objects: {root2 is not cloned}")

print()


# Maximum width
def max_width(root):
    """
    Find maximum width (max nodes at any level).
    
    How it works:
    1. Level order traversal
    2. Track size of each level
    3. Return maximum
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return 0
    
    max_w = 0
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        max_w = max(max_w, level_size)
        
        for _ in range(level_size):
            node = queue.popleft()
            for child in node.children:
                queue.append(child)
    
    return max_w


def is_symmetric(root):
    """
    Check if tree is symmetric (mirror of itself).
    
    How it works:
    1. Compare children in pairs from outside-in
    2. Recursively check subtrees
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return True
    
    def is_mirror(children):
        if not children:
            return True
        
        n = len(children)
        
        # Check if values are symmetric
        for i in range(n // 2):
            if children[i].val != children[n - 1 - i].val:
                return False
        
        # Check if subtrees are mirror
        for i in range(n // 2):
            if not is_mirror_subtree(children[i], children[n - 1 - i]):
                return False
        
        # If odd number of children, check middle
        if n % 2 == 1:
            if not is_symmetric(children[n // 2]):
                return False
        
        return True
    
    def is_mirror_subtree(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        
        # Children must be mirror images
        left_children = left.children
        right_children = right.children[::-1]  # Reverse
        
        if len(left_children) != len(right_children):
            return False
        
        for l, r in zip(left_children, right_children):
            if not is_mirror_subtree(l, r):
                return False
        
        return True
    
    return is_mirror(root.children)


print("=" * 60)
print("Additional Properties")
print("=" * 60)
print()

print(f"Maximum width: {max_width(root2)}")

# Build symmetric tree
sym = Node(1)
sym.children = [Node(2), Node(3), Node(2)]
sym.children[0].children = [Node(4)]
sym.children[2].children = [Node(4)]

print()
print("Symmetric tree:")
print("       1")
print("     / | \\")
print("    2  3  2")
print("    |     |")
print("    4     4")
print(f"Is symmetric? {is_symmetric(sym)}")

print()


# Path operations
def find_path(root, target):
    """
    Find path from root to target node.
    
    How it works:
    1. DFS with path tracking
    2. If target found, return path
    3. Backtrack if not found
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return None
    
    path = []
    
    def dfs(node):
        if not node:
            return False
        
        path.append(node.val)
        
        if node.val == target:
            return True
        
        for child in node.children:
            if dfs(child):
                return True
        
        path.pop()  # Backtrack
        return False
    
    if dfs(root):
        return path
    return None


def all_paths_to_leaves(root):
    """
    Find all paths from root to leaves.
    
    Time: O(n * h), Space: O(n * h)
    """
    if not root:
        return []
    
    paths = []
    
    def dfs(node, path):
        path.append(node.val)
        
        if not node.children:
            paths.append(path[:])  # Leaf - save path
        else:
            for child in node.children:
                dfs(child, path)
        
        path.pop()  # Backtrack
    
    dfs(root, [])
    return paths


print("=" * 60)
print("Path Operations")
print("=" * 60)
print()

print("Tree:")
print("           1")
print("        /  |  \\")
print("       2   3   4")
print("      /|   |   |\\")
print("     5 6   7   8 9")
print()

path_to_7 = find_path(root2, 7)
print(f"Path to node 7: {path_to_7}")

path_to_9 = find_path(root2, 9)
print(f"Path to node 9: {path_to_9}")

print()
print("All paths to leaves:")
all_paths = all_paths_to_leaves(root2)
for i, path in enumerate(all_paths, 1):
    print(f"  Path {i}: {path}")

print()


# Convert representations
def tree_to_adjacency_list(root):
    """
    Convert N-ary tree to adjacency list representation.
    
    Time: O(n), Space: O(n)
    """
    if not root:
        return {}
    
    adj_list = {}
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        adj_list[node.val] = [child.val for child in node.children]
        
        for child in node.children:
            queue.append(child)
    
    return adj_list


def adjacency_list_to_tree(adj_list, root_val):
    """
    Convert adjacency list to N-ary tree.
    
    Time: O(n), Space: O(n)
    """
    if not adj_list or root_val not in adj_list:
        return None
    
    # Build nodes
    nodes = {val: Node(val) for val in adj_list}
    
    # Connect children
    for parent_val, children_vals in adj_list.items():
        parent = nodes[parent_val]
        parent.children = [nodes[val] for val in children_vals]
    
    return nodes[root_val]


print("=" * 60)
print("Representation Conversion")
print("=" * 60)
print()

adj_list = tree_to_adjacency_list(root2)
print("Tree as adjacency list:")
for node, children in sorted(adj_list.items()):
    print(f"  {node} → {children}")

print()

reconstructed = adjacency_list_to_tree(adj_list, 1)
print(f"Reconstructed (level order): {level_order(reconstructed)}")

print()


# Real-world applications
print("=" * 60)
print("Real-World Applications of N-ary Trees")
print("=" * 60)
print()
print("1. File Systems:")
print("   • Directories can have multiple files/subdirectories")
print("   • Root = top-level directory")
print("   • Leaves = files")
print()
print("   /")
print("   ├── home/")
print("   │   ├── user1/")
print("   │   └── user2/")
print("   ├── etc/")
print("   └── var/")
print()
print("2. Organization Charts:")
print("   • CEO at root")
print("   • Managers can have multiple subordinates")
print("   • Employees = nodes")
print()
print("         CEO")
print("       /  |  \\")
print("     VP1 VP2 VP3")
print("     /|  |   |\\")
print("   M1 M2 M3  M4 M5")
print()
print("3. XML/HTML DOM:")
print("   • Tags can have multiple children")
print("   • Document = tree structure")
print()
print("   <html>")
print("     <head>")
print("       <title>Page</title>")
print("     </head>")
print("     <body>")
print("       <h1>Header</h1>")
print("       <p>Paragraph 1</p>")
print("       <p>Paragraph 2</p>")
print("     </body>")
print("   </html>")
print()
print("4. Decision Trees:")
print("   • Each decision can have multiple outcomes")
print("   • Used in AI/ML")
print()
print("5. Game Trees:")
print("   • Each state can lead to multiple next states")
print("   • Chess, Go, etc.")
print()
print("6. Syntax Trees:")
print("   • Programming language parsers")
print("   • Expression evaluation")
print()
print("7. Category Hierarchies:")
print("   • E-commerce product categories")
print("   • Library classification systems")
print()


# Common patterns
print("=" * 60)
print("Common N-ary Tree Patterns")
print("=" * 60)
print()
print("Pattern 1: Traversal")
print("  • Preorder: Process node, then children")
print("  • Postorder: Process children, then node")
print("  • Level order: Process level by level")
print()
print("Pattern 2: Properties")
print("  • Height: max depth among children + 1")
print("  • Size: 1 + sum of children sizes")
print("  • Diameter: sum of two deepest branches")
print()
print("Pattern 3: Path Finding")
print("  • DFS with backtracking")
print("  • Track path during traversal")
print("  • Return when target found")
print()
print("Pattern 4: Serialization")
print("  • Store value + children count")
print("  • Recursively serialize children")
print("  • Reconstruct using same format")
print()
print("Pattern 5: Level-wise Processing")
print("  • Use queue for BFS")
print("  • Process all nodes at each level")
print("  • Track level information")
print()


# Time complexity summary
print("=" * 60)
print("Time Complexity Summary")
print("=" * 60)
print()
print("Operation              Time        Space")
print("-" * 60)
print("Traversal (any)        O(n)        O(h)")
print("Search                 O(n)        O(h)")
print("Insert                 O(1)*       O(1)")
print("Delete                 O(n)        O(h)")
print("Height                 O(n)        O(h)")
print("Level order            O(n)        O(w)")
print("Serialize              O(n)        O(n)")
print("Clone                  O(n)        O(n)")
print("LCA                    O(n)        O(h)")
print()
print("n = number of nodes")
print("h = height of tree")
print("w = maximum width")
print()
print("* Insert at known parent location")
print()


# Comparison with binary trees
print("=" * 60)
print("N-ary Trees vs Binary Trees")
print("=" * 60)
print()
print("                Binary Tree    N-ary Tree")
print("-" * 60)
print("Max children    2              Unlimited")
print("Storage         2 pointers     Array/List")
print("Flexibility     Limited        High")
print("Cache locality  Better         Worse")
print("Implementation  Simpler        More complex")
print()
print("Use Binary Tree when:")
print("  • At most 2 choices per node")
print("  • Need BST properties")
print("  • Better cache performance")
print()
print("Use N-ary Tree when:")
print("  • Variable number of children")
print("  • Modeling hierarchies (file systems)")
print("  • Flexible structure needed")
print()
