"""
Bit Manipulation - Common Patterns
==================================
Common patterns and techniques using bitwise operations.
"""

from typing import List


print("=" * 60)
print("Pattern 1: XOR Properties")
print("=" * 60)
print()

def find_single_number(nums: List[int]) -> int:
    """Find element that appears once (others appear twice)."""
    result = 0
    for num in nums:
        result ^= num
    return result

print("XOR Properties: a ^ a = 0, a ^ 0 = a")
print("Find single number in [4,1,2,1,2]:")
nums = [4, 1, 2, 1, 2]
print(f"  Result: {find_single_number(nums)}")
print()


def swap_numbers(a: int, b: int) -> tuple:
    """Swap two numbers without temporary variable."""
    print(f"  Before: a={a}, b={b}")
    a = a ^ b
    b = a ^ b  # b becomes original a
    a = a ^ b  # a becomes original b
    print(f"  After:  a={a}, b={b}")
    return a, b

print("Swap using XOR:")
swap_numbers(5, 10)
print()


print("=" * 60)
print("Pattern 2: Power of 2 Operations")
print("=" * 60)
print()

def is_power_of_2(n: int) -> bool:
    """Check if number is power of 2."""
    return n > 0 and (n & (n - 1)) == 0

def is_power_of_4(n: int) -> bool:
    """Check if number is power of 4."""
    # Must be power of 2 AND have 1 bit at even position
    return (n > 0 and 
            (n & (n - 1)) == 0 and 
            (n & 0x55555555) != 0)  # 0x55555555 = 01010101...

def next_power_of_2(n: int) -> int:
    """Find next power of 2 >= n."""
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1

print("Power of 2 checks:")
test_nums = [1, 2, 3, 4, 7, 8, 16, 31, 32]
for n in test_nums:
    pow2 = is_power_of_2(n)
    pow4 = is_power_of_4(n)
    print(f"  {n:2d}: Power of 2={pow2:5}, Power of 4={pow4}")
print()

print("Next power of 2:")
test_nums = [5, 10, 17, 33, 100]
for n in test_nums:
    print(f"  {n:3d} -> {next_power_of_2(n):3d}")
print()


print("=" * 60)
print("Pattern 3: Bit Counting")
print("=" * 60)
print()

def count_bits_dp(n: int) -> List[int]:
    """Count bits for numbers 0 to n using DP."""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        # i has same bits as i//2, plus 1 if i is odd
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

print("Counting bits from 0 to 10:")
result = count_bits_dp(10)
for i, count in enumerate(result):
    print(f"  {i:2d} = {format(i, '04b')}: {count} bits")
print()


def hamming_weight(n: int) -> int:
    """Count number of 1 bits (Hamming weight)."""
    count = 0
    while n:
        n &= n - 1  # Clear rightmost bit
        count += 1
    return count

def hamming_distance(x: int, y: int) -> int:
    """Count positions where bits differ."""
    return hamming_weight(x ^ y)

print("Hamming operations:")
x, y = 1, 4
print(f"  x = {x} = {format(x, '08b')}")
print(f"  y = {y} = {format(y, '08b')}")
print(f"  XOR = {format(x^y, '08b')}")
print(f"  Hamming distance: {hamming_distance(x, y)}")
print()


print("=" * 60)
print("Pattern 4: Subset Generation")
print("=" * 60)
print()

def generate_subsets(nums: List[int]) -> List[List[int]]:
    """Generate all subsets using bit manipulation."""
    n = len(nums)
    total = 1 << n  # 2^n subsets
    result = []
    
    for mask in range(total):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result

nums = [1, 2, 3]
print(f"All subsets of {nums}:")
subsets = generate_subsets(nums)
for i, subset in enumerate(subsets):
    print(f"  {format(i, '03b')}: {subset}")
print(f"Total: {len(subsets)} subsets")
print()


print("=" * 60)
print("Pattern 5: Missing Number Variants")
print("=" * 60)
print()

def find_missing_number(nums: List[int]) -> int:
    """Find missing number in range [0, n]."""
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

nums = [3, 0, 1]
print(f"Find missing in {nums}:")
print(f"  Missing: {find_missing_number(nums)}")
print()


def find_two_missing(nums: List[int], n: int) -> List[int]:
    """Find two missing numbers in range [1, n]."""
    # XOR all numbers and find XOR of two missing
    xor = 0
    for i in range(1, n + 1):
        xor ^= i
    for num in nums:
        xor ^= num
    
    # Find rightmost set bit
    rightmost_bit = xor & -xor
    
    # Divide into two groups
    num1 = num2 = 0
    for i in range(1, n + 1):
        if i & rightmost_bit:
            num1 ^= i
        else:
            num2 ^= i
    
    for num in nums:
        if num & rightmost_bit:
            num1 ^= num
        else:
            num2 ^= num
    
    return [num1, num2]

nums = [1, 3, 4, 6]
n = 6
print(f"Find two missing in {nums} (range 1-{n}):")
print(f"  Missing: {sorted(find_two_missing(nums, n))}")
print()


print("=" * 60)
print("Pattern 6: Bitwise AND Range")
print("=" * 60)
print()

def range_bitwise_and(left: int, right: int) -> int:
    """Bitwise AND of all numbers in range [left, right]."""
    shift = 0
    # Find common prefix
    while left != right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift

print("Bitwise AND of ranges:")
test_cases = [(5, 7), (0, 0), (1, 2147483647)]
for left, right in test_cases:
    result = range_bitwise_and(left, right)
    print(f"  [{left}, {right}]: {result}")
print()


print("=" * 60)
print("Pattern 7: Maximum XOR")
print("=" * 60)
print()

def find_maximum_xor(nums: List[int]) -> int:
    """Find maximum XOR of two numbers in array."""
    max_xor = 0
    mask = 0
    
    # Check from highest bit to lowest
    for i in range(31, -1, -1):
        mask |= (1 << i)
        prefixes = set()
        
        # Collect all prefixes
        for num in nums:
            prefixes.add(num & mask)
        
        # Try to set current bit to 1
        temp = max_xor | (1 << i)
        
        # Check if we can achieve this XOR
        for prefix in prefixes:
            if (temp ^ prefix) in prefixes:
                max_xor = temp
                break
    
    return max_xor

nums = [3, 10, 5, 25, 2, 8]
print(f"Maximum XOR in {nums}:")
print(f"  Result: {find_maximum_xor(nums)}")
print(f"  (25 ^ 2 = {25 ^ 2})")
print()


print("=" * 60)
print("Pattern 8: Gray Code")
print("=" * 60)
print()

def gray_code(n: int) -> List[int]:
    """Generate n-bit Gray code sequence."""
    result = []
    for i in range(1 << n):
        result.append(i ^ (i >> 1))
    return result

def binary_to_gray(n: int) -> int:
    """Convert binary to Gray code."""
    return n ^ (n >> 1)

def gray_to_binary(gray: int) -> int:
    """Convert Gray code to binary."""
    binary = gray
    gray >>= 1
    while gray:
        binary ^= gray
        gray >>= 1
    return binary

n = 3
print(f"{n}-bit Gray code:")
codes = gray_code(n)
for i, code in enumerate(codes):
    print(f"  {i}: {format(code, '03b')}")
print()


print("=" * 60)
print("Pattern 9: Reverse Bits")
print("=" * 60)
print()

def reverse_bits(n: int) -> int:
    """Reverse bits of a 32-bit integer."""
    result = 0
    for i in range(32):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result

def reverse_bits_optimized(n: int) -> int:
    """Reverse bits using divide and conquer."""
    # Swap adjacent bits
    n = ((n & 0x55555555) << 1) | ((n & 0xAAAAAAAA) >> 1)
    # Swap adjacent pairs
    n = ((n & 0x33333333) << 2) | ((n & 0xCCCCCCCC) >> 2)
    # Swap adjacent quads
    n = ((n & 0x0F0F0F0F) << 4) | ((n & 0xF0F0F0F0) >> 4)
    # Swap adjacent bytes
    n = ((n & 0x00FF00FF) << 8) | ((n & 0xFF00FF00) >> 8)
    # Swap adjacent 16-bit blocks
    n = (n << 16) | (n >> 16)
    return n & 0xFFFFFFFF

n = 43261596  # 00000010100101000001111010011100
print(f"Reverse bits of {n}:")
print(f"  Original: {format(n, '032b')}")
reversed_n = reverse_bits(n)
print(f"  Reversed: {format(reversed_n, '032b')}")
print(f"  Decimal:  {reversed_n}")
print()


print("=" * 60)
print("Pattern 10: Single Number Variants")
print("=" * 60)
print()

def single_number_iii(nums: List[int]) -> List[int]:
    """Two elements appear once, others twice."""
    # XOR all numbers
    xor = 0
    for num in nums:
        xor ^= num
    
    # Find rightmost set bit
    rightmost_bit = xor & -xor
    
    # Divide into two groups
    num1 = num2 = 0
    for num in nums:
        if num & rightmost_bit:
            num1 ^= num
        else:
            num2 ^= num
    
    return [num1, num2]

nums = [1, 2, 1, 3, 2, 5]
print(f"Find two unique numbers in {nums}:")
print(f"  Result: {single_number_iii(nums)}")
print()


print("=" * 60)
print("Bit Manipulation Patterns Summary")
print("=" * 60)
print()
print("Key Patterns:")
print("  1. XOR: Finding unique elements, swapping")
print("  2. Power of 2: n & (n-1) == 0")
print("  3. Counting: Brian Kernighan's algorithm")
print("  4. Subsets: Iterate through 2^n masks")
print("  5. Missing numbers: XOR properties")
print("  6. Range AND: Find common prefix")
print("  7. Maximum XOR: Trie or greedy bit-by-bit")
print("  8. Gray code: n ^ (n >> 1)")
print("  9. Reverse bits: Swap adjacent groups")
print(" 10. Partitioning: Use rightmost set bit")
print()
print("Time Complexity Tips:")
print("  • Most operations: O(1) or O(log n)")
print("  • Bit counting: O(number of set bits)")
print("  • Generating subsets: O(n * 2^n)")
