def countOnes(start, end):
    if start > 0: return countOnes(0, end) - countOnes(0, start - 1)
    return sum((end >> (d + 1) << d) + max(0, (end & (2 << d) - 1) + 1 - (1 << d))
               for d in range((end + 1).bit_length())) if end > 1 else end


if __name__ == "__main__":
    for n in range(1, 10):
        print(f'{n}: {n.bit_length()} -- {countOnes(start=0, end=n)}')
