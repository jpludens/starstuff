from enums.enums import Zones, ValueTypes
from strategies.strategies import Strategy


class SplurgeStrategy(Strategy):
    def get_moves(self, gamestate):
        playerstate = gamestate.active_player

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self._get_play_all_cards_moves(gamestate)

        # If we can afford a card, buy it, starting with the most expensive
        if playerstate[ValueTypes.TRADE] > 0:
            move = self._get_buy_most_expensive_card_move(gamestate)
            if move is not None:
                return move

        # If we can't buy, Attack!
        if playerstate[ValueTypes.DAMAGE] > 0:
            return self._get_attack_move(gamestate)

        # If we can't Attack, End Turn
        return self._get_end_turn_move()