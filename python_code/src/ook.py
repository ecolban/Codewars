TRANSLATION_TABLE = {ord(k): ord(v) for k, v in (('O', '0'), ('o', '0'), ('K', '1'), ('k', '1'))}


def okkOokOo(s):
    letters = s.split('? ')
    res = ''.join((decode(letter) for letter in letters))
    return res


def decode(letter):
    binary = ''.join(letter.split(', ')).translate(TRANSLATION_TABLE).replace('!', '')
    res = chr(int(binary, 2))
    return res


if __name__ == '__main__':
    print(TRANSLATION_TABLE)
    assert okkOokOo('Ok, Ook, Ooo!') == 'H'
    assert okkOokOo('Ok, Ook, Ooo?  Okk, Ook, Ok?  Okk, Okk, Oo?  Okk, Okk, Oo?  Okk, Okkkk!') == 'Hello'
    assert okkOokOo('Ok, Ok, Okkk?  Okk, Okkkk?  Okkk, Ook, O?  Okk, Okk, Oo?  Okk, Ook, Oo?  Ook, Ooook!') == 'World!'
