from random import shuffle
from collections import Counter

from cards import Scout, Viper
from util import move_list_contents, move_list_item
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
            deck.append(Scout())
        for _ in range(2):
            deck.append(Viper())
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
        move_list_contents(self[Zones.DISCARD], self[Zones.DECK])
        shuffle(self[Zones.DECK])

    def draw(self, n=5):
        for i in range(n):
            try:
                card = self[Zones.DECK].pop(0)
            except IndexError:
                self.shuffle_deck()
                card = self[Zones.DECK].pop(0)
            self[Zones.HAND].append(card)

    def start_turn(self):
        for base in self[Zones.IN_PLAY]:
            base.initialize_in_play()

    def end_turn(self):
        self[ValueTypes.DAMAGE] = 0
        self[ValueTypes.TRADE] = 0
        self.active_factions.clear()

        ships = []
        for card in self[Zones.IN_PLAY]:
            card.deinitialize_from_play()
            if card.is_ship():
                ships.append(card)
        for ship in ships:
            move_list_item(ship, self[Zones.IN_PLAY], self[Zones.DISCARD])

        try:
            self.draw(5)
        except IndexError:
            assert len(self[Zones.DECK]) + len(self[Zones.DISCARD]) == 0

    def destroy_base(self, base):
        base.deinitialize_from_play()
        move_list_item(base, self[Zones.IN_PLAY], self[Zones.DISCARD])
