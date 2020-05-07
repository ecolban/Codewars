import re


def is_sum_of_cubes_(s):
    # extract digits and spaces
    s = "".join([c for c in s if '0' <= c <= '9' or c == ' ']).strip().replace("  ", " ")

    def chunk(string):
        for i in range(0, len(string), 3):
            yield string[i:i + 3]

    result, total = [], 0
    for number in s.split(" "):
        for num in chunk(number):
            n = int(num)
            magic = sum([int(d) ** 3 for d in num])
            if n == magic:
                result.append(num)
                total += n

    if len(result) > 0:
        return " ".join(result) + " {} Lucky".format(total)
    return "Unlucky"


def is_sum_of_cubes(s):
    cubes = {0, 1, 153, 370, 371, 407}
    res = [int(n) for n in re.findall(r'\d{1,3}', s) if int(n) in cubes]
    return f"{' '.join(map(str, res))} {sum(res)} Lucky" if res else "Unlucky"


if __name__ == "__main__":
    print(is_sum_of_cubes("000001"))
