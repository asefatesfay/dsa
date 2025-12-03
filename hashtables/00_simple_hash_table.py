"""
Simple Hash Table Implementation
=================================

Basic hash table with simple hash function and collision handling using lists.
This demonstrates the core concept before moving to more complex implementations.
"""

class SimpleHashTable:
    """
    Simple hash table with chaining for collision handling.
    
    How it works:
      1. Array of buckets (each bucket is a list)
      2. Hash function: convert key to index using modulo
      3. Collision: if multiple keys hash to same index, store in same bucket list
      4. Each bucket stores list of [key, value] pairs
    """
    
    def __init__(self, size=10):
        """Initialize hash table with given size"""
        self.size = size
        self.buckets = [[] for _ in range(size)]  # List of empty lists
        self.count = 0  # Track number of items
    
    def _hash(self, key):
        """
        Simple hash function - converts key to index
        
        How it works:
          1. Use Python's built-in hash() function to get hash code
          2. Take modulo with table size to get valid index (0 to size-1)
          3. hash() works with strings, numbers, tuples, etc.
        
        Examples:
          hash("apple") % 10 might give 3
          hash("banana") % 10 might give 7
          hash("cherry") % 10 might give 3 (collision with apple!)
        """
        return hash(key) % self.size
    
    def put(self, key, value):
        """
        Insert or update key-value pair
        
        How it works:
          1. Hash the key to get bucket index
          2. Look through bucket list for existing key
          3. If found: update value
          4. If not found: append [key, value] to bucket
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check if key already exists (update case)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = [key, value]  # Update existing
                print(f"Updated: '{key}' = {value} at bucket {index}")
                return
        
        # Key doesn't exist, add new entry
        bucket.append([key, value])
        self.count += 1
        print(f"Inserted: '{key}' = {value} at bucket {index}")
        
        # Show collision if bucket has multiple items
        if len(bucket) > 1:
            print(f"  → Collision! Bucket {index} now has {len(bucket)} items")
    
    def get(self, key):
        """
        Retrieve value for given key
        
        How it works:
          1. Hash the key to get bucket index
          2. Search through bucket list for matching key
          3. Return value if found, None if not found
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None  # Key not found
    
    def remove(self, key):
        """
        Remove key-value pair
        
        How it works:
          1. Hash the key to get bucket index
          2. Search through bucket list
          3. Remove [key, value] pair if found
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                print(f"Removed: '{key}' from bucket {index}")
                return True
        
        print(f"Key '{key}' not found")
        return False
    
    def display(self):
        """Show contents of all buckets"""
        print("\n" + "=" * 60)
        print("Hash Table Contents")
        print("=" * 60)
        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"Bucket {i}: {bucket}")
            else:
                print(f"Bucket {i}: (empty)")
        print(f"\nTotal items: {self.count}")
        print(f"Load factor: {self.count / self.size:.2f}")
    
    def __str__(self):
        """String representation"""
        items = []
        for bucket in self.buckets:
            for key, value in bucket:
                items.append(f"'{key}': {value}")
        return "{" + ", ".join(items) + "}"


# Demonstration
print("=" * 60)
print("Simple Hash Table Demo")
print("=" * 60)
print("\nCreating hash table with size=10\n")

ht = SimpleHashTable(size=10)

# Basic operations
print("\n--- Inserting Items ---")
ht.put("apple", 100)
ht.put("banana", 200)
ht.put("cherry", 300)
ht.put("date", 400)
ht.put("elderberry", 500)

# Display contents
ht.display()

# Retrieve values
print("\n--- Getting Values ---")
print(f"get('apple'): {ht.get('apple')}")
print(f"get('banana'): {ht.get('banana')}")
print(f"get('grape'): {ht.get('grape')}")  # Not found

# Update existing key
print("\n--- Updating Values ---")
ht.put("apple", 150)  # Update

# Remove a key
print("\n--- Removing Items ---")
ht.remove("banana")
ht.remove("grape")  # Doesn't exist

# Display final state
ht.display()

# Demonstrate collisions
print("\n" + "=" * 60)
print("Demonstrating Collisions")
print("=" * 60)
print("\nCreating small hash table (size=5) to force collisions\n")

small_ht = SimpleHashTable(size=5)

# These keys will likely collide
print("--- Inserting Items ---")
small_ht.put("a", 1)
small_ht.put("b", 2)
small_ht.put("c", 3)
small_ht.put("d", 4)
small_ht.put("e", 5)
small_ht.put("f", 6)
small_ht.put("g", 7)
small_ht.put("h", 8)

small_ht.display()

# Understanding Python's hash() function
print("\n" + "=" * 60)
print("Understanding Python's hash() Function")
print("=" * 60)
print("""
Python's built-in hash() function:
  - Converts objects to integer hash codes
  - Same object always gives same hash (during program run)
  - Different objects usually give different hashes
  - Works with: strings, numbers, tuples (immutable types)
  - Doesn't work with: lists, dicts, sets (mutable types)
""")

print("\nExamples of hash() function:")
keys = ["apple", "banana", "cherry", "date", "elderberry"]
for key in keys:
    hash_value = hash(key)
    index = hash_value % 10
    print(f"hash('{key}') = {hash_value:20d} → index {index}")

print("\n" + "=" * 60)
print("How Collisions Are Handled")
print("=" * 60)
print("""
When two keys hash to same index:
  1. Both stored in same bucket (list)
  2. Bucket becomes: [[key1, value1], [key2, value2]]
  3. Lookup requires searching through bucket list
  4. Average time still O(1) if collisions are rare
  5. Worst case O(n) if all keys hash to same bucket

Example:
  Bucket 3: [['apple', 100], ['cherry', 300]]
  Both 'apple' and 'cherry' hashed to index 3
  
When getting 'apple':
  1. Hash 'apple' → index 3
  2. Check bucket 3
  3. Search through list: is first item 'apple'? Yes!
  4. Return 100
""")

# Performance with collisions
print("\n" + "=" * 60)
print("Load Factor and Performance")
print("=" * 60)
print("""
Load Factor (α) = number_of_items / table_size

  α = 0.5 (50% full): Very fast, few collisions
  α = 0.75 (75% full): Still good performance
  α = 1.0 (100% full): Every bucket has item, more collisions
  α > 1.0 (>100% full): Multiple items per bucket, slower

Our examples:
""")

print(f"\nLarge table: {ht.count} items / {ht.size} buckets = α = {ht.count/ht.size:.2f}")
print(f"Small table: {small_ht.count} items / {small_ht.size} buckets = α = {small_ht.count/small_ht.size:.2f}")
print("\nSmall table has higher load factor → more collisions")

# Custom hash function example
print("\n" + "=" * 60)
print("Custom Hash Function Example")
print("=" * 60)
print("""
Simple custom hash for strings (educational purpose):
  1. Sum ASCII values of all characters
  2. Multiply by position for better distribution
  3. Take modulo with table size
""")

def custom_hash(key, size):
    """Custom hash function for strings"""
    hash_value = 0
    for i, char in enumerate(key):
        hash_value += ord(char) * (i + 1)
    return hash_value % size

print("\nCustom hash examples:")
for key in ["apple", "banana", "cherry"]:
    custom_index = custom_hash(key, 10)
    builtin_index = hash(key) % 10
    print(f"'{key}':")
    print(f"  Custom hash: {custom_index}")
    print(f"  Built-in hash: {builtin_index}")

print("\n" + "=" * 60)
print("Key Takeaways")
print("=" * 60)
print("""
1. Hash function converts key → integer → index
2. Python's hash() is reliable and fast
3. Collisions handled by storing multiple items in same bucket
4. Each bucket is a list of [key, value] pairs
5. Lower load factor = fewer collisions = faster operations
6. This simple approach works well for most use cases!

Time Complexity:
  - Average: O(1) for put, get, remove
  - Worst: O(n) if all keys collide (rare with good hash function)

Space Complexity: O(n) where n is number of items
""")
