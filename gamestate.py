import logging
from enums import *
from util import move_list_item
from playerstate import Player, PlayerState
from cards import Explorer


class GameState(object):
    def __init__(self, alice_strategy, bob_strategy):
        # Create players
        self.alice = Player("Alice", alice_strategy, PlayerState(first_player=True))
        self.bob = Player("Bob", bob_strategy, PlayerState(first_player=False))

        # Set up for Turn 1
        self.turn_number = 1
        self.active_player = self.alice
        self.inactive_player = self.bob

    def do_move(self, move):
        logging.warning("Move: {} {}".format(move.action, move.target))
        if move.action == PLAY:
            move_list_item(move.target,
                           self.active_player[HAND],
                           self.active_player[IN_PLAY])
            self.apply_abilities(move)
        elif move.action == SCRAP:
            move_list_item(move.target, self.active_player[IN_PLAY], [])
            self.apply_abilities(move)
        elif move.action == BUY:
            # No trade deck yet, only Explorers, so append instead of move
            assert move.target == Explorer
            self.active_player[DISCARD].append(move.target)
            self.active_player[TRADE] -= move.target[COST]
        elif move.action == ATTACK:
            logging.warning("Attacking for {} damage!".format(self.active_player.state.values[DAMAGE]))
            self.inactive_player.state.values[AUTHORITY] -= self.active_player.state.values[DAMAGE]
            self.active_player.state.values[DAMAGE] = 0
        elif move.action == END_TURN:
            self.next_turn()

    def apply_abilities(self, move):
        for value_type, value_amount in move.target[move.action].items():
            self.active_player.state.values[value_type] += value_amount

    def next_turn(self):
        self.active_player.state.end_turn()
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.turn_number += 1
