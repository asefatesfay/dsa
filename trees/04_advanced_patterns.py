"""
Advanced Tree Patterns
======================
Complex tree problems and advanced techniques.
"""

from collections import deque, defaultdict
from typing import Optional, List


class TreeNode:
    """Binary tree node"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


print("=" * 60)
print("Advanced Tree Patterns")
print("=" * 60)
print()


# ============================================================
# Pattern 1: Construct Binary Tree from Traversals
# ============================================================

def build_tree_from_inorder_preorder(preorder, inorder):
    """
    Construct tree from preorder and inorder traversals.
    
    How it works:
    1. First element in preorder is root
    2. Find root in inorder to split left/right subtrees
    3. Recursively build left and right subtrees
    4. Left size determines preorder split
    
    Example:
      preorder = [3,9,20,15,7]
      inorder = [9,3,15,20,7]
      
      Root = 3 (first in preorder)
      In inorder: [9] | 3 | [15,20,7]
                  left     right
    
    Time: O(n), Space: O(n)
    """
    if not preorder or not inorder:
        return None
    
    # STEP 1: Build hash map for O(1) lookup of root position in inorder
    # Key insight: We'll need to find root in inorder array many times
    # Without map: O(n) search each time = O(n²) total
    # With map: O(1) search = O(n) total
    inorder_map = {val: i for i, val in enumerate(inorder)}
    
    def helper(pre_start, pre_end, in_start, in_end):
        # STEP 2: Base case - no elements to process
        if pre_start > pre_end:
            return None
        
        # STEP 3: First element in preorder range is the root
        # Preorder visits: root → left subtree → right subtree
        root_val = preorder[pre_start]
        root = TreeNode(root_val)
        
        # STEP 4: Find root's position in inorder
        # This splits inorder into: [left subtree] root [right subtree]
        in_root_idx = inorder_map[root_val]
        
        # STEP 5: Calculate size of left subtree
        # Left subtree = elements from in_start to in_root_idx-1
        left_size = in_root_idx - in_start
        
        # STEP 6: Recursively build LEFT subtree
        # In preorder: elements from pre_start+1 to pre_start+left_size
        #   (skip pre_start because that's the root we just used)
        # In inorder: elements from in_start to in_root_idx-1
        root.left = helper(
            pre_start + 1,           # Skip root in preorder
            pre_start + left_size,   # Include left_size elements
            in_start,                # Start of left in inorder
            in_root_idx - 1          # End of left in inorder
        )
        
        # STEP 7: Recursively build RIGHT subtree
        # In preorder: elements after left subtree
        # In inorder: elements from in_root_idx+1 to in_end
        root.right = helper(
            pre_start + left_size + 1,  # After root and left subtree
            pre_end,                     # Rest of preorder
            in_root_idx + 1,             # After root in inorder
            in_end                       # End of inorder range
        )
        
        # STEP 8: Return constructed subtree
        return root
    
    return helper(0, len(preorder) - 1, 0, len(inorder) - 1)


print("Pattern 1: Construct Tree from Traversals")
print("-" * 60)
print()

preorder = [3, 9, 20, 15, 7]
inorder = [9, 3, 15, 20, 7]

print(f"Preorder: {preorder}")
print(f"Inorder: {inorder}")
print()
print("How it works:")
print("  Step 1: Root = 3 (first in preorder)")
print("  Step 2: Find 3 in inorder → [9] | 3 | [15,20,7]")
print("  Step 3: Left subtree has 1 element, right has 3")
print("  Step 4: Recursively build left from [9] and [9]")
print("  Step 5: Recursively build right from [20,15,7] and [15,20,7]")
print()

tree = build_tree_from_inorder_preorder(preorder, inorder)

def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result

print(f"Result (level order): {level_order(tree)}")
print()


# ============================================================
# Pattern 2: Binary Tree from Inorder and Postorder
# ============================================================

def build_tree_from_inorder_postorder(inorder, postorder):
    """
    Construct tree from inorder and postorder traversals.
    
    How it works:
    1. Last element in postorder is root
    2. Find root in inorder to split left/right
    3. Recursively build subtrees
    
    Time: O(n), Space: O(n)
    """
    if not inorder or not postorder:
        return None
    
    inorder_map = {val: i for i, val in enumerate(inorder)}
    
    def helper(in_start, in_end):
        if in_start > in_end:
            return None
        
        # Root is last element in postorder
        root_val = postorder.pop()
        root = TreeNode(root_val)
        
        # Find root in inorder
        in_root_idx = inorder_map[root_val]
        
        # Build right first (postorder processes right before left)
        root.right = helper(in_root_idx + 1, in_end)
        root.left = helper(in_start, in_root_idx - 1)
        
        return root
    
    return helper(0, len(inorder) - 1)


print("Pattern 2: Tree from Inorder and Postorder")
print("-" * 60)
print()

inorder2 = [9, 3, 15, 20, 7]
postorder = [9, 15, 7, 20, 3]

print(f"Inorder: {inorder2}")
print(f"Postorder: {postorder}")
print()
print("Root = 3 (last in postorder)")
print("Build right subtree first, then left")
print()

tree2 = build_tree_from_inorder_postorder(inorder2, postorder[:])
print(f"Result (level order): {level_order(tree2)}")
print()


# ============================================================
# Pattern 3: Flatten Binary Tree to Linked List
# ============================================================

def flatten_tree(root):
    """
    Flatten tree to linked list (in-place, preorder).
    
    How it works:
    1. Process right subtree first
    2. Process left subtree
    3. Connect current to flattened left
    4. Find end of flattened left, connect to right
    
    Time: O(n), Space: O(h)
    """
    def flatten_helper(node):
        # STEP 1: Base case - null node
        if not node:
            return None
        
        # STEP 2: Save the right subtree
        # We need this because we're going to modify node.right
        right_subtree = node.right
        
        # STEP 3: If there's a left subtree, process it
        if node.left:
            # STEP 4: Move left subtree to right
            # This is the "flattening" - everything goes to the right
            node.right = node.left
            node.left = None  # Clear left pointer (linked list uses only right)
            
            # STEP 5: Find the tail of the flattened left subtree
            # We need to find the end so we can attach the right subtree
            # The tail is the rightmost node (keep going right until null)
            tail = node.right
            while tail.right:
                tail = tail.right
            
            # STEP 6: Connect tail to the saved right subtree
            # Now we have: node → (flattened left) → (original right)
            tail.right = right_subtree
        
        # STEP 7: Continue flattening the right side
        # At this point, node.right contains what we want to flatten next:
        # - Either the moved left subtree (followed by original right)
        # - Or just the original right subtree (if no left existed)
        flatten_helper(node.right)
    
    flatten_helper(root)


print("Pattern 3: Flatten to Linked List")
print("-" * 60)
print()
print("Before:")
print("     1")
print("    / \\")
print("   2   5")
print("  / \\   \\")
print(" 3   4   6")
print()

tree3 = TreeNode(1)
tree3.left = TreeNode(2)
tree3.right = TreeNode(5)
tree3.left.left = TreeNode(3)
tree3.left.right = TreeNode(4)
tree3.right.right = TreeNode(6)

flatten_tree(tree3)

print("After (preorder linked list):")
print("1 → 2 → 3 → 4 → 5 → 6")

current = tree3
result = []
while current:
    result.append(current.val)
    current = current.right

print(f"Result: {result}")
print()


# ============================================================
# Pattern 4: Recover Binary Search Tree
# ============================================================

def recover_bst(root):
    """
    Fix BST where two nodes are swapped.
    
    How it works:
    1. Inorder traversal should be sorted for valid BST
    2. Find two nodes that break sorted order
    3. Swap their values back
    
    Example: [1,3,2,4] → 3 and 2 are swapped
    
    Time: O(n), Space: O(h)
    """
    # STEP 1: Initialize tracking variables
    # first: first node that's out of order
    # second: second node that's out of order  
    # prev: previous node in inorder traversal (for comparison)
    first = second = prev = None
    
    def inorder(node):
        nonlocal first, second, prev
        
        # STEP 2: Base case
        if not node:
            return
        
        # STEP 3: Process left subtree (inorder: left → node → right)
        inorder(node.left)
        
        # STEP 4: Check if current node violates BST property
        # In valid BST inorder: each node > previous node
        # If prev > current, we found a violation!
        if prev and prev.val > node.val:
            # STEP 5: Record the violation
            if not first:
                # First violation: prev is the first wrong node
                # Example: [1, 3, 2, 4] → when we see 3 > 2
                # first = 3 (prev), second = 2 (current)
                first = prev
            # Always update second
            # This handles both: 
            # - Adjacent swaps: first and second next to each other
            # - Distant swaps: need to update second at second violation
            second = node
        
        # STEP 6: Update prev for next comparison
        prev = node
        
        # STEP 7: Process right subtree
        inorder(node.right)
    
    # STEP 8: Do inorder traversal to find swapped nodes
    inorder(root)
    
    # STEP 9: Swap the values back to fix the BST
    # We only swap values (not node pointers) to keep tree structure
    if first and second:
        first.val, second.val = second.val, first.val


print("Pattern 4: Recover BST")
print("-" * 60)
print()
print("Broken BST (1 and 3 swapped):")
print("     3")
print("    / \\")
print("   1   4")
print("    \\")
print("     2")
print()

tree4 = TreeNode(3)
tree4.left = TreeNode(1)
tree4.right = TreeNode(4)
tree4.left.right = TreeNode(2)

def inorder_list(node):
    result = []
    def helper(n):
        if n:
            helper(n.left)
            result.append(n.val)
            helper(n.right)
    helper(node)
    return result

print(f"Before recovery (inorder): {inorder_list(tree4)}")
print("Expected: [1,2,3,4]")

recover_bst(tree4)

print(f"After recovery (inorder): {inorder_list(tree4)}")
print()


# ============================================================
# Pattern 5: Count Complete Tree Nodes
# ============================================================

def count_nodes_complete_tree(root):
    """
    Count nodes in complete binary tree efficiently.
    
    How it works:
    1. If tree is perfect: count = 2^height - 1
    2. Check if left and right heights are same
    3. If yes, left subtree is perfect
    4. If no, right subtree is perfect
    5. Recurse on non-perfect subtree
    
    Time: O(log²n), Space: O(log n)
    """
    if not root:
        return 0
    
    def get_height(node):
        height = 0
        while node:
            height += 1
            node = node.left
        return height
    
    left_height = get_height(root.left)
    right_height = get_height(root.right)
    
    if left_height == right_height:
        # Left subtree is perfect
        return (1 << left_height) + count_nodes_complete_tree(root.right)
    else:
        # Right subtree is perfect
        return (1 << right_height) + count_nodes_complete_tree(root.left)


print("Pattern 5: Count Complete Tree Nodes")
print("-" * 60)
print()
print("Complete tree:")
print("       1")
print("      / \\")
print("     2   3")
print("    / \\ /")
print("   4  5 6")
print()

tree5 = TreeNode(1)
tree5.left = TreeNode(2)
tree5.right = TreeNode(3)
tree5.left.left = TreeNode(4)
tree5.left.right = TreeNode(5)
tree5.right.left = TreeNode(6)

print(f"Node count: {count_nodes_complete_tree(tree5)}")
print("Optimization: O(log²n) vs O(n) for normal counting")
print()


# ============================================================
# Pattern 6: Binary Tree Cameras
# ============================================================

def min_camera_cover(root):
    """
    Minimum cameras to monitor all nodes.
    (Camera can monitor itself, parent, and children)
    
    How it works:
    1. Leaves don't need cameras (parent can monitor)
    2. Parents of leaves need cameras
    3. Use post-order DFS (bottom-up)
    4. States: 0=needs cover, 1=has camera, 2=covered
    
    Time: O(n), Space: O(h)
    """
    cameras = [0]
    
    def dfs(node):
        if not node:
            return 2  # Null nodes are covered
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # If any child needs cover, place camera here
        if left == 0 or right == 0:
            cameras[0] += 1
            return 1  # This node has camera
        
        # If any child has camera, this is covered
        if left == 1 or right == 1:
            return 2  # Covered by child
        
        # Both children covered, but not this node
        return 0  # Needs cover
    
    # Handle root separately
    if dfs(root) == 0:
        cameras[0] += 1
    
    return cameras[0]


print("Pattern 6: Binary Tree Cameras")
print("-" * 60)
print()
print("Tree:")
print("       0")
print("      / \\")
print("     0   0")
print("      \\   \\")
print("       0   0")
print()

tree6 = TreeNode(0)
tree6.left = TreeNode(0)
tree6.right = TreeNode(0)
tree6.left.right = TreeNode(0)
tree6.right.right = TreeNode(0)

print(f"Minimum cameras needed: {min_camera_cover(tree6)}")
print("Place cameras at nodes to cover all")
print()


# ============================================================
# Pattern 7: House Robber III
# ============================================================

def rob_tree(root):
    """
    Rob houses in tree (can't rob parent and child).
    
    How it works:
    1. For each node, choose to rob or not rob
    2. If rob: add value + not_rob(children)
    3. If not rob: max(rob or not_rob children)
    4. Return max of both choices
    
    Time: O(n), Space: O(h)
    """
    def rob_helper(node):
        if not node:
            return (0, 0)  # (rob, not_rob)
        
        left = rob_helper(node.left)
        right = rob_helper(node.right)
        
        # If we rob this node, can't rob children
        rob = node.val + left[1] + right[1]
        
        # If we don't rob, take max from children
        not_rob = max(left) + max(right)
        
        return (rob, not_rob)
    
    return max(rob_helper(root))


print("Pattern 7: House Robber III")
print("-" * 60)
print()
print("Tree (house values):")
print("       3")
print("      / \\")
print("     2   3")
print("      \\   \\")
print("       3   1")
print()

tree7 = TreeNode(3)
tree7.left = TreeNode(2)
tree7.right = TreeNode(3)
tree7.left.right = TreeNode(3)
tree7.right.right = TreeNode(1)

print(f"Maximum robbery: {rob_tree(tree7)}")
print("Rob: 3 + 3 + 1 = 7 (rob root and leaves)")
print("Don't rob: 2 + 3 = 5 (rob level 1)")
print()


# ============================================================
# Pattern 8: All Nodes Distance K
# ============================================================

def distance_k(root, target_val, k):
    """
    Find all nodes at distance K from target.
    
    How it works:
    1. Build parent pointers for upward traversal
    2. BFS from target node
    3. Track visited to avoid cycles
    4. Stop at distance K
    
    Time: O(n), Space: O(n)
    """
    # Build parent map
    parent = {}
    
    def build_parent(node, par=None):
        if not node:
            return
        parent[node] = par
        build_parent(node.left, node)
        build_parent(node.right, node)
    
    build_parent(root)
    
    # Find target node
    target = None
    def find_target(node):
        nonlocal target
        if not node:
            return
        if node.val == target_val:
            target = node
            return
        find_target(node.left)
        find_target(node.right)
    
    find_target(root)
    
    # BFS from target
    queue = deque([(target, 0)])
    visited = {target}
    result = []
    
    while queue:
        node, dist = queue.popleft()
        
        if dist == k:
            result.append(node.val)
            continue
        
        # Check all neighbors (left, right, parent)
        for neighbor in [node.left, node.right, parent[node]]:
            if neighbor and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return result


print("Pattern 8: All Nodes Distance K")
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

tree8 = TreeNode(3)
tree8.left = TreeNode(5)
tree8.right = TreeNode(1)
tree8.left.left = TreeNode(6)
tree8.left.right = TreeNode(2)
tree8.left.right.left = TreeNode(7)
tree8.left.right.right = TreeNode(4)
tree8.right.left = TreeNode(0)
tree8.right.right = TreeNode(8)

print(f"Nodes at distance 2 from node 5: {distance_k(tree8, 5, 2)}")
print("Distance 2 from 5: [7, 4, 1]")
print()


# ============================================================
# Pattern 9: Distribute Coins in Binary Tree
# ============================================================

def distribute_coins(root):
    """
    Minimum moves to distribute coins evenly.
    (Each node should have exactly 1 coin)
    
    How it works:
    1. Calculate excess/deficit at each node
    2. Excess = coins - 1 (what we can give)
    3. Moves = sum of absolute excess across edges
    4. Use post-order DFS (bottom-up)
    
    Time: O(n), Space: O(h)
    """
    moves = [0]
    
    def dfs(node):
        if not node:
            return 0
        
        # Get excess from children
        left_excess = dfs(node.left)
        right_excess = dfs(node.right)
        
        # Moves = coins that must cross this edge
        moves[0] += abs(left_excess) + abs(right_excess)
        
        # Return excess to parent
        return node.val + left_excess + right_excess - 1
    
    dfs(root)
    return moves[0]


print("Pattern 9: Distribute Coins")
print("-" * 60)
print()
print("Tree (coin counts):")
print("       3")
print("      / \\")
print("     0   0")
print()

tree9 = TreeNode(3)
tree9.left = TreeNode(0)
tree9.right = TreeNode(0)

print(f"Minimum moves: {distribute_coins(tree9)}")
print("Move 1 coin to left, 1 coin to right = 2 moves")
print()


# ============================================================
# Pattern 10: Vertical Sum
# ============================================================

def vertical_sum(root):
    """
    Sum of nodes at each vertical column.
    
    How it works:
    1. Assign column numbers (root=0, left=-1, right=+1)
    2. Sum all nodes in same column
    3. Return sums ordered by column
    
    Time: O(n), Space: O(n)
    """
    column_sums = defaultdict(int)
    
    def dfs(node, col):
        if not node:
            return
        
        column_sums[col] += node.val
        dfs(node.left, col - 1)
        dfs(node.right, col + 1)
    
    dfs(root, 0)
    
    # Return in column order
    return [column_sums[col] for col in sorted(column_sums.keys())]


print("Pattern 10: Vertical Sum")
print("-" * 60)
print()
print("Tree:")
print("       1")
print("      / \\")
print("     2   3")
print("    / \\ / \\")
print("   4  5 6  7")
print()

tree10 = TreeNode(1)
tree10.left = TreeNode(2)
tree10.right = TreeNode(3)
tree10.left.left = TreeNode(4)
tree10.left.right = TreeNode(5)
tree10.right.left = TreeNode(6)
tree10.right.right = TreeNode(7)

print(f"Vertical sums: {vertical_sum(tree10)}")
print("Column -2: 4")
print("Column -1: 2")
print("Column  0: 1+5+6 = 12")
print("Column  1: 3")
print("Column  2: 7")
print()


# Summary
print("=" * 60)
print("Advanced Pattern Summary")
print("=" * 60)
print()
print("Construction:")
print("  1. Build from Preorder+Inorder - first elem is root")
print("  2. Build from Postorder+Inorder - last elem is root")
print("  3. Flatten to Linked List - in-place restructure")
print()
print("BST Problems:")
print("  4. Recover BST - find two swapped nodes")
print("  5. Count Complete Tree - exploit structure")
print()
print("Optimization Problems:")
print("  6. Binary Tree Cameras - minimum coverage")
print("  7. House Robber III - max value, no adjacent")
print()
print("Distance/Position:")
print("  8. Distance K - BFS with parent pointers")
print("  9. Distribute Coins - calculate excess flow")
print(" 10. Vertical Sum - sum by column")
print()
print("Key Techniques:")
print("  • Build index maps for O(1) lookup")
print("  • Track parent pointers for upward traversal")
print("  • Use tuples to return multiple values")
print("  • Post-order for bottom-up calculations")
print("  • BFS with visited set for graph-like problems")
print("  • Column/position tracking with offsets")
print()
