from components.cards import Explorer
from engine.move import AcquireCard
from enums.enums import Zones, ValueTypes
from strategies.strategies import Strategy


class ExplorerStrategy(Strategy):
    def __init__(self, max_exp=None, min_exp=None, ratio=None):
        # There should probably be a point below which a maximum loses more, but above which it doesn't matter
        self.maximum_explorers = max_exp

        # Should be a sweet spot
        self.minimum_explorers = min_exp

        # This should squeak ahead at the margins
        self.authority_to_explorer_ratio_to_ignore_minimum = ratio

    def get_moves(self, gamestate):
        playerstate = gamestate.active_player

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self._get_play_all_cards_moves(gamestate)

        # If we don't have cards, buy some explorers?
        owned_explorers = sum([zone.count(Explorer) for zone in playerstate.zones.values()])
        if self.maximum_explorers and owned_explorers < self.maximum_explorers:
            number_to_buy = playerstate[ValueTypes.TRADE] // Explorer.cost
            if number_to_buy:
                return [AcquireCard(Explorer)] * number_to_buy

        # If we aren't buying, scrap?
        if owned_explorers:
            ratio = gamestate.opponent.values[ValueTypes.AUTHORITY] / owned_explorers
            if owned_explorers >= self.minimum_explorers\
                    or ratio < self.authority_to_explorer_ratio_to_ignore_minimum:
                number_to_scrap = playerstate[Zones.IN_PLAY].count(Explorer)
                if number_to_scrap:
                    # TODO: target individual Explorers for ScrapAbility
                    return [] * number_to_scrap

        # If we're not scrapping, attack?
        if playerstate[ValueTypes.DAMAGE]:
            return self._get_attack_move(gamestate)

        # Guess we're done then
        return self._get_end_turn_move()