from typing import List, Tuple


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        last_seen = {}
        for i, n in enumerate(nums):
            if n in last_seen and i - last_seen[n] <= k:
                return True
            last_seen[n] = i
        return False

    def nearby_almost_duplicate(self, nums: List[int], k: int, t: int) -> Tuple:
        def h(a):
            if not a:
                return None
            min_value, max_value = min(v for _, v in a), max(v for _, v in a)
            if max_value - min_value <= 2 * t:
                return next((((i1, v1), (i2, v2))
                            for j, (i1, v1) in enumerate(a)
                            for (i2, v2) in a[j + 1: j + 3]
                            if i2 - i1 <= k and abs(v1 - v2) <= t), None)
            med = (min_value + max_value) // 2
            return h([(i, v) for i, v in a if v <= med]) \
                   or h([(i, v) for i, v in a if v > med]) \
                   or h([(i, v) for i, v in a if abs(med - v) <= t])

        return h(list(enumerate(nums)))

    def containsNearbyAlmostDuplicate(self, nums, k, t):
        if t < 0: return False
        d = {}
        for i, v in enumerate(nums):
            m = v // (t + 1)
            if m in d or (m - 1 in d and v - d[m - 1] <= t) or (m + 1 in d and d[m + 1] - v <= t):
                return True
            d[m] = v
            if i >= k:
                del d[nums[i - k] // (t + 1)]
        return False


