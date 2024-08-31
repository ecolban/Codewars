from random import randrange

from unfinished_game import divide_pot4 as divide_pot
# from unfinished_game_lachesism import divide_pot as divide_pot
# from unfinished_game_dfhwze import divide_pot as divide_pot
from unfinished_game_dfhwze import divide_pot as divide_pot_ref


def test_simple_cases():
    assert divide_pot(3, [1, 0]) == [11, 5]
    assert divide_pot(3, [2, 0]) == [7, 1]
    assert divide_pot(3, [2, 1]) == [3, 1]
    assert divide_pot(3, [0, 0, 0]) == [1, 1, 1]
    assert divide_pot(3, [0, 0, 1]) == [55, 55, 133]
    assert divide_pot(3, [0, 0, 2]) == [8, 8, 65]
    assert divide_pot(3, [0, 1, 1]) == [13, 34, 34]
    assert divide_pot(3, [0, 1, 2]) == [2, 6, 19]
    assert divide_pot(3, [0, 2, 2]) == [1, 13, 13]
    assert divide_pot(3, [1, 1, 2]) == [5, 5, 17]
    assert divide_pot(3, [1, 2, 2]) == [1, 4, 4]
    assert divide_pot(4, [1, 2, 2, 1]) == [541, 1507, 1507, 541]
    assert divide_pot(5, [1, 1, 2, 0, 2]) == [172086568, 172086568, 403132603, 70264783, 403132603]
    assert divide_pot(6, [1, 2, 4, 0, 1]) == [9252454862, 21634178542, 108637864327, 3810938032, 9252454862]


def batch(rounds_to_win, num_players, num_tests):
    for _ in range(num_tests):
        wins = [randrange(rounds_to_win // 2, rounds_to_win) for _ in range(num_players)]
        actual = divide_pot(rounds_to_win, wins.copy())
        expected = divide_pot_ref(rounds_to_win, wins)
        assert actual == expected


def test_few_players_few_rounds():
    batch(4, 2, 100)


def test_few_players_many_rounds():
    batch(100, 2, 30)
    batch(100, 3, 30)


def test_many_players_few_rounds():
    batch(7, 8, 50)
    batch(6, 9, 25)
    batch(5, 10, 25)
