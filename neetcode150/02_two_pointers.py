"""
NeetCode 150 - Two Pointers
============================
Master the two-pointer technique.
"""


# PATTERN: Two Pointers (Converging)
def is_palindrome(s):
    """
    Valid Palindrome - check if string is palindrome (alphanumeric only).
    
    Pattern: Two pointers from both ends
    
    Algorithm Steps:
    1. Use left and right pointers
    2. Skip non-alphanumeric characters
    3. Compare characters (case-insensitive)
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True


# PATTERN: Two Pointers (Converging on Sorted Array)
def two_sum_ii(numbers, target):
    """
    Two Sum II - sorted array, return 1-indexed positions.
    
    Pattern: Two pointers on sorted array
    
    Algorithm Steps:
    1. Start with left=0, right=n-1
    2. If sum < target, move left right (increase sum)
    3. If sum > target, move right left (decrease sum)
    4. If sum == target, found answer
    
    Why it works: Array is sorted, so we can eliminate half the search space
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []


# PATTERN: Two Pointers with Sorting
def three_sum(nums):
    """
    3Sum - find all unique triplets that sum to zero.
    
    Pattern: Sort + Two pointers for each element
    
    Algorithm Steps:
    1. Sort array
    2. For each element i, use two pointers for remaining array
    3. Skip duplicates to avoid duplicate triplets
    
    Example: [-1,0,1,2,-1,-4]
    - Sort: [-4,-1,-1,0,1,2]
    - Fix -1, find two pointers in [-1,0,1,2] that sum to 1
    
    Time: O(n²), Space: O(1) excluding output
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        target = -nums[i]
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result


# PATTERN: Two Pointers (Converging)
def max_area(height):
    """
    Container With Most Water - maximize area between two lines.
    
    Pattern: Two pointers from both ends
    
    Algorithm Steps:
    1. Start with widest container (left=0, right=n-1)
    2. Area = min(height[left], height[right]) * width
    3. Move pointer with smaller height (only way to potentially improve)
    
    Why it works: Moving the taller line can't improve area because:
    - Width decreases
    - Height is still limited by shorter line
    
    Example: [1,8,6,2,5,4,8,3,7]
    - Start: left=0 (h=1), right=8 (h=7), area = 1*8 = 8
    - Move left (h=1 is smaller): left=1 (h=8), right=8 (h=7), area = 7*7 = 49
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        current_area = min(height[left], height[right]) * width
        max_area = max(max_area, current_area)
        
        # Move pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


# PATTERN: Two Pointers / Stack
def trap(height):
    """
    Trapping Rain Water.
    
    Pattern: Two pointers with max heights tracking
    
    Algorithm Steps:
    1. Use left and right pointers
    2. Track left_max and right_max seen so far
    3. Water at position = min(left_max, right_max) - height
    4. Move pointer from side with smaller max
    
    Why it works: Water level is determined by smaller of the two boundaries
    
    Example: [0,1,0,2,1,0,1,3,2,1,2,1]
    - At position 2 (h=0): left_max=1, right_max=3, water = 1-0 = 1
    - At position 5 (h=0): left_max=2, right_max=3, water = 2-0 = 2
    
    Time: O(n), Space: O(1)
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water


if __name__ == "__main__":
    print("=== NeetCode 150 - Two Pointers ===\n")
    
    # Valid Palindrome
    print(f"Is Palindrome 'A man, a plan, a canal: Panama': {is_palindrome('A man, a plan, a canal: Panama')}")
    print(f"Is Palindrome 'race a car': {is_palindrome('race a car')}")
    
    # Two Sum II
    print(f"Two Sum II [2,7,11,15] target=9: {two_sum_ii([2, 7, 11, 15], 9)}")
    print(f"Two Sum II [2,3,4] target=6: {two_sum_ii([2, 3, 4], 6)}")
    
    # 3Sum
    print(f"3Sum [-1,0,1,2,-1,-4]: {three_sum([-1, 0, 1, 2, -1, -4])}")
    
    # Container With Most Water
    print(f"Max Area [1,8,6,2,5,4,8,3,7]: {max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])}")
    
    # Trapping Rain Water
    print(f"Trap Rain Water [0,1,0,2,1,0,1,3,2,1,2,1]: {trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])}")
    print(f"Trap Rain Water [4,2,0,3,2,5]: {trap([4, 2, 0, 3, 2, 5])}")
