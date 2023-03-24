from cards import Explorer
from enums import Actions, CardTypes, Values, Zones, Factions
from move import Move


class Strategy(object):
    @classmethod
    def _get_play_all_cards_moves(cls, gamestate):
        return [Move(gamestate.active_player, Actions.PLAY, card) for card in gamestate.active_player.state[Zones.HAND]]

    @classmethod
    def _get_attack_move(cls, gamestate, target_base=None):
        return [Move(gamestate.active_player,
                     Actions.ATTACK,
                     target_base if target_base else gamestate.inactive_player)]

    @classmethod
    def _get_end_turn_move(cls, gamestate):
        return [Move(gamestate.active_player, Actions.END_TURN)]

    @classmethod
    def _get_activate_base_move(cls, gamestate, card):
        return [Move(gamestate.active_player, Actions.ACTIVATE_BASE, card)]

    @classmethod
    def _get_buy_most_expensive_card_move(cls, gamestate, faction=None):
        cards_by_cost = sorted(gamestate.trade_row, key=lambda c: c.cost)
        for card in cards_by_cost:
            if faction is not None and faction != card.faction:
                continue
            if gamestate.active_player.state[Values.TRADE] >= card.cost:
                return [Move(gamestate.active_player, Actions.BUY, card)]

    @classmethod
    def _get_attack_all_outposts_moves(cls, gamestate):
        moves = []
        for card in gamestate.inactive_player[Zones.IN_PLAY]:
            if card.card_type == CardTypes.OUTPOST:
                moves.append(Move(gamestate.active_player, Actions.ATTACK, card))
        return moves

    @classmethod
    def _get_damage_required_to_win(cls, gamestate):
        damage = gamestate.inactive_player[Values.AUTHORITY]
        for card in gamestate.inactive_player[Zones.IN_PLAY]:
            if card.card_type == CardTypes.OUTPOST:
                damage += card.defense
        return damage

    @classmethod
    def _get_total_available_scrap_damage(cls, gamestate):
        total = 0
        for card in gamestate.active_player[Zones.IN_PLAY]:
            scrap_ability = card.abilities.get(Actions.SCRAP, {})
            total += scrap_ability.get(Values.DAMAGE, 0)
        return total

    @classmethod
    def _get_scrap_all_cards_for_damage_moves(cls, gamestate):
        scrap_moves = []
        for card in gamestate.active_player[Zones.IN_PLAY]:
            scrap_ability = card.abilities.get(Actions.SCRAP, {})
            if scrap_ability.get(Values.DAMAGE) is not None:
                scrap_moves.append(Move(gamestate.active_player, Actions.SCRAP, card))
        return scrap_moves

    @classmethod
    def _get_activate_all_ally_abilities(cls, gamestate):
        moves = []
        for card in gamestate.active_player[Zones.IN_PLAY]:
            if Actions.ALLY in card.available_abilities and gamestate.active_factions[card.faction] > 1:
                moves.append(Move(gamestate.active_player, Actions.ALLY, card))
        return moves


# class BasicStrategy(Strategy):
#     def get_moves(self, gamestate):
#         sequence = [self.get_purchases,
#                     self.get_explorer_purchases,
#                     self._get_attack_move,
#                     self._get_end_turn_move]
#         for step in sequence:
#             moves = step(gamestate)
#             if moves:
#                 return moves
#
#     def get_purchases(self, gamestate):
#         raise NotImplementedError
#
#     def get_explorer_purchases(self, gamestate):
#         raise NotImplementedError


class FactionStrategy(Strategy):
    def __init__(self, faction=Factions.TRADE_FEDERATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faction = faction

    def get_moves(self, gamestate):
        playerstate = gamestate.active_player.state

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self._get_play_all_cards_moves(gamestate)

        # If we have bases, activate them
        for card in playerstate[Zones.IN_PLAY]:
            if card.is_base() and Actions.ACTIVATE_BASE in card.available_abilities:
                return self._get_activate_base_move(gamestate, card)

        # If we have ally abilities available, activate them
        ally_moves = self._get_activate_all_ally_abilities(gamestate)
        if ally_moves:
            return ally_moves

        # If we can afford a card, buy it, starting with the most expensive
        if playerstate[Values.TRADE] > 0:
            move = self._get_buy_most_expensive_card_move(gamestate, self.faction)
            if move is not None:
                return move

        # If we can't buy, see if we can just win
        current_damage = playerstate[Values.DAMAGE]
        damage_to_win = self._get_damage_required_to_win(gamestate)
        if current_damage >= damage_to_win:
            return self._get_attack_all_outposts_moves(gamestate) + self._get_attack_move(gamestate)

        # If we can't win now, see if we could win by scrapping for damage
        available_scrap_damage = Strategy._get_total_available_scrap_damage(gamestate)
        if current_damage + available_scrap_damage >= damage_to_win:
            scrap_moves = self._get_scrap_all_cards_for_damage_moves(gamestate)
            outpost_moves = self._get_attack_all_outposts_moves(gamestate)
            deathblow_move = self._get_attack_move(gamestate)
            return scrap_moves + outpost_moves + deathblow_move

        # If we can't win and there's an outpost, destroy it; or destroy a base; or attack the opponent
        if current_damage > 0:
            bases = gamestate.inactive_player[Zones.IN_PLAY]
            if bases:
                outposts = [b for b in bases if b.card_type == CardTypes.OUTPOST]
                if outposts:
                    if outposts[0].defense <= current_damage:
                        return self._get_attack_move(gamestate, target_base=outposts[0])
                if bases[0].defense <= current_damage:
                    return self._get_attack_move(gamestate, target_base=bases[0])
            return self._get_attack_move(gamestate)

        # If we can't Attack, End Turn
        return self._get_end_turn_move(gamestate)


class SplurgeStrategy(Strategy):
    def get_moves(self, gamestate):
        playerstate = gamestate.active_player.state

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self._get_play_all_cards_moves(gamestate)

        # If we can afford a card, buy it, starting with the most expensive
        if playerstate[Values.TRADE] > 0:
            move = self._get_buy_most_expensive_card_move(gamestate)
            if move is not None:
                return move

        # If we can't buy, Attack!
        if playerstate[Values.DAMAGE] > 0:
            return self._get_attack_move(gamestate)

        # If we can't Attack, End Turn
        return self._get_end_turn_move(gamestate)


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
            return self._get_play_all_cards_moves(gamestate)

        # If we don't have cards, buy some explorers?
        owned_explorers = playerstate.count_explorers()
        if self.maximum_explorers and owned_explorers < self.maximum_explorers:
            number_to_buy = playerstate[Values.TRADE] // Explorer.cost
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
            return self._get_attack_move(gamestate)

        # Guess we're done then
        return self._get_end_turn_move(gamestate)
