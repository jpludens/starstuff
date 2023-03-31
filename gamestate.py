import logging
from itertools import cycle
from random import shuffle

from cards import Explorer
from enums import Zones
from playerstate import PlayerState
from decks import get_fresh_trade_deck


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class GameState(object):
    def __init__(self, p1_name, p2_name):
        player1 = PlayerState(name=p1_name, first_player=True)
        player2 = PlayerState(name=p2_name, first_player=False)
        self.players = {
            p1_name: player1,
            p2_name: player2}

        self.trade_deck = get_fresh_trade_deck()
        shuffle(self.trade_deck)

        self.trade_row = []
        self.fill_trade_row()

        self.turn_number = 1
        self._turn_order = cycle([player1, player2])
        self.active_player = next(self._turn_order)
        self.opponent = player2

        self.victor = None
        self.pending_effects = []

        # Hacky? Yes! Works? Yes!
        self.forced_discards = 0
        self.last_activated_card = None
        self.blob_cards_played_this_turn = 0
        self.freighter_hauls = 0

    def __getitem__(self, key):
        try:
            return self.players[key]
        except KeyError:
            try:
                # This allows player-state access without a player id, but only to the active player.
                # This works untless we need to start accessing the inactive player's stuff,
                return self.active_player[key]
            except KeyError:
                if key == Zones.TRADE_ROW:
                    return self.trade_row
                elif key == Zones.TRADE_DECK:
                    return self.trade_deck
                elif isinstance(key, tuple):  # Ensure old (player, zone) key strategy isn't in use
                    raise RuntimeError

    def remove_from_trade_row(self, card):
        try:
            self.trade_row.remove(card)
        except ValueError:
            if not isinstance(card, Explorer):
                raise
        self.fill_trade_row()

    def fill_trade_row(self):
        cards_in_row = len(self.trade_row)
        empty_slots = 5 - cards_in_row
        new_cards = self.trade_deck[:empty_slots]
        if new_cards:
            for new_card in new_cards:
                logging.warning("Trade Row: {} added".format(new_card.name))
                new_card.move_to(Zones.TRADE_ROW)
                self.trade_row.append(new_card)
        else:
            logging.warning("Trade Row: Empty!")

        self.trade_deck[:empty_slots] = []

    def next_turn(self):
        self.active_player.end_turn()  # The King is dead.
        self.turn_number += 1
        self.blob_cards_played_this_turn = 0
        self.opponent = self.active_player
        self.active_player = next(self._turn_order)
        self.active_player.start_turn()  # Long live the King!
