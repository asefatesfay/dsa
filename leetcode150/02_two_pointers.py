"""
LeetCode 150 - Two Pointers
============================
Problems using two-pointer technique.
"""


# PATTERN: Two Pointers
def is_palindrome(s):
    """
    Valid Palindrome - check if alphanumeric characters form palindrome.
    
    Pattern: Two pointers from both ends
    
    Algorithm Steps:
    1. Use two pointers from start and end
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


# PATTERN: Two Pointers
def is_subsequence(s, t):
    """
    Check if s is subsequence of t.
    
    Pattern: Two pointers tracking match progress
    
    Algorithm Steps:
    1. Pointer i for s, pointer j for t
    2. When s[i] == t[j], advance i
    3. Always advance j
    4. If i reaches end of s, found subsequence
    
    Time: O(n), Space: O(1)
    """
    i = 0
    for j in range(len(t)):
        if i < len(s) and s[i] == t[j]:
            i += 1
    return i == len(s)


# PATTERN: Two Pointers
def two_sum_ii(numbers, target):
    """
    Two Sum II - array is sorted, return 1-indexed positions.
    
    Pattern: Two pointers from both ends
    
    Algorithm Steps:
    1. Start with left=0, right=n-1
    2. If sum < target, move left pointer right
    3. If sum > target, move right pointer left
    4. If sum == target, found answer
    
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


# PATTERN: Two Pointers
def max_area(height):
    """
    Container With Most Water - maximize area between two lines.
    
    Pattern: Two pointers from both ends
    
    Algorithm Steps:
    1. Start with widest container (left=0, right=n-1)
    2. Area = min(height[left], height[right]) * width
    3. Move pointer with smaller height (potential for improvement)
    
    Why it works: Moving the taller line can't improve area
    (width decreases, height limited by shorter line)
    
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


# PATTERN: Two Pointers with Sorting
def three_sum(nums):
    """
    3Sum - find all unique triplets that sum to zero.
    
    Pattern: Sort + Two pointers for each element
    
    Algorithm Steps:
    1. Sort array
    2. For each element i, use two pointers for remaining array
    3. Skip duplicates to avoid duplicate triplets
    
    Time: O(n²), Space: O(1) excluding output
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first element
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


# PATTERN: Two Pointers with Sorting
def three_sum_closest(nums, target):
    """
    3Sum Closest - find triplet with sum closest to target.
    
    Pattern: Sort + Two pointers
    
    Algorithm Steps:
    1. Sort array
    2. For each element, use two pointers
    3. Track closest sum found
    
    Time: O(n²), Space: O(1)
    """
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest if current is closer
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return current_sum  # Exact match
    
    return closest_sum


if __name__ == "__main__":
    print("=== LeetCode 150 - Two Pointers ===\n")
    
    # Valid Palindrome
    print(f"Is Palindrome 'A man, a plan, a canal: Panama': {is_palindrome('A man, a plan, a canal: Panama')}")
    print(f"Is Palindrome 'race a car': {is_palindrome('race a car')}")
    
    # Is Subsequence
    print(f"Is Subsequence 'abc' in 'ahbgdc': {is_subsequence('abc', 'ahbgdc')}")
    print(f"Is Subsequence 'axc' in 'ahbgdc': {is_subsequence('axc', 'ahbgdc')}")
    
    # Two Sum II
    print(f"Two Sum II [2,7,11,15] target=9: {two_sum_ii([2, 7, 11, 15], 9)}")
    
    # Container With Most Water
    print(f"Max Area [1,8,6,2,5,4,8,3,7]: {max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])}")
    
    # 3Sum
    print(f"3Sum [-1,0,1,2,-1,-4]: {three_sum([-1, 0, 1, 2, -1, -4])}")
    
    # 3Sum Closest
    print(f"3Sum Closest [-1,2,1,-4] target=1: {three_sum_closest([-1, 2, 1, -4], 1)}")
