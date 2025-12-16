"""
NeetCode 150 - Greedy
=====================
Locally optimal choices (8 problems).
"""


# PATTERN: Greedy Frequency
def is_n_straight_hand(hand, groupSize):
    """
    Hand of Straights - can rearrange into groups of consecutive cards.
    
    Pattern: Greedy with frequency map
    
    Time: O(n log n), Space: O(n)
    """
    if len(hand) % groupSize != 0:
        return False
    
    from collections import Counter
    count = Counter(hand)
    
    for card in sorted(count.keys()):
        if count[card] > 0:
            needed = count[card]
            for i in range(groupSize):
                if count[card + i] < needed:
                    return False
                count[card + i] -= needed
    
    return True


# PATTERN: Greedy Two Pointers
def merge_triplets(triplets, target):
    """
    Merge Triplets to Form Target - can merge triplets to match target.
    
    Pattern: Check if all positions can reach target
    
    Time: O(n), Space: O(1)
    """
    good = set()
    
    for t in triplets:
        if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
            continue
        
        for i in range(3):
            if t[i] == target[i]:
                good.add(i)
    
    return len(good) == 3


# PATTERN: Greedy Interval
def partition_labels(s):
    """
    Partition Labels - partition string into max parts where each char appears in one part.
    
    Pattern: Track last occurrence of each char
    
    Time: O(n), Space: O(26)
    """
    last = {c: i for i, c in enumerate(s)}
    
    result = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        end = max(end, last[char])
        
        if i == end:
            result.append(end - start + 1)
            start = i + 1
    
    return result


# PATTERN: Greedy with Validation
def check_valid_string(s):
    """
    Valid Parenthesis String - '(' ')' and '*' (wildcard).
    
    Pattern: Track min/max possible open brackets
    
    Time: O(n), Space: O(1)
    """
    left_min, left_max = 0, 0
    
    for char in s:
        if char == '(':
            left_min += 1
            left_max += 1
        elif char == ')':
            left_min -= 1
            left_max -= 1
        else:  # '*'
            left_min -= 1  # Treat as ')'
            left_max += 1  # Treat as '('
        
        if left_max < 0:
            return False
        
        left_min = max(left_min, 0)
    
    return left_min == 0


# PATTERN: Greedy Sorting
def find_min_arrow_shots(points):
    """
    Minimum Number of Arrows to Burst Balloons.
    
    Pattern: Sort by end, shoot at earliest end
    
    Time: O(n log n), Space: O(1)
    """
    if not points:
        return 0
    
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    
    for start, balloon_end in points:
        if start > end:
            arrows += 1
            end = balloon_end
    
    return arrows


# PATTERN: Greedy Jump
def can_jump(nums):
    """
    Jump Game - can reach last index.
    
    Pattern: Track farthest reachable position
    
    Time: O(n), Space: O(1)
    """
    goal = len(nums) - 1
    
    for i in range(len(nums) - 2, -1, -1):
        if i + nums[i] >= goal:
            goal = i
    
    return goal == 0


# PATTERN: Greedy BFS
def jump(nums):
    """
    Jump Game II - minimum jumps to reach last index.
    
    Pattern: BFS-like greedy (track window)
    
    Time: O(n), Space: O(1)
    """
    jumps = 0
    l, r = 0, 0
    
    while r < len(nums) - 1:
        farthest = 0
        for i in range(l, r + 1):
            farthest = max(farthest, i + nums[i])
        
        l = r + 1
        r = farthest
        jumps += 1
    
    return jumps


# PATTERN: Greedy Stack
def can_complete_circuit(gas, cost):
    """
    Gas Station - find starting station to complete circuit.
    
    Pattern: If total gas >= total cost, solution exists
    
    Time: O(n), Space: O(1)
    """
    if sum(gas) < sum(cost):
        return -1
    
    total = 0
    start = 0
    
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        
        if total < 0:
            total = 0
            start = i + 1
    
    return start


if __name__ == "__main__":
    print("=== NeetCode 150 - Greedy ===\n")
    
    print("Test 1: Hand of Straights")
    print(f"[1,2,3,6,2,3,4,7,8], groupSize=3: {is_n_straight_hand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3)}")
    
    print("\nTest 2: Merge Triplets")
    triplets = [[2, 5, 3], [1, 8, 4], [1, 7, 5]]
    target = [2, 7, 5]
    print(f"Can merge to {target}: {merge_triplets(triplets, target)}")
    
    print("\nTest 3: Partition Labels")
    print(f"'ababcbacadefegdehijhklij': {partition_labels('ababcbacadefegdehijhklij')}")
    
    print("\nTest 4: Valid Parenthesis String")
    print(f"'(*)': {check_valid_string('(*)')}")
    print(f"'(*))': {check_valid_string('(*))')}")
    
    print("\nTest 5: Minimum Arrows")
    points = [[10, 16], [2, 8], [1, 6], [7, 12]]
    print(f"Points {points}: {find_min_arrow_shots(points)} arrows")
    
    print("\nTest 6: Jump Game")
    print(f"[2,3,1,1,4]: {can_jump([2, 3, 1, 1, 4])}")
    print(f"[3,2,1,0,4]: {can_jump([3, 2, 1, 0, 4])}")
    
    print("\nTest 7: Jump Game II")
    print(f"[2,3,1,1,4]: {jump([2, 3, 1, 1, 4])} jumps")
    
    print("\nTest 8: Gas Station")
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    print(f"Gas {gas}, Cost {cost}: start at {can_complete_circuit(gas, cost)}")
