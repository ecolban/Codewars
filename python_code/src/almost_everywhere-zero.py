from scipy.special import comb


def almost_everywhere_zero(n, k):
    def h(s, k):
        s = s.lstrip('0')
        return 1 if k == 0 \
            else 0 if len(s) < k \
            else comb(len(s), k, exact=True) * pow(9, k) if all(d == '9' for d in s) \
            else h(s[1:], k - 1) + h(str(int(s[0]) - 1) + '9' * (len(s) - 1), k)

    return h(str(n), k)


if __name__ == '__main__':
    print(almost_everywhere_zero(10001, 2))
