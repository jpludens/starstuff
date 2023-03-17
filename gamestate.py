from playerstate import PlayerState


class GameState(object):
    def __init__(self, alice_strategy, bob_strategy):
        self.p1_state = PlayerState(first_player=True, name="Alice", strategy=alice_strategy)
        self.p2_state = PlayerState(first_player=False, name="Bob", strategy=bob_strategy)

        self.p1_state.opponent_state, self.p2_state.opponent_state = self.p2_state, self.p1_state
        self.active_player = self.p1_state
        self.inactive_player = self.p2_state

        self.turn_number = 1

    def next_turn(self):
        self.active_player.end_turn()
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.turn_number += 1
