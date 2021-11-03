def roblox1(nums):
    # if 0 not in (a, b, c): b / a ==  c / b <==> a / b ==  b / c  <==> a * c == b * b
    return [a * c == b * b for a, b, c in zip(nums, nums[1:], nums[2:])]


def roblox2(histo):
    s, m = [(0, 0)], 0
    histo.append(0)
    for i, h in enumerate(histo):
        j = i
        while s[-1][1] > h:
            j, h2 = s.pop()
            m = max(m, min(i - j, h2))
        if h > s[-1][1]:
            s.append((j, h))
    return m * m


if __name__ == '__main__':
    print(roblox1([1, 2, 4, 5, 35, 245, 49, 14, 4, 6, 12, 24, 48, 12, 3]))
    print(roblox1([1, 2, 4] * 10))
    print(roblox1([0, 0, 0]))
    print(roblox2([1, 2, 4, 7, 3, 6, 4, 6, 6, 5, 8, 10]))
    print(roblox2([10] * 11))
