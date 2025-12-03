"""
Red-Black Trees (Self-Balancing BST)
====================================
Understanding Red-Black trees and their properties.
"""


class RBNode:
    """Red-Black Tree Node"""
    def __init__(self, val, color="RED"):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.color = color  # "RED" or "BLACK"


print("=" * 60)
print("What is a Red-Black Tree?")
print("=" * 60)
print()
print("A Red-Black tree is a self-balancing BST with colored nodes.")
print()
print("Five Properties (invariants):")
print("  1. Every node is either RED or BLACK")
print("  2. Root is always BLACK")
print("  3. All leaves (NULL nodes) are BLACK")
print("  4. If a node is RED, both children are BLACK")
print("     (No two RED nodes in a row)")
print("  5. All paths from node to leaves have same number of BLACK nodes")
print("     (Black-height property)")
print()
print("Why Red-Black Trees?")
print("  • Looser balancing than AVL → fewer rotations")
print("  • Still guarantees O(log n) operations")
print("  • Better for frequent insertions/deletions")
print("  • Height at most 2 * log(n + 1)")
print("  • Used in Linux kernel, Java TreeMap, C++ std::map")
print()
print("Example Red-Black Tree:")
print("         11(B)")
print("        /     \\")
print("      2(R)    14(B)")
print("     /  \\       \\")
print("   1(B) 7(B)    15(R)")
print("        / \\")
print("      5(R) 8(R)")
print()
print("Key difference from AVL:")
print("  • AVL: Strict balance (height diff ≤ 1)")
print("  • RB:  Loose balance (longest path ≤ 2 × shortest)")
print()


class RedBlackTree:
    """Red-Black Tree implementation"""
    
    def __init__(self):
        self.NIL = RBNode(None, "BLACK")  # Sentinel node
        self.root = self.NIL
    
    def rotate_left(self, x):
        """
        Left rotation around x.
        
        Before:      After:
           x            y
            \\          /
             y   →    x
            /          \\
           T2           T2
        """
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def rotate_right(self, y):
        """
        Right rotation around y.
        
        Before:      After:
           y            x
          /              \\
         x        →       y
          \\              /
           T2           T2
        """
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        
        x.right = y
        y.parent = x
    
    def insert(self, val):
        """
        Insert value and fix violations.
        
        How it works:
        1. Normal BST insert (new node is RED)
        2. Fix Red-Black properties if violated
        3. Recolor and rotate as needed
        
        Time: O(log n)
        """
        # Create new RED node
        node = RBNode(val, "RED")
        node.left = self.NIL
        node.right = self.NIL
        
        # BST insert
        parent = None
        current = self.root
        
        while current != self.NIL:
            parent = current
            if node.val < current.val:
                current = current.left
            else:
                current = current.right
        
        node.parent = parent
        
        if parent is None:
            self.root = node
        elif node.val < parent.val:
            parent.left = node
        else:
            parent.right = node
        
        # Fix violations
        self._fix_insert(node)
    
    def _fix_insert(self, node):
        """
        Fix Red-Black tree violations after insert.
        
        Cases to handle:
        1. Parent is BLACK → No violation
        2. Uncle is RED → Recolor
        3. Uncle is BLACK, node is right child → Left rotation
        4. Uncle is BLACK, node is left child → Right rotation + recolor
        """
        while node.parent and node.parent.color == "RED":
            # Parent is left child of grandparent
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                # Case 1: Uncle is RED → Recolor
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    # Case 2: Node is right child → Left rotation
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    
                    # Case 3: Node is left child → Right rotation + recolor
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.rotate_right(node.parent.parent)
            else:
                # Mirror cases (parent is right child)
                uncle = node.parent.parent.left
                
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.rotate_left(node.parent.parent)
        
        # Root must be BLACK
        self.root.color = "BLACK"
    
    def inorder(self, node=None, result=None):
        """Inorder traversal"""
        if node is None:
            node = self.root
        if result is None:
            result = []
        
        if node != self.NIL:
            self.inorder(node.left, result)
            result.append((node.val, node.color[0]))  # Value and color
            self.inorder(node.right, result)
        
        return result


print("=" * 60)
print("Insert Operation Cases")
print("=" * 60)
print()

print("Case 1: Uncle is RED (Recoloring)")
print("-" * 60)
print()
print("Before:")
print("         G(B)")
print("        /    \\")
print("      P(R)   U(R)  ← Uncle is RED")
print("     /")
print("   N(R)  ← New node")
print()
print("Action: Recolor P, U, and G")
print()
print("After:")
print("         G(R)")
print("        /    \\")
print("      P(B)   U(B)")
print("     /")
print("   N(R)")
print()

print("Case 2: Uncle is BLACK, Node is Right Child")
print("-" * 60)
print()
print("Before:")
print("         G(B)")
print("        /    \\")
print("      P(R)   U(B)  ← Uncle is BLACK")
print("       \\")
print("        N(R)  ← Right child")
print()
print("Action: Left rotate at P")
print()
print("After:")
print("         G(B)")
print("        /    \\")
print("      N(R)   U(B)")
print("     /")
print("   P(R)")
print()
print("Then apply Case 3...")
print()

print("Case 3: Uncle is BLACK, Node is Left Child")
print("-" * 60)
print()
print("Before:")
print("         G(B)")
print("        /    \\")
print("      P(R)   U(B)  ← Uncle is BLACK")
print("     /")
print("   N(R)  ← Left child")
print()
print("Action: Right rotate at G, recolor")
print()
print("After:")
print("         P(B)")
print("        /    \\")
print("      N(R)   G(R)")
print("              \\")
print("              U(B)")
print()


print("=" * 60)
print("Red-Black Tree Demo")
print("=" * 60)
print()

rb_tree = RedBlackTree()
values = [7, 3, 18, 10, 22, 8, 11, 26]

print(f"Inserting values: {values}")
print()

for val in values:
    rb_tree.insert(val)
    print(f"After inserting {val}:")
    print(f"  Tree (inorder): {rb_tree.inorder()}")

print()
print("Final Red-Black tree maintains all 5 properties!")
print()


# Red-Black vs AVL comparison
print("=" * 60)
print("Red-Black vs AVL Trees")
print("=" * 60)
print()
print("Balancing:")
print("  AVL:       Strictly balanced (height diff ≤ 1)")
print("  Red-Black: Loosely balanced (longest ≤ 2 × shortest)")
print()
print("Rotations:")
print("  AVL:       More rotations (up to O(log n) per delete)")
print("  Red-Black: Fewer rotations (at most 3 per insert, 3 per delete)")
print()
print("Search Performance:")
print("  AVL:       Slightly faster (shorter tree)")
print("  Red-Black: Slightly slower (taller tree)")
print()
print("Insert/Delete Performance:")
print("  AVL:       Slower (more rotations)")
print("  Red-Black: Faster (fewer rotations)")
print()
print("Memory:")
print("  AVL:       1 int per node (height)")
print("  Red-Black: 1 bit per node (color)")
print()
print("Use Cases:")
print("  AVL:       Read-heavy workloads")
print("  Red-Black: Write-heavy workloads")
print()


# Time complexity comparison
print("=" * 60)
print("Time Complexity Comparison")
print("=" * 60)
print()
print("Operation     AVL Tree    Red-Black    BST (worst)")
print("-" * 60)
print("Search        O(log n)    O(log n)     O(n)")
print("Insert        O(log n)    O(log n)     O(n)")
print("Delete        O(log n)    O(log n)     O(n)")
print("Min/Max       O(log n)    O(log n)     O(n)")
print()
print("Height:")
print("  AVL:       1.44 × log(n)")
print("  Red-Black: 2.00 × log(n)")
print("  BST worst: n")
print()


# Real-world usage
print("=" * 60)
print("Real-World Usage")
print("=" * 60)
print()
print("Red-Black Trees are used in:")
print()
print("1. Linux Kernel:")
print("   • Process scheduling (Completely Fair Scheduler)")
print("   • Memory management")
print("   • File system operations")
print()
print("2. Java:")
print("   • TreeMap")
print("   • TreeSet")
print("   • Collections.sort() (TimSort with RB tree)")
print()
print("3. C++ STL:")
print("   • std::map")
print("   • std::multimap")
print("   • std::set")
print("   • std::multiset")
print()
print("4. Database Systems:")
print("   • MySQL InnoDB (B-tree variant)")
print("   • PostgreSQL (B-tree indexes)")
print()
print("5. Network Routers:")
print("   • Routing table lookups")
print("   • Packet scheduling")
print()


# Properties validation
print("=" * 60)
print("Validating Red-Black Properties")
print("=" * 60)
print()


def validate_rb_properties(tree):
    """Check if tree satisfies all RB properties"""
    
    def is_red(node):
        return node != tree.NIL and node.color == "RED"
    
    def is_black(node):
        return node == tree.NIL or node.color == "BLACK"
    
    # Property 1: Every node is RED or BLACK (enforced by design)
    
    # Property 2: Root is BLACK
    if tree.root != tree.NIL and tree.root.color != "BLACK":
        return False, "Root is not BLACK"
    
    # Property 4: No two consecutive RED nodes
    def check_no_red_red(node):
        if node == tree.NIL:
            return True
        if is_red(node):
            if is_red(node.left) or is_red(node.right):
                return False
        return check_no_red_red(node.left) and check_no_red_red(node.right)
    
    if not check_no_red_red(tree.root):
        return False, "Two consecutive RED nodes found"
    
    # Property 5: Same BLACK height on all paths
    def check_black_height(node):
        if node == tree.NIL:
            return 1  # NIL nodes are BLACK
        
        left_height = check_black_height(node.left)
        right_height = check_black_height(node.right)
        
        if left_height == -1 or right_height == -1:
            return -1
        
        if left_height != right_height:
            return -1
        
        return left_height + (1 if is_black(node) else 0)
    
    if check_black_height(tree.root) == -1:
        return False, "BLACK heights are not equal"
    
    return True, "All properties satisfied!"


valid, message = validate_rb_properties(rb_tree)
print(f"Validation result: {message}")
print()


# When to use each tree type
print("=" * 60)
print("Decision Guide: Which Tree to Use?")
print("=" * 60)
print()
print("Use Regular BST when:")
print("  • Data is randomly distributed")
print("  • Simple implementation needed")
print("  • Small datasets")
print()
print("Use AVL Tree when:")
print("  • Search-heavy workload (90%+ reads)")
print("  • Need best search performance")
print("  • Memory for height storage available")
print("  • Predictable performance critical")
print()
print("Use Red-Black Tree when:")
print("  • Balanced read/write workload")
print("  • Frequent insertions/deletions")
print("  • Memory is tight (1 bit vs int)")
print("  • Industry-standard solution needed")
print()
print("Use B-Tree when:")
print("  • Working with disk storage")
print("  • Database indexing")
print("  • Large datasets")
print("  • Minimizing disk I/O")
print()


# Common interview questions
print("=" * 60)
print("Common Interview Questions")
print("=" * 60)
print()
print("Q1: Why not just use AVL trees for everything?")
print("A:  Red-Black trees have fewer rotations, making them")
print("    faster for insert/delete heavy workloads. The slight")
print("    increase in height is usually worth the trade-off.")
print()
print("Q2: Why is the root always BLACK?")
print("A:  To maintain the BLACK-height property. If root were")
print("    RED, we'd need to track different BLACK heights.")
print()
print("Q3: Why are new nodes inserted as RED?")
print("A:  Inserting RED doesn't change BLACK height, minimizing")
print("    violations. Only fixes color conflicts locally.")
print()
print("Q4: How many rotations are needed for insert?")
print("A:  At most 2 rotations (one double rotation case).")
print()
print("Q5: How many colors do we need?")
print("A:  Just 2 colors (RED/BLACK) are sufficient to maintain")
print("    balance. More colors don't provide benefits.")
print()


# Performance characteristics
print("=" * 60)
print("Performance Characteristics")
print("=" * 60)
print()
print("Asymptotic Guarantees (n nodes):")
print()
print("Height:")
print("  • Maximum: 2 × log₂(n + 1)")
print("  • Minimum: log₂(n + 1)")
print()
print("Operations (worst case):")
print("  • Search:  O(log n)")
print("  • Insert:  O(log n) - at most 2 rotations")
print("  • Delete:  O(log n) - at most 3 rotations")
print("  • Min/Max: O(log n)")
print()
print("Space:")
print("  • O(n) for n nodes")
print("  • 1 bit color + 3 pointers per node")
print()
