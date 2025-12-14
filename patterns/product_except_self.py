# The product of an array execpt self

def product_except_self(nums):
    total_product = 1
    zero_count = 0
    
    for num in nums:
        if num !=0:
            total_product *= num
        else:
            zero_count += 1
    
    for i in range(len(nums)):
        if zero_count > 1:
            nums[i] = 0
        elif zero_count == 1:
            if nums[i] == 0:
                nums[i] = total_product
            else:
                nums[i] = 0
        else:
            nums[i] = total_product // nums[i]
    return nums

def product_except_self_prefix_suffix(nums):
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n
    result = [1] * n
    
    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]
    
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]
    
    for i in range(n):
        result[i] = prefix[i] * suffix[i]
    
    return result

def product_except_self_optimized(nums):
    n = len(nums)
    result = [1] * n
    
    # Left pass
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    
    # Right pass
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    
    return result

if __name__ == "__main__":
    # Test the product_except_self function
    print("Product of Array Except Self")
    test_array = [1, 2, 3, 4]
    print(f"Input: {test_array}")
    print(f"Output: {product_except_self(test_array)}")
    
    test_array = [0, 2, 3, 4]
    print(f"Input: {test_array}")
    print(f"Output: {product_except_self(test_array)}")
    test_array = [0, 2, 0, 4]
    print(f"Input: {test_array}")
    print(f"Output: {product_except_self(test_array)}")
    test_array = [-1, 1, 0, -3, 3]
    print(f"Input: {test_array}")
    print(f"Output: {product_except_self(test_array)}")
    print()