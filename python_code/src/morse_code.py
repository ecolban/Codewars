import random
from collections import defaultdict

MORSE_CODE = {
    '.-': 'A',
    '-...': 'B',
    '-.-.': 'C',
    '-..': 'D',
    '.': 'E',
    '..-.': 'F',
    '--.': 'G',
    '....': 'H',
    '..': 'I',
    '.---': 'J',
    '-.-': 'K',
    '.-..': 'L',
    '--': 'M',
    '-.': 'N',
    '---': 'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.': 'R',
    '...': 'S',
    '-': 'T',
    '..-': 'U',
    '...-': 'V',
    '.--': 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z',
    '-----': '0',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '.-.-.-': '.',
    '--..--': ',',
    '..--..': '?',
    '.----.': "'",
    '-.-.--': '!',
    '-..-.': '/',
    '-.--.': '(',
    '-.--.-': ')',
    '.-...': '&',
    '---...': ':',
    '-.-.-.': ';',
    '-...-': '=',
    '.-.-.': '+',
    '-....-': '-',
    '..--.-': '_',
    '.-..-.': '"',
    '...-..-': '$',
    '.--.-.': '@',
    '...---...': 'SOS'
}

from itertools import groupby, count


def decodeBitsAdvanced(bits):
    bits = bits.strip('0')
    data = [len(list(bs)) for _, bs in groupby(bits)]
    centroids = k_clusters(data, 3)
    codes = (''.join(c for c in gen_morse_code(bits, 0, 0 + i)) for i in count())
    return next(code for code in codes if try_decode(code))


def try_decode(code):
    try:
        decodeMorse(code)
    except KeyError:
        return False
    else:
        return True


def gen_morse_code(bits, hi, lo):
    for b, bs in groupby(bits):
        le = len(list(bs))
        if b == '1':
            if le < lo:
                yield '.'
            else:
                yield '-'
        else:
            if lo <= le < hi:
                yield ' '
            elif hi <= le:
                yield '   '


def decodeMorse(morseCode):
    words = morseCode.split('  ')
    return " ".join(map(lambda w: "".join(map(lambda c: MORSE_CODE[c], w.split())), words)).strip()


def k_clusters(data, k):
    min_data = min(data)
    max_data = max(data)
    epsilon = 0.01
    centroids_next = [random.uniform(min_data, max_data) for _ in range(k)]
    centroids_prev = [c + 2 * epsilon for c in centroids_next]
    while any(abs(c2 - c1) > epsilon for c1, c2 in zip(centroids_prev, centroids_next)):
        centroids_prev = centroids_next
        d = defaultdict(list)
        for p in data:
            d[min(centroids_prev, key=lambda c: abs(p - c))].append(p)
        centroids_next = [sum(v) / len(v) for v in d.values() if v]
    centroids_next.sort()
    return centroids_next


if __name__ == '__main__':
    bits = '0000000011011010011100000110000001111110100111110011111100000000000' \
           '111011111111011111011111000000101100011111100000111110011101100000100000'
    morse_code = decodeBitsAdvanced(bits)
    print(decodeMorse(morse_code))
