from random import shuffle

from cards import Scout, Viper, Explorer
from util import move_list_contents
from enums import *


class Player(object):
    def __init__(self, name, strategy, state=None):
        self.name = name
        self.strategy = strategy
        self.state = state

    def get_moves(self, gamestate):
        assert gamestate.active_player is self
        return self.strategy.get_moves(gamestate)


class PlayerState(object):
    def __init__(self, first_player=False):
        self.values = {
            AUTHORITY: 50,
            TRADE: 0,
            DAMAGE: 0
        }

        self.zones = {
            DECK: [Scout] * 8 + [Viper] * 2,
            HAND: [],
            IN_PLAY: [],
            DISCARD: []
        }
        self._deck = self.zones[DECK]
        self._hand = self.zones[HAND]
        self._play = self.zones[IN_PLAY]
        self._discard = self.zones[DISCARD]

        shuffle(self.zones[Zones.DECK])
        self.draw(3 if first_player else 5)

    def shuffle_deck(self):
        assert len(self._deck) == 0
        move_list_contents(self._discard, self._deck)
        shuffle(self._deck)

    def draw(self, n=5):
        for i in range(n):
            try:
                card = self._deck.pop(0)
            except IndexError:
                self.shuffle_deck()
                try:
                    card = self._deck.pop(0)
                except IndexError:
                    return
            self._hand.append(card)

    def end_turn(self):
        self.values[Values.DAMAGE] = 0
        self.values[Values.TRADE] = 0
        move_list_contents(self._hand, self._discard)
        move_list_contents(self._play, self._discard)
        self.draw(5)

    def count_explorers(self):
        return sum([zone.count(Explorer) for zone in self.zones.values()])
