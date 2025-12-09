"""
Linear Search
=============
Simple search that scans the array from left to right.
"""


def linear_search(arr, target):
    """
    Return index of target in arr, or -1 if not found.
    Time: O(n)  Space: O(1)
    """
    # STEP 1: Iterate through each element
    for i, val in enumerate(arr):
        # STEP 2: Compare current value with target
        if val == target:
            # STEP 3: Found → return index
            return i
    # STEP 4: Not found → return -1
    return -1


if __name__ == "__main__":
    data = [4, 2, 7, 1, 9]
    print("Array:", data)
    for t in [7, 3, 1]:
        idx = linear_search(data, t)
        print(f"Find {t}: index={idx}")
