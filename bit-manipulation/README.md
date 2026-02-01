# Bit Manipulation

Bitwise operations and binary number manipulation techniques.

## Overview

Bit manipulation involves directly manipulating bits using bitwise operators. It's essential for optimization, low-level programming, and certain algorithmic problems.

## Contents

### 01_basics.py
- Binary representation
- Bitwise operators (AND, OR, XOR, NOT, shifts)
- Common bit operations (set, clear, toggle, check)
- Bit masks and flags
- Two's complement
- Counting bits

### 02_common_patterns.py
- XOR properties and tricks
- Bit manipulation patterns
- Power of 2 operations
- Single number variants
- Bit masking techniques
- Gray code
- Subset generation

### 03_leetcode_problems.py
- Single Number (LC 136)
- Number of 1 Bits (LC 191)
- Counting Bits (LC 338)
- Reverse Bits (LC 190)
- Missing Number (LC 268)
- Sum of Two Integers (LC 371)
- Hamming Distance (LC 461)
- Power of Two/Four (LC 231, 342)
- Bitwise AND of Range (LC 201)
- Maximum XOR (LC 421)

## Key Concepts

### Bitwise Operators
- `&` (AND): Both bits must be 1
- `|` (OR): At least one bit is 1
- `^` (XOR): Bits are different
- `~` (NOT): Flip all bits
- `<<` (Left shift): Multiply by 2^n
- `>>` (Right shift): Divide by 2^n

### Time Complexity
- Most bit operations: O(1)
- Counting bits in n: O(log n) or O(number of bits)
- Operating on k bits: O(k)

### Space Complexity
- Typically O(1) - in-place operations

## Common Patterns

1. **XOR Tricks**: Find unique elements, swap without temp
2. **Bit Masks**: Set/clear/toggle specific bits
3. **Power of 2**: Check with `n & (n-1) == 0`
4. **Counting Bits**: Brian Kernighan's algorithm
5. **Rightmost Set Bit**: `n & -n`
6. **Clear Rightmost Bit**: `n & (n-1)`

## XOR Properties

- `a ^ 0 = a` (identity)
- `a ^ a = 0` (self-inverse)
- `a ^ b = b ^ a` (commutative)
- `(a ^ b) ^ c = a ^ (b ^ c)` (associative)

## Common Bit Tricks

```python
# Check if bit is set
def is_bit_set(n, i):
    return (n & (1 << i)) != 0

# Set bit to 1
def set_bit(n, i):
    return n | (1 << i)

# Clear bit to 0
def clear_bit(n, i):
    return n & ~(1 << i)

# Toggle bit
def toggle_bit(n, i):
    return n ^ (1 << i)

# Get rightmost set bit
def rightmost_set_bit(n):
    return n & -n

# Clear rightmost set bit
def clear_rightmost_bit(n):
    return n & (n - 1)

# Check if power of 2
def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

# Count set bits
def count_bits(n):
    count = 0
    while n:
        n &= n - 1  # Clear rightmost bit
        count += 1
    return count
```

## Real-World Applications

- **Flags and Permissions**: Unix file permissions (rwx)
- **Network Masks**: IP address subnetting
- **Graphics**: Color manipulation (RGB values)
- **Compression**: Data encoding/decoding
- **Cryptography**: XOR encryption
- **Embedded Systems**: Hardware register manipulation
- **Game Development**: State flags, collision detection

## Interview Tips

- Always consider the number of bits (32-bit vs 64-bit)
- Watch for signed vs unsigned integers
- XOR is powerful for finding unique elements
- Power of 2 operations are very common
- Bit manipulation often provides O(1) space solutions
- Practice visualizing binary representations
- Remember: `x & 1` checks if number is odd

## Performance Benefits

- Faster than arithmetic operations (CPU-level)
- No need for extra data structures
- Constant space complexity
- Can replace certain mathematical operations
