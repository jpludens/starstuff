import logging
from enums import *
from util import move_list_item
from playerstate import Player, PlayerState
from cards import Explorer


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


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
        if move.action == PLAY:
            logging.warning("{} is PLAYING: {}".format(move.actor.name, move.target[NAME]))
            move_list_item(move.target,
                           move.actor[HAND],
                           move.actor[IN_PLAY])
            self.apply_abilities(move)
        elif move.action == SCRAP:
            logging.warning("{} is SCRAPPING: {}".format(move.actor.name, move.target[NAME]))
            move_list_item(move.target, move.actor[IN_PLAY], [])
            self.apply_abilities(move)
        elif move.action == BUY:
            # No trade deck yet, only Explorers, so append instead of move
            logging.warning("{} is BUYING: {}".format(move.actor.name, move.target[NAME]))
            assert move.target == Explorer
            move.actor[TRADE] -= move.target[COST]
            move.actor[DISCARD].append(move.target)
            logging.warning("{} spent {} TRADE and has {} remaining".format(move.actor.name,
                                                                            move.target[COST],
                                                                            move.actor[TRADE]))
        elif move.action == ATTACK:
            logging.warning("{} is ATTACKING {} for {} damage!".format(move.actor.name,
                                                                       move.target.name,
                                                                       move.actor[DAMAGE]))
            move.target[AUTHORITY] -= move.actor[DAMAGE]
            move.actor[DAMAGE] = 0
            logging.warning("{} has {} AUTHORITY remaining".format(move.target.name,
                                                                   move.target[AUTHORITY]))
        elif move.action == END_TURN:
            logging.warning("{} is ENDING THEIR TURN".format(move.actor.name))
            self.next_turn()

    def apply_abilities(self, move):
        for value_type, value_amount in move.target[move.action].items():
            new_value = move.actor[value_type] + value_amount
            logging.warning("Adding {} to {}'s {} for a total of {}".format(value_amount,
                                                                            move.actor.name,
                                                                            value_type.name,
                                                                            new_value))
            self.active_player[value_type] = new_value

    def next_turn(self):
        self.active_player.state.end_turn()
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.turn_number += 1
