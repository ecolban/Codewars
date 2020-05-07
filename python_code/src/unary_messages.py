from itertools import groupby, chain


def send(s):
    bits = chain.from_iterable(f'{ord(c) :0>7b}' for c in s)
    return ' '.join(f"{'00' if k == '0' else '0'} {''.join('0' for _ in g)}" for k, g in groupby(bits))


def receive(s):
    it = iter(s.split())
    bits = chain.from_iterable(('0' if a == '00' else '1') * len(b) for a, b in zip(it, it))
    byte_seq = (''.join(chunk) for chunk in zip(*([bits] * 7)))
    return ''.join(chr(int(byte, 2)) for byte in byte_seq)


if __name__ == "__main__":
    message = send("Chuck Norris' keyboard has 2 keys: 0 and white space.")
    print(message)
    print(receive(message))
