"""
Custom Hash Table Implementations
==================================

Different collision handling strategies and hash table variations.
"""

# Implementation 1: Separate Chaining (Linked Lists)
print("=" * 60)
print("Implementation 1: Separate Chaining")
print("=" * 60)
print("""
How it works:
  1. Array of buckets, each bucket is a linked list
  2. Hash function maps key to bucket index
  3. Collisions: multiple keys hash to same bucket → store in list
  4. Put: hash key → append to bucket's list
  5. Get: hash key → search through bucket's list
  6. Load factor = n/m (items/buckets), rehash if > threshold

Pros: Simple, handles high load factors well
Cons: Extra memory for pointers, cache unfriendly
Time: O(1 + α) where α is load factor
""")

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTableChaining:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity
    
    def _hash(self, key):
        """Simple hash function"""
        return hash(key) % self.capacity
    
    def put(self, key, value):
        index = self._hash(key)
        node = self.buckets[index]
        
        # Search for existing key
        while node:
            if node.key == key:
                node.value = value  # Update
                return
            node = node.next
        
        # Insert new key at head
        new_node = Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1
        
        # Rehash if load factor > 0.75
        if self.size / self.capacity > 0.75:
            self._rehash()
    
    def get(self, key):
        index = self._hash(key)
        node = self.buckets[index]
        
        while node:
            if node.key == key:
                return node.value
            node = node.next
        
        return None
    
    def remove(self, key):
        index = self._hash(key)
        node = self.buckets[index]
        prev = None
        
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next
        
        return False
    
    def _rehash(self):
        """Double capacity and rehash all keys"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        for node in old_buckets:
            while node:
                self.put(node.key, node.value)
                node = node.next
    
    def display(self):
        for i, node in enumerate(self.buckets):
            if node:
                print(f"Bucket {i}: ", end="")
                current = node
                while current:
                    print(f"({current.key}: {current.value}) -> ", end="")
                    current = current.next
                print("None")

print("\nExample:")
ht_chain = HashTableChaining(capacity=5)
ht_chain.put("apple", 100)
ht_chain.put("banana", 200)
ht_chain.put("cherry", 300)
ht_chain.put("date", 400)
ht_chain.put("elderberry", 500)  # May cause collision
print(f"get('apple'): {ht_chain.get('apple')}")
print(f"get('banana'): {ht_chain.get('banana')}")
ht_chain.display()

# Implementation 2: Linear Probing (Open Addressing)
print("\n" + "=" * 60)
print("Implementation 2: Linear Probing")
print("=" * 60)
print("""
How it works:
  1. All elements stored directly in array (no extra lists)
  2. Hash function gives initial index
  3. Collision: probe next slots linearly (index+1, index+2, ...)
  4. Put: find first empty slot or matching key
  5. Get: probe until found, empty, or wrapped around
  6. Remove: mark as deleted (tombstone) to maintain probe sequence
  7. Clustering problem: collisions create long probe chains

Pros: Cache friendly, less memory overhead
Cons: Primary clustering, degrades with high load factor
Time: O(1/(1-α)) where α is load factor
""")

class HashTableLinearProbing:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.DELETED = object()  # Tombstone marker
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def put(self, key, value):
        if self.size / self.capacity > 0.7:
            self._rehash()
        
        index = self._hash(key)
        probes = 0
        
        while probes < self.capacity:
            # Empty or deleted slot
            if self.keys[index] is None or self.keys[index] is self.DELETED:
                self.keys[index] = key
                self.values[index] = value
                self.size += 1
                return
            
            # Update existing key
            if self.keys[index] == key:
                self.values[index] = value
                return
            
            # Linear probe
            index = (index + 1) % self.capacity
            probes += 1
        
        raise Exception("Hash table is full")
    
    def get(self, key):
        index = self._hash(key)
        probes = 0
        
        while probes < self.capacity:
            # Empty slot means key not found
            if self.keys[index] is None:
                return None
            
            # Found key
            if self.keys[index] != self.DELETED and self.keys[index] == key:
                return self.values[index]
            
            # Continue probing
            index = (index + 1) % self.capacity
            probes += 1
        
        return None
    
    def remove(self, key):
        index = self._hash(key)
        probes = 0
        
        while probes < self.capacity:
            if self.keys[index] is None:
                return False
            
            if self.keys[index] != self.DELETED and self.keys[index] == key:
                self.keys[index] = self.DELETED
                self.values[index] = None
                self.size -= 1
                return True
            
            index = (index + 1) % self.capacity
            probes += 1
        
        return False
    
    def _rehash(self):
        old_keys = self.keys
        old_values = self.values
        
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        
        for i in range(len(old_keys)):
            if old_keys[i] is not None and old_keys[i] is not self.DELETED:
                self.put(old_keys[i], old_values[i])
    
    def display(self):
        print("Index | Key        | Value")
        print("-" * 35)
        for i in range(self.capacity):
            key_str = str(self.keys[i]) if self.keys[i] is not None else "None"
            if self.keys[i] is self.DELETED:
                key_str = "DELETED"
            val_str = str(self.values[i]) if self.values[i] is not None else "None"
            print(f"{i:5} | {key_str:10} | {val_str}")

print("\nExample:")
ht_linear = HashTableLinearProbing(capacity=7)
ht_linear.put("a", 1)
ht_linear.put("b", 2)
ht_linear.put("c", 3)
ht_linear.put("h", 8)  # May collide with 'a' depending on hash
ht_linear.put("o", 15)  # May collide
print(f"get('a'): {ht_linear.get('a')}")
print(f"get('h'): {ht_linear.get('h')}")
ht_linear.remove('b')
ht_linear.display()

# Implementation 3: Quadratic Probing
print("\n" + "=" * 60)
print("Implementation 3: Quadratic Probing")
print("=" * 60)
print("""
How it works:
  1. Similar to linear probing but better distribution
  2. Collision: probe using quadratic sequence
  3. Next index = (hash + i²) % capacity for i = 1, 2, 3, ...
  4. Reduces primary clustering compared to linear probing
  5. Still uses tombstones for deletion
  6. May not find empty slot even if one exists (secondary clustering)

Pros: Less primary clustering than linear probing
Cons: Secondary clustering, harder to guarantee finding slots
Time: O(1/(1-α)) but better cache performance than chaining
""")

class HashTableQuadraticProbing:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.DELETED = object()
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def put(self, key, value):
        if self.size / self.capacity > 0.7:
            self._rehash()
        
        index = self._hash(key)
        i = 0
        
        while i < self.capacity:
            probe_index = (index + i * i) % self.capacity
            
            # Empty or deleted slot
            if self.keys[probe_index] is None or self.keys[probe_index] is self.DELETED:
                self.keys[probe_index] = key
                self.values[probe_index] = value
                self.size += 1
                return
            
            # Update existing key
            if self.keys[probe_index] == key:
                self.values[probe_index] = value
                return
            
            i += 1
        
        raise Exception("Hash table is full")
    
    def get(self, key):
        index = self._hash(key)
        i = 0
        
        while i < self.capacity:
            probe_index = (index + i * i) % self.capacity
            
            if self.keys[probe_index] is None:
                return None
            
            if self.keys[probe_index] != self.DELETED and self.keys[probe_index] == key:
                return self.values[probe_index]
            
            i += 1
        
        return None
    
    def remove(self, key):
        index = self._hash(key)
        i = 0
        
        while i < self.capacity:
            probe_index = (index + i * i) % self.capacity
            
            if self.keys[probe_index] is None:
                return False
            
            if self.keys[probe_index] != self.DELETED and self.keys[probe_index] == key:
                self.keys[probe_index] = self.DELETED
                self.values[probe_index] = None
                self.size -= 1
                return True
            
            i += 1
        
        return False
    
    def _rehash(self):
        old_keys = self.keys
        old_values = self.values
        
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        
        for i in range(len(old_keys)):
            if old_keys[i] is not None and old_keys[i] is not self.DELETED:
                self.put(old_keys[i], old_values[i])
    
    def display(self):
        print("Index | Key        | Value")
        print("-" * 35)
        for i in range(self.capacity):
            key_str = str(self.keys[i]) if self.keys[i] is not None else "None"
            if self.keys[i] is self.DELETED:
                key_str = "DELETED"
            val_str = str(self.values[i]) if self.values[i] is not None else "None"
            print(f"{i:5} | {key_str:10} | {val_str}")

print("\nExample:")
ht_quad = HashTableQuadraticProbing(capacity=11)
ht_quad.put("x", 10)
ht_quad.put("y", 20)
ht_quad.put("z", 30)
print(f"get('x'): {ht_quad.get('x')}")
print(f"get('y'): {ht_quad.get('y')}")
ht_quad.display()

# Implementation 4: Double Hashing
print("\n" + "=" * 60)
print("Implementation 4: Double Hashing")
print("=" * 60)
print("""
How it works:
  1. Uses TWO hash functions for better distribution
  2. First hash: determines initial index
  3. Second hash: determines probe step size
  4. Next index = (hash1 + i * hash2) % capacity
  5. Step size varies per key, reduces clustering
  6. hash2 must never be 0 (infinite loop)
  7. Best open addressing method for avoiding clustering

Pros: Minimal clustering, uniform distribution
Cons: Two hash computations, still needs low load factor
Time: O(1/(1-α)) with best distribution
""")

class HashTableDoubleHashing:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.DELETED = object()
    
    def _hash1(self, key):
        return hash(key) % self.capacity
    
    def _hash2(self, key):
        # Second hash must never be 0, use prime number
        return 7 - (hash(key) % 7)
    
    def put(self, key, value):
        if self.size / self.capacity > 0.7:
            self._rehash()
        
        index = self._hash1(key)
        step = self._hash2(key)
        i = 0
        
        while i < self.capacity:
            probe_index = (index + i * step) % self.capacity
            
            # Empty or deleted slot
            if self.keys[probe_index] is None or self.keys[probe_index] is self.DELETED:
                self.keys[probe_index] = key
                self.values[probe_index] = value
                self.size += 1
                return
            
            # Update existing key
            if self.keys[probe_index] == key:
                self.values[probe_index] = value
                return
            
            i += 1
        
        raise Exception("Hash table is full")
    
    def get(self, key):
        index = self._hash1(key)
        step = self._hash2(key)
        i = 0
        
        while i < self.capacity:
            probe_index = (index + i * step) % self.capacity
            
            if self.keys[probe_index] is None:
                return None
            
            if self.keys[probe_index] != self.DELETED and self.keys[probe_index] == key:
                return self.values[probe_index]
            
            i += 1
        
        return None
    
    def remove(self, key):
        index = self._hash1(key)
        step = self._hash2(key)
        i = 0
        
        while i < self.capacity:
            probe_index = (index + i * step) % self.capacity
            
            if self.keys[probe_index] is None:
                return False
            
            if self.keys[probe_index] != self.DELETED and self.keys[probe_index] == key:
                self.keys[probe_index] = self.DELETED
                self.values[probe_index] = None
                self.size -= 1
                return True
            
            i += 1
        
        return False
    
    def _rehash(self):
        old_keys = self.keys
        old_values = self.values
        
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        
        for i in range(len(old_keys)):
            if old_keys[i] is not None and old_keys[i] is not self.DELETED:
                self.put(old_keys[i], old_values[i])
    
    def display(self):
        print("Index | Key        | Value")
        print("-" * 35)
        for i in range(self.capacity):
            key_str = str(self.keys[i]) if self.keys[i] is not None else "None"
            if self.keys[i] is self.DELETED:
                key_str = "DELETED"
            val_str = str(self.values[i]) if self.values[i] is not None else "None"
            print(f"{i:5} | {key_str:10} | {val_str}")

print("\nExample:")
ht_double = HashTableDoubleHashing(capacity=13)
ht_double.put("m", 100)
ht_double.put("n", 200)
ht_double.put("p", 300)
print(f"get('m'): {ht_double.get('m')}")
print(f"get('p'): {ht_double.get('p')}")
ht_double.display()

# Collision Handling Comparison
print("\n" + "=" * 60)
print("Collision Handling Strategies Comparison")
print("=" * 60)
print("""
1. Separate Chaining (Linked Lists):
   - Collision: Add to linked list in same bucket
   - Pros: Simple, handles high load factors
   - Cons: Extra memory for pointers
   - Best for: Unknown/high load factors
   - Time: O(1 + α) where α = n/m

2. Linear Probing:
   - Collision: Try next slot (i+1, i+2, ...)
   - Pros: Cache friendly, simple
   - Cons: Primary clustering
   - Best for: Low load factors, cache performance
   - Time: O(1/(1-α))

3. Quadratic Probing:
   - Collision: Try slots at i², 2², 3² ...
   - Pros: Reduces primary clustering
   - Cons: Secondary clustering, may not find slots
   - Best for: Medium load factors
   - Time: O(1/(1-α))

4. Double Hashing:
   - Collision: Use second hash for step size
   - Pros: Best distribution, minimal clustering
   - Cons: Two hash computations
   - Best for: Need uniform distribution
   - Time: O(1/(1-α))

Load Factor Impact:
  α < 0.5: All methods work well
  α = 0.7: Open addressing starts degrading
  α > 0.8: Chaining preferred
  α > 0.9: Significant performance loss

Rehashing Triggers:
  - Chaining: α > 0.75 typically
  - Open Addressing: α > 0.5-0.7 typically
  - Cost: O(n) to rehash all elements
""")

# Performance Demonstration
print("\n" + "=" * 60)
print("Performance with Collisions")
print("=" * 60)

import time

def benchmark(hash_table, operations):
    start = time.time()
    for op, key, value in operations:
        if op == "put":
            hash_table.put(key, value)
        elif op == "get":
            hash_table.get(key)
    return time.time() - start

# Create operations that cause collisions
ops = []
for i in range(100):
    ops.append(("put", f"key{i}", i))
for i in range(100):
    ops.append(("get", f"key{i}", None))

ht_chain = HashTableChaining(capacity=20)
ht_linear = HashTableLinearProbing(capacity=20)
ht_quad = HashTableQuadraticProbing(capacity=20)
ht_double = HashTableDoubleHashing(capacity=20)

time_chain = benchmark(ht_chain, ops)
time_linear = benchmark(ht_linear, ops)
time_quad = benchmark(ht_quad, ops)
time_double = benchmark(ht_double, ops)

print(f"Chaining:        {time_chain:.6f} seconds")
print(f"Linear Probing:  {time_linear:.6f} seconds")
print(f"Quadratic:       {time_quad:.6f} seconds")
print(f"Double Hashing:  {time_double:.6f} seconds")
print("\nNote: Performance varies by load factor and collision patterns")
