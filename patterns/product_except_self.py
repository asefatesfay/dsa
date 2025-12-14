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