from random import shuffle

from cards import Scout, Viper, Explorer
from util import move_list_contents, move_list_item
from enums import CardTypes, Values, Zones


class Player(object):
    def __init__(self, name, strategy, state=None):
        self.name = name
        self.strategy = strategy
        self.state = state

    def get_moves(self, gamestate):
        assert gamestate.active_player is self
        return self.strategy.get_moves(gamestate)

    # Allows dict-style access to "values" and "zones" in PlayerState
    def __getitem__(self, item):
        return self.state[item]

    # Allows dict-style access to "values" and "zones" in PlayerState
    def __setitem__(self, item, *args, **kwargs):
        return self.state.__setitem__(item, *args, **kwargs)


class PlayerState(object):
    def __init__(self, first_player=False):
        self.values = {
            Values.AUTHORITY: 50,
            Values.TRADE: 0,
            Values.DAMAGE: 0
        }

        self.zones = {
            Zones.DECK: [Scout()] * 8 + [Viper()] * 2,
            Zones.HAND: [],
            Zones.IN_PLAY: [],
            Zones.DISCARD: []
        }

        shuffle(self.zones[Zones.DECK])
        self.draw(3 if first_player else 5)

    # Allow dict-style access to values and zones
    def __getitem__(self, item):
        try:
            return self.values[item]
        except KeyError:
            return self.zones[item]

    # Allow dict-style access to values and zones
    # Presumes the key argument is an Enum value
    def __setitem__(self, key, *args, **kwargs):
        if key in self.values:
            self.values.__setitem__(key, *args, **kwargs)
        elif key in self.zones:
            raise KeyError  # this probably shouldn't happen
            # self.zones.__setitem__(item, *args, **kwargs)
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
                try:
                    card = self[Zones.DECK].pop(0)
                except IndexError:
                    return
            self[Zones.HAND].append(card)

    def end_turn(self):
        self[Values.DAMAGE] = 0
        self[Values.TRADE] = 0

        ships = []
        for card in self[Zones.IN_PLAY]:
            card.remove_from_play()
            if card.is_ship():
                ships.append(card)
        for ship in ships:
            move_list_item(ship, self[Zones.IN_PLAY], self[Zones.DISCARD])

        self.draw(5)

    def destroy_base(self, base):
        base.remove_from_play()
        move_list_item(base, self[Zones.IN_PLAY], self[Zones.DISCARD])

    def count_explorers(self):
        return sum([zone.count(Explorer) for zone in self.zones.values()])
