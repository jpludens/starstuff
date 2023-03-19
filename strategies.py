from cards import Explorer
from enums import Actions, CardAttrs, Values, Zones, Factions
from move import Move


class Strategy(object):
    @classmethod
    def get_play_all_cards(cls, gamestate):
        return [Move(gamestate.active_player, Actions.PLAY, card) for card in gamestate.active_player.state[Zones.HAND]]

    @classmethod
    def get_attack_opponent(cls, gamestate):
        return [Move(gamestate.active_player, Actions.ATTACK, gamestate.inactive_player)]

    @classmethod
    def get_end_turn(cls, gamestate):
        return [Move(gamestate.active_player, Actions.END_TURN)]

    @classmethod
    def get_buy_the_biggest(cls, gamestate, faction=None):
        cards_by_cost = sorted(gamestate.trade_row, key=lambda c: c.data[CardAttrs.COST])
        for card in cards_by_cost:
            if faction is not None and faction != card.data[CardAttrs.FACTION]:
                continue
            if gamestate.active_player.state[Values.TRADE] >= card.data[CardAttrs.COST]:
                return [Move(gamestate.active_player, Actions.BUY, card)]


class FactionStrategy(Strategy):
    def __init__(self, faction=Factions.TRADE_FEDERATION):
        # TODO: improve strategy to handle ranked faction preferences
        # TODO: improve strategy to buy explorers
        self.faction = faction

    def get_moves(self, gamestate):
        playerstate = gamestate.active_player.state

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self.get_play_all_cards(gamestate)

        # If we can afford a card, buy it, starting with the most expensive
        if playerstate[Values.TRADE] > 0:
            move = self.get_buy_the_biggest(gamestate, self.faction)
            if move is not None:
                return move

        # If we can't buy, Attack!
        if playerstate[Values.DAMAGE] > 0:
            return self.get_attack_opponent(gamestate)

        # If we can't Attack, End Turn
        return self.get_end_turn(gamestate)


class SplurgeStrategy(Strategy):
    def get_moves(self, gamestate):
        playerstate = gamestate.active_player.state

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self.get_play_all_cards(gamestate)

        # If we can afford a card, buy it, starting with the most expensive
        if playerstate[Values.TRADE] > 0:
            move = self.get_buy_the_biggest(gamestate)
            if move is not None:
                return move

        # If we can't buy, Attack!
        if playerstate[Values.DAMAGE] > 0:
            return self.get_attack_opponent(gamestate)

        # If we can't Attack, End Turn
        return self.get_end_turn(gamestate)


class ExplorerStrategy(Strategy):
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
        if playerstate[Zones.HAND]:
            return self.get_play_all_cards(gamestate)

        # If we don't have cards, buy some explorers?
        owned_explorers = playerstate.count_explorers()
        if self.maximum_explorers and owned_explorers < self.maximum_explorers:
            number_to_buy = playerstate[Values.TRADE] // Explorer.data[CardAttrs.COST]
            if number_to_buy:
                return [Move(gamestate.active_player, Actions.BUY, Explorer)] * number_to_buy

        # If we aren't buying, scrap?
        owned_explorers = playerstate.count_explorers()
        if owned_explorers:
            ratio = gamestate.inactive_player.state.values[Values.AUTHORITY] / owned_explorers
            if owned_explorers >= self.minimum_explorers\
                    or ratio < self.authority_to_explorer_ratio_to_ignore_minimum:
                number_to_scrap = playerstate[Zones.IN_PLAY].count(Explorer)
                if number_to_scrap:
                    return [Move(gamestate.active_player, Actions.SCRAP, Explorer)] * number_to_scrap

        # If we're not scrapping, attack?
        if playerstate[Values.DAMAGE]:
            return self.get_attack_opponent(gamestate)

        # Guess we're done then
        return self.get_end_turn(gamestate)
