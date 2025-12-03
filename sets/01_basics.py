"""
Sets - Basics
=============
Understanding sets and their operations in Python.
"""

print("=" * 60)
print("What is a Set?")
print("=" * 60)
print("A set is an unordered collection of unique elements.")
print()
print("Key Properties:")
print("  - No duplicates: automatically removes duplicate values")
print("  - Unordered: elements have no index or position")
print("  - Mutable: can add/remove elements (but elements must be immutable)")
print("  - Fast lookup: O(1) average time to check membership")
print("  - Based on hash tables internally")
print()
print("Use Sets When:")
print("  - Need to track unique items")
print("  - Need fast membership testing (x in set)")
print("  - Need set operations (union, intersection, difference)")
print("  - Order doesn't matter")
print()


# Creating Sets
print("=" * 60)
print("Creating Sets")
print("=" * 60)

# 1. Using curly braces
print("\n1. Using curly braces:")
fruits = {'apple', 'banana', 'orange'}
print(f"   fruits = {fruits}")

# 2. Using set() constructor
print("\n2. Using set() constructor:")
numbers = set([1, 2, 3, 4, 5])
print(f"   numbers = {numbers}")

# 3. Creating from string (each character becomes element)
print("\n3. From string:")
letters = set('hello')
print(f"   set('hello') = {letters}")
print(f"   Note: Only unique letters, unordered")

# 4. Empty set (must use set(), not {})
print("\n4. Empty set:")
empty = set()
print(f"   empty = {empty}")
print(f"   Note: {{}} creates empty dict, not set!")

# 5. Automatic duplicate removal
print("\n5. Automatic duplicate removal:")
duplicates = {1, 2, 2, 3, 3, 3, 4}
print(f"   {{1, 2, 2, 3, 3, 3, 4}} = {duplicates}")

print()


# Basic Operations
print("=" * 60)
print("Basic Set Operations")
print("=" * 60)

# Adding elements
print("\n1. Adding elements:")
my_set = {1, 2, 3}
print(f"   Initial: {my_set}")
my_set.add(4)
print(f"   After add(4): {my_set}")
my_set.add(2)  # No effect, already exists
print(f"   After add(2): {my_set} (no duplicate)")

# Removing elements
print("\n2. Removing elements:")
my_set = {1, 2, 3, 4, 5}
print(f"   Initial: {my_set}")

# remove() - raises error if not found
my_set.remove(3)
print(f"   After remove(3): {my_set}")

# discard() - doesn't raise error if not found
my_set.discard(10)  # No error even though 10 not in set
print(f"   After discard(10): {my_set} (no error)")

# pop() - removes and returns arbitrary element
popped = my_set.pop()
print(f"   After pop(): removed {popped}, set = {my_set}")

# clear() - removes all elements
my_set.clear()
print(f"   After clear(): {my_set}")

# Membership testing
print("\n3. Membership testing (O(1) average):")
fruits = {'apple', 'banana', 'orange'}
print(f"   fruits = {fruits}")
print(f"   'apple' in fruits: {('apple' in fruits)}")
print(f"   'grape' in fruits: {('grape' in fruits)}")
print(f"   'grape' not in fruits: {('grape' not in fruits)}")

# Set size
print("\n4. Set size:")
print(f"   len(fruits): {len(fruits)}")

# Iterating over set
print("\n5. Iterating (order not guaranteed):")
print("   for fruit in fruits:")
for fruit in fruits:
    print(f"     {fruit}")

print()


# Set Mathematical Operations
print("=" * 60)
print("Set Mathematical Operations")
print("=" * 60)

set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

print(f"\nset_a = {set_a}")
print(f"set_b = {set_b}")

# 1. Union (all elements from both sets)
print("\n1. Union (|) - elements in A or B or both:")
union1 = set_a | set_b
union2 = set_a.union(set_b)
print(f"   set_a | set_b = {union1}")
print(f"   set_a.union(set_b) = {union2}")

# 2. Intersection (elements in both sets)
print("\n2. Intersection (&) - elements in both A and B:")
intersection1 = set_a & set_b
intersection2 = set_a.intersection(set_b)
print(f"   set_a & set_b = {intersection1}")
print(f"   set_a.intersection(set_b) = {intersection2}")

# 3. Difference (elements in first but not second)
print("\n3. Difference (-) - elements in A but not in B:")
difference1 = set_a - set_b
difference2 = set_a.difference(set_b)
print(f"   set_a - set_b = {difference1}")
print(f"   set_a.difference(set_b) = {difference2}")
print(f"   set_b - set_a = {set_b - set_a} (note: different result)")

# 4. Symmetric Difference (elements in either but not both)
print("\n4. Symmetric Difference (^) - in A or B but not both:")
sym_diff1 = set_a ^ set_b
sym_diff2 = set_a.symmetric_difference(set_b)
print(f"   set_a ^ set_b = {sym_diff1}")
print(f"   set_a.symmetric_difference(set_b) = {sym_diff2}")

print()


# Set Relationships
print("=" * 60)
print("Set Relationships")
print("=" * 60)

a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
c = {6, 7, 8}
d = {1, 2, 3}

print(f"\na = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")

# 1. Subset (all elements of A are in B)
print("\n1. Subset (<=) - is A contained in B?:")
print(f"   a.issubset(b): {a.issubset(b)} (a ⊆ b)")
print(f"   a <= b: {a <= b}")
print(f"   b.issubset(a): {b.issubset(a)} (b ⊄ a)")

# 2. Proper subset (subset but not equal)
print("\n2. Proper Subset (<) - A ⊂ B and A ≠ B:")
print(f"   a < b: {a < b} (a is proper subset of b)")
print(f"   a < d: {a < d} (a equals d, not proper subset)")

# 3. Superset (all elements of B are in A)
print("\n3. Superset (>=) - does A contain B?:")
print(f"   b.issuperset(a): {b.issuperset(a)} (b ⊇ a)")
print(f"   b >= a: {b >= a}")

# 4. Proper superset
print("\n4. Proper Superset (>) - A ⊃ B and A ≠ B:")
print(f"   b > a: {b > a}")
print(f"   a > d: {a > d}")

# 5. Disjoint (no common elements)
print("\n5. Disjoint - no elements in common:")
print(f"   a.isdisjoint(c): {a.isdisjoint(c)} (no overlap)")
print(f"   a.isdisjoint(b): {a.isdisjoint(b)} (have overlap)")

print()


# Modifying Sets In-Place
print("=" * 60)
print("Modifying Sets In-Place")
print("=" * 60)

print("\nThese methods modify the original set:")

# 1. update() - add multiple elements
print("\n1. update() - add elements from another iterable:")
s = {1, 2, 3}
print(f"   s = {s}")
s.update([4, 5, 6])
print(f"   s.update([4, 5, 6]): {s}")
s.update({7, 8}, [9, 10])
print(f"   s.update({{7, 8}}, [9, 10]): {s}")

# 2. intersection_update() - keep only common elements
print("\n2. intersection_update() - keep only intersection:")
s = {1, 2, 3, 4, 5}
print(f"   s = {s}")
s.intersection_update({3, 4, 5, 6, 7})
print(f"   s.intersection_update({{3, 4, 5, 6, 7}}): {s}")

# 3. difference_update() - remove elements found in other
print("\n3. difference_update() - remove elements in other:")
s = {1, 2, 3, 4, 5}
print(f"   s = {s}")
s.difference_update({3, 4, 5})
print(f"   s.difference_update({{3, 4, 5}}): {s}")

# 4. symmetric_difference_update()
print("\n4. symmetric_difference_update() - keep only unique:")
s = {1, 2, 3, 4}
print(f"   s = {s}")
s.symmetric_difference_update({3, 4, 5, 6})
print(f"   s.symmetric_difference_update({{3, 4, 5, 6}}): {s}")

print()


# Frozen Sets (Immutable)
print("=" * 60)
print("Frozen Sets (Immutable)")
print("=" * 60)

print("\nfrozenset is immutable version of set:")
print("  - Can't add/remove elements after creation")
print("  - Can be used as dictionary keys (regular sets can't)")
print("  - Can be elements of another set")
print("  - Hashable, so can be used anywhere immutable objects needed")
print("  - All read-only set operations work (union, intersection, etc.)")

# Creating frozen set
print("\n1. Creating frozensets:")
fs = frozenset([1, 2, 3, 4, 5])
print(f"   fs = frozenset([1, 2, 3, 4, 5])")
print(f"   fs = {fs}")

fs_empty = frozenset()
print(f"   Empty: frozenset() = {fs_empty}")

fs_from_string = frozenset('hello')
print(f"   From string: frozenset('hello') = {fs_from_string}")

# Can perform operations but can't modify
print("\n2. Read-only operations work:")
fs2 = frozenset([4, 5, 6, 7])
print(f"   fs = {fs}")
print(f"   fs2 = {fs2}")
print(f"   fs | fs2 = {fs | fs2} (union)")
print(f"   fs & fs2 = {fs & fs2} (intersection)")
print(f"   fs - fs2 = {fs - fs2} (difference)")
print(f"   fs ^ fs2 = {fs ^ fs2} (symmetric difference)")

# Can't modify
print("\n3. Can't modify frozensets:")
try:
    fs.add(6)
except AttributeError as e:
    print(f"   fs.add(6) → Error: 'frozenset' object has no attribute 'add'")

try:
    fs.remove(1)
except AttributeError as e:
    print(f"   fs.remove(1) → Error: 'frozenset' object has no attribute 'remove'")

print()


# Frozenset Real-World Applications
print("=" * 60)
print("Frozenset Real-World Applications")
print("=" * 60)

# Application 1: Representing immutable groups/relationships
print("\n1. Representing Undirected Edges in Graphs:")
print("   Problem: Edge (A,B) same as (B,A), need unique representation")
print()

# Graph edges as frozensets (undirected)
edges = {
    frozenset(['A', 'B']),
    frozenset(['B', 'C']),
    frozenset(['A', 'C']),
    frozenset(['B', 'A'])  # This is duplicate of ('A', 'B')
}
print(f"   edges = {{('A','B'), ('B','C'), ('A','C'), ('B','A')}}")
print(f"   Result: {edges}")
print(f"   Note: Only 3 edges (B,A) merged with (A,B)")

# Check if edge exists (order doesn't matter)
edge_to_check = frozenset(['C', 'A'])
print(f"\n   Check if edge (C,A) exists: {edge_to_check in edges}")
print(f"   Check if edge (A,C) exists: {frozenset(['A', 'C']) in edges}")
print(f"   Both return True - order doesn't matter!")

# Application 2: Dictionary keys for complex lookups
print("\n2. Caching Results for Sets of Items:")
print("   Problem: Cache results based on combination of items")
print()

# Example: Restaurant order pricing (order doesn't matter)
menu_cache = {
    frozenset(['burger', 'fries']): 12.99,
    frozenset(['burger', 'fries', 'drink']): 14.99,
    frozenset(['pizza', 'drink']): 15.99,
    frozenset(['salad', 'drink']): 10.99
}

print("   menu_cache = {")
for items, price in menu_cache.items():
    print(f"      {set(items)}: ${price}")
print("   }")

# Look up price (order doesn't matter)
order1 = frozenset(['fries', 'burger'])  # Different order
order2 = frozenset(['burger', 'fries'])
print(f"\n   Order ['fries', 'burger']: ${menu_cache.get(order1, 'Not found')}")
print(f"   Order ['burger', 'fries']: ${menu_cache.get(order2, 'Not found')}")
print(f"   Both orders find same price!")

# Application 3: Grouping by characteristics
print("\n3. Grouping Students by Skills:")
print("   Problem: Group students who have same set of skills")
print()

students_by_skills = {}
students = [
    ("Alice", frozenset(['Python', 'Java', 'C++'])),
    ("Bob", frozenset(['Python', 'JavaScript'])),
    ("Charlie", frozenset(['Java', 'Python', 'C++'])),  # Same as Alice
    ("David", frozenset(['Python', 'JavaScript']))  # Same as Bob
]

for name, skills in students:
    if skills not in students_by_skills:
        students_by_skills[skills] = []
    students_by_skills[skills].append(name)

print("   Students grouped by skill set:")
for skills, names in students_by_skills.items():
    print(f"      {set(skills)}: {names}")

# Application 4: Set of sets (tracking combinations)
print("\n4. Tracking Completed Task Combinations:")
print("   Problem: Track which combinations of tasks completed together")
print()

completed_combinations = set()

# Teams complete different task combinations
team_completions = [
    frozenset(['task_a', 'task_b']),
    frozenset(['task_a', 'task_c']),
    frozenset(['task_b', 'task_a']),  # Duplicate
    frozenset(['task_b', 'task_c', 'task_d'])
]

for combo in team_completions:
    completed_combinations.add(combo)

print(f"   Unique combinations completed:")
for combo in completed_combinations:
    print(f"      {set(combo)}")

# Check if specific combination was completed
check_combo = frozenset(['task_a', 'task_b'])
print(f"\n   Was ['task_a', 'task_b'] completed? {check_combo in completed_combinations}")

# Application 5: Permissions and access control
print("\n5. User Permission Sets:")
print("   Problem: Define and check user permissions")
print()

# Define permission sets for different roles
permissions = {
    'admin': frozenset(['read', 'write', 'delete', 'admin']),
    'editor': frozenset(['read', 'write']),
    'viewer': frozenset(['read'])
}

user_roles = {
    'alice': 'admin',
    'bob': 'editor',
    'charlie': 'viewer'
}

print("   Permission sets:")
for role, perms in permissions.items():
    print(f"      {role}: {set(perms)}")

# Check if user can perform action
def can_perform(user, action):
    role = user_roles.get(user)
    if not role:
        return False
    return action in permissions[role]

print(f"\n   Can alice delete? {can_perform('alice', 'delete')}")
print(f"   Can bob delete? {can_perform('bob', 'delete')}")
print(f"   Can charlie read? {can_perform('charlie', 'read')}")

# Find users with specific permission set
def find_users_with_permissions(required_perms):
    """Find users who have at least the required permissions"""
    users = []
    required = frozenset(required_perms)
    
    for user, role in user_roles.items():
        if required.issubset(permissions[role]):
            users.append(user)
    
    return users

print(f"\n   Users who can read and write: {find_users_with_permissions(['read', 'write'])}")
print(f"   Users who can only read: {find_users_with_permissions(['read'])}")

# Application 6: Memoization with set parameters
print("\n6. Memoization with Set Parameters:")
print("   Problem: Cache function results when input is a set")
print()

def subset_sum_memo(numbers, target):
    """
    Check if any subset sums to target (with memoization).
    Use frozenset as cache key.
    """
    cache = {}
    
    def helper(remaining_nums, current_target):
        # Convert to frozenset for cache key
        key = (frozenset(remaining_nums), current_target)
        
        if key in cache:
            return cache[key]
        
        if current_target == 0:
            return True
        if current_target < 0 or not remaining_nums:
            return False
        
        # Try including or excluding first number
        num = remaining_nums[0]
        rest = remaining_nums[1:]
        
        result = (helper(rest, current_target - num) or 
                 helper(rest, current_target))
        
        cache[key] = result
        return result
    
    return helper(list(numbers), target)

numbers = [3, 7, 1, 8, 2]
target = 10
print(f"   Numbers: {numbers}")
print(f"   Target: {target}")
print(f"   Can make target? {subset_sum_memo(numbers, target)}")
print(f"   (Example: 3+7=10 or 8+2=10)")

print()


# When to Use Frozenset vs Set
print("=" * 60)
print("When to Use Frozenset vs Regular Set")
print("=" * 60)

print("\nUse FROZENSET when:")
print("  ✓ Need to use as dictionary key")
print("  ✓ Need to store in another set (set of sets)")
print("  ✓ Want to ensure data can't be modified")
print("  ✓ Need hashable collection of unique items")
print("  ✓ Representing constant/immutable groups (permissions, edges)")
print()
print("Use REGULAR SET when:")
print("  ✓ Need to add/remove elements dynamically")
print("  ✓ Don't need to use as dict key or in another set")
print("  ✓ Building up a collection incrementally")
print("  ✓ Tracking changing state")
print()
print("Performance:")
print("  - Both have O(1) lookup")
print("  - Frozenset may be slightly faster (fewer operations available)")
print("  - Frozenset computed hash once and cached")

print()


# Common Patterns
print("=" * 60)
print("Common Set Patterns")
print("=" * 60)

# 1. Remove duplicates from list
print("\n1. Remove duplicates from list:")
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 5]
print(f"   Original: {numbers}")
unique = list(set(numbers))
print(f"   Unique: {unique}")
print(f"   Note: Order not preserved!")

# Preserve order while removing duplicates
def remove_duplicates_preserve_order(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

unique_ordered = remove_duplicates_preserve_order(numbers)
print(f"   Unique (ordered): {unique_ordered}")

# 2. Find common elements between lists
print("\n2. Find common elements:")
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
common = set(list1) & set(list2)
print(f"   list1: {list1}")
print(f"   list2: {list2}")
print(f"   common: {common}")

# 3. Find elements in one list but not another
print("\n3. Find elements only in first list:")
only_in_list1 = set(list1) - set(list2)
print(f"   In list1 but not list2: {only_in_list1}")

# 4. Check if two lists have any common elements
print("\n4. Check for any common elements:")
list_a = [1, 2, 3]
list_b = [4, 5, 6]
list_c = [3, 4, 5]
print(f"   list_a & list_b overlap: {bool(set(list_a) & set(list_b))}")
print(f"   list_a & list_c overlap: {bool(set(list_a) & set(list_c))}")

# 5. Count unique elements
print("\n5. Count unique elements:")
text = "hello world"
unique_chars = set(text)
print(f"   Text: '{text}'")
print(f"   Unique characters: {unique_chars}")
print(f"   Count: {len(unique_chars)}")

print()


# Set Comprehension
print("=" * 60)
print("Set Comprehension")
print("=" * 60)

print("\nSimilar to list comprehension, but creates a set:")

# 1. Basic comprehension
print("\n1. Basic set comprehension:")
squares = {x**2 for x in range(10)}
print(f"   {{x**2 for x in range(10)}} = {squares}")

# 2. With condition
print("\n2. With condition:")
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(f"   {{x**2 for x in range(10) if x % 2 == 0}} = {even_squares}")

# 3. From string
print("\n3. Unique vowels in string:")
text = "hello world"
vowels = {char for char in text if char in 'aeiou'}
print(f"   Text: '{text}'")
print(f"   Vowels: {vowels}")

# 4. Multiple variables
print("\n4. With multiple variables:")
pairs = {(x, y) for x in range(3) for y in range(3) if x != y}
print(f"   {{(x, y) for x in range(3) for y in range(3) if x != y}}:")
print(f"   {pairs}")

print()


# Performance Comparison
print("=" * 60)
print("Set vs List Performance")
print("=" * 60)

print("\nMembership testing (x in collection):")
print("  List: O(n) - must check each element")
print("  Set:  O(1) - hash table lookup")
print()
print("When to use Set:")
print("  ✓ Frequent membership testing")
print("  ✓ Need unique elements")
print("  ✓ Mathematical set operations")
print("  ✓ Order doesn't matter")
print()
print("When to use List:")
print("  ✓ Need to maintain order")
print("  ✓ Need duplicates")
print("  ✓ Need indexing (list[0])")
print("  ✓ Elements aren't hashable")

print()
