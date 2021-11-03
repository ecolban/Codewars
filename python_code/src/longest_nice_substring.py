from collections import Counter

"""
A string is nice if every every letter it contains occurs in upper and lower case. 
Given a string, find the longest substring that is nice.
"""


class Solution1:
    @staticmethod
    def longest_nice_substring(s: str) -> str:
        start, end = 0, len(s)
        lower_letters = Counter(c for c in s if c.islower())
        upper_letters = Counter(c for c in s if c.isupper())
        while {k for k, v in lower_letters.items() if v > 0} != {k.lower() for k, v in upper_letters.items() if v > 0}:
            if end == len(s):
                end -= start + 1
                start = 0
                lower_letters = Counter(c for c in s[:end] if c.islower())
                upper_letters = Counter(c for c in s[:end] if c.isupper())
            else:
                if s[start].islower():
                    lower_letters[s[start]] -= 1
                else:
                    upper_letters[s[start]] -= 1
                if s[end].islower():
                    lower_letters[s[end]] += 1
                else:
                    upper_letters[s[end]] += 1
                start += 1
                end += 1
        return s[start: end]


class Solution2:
    @staticmethod
    def longest_nice_substring(s: str) -> str:
        def h(i, j):
            if i >= j: return ''
            k = next((
                k_ for k_, c in enumerate(s[i:j], start=i)
                if c.islower() and c.upper() not in s[i:j] or c.isupper() and c.lower() not in s[i:j]
            ), None)
            if k is None:
                return s[i:j]
            else:
                return max(h(i, k), h(k + 1, j), key=len)

        return h(0, len(s))
