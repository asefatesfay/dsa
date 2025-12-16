"""
NeetCode 150 - Bit Manipulation
================================
Bitwise operations (7 problems).
"""


# PATTERN: XOR Property
def single_number(nums):
    """
    Single Number - find element that appears once.
    
    Pattern: XOR cancels duplicates (a ^ a = 0)
    
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


# PATTERN: Bit Counting
def hamming_weight(n):
    """
    Number of 1 Bits - count set bits.
    
    Pattern: n & (n-1) removes rightmost 1
    
    Time: O(1), Space: O(1)
    """
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


# PATTERN: Bit Counting
def counting_bits(n):
    """
    Counting Bits - count 1s for all numbers 0 to n.
    
    Pattern: DP with bit shift (num >> 1)
    
    Algorithm Steps:
    1. dp[i] = dp[i >> 1] + (i & 1)
    2. Right shift removes last bit
    3. Add 1 if last bit was 1
    
    Time: O(n), Space: O(n)
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp


# PATTERN: Bit Reversal
def reverse_bits(n):
    """
    Reverse Bits - reverse bits of 32-bit integer.
    
    Pattern: Extract bits and build reversed number
    
    Time: O(1), Space: O(1)
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# PATTERN: Bit Masking
def missing_number(nums):
    """
    Missing Number - find missing number in [0, n].
    
    Pattern: XOR all indices and values
    
    Time: O(n), Space: O(1)
    """
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result


# PATTERN: XOR with Index
def get_sum(a, b):
    """
    Sum of Two Integers - add without + or - operators.
    
    Pattern: XOR for sum, AND << 1 for carry
    
    Time: O(1), Space: O(1)
    """
    mask = 0xFFFFFFFF
    
    while b != 0:
        sum_without_carry = (a ^ b) & mask
        carry = ((a & b) << 1) & mask
        a = sum_without_carry
        b = carry
    
    # Handle negative numbers
    if a > 0x7FFFFFFF:
        return ~(a ^ mask)
    return a


# PATTERN: Bit Manipulation
def reverse_integer(x):
    """
    Reverse Integer - reverse digits of signed integer.
    
    Pattern: Extract digits and build reversed number
    
    Time: O(log x), Space: O(1)
    """
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    
    result = 0
    sign = -1 if x < 0 else 1
    x = abs(x)
    
    while x:
        digit = x % 10
        x //= 10
        
        # Check overflow
        if result > INT_MAX // 10:
            return 0
        
        result = result * 10 + digit
    
    result *= sign
    
    return result if INT_MIN <= result <= INT_MAX else 0


if __name__ == "__main__":
    print("=== NeetCode 150 - Bit Manipulation ===\n")
    
    print("Test 1: Single Number")
    print(f"Single in [2,2,1]: {single_number([2, 2, 1])}")
    print(f"Single in [4,1,2,1,2]: {single_number([4, 1, 2, 1, 2])}")
    
    print("\nTest 2: Number of 1 Bits")
    print(f"Hamming weight of 11 (1011): {hamming_weight(11)}")
    print(f"Hamming weight of 128 (10000000): {hamming_weight(128)}")
    
    print("\nTest 3: Counting Bits")
    print(f"Counting bits 0 to 5: {counting_bits(5)}")
    
    print("\nTest 4: Reverse Bits")
    n = 0b00000010100101000001111010011100
    print(f"Reverse of {bin(n)}: {bin(reverse_bits(n))}")
    
    print("\nTest 5: Missing Number")
    print(f"Missing in [3,0,1]: {missing_number([3, 0, 1])}")
    print(f"Missing in [0,1]: {missing_number([0, 1])}")
    
    print("\nTest 6: Sum of Two Integers")
    print(f"Sum of 1 and 2: {get_sum(1, 2)}")
    print(f"Sum of 2 and 3: {get_sum(2, 3)}")
    
    print("\nTest 7: Reverse Integer")
    print(f"Reverse 123: {reverse_integer(123)}")
    print(f"Reverse -123: {reverse_integer(-123)}")
    print(f"Reverse 120: {reverse_integer(120)}")
    
    print("\n=== NeetCode 150 - All 18 Categories Complete! ===")
