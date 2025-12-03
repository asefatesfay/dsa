"""
Trees - Basics
==============
Understanding tree data structures from the ground up.
"""

print("=" * 60)
print("What is a Tree?")
print("=" * 60)
print("A tree is a hierarchical data structure with nodes connected by edges.")
print()
print("Key Terminology:")
print("  - Node: Contains data and links to other nodes")
print("  - Root: The topmost node (no parent)")
print("  - Parent: Node with children below it")
print("  - Child: Node below another node")
print("  - Leaf: Node with no children")
print("  - Edge: Connection between two nodes")
print("  - Height: Longest path from node to leaf")
print("  - Depth: Distance from root to node")
print("  - Subtree: Tree formed by a node and its descendants")
print()
print("Tree Properties:")
print("  - Exactly ONE path between any two nodes")
print("  - N nodes have N-1 edges")
print("  - No cycles (unlike graphs)")
print("  - Hierarchical structure")
print()
print("Why Use Trees?")
print("  - Natural hierarchy (file systems, org charts)")
print("  - Fast search/insert/delete (binary search trees)")
print("  - Maintain sorted data (BST)")
print("  - Expression evaluation (expression trees)")
print("  - Prefix matching (tries)")
print()


# Basic Tree Node
class TreeNode:
    """Basic tree node with value and children list"""
    def __init__(self, val=0):
        self.val = val
        self.children = []  # List of child nodes
    
    def add_child(self, child_node):
        """Add a child to this node"""
        self.children.append(child_node)


print("=" * 60)
print("General Tree (N-ary Tree)")
print("=" * 60)
print("A tree where each node can have any number of children.")
print()

# Create a general tree
#        1
#      / | \
#     2  3  4
#    /|   |
#   5 6   7

root = TreeNode(1)
child1 = TreeNode(2)
child2 = TreeNode(3)
child3 = TreeNode(4)
root.add_child(child1)
root.add_child(child2)
root.add_child(child3)

child1.add_child(TreeNode(5))
child1.add_child(TreeNode(6))
child2.add_child(TreeNode(7))

print("Example tree structure:")
print("         1")
print("       / | \\")
print("      2  3  4")
print("     /|   |")
print("    5 6   7")
print()


# Tree Traversal Methods
def print_tree_preorder(node, level=0):
    """
    Preorder: Visit node, then children (DFS)
    Used for: copying tree, prefix expression
    """
    if node is None:
        return
    print("  " * level + f"→ {node.val}")
    for child in node.children:
        print_tree_preorder(child, level + 1)


def print_tree_postorder(node, level=0):
    """
    Postorder: Visit children, then node (DFS)
    Used for: deletion, postfix expression, calculating sizes
    """
    if node is None:
        return
    for child in node.children:
        print_tree_postorder(child, level + 1)
    print("  " * level + f"→ {node.val}")


def print_tree_level_order(root):
    """
    Level order: Visit level by level (BFS)
    Used for: finding shortest path, level-wise processing
    """
    if not root:
        return
    
    from collections import deque
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.val)
            
            for child in node.children:
                queue.append(child)
        
        print(f"  → {level_nodes}")


print("=" * 60)
print("Tree Traversal Methods")
print("=" * 60)

print("\n1. Preorder (Root → Left → Right):")
print("   Visit node before its children")
print_tree_preorder(root)

print("\n2. Postorder (Left → Right → Root):")
print("   Visit node after its children")
print_tree_postorder(root)

print("\n3. Level Order (Breadth-First):")
print("   Visit nodes level by level")
print_tree_level_order(root)

print()


# Binary Tree (most common type)
class BinaryTreeNode:
    """Binary tree node - maximum 2 children"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left    # Left child
        self.right = right  # Right child


print("=" * 60)
print("Binary Tree")
print("=" * 60)
print("A tree where each node has at most 2 children (left and right).")
print()

# Create a binary tree
#        1
#      /   \
#     2     3
#    / \   /
#   4   5 6

bt_root = BinaryTreeNode(1)
bt_root.left = BinaryTreeNode(2)
bt_root.right = BinaryTreeNode(3)
bt_root.left.left = BinaryTreeNode(4)
bt_root.left.right = BinaryTreeNode(5)
bt_root.right.left = BinaryTreeNode(6)

print("Example binary tree:")
print("        1")
print("      /   \\")
print("     2     3")
print("    / \\   /")
print("   4   5 6")
print()


# Binary Tree Traversals
def inorder(node, result=None):
    """
    Inorder: Left → Root → Right
    For BST: gives sorted order
    """
    if result is None:
        result = []
    if node:
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)
    return result


def preorder(node, result=None):
    """
    Preorder: Root → Left → Right
    Used for: creating copy of tree
    """
    if result is None:
        result = []
    if node:
        result.append(node.val)
        preorder(node.left, result)
        preorder(node.right, result)
    return result


def postorder(node, result=None):
    """
    Postorder: Left → Right → Root
    Used for: deleting tree, evaluating expression
    """
    if result is None:
        result = []
    if node:
        postorder(node.left, result)
        postorder(node.right, result)
        result.append(node.val)
    return result


def level_order(root):
    """
    Level order: Level by level (BFS)
    """
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


print("=" * 60)
print("Binary Tree Traversals")
print("=" * 60)

print("\n1. Inorder (Left → Root → Right):")
print(f"   Result: {inorder(bt_root)}")
print("   Path: 4 → 2 → 5 → 1 → 6 → 3")

print("\n2. Preorder (Root → Left → Right):")
print(f"   Result: {preorder(bt_root)}")
print("   Path: 1 → 2 → 4 → 5 → 3 → 6")

print("\n3. Postorder (Left → Right → Root):")
print(f"   Result: {postorder(bt_root)}")
print("   Path: 4 → 5 → 2 → 6 → 3 → 1")

print("\n4. Level Order (BFS):")
result = level_order(bt_root)
print(f"   Result: {result}")
print("   Level 0: [1], Level 1: [2,3], Level 2: [4,5,6]")

print()


# Basic Binary Tree Operations
def tree_height(node):
    """
    Calculate height of tree.
    Height = longest path from node to leaf
    """
    if not node:
        return -1  # Empty tree height = -1
    
    left_height = tree_height(node.left)
    right_height = tree_height(node.right)
    
    return 1 + max(left_height, right_height)


def tree_size(node):
    """Count total number of nodes"""
    if not node:
        return 0
    return 1 + tree_size(node.left) + tree_size(node.right)


def count_leaves(node):
    """Count leaf nodes (nodes with no children)"""
    if not node:
        return 0
    if not node.left and not node.right:
        return 1  # This is a leaf
    return count_leaves(node.left) + count_leaves(node.right)


def max_value(node):
    """Find maximum value in tree"""
    if not node:
        return float('-inf')
    
    left_max = max_value(node.left)
    right_max = max_value(node.right)
    
    return max(node.val, left_max, right_max)


def min_value(node):
    """Find minimum value in tree"""
    if not node:
        return float('inf')
    
    left_min = min_value(node.left)
    right_min = min_value(node.right)
    
    return min(node.val, left_min, right_min)


def search_tree(node, target):
    """Search for a value in tree"""
    if not node:
        return False
    if node.val == target:
        return True
    
    return search_tree(node.left, target) or search_tree(node.right, target)


print("=" * 60)
print("Basic Binary Tree Operations")
print("=" * 60)

print(f"\nTree structure:")
print("        1")
print("      /   \\")
print("     2     3")
print("    / \\   /")
print("   4   5 6")

print(f"\n1. Height: {tree_height(bt_root)}")
print("   (Longest path from root to leaf)")

print(f"\n2. Size: {tree_size(bt_root)}")
print("   (Total number of nodes)")

print(f"\n3. Leaf count: {count_leaves(bt_root)}")
print("   (Nodes with no children: 4, 5, 6)")

print(f"\n4. Maximum value: {max_value(bt_root)}")
print(f"   Minimum value: {min_value(bt_root)}")

print(f"\n5. Search for 5: {search_tree(bt_root, 5)}")
print(f"   Search for 10: {search_tree(bt_root, 10)}")

print()


# Types of Binary Trees
print("=" * 60)
print("Types of Binary Trees")
print("=" * 60)

print("\n1. FULL Binary Tree:")
print("   Every node has 0 or 2 children (no node has only 1 child)")
print()
print("        1")
print("      /   \\")
print("     2     3")
print("    / \\")
print("   4   5")
print()

print("2. COMPLETE Binary Tree:")
print("   All levels filled except possibly last")
print("   Last level filled from left to right")
print("   (Used in heaps)")
print()
print("        1")
print("      /   \\")
print("     2     3")
print("    / \\   /")
print("   4   5 6")
print()

print("3. PERFECT Binary Tree:")
print("   All internal nodes have 2 children")
print("   All leaves at same level")
print()
print("        1")
print("      /   \\")
print("     2     3")
print("    / \\   / \\")
print("   4   5 6   7")
print()

print("4. BALANCED Binary Tree:")
print("   Height of left and right subtrees differ by at most 1")
print("   For every node (AVL trees)")
print()
print("        1")
print("      /   \\")
print("     2     3")
print("    /")
print("   4")
print("   (Balanced: heights differ by 1)")
print()

print("5. DEGENERATE (Skewed) Tree:")
print("   Each node has only one child")
print("   Essentially a linked list")
print()
print("   1")
print("    \\")
print("     2")
print("      \\")
print("       3")
print("        \\")
print("         4")
print()


# Building Trees
print("=" * 60)
print("Building Trees from Arrays")
print("=" * 60)

print("\nLevel-order array representation:")
print("Array: [1, 2, 3, 4, 5, 6, 7]")
print()
print("        1      (index 0)")
print("      /   \\")
print("     2     3   (indices 1, 2)")
print("    / \\   / \\")
print("   4   5 6   7 (indices 3, 4, 5, 6)")
print()
print("For node at index i:")
print("  - Left child:  2*i + 1")
print("  - Right child: 2*i + 2")
print("  - Parent:      (i-1) // 2")
print()


def build_tree_from_array(arr):
    """Build complete binary tree from level-order array"""
    if not arr:
        return None
    
    def helper(index):
        if index >= len(arr) or arr[index] is None:
            return None
        
        node = BinaryTreeNode(arr[index])
        node.left = helper(2 * index + 1)
        node.right = helper(2 * index + 2)
        return node
    
    return helper(0)


print("Example: Build tree from [1,2,3,4,5,6,7]")
arr = [1, 2, 3, 4, 5, 6, 7]
tree_from_array = build_tree_from_array(arr)
print(f"Level order result: {level_order(tree_from_array)}")
print(f"Inorder result: {inorder(tree_from_array)}")

print()


# Tree Comparison
def are_identical(tree1, tree2):
    """Check if two trees are identical (structure and values)"""
    # Both empty
    if not tree1 and not tree2:
        return True
    
    # One empty, one not
    if not tree1 or not tree2:
        return False
    
    # Check current node and recurse
    return (tree1.val == tree2.val and
            are_identical(tree1.left, tree2.left) and
            are_identical(tree1.right, tree2.right))


def is_symmetric(root):
    """
    Check if tree is mirror of itself.
    
    How it works:
    1. Compare left subtree with right subtree
    2. For mirror: left.left ↔ right.right and left.right ↔ right.left
    3. Values must match at corresponding positions
    
    Example of symmetric tree:
           1
         /   \
        2     2
       / \   / \
      3   4 4   3
    
    Left subtree (2,3,4) mirrors right subtree (2,4,3)
    
    Example of non-symmetric tree:
           1
         /   \
        2     2
         \     \
          3     3
    
    Left has right child, but right also has right child (not mirrored)
    
    Time: O(n), Space: O(h) where h is height (recursion stack)
    """
    def is_mirror(left, right):
        # Both null - symmetric
        if not left and not right:
            return True
        
        # One null, one not - not symmetric
        if not left or not right:
            return False
        
        # Check:
        # 1. Current values match
        # 2. Left's left mirrors Right's right
        # 3. Left's right mirrors Right's left
        return (left.val == right.val and
                is_mirror(left.left, right.right) and
                is_mirror(left.right, right.left))
    
    return is_mirror(root, root) if root else True


print("=" * 60)
print("Tree Comparisons")
print("=" * 60)

# Identical trees
tree1 = BinaryTreeNode(1)
tree1.left = BinaryTreeNode(2)
tree1.right = BinaryTreeNode(3)

tree2 = BinaryTreeNode(1)
tree2.left = BinaryTreeNode(2)
tree2.right = BinaryTreeNode(3)

print("\nTree 1 and Tree 2:")
print("   1       1")
print("  / \\     / \\")
print(" 2   3   2   3")
print(f"\nAre identical? {are_identical(tree1, tree2)}")

# Symmetric tree
sym_tree = BinaryTreeNode(1)
sym_tree.left = BinaryTreeNode(2)
sym_tree.right = BinaryTreeNode(2)
sym_tree.left.left = BinaryTreeNode(3)
sym_tree.right.right = BinaryTreeNode(3)

print("\nSymmetric tree:")
print("     1")
print("   /   \\")
print("  2     2")
print(" /       \\")
print("3         3")
print(f"\nIs symmetric? {is_symmetric(sym_tree)}")

print()


# Practical Applications
print("=" * 60)
print("Real-World Applications of Trees")
print("=" * 60)

print("\n1. File System:")
print("   - Directories = nodes")
print("   - Files/subdirectories = children")
print("   - Root directory = root node")

print("\n2. HTML/XML DOM:")
print("   - HTML tags = nodes")
print("   - Nested tags = children")
print("   - Document traversal = tree traversal")

print("\n3. Organization Chart:")
print("   - CEO = root")
print("   - Managers = internal nodes")
print("   - Employees = leaf nodes")

print("\n4. Decision Trees:")
print("   - Questions = internal nodes")
print("   - Answers = edges")
print("   - Decisions = leaf nodes")

print("\n5. Expression Trees:")
print("   - Operators = internal nodes")
print("   - Operands = leaf nodes")
print("   - Evaluate by postorder traversal")

print("\n6. Game Trees:")
print("   - Game states = nodes")
print("   - Possible moves = edges")
print("   - Win/lose conditions = leaves")

print()
