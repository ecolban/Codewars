from unittest import TestCase

from src.dobbel import get_cards


class TestDobbel(TestCase):

    def testCards(self):
        cards = get_cards(7)
        self.assertEqual(len(cards), 57)
        self.assertTrue(all(len(card) == 8 for card in cards))
        self.assertTrue(all(len(set(card)) == 8 for card in cards))
        self.assertEqual(len(set.union(*(set(card) for card in cards))), 57)
        card_list = list(cards)
        # for i in range(1, len(card_list)):
        #     for j in range(i):
        #         self.assertEqual(set(card_list[i]) & set(card_list[j]), 1)
        self.assertTrue(all(len(set(card1) & set(card2)) == 1
                            for i, card1 in enumerate(card_list[1:])
                            for card2 in card_list[:i]))
