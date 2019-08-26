from itertools import combinations


def get_cards(p):
    """p must be prime."""
    gf = range(p)
    points = {(x, y) for x in gf for y in gf}
    directions = {(1, y) for y in gf} | {(0, 1)}
    lines = {(a, b, c) for (a, b) in directions for c in gf}
    line_nums = {line: i for i, line in enumerate(lines, start=1)}
    cards_fin = {tuple(line_nums[(a, b, -(a * x + b * y) % p)] for (a, b) in directions) for (x, y) in points}
    line_inf = len(lines) + 1
    cards_inf = {tuple(line_nums[(a, b, c)] for c in gf) + (line_inf,) for (a, b) in directions}
    return cards_fin | cards_inf


def test_get_cards():
    cards = get_cards(7)
    images = {image for card in cards for image in card}
    print('Number of cards is ' + str(len(cards)))
    print('Number of images is ' + str(len(images)))
    if all(len(card) == 8 for card in cards):
        print("All cards have 8 images, and ...")
    if all(len(set(card)) == 8 for card in cards):
        print("... the 8 images are distinct.")
    if all(len(set(c1) & set(c2)) == 1 for c1, c2 in combinations(cards, 2)):
        print("Any two cards have exactly one image in common.")


if __name__ == "__main__":
    test_get_cards()
