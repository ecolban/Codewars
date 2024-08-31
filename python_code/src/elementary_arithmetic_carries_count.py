def solve(s):
    pairs = s.split('\n')
    return '\n'.join(count_carries(p.split()) for p in pairs)


def count_carries(p):
    carries = 0
    carry = 0
    s = zip(*map(reversed, p))
    for a, b in s:
        if int(a) + int(b) + carry > 9:
            carries += 1
            carry = 1
        else:
            carry = 0
    return 'No carry operation' if carries == 0 else f'{carries:d} carry operations'


if __name__ == '__main__':
    print(solve("123 456\n555 555\n123 594"))
