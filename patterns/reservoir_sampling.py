"""
Reservoir Sampling / Randomized Algorithms
=========================================
Sample k items uniformly at random from a stream of unknown length.
"""

import random


def reservoir_sample(stream, k, seed=None):
    """
    Keep a reservoir of size k. For i-th item (1-indexed), replace with prob k/i.
    Ensures uniform sampling over the stream.
    Time: O(n) Space: O(k)
    """
    if seed is not None:
        random.seed(seed)
    reservoir = []
    for i, item in enumerate(stream, start=1):
        if i <= k:
            reservoir.append(item)
        else:
            j = random.randint(1, i)
            if j <= k:
                reservoir[j - 1] = item
    return reservoir


def random_shuffle(arr, seed=None):
    """
    Fisher-Yates shuffle for unbiased random permutation.
    """
    if seed is not None:
        random.seed(seed)
    a = arr[:]
    for i in range(len(a) - 1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return a


if __name__ == "__main__":
    stream = range(1, 101)
    print("reservoir 5:", reservoir_sample(stream, 5, seed=42))
    print("shuffle:", random_shuffle([1,2,3,4,5], seed=123))

# =====================
# Additional Randomized Problems
# =====================

class RandomPickIndex:
    """
    Given array with duplicates, pick a random index of a target with uniform probability.
    Uses reservoir sampling per query.
    """
    def __init__(self, nums):
        self.nums = nums

    def pick(self, target, seed=None):
        import random
        if seed is not None:
            random.seed(seed)
        count = 0
        chosen = -1
        for i, x in enumerate(self.nums):
            if x == target:
                count += 1
                if random.randint(1, count) == 1:
                    chosen = i
        return chosen


def sample_distinct_users(stream_ids, k, seed=None):
    """
    Reservoir sample distinct user IDs from a stream with repeats.
    Maintains a set to avoid duplicates in the reservoir.
    """
    import random
    if seed is not None:
        random.seed(seed)
    reservoir = []
    seen = set()
    i = 0
    for uid in stream_ids:
        if uid in seen:
            continue
        i += 1
        if len(reservoir) < k:
            reservoir.append(uid)
            seen.add(uid)
        else:
            j = random.randint(1, i)
            if j <= k:
                # replace random slot
                pos = random.randint(0, k - 1)
                seen.discard(reservoir[pos])
                reservoir[pos] = uid
                seen.add(uid)
    return reservoir


if __name__ == "__main__":
    rpi = RandomPickIndex([1,2,3,3,3])
    print("pick idx of 3:", rpi.pick(3, seed=7))
    print("distinct sample:", sample_distinct_users([1,1,2,3,3,4,5,5,6], 3, seed=99))
