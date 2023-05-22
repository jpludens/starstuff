from abc import ABC


class Strategy(object):
    def get_move(self, gamestate_view):
        raise NotImplementedError

    def what_to_buy(self, gamestate_view):
        raise NotImplementedError

    def what_to_play(self, gamestate_view):
        raise NotImplementedError

    def what_to_activate(self, gamestate_view):
        raise NotImplementedError

    def what_to_discard(self, gamestate_view):
        raise NotImplementedError


class RandomStrategy(Strategy):
    def get_moves(self, gamestate_view):
        # Check for pending effects
        #

        # Identify all playable cards
        # Identify all available abilities
        # Pick one at random

        # If NO cards or abilities, make random purchases until unable
        pass
