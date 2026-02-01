"""
Bit Manipulation - Basics
=========================
Fundamental bitwise operations and binary number concepts.
"""

print("=" * 60)
print("Binary Representation")
print("=" * 60)
print()

# Converting between decimal and binary
num = 42
print(f"Decimal: {num}")
print(f"Binary: {bin(num)}")  # 0b prefix
print(f"Binary (no prefix): {bin(num)[2:]}")
print(f"Binary (8 bits): {format(num, '08b')}")
print()

# Converting binary to decimal
binary_str = "101010"
decimal = int(binary_str, 2)
print(f"Binary '{binary_str}' = Decimal {decimal}")
print()


print("=" * 60)
print("Bitwise Operators")
print("=" * 60)
print()

a = 12  # 1100 in binary
b = 10  # 1010 in binary

print(f"a = {a:4d} = {format(a, '08b')}")
print(f"b = {b:4d} = {format(b, '08b')}")
print()

# AND - both bits must be 1
result = a & b
print(f"AND:  a & b  = {result:4d} = {format(result, '08b')}")

# OR - at least one bit is 1
result = a | b
print(f"OR:   a | b  = {result:4d} = {format(result, '08b')}")

# XOR - bits are different
result = a ^ b
print(f"XOR:  a ^ b  = {result:4d} = {format(result, '08b')}")

# NOT - flip all bits (in Python, uses two's complement)
result = ~a
print(f"NOT:  ~a     = {result:4d} = {bin(result)}")

# Left shift - multiply by 2^n
result = a << 2
print(f"LEFT: a << 2 = {result:4d} = {format(result, '08b')} (multiply by 4)")

# Right shift - divide by 2^n
result = a >> 2
print(f"RIGHT: a >> 2 = {result:4d} = {format(result, '08b')} (divide by 4)")
print()


print("=" * 60)
print("Common Bit Operations")
print("=" * 60)
print()

def is_bit_set(n, i):
    """Check if i-th bit is set (1)."""
    return (n & (1 << i)) != 0

def set_bit(n, i):
    """Set i-th bit to 1."""
    return n | (1 << i)

def clear_bit(n, i):
    """Clear i-th bit to 0."""
    return n & ~(1 << i)

def toggle_bit(n, i):
    """Toggle i-th bit (0->1, 1->0)."""
    return n ^ (1 << i)

def update_bit(n, i, value):
    """Update i-th bit to given value (0 or 1)."""
    mask = ~(1 << i)
    return (n & mask) | (value << i)

n = 10  # 1010
print(f"Number: {n} = {format(n, '08b')}")
print()

# Check bit
print("Check bits:")
for i in range(4):
    print(f"  Bit {i}: {is_bit_set(n, i)}")
print()

# Set bit
n_set = set_bit(n, 0)
print(f"Set bit 0: {n} -> {n_set} = {format(n_set, '08b')}")

# Clear bit
n_clear = clear_bit(n, 1)
print(f"Clear bit 1: {n} -> {n_clear} = {format(n_clear, '08b')}")

# Toggle bit
n_toggle = toggle_bit(n, 2)
print(f"Toggle bit 2: {n} -> {n_toggle} = {format(n_toggle, '08b')}")

# Update bit
n_update = update_bit(n, 0, 1)
print(f"Update bit 0 to 1: {n} -> {n_update} = {format(n_update, '08b')}")
print()


print("=" * 60)
print("Counting Bits")
print("=" * 60)
print()

def count_bits_naive(n):
    """Count set bits - naive approach."""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def count_bits_kernighan(n):
    """Count set bits - Brian Kernighan's algorithm."""
    count = 0
    while n:
        n &= n - 1  # Clear rightmost set bit
        count += 1
    return count

def count_bits_builtin(n):
    """Count set bits using built-in."""
    return bin(n).count('1')

numbers = [0, 1, 7, 15, 255]
print("Count Set Bits:")
for n in numbers:
    print(f"  {n:3d} = {format(n, '08b')} -> {count_bits_kernighan(n)} bits")
print()


print("=" * 60)
print("Special Operations")
print("=" * 60)
print()

def get_rightmost_set_bit(n):
    """Get position of rightmost set bit."""
    return n & -n

def clear_rightmost_set_bit(n):
    """Clear the rightmost set bit."""
    return n & (n - 1)

def is_power_of_2(n):
    """Check if number is power of 2."""
    return n > 0 and (n & (n - 1)) == 0

def isolate_rightmost_zero(n):
    """Isolate rightmost zero bit."""
    return ~n & (n + 1)

n = 12  # 1100
print(f"Number: {n} = {format(n, '08b')}")
print()

rightmost = get_rightmost_set_bit(n)
print(f"Rightmost set bit: {rightmost} = {format(rightmost, '08b')}")

cleared = clear_rightmost_set_bit(n)
print(f"Clear rightmost bit: {cleared} = {format(cleared, '08b')}")
print()

print("Power of 2 check:")
test_nums = [1, 2, 3, 4, 8, 15, 16]
for num in test_nums:
    print(f"  {num:2d}: {is_power_of_2(num)}")
print()


print("=" * 60)
print("Bit Masks and Flags")
print("=" * 60)
print()

# Example: Unix file permissions
READ = 1 << 0    # 001
WRITE = 1 << 1   # 010
EXECUTE = 1 << 2 # 100

def has_permission(permissions, flag):
    return (permissions & flag) != 0

def grant_permission(permissions, flag):
    return permissions | flag

def revoke_permission(permissions, flag):
    return permissions & ~flag

# Start with no permissions
perms = 0
print(f"Initial permissions: {format(perms, '03b')}")

# Grant read and write
perms = grant_permission(perms, READ)
perms = grant_permission(perms, WRITE)
print(f"After granting R+W: {format(perms, '03b')}")
print(f"  Has READ: {has_permission(perms, READ)}")
print(f"  Has WRITE: {has_permission(perms, WRITE)}")
print(f"  Has EXECUTE: {has_permission(perms, EXECUTE)}")

# Revoke write
perms = revoke_permission(perms, WRITE)
print(f"After revoking W: {format(perms, '03b')}")
print(f"  Has WRITE: {has_permission(perms, WRITE)}")
print()


print("=" * 60)
print("Two's Complement (Negative Numbers)")
print("=" * 60)
print()

# In Python, integers have unlimited precision
# But in low-level systems (C, Java), integers are fixed width
def to_signed_32bit(n):
    """Convert to 32-bit signed integer."""
    if n >= (1 << 31):
        return n - (1 << 32)
    return n

print("Positive and negative representations:")
positive = 5
negative = -5
print(f"  {positive}: {bin(positive)}")
print(f" {negative}: {bin(negative & 0xFFFFFFFF)} (32-bit)")
print()

# Negation using two's complement: ~n + 1
n = 5
negated = (~n + 1) & 0xFFFFFFFF
print(f"Negate {n} using ~n+1:")
print(f"  Result: {bin(negated)} (32-bit)")
print(f"  As signed: {to_signed_32bit(negated)}")
print()


print("=" * 60)
print("Swap Without Temporary Variable")
print("=" * 60)
print()

def swap_xor(a, b):
    """Swap two numbers using XOR."""
    print(f"Before: a={a}, b={b}")
    a = a ^ b
    b = a ^ b  # b = (a ^ b) ^ b = a
    a = a ^ b  # a = (a ^ b) ^ a = b
    print(f"After:  a={a}, b={b}")
    return a, b

a, b = 5, 10
a, b = swap_xor(a, b)
print()


print("=" * 60)
print("Extract and Set Bit Ranges")
print("=" * 60)
print()

def get_bits(n, i, j):
    """Get bits from position i to j (inclusive)."""
    mask = ((1 << (j - i + 1)) - 1) << i
    return (n & mask) >> i

def set_bits(n, i, j, value):
    """Set bits from position i to j to value."""
    # Create mask with 1s from i to j
    mask = ((1 << (j - i + 1)) - 1) << i
    # Clear those bits and set new value
    return (n & ~mask) | (value << i)

n = 0b10110100  # 180
print(f"Number: {n} = {format(n, '08b')}")
print()

# Extract bits 2-4
bits = get_bits(n, 2, 4)
print(f"Extract bits 2-4: {bits} = {format(bits, '03b')}")

# Set bits 1-3 to 0b101
n_new = set_bits(n, 1, 3, 0b101)
print(f"Set bits 1-3 to 101: {n_new} = {format(n_new, '08b')}")
print()


print("=" * 60)
print("Bit Manipulation Tips")
print("=" * 60)
print()
print("Common operations:")
print("  • x & 1        : Check if odd")
print("  • x & (x-1)    : Clear rightmost bit")
print("  • x & -x       : Get rightmost bit")
print("  • x ^ x        : Always 0")
print("  • x ^ 0        : Always x")
print("  • x | (1 << i) : Set bit i")
print("  • x & ~(1 << i): Clear bit i")
print("  • x ^ (1 << i) : Toggle bit i")
print()
print("Check operations:")
print("  • x & (x-1) == 0 : Power of 2 (if x > 0)")
print("  • x & (x+1) == 0 : All 1s or 0")
print("  • x & (~x) == 0  : Always true")
print()
print("Arithmetic shortcuts:")
print("  • x << n       : Multiply by 2^n")
print("  • x >> n       : Divide by 2^n")
print("  • ~x           : -(x+1) in two's complement")
