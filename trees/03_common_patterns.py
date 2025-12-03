"""
Tree Traversal Patterns
=======================
Common patterns and techniques for tree traversal problems.
"""

from collections import deque
from typing import Optional, List


class TreeNode:
    """Binary tree node"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


print("=" * 60)
print("Tree Traversal Patterns")
print("=" * 60)
print()


# ============================================================
# Pattern 1: Level Order Traversal (BFS)
# ============================================================

def level_order_traversal(root):
    """
    Traverse tree level by level.
    
    How it works:
    1. Use queue to track nodes at each level
    2. Process all nodes at current level
    3. Add their children for next level
    4. Repeat until queue is empty
    
    Time: O(n), Space: O(w) where w is max width
    """
    if not root:
        return []
    
    result = []
    # STEP 1: Initialize queue with root node
    # Queue will hold nodes to process at current level
    queue = deque([root])
    
    # STEP 2: Process level by level until queue is empty
    while queue:
        # STEP 3: Snapshot the queue size - this is how many nodes
        # are at the CURRENT level (important: size changes as we add children)
        level_size = len(queue)
        level = []
        
        # STEP 4: Process exactly level_size nodes (all nodes at this level)
        # Don't use while queue - that would process children too!
        for _ in range(level_size):
            # STEP 5: Remove node from front of queue (FIFO)
            node = queue.popleft()
            # STEP 6: Add node's value to current level
            level.append(node.val)
            
            # STEP 7: Add children to queue for NEXT level
            # Children go to back of queue, won't be processed in this loop
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # STEP 8: After processing all nodes at this level, save the level
        result.append(level)
    
    # STEP 9: Return all levels
    return result


print("Pattern 1: Level Order Traversal")
print("-" * 60)
print()
print("Tree:")
print("     3")
print("   /   \\")
print("  9     20")
print("       /  \\")
print("      15   7")
print()

tree1 = TreeNode(3)
tree1.left = TreeNode(9)
tree1.right = TreeNode(20)
tree1.right.left = TreeNode(15)
tree1.right.right = TreeNode(7)

print(f"Level order: {level_order_traversal(tree1)}")
print("Output: [[3], [9,20], [15,7]]")
print()


# ============================================================
# Pattern 2: Zigzag Level Order
# ============================================================

def zigzag_level_order(root):
    """
    Traverse level by level, alternating direction.
    
    How it works:
    1. Same as level order
    2. Use flag to track direction
    3. Reverse even levels
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True  # Direction flag
    
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
        
        # Reverse if going right to left
        if not left_to_right:
            level.reverse()
        
        result.append(level)
        left_to_right = not left_to_right  # Toggle direction
    
    return result


print("Pattern 2: Zigzag Level Order")
print("-" * 60)
print()
print("Tree:")
print("     3")
print("   /   \\")
print("  9     20")
print("       /  \\")
print("      15   7")
print()

print(f"Zigzag order: {zigzag_level_order(tree1)}")
print("Output: [[3], [20,9], [15,7]]")
print("Level 0: left to right [3]")
print("Level 1: right to left [20,9]")
print("Level 2: left to right [15,7]")
print()


# ============================================================
# Pattern 3: Right Side View
# ============================================================

def right_side_view(root):
    """
    Return rightmost node at each level.
    
    How it works:
    1. Do level order traversal
    2. Take last node of each level
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.popleft()
            
            # Last node in this level
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result


print("Pattern 3: Right Side View")
print("-" * 60)
print()
print("Tree:")
print("     1")
print("   /   \\")
print("  2     3")
print("   \\     \\")
print("    5     4")
print()

tree2 = TreeNode(1)
tree2.left = TreeNode(2)
tree2.right = TreeNode(3)
tree2.left.right = TreeNode(5)
tree2.right.right = TreeNode(4)

print(f"Right side view: {right_side_view(tree2)}")
print("Output: [1, 3, 4]")
print("Standing on right, you see: 1 → 3 → 4")
print()


# ============================================================
# Pattern 4: Vertical Order Traversal
# ============================================================

def vertical_order(root):
    """
    Traverse tree vertically (top to bottom, left to right).
    
    How it works:
    1. Assign column numbers (root = 0, left = -1, right = +1)
    2. Group nodes by column
    3. Sort by column, then level, then value
    
    Time: O(n log n), Space: O(n)
    """
    if not root:
        return []
    
    # column -> [(row, value)]
    column_table = {}
    queue = deque([(root, 0, 0)])  # (node, row, col)
    
    while queue:
        node, row, col = queue.popleft()
        
        if col not in column_table:
            column_table[col] = []
        column_table[col].append((row, node.val))
        
        if node.left:
            queue.append((node.left, row + 1, col - 1))
        if node.right:
            queue.append((node.right, row + 1, col + 1))
    
    # Sort by column, then row, then value
    result = []
    for col in sorted(column_table.keys()):
        column_table[col].sort()
        result.append([val for row, val in column_table[col]])
    
    return result


print("Pattern 4: Vertical Order Traversal")
print("-" * 60)
print()
print("Tree with column numbers:")
print("       3 (col 0)")
print("      / \\")
print("     9   20 (col -1, col 1)")
print("        /  \\")
print("       15  7 (col 0, col 2)")
print()

print(f"Vertical order: {vertical_order(tree1)}")
print("Output: [[9], [3,15], [20], [7]]")
print("Column -1: [9]")
print("Column  0: [3,15]")
print("Column  1: [20]")
print("Column  2: [7]")
print()


# ============================================================
# Pattern 5: Path Sum
# ============================================================

def has_path_sum(root, target_sum):
    """
    Check if root-to-leaf path sums to target.
    
    How it works:
    1. Subtract current value from target
    2. At leaf, check if remaining sum is 0
    3. Recurse on left and right
    
    Time: O(n), Space: O(h)
    """
    # STEP 1: Base case - null node, no path
    if not root:
        return False
    
    # STEP 2: Check if we're at a LEAF node (no children)
    # Only leaf nodes can be the end of a valid path
    if not root.left and not root.right:
        # STEP 3: At leaf, check if we've used up exactly target_sum
        # If root.val == target_sum, we found a valid path!
        return root.val == target_sum
    
    # STEP 4: Not at leaf, so continue down the tree
    # Subtract current node's value from remaining sum needed
    remaining = target_sum - root.val
    
    # STEP 5: Recursively check left and right subtrees
    # If EITHER path works, return True (that's why we use OR)
    # Each recursive call gets the remaining sum it needs to find
    return (has_path_sum(root.left, remaining) or
            has_path_sum(root.right, remaining))


def all_path_sums(root, target_sum):
    """
    Return all root-to-leaf paths that sum to target.
    
    How it works:
    1. Track current path
    2. At leaf, check if sum matches
    3. Backtrack after exploring each path
    
    Time: O(n²), Space: O(h)
    """
    result = []
    
    def dfs(node, remaining, path):
        # STEP 1: Base case - null node
        if not node:
            return
        
        # STEP 2: Add current node to path (exploring this node)
        path.append(node.val)
        
        # STEP 3: Check if we're at a leaf node
        if not node.left and not node.right:
            # STEP 4: At leaf - check if this path sums to target
            if remaining == node.val:
                # STEP 5: Found valid path! Make a COPY and save it
                # IMPORTANT: Use path[:] to copy, not just path
                # (path will be modified as we backtrack)
                result.append(path[:])
        else:
            # STEP 6: Not at leaf - explore children
            # Subtract current value from remaining sum
            # Pass the same path list (will be modified in-place)
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        
        # STEP 7: BACKTRACK - remove current node from path
        # This happens after exploring both children (or at leaf)
        # Prepares path for exploring other branches
        path.pop()
    
    dfs(root, target_sum, [])
    return result


print("Pattern 5: Path Sum")
print("-" * 60)
print()
print("Tree:")
print("       5")
print("      / \\")
print("     4   8")
print("    /   / \\")
print("   11  13  4")
print("  /  \\      \\")
print(" 7    2     1")
print()

tree3 = TreeNode(5)
tree3.left = TreeNode(4)
tree3.right = TreeNode(8)
tree3.left.left = TreeNode(11)
tree3.left.left.left = TreeNode(7)
tree3.left.left.right = TreeNode(2)
tree3.right.left = TreeNode(13)
tree3.right.right = TreeNode(4)
tree3.right.right.right = TreeNode(1)

print(f"Has path sum 22? {has_path_sum(tree3, 22)}")
print("Path: 5 → 4 → 11 → 2 (sum = 22)")

print(f"\nAll paths summing to 22: {all_path_sums(tree3, 22)}")
print("Output: [[5,4,11,2]]")
print()


# ============================================================
# Pattern 6: Lowest Common Ancestor (LCA)
# ============================================================

def lowest_common_ancestor(root, p, q):
    """
    Find lowest common ancestor of two nodes.
    
    How it works:
    1. If current node is p or q, return it
    2. Search in left and right subtrees
    3. If both return non-null, current is LCA
    4. Otherwise, return the non-null one
    
    Time: O(n), Space: O(h)
    """
    # STEP 1: Base cases
    # - Null node: can't be ancestor
    # - Current node is p or q: this is one of the targets!
    if not root or root.val == p or root.val == q:
        return root
    
    # STEP 2: Search for p and q in left and right subtrees
    # Each recursive call returns:
    # - None if neither p nor q found
    # - The node (p or q) if found
    # - The LCA if both found in that subtree
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    # STEP 3: Analyze results from left and right
    # If BOTH left and right are non-null:
    # - One target found in left subtree
    # - Other target found in right subtree
    # - Current root is the split point = LCA!
    if left and right:
        return root
    
    # STEP 4: Only one side (or neither) found something
    # - If left is non-null: both targets in left subtree (or only left found one)
    # - If right is non-null: both targets in right subtree (or only right found one)
    # - Return whichever is non-null (or None if both null)
    return left if left else right


print("Pattern 6: Lowest Common Ancestor")
print("-" * 60)
print()
print("Tree:")
print("       3")
print("      / \\")
print("     5   1")
print("    / \\ / \\")
print("   6  2 0  8")
print("     / \\")
print("    7   4")
print()

tree4 = TreeNode(3)
tree4.left = TreeNode(5)
tree4.right = TreeNode(1)
tree4.left.left = TreeNode(6)
tree4.left.right = TreeNode(2)
tree4.left.right.left = TreeNode(7)
tree4.left.right.right = TreeNode(4)
tree4.right.left = TreeNode(0)
tree4.right.right = TreeNode(8)

lca1 = lowest_common_ancestor(tree4, 5, 1)
print(f"LCA of 5 and 1: {lca1.val}")
print("Explanation: 3 is the lowest node that has both 5 and 1 as descendants")

lca2 = lowest_common_ancestor(tree4, 5, 4)
print(f"\nLCA of 5 and 4: {lca2.val}")
print("Explanation: 5 is ancestor of 4, so 5 is the LCA")
print()


# ============================================================
# Pattern 7: Serialize and Deserialize
# ============================================================

def serialize(root):
    """
    Convert tree to string (preorder with nulls).
    
    How it works:
    1. Preorder traversal
    2. Use special marker for null nodes
    3. Join with delimiter
    
    Time: O(n), Space: O(n)
    """
    def helper(node):
        if not node:
            return ['null']
        return [str(node.val)] + helper(node.left) + helper(node.right)
    
    return ','.join(helper(root))


def deserialize(data):
    """
    Convert string back to tree.
    
    How it works:
    1. Split string into list
    2. Build tree recursively (preorder)
    3. Consume one value per node
    
    Time: O(n), Space: O(n)
    """
    def helper(values):
        val = values.pop(0)
        if val == 'null':
            return None
        
        node = TreeNode(int(val))
        node.left = helper(values)
        node.right = helper(values)
        return node
    
    return helper(data.split(','))


print("Pattern 7: Serialize and Deserialize")
print("-" * 60)
print()
print("Tree:")
print("     1")
print("    / \\")
print("   2   3")
print("      / \\")
print("     4   5")
print()

tree5 = TreeNode(1)
tree5.left = TreeNode(2)
tree5.right = TreeNode(3)
tree5.right.left = TreeNode(4)
tree5.right.right = TreeNode(5)

serialized = serialize(tree5)
print(f"Serialized: {serialized}")

deserialized = deserialize(serialized)
print(f"Deserialized and re-serialized: {serialize(deserialized)}")
print("Trees match!")
print()


# ============================================================
# Pattern 8: Diameter of Tree
# ============================================================

def diameter_of_tree(root):
    """
    Find longest path between any two nodes.
    
    How it works:
    1. For each node, diameter might pass through it
    2. Diameter through node = left_height + right_height
    3. Track maximum diameter seen
    4. Return height for parent's calculation
    
    Time: O(n), Space: O(h)
    """
    # STEP 1: Use list to hold max_diameter so inner function can modify it
    # (Python nested functions can't reassign outer variables directly)
    max_diameter = [0]
    
    def height(node):
        # STEP 2: Base case - null node has height 0
        if not node:
            return 0
        
        # STEP 3: Recursively get heights of left and right subtrees
        # This processes the tree bottom-up (leaf to root)
        left_height = height(node.left)
        right_height = height(node.right)
        
        # STEP 4: Calculate diameter THROUGH this node
        # Diameter = path from left subtree → node → right subtree
        # Number of edges = left_height + right_height
        # Example: left_height=2, right_height=1 means:
        #   - 2 edges from node down to leftmost node
        #   - 1 edge from node down to rightmost node
        #   - Total path = 3 edges
        current_diameter = left_height + right_height
        
        # STEP 5: Update global maximum diameter
        # The answer might not go through root - could be in any subtree
        max_diameter[0] = max(max_diameter[0], current_diameter)
        
        # STEP 6: Return height of this subtree for parent's calculation
        # Height = 1 (current node) + max of left/right heights
        # We return height (not diameter) because parent needs to know
        # how far down it can reach through this node
        return 1 + max(left_height, right_height)
    
    # STEP 7: Start recursion from root
    height(root)
    # STEP 8: Return the maximum diameter found
    return max_diameter[0]


print("Pattern 8: Diameter of Tree")
print("-" * 60)
print()
print("Tree:")
print("       1")
print("      / \\")
print("     2   3")
print("    / \\")
print("   4   5")
print()

tree6 = TreeNode(1)
tree6.left = TreeNode(2)
tree6.right = TreeNode(3)
tree6.left.left = TreeNode(4)
tree6.left.right = TreeNode(5)

print(f"Diameter: {diameter_of_tree(tree6)}")
print("Longest path: 4 → 2 → 5 (or 4 → 2 → 1 → 3)")
print("Length: 3 edges")
print()


# ============================================================
# Pattern 9: Maximum Path Sum
# ============================================================

def max_path_sum(root):
    """
    Find maximum sum along any path in tree.
    
    How it works:
    1. For each node, path can:
       - Go through node connecting left and right
       - Only go through left
       - Only go through right
       - Just be the node itself
    2. Track maximum sum seen
    3. Return best single path for parent
    
    Time: O(n), Space: O(h)
    """
    max_sum = [float('-inf')]
    
    def max_gain(node):
        if not node:
            return 0
        
        # Get max gain from subtrees (ignore negative gains)
        left_gain = max(0, max_gain(node.left))
        right_gain = max(0, max_gain(node.right))
        
        # Path through this node
        path_sum = node.val + left_gain + right_gain
        
        # Update global maximum
        max_sum[0] = max(max_sum[0], path_sum)
        
        # Return max gain if parent uses this path
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum[0]


print("Pattern 9: Maximum Path Sum")
print("-" * 60)
print()
print("Tree:")
print("      -10")
print("      /  \\")
print("     9   20")
print("         / \\")
print("        15  7")
print()

tree7 = TreeNode(-10)
tree7.left = TreeNode(9)
tree7.right = TreeNode(20)
tree7.right.left = TreeNode(15)
tree7.right.right = TreeNode(7)

print(f"Maximum path sum: {max_path_sum(tree7)}")
print("Best path: 15 → 20 → 7")
print("Sum: 15 + 20 + 7 = 42")
print()


# ============================================================
# Pattern 10: Balanced Tree Check
# ============================================================

def is_balanced(root):
    """
    Check if tree is height-balanced.
    (Heights of left and right subtrees differ by at most 1)
    
    How it works:
    1. Calculate height of each subtree
    2. Check if heights differ by more than 1
    3. Return -1 if unbalanced, height otherwise
    
    Time: O(n), Space: O(h)
    """
    def check_height(node):
        if not node:
            return 0
        
        # Check left subtree
        left_height = check_height(node.left)
        if left_height == -1:
            return -1  # Left subtree unbalanced
        
        # Check right subtree
        right_height = check_height(node.right)
        if right_height == -1:
            return -1  # Right subtree unbalanced
        
        # Check current node
        if abs(left_height - right_height) > 1:
            return -1  # Current node unbalanced
        
        return 1 + max(left_height, right_height)
    
    return check_height(root) != -1


print("Pattern 10: Balanced Tree Check")
print("-" * 60)
print()
print("Balanced tree:")
print("     3")
print("    / \\")
print("   9   20")
print("      /  \\")
print("     15   7")

print(f"Is balanced? {is_balanced(tree1)}")

print("\nUnbalanced tree:")
print("       1")
print("      /")
print("     2")
print("    /")
print("   3")

tree8 = TreeNode(1)
tree8.left = TreeNode(2)
tree8.left.left = TreeNode(3)

print(f"Is balanced? {is_balanced(tree8)}")
print()


# Summary
print("=" * 60)
print("Tree Traversal Pattern Summary")
print("=" * 60)
print()
print("BFS Patterns (use queue):")
print("  1. Level Order - process level by level")
print("  2. Zigzag - alternate direction each level")
print("  3. Right/Left View - rightmost/leftmost at each level")
print("  4. Vertical Order - group by column number")
print()
print("DFS Patterns (use recursion):")
print("  5. Path Sum - track sum along root-to-leaf paths")
print("  6. LCA - find common ancestor")
print("  7. Serialize - convert tree to/from string")
print("  8. Diameter - longest path between any nodes")
print("  9. Max Path Sum - maximum sum along any path")
print(" 10. Balance Check - verify height property")
print()
print("Key Techniques:")
print("  • Use queue for BFS (level-by-level)")
print("  • Use recursion for DFS (depth-first)")
print("  • Track global variables for max/min")
print("  • Return multiple values (height + result)")
print("  • Backtracking for path problems")
print()
