"""
NeetCode 150 - Trees
====================
Binary tree traversal and manipulation (15 problems).
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# PATTERN: DFS (Recursion)
def invert_tree(root):
    """
    Invert Binary Tree - mirror the tree.
    
    Pattern: Recursive DFS with swap
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return None
    
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# PATTERN: DFS (Recursion)
def max_depth(root):
    """
    Maximum Depth of Binary Tree.
    
    Pattern: Recursive DFS
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# PATTERN: DFS (Recursion)
def diameter_of_binary_tree(root):
    """
    Diameter of Binary Tree - longest path between any two nodes.
    
    Pattern: DFS with path tracking
    
    Algorithm Steps:
    1. For each node, diameter through it = left_height + right_height
    2. Track maximum diameter seen
    
    Time: O(n), Space: O(h)
    """
    diameter = [0]
    
    def height(node):
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        diameter[0] = max(diameter[0], left + right)
        return 1 + max(left, right)
    
    height(root)
    return diameter[0]


# PATTERN: DFS (Recursion)
def is_balanced(root):
    """
    Balanced Binary Tree - height difference <= 1 for all nodes.
    
    Pattern: DFS with height tracking
    
    Time: O(n), Space: O(h)
    """
    def height(node):
        if not node:
            return 0
        
        left = height(node.left)
        right = height(node.right)
        
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        
        return 1 + max(left, right)
    
    return height(root) != -1


# PATTERN: DFS (Recursion)
def is_same_tree(p, q):
    """
    Same Tree - check if two trees are identical.
    
    Pattern: Recursive pre-order traversal
    
    Time: O(n), Space: O(h)
    """
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


# PATTERN: DFS (Recursion)
def is_subtree(root, subRoot):
    """
    Subtree of Another Tree.
    
    Pattern: Check at each node if subtree matches
    
    Time: O(m * n), Space: O(h)
    """
    if not root:
        return False
    if is_same_tree(root, subRoot):
        return True
    return is_subtree(root.left, subRoot) or is_subtree(root.right, subRoot)


# PATTERN: BST Property
def lowest_common_ancestor(root, p, q):
    """
    Lowest Common Ancestor of BST.
    
    Pattern: BST property - compare values
    
    Algorithm Steps:
    1. If both p and q < root, LCA is in left subtree
    2. If both p and q > root, LCA is in right subtree
    3. Otherwise, root is LCA
    
    Time: O(h), Space: O(1) iterative
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root


# PATTERN: BFS (Level Order)
def level_order(root):
    """
    Binary Tree Level Order Traversal.
    
    Pattern: BFS with queue
    
    Time: O(n), Space: O(w) where w = max width
    """
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    
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


# PATTERN: BFS (Level Order)
def right_side_view(root):
    """
    Binary Tree Right Side View - rightmost node at each level.
    
    Pattern: BFS, take last node of each level
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:  # Last node in level
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result


# PATTERN: DFS with Counter
def good_nodes(root):
    """
    Count Good Nodes - node X is good if no node on path from root to X has value > X.
    
    Pattern: DFS with max value tracking
    
    Time: O(n), Space: O(h)
    """
    def dfs(node, max_val):
        if not node:
            return 0
        
        count = 1 if node.val >= max_val else 0
        max_val = max(max_val, node.val)
        
        count += dfs(node.left, max_val)
        count += dfs(node.right, max_val)
        
        return count
    
    return dfs(root, float('-inf'))


# PATTERN: BST In-order Traversal
def is_valid_bst(root):
    """
    Validate Binary Search Tree.
    
    Pattern: DFS with range validation
    
    Time: O(n), Space: O(h)
    """
    def valid(node, left, right):
        if not node:
            return True
        if not (left < node.val < right):
            return False
        return valid(node.left, left, node.val) and valid(node.right, node.val, right)
    
    return valid(root, float('-inf'), float('inf'))


# PATTERN: BST In-order Traversal
def kth_smallest(root, k):
    """
    Kth Smallest Element in BST.
    
    Pattern: In-order traversal (sorted order for BST)
    
    Time: O(n), Space: O(h)
    """
    stack = []
    curr = root
    count = 0
    
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right


# PATTERN: DFS with Array Slicing
def build_tree(preorder, inorder):
    """
    Construct Binary Tree from Preorder and Inorder Traversal.
    
    Pattern: Recursive construction with index mapping
    
    Algorithm Steps:
    1. First element of preorder is root
    2. Find root in inorder to split left/right subtrees
    3. Recursively build left and right
    
    Time: O(n), Space: O(n)
    """
    if not preorder or not inorder:
        return None
    
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])
    
    root.left = build_tree(preorder[1:mid + 1], inorder[:mid])
    root.right = build_tree(preorder[mid + 1:], inorder[mid + 1:])
    
    return root


# PATTERN: DFS (Path Sum)
def max_path_sum(root):
    """
    Binary Tree Maximum Path Sum.
    
    Pattern: DFS with global maximum tracking
    
    Algorithm Steps:
    1. For each node, calculate max path through it
    2. Path through node = node.val + left_gain + right_gain
    3. Return to parent: node.val + max(left_gain, right_gain)
    
    Time: O(n), Space: O(h)
    """
    max_sum = [float('-inf')]
    
    def max_gain(node):
        if not node:
            return 0
        
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)
        
        # Path through current node
        path_sum = node.val + left_gain + right_gain
        max_sum[0] = max(max_sum[0], path_sum)
        
        # Return max gain continuing to parent
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum[0]


# PATTERN: DFS + String Encoding
def serialize(root):
    """
    Serialize Binary Tree to string.
    
    Pattern: Pre-order DFS with null markers
    
    Time: O(n), Space: O(n)
    """
    def dfs(node):
        if not node:
            return "null,"
        return str(node.val) + "," + dfs(node.left) + dfs(node.right)
    
    return dfs(root)


def deserialize(data):
    """
    Deserialize string to Binary Tree.
    
    Pattern: Pre-order reconstruction
    
    Time: O(n), Space: O(n)
    """
    def dfs(nodes):
        val = next(nodes)
        if val == "null":
            return None
        node = TreeNode(int(val))
        node.left = dfs(nodes)
        node.right = dfs(nodes)
        return node
    
    return dfs(iter(data.split(",")))


if __name__ == "__main__":
    print("=== NeetCode 150 - Trees ===\n")
    
    # Create sample tree: [3,9,20,null,null,15,7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    print(f"Max Depth: {max_depth(root)}")
    print(f"Is Balanced: {is_balanced(root)}")
    print(f"Diameter: {diameter_of_binary_tree(root)}")
    print(f"Level Order: {level_order(root)}")
    print(f"Right Side View: {right_side_view(root)}")
    print(f"Good Nodes: {good_nodes(root)}")
    print(f"Is Valid BST: {is_valid_bst(root)}")
    print(f"Max Path Sum: {max_path_sum(root)}")
    
    # Serialize/Deserialize
    serialized = serialize(root)
    print(f"Serialized: {serialized}")
    deserialized = deserialize(serialized)
    print(f"Deserialized Max Depth: {max_depth(deserialized)}")
