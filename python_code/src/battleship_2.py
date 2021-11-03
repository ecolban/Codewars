from copy import deepcopy


def possible_placements(field_in, ship_size):
    for r in range(10):
        for c in range(11 - ship_size):
            if all(field_in[r][c_] for c_ in range(c, c + ship_size)):
                placement = [(r, c_) for c_ in range(c, c + ship_size)]
                field_out = deepcopy(field_in)
                for r, c_ in placement:
                    field_out[r][c_] = 0
                yield placement, field_out
    for r in range(11 - ship_size):
        for c in range(10):
            if all(field_in[r_][c] for r_ in range(r, r + ship_size)):
                placement = [(r_, c) for r_ in range(r, r + ship_size)]
                field_out = deepcopy(field_in)
                for r_, c in placement:
                    field_out[r_][c] = 0
                yield placement, field_out


def validate_battlefield(battlefield):
    if sum(sum(row) for row in battlefield) != 20:
        return False
    for pl1, bf1 in possible_placements(battlefield, 4):
        for pl2, bf2 in possible_placements(bf1, 3):
            for pl3, bf3 in possible_placements(bf2, 3):
                for pl4, bf4 in possible_placements(bf3, 2):
                    for pl5, bf5 in possible_placements(bf4, 2):
                        if next(possible_placements(bf5, 2), None):
                            return True
    return False


if __name__ == '__main__':
    battlefield = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1, 1]]


    print(validate_battlefield(battlefield))
