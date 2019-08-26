def next_smaller(n):
    digits = list(str(n))
    k1 = next((i for i in range(len(digits) - 2, -1, -1) if digits[i] > digits[i + 1]), -1)
    if k1 < 0:
        return -1
    k2 = next(i for i in range(len(digits) - 1, k1, -1) if digits[i] < digits[k1])
    if k1 == 0 and digits[k2] == '0':
        return -1
    digits[k1], digits[k2] = digits[k2], digits[k1]
    digits[k1 + 1:] = reversed(digits[k1 + 1:])
    return int(''.join(digits))


if __name__ == "__main__":
    print(8888, next_smaller(8888))
    print(12333345556778999, next_smaller(12333345556778999))
    print(10127, next_smaller(10127))
    print(2390127, next_smaller(2390127))
    print(90127, next_smaller(90127))
    print(110127, next_smaller(110127))
    print(10101111, next_smaller(10101111))
