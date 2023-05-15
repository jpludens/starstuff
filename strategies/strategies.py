from random import choice
from components.cards import Viper, Scout, MachineBase
from engine.effects import PendScrap, PendChoice, PendRecycle, GainDamage
from enums.enums import Triggers, CardTypes, ValueTypes, Zones
from engine.move import PlayCard, ActivateBase, ActivateAlly, ActivateScrap, AcquireCard, EndTurn, Choose, Scrap, \
    AttackBase, AttackOpponent


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
                return [AcquireCard(card)]

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


