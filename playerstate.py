from random import shuffle
from collections import Counter

from cards import Scout, Viper
from util import move_list_item
from enums import ValueTypes, Zones


class PlayerState(object):
    def __init__(self, name="Unnamed Player", first_player=False):
        self.name = name

        self.values = {
            ValueTypes.AUTHORITY: 50,
            ValueTypes.TRADE: 0,
            ValueTypes.DAMAGE: 0
        }

        deck = []
        for _ in range(8):
            deck.append(Scout(owner_id=name, location=Zones.DECK))
        for _ in range(2):
            deck.append(Viper(owner_id=name, location=Zones.DECK))
        self.zones = {
            Zones.DECK: deck,
            Zones.HAND: [],
            Zones.IN_PLAY: [],
            Zones.DISCARD: []
        }

        self.active_factions = Counter()

        shuffle(self.zones[Zones.DECK])
        self.draw(3 if first_player else 5)

    # Allow dict-style access to values and zones
    def __getitem__(self, key):
        try:
            return self.values[key]
        except KeyError:
            return self.zones[key]

    # Allow dict-style access to values and zones
    def __setitem__(self, key, value):
        if key in self.values:
            self.values[key] = value
        elif key in self.zones:
            self.zones[key] = value
        else:
            raise KeyError

    def shuffle_deck(self):
        assert len(self[Zones.DECK]) == 0
        for card in list(self[Zones.DISCARD]):
            card.move_to(Zones.DECK)
            move_list_item(card, self[Zones.DISCARD], self[Zones.DECK])
        shuffle(self[Zones.DECK])

    def draw(self, n=5):
        for i in range(n):
            try:
                card = self[Zones.DECK].pop(0)
            except IndexError:
                self.shuffle_deck()
                card = self[Zones.DECK].pop(0)

            card.move_to(Zones.HAND)
            self[Zones.HAND].append(card)

    def start_turn(self):
        for base in self[Zones.IN_PLAY]:
            base.ready()

    def end_turn(self):
        self[ValueTypes.DAMAGE] = 0
        self[ValueTypes.TRADE] = 0
        self.active_factions.clear()

        ships = []
        for card in self[Zones.IN_PLAY]:
            if card.is_ship():
                ships.append(card)
            card.move_to(Zones.DISCARD)
        for ship in ships:
            move_list_item(ship, self[Zones.IN_PLAY], self[Zones.DISCARD])

        try:
            self.draw(5)
        except IndexError:
            assert len(self[Zones.DECK]) + len(self[Zones.DISCARD]) == 0
