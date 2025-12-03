"""
Segment Trees & Fenwick Trees (Binary Indexed Tree)
===================================================
Understanding range query data structures.
"""


print("=" * 60)
print("What is a Segment Tree?")
print("=" * 60)
print()
print("A Segment Tree is a tree for range queries on arrays.")
print()
print("Key Properties:")
print("  • Each node represents a range [L, R]")
print("  • Leaf nodes represent single elements")
print("  • Internal nodes represent merged results")
print("  • Height = O(log n)")
print()
print("Why Segment Trees?")
print("  • Fast range queries: O(log n)")
print("  • Fast point updates: O(log n)")
print("  • Works for any associative operation")
print("  • Examples: sum, min, max, GCD")
print()
print("Example: Range Sum Query")
print("Array: [1, 3, 5, 7, 9, 11]")
print()
print("Segment Tree:")
print("                36 [0-5]")
print("               /         \\")
print("          9 [0-2]       27 [3-5]")
print("         /      \\       /      \\")
print("      4 [0-1]  5[2]  16[3-4]  11[5]")
print("      /    \\          /    \\")
print("    1[0]  3[1]      7[3]  9[4]")
print()
print("Each node stores sum of its range")
print()


class SegmentTree:
    """Segment Tree for range sum queries"""
    
    def __init__(self, arr):
        """
        Build segment tree from array.
        
        How it works:
        1. Tree stored in array (like heap)
        2. Node i has children at 2i+1 and 2i+2
        3. Build bottom-up or top-down
        
        Time: O(n), Space: O(4n) ≈ O(n)
        """
        self.n = len(arr)
        # Tree size: 4n is always enough
        self.tree = [0] * (4 * self.n)
        if arr:
            self._build(arr, 0, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        """Build tree recursively"""
        if start == end:
            # Leaf node
            self.tree[node] = arr[start]
            return
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        # Build left and right subtrees
        self._build(arr, left_child, start, mid)
        self._build(arr, right_child, mid + 1, end)
        
        # Merge results (sum for this example)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def range_sum(self, L, R):
        """
        Query sum in range [L, R].
        
        How it works:
        1. If range fully covers node, return node value
        2. If range partially overlaps, recurse on children
        3. Combine results
        
        Time: O(log n)
        """
        return self._range_sum_helper(0, 0, self.n - 1, L, R)
    
    def _range_sum_helper(self, node, start, end, L, R):
        # No overlap
        if R < start or L > end:
            return 0
        
        # Complete overlap
        if L <= start and end <= R:
            return self.tree[node]
        
        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_sum = self._range_sum_helper(left_child, start, mid, L, R)
        right_sum = self._range_sum_helper(right_child, mid + 1, end, L, R)
        
        return left_sum + right_sum
    
    def update(self, index, value):
        """
        Update element at index.
        
        How it works:
        1. Navigate to leaf node
        2. Update leaf
        3. Propagate changes upward
        
        Time: O(log n)
        """
        self._update_helper(0, 0, self.n - 1, index, value)
    
    def _update_helper(self, node, start, end, index, value):
        if start == end:
            # Leaf node
            self.tree[node] = value
            return
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        if index <= mid:
            self._update_helper(left_child, start, mid, index, value)
        else:
            self._update_helper(right_child, mid + 1, end, index, value)
        
        # Update current node
        self.tree[node] = self.tree[left_child] + self.tree[right_child]


print("=" * 60)
print("Segment Tree Demo")
print("=" * 60)
print()

arr = [1, 3, 5, 7, 9, 11]
seg_tree = SegmentTree(arr)

print(f"Array: {arr}")
print()

print("Range queries:")
print(f"  Sum[0, 2] = {seg_tree.range_sum(0, 2)}")
print(f"  Sum[1, 4] = {seg_tree.range_sum(1, 4)}")
print(f"  Sum[0, 5] = {seg_tree.range_sum(0, 5)}")

print()
print("Update arr[1] = 10")
seg_tree.update(1, 10)

print()
print("Range queries after update:")
print(f"  Sum[0, 2] = {seg_tree.range_sum(0, 2)}")
print(f"  Sum[1, 4] = {seg_tree.range_sum(1, 4)}")

print()


# Lazy Propagation
print("=" * 60)
print("Segment Tree with Lazy Propagation")
print("=" * 60)
print()
print("Problem: Range updates are slow O(n log n)")
print()
print("Solution: Lazy Propagation")
print("  • Defer updates until needed")
print("  • Store pending updates in lazy array")
print("  • Apply updates only when node is visited")
print()
print("Example: Add 5 to range [1, 3]")
print()
print("Step 1: Mark nodes covering [1,3] with +5")
print("Step 2: Don't update children yet (lazy)")
print("Step 3: When querying, apply pending updates")
print()
print("Time Complexity:")
print("  • Range update: O(log n)  [was O(n log n)]")
print("  • Range query:  O(log n)")
print()


class LazySegmentTree:
    """Segment Tree with lazy propagation"""
    
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)  # Pending updates
        if arr:
            self._build(arr, 0, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        
        mid = (start + end) // 2
        self._build(arr, 2 * node + 1, start, mid)
        self._build(arr, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def _push_down(self, node, start, end):
        """Apply pending updates to children"""
        if self.lazy[node] != 0:
            # Apply to current node
            self.tree[node] += (end - start + 1) * self.lazy[node]
            
            # Push to children if not leaf
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            
            # Clear lazy value
            self.lazy[node] = 0
    
    def range_update(self, L, R, delta):
        """Add delta to all elements in [L, R]"""
        self._range_update_helper(0, 0, self.n - 1, L, R, delta)
    
    def _range_update_helper(self, node, start, end, L, R, delta):
        # Apply pending updates
        self._push_down(node, start, end)
        
        # No overlap
        if R < start or L > end:
            return
        
        # Complete overlap
        if L <= start and end <= R:
            self.lazy[node] += delta
            self._push_down(node, start, end)
            return
        
        # Partial overlap
        mid = (start + end) // 2
        self._range_update_helper(2 * node + 1, start, mid, L, R, delta)
        self._range_update_helper(2 * node + 2, mid + 1, end, L, R, delta)
        
        # Update current node
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def range_sum(self, L, R):
        """Query sum in range [L, R]"""
        return self._range_sum_helper(0, 0, self.n - 1, L, R)
    
    def _range_sum_helper(self, node, start, end, L, R):
        self._push_down(node, start, end)
        
        if R < start or L > end:
            return 0
        
        if L <= start and end <= R:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._range_sum_helper(2 * node + 1, start, mid, L, R)
        right_sum = self._range_sum_helper(2 * node + 2, mid + 1, end, L, R)
        
        return left_sum + right_sum


print("Lazy Segment Tree Demo")
print("-" * 60)

arr2 = [1, 2, 3, 4, 5]
lazy_tree = LazySegmentTree(arr2)

print(f"Array: {arr2}")
print()

print("Add 10 to range [1, 3]...")
lazy_tree.range_update(1, 3, 10)

print(f"  Sum[1, 3] = {lazy_tree.range_sum(1, 3)}")
print(f"  Sum[0, 4] = {lazy_tree.range_sum(0, 4)}")

print()


# Fenwick Tree (Binary Indexed Tree)
print("=" * 60)
print("Fenwick Tree (Binary Indexed Tree)")
print("=" * 60)
print()
print("A Fenwick Tree is a space-efficient alternative to Segment Tree.")
print("Also called: Binary Indexed Tree (BIT)")
print()
print("Key Properties:")
print("  • Uses array of same size as input")
print("  • Each index stores partial sum")
print("  • Uses bit manipulation for navigation")
print()
print("Why Fenwick Tree?")
print("  • Simpler than segment tree")
print("  • Less space: O(n) vs O(4n)")
print("  • Easier to code")
print("  • Same time complexity: O(log n)")
print()
print("Limitation:")
print("  • Only works for invertible operations")
print("  • Sum, XOR work (can subtract)")
print("  • Min, Max don't work (can't invert)")
print()
print("How indexing works:")
print("  Index 1 (0001): stores A[1]")
print("  Index 2 (0010): stores sum A[1..2]")
print("  Index 3 (0011): stores A[3]")
print("  Index 4 (0100): stores sum A[1..4]")
print("  ...")
print()
print("Pattern: Index i stores sum of last (i & -i) elements")
print()


class FenwickTree:
    """Fenwick Tree (Binary Indexed Tree) for range sum"""
    
    def __init__(self, n):
        """
        Initialize Fenwick tree.
        
        How it works:
        • 1-indexed array (index 0 unused)
        • tree[i] stores partial sum
        
        Time: O(n), Space: O(n)
        """
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed
    
    def update(self, index, delta):
        """
        Add delta to element at index.
        
        How it works:
        1. Start at index
        2. Add delta to current position
        3. Move to next responsible index
        4. Repeat until out of range
        
        Next index = index + (index & -index)
        (Add last set bit)
        
        Time: O(log n)
        """
        index += 1  # Convert to 1-indexed
        
        while index <= self.n:
            self.tree[index] += delta
            index += index & (-index)  # Add last set bit
    
    def prefix_sum(self, index):
        """
        Sum of elements [0, index].
        
        How it works:
        1. Start at index
        2. Add value at current position
        3. Move to previous responsible index
        4. Repeat until 0
        
        Previous index = index - (index & -index)
        (Remove last set bit)
        
        Time: O(log n)
        """
        index += 1  # Convert to 1-indexed
        total = 0
        
        while index > 0:
            total += self.tree[index]
            index -= index & (-index)  # Remove last set bit
        
        return total
    
    def range_sum(self, left, right):
        """
        Sum of elements [left, right].
        
        Time: O(log n)
        """
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


print("Fenwick Tree Demo")
print("-" * 60)
print()

arr3 = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
fenwick = FenwickTree(len(arr3))

# Build tree
for i, val in enumerate(arr3):
    fenwick.update(i, val)

print(f"Array: {arr3}")
print()

print("Range sum queries:")
print(f"  Sum[0, 4] = {fenwick.range_sum(0, 4)}")
print(f"  Sum[2, 7] = {fenwick.range_sum(2, 7)}")
print(f"  Sum[0, 10] = {fenwick.range_sum(0, 10)}")

print()
print("Update: Add 5 to index 3")
fenwick.update(3, 5)

print(f"  Sum[2, 7] = {fenwick.range_sum(2, 7)}")

print()


# Bit manipulation explanation
print("=" * 60)
print("Understanding i & -i (Last Set Bit)")
print("=" * 60)
print()
print("This gives the least significant bit that is 1.")
print()
print("Examples:")
print("  6 (0110) & -6 (1010) = 0010 = 2")
print("  12 (1100) & -12 (0100) = 0100 = 4")
print("  10 (1010) & -10 (0110) = 0010 = 2")
print()
print("Why it works:")
print("  -i in two's complement = ~i + 1")
print("  i & (~i + 1) isolates rightmost 1 bit")
print()
print("Usage in Fenwick Tree:")
print("  • Update: index += index & -index")
print("  • Query:  index -= index & -index")
print()


# Comparison table
print("=" * 60)
print("Segment Tree vs Fenwick Tree")
print("=" * 60)
print()
print("                Segment Tree    Fenwick Tree")
print("-" * 60)
print("Space           O(4n)           O(n)")
print("Build           O(n)            O(n log n)")
print("Point update    O(log n)        O(log n)")
print("Range query     O(log n)        O(log n)")
print("Range update    O(log n)*       Not efficient")
print("Operations      Any             Invertible only")
print("Implementation  Complex         Simple")
print()
print("* With lazy propagation")
print()
print("Use Segment Tree when:")
print("  • Need range updates")
print("  • Non-invertible operation (min, max)")
print("  • Need more complex queries")
print()
print("Use Fenwick Tree when:")
print("  • Only point updates")
print("  • Invertible operation (sum, XOR)")
print("  • Want simpler code")
print("  • Tight space constraint")
print()


# Real-world applications
print("=" * 60)
print("Real-World Applications")
print("=" * 60)
print()
print("1. Stock Trading:")
print("   • Track price ranges")
print("   • Find min/max in time window")
print("   • Calculate moving averages")
print()
print("2. Gaming:")
print("   • Leaderboard ranking")
print("   • Score range queries")
print("   • Dynamic difficulty adjustment")
print()
print("3. Analytics:")
print("   • Time series analysis")
print("   • Event counting in ranges")
print("   • Real-time statistics")
print()
print("4. Computational Geometry:")
print("   • Rectangle area queries")
print("   • Point in range counting")
print("   • Interval scheduling")
print()
print("5. Database Systems:")
print("   • Range sum queries")
print("   • OLAP operations")
print("   • Aggregate functions")
print()


# Common patterns
print("=" * 60)
print("Common Patterns")
print("=" * 60)
print()
print("Pattern 1: Range Sum Query")
print("  • Use Fenwick Tree or Segment Tree")
print("  • Point update + range query")
print()
print("Pattern 2: Range Minimum/Maximum")
print("  • Use Segment Tree (not Fenwick)")
print("  • Can't invert min/max operation")
print()
print("Pattern 3: Range Updates")
print("  • Use Segment Tree with lazy propagation")
print("  • Efficient bulk modifications")
print()
print("Pattern 4: 2D Range Queries")
print("  • Build 2D Fenwick Tree")
print("  • Or use nested Segment Trees")
print()
print("Pattern 5: Inversion Count")
print("  • Count inversions in array")
print("  • Use Fenwick Tree while iterating")
print()


# Time complexity summary
print("=" * 60)
print("Time Complexity Summary")
print("=" * 60)
print()
print("Naive approach (no tree):")
print("  • Range query: O(n)")
print("  • Point update: O(1)")
print()
print("Prefix sum array:")
print("  • Range query: O(1)")
print("  • Point update: O(n)  [rebuild needed]")
print()
print("Segment Tree:")
print("  • Build:        O(n)")
print("  • Range query:  O(log n)")
print("  • Point update: O(log n)")
print("  • Range update: O(log n)  [with lazy]")
print()
print("Fenwick Tree:")
print("  • Build:        O(n log n)  [n updates]")
print("  • Range query:  O(log n)")
print("  • Point update: O(log n)")
print()
print("Space:")
print("  • Segment Tree: O(4n) ≈ O(n)")
print("  • Fenwick Tree: O(n)")
print()
