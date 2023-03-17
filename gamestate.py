from playerstate import PlayerState
from strategies import ExplorerStrategy
from util import move_list_contents


class GameState(object):
    def __init__(self):
        self.p1_state = PlayerState(first_player=True, name="Alice", strategy=ExplorerStrategy(max_exp=25,
                                                                                               min_exp=6,
                                                                                               ratio=2))
        self.p2_state = PlayerState(first_player=False, name="Bob", strategy=ExplorerStrategy(max_exp=25,
                                                                                              min_exp=6,
                                                                                              ratio=2.5))

        self.p1_state.opponent_state, self.p2_state.opponent_state = self.p2_state, self.p1_state
        self.active_player = self.p1_state
        self.inactive_player = self.p2_state

        self.turn_number = 1

    def next_turn(self):
        move_list_contents(self.active_player.hand, self.active_player.discard)
        self.active_player.draw()
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.turn_number += 1
