from collections import defaultdict
from itertools import combinations, product
from random import shuffle, sample

CARDS = [
    ("DAISY", "G-KEY", "KEY", "PADLOCK", "TAXI", "EXCLAMATION MARK", "ANCHOR", "LIPS"),
    ("GHOST", "DOLPHIN", "DINOSAUR", "ART", "OK", "APPLE", "LADYBUG", "ANCHOR"),
    ("QUESTION MARK", "OK", "TREE", "KEY", "SPIDER", "KNIGHT", "SKULL", "BOTTLE"),
    ("KNIGHT", "CLOVER", "G-KEY", "SNOWMAN", "DROP", "SCISSORS", "GHOST", "HEART"),
    ("FIRE", "IGLOO", "CHEESE", "SNOWMAN", "TAXI", "BOTTLE", "DOLPHIN", "SPOTS"),
    ("TAXI", "CANDLE", "DRAGON", "DROP", "SPIDER", "COBWEB", "ICE CUBE", "LADYBUG"),
    ("CANDLE", "ANCHOR", "GINGERBREAD MAN", "SKULL", "SNOWFLAKE", "CLOVER", "HAND", "SPOTS"),
    ("SPIDER", "FIRE", "DINOSAUR", "ZEBRA", "CARROT", "PADLOCK", "EYE", "CLOVER"),
    ("DOLPHIN", "DOG", "SHADES", "DAISY", "SNOWFLAKE", "TREE", "DROP", "CARROT"),
    ("MOON", "SKULL", "DRAGON", "CAT", "CHEESE", "G-KEY", "SHADES", "DINOSAUR"),
    ("BOTTLE", "APPLE", "DAISY", "BALLOON", "STOP", "CLOVER", "YING-YANG", "DRAGON"),
    ("YING-YANG", "CHEESE", "GHOST", "CACTUS", "HAND", "DOG", "LIPS", "SPIDER"),
    ("BOMB", "COBWEB", "PADLOCK", "APPLE", "HAND", "TREE", "SNOWMAN", "CAT"),
    ("EYE", "HAND", "DOLPHIN", "KEY", "MAPLE LEAF", "HEART", "TARGET", "DRAGON"),
    ("FIRE", "GINGERBREAD MAN", "COBWEB", "HEART", "YING-YANG", "SHADES", "OK", "EXCLAMATION MARK"),
    ("ART", "DAISY", "SPOTS", "CAT", "LIGHT BULB", "SPIDER", "HEART", "CLOCK"),
    ("LIGHTNING BOLT", "DAISY", "OK", "CHEESE", "SCISSORS", "EYE", "BOMB", "CANDLE"),
    ("ICE CUBE", "PADLOCK", "CLOCK", "SKULL", "SCISSORS", "YING-YANG", "CLOWN", "DOLPHIN"),
    ("PENCIL", "SNOWMAN", "OK", "DRAGON", "LIPS", "CLOCK", "SNOWFLAKE", "ZEBRA"),
    ("EYE", "QUESTION MARK", "ANCHOR", "DROP", "PENCIL", "CAT", "YING-YANG", "IGLOO"),
    ("CAT", "TAXI", "SUN", "OK", "CLOWN", "DOG", "CLOVER", "MAPLE LEAF"),
    ("MOON", "CANDLE", "CARROT", "SNOWMAN", "KEY", "SUN", "ART", "YING-YANG"),
    ("G-KEY", "PENCIL", "DOLPHIN", "GINGERBREAD MAN", "SPIDER", "SUN", "STOP", "BOMB"),
    ("PENCIL", "FIRE", "KNIGHT", "LADYBUG", "HAND", "DAISY", "CLOWN", "MOON"),
    ("GINGERBREAD MAN", "CARROT", "SCISSORS", "LADYBUG", "TARGET", "BOTTLE", "CAT", "LIPS"),
    ("SPIDER", "IGLOO", "SCISSORS", "APPLE", "MAPLE LEAF", "EXCLAMATION MARK", "MOON", "SNOWFLAKE"),
    ("BALLOON", "LADYBUG", "SNOWFLAKE", "SUN", "HEART", "CHEESE", "QUESTION MARK", "PADLOCK"),
    ("LIPS", "TREE", "STOP", "IGLOO", "HEART", "CLOWN", "DINOSAUR", "CANDLE"),
    ("CARROT", "HEART", "SKULL", "APPLE", "PENCIL", "LIGHTNING BOLT", "CACTUS", "TAXI"),
    ("DROP", "EXCLAMATION MARK", "DINOSAUR", "SUN", "HAND", "LIGHTNING BOLT", "CLOCK", "BOTTLE"),
    ("BOMB", "CARROT", "SPOTS", "GHOST", "CLOWN", "DRAGON", "QUESTION MARK", "EXCLAMATION MARK"),
    ("DINOSAUR", "LIGHT BULB", "BOMB", "SNOWFLAKE", "TAXI", "TARGET", "YING-YANG", "KNIGHT"),
    ("ANCHOR", "BALLOON", "CLOWN", "SNOWMAN", "SPIDER", "TARGET", "SHADES", "LIGHTNING BOLT"),
    ("SPOTS", "KNIGHT", "SHADES", "SUN", "EYE", "APPLE", "LIPS", "ICE CUBE"),
    ("FIRE", "ICE CUBE", "SNOWFLAKE", "STOP", "KEY", "LIGHTNING BOLT", "CAT", "GHOST"),
    ("BOTTLE", "GHOST", "PADLOCK", "SHADES", "PENCIL", "MAPLE LEAF", "CANDLE", "LIGHT BULB"),
    ("EYE", "GINGERBREAD MAN", "GHOST", "TAXI", "CLOCK", "BALLOON", "MOON", "TREE"),
    ("YING-YANG", "TREE", "LADYBUG", "MAPLE LEAF", "SPOTS", "G-KEY", "ZEBRA", "LIGHTNING BOLT"),
    ("IGLOO", "LIGHT BULB", "OK", "HAND", "ICE CUBE", "BALLOON", "CARROT", "G-KEY"),
    ("LIGHT BULB", "APPLE", "GINGERBREAD MAN", "CLOWN", "CHEESE", "DROP", "ZEBRA", "KEY"),
    ("CHEESE", "ART", "TARGET", "CLOVER", "EXCLAMATION MARK", "PENCIL", "ICE CUBE", "TREE"),
    ("KNIGHT", "DRAGON", "DOG", "IGLOO", "ART", "PADLOCK", "GINGERBREAD MAN", "LIGHTNING BOLT"),
    ("EXCLAMATION MARK", "ZEBRA", "KNIGHT", "DOLPHIN", "BALLOON", "CANDLE", "CACTUS", "CAT"),
    ("TARGET", "SPOTS", "OK", "CACTUS", "STOP", "DROP", "PADLOCK", "MOON"),
    ("TARGET", "FIRE", "QUESTION MARK", "CANDLE", "CLOCK", "APPLE", "G-KEY", "DOG"),
    ("COBWEB", "CLOWN", "ART", "BOTTLE", "CACTUS", "G-KEY", "SNOWFLAKE", "EYE"),
    ("HEART", "DOG", "ANCHOR", "BOMB", "MOON", "ZEBRA", "BOTTLE", "ICE CUBE"),
    ("DRAGON", "FIRE", "ANCHOR", "CACTUS", "SUN", "SCISSORS", "TREE", "LIGHT BULB"),
    ("MAPLE LEAF", "STOP", "CARROT", "KNIGHT", "CHEESE", "CLOCK", "ANCHOR", "COBWEB"),
    ("DOG", "PENCIL", "SCISSORS", "COBWEB", "KEY", "BALLOON", "SPOTS", "DINOSAUR"),
    ("CLOVER", "LIGHT BULB", "COBWEB", "MOON", "LIPS", "LIGHTNING BOLT", "DOLPHIN", "QUESTION MARK"),
    ("QUESTION MARK", "STOP", "HAND", "ZEBRA", "SHADES", "ART", "SCISSORS", "TAXI"),
    ("BOMB", "BALLOON", "LIPS", "SKULL", "DROP", "ART", "MAPLE LEAF", "FIRE"),
    ("GHOST", "IGLOO", "SUN", "COBWEB", "SKULL", "DAISY", "ZEBRA", "TARGET"),
    ("CLOVER", "KEY", "CACTUS", "LADYBUG", "CLOCK", "IGLOO", "SHADES", "BOMB"),
    # ("CACTUS", "DAISY", "DINOSAUR", "GINGERBREAD MAN", "ICE CUBE", "MAPLE LEAF", "QUESTION MARK", "SNOWMAN"),
    # ("DOG", "EXCLAMATION MARK", "EYE", "LADYBUG", "LIGHT BULB", "SKULL", "SNOWMAN", "STOP"),
]


def get_cards():
    figures = [
        "ANCHOR", "APPLE", "ART", "BALLOON", "BOMB", "BOTTLE", "CACTUS", "CANDLE", "CARROT", "CAT", "CHEESE",
        "CLOCK", "CLOVER", "CLOWN", "COBWEB", "DAISY", "DINOSAUR", "DOG", "DOLPHIN", "DRAGON", "DROP",
        "EXCLAMATION MARK", "EYE", "FIRE", "GHOST", "GINGERBREAD MAN", "G-KEY", "HAND", "HEART", "ICE CUBE",
        "IGLOO", "KEY", "KNIGHT", "LADYBUG", "LIGHT BULB", "LIGHTNING BOLT", "LIPS", "MAPLE LEAF", "MOON",
        "OK", "PADLOCK", "PENCIL", "QUESTION MARK", "SCISSORS", "SHADES", "SKULL", "SNOWFLAKE", "SNOWMAN",
        "SPIDER", "SPOTS", "STOP", "SUN", "TARGET", "TAXI", "TREE", "YING-YANG", "ZEBRA"
    ]
    shuffle(figures)
    gf = range(7)
    points = product(gf, gf)  # [(x, y) for x in gf for y in gf]
    directions = [(1, b) for b in gf] + [(0, 1)]
    lines = [(a, b, c) for a, b in directions for c in gf]
    figure_map = {line: fig for line, fig in zip(lines, figures)}
    cards_affine = [tuple(figure_map[(a, b, -(a * x + b * y) % 7)] for a, b in directions)
                    for x, y in points]
    line_at_infinity = figures[-1]
    cards_at_infinity = [(*(figure_map[(a, b, c)] for c in gf), line_at_infinity)
                         for a, b in directions]
    return cards_affine + cards_at_infinity


def missing_cards(cards):
    line_map = defaultdict(set)
    for card in cards:
        for figure in card:
            line_map[figure].add(frozenset(card))
    figures = line_map.keys()
    res = {frozenset(figures - {figure for card in card_set for figure in card if figure != line})
           for line, card_set in line_map.items() if len(card_set) == 7}
    return [tuple(card) for card in res]


if __name__ == "__main__":
    assert len(CARDS) == 55
    # assert len(CARDS) == 57
    assert len({fig for card in CARDS for fig in card}) == 57
    assert all(len(card) == 8 for card in CARDS)
    assert all(len(set(card)) == 8 for card in CARDS)
    assert all(len(set(card1) & set(card2)) == 1 for card1, card2 in combinations(CARDS, 2))
    expected = [
        ["CACTUS", "DAISY", "DINOSAUR", "GINGERBREAD MAN", "ICE CUBE", "MAPLE LEAF", "QUESTION MARK", "SNOWMAN"],
        ["DOG", "EXCLAMATION MARK", "EYE", "LADYBUG", "LIGHT BULB", "SKULL", "SNOWMAN", "STOP"],
    ]
    assert sorted(sorted(card) for card in missing_cards(CARDS)) == expected
    assert all(len(set(card1) & set(card2)) == 1 for card1, card2 in combinations(CARDS + expected, 2))
    print("Random test")
    new_cards = get_cards()
    missing = sorted(sample(new_cards, 2))
    for card in missing:
        print(tuple(sorted(card)))
        new_cards.remove(card)
    for card in (tuple(sorted(card)) for card in missing_cards(new_cards)):
        print(card)
