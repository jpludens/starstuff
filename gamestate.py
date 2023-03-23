import logging
from enums import Abilities, Actions, CardAttrs, Values, Zones
from random import shuffle
from util import move_list_item
from playerstate import Player, PlayerState
from cards import Explorer, PlayedCard
from decks import get_fresh_trade_deck


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class GameState(object):
    def __init__(self, alice_strategy, bob_strategy):
        # Create players
        self.alice = Player("Alice", alice_strategy, PlayerState(first_player=True))
        self.bob = Player("Bob", bob_strategy, PlayerState(first_player=False))

        # Set up Trade Deck
        self.trade_deck = get_fresh_trade_deck()
        shuffle(self.trade_deck)
        self.trade_row = []
        self._fill_trade_row()

        # Set up for Turn 1
        self.turn_number = 1
        self.active_player = self.alice
        self.inactive_player = self.bob

    def do_move(self, move):
        # TODO: Accept ACTIVATE_BASE action
        # TODO: Track activated vs unactivated bases
        if move.action == Actions.PLAY:
            logging.warning("{} is PLAYING: {}".format(move.actor.name, move.target.data[CardAttrs.NAME]))
            move_list_item(move.target,
                           move.actor[Zones.HAND],
                           move.actor[Zones.IN_PLAY])
            self._apply_abilities(move)
        elif move.action == Actions.SCRAP:
            logging.warning("{} is SCRAPPING: {}".format(move.actor.name, move.target.data[CardAttrs.NAME]))
            move_list_item(move.target, move.actor[Zones.IN_PLAY], [])
            self._apply_abilities(move)
        elif move.action == Actions.BUY:
            logging.warning("{} is BUYING: {}".format(move.actor.name, move.target.data[CardAttrs.NAME]))

            move.actor[Values.TRADE] -= move.target.data[CardAttrs.COST]
            logging.warning("{} spent {} TRADE and has {} remaining".format(move.actor.name,
                                                                            move.target.data[CardAttrs.COST],
                                                                            move.actor[Values.TRADE]))

            if move.target == Explorer:
                move.actor[Zones.DISCARD].append(move.target)
            else:
                move_list_item(move.target, self.trade_row, move.actor[Zones.DISCARD])
                self._fill_trade_row()
        elif move.action == Actions.ATTACK:
            logging.warning("{} is ATTACKING {} for {} damage!".format(move.actor.name,
                                                                       move.target.name,
                                                                       move.actor[Values.DAMAGE]))
            move.target[Values.AUTHORITY] -= move.actor[Values.DAMAGE]
            move.actor[Values.DAMAGE] = 0
            logging.warning("{} has {} AUTHORITY remaining".format(move.target.name,
                                                                   move.target[Values.AUTHORITY]))
        elif move.action == Actions.END_TURN:
            logging.warning("{} is ENDING THEIR TURN".format(move.actor.name))
            self.active_player.state.end_turn()
            self.active_player, self.inactive_player = self.inactive_player, self.active_player
            self.turn_number += 1

    def _apply_abilities(self, move):
        for key, value in move.target.data[move.action].items():
            if key in [Values.DAMAGE, Values.TRADE, Values.AUTHORITY]:
                new_value = move.actor[key] + value
                logging.warning("Adding {} to {}'s {} for a total of {}".format(value,
                                                                                move.actor.name,
                                                                                key.name,
                                                                                new_value))
                self.active_player[key] = new_value

            elif key == Abilities.DRAW:
                move.actor.state.draw(1)
                logging.warning("{} DRAWS a card".format(move.actor.name))

            else:
                logging.warning("Ignoring ability - {}: {}".format(key, value))

    def _fill_trade_row(self):
        cards_in_row = len(self.trade_row)
        empty_slots = 5 - cards_in_row
        new_cards = self.trade_deck[:empty_slots]
        for new_card in new_cards:
            logging.warning("Trade Row: {} added".format(new_card.data[CardAttrs.NAME]))
            self.trade_row.append(new_card)
        self.trade_deck[:empty_slots] = []
