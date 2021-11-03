class RegExp:
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        args = ", ".join(map(repr, self.args))
        return f"{self.__class__.__name__}({args})"

    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args


class Any(RegExp): pass


class Normal(RegExp): pass


class Or(RegExp): pass


class Str(RegExp): pass


class ZeroOrMore(RegExp): pass


"""
Regex      ==> Orex
Orex       ==> Seq ( '|' Seq )?
Seq        ==> (Term '*'?)+
Term       ==> '(' Orex ')' | '.' | Other
"""


def parse_regexp(regex):
    tokens = tuple(regex)
    try:
        res, i = parse_orex(tokens, start=0)
        assert i == len(tokens)
    except AssertionError:
        return None
    return res


def parse_orex(tokens, start):
    res, i = parse_seq(tokens, start)
    if i < len(tokens) and tokens[i] == '|':
        b, i = parse_seq(tokens, start=i + 1)
        return Or(res, b), i
    return res, i


def parse_seq(tokens, start):
    res, i = [], start
    while i < len(tokens) and tokens[i] not in ")|*":
        a, i = parse_term(tokens, i)
        if i < len(tokens) and tokens[i] == '*':
            a, i = ZeroOrMore(a), i + 1
        res.append(a)
    assert len(res) > 0
    return res[0] if len(res) == 1 else Str(res), i


def parse_term(tokens, start):
    c = tokens[start]
    if c == '(':
        res, i = parse_orex(tokens, start + 1)
        assert i < len(tokens) and tokens[i] == ')'
        return res, i + 1
    if c == '.':
        return Any(), start + 1
    return Normal(c), start + 1


if __name__ == '__main__':
    print(parse_regexp('(b*(.*)(.*))'))

