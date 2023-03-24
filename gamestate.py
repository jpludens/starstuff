import logging
from random import shuffle

from enums import PlayerIndicators, Zones
from playerstate import PlayerState
from decks import get_fresh_trade_deck


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class GameState(object):
    def __init__(self, p1_name, p2_name):
        self.players = {
            PlayerIndicators.ACTIVE: PlayerState(name=p1_name, first_player=True),
            PlayerIndicators.INACTIVE: PlayerState(name=p2_name, first_player=False)}

        self.trade_deck = get_fresh_trade_deck()
        shuffle(self.trade_deck)

        self.trade_row = []
        self.fill_trade_row()

        self.turn_number = 1

    def __getitem__(self, key):
        if isinstance(key, PlayerIndicators):
            return self.players[key]
        elif key == Zones.TRADE_ROW:
            return self.trade_row
        elif key == Zones.TRADE_DECK:
            return self.trade_deck

    def fill_trade_row(self):
        cards_in_row = len(self.trade_row)
        empty_slots = 5 - cards_in_row
        new_cards = self.trade_deck[:empty_slots]
        for new_card in new_cards:
            logging.warning("Trade Row: {} added".format(new_card.name))
            self.trade_row.append(new_card)
        self.trade_deck[:empty_slots] = []

    def next_turn(self):
        self[PlayerIndicators.ACTIVE].end_turn()

        self.turn_number += 1
        next_player = self[PlayerIndicators.INACTIVE]
        self.players[PlayerIndicators.INACTIVE] = self[PlayerIndicators.ACTIVE]
        self.players[PlayerIndicators.ACTIVE] = next_player

        self[PlayerIndicators.ACTIVE].start_turn()
