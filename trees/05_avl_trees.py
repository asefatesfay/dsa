"""
AVL Trees (Self-Balancing Binary Search Trees)
===============================================
Understanding AVL trees and their balancing operations.
"""


class AVLNode:
    """AVL Tree Node with height tracking"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # Height of subtree rooted at this node


print("=" * 60)
print("What is an AVL Tree?")
print("=" * 60)
print()
print("An AVL tree is a self-balancing Binary Search Tree where:")
print("  • Heights of left and right subtrees differ by at most 1")
print("  • This property holds for EVERY node")
print("  • Named after inventors: Adelson-Velsky and Landis (1962)")
print()
print("Why AVL Trees?")
print("  • BST can degenerate to O(n) if unbalanced")
print("  • AVL guarantees O(log n) for search, insert, delete")
print("  • Strict balancing ensures minimum height")
print("  • Height of AVL tree with n nodes: 1.44 * log(n)")
print()
print("Balance Factor:")
print("  BF(node) = height(left) - height(right)")
print("  Valid: BF ∈ {-1, 0, 1}")
print("  If |BF| > 1, tree needs rebalancing")
print()
print("Example - Balanced (AVL):")
print("        4  (BF=0)")
print("       / \\")
print("      2   6  (BF=0, BF=0)")
print("     / \\ / \\")
print("    1  3 5  7")
print()
print("Example - Unbalanced (NOT AVL):")
print("        4  (BF=2) ← violates!")
print("       /")
print("      2  (BF=1)")
print("     /")
print("    1  (BF=0)")
print()


class AVLTree:
    """AVL Tree implementation with automatic balancing"""
    
    def __init__(self):
        self.root = None
    
    def get_height(self, node):
        """Get height of node (0 for None)"""
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        """
        Calculate balance factor.
        BF = height(left) - height(right)
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        """Update height based on children's heights"""
        if not node:
            return
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )
    
    def rotate_right(self, z):
        """
        Right rotation (for left-left case).
        
        WHEN TO USE:
        • Node z has balance factor +2 (left-heavy)
        • Left child has balance factor ≥ 0 (also left-heavy or balanced)
        • Insertion happened in the LEFT subtree of LEFT child
        
        VISUAL EXAMPLE WITH COMPLETE TREES:
        
        Before rotation (unbalanced):
                z(30) BF=+2
               /
            y(20) BF=+1
           /   \\
        x(10)  T3(25)
        /  \\
      T1  T2
        
        After rotation (balanced):
              y(20) BF=0
             /    \\
          x(10)   z(30)
          /  \\    /
        T1  T2  T3(25)
        
        WHAT HAPPENS:
        1. y becomes the new root (moves up)
        2. z becomes y's right child (moves down-right)
        3. T3 (y's right subtree) becomes z's left subtree
        4. All other subtrees stay with their original parents
        
        WHY IT WORKS (BST Property Preserved):
        Original order: T1 < x < T2 < y < T3 < z
        After rotation: T1 < x < T2 < y < T3 < z (same!)
        
        Tree structure:
        • T1, T2 stay under x (values < x)
        • T3 moves to z's left (values: y < T3 < z) ✓
        • x stays under y (x < y) ✓
        • z moves to y's right (y < z) ✓
        
        POINTER CHANGES:
        Before: z.left = y,  y.right = T3
        After:  y.right = z, z.left = T3
        
        Time: O(1) - Only 3 pointer changes!
        Space: O(1) - No extra memory needed
        """
        # STEP 1: Save the left child (will become new root)
        # This is y in our diagram - it will replace z as the subtree root
        y = z.left
        
        # STEP 2: Save y's right subtree (will be moved to z's left)
        # This is T3 - it has to move because y.right will point to z
        # Values in T3: x < T3 < y < z
        # After rotation, T3 needs to be z's left child (y < T3 < z)
        T3 = y.right
        
        # STEP 3: Perform rotation - make z the right child of y
        # y "moves up" to replace z as the subtree root
        # This is the core of the rotation!
        y.right = z
        
        # STEP 4: Attach T3 as z's left child
        # T3 values are greater than y but less than z (BST property maintained)
        # Before: T3 was y's right child
        # After: T3 becomes z's left child (makes sense: y < T3 < z)
        z.left = T3
        
        # STEP 5: Update heights (bottom-up: z first, then y)
        # IMPORTANT: Update z before y because y's height depends on z's height!
        # z's height changed because its left child changed (was y, now T3)
        self.update_height(z)
        # y's height changed because it now has z as right child
        self.update_height(y)
        
        # STEP 6: Return new root of this subtree
        # Parent of z (if any) needs to update its pointer to y
        return y
    
    def rotate_left(self, z):
        """
        Left rotation (for right-right case).
        
        WHEN TO USE:
        • Node z has balance factor -2 (right-heavy)
        • Right child has balance factor ≤ 0 (also right-heavy or balanced)
        • Insertion happened in the RIGHT subtree of RIGHT child
        
        VISUAL EXAMPLE WITH COMPLETE TREES:
        
        Before rotation (unbalanced):
            z(10) BF=-2
                \\
                y(20) BF=-1
               /   \\
            T2(15)  x(30)
                    /  \\
                  T3  T4
        
        After rotation (balanced):
              y(20) BF=0
             /    \\
          z(10)   x(30)
             \\    /  \\
            T2  T3  T4
        
        WHAT HAPPENS:
        1. y becomes the new root (moves up)
        2. z becomes y's left child (moves down-left)
        3. T2 (y's left subtree) becomes z's right subtree
        4. All other subtrees stay with their original parents
        
        WHY IT WORKS (BST Property Preserved):
        Original order: z < T2 < y < T3 < x < T4
        After rotation: z < T2 < y < T3 < x < T4 (same!)
        
        Tree structure:
        • T3, T4 stay under x (values > x)
        • T2 moves to z's right (values: z < T2 < y) ✓
        • x stays under y (x > y) ✓
        • z moves to y's left (z < y) ✓
        
        MIRROR IMAGE OF RIGHT ROTATION:
        • Right rotation: pivot node moves up from LEFT
        • Left rotation: pivot node moves up from RIGHT
        • Same logic, opposite directions!
        
        POINTER CHANGES:
        Before: z.right = y,  y.left = T2
        After:  y.left = z,   z.right = T2
        
        Time: O(1) - Only 3 pointer changes!
        Space: O(1) - No extra memory needed
        """
        # STEP 1: Save the right child (will become new root)
        # This is y in our diagram - it will replace z as the subtree root
        y = z.right
        
        # STEP 2: Save y's left subtree (will be moved to z's right)
        # This is T2 - it has to move because y.left will point to z
        # Values in T2: z < T2 < y < x
        # After rotation, T2 needs to be z's right child (z < T2 < y)
        T2 = y.left
        
        # STEP 3: Perform rotation - make z the left child of y
        # y "moves up" to replace z as the subtree root
        # This is the core of the rotation!
        y.left = z
        
        # STEP 4: Attach T2 as z's right child
        # T2 values are greater than z but less than y (BST property maintained)
        # Before: T2 was y's left child
        # After: T2 becomes z's right child (makes sense: z < T2 < y)
        z.right = T2
        
        # STEP 5: Update heights (bottom-up: z first, then y)
        # IMPORTANT: Update z before y because y's height depends on z's height!
        # z's height changed because its right child changed (was y, now T2)
        self.update_height(z)
        # y's height changed because it now has z as left child
        self.update_height(y)
        
        # STEP 6: Return new root of this subtree
        # Parent of z (if any) needs to update its pointer to y
        return y
    
    def insert(self, root, val):
        """
        Insert value and rebalance if needed.
        
        How it works:
        1. Normal BST insert
        2. Update heights on path back to root
        3. Check balance factor at each node
        4. If unbalanced, perform rotation(s)
        
        Time: O(log n), Space: O(log n)
        """
        # STEP 1: Perform standard BST insertion
        if not root:
            return AVLNode(val)
        
        # STEP 2: Recursively insert into appropriate subtree
        if val < root.val:
            root.left = self.insert(root.left, val)
        elif val > root.val:
            root.right = self.insert(root.right, val)
        else:
            # STEP 3: Duplicate values not allowed in AVL tree
            return root
        
        # STEP 4: Update height of current node
        # As we return from recursion, update heights bottom-up
        self.update_height(root)
        
        # STEP 5: Calculate balance factor to check if node became unbalanced
        # BF = height(left) - height(right)
        # Valid range: [-1, 0, 1]
        balance = self.get_balance(root)
        
        # STEP 6: If node is unbalanced, there are 4 cases:
        
        # ========================================
        # Case 1: Left-Left (LL) - Single Right Rotation
        # ========================================
        # Pattern: z has balance factor +2, left child has BF >= 0
        # Structure: z has left child y, y has left child x
        # 
        # Visual:
        #       z (BF=+2)         y
        #      /                 / \\
        #     y (BF>=0)    →    x   z
        #    /
        #   x
        #
        # Fix: Single right rotation at z
        # Why: The "heavy" side (left-left) straightens with one rotation
        if balance > 1 and val < root.left.val:
            return self.rotate_right(root)
        
        # ========================================
        # Case 2: Right-Right (RR) - Single Left Rotation
        # ========================================
        # Pattern: z has balance factor -2, right child has BF <= 0
        # Structure: z has right child y, y has right child x
        #
        # Visual:
        #   z (BF=-2)              y
        #    \\                    / \\
        #     y (BF<=0)    →    z   x
        #      \\
        #       x
        #
        # Fix: Single left rotation at z
        # Why: The "heavy" side (right-right) straightens with one rotation
        if balance < -1 and val > root.right.val:
            return self.rotate_left(root)
        
        # ========================================
        # Case 3: Left-Right (LR) - Double Rotation
        # ========================================
        # Pattern: z has balance factor +2, left child has BF < 0
        # Structure: z has left child y, y has right child x
        #
        # PROBLEM: Single right rotation doesn't work here!
        #
        # If we try single right rotation:
        #       z (BF=+2)           y               y
        #      /                   / \\               \\
        #     y (BF=-1)    →     ?   z    Still    z
        #      \\                       \\          unbalanced!
        #       x                       x
        #
        # SOLUTION: Two rotations!
        #
        # Step 1: Left rotation at y (converts LR to LL case)
        #       z                  z (BF=+2)
        #      /                  /
        #     y (BF=-1)    →    x (BF>=0)    Now it's LL case!
        #      \\                /
        #       x              y
        #
        # Step 2: Right rotation at z (solves the LL case)
        #       z                  x
        #      /                  / \\
        #     x (BF>=0)    →      y   z      Balanced!
        #    /
        #   y
        #
        # Complete transformation:
        #     z              z              x
        #    /              /              / \\
        #   y      →      x      →      y   z
        #    \\            /
        #     x          y
        #
        # WHY TWO ROTATIONS?
        # The \"zig-zag\" pattern (left then right) needs to be
        # straightened before we can balance it
        if balance > 1 and val > root.left.val:
            root.left = self.rotate_left(root.left)  # First: convert LR to LL
            return self.rotate_right(root)            # Second: solve LL
        
        # ========================================
        # Case 4: Right-Left (RL) - Double Rotation
        # ========================================
        # Pattern: z has balance factor -2, right child has BF > 0
        # Structure: z has right child y, y has left child x
        #
        # MIRROR IMAGE of Left-Right case!
        #
        # PROBLEM: Single left rotation doesn't work here!
        #
        # If we try single left rotation:
        #   z (BF=-2)            y              y
        #    \\                  / \\            /
        #     y (BF=+1)  →     z   ?    Still z
        #    /                  /          unbalanced!
        #   x                  x
        #
        # SOLUTION: Two rotations!
        #
        # Step 1: Right rotation at y (converts RL to RR case)
        #   z                  z (BF=-2)
        #    \\                  \\
        #     y (BF=+1)  →       x (BF<=0)    Now it's RR case!
        #    /                    \\
        #   x                      y
        #
        # Step 2: Left rotation at z (solves the RR case)
        #   z                  x
        #    \\                / \\
        #     x (BF<=0)  →   z   y      Balanced!
        #      \\
        #       y
        #
        # Complete transformation:
        #   z              z              x
        #    \\              \\            / \\
        #     y      →      x      →   z   y
        #    /                \\
        #   x                  y
        #
        # WHY TWO ROTATIONS?
        # The \"zig-zag\" pattern (right then left) needs to be
        # straightened before we can balance it
        if balance < -1 and val < root.right.val:
            root.right = self.rotate_right(root.right)  # First: convert RL to RR
            return self.rotate_left(root)                # Second: solve RR
        
        # ========================================
        # KEY INSIGHTS:
        # • Single rotations (LL, RR): straight line patterns
        # • Double rotations (LR, RL): zig-zag patterns
        # • Double rotation = straighten first, then balance
        # • LR and RL are mirror images of each other
        # ========================================
        
        # STEP 7: If balanced (or after rotation), return the node
        return root
    
    def get_min_node(self, node):
        """Find node with minimum value"""
        while node.left:
            node = node.left
        return node
    
    def delete(self, root, val):
        """
        Delete value and rebalance if needed.
        
        How it works:
        1. Normal BST delete
        2. Update heights on path back
        3. Check balance and rotate if needed
        
        Time: O(log n), Space: O(log n)
        """
        # Step 1: Normal BST deletion
        if not root:
            return root
        
        if val < root.val:
            root.left = self.delete(root.left, val)
        elif val > root.val:
            root.right = self.delete(root.right, val)
        else:
            # Node to delete found
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            # Node has two children
            temp = self.get_min_node(root.right)
            root.val = temp.val
            root.right = self.delete(root.right, temp.val)
        
        if not root:
            return root
        
        # Step 2: Update height
        self.update_height(root)
        
        # Step 3: Get balance factor
        balance = self.get_balance(root)
        
        # Step 4: Rebalance if needed
        
        # Left-Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.rotate_right(root)
        
        # Left-Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        
        # Right-Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.rotate_left(root)
        
        # Right-Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        
        return root
    
    def inorder(self, node, result=None):
        """Inorder traversal (sorted order)"""
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.val)
            self.inorder(node.right, result)
        return result
    
    def preorder(self, node, result=None):
        """Preorder traversal"""
        if result is None:
            result = []
        if node:
            result.append(node.val)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result


print("=" * 60)
print("Four Types of Rotations")
print("=" * 60)
print()

print("1. LEFT-LEFT Case (Single Right Rotation)")
print("-" * 60)
print()
print("Occurs when:")
print("  • Insert into left subtree of left child")
print("  • Balance factor of node = +2")
print()
print("Before:          After:")
print("      30            20")
print("     /             /  \\")
print("    20      →     10   30")
print("   /")
print("  10")
print()
print("Solution: Single right rotation at 30")
print()

print("2. RIGHT-RIGHT Case (Single Left Rotation)")
print("-" * 60)
print()
print("Occurs when:")
print("  • Insert into right subtree of right child")
print("  • Balance factor of node = -2")
print()
print("Before:          After:")
print("  10               20")
print("   \\              /  \\")
print("    20     →     10   30")
print("     \\")
print("      30")
print()
print("Solution: Single left rotation at 10")
print()

print("3. LEFT-RIGHT Case (Double Rotation)")
print("-" * 60)
print()
print("Occurs when:")
print("  • Insert into right subtree of left child")
print("  • Balance factor of node = +2")
print()
print("Before:          Step 1:         Step 2:")
print("    30             30              20")
print("   /              /               /  \\")
print("  10      →      20      →       10   30")
print("   \\            /")
print("    20         10")
print()
print("Solution: Left rotation at 10, then right rotation at 30")
print()

print("4. RIGHT-LEFT Case (Double Rotation)")
print("-" * 60)
print()
print("Occurs when:")
print("  • Insert into left subtree of right child")
print("  • Balance factor of node = -2")
print()
print("Before:          Step 1:         Step 2:")
print("  10               10              20")
print("   \\                \\            /  \\")
print("    30       →       20    →    10   30")
print("   /                  \\")
print("  20                   30")
print()
print("Solution: Right rotation at 30, then left rotation at 10")
print()


print("=" * 60)
print("AVL Tree Operations Demo")
print("=" * 60)
print()

avl = AVLTree()
values = [10, 20, 30, 40, 50, 25]

print("Inserting values: 10, 20, 30, 40, 50, 25")
print()

for val in values:
    avl.root = avl.insert(avl.root, val)
    print(f"After inserting {val}:")
    print(f"  Inorder: {avl.inorder(avl.root)}")
    print(f"  Height: {avl.get_height(avl.root)}")

print()
print("Final AVL tree structure:")
print("       30")
print("      /  \\")
print("    20    40")
print("   / \\     \\")
print("  10  25    50")
print()
print("All balance factors: {-1, 0, 1} ✓")
print()

print("Deleting 40...")
avl.root = avl.delete(avl.root, 40)
print(f"Inorder after delete: {avl.inorder(avl.root)}")
print()


# Detailed rotation example
print("=" * 60)
print("Step-by-Step Insertion Example")
print("=" * 60)
print()

avl2 = AVLTree()

print("Insert 10:")
avl2.root = avl2.insert(avl2.root, 10)
print("    10  (BF=0)")
print()

print("Insert 20:")
avl2.root = avl2.insert(avl2.root, 20)
print("    10  (BF=-1)")
print("     \\")
print("      20  (BF=0)")
print()

print("Insert 30:")
print("Before rotation:")
print("    10  (BF=-2) ← Unbalanced!")
print("     \\")
print("      20  (BF=-1)")
print("       \\")
print("        30  (BF=0)")
print()
avl2.root = avl2.insert(avl2.root, 30)
print("After left rotation at 10:")
print("       20  (BF=0)")
print("      /  \\")
print("    10    30")
print("  (BF=0) (BF=0)")
print()

print("Insert 40:")
avl2.root = avl2.insert(avl2.root, 40)
print("       20  (BF=-1)")
print("      /  \\")
print("    10    30  (BF=-1)")
print("           \\")
print("            40  (BF=0)")
print()

print("Insert 50:")
print("Before rotation:")
print("       20  (BF=-2) ← Unbalanced!")
print("      /  \\")
print("    10    30  (BF=-2)")
print("           \\")
print("            40  (BF=-1)")
print("             \\")
print("              50  (BF=0)")
print()
avl2.root = avl2.insert(avl2.root, 50)
print("After left rotation at 30:")
print("       20  (BF=-1)")
print("      /  \\")
print("    10    40  (BF=0)")
print("         /  \\")
print("       30    50")
print()

print("Insert 25:")
avl2.root = avl2.insert(avl2.root, 25)
print("       20  (BF=0)")
print("      /  \\")
print("    10    40  (BF=1)")
print("         /  \\")
print("       30    50")
print("      /")
print("    25")
print()


# Helper functions for visualization
def print_balance_factors(node, level=0):
    """Print tree with balance factors"""
    if node:
        print_balance_factors(node.right, level + 1)
        balance = avl.get_balance(node)
        print('    ' * level + f'{node.val} (BF={balance})')
        print_balance_factors(node.left, level + 1)


print("=" * 60)
print("Balance Factors")
print("=" * 60)
print()
print("Current tree with balance factors:")
print_balance_factors(avl2.root)
print()


# AVL vs Regular BST comparison
print("=" * 60)
print("AVL Tree vs Regular BST")
print("=" * 60)
print()
print("Worst Case Comparison (inserting sorted data):")
print()
print("Regular BST with [1,2,3,4,5]:")
print("  1")
print("   \\")
print("    2")
print("     \\")
print("      3")
print("       \\")
print("        4")
print("         \\")
print("          5")
print()
print("Height: 5 (degenerate - like linked list)")
print("Search time: O(n)")
print()

print("AVL Tree with [1,2,3,4,5]:")
print("       2")
print("      / \\")
print("     1   4")
print("        / \\")
print("       3   5")
print()
print("Height: 3 (balanced)")
print("Search time: O(log n)")
print()


# Performance comparison
print("=" * 60)
print("Performance Comparison")
print("=" * 60)
print()
print("Operation         AVL Tree      Regular BST (worst)")
print("-" * 60)
print("Search            O(log n)      O(n)")
print("Insert            O(log n)      O(n)")
print("Delete            O(log n)      O(n)")
print("Min/Max           O(log n)      O(n)")
print()
print("Space Overhead:")
print("  • AVL: Extra height field per node")
print("  • BST: No extra space")
print()
print("Rebalancing Cost:")
print("  • AVL: At most 2 rotations per insert")
print("  • AVL: At most O(log n) rotations per delete")
print("  • BST: No rebalancing needed")
print()


# When to use AVL
print("=" * 60)
print("When to Use AVL Trees")
print("=" * 60)
print()
print("✓ Use AVL when:")
print("  • Lookups are more frequent than updates")
print("  • Need guaranteed O(log n) operations")
print("  • Data arrives in sorted/nearly sorted order")
print("  • Worst-case performance is critical")
print()
print("✗ Don't use AVL when:")
print("  • Frequent insertions/deletions (consider Red-Black)")
print("  • Memory is very limited")
print("  • Simple operations on small datasets")
print("  • Order doesn't matter (use hash table)")
print()


# Real-world applications
print("=" * 60)
print("Real-World Applications")
print("=" * 60)
print()
print("1. Database Indexing:")
print("   • B-trees (generalization of AVL)")
print("   • Fast sorted access")
print("   • Range queries")
print()
print("2. In-Memory Databases:")
print("   • Redis sorted sets")
print("   • Priority queues")
print("   • Leaderboards")
print()
print("3. File Systems:")
print("   • File lookup by name")
print("   • Directory structures")
print("   • HFS+ (Apple's file system)")
print()
print("4. Networking:")
print("   • Router tables")
print("   • IP address lookup")
print("   • Traffic shaping")
print()
print("5. Graphics:")
print("   • Scene graphs")
print("   • Collision detection")
print("   • Z-buffer ordering")
print()


# Common pitfalls
print("=" * 60)
print("Common Pitfalls & Tips")
print("=" * 60)
print()
print("Pitfall 1: Forgetting to update heights")
print("  ✓ Always update heights after rotations")
print()
print("Pitfall 2: Wrong rotation direction")
print("  ✓ Left-heavy (BF > 1) → Right rotation")
print("  ✓ Right-heavy (BF < -1) → Left rotation")
print()
print("Pitfall 3: Not handling double rotations")
print("  ✓ Check child's balance factor")
print("  ✓ Left-Right and Right-Left need 2 rotations")
print()
print("Pitfall 4: Modifying during traversal")
print("  ✓ Collect nodes first, then modify")
print()
print("Tip: AVL trees are stricter than Red-Black trees")
print("  • AVL: More rotations, better search")
print("  • Red-Black: Fewer rotations, better insert/delete")
print()
