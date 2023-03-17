from cards import Explorer


class ExplorerStrategy(object):
    def __init__(self, max_exp=None, min_exp=None, ratio=None):
        # There should probably be a point below which a maximum loses more, but above which it doesn't matter
        self.maximum_explorers = max_exp

        # Should be a sweet spot
        self.minimum_explorers = min_exp

        # This should squeak ahead at the margins
        self.authority_to_explorer_ratio_to_ignore_minimum = ratio

    def get_explorers_to_buy(self, state):
        if self.maximum_explorers and state.explorer_count >= self.maximum_explorers:
            return 0
        return sum([card.trade for card in state.hand]) // Explorer.cost

    def get_explorers_to_scrap(self, state):
        # (avoid a divide by 0)
        if state.explorer_count:
            if state.opponent_state.authority / state.explorer_count < self.authority_to_explorer_ratio_to_ignore_minimum:
                return state.hand.count(Explorer)

            if state.explorer_count >= self.minimum_explorers:
                return state.hand.count(Explorer)

        return 0
