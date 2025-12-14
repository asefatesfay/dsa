"""
Blind 75 - Binary Problems
===========================
Bit manipulation problems for technical interviews.
"""


# 1. Sum of Two Integers
# PATTERN: Bit Manipulation (XOR and AND)
def get_sum(a, b):
    """
    Add two integers without using + or - operators.
    
    Pattern: XOR for sum, AND << 1 for carry
    Approach: Bit manipulation with XOR and AND
    Steps:
    1. XOR gives sum without carry: a ^ b
    2. AND gives carry positions: (a & b) << 1
    3. Repeat until no carry
    
    Note: Python has arbitrary precision, need mask for negatives
    
    Time: O(1), Space: O(1)
    """
    mask = 0xFFFFFFFF
    while b != 0:
        carry = (a & b) << 1
        a = (a ^ b) & mask
        b = carry & mask
    # Handle negative in Python
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)


# 2. Number of 1 Bits (Hamming Weight)
# PATTERN: Bit Manipulation (Brian Kernighan's Algorithm)
def hamming_weight(n):
    """
    Count number of '1' bits in integer.
    
    Pattern: n & (n-1) removes rightmost 1-bit
    Approach: Check each bit or use n & (n-1) trick
    Steps:
    1. n & (n-1) removes rightmost 1 bit
    2. Count how many times we can do this
    
    Time: O(number of 1 bits), Space: O(1)
    """
    count = 0
    while n:
        n &= n - 1  # Remove rightmost 1
        count += 1
    return count


# 3. Counting Bits
# PATTERN: Dynamic Programming (Bit DP)
def count_bits(n):
    """
    Return array where ans[i] is number of 1's in binary of i.
    
    Pattern: DP with i >> 1 + (i & 1)
    Approach: DP using i & (i-1) relationship
    Steps:
    1. dp[i] = dp[i & (i-1)] + 1
    2. i & (i-1) is i with rightmost 1 removed
    3. So count[i] = count[i with rightmost 1 removed] + 1
    
    Alternative: dp[i] = dp[i >> 1] + (i & 1)
    
    Time: O(n), Space: O(1) excluding output
    """
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i & (i - 1)] + 1
    return result


# 4. Missing Number
# PATTERN: Bit Manipulation (XOR)
def missing_number(nums):
    """
    Find missing number in array containing n distinct numbers in range [0, n].
    
    Pattern: XOR cancellation - all pairs cancel out
    Approach 1: XOR (all numbers XOR with indices)
    Approach 2: Gauss sum formula
    
    XOR approach:
    - XOR all array elements with all indices 0 to n
    - Pairs cancel out, leaving missing number
    
    Time: O(n), Space: O(1)
    """
    # Method 1: XOR
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
    
    # Method 2: Sum formula
    # n = len(nums)
    # expected_sum = n * (n + 1) // 2
    # return expected_sum - sum(nums)


# 5. Reverse Bits
# PATTERN: Bit Manipulation (Bit Reversal)
def reverse_bits(n):
    """
    Reverse bits of a 32-bit unsigned integer.
    
    Pattern: Extract each bit and build reversed result
    Approach: Build result bit by bit
    Steps:
    1. Extract rightmost bit: n & 1
    2. Shift result left and add extracted bit
    3. Shift n right
    4. Repeat 32 times
    
    Time: O(1), Space: O(1)
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# Additional: Power of Two
def is_power_of_two(n):
    """
    Check if n is power of two.
    
    Approach: Power of 2 has exactly one 1 bit
    - n & (n-1) removes rightmost 1
    - If n is power of 2, result should be 0
    
    Time: O(1), Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Additional: Single Number
def single_number(nums):
    """
    Find element that appears once (all others appear twice).
    
    Approach: XOR
    - a ^ a = 0
    - a ^ 0 = a
    - XOR is commutative and associative
    
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


if __name__ == "__main__":
    print("=== Binary Problems ===\n")
    
    # Sum of Two Integers
    print("1. Sum(3, 5):", get_sum(3, 5))
    
    # Number of 1 Bits
    print("2. Hamming Weight(11):", hamming_weight(11))  # 1011 -> 3
    
    # Counting Bits
    print("3. Count Bits(5):", count_bits(5))
    
    # Missing Number
    print("4. Missing Number([3,0,1]):", missing_number([3, 0, 1]))
    
    # Reverse Bits
    print("5. Reverse Bits(43261596):", reverse_bits(43261596))
    
    # Additional
    print("\n--- Additional ---")
    print("Power of Two(16):", is_power_of_two(16))
    print("Single Number([4,1,2,1,2]):", single_number([4, 1, 2, 1, 2]))
