from random import sample, randint

from engine.effects import PendDiscard, PendScrap, PendDestroyBase
from engine.move import Discard, Scrap, DestroyBase, AttackBase, AttackOpponent
from enums.enums import Factions, Zones, Triggers, ValueTypes
from strategies.strategies import Strategy


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