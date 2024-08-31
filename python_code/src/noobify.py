import re


def n00bify(text_in):
    text_out = text_in[:]
    substitutions = {
        r'too|to': '2', r'fore|for': '4', r'oo': '00', 'be': 'b', 'are': 'r', 'you': 'u', 'please': 'plz',
        'people': 'ppl', 'really': 'rly', 'have': 'haz', 'know': 'no', "[.,']": '', 's': 'z'
    }
    for w, s in substitutions.items():
        text_out = re.sub(w, s, text_out, flags=re.IGNORECASE)

    words_in = text_in.split()
    words_out = [list(w) for w in text_out.split()]

    for wi, wo in zip(words_in, words_out):
        if wi[0].isupper():
            wo[0].upper()

    lol_added = False
    if words_out[0][0] in ('w', 'W'):
        words_out = [list('LOL')] + words_out
        lol_added = True
    if sum(len(w) for w in words_out) + len(words_out) - sum(1 for c in text_out if c in '.!?') - 1 >= 32:
        if lol_added:
            words_out = [list('LOL'), list('OMG')] + words_out[1:]
        else:
            words_out = [list('OMG')] + words_out

    for i, w in enumerate(words_out):
        if i % 2 == 1 or words_out[0][0] in ('h', 'H'):
            words_out[i] = [c.upper() for c in words_out[i]]

    for w in words_out:
        if w[-1] == '?':
            for _ in range(len(words_out) - 1):
                w.append('?')
        elif w[-1] == '!':
            for i in range(len(words_out) - 1):
                w.append('1' if i % 2 == 0 else '!')

    return ' '.join(''.join(word) for word in words_out)


if __name__ == '__main__':
    res = n00bify('Hi, how are you TODAY?')
    print(res)
    res = n00bify('I think it would be nice if we could all get along.')
    print(res)
    res = n00bify("Let's eat, Grandma!")
    print(res)
