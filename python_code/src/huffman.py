from collections import Counter
from heapq import heappop, heappush, heapify


def frequencies(s):
    return Counter(s).most_common()


def build_tree(freqs):
    if len(freqs) < 2: return None
    tree = [(f, i, c) for i, (c, f) in enumerate(freqs)]
    heapify(tree)
    while len(tree) > 1:
        (f1, i1, t1) = heappop(tree)
        (f2, i2, t2) = heappop(tree)
        t_new = (f1 + f2, i1, (t1, t2))
        heappush(tree, t_new)
    return tree[0][2] if tree else None


def build_dict(tree, path):
    if not tree: return None
    if isinstance(tree, str): return {tree: path}
    d = build_dict(tree[0], path + '0')
    d.update(build_dict(tree[1], path + '1'))
    return d


def encode(freqs, s):
    d = build_dict(build_tree(freqs), '')
    return ''.join(d[c] for c in s) if d else None


def decode(freqs, bits):
    d = build_dict(build_tree(freqs), '')
    d_inv = {v: k for k, v in d.items()}
    res = ''
    while bits:
        i = 1
        while bits[:i] not in d_inv:
            i += 1
        res += d_inv[bits[:i]]
        bits = bits[i:]
    return res


s = 'bsjezexfagstlmmbjbmnxttlzzmdnhuliekmwatjnyxtuograadbjscoqnvfdkdinfkcrrfiqzoyeoaplkokyly'
freqs = frequencies(s)
tree = build_tree(freqs)
d = build_dict(tree, '')
print('freqs = %s' % freqs)
print('tree = ' + str(tree))
print('d = %s' % d)
print(decode(freqs, encode(freqs, "hello")) == "hello")
s.index('h')

