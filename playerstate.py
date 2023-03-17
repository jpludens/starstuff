from random import shuffle

from cards import Scout, Viper
from util import move_list_contents


class PlayerState(object):
    def __init__(self, first_player=False, name=None, strategy=None):
        self.name = name
        self.strategy = strategy
        self.opponent_state = None

        self.authority = 50

        # noinspection PyTypeChecker
        self.deck = [Scout] * 8 + [Viper] * 2
        shuffle(self.deck)

        self.hand = []
        self.draw(3 if first_player else 5)

        self.discard = []

        self.metrics = {}

    def shuffle_deck(self):
        assert len(self.deck) == 0
        move_list_contents(self.discard, self.deck)
        shuffle(self.deck)

    def draw(self, n=5):
        for i in range(n):
            try:
                card = self.deck.pop(0)
            except IndexError:
                self.shuffle_deck()
                try:
                    card = self.deck.pop(0)
                except IndexError:
                    return
            self.hand.append(card)

    def end_turn(self):
        move_list_contents(self.hand, self.discard)
        self.draw()
