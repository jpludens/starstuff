from cards import Explorer


class ExplorerStrategy(object):
    def __init__(self, max_exp=None, min_exp=None, ratio=None):
        # There should probably be a point below which a maximum loses more, but above which it doesn't matter
        self.maximum_explorers = max_exp

        # Should be a sweet spot
        self.minimum_explorers = min_exp

        # This should squeak ahead at the margins
        self.authority_to_explorer_ratio_to_ignore_minimum = ratio

    def buy_explorers(self, state):
        if self.maximum_explorers and state.metrics[Explorer] >= self.maximum_explorers:
            return

        explorers_to_buy = sum([card.trade for card in state.hand]) // Explorer.cost
        state.discard.extend([Explorer] * explorers_to_buy)
        state.metrics[Explorer] += explorers_to_buy

    def scrap_explorers(self, state):
        # (avoid a divide by 0)
        if not state.metrics[Explorer]:
            return

        explorers_to_scrap = 0
        if state.opponent_state.authority / state.metrics[Explorer] < self.authority_to_explorer_ratio_to_ignore_minimum:
            explorers_to_scrap = state.hand.count(Explorer)

        if state.metrics[Explorer] >= self.minimum_explorers:
            explorers_to_scrap = state.hand.count(Explorer)

        if explorers_to_scrap:
            explorer_damage = 0
            while explorers_to_scrap:
                try:
                    state.hand.remove(Explorer)
                except ValueError:
                    break
                else:
                    explorer_damage += 2
                    state.metrics[Explorer] -= 1

            # Not sure how I feel about directly modifying opponent state here but fine for now
            if explorer_damage:
                state.opponent_state.authority -= explorer_damage
