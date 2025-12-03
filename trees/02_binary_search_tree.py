"""
Binary Search Trees (BST)
==========================
Understanding Binary Search Trees and their operations.
"""

from typing import Optional


class BSTNode:
    """Binary Search Tree Node"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


print("=" * 60)
print("What is a Binary Search Tree (BST)?")
print("=" * 60)
print("A Binary Search Tree is a binary tree with a special property:")
print()
print("BST Property:")
print("  For every node:")
print("  - All values in LEFT subtree < node value")
print("  - All values in RIGHT subtree > node value")
print("  - Both left and right subtrees are also BSTs")
print()
print("Why BSTs?")
print("  - Fast search: O(log n) average")
print("  - Fast insert: O(log n) average")
print("  - Fast delete: O(log n) average")
print("  - Inorder traversal gives sorted order")
print("  - No duplicates (typically)")
print()
print("Example BST:")
print("        8")
print("      /   \\")
print("     3     10")
print("    / \\      \\")
print("   1   6     14")
print("      / \\    /")
print("     4   7  13")
print()
print("Notice: 1,3,4,6,7 < 8 < 10,13,14")
print()


# BST Operations
class BST:
    """Binary Search Tree implementation"""
    
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        """
        Insert value into BST.
        Time: O(h) where h is height
        Average: O(log n), Worst: O(n) for skewed tree
        """
        def insert_helper(node, val):
            # Base case: found position for new node
            if not node:
                return BSTNode(val)
            
            # Decide which subtree to insert into
            if val < node.val:
                node.left = insert_helper(node.left, val)
            elif val > node.val:
                node.right = insert_helper(node.right, val)
            # If val == node.val, don't insert (no duplicates)
            
            return node
        
        self.root = insert_helper(self.root, val)
    
    def search(self, val):
        """
        Search for value in BST.
        Time: O(h) - average O(log n)
        """
        def search_helper(node, val):
            # Base cases
            if not node:
                return False
            if node.val == val:
                return True
            
            # Search in appropriate subtree
            if val < node.val:
                return search_helper(node.left, val)
            else:
                return search_helper(node.right, val)
        
        return search_helper(self.root, val)
    
    def find_min(self, node=None):
        """
        Find minimum value (leftmost node).
        Time: O(h)
        """
        if node is None:
            node = self.root
        
        if not node:
            return None
        
        # Keep going left
        while node.left:
            node = node.left
        
        return node.val
    
    def find_max(self, node=None):
        """
        Find maximum value (rightmost node).
        Time: O(h)
        """
        if node is None:
            node = self.root
        
        if not node:
            return None
        
        # Keep going right
        while node.right:
            node = node.right
        
        return node.val
    
    def delete(self, val):
        """
        Delete value from BST.
        
        Three cases to handle:
        1. Leaf node (no children) - simply remove it
        2. One child - replace node with its child
        3. Two children - replace with inorder successor, then delete successor
        
        Detailed example - Delete 50 from:
                50
              /    \\
            30      70
           /  \\    /  \\
          20  40  60  80
         /
        10
        
        Case 1 - Delete 10 (leaf):
          10 has no children, just remove it
          Result: parent's left pointer becomes None
        
        Case 2 - Delete 20 (one child):
          20 has one child (10)
          Replace 20 with 10
          Before:        After:
            30             30
           /  \\           /  \\
          20  40         10  40
         /
        10
        
        Case 3 - Delete 50 (two children) - MOST COMPLEX:
          Step 1: Find inorder successor (smallest in right subtree)
            Start at 50's right child (70)
            Go left as far as possible: 70 → 60
            Successor = 60
          
          Step 2: Copy successor's value to node being deleted
                60  ← Copy this value
              /    \\
            30      70
           /  \\    /  \\
          20  40  60  80  ← Original 60 still here
          
          Step 3: Delete the successor (60) from right subtree
            60 is a leaf, so Case 1 applies
            Result:
                60
              /    \\
            30      70
           /  \\      \\
          20  40      80
        
        Why inorder successor?
          - It's the next larger value in sorted order
          - Maintains BST property (all left < 60 < all right)
          - Always in right subtree (may be right child itself)
          - Has at most one child (right child only)
        
        Alternative: Could use inorder predecessor (largest in left subtree)
        
        Time: O(h) - average O(log n)
        Space: O(h) for recursion stack
        """
        def delete_helper(node, val):
            if not node:
                return None
            
            # Find the node to delete
            if val < node.val:
                node.left = delete_helper(node.left, val)
            elif val > node.val:
                node.right = delete_helper(node.right, val)
            else:
                # Found the node to delete
                
                # Case 1: Leaf node (no children)
                if not node.left and not node.right:
                    return None
                
                # Case 2: One child
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                
                # Case 3: Two children
                # Find inorder successor (smallest in right subtree)
                min_right = node.right
                while min_right.left:
                    min_right = min_right.left
                
                # Replace node's value with successor's value
                node.val = min_right.val
                
                # Delete the successor (will be Case 1 or 2)
                node.right = delete_helper(node.right, min_right.val)
            
            return node
        
        self.root = delete_helper(self.root, val)
    
    def inorder(self):
        """Inorder traversal (gives sorted order)"""
        result = []
        
        def helper(node):
            if node:
                helper(node.left)
                result.append(node.val)
                helper(node.right)
        
        helper(self.root)
        return result


print("=" * 60)
print("BST Operations Demo")
print("=" * 60)

# Create BST and insert values
bst = BST()
values = [8, 3, 10, 1, 6, 14, 4, 7, 13]

print("\nInserting values: 8, 3, 10, 1, 6, 14, 4, 7, 13")
for val in values:
    bst.insert(val)

print("\nResulting BST structure:")
print("        8")
print("      /   \\")
print("     3     10")
print("    / \\      \\")
print("   1   6     14")
print("      / \\    /")
print("     4   7  13")

print(f"\nInorder traversal (sorted): {bst.inorder()}")

print(f"\nSearch for 6: {bst.search(6)}")
print(f"Search for 15: {bst.search(15)}")

print(f"\nMinimum value: {bst.find_min()}")
print(f"Maximum value: {bst.find_max()}")

print("\nDeleting 10 (node with one child)...")
bst.delete(10)
print(f"Inorder after delete: {bst.inorder()}")

print("\nDeleting 3 (node with two children)...")
bst.delete(3)
print(f"Inorder after delete: {bst.inorder()}")

print()


# How Insert Works
print("=" * 60)
print("How BST Insert Works")
print("=" * 60)

print("\nInserting 5 into BST:")
print()
print("Step 1: Start at root (8)")
print("        8 ← Start here")
print("      /   \\")
print("     3     10")
print("    / \\")
print("   1   6")
print()
print("Step 2: 5 < 8, go left to 3")
print("        8")
print("      /")
print("     3 ← Now here")
print("    / \\")
print("   1   6")
print()
print("Step 3: 5 > 3, go right to 6")
print("        8")
print("      /")
print("     3")
print("      \\")
print("       6 ← Now here")
print()
print("Step 4: 5 < 6, go left (empty)")
print("        8")
print("      /")
print("     3")
print("      \\")
print("       6")
print("      /")
print("     5 ← Insert here!")
print()


# How Delete Works
print("=" * 60)
print("How BST Delete Works")
print("=" * 60)

print("\nThree cases when deleting a node:")
print()
print("Case 1: Deleting LEAF node (no children)")
print("  Example: Delete 1")
print()
print("  Before:        After:")
print("     3              3")
print("    / \\            / \\")
print("   1   6          ∅   6")
print()
print("  Simply remove the node.")
print()

print("Case 2: Deleting node with ONE child")
print("  Example: Delete 10")
print()
print("  Before:        After:")
print("     8              8")
print("      \\              \\")
print("      10             14")
print("        \\")
print("        14")
print()
print("  Replace node with its child.")
print()

print("Case 3: Deleting node with TWO children")
print("  Example: Delete 3")
print()
print("  Before:")
print("     8")
print("    / \\")
print("   3   10")
print("  / \\")
print(" 1   6")
print("    / \\")
print("   4   7")
print()
print("  Step 1: Find inorder successor (smallest in right subtree)")
print("          That's 4 (leftmost in right subtree of 3)")
print()
print("  Step 2: Replace 3's value with 4")
print("     8")
print("    / \\")
print("   4   10")
print("  / \\")
print(" 1   6")
print("    / \\")
print("   4   7  ← Still here, will be deleted")
print()
print("  Step 3: Delete the duplicate 4 (now a Case 1 or 2)")
print("     8")
print("    / \\")
print("   4   10")
print("  / \\")
print(" 1   6")
print("      \\")
print("       7")
print()


# BST Validation
def is_valid_bst(root):
    """
    Check if tree is a valid BST.
    Time: O(n), Space: O(h)
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        # Check BST property
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Check left subtree (values must be < node.val)
        # Check right subtree (values must be > node.val)
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


print("=" * 60)
print("BST Validation")
print("=" * 60)

print("\nValid BST:")
print("     5")
print("   /   \\")
print("  3     7")
print(" / \\   / \\")
print("1   4 6   9")

valid_bst = BSTNode(5)
valid_bst.left = BSTNode(3)
valid_bst.right = BSTNode(7)
valid_bst.left.left = BSTNode(1)
valid_bst.left.right = BSTNode(4)
valid_bst.right.left = BSTNode(6)
valid_bst.right.right = BSTNode(9)

print(f"Is valid BST? {is_valid_bst(valid_bst)}")

print("\nInvalid BST:")
print("     5")
print("   /   \\")
print("  3     7")
print(" / \\   / \\")
print("1   6 4   9  ← 6 > 5 (violates BST property)")

invalid_bst = BSTNode(5)
invalid_bst.left = BSTNode(3)
invalid_bst.right = BSTNode(7)
invalid_bst.left.left = BSTNode(1)
invalid_bst.left.right = BSTNode(6)  # Invalid: 6 > 5
invalid_bst.right.left = BSTNode(4)
invalid_bst.right.right = BSTNode(9)

print(f"Is valid BST? {is_valid_bst(invalid_bst)}")

print()


# BST Common Operations
def kth_smallest(root, k):
    """
    Find kth smallest element in BST.
    Time: O(h + k), Space: O(h)
    """
    result = []
    
    def inorder(node):
        if not node or len(result) >= k:
            return
        
        inorder(node.left)
        result.append(node.val)
        inorder(node.right)
    
    inorder(root)
    return result[k-1] if k <= len(result) else None


def lowest_common_ancestor_bst(root, p, q):
    """
    Find lowest common ancestor in BST.
    Time: O(h), Space: O(1)
    """
    # Start from root
    current = root
    
    while current:
        # If both p and q are smaller, go left
        if p < current.val and q < current.val:
            current = current.left
        # If both p and q are larger, go right
        elif p > current.val and q > current.val:
            current = current.right
        else:
            # We found the split point (LCA)
            return current.val
    
    return None


def range_sum_bst(root, low, high):
    """
    Sum of all nodes with values in range [low, high].
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0
    
    total = 0
    
    # Add current node if in range
    if low <= root.val <= high:
        total += root.val
    
    # Search left if current value > low
    if root.val > low:
        total += range_sum_bst(root.left, low, high)
    
    # Search right if current value < high
    if root.val < high:
        total += range_sum_bst(root.right, low, high)
    
    return total


print("=" * 60)
print("Common BST Operations")
print("=" * 60)

bst2 = BST()
for val in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    bst2.insert(val)

print("\nBST:")
print("        8")
print("      /   \\")
print("     3     10")
print("    / \\      \\")
print("   1   6     14")
print("      / \\    /")
print("     4   7  13")

print(f"\nInorder: {bst2.inorder()}")

k = 3
print(f"\n{k}rd smallest element: {kth_smallest(bst2.root, k)}")

p, q = 1, 7
print(f"\nLowest Common Ancestor of {p} and {q}: {lowest_common_ancestor_bst(bst2.root, p, q)}")

low, high = 4, 10
print(f"\nSum of values in range [{low}, {high}]: {range_sum_bst(bst2.root, low, high)}")

print()


# BST vs Array vs Hash Table
print("=" * 60)
print("BST vs Other Data Structures")
print("=" * 60)

print("\nOperation Comparison:")
print()
print("                BST (balanced)  Array (sorted)  Hash Table")
print("  Search        O(log n)        O(log n)        O(1)")
print("  Insert        O(log n)        O(n)            O(1)")
print("  Delete        O(log n)        O(n)            O(1)")
print("  Min/Max       O(log n)        O(1)            O(n)")
print("  Sorted Order  O(n)            Already sorted  O(n log n)")
print("  Range Query   O(log n + k)    O(log n + k)    O(n)")
print()
print("When to use BST:")
print("  ✓ Need dynamic sorted data")
print("  ✓ Frequent insertions/deletions")
print("  ✓ Need min/max quickly")
print("  ✓ Range queries")
print("  ✓ Finding predecessors/successors")
print()
print("When NOT to use BST:")
print("  ✗ Just need fast lookup (use hash table)")
print("  ✗ Data rarely changes (use sorted array)")
print("  ✗ Can't guarantee balance (degenerates to O(n))")
print()


# BST Real-World Applications
print("=" * 60)
print("Real-World Applications of BST")
print("=" * 60)

print("\n1. Database Indexing:")
print("   - B-trees (generalization of BST)")
print("   - Fast search, insert, delete")
print("   - Maintain sorted order")

print("\n2. File Systems:")
print("   - Directory structures")
print("   - Quick file lookup")
print("   - Alphabetical ordering")

print("\n3. Auto-complete:")
print("   - Trie (specialized BST)")
print("   - Dictionary suggestions")
print("   - Search engine queries")

print("\n4. Databases:")
print("   - In-memory databases")
print("   - Transaction logs")
print("   - Priority-based scheduling")

print("\n5. Graphics:")
print("   - Scene management")
print("   - Collision detection")
print("   - Spatial partitioning")

print("\n6. Network Routing:")
print("   - IP address lookup")
print("   - Routing tables")
print("   - Fast packet forwarding")

print()
