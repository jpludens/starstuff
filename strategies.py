from random import choice, sample, randint
from cards import Explorer, Viper, Scout, MachineBase
from effects import PendDiscard, PendScrap, PendDestroyBase, PendChoice, PendRecycle, GainDamage
from enums import Triggers, CardTypes, ValueTypes, Zones, Factions
from move import PlayCard, ActivateBase, ActivateAlly, ActivateScrap, BuyCard, EndTurn, Choose, Scrap, \
    Discard, AttackBase, AttackOpponent, DestroyBase


class Strategy(object):
    @classmethod
    def _get_play_all_cards_moves(cls, gamestate):
        moves = []
        for card in gamestate.active_player[Zones.HAND]:
            moves.append(PlayCard(card))
            if card.card_type == CardTypes.SHIP:
                abilities = card.abilities[Triggers.SHIP]
                for ability in abilities:
                    if PendChoice in abilities:
                        if isinstance(ability, PendChoice):
                            chosen_choice = type(choice(list(ability.choices.keys())))
                            moves.append(Choose(chosen_choice))
                    if PendScrap in abilities:
                        raise RuntimeError  # Scrap cards should be getting played individually
        return moves

    @classmethod
    def _get_play_scrap_ship_moves(cls, gamestate, card, effect):
        cards_in_zones = sum([len(gamestate[z]) for z in effect.zones])
        # At least 1 card in trade row, or at least 2 cards across hand/discard,
        # because the card being played right now is also in hand and won't be a valid target!
        if Zones.TRADE_ROW in effect.zones and cards_in_zones or cards_in_zones > 1:
            card_to_scrap = cls._get_card_to_scrap(gamestate, effect)
            if card_to_scrap:
                return [PlayCard(card), Scrap(card_to_scrap)]
            else:
                return [PlayCard(card), Scrap()]
        else:
            return [PlayCard(card)]

    @classmethod
    def _get_card_to_scrap(cls, gamestate, scrap_effect):
        if Zones.TRADE_ROW in scrap_effect.zones:
            return choice(gamestate[Zones.TRADE_ROW])

        elif len(scrap_effect.zones) == 2:  # Hacky, but catches everything except blobs and machine base
            scout_to_scrap = None
            for d_card in gamestate.active_player[Zones.DISCARD]:
                if isinstance(d_card, Viper):
                    return d_card
                elif not scout_to_scrap and isinstance(d_card, Scout):
                    scout_to_scrap = d_card
            else:
                if scout_to_scrap:
                    return scout_to_scrap
                else:
                    for h_card in gamestate.active_player[Zones.HAND]:
                        if isinstance(h_card, Viper):
                            return h_card
        else:
            # Machine Base case - currently handled in get_moves
            return None

    @classmethod
    def _get_attack_move(cls, gamestate, target_base=None):
        return [AttackBase(target_base) if target_base else AttackOpponent(gamestate.opponent)]

    @classmethod
    def _get_end_turn_move(cls):
        return [EndTurn()]

    @classmethod
    def _get_activate_base_move(cls, gamestate, card):
        for ability in card.abilities[Triggers.BASE]:
            if isinstance(ability, PendChoice):
                chosen_choice = choice(list(ability.choices.keys()))
                if isinstance(ability, PendRecycle):
                    pass
                else:
                    return [ActivateBase(card), Choose(chosen_choice)]
            if isinstance(ability, PendScrap):
                if not isinstance(card, MachineBase):  # Handled at top level bc the DRAW provides more info/options
                    # Only include a scrap move if there's anything available to scrap
                    if any([gamestate[z] for z in ability.zones]):
                        scrap_card = cls._get_card_to_scrap(gamestate, ability)
                        return [ActivateBase(card), Scrap(scrap_card) if scrap_card else Scrap()]
                    else:
                        pass
        return [ActivateBase(card)]

    @classmethod
    def _get_buy_most_expensive_card_move(cls, gamestate, faction=None):
        cards_by_cost = sorted(gamestate.trade_row, key=lambda c: c.cost)
        for card in cards_by_cost:
            if faction is not None and faction != card.faction:
                continue
            if gamestate.active_player[ValueTypes.TRADE] >= card.cost:
                return [BuyCard(card)]

    @classmethod
    def _get_attack_all_outposts_moves(cls, gamestate):
        moves = []
        for card in gamestate.opponent[Zones.IN_PLAY]:
            if card.card_type == CardTypes.OUTPOST:
                moves.append(AttackBase(card))
        return moves

    @classmethod
    def _get_damage_required_to_win(cls, gamestate):
        damage = gamestate.opponent[ValueTypes.AUTHORITY]
        for card in gamestate.opponent[Zones.IN_PLAY]:
            if card.card_type == CardTypes.OUTPOST:
                damage += card.defense
        return damage

    @classmethod
    def _get_total_available_scrap_damage(cls, gamestate):
        total = 0
        for card in gamestate.active_player[Zones.IN_PLAY]:
            scrap_ability = card.abilities.get(Triggers.SCRAP, {})
            if isinstance(scrap_ability, GainDamage):
                total += scrap_ability.amount
        return total

    @classmethod
    def _get_scrap_all_cards_for_damage_moves(cls, gamestate):
        scrap_moves = []
        for card in gamestate.active_player[Zones.IN_PLAY]:
            scrap_ability = card.abilities.get(Triggers.SCRAP, {})
            if isinstance(scrap_ability, GainDamage):
                scrap_moves.append(ActivateScrap(card))
        return scrap_moves

    @classmethod
    def _get_activate_all_ally_abilities(cls, gamestate):
        moves = []
        active_player = gamestate.active_player
        for card in active_player[Zones.IN_PLAY]:
            if Triggers.ALLY in card.available_abilities and active_player.active_factions[card.faction] > 1:
                moves.append(ActivateAlly(card))
        return moves

    @classmethod
    def _get_target_base(cls, gamestate):
        bases = gamestate.opponent[Zones.IN_PLAY]
        if bases:
            outposts = [b for b in bases if b.card_type == CardTypes.OUTPOST]
            if outposts:
                return outposts[0]
            return bases[0]
        return None


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
        first_pending_effect = gamestate.pending_effects[0] if gamestate.pending_effects else None
        if isinstance(first_pending_effect, PendDiscard):
            if first_pending_effect.mandatory:
                if first_pending_effect.up_to >= len(gamestate[Zones.HAND]):
                    return [Discard(*gamestate[Zones.HAND])]
                return [Discard(*sample(gamestate[Zones.HAND], first_pending_effect.up_to))]
            number_to_discard = randint(0, first_pending_effect.up_to)
            if number_to_discard >= len(gamestate[Zones.HAND]):
                return [Discard(*gamestate[Zones.HAND])]
            return [Discard(*sample(gamestate[Zones.HAND], number_to_discard))]

        playerstate = gamestate.active_player

        # If we have to Scrap (because of Machine Base), do it
        if isinstance(first_pending_effect, PendScrap) and first_pending_effect.mandatory:
            if gamestate.active_player[Zones.HAND]:
                return [Scrap(gamestate.active_player[Zones.HAND][0])]

        if isinstance(first_pending_effect, PendDestroyBase):
            return [DestroyBase(self._get_target_base(gamestate))]

        # If we have bases, activate them
        for card in playerstate[Zones.IN_PLAY]:
            if card.is_base() and Triggers.BASE in card.available_abilities:
                return self._get_activate_base_move(gamestate, card)

        # If we have any ships with scrap abilities, play them
        scrap_ships = [card for card in playerstate[Zones.HAND]
                       if card.has_ability(PendScrap, triggers=[Triggers.SHIP])]
        if scrap_ships:
            x = [e for e in scrap_ships[0].abilities[Triggers.SHIP]]
            return self._get_play_scrap_ship_moves(gamestate,
                                                   scrap_ships[0],
                                                   [e for e in scrap_ships[0].abilities[Triggers.SHIP]
                                                    if isinstance(e, PendScrap)][0])

        # If we have cards, play them
        if playerstate[Zones.HAND]:
            return self._get_play_all_cards_moves(gamestate)

        # If we have ally abilities available, activate them
        ally_moves = self._get_activate_all_ally_abilities(gamestate)
        if ally_moves:
            return ally_moves

        # If we can afford a card, buy it, starting with the most expensive
        if playerstate[ValueTypes.TRADE] > 0:
            move = self._get_buy_most_expensive_card_move(gamestate, self.faction)
            if move is not None:
                return move

        # If we can't buy, see if we can just win
        current_damage = playerstate[ValueTypes.DAMAGE]
        damage_to_win = self._get_damage_required_to_win(gamestate)
        if current_damage >= damage_to_win:
            return self._get_attack_all_outposts_moves(gamestate) + self._get_attack_move(gamestate)

        # If we can't win now, see if we could win by scrapping for damage
        available_scrap_damage = Strategy._get_total_available_scrap_damage(gamestate)
        if current_damage + available_scrap_damage >= damage_to_win:
            scrap_moves = self._get_scrap_all_cards_for_damage_moves(gamestate)
            outpost_moves = self._get_attack_all_outposts_moves(gamestate)
            deathblow_move = self._get_attack_move(gamestate)
            # noinspection PyTypeChecker
            return scrap_moves + outpost_moves + deathblow_move

        # If we can't win and there's an outpost, destroy it; or destroy a base; or attack the opponent
        if current_damage > 0:
            base_to_hit = self._get_target_base(gamestate)
            if base_to_hit:
                return [AttackBase(base_to_hit)]
            return [AttackOpponent(gamestate.opponent)]

        # If we can't Attack, End Turn
        return self._get_end_turn_move()


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
                return [BuyCard(Explorer)] * number_to_buy

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
