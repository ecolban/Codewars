from itertools import chain, cycle


def rail_index_generator(k):
    return cycle(chain(range(0, k - 1), range(k - 1, 0, -1)))


def encode_rail_fence_cipher(s, k):
    g = rail_index_generator(k)
    return ''.join(sorted(s, key=lambda c: next(g)))


def decode_rail_fence_cipher(s, k):
    g = rail_index_generator(k)
    indexes = iter(sorted(range(len(s)), key=lambda i: next(g)))
    return ''.join(sorted(s, key=lambda c: next(indexes)))


if __name__ == '__main__':
    s = encode_rail_fence_cipher('We are discovered. Flee at once!', 3)
    print(s)
    print(decode_rail_fence_cipher(s, 3))
