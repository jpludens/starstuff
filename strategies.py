from cards import Explorer
from enums import *
from move import Move


class ExplorerStrategy(object):
    def __init__(self, max_exp=None, min_exp=None, ratio=None):
        # There should probably be a point below which a maximum loses more, but above which it doesn't matter
        self.maximum_explorers = max_exp

        # Should be a sweet spot
        self.minimum_explorers = min_exp

        # This should squeak ahead at the margins
        self.authority_to_explorer_ratio_to_ignore_minimum = ratio

    def get_moves(self, gamestate):
        playerstate = gamestate.active_player.state

        # If we have cards, play them
        if playerstate.zones[HAND]:
            return [Move(PLAY, card) for card in playerstate.zones[HAND]]

        # If we don't have cards, buy some explorers?
        owned_explorers = playerstate.count_explorers()
        if self.maximum_explorers and owned_explorers < self.maximum_explorers:
            number_to_buy = playerstate.values[TRADE] // Explorer[COST]
            if number_to_buy:
                return [Move(BUY, Explorer)] * number_to_buy

        # If we aren't buying, scrap?
        owned_explorers = playerstate.count_explorers()
        if owned_explorers:
            ratio = gamestate.inactive_player.state.values[AUTHORITY] / owned_explorers
            if owned_explorers >= self.minimum_explorers\
                    or ratio < self.authority_to_explorer_ratio_to_ignore_minimum:
                number_to_scrap = playerstate.zones[IN_PLAY].count(Explorer)
                if number_to_scrap:
                    return [Move(SCRAP, Explorer)] * number_to_scrap

        # If we're not scrapping, attack?
        if playerstate.values[DAMAGE]:
            return [Move(ATTACK)]

        # Guess we're done then
        return [Move(END_TURN)]
