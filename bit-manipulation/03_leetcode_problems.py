"""
Bit Manipulation - LeetCode Problems
====================================
Common bit manipulation interview problems.
"""

from typing import List


print("=" * 60)
print("Problem 1: Single Number (LeetCode 136)")
print("=" * 60)
print()

def single_number(nums: List[int]) -> int:
    """
    Find the number that appears once (others appear twice).
    
    Time: O(n), Space: O(1)
    Pattern: XOR - a ^ a = 0, a ^ 0 = a
    """
    result = 0
    for num in nums:
        result ^= num
    return result

print("Single Number:")
test_cases = [
    [2, 2, 1],
    [4, 1, 2, 1, 2],
    [1]
]
for nums in test_cases:
    result = single_number(nums)
    print(f"  {nums} -> {result}")
print()


print("=" * 60)
print("Problem 2: Number of 1 Bits (LeetCode 191)")
print("=" * 60)
print()

def hamming_weight(n: int) -> int:
    """
    Count number of 1 bits (Hamming weight).
    
    Time: O(1) - at most 32 iterations, Space: O(1)
    Pattern: Brian Kernighan's algorithm
    """
    count = 0
    while n:
        n &= n - 1  # Clear rightmost set bit
        count += 1
    return count

print("Count 1 Bits:")
test_cases = [11, 128, 2147483645]
for n in test_cases:
    result = hamming_weight(n)
    print(f"  {n} ({bin(n)}) -> {result} ones")
print()


print("=" * 60)
print("Problem 3: Counting Bits (LeetCode 338)")
print("=" * 60)
print()

def count_bits(n: int) -> List[int]:
    """
    Count 1 bits for all numbers from 0 to n.
    
    Time: O(n), Space: O(1) excluding output
    Pattern: DP - bits[i] = bits[i >> 1] + (i & 1)
    """
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    return result

print("Counting Bits 0 to n:")
for n in [2, 5, 8]:
    result = count_bits(n)
    print(f"  n={n}: {result}")
print()


print("=" * 60)
print("Problem 4: Reverse Bits (LeetCode 190)")
print("=" * 60)
print()

def reverse_bits(n: int) -> int:
    """
    Reverse bits of a 32-bit unsigned integer.
    
    Time: O(1), Space: O(1)
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

print("Reverse Bits:")
test_cases = [
    (0b00000010100101000001111010011100, "43261596"),
    (0b11111111111111111111111111111101, "3221225471")
]
for n, expected in test_cases:
    result = reverse_bits(n)
    print(f"  Input:  {format(n, '032b')}")
    print(f"  Output: {format(result, '032b')} = {result}")
print()


print("=" * 60)
print("Problem 5: Missing Number (LeetCode 268)")
print("=" * 60)
print()

def missing_number(nums: List[int]) -> int:
    """
    Find missing number in range [0, n].
    
    Time: O(n), Space: O(1)
    Pattern: XOR - missing number is XOR of all
    """
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

print("Missing Number:")
test_cases = [
    [3, 0, 1],
    [0, 1],
    [9, 6, 4, 2, 3, 5, 7, 0, 1]
]
for nums in test_cases:
    result = missing_number(nums)
    print(f"  {nums} -> missing: {result}")
print()


print("=" * 60)
print("Problem 6: Sum of Two Integers (LeetCode 371)")
print("=" * 60)
print()

def get_sum(a: int, b: int) -> int:
    """
    Add two integers without using + or -.
    
    Time: O(1), Space: O(1)
    Pattern: XOR for sum, AND << 1 for carry
    """
    mask = 0xFFFFFFFF
    
    while b != 0:
        # Calculate sum without carry
        sum_without_carry = (a ^ b) & mask
        # Calculate carry
        carry = ((a & b) << 1) & mask
        
        a = sum_without_carry
        b = carry
    
    # Handle negative numbers
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)

print("Sum of Two Integers (without + or -):")
test_cases = [(1, 2), (2, 3), (-1, 1), (-12, -8)]
for a, b in test_cases:
    result = get_sum(a, b)
    print(f"  {a} + {b} = {result}")
print()


print("=" * 60)
print("Problem 7: Hamming Distance (LeetCode 461)")
print("=" * 60)
print()

def hamming_distance(x: int, y: int) -> int:
    """
    Count positions where bits differ.
    
    Time: O(1), Space: O(1)
    Pattern: XOR + count set bits
    """
    xor = x ^ y
    count = 0
    while xor:
        count += xor & 1
        xor >>= 1
    return count

print("Hamming Distance:")
test_cases = [(1, 4), (3, 1), (93, 73)]
for x, y in test_cases:
    result = hamming_distance(x, y)
    print(f"  {x} ({bin(x)}) vs {y} ({bin(y)}) -> distance: {result}")
print()


print("=" * 60)
print("Problem 8: Power of Two (LeetCode 231)")
print("=" * 60)
print()

def is_power_of_two(n: int) -> bool:
    """
    Check if n is power of 2.
    
    Time: O(1), Space: O(1)
    Pattern: Power of 2 has only one set bit
    """
    return n > 0 and (n & (n - 1)) == 0

print("Power of Two:")
test_cases = [1, 16, 3, 4, 5, 1024]
for n in test_cases:
    result = is_power_of_two(n)
    print(f"  {n} ({bin(n)}) -> {result}")
print()


print("=" * 60)
print("Problem 9: Power of Four (LeetCode 342)")
print("=" * 60)
print()

def is_power_of_four(n: int) -> bool:
    """
    Check if n is power of 4.
    
    Time: O(1), Space: O(1)
    Pattern: Power of 4 = power of 2 AND bit at even position
    """
    # Must be power of 2 and bit must be at even position
    # 0x55555555 = 0b01010101010101010101010101010101
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0

print("Power of Four:")
test_cases = [1, 4, 5, 16, 64, 8]
for n in test_cases:
    result = is_power_of_four(n)
    print(f"  {n} ({bin(n)}) -> {result}")
print()


print("=" * 60)
print("Problem 10: Bitwise AND of Range (LeetCode 201)")
print("=" * 60)
print()

def range_bitwise_and(left: int, right: int) -> int:
    """
    Bitwise AND of all numbers in range [left, right].
    
    Time: O(log n), Space: O(1)
    Pattern: Find common prefix of left and right
    """
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift

print("Bitwise AND of Range:")
test_cases = [(5, 7), (0, 0), (1, 2147483647)]
for left, right in test_cases:
    result = range_bitwise_and(left, right)
    print(f"  [{left}, {right}] -> {result}")
print()


print("=" * 60)
print("Problem 11: Single Number II (LeetCode 137)")
print("=" * 60)
print()

def single_number_ii(nums: List[int]) -> int:
    """
    Find element appearing once (others appear 3 times).
    
    Time: O(n), Space: O(1)
    Pattern: Count bits modulo 3
    """
    ones = twos = 0
    
    for num in nums:
        twos |= ones & num
        ones ^= num
        threes = ones & twos
        ones &= ~threes
        twos &= ~threes
    
    return ones

print("Single Number II (others appear 3 times):")
test_cases = [
    [2, 2, 3, 2],
    [0, 1, 0, 1, 0, 1, 99]
]
for nums in test_cases:
    result = single_number_ii(nums)
    print(f"  {nums} -> {result}")
print()


print("=" * 60)
print("Problem 12: Single Number III (LeetCode 260)")
print("=" * 60)
print()

def single_number_iii(nums: List[int]) -> List[int]:
    """
    Find two elements appearing once (others appear twice).
    
    Time: O(n), Space: O(1)
    Pattern: XOR + partition by rightmost set bit
    """
    # Get XOR of the two unique numbers
    xor = 0
    for num in nums:
        xor ^= num
    
    # Get rightmost set bit
    rightmost_bit = xor & -xor
    
    # Partition numbers into two groups
    num1 = num2 = 0
    for num in nums:
        if num & rightmost_bit:
            num1 ^= num
        else:
            num2 ^= num
    
    return [num1, num2]

print("Single Number III (two unique numbers):")
test_cases = [
    [1, 2, 1, 3, 2, 5],
    [-1, 0],
    [0, 1]
]
for nums in test_cases:
    result = single_number_iii(nums)
    print(f"  {nums} -> {result}")
print()


print("=" * 60)
print("Problem 13: Maximum XOR (LeetCode 421)")
print("=" * 60)
print()

def find_maximum_xor(nums: List[int]) -> int:
    """
    Find maximum XOR of two numbers in array.
    
    Time: O(n), Space: O(1)
    Pattern: Greedy bit by bit from left
    """
    max_xor = 0
    mask = 0
    
    for i in range(31, -1, -1):
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}
        
        temp = max_xor | (1 << i)
        
        for prefix in prefixes:
            if temp ^ prefix in prefixes:
                max_xor = temp
                break
    
    return max_xor

print("Maximum XOR of Two Numbers:")
test_cases = [
    [3, 10, 5, 25, 2, 8],
    [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]
]
for nums in test_cases:
    result = find_maximum_xor(nums)
    print(f"  {nums[:5]}{'...' if len(nums) > 5 else ''} -> {result}")
print()


print("=" * 60)
print("Problem 14: Subsets (LeetCode 78)")
print("=" * 60)
print()

def subsets(nums: List[int]) -> List[List[int]]:
    """
    Generate all subsets using bit manipulation.
    
    Time: O(n * 2^n), Space: O(1) excluding output
    Pattern: Each bit represents include/exclude
    """
    n = len(nums)
    result = []
    
    for mask in range(1 << n):  # 2^n subsets
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result

print("Generate Subsets (bit masking):")
nums = [1, 2, 3]
result = subsets(nums)
print(f"  {nums} -> {len(result)} subsets:")
for subset in result:
    print(f"    {subset}")
print()


print("=" * 60)
print("Problem 15: UTF-8 Validation (LeetCode 393)")
print("=" * 60)
print()

def valid_utf8(data: List[int]) -> bool:
    """
    Check if data represents valid UTF-8 encoding.
    
    Time: O(n), Space: O(1)
    Pattern: Bit pattern matching
    """
    n_bytes = 0
    
    for num in data:
        if n_bytes == 0:
            # Count leading 1s to determine byte count
            if (num >> 7) == 0b0:
                continue
            elif (num >> 5) == 0b110:
                n_bytes = 1
            elif (num >> 4) == 0b1110:
                n_bytes = 2
            elif (num >> 3) == 0b11110:
                n_bytes = 3
            else:
                return False
        else:
            # Check continuation byte starts with 10
            if (num >> 6) != 0b10:
                return False
            n_bytes -= 1
    
    return n_bytes == 0

print("UTF-8 Validation:")
test_cases = [
    ([197, 130, 1], True),
    ([235, 140, 4], False)
]
for data, expected in test_cases:
    result = valid_utf8(data)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {data} -> {result}")
print()


print("=" * 60)
print("Bit Manipulation Summary")
print("=" * 60)
print()
print("Key Patterns:")
print("  1. XOR: Find unique elements, swap values")
print("  2. AND/OR: Set/clear/check bits")
print("  3. Shift: Multiply/divide by powers of 2")
print("  4. Counting: Brian Kernighan's algorithm")
print("  5. Power of 2: n & (n-1) == 0")
print("  6. Rightmost bit: n & -n")
print()
print("Common Tricks:")
print("  • XOR all: Find missing/unique element")
print("  • Count bits: n & (n-1) removes rightmost 1")
print("  • Bit masking: Generate subsets")
print("  • Partition: Use rightmost set bit")
print()
print("Time Complexity:")
print("  • Most operations: O(1)")
print("  • Iterating bits: O(log n) or O(32)")
