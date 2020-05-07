def longest_palindrome(s):
    """
    # Find the longest palindromic substring in s. If there are multiple such palindromic substrings,
    # the first occurrence is returned.
    # :param s: input string
    # :return: The longest palindromic substring of s
    >>> longest_palindrome('abaabxxbaabc')
    'baabxxbaab'
    >>> longest_palindrome('addis ababa')
    'ababa'
    >>> longest_palindrome('abb')
    'bb'
    >>> longest_palindrome('bananas')
    'anana'
    >>> len(longest_palindrome('a' * 100_000))
    100000
    """

    # s_sep = '_' + '_'.join(s) + '_' (s_sep[i] = '_' if i % 2 == 0 else s[i >> 1])
    n = 2 * len(s) + 1  # n = len(s_sep)
    r = [0] * n
    start = ctr = end = 0
    while end < n - 1:
        # Loop invariant:
        # ctr is the index some character in s_sep
        # start is the index of first character in s_sep of the longest palindrome centered at ctr
        # end is the index of last character in s_sep of the longest palindrome centered at ctr
        # r[k] == radius of longest palindromic substring of s_sep centered in k, for 0 <= k <= ctr
        i, j = ctr - 1, ctr + 1
        while j <= end and r[i] != end - j:
            r[j] = min(r[i], end - j)
            i, j = i - 1, j + 1
        ctr, end = j, max(end, j)
        start = ctr - (end - ctr)
        while start & 1 or 0 < start and end < n - 1 and s[(start >> 1) - 1] == s[end >> 1]:
            start, end = start - 1, end + 1
        r[ctr] = end - ctr
    max_ctr = max(range(n), key=lambda k: r[k])
    return s[max_ctr - r[max_ctr] >> 1: max_ctr + r[max_ctr] >> 1]
