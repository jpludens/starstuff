import logging
from abc import ABC

from components.cards import Explorer, FleetHQ
from engine.effects import PendScrap, PendChoice, PendDiscard, DestroyBaseEffect, PendDestroyBase, PendCopyShip,\
    AcquireEffect, PendAcquireShipToTopForFree, GainDamage
from enums.enums import Zones, CardTypes, Triggers, ValueTypes, Factions
from util.util import move_list_item


class Move(ABC):
    def execute(self, gamestate):
        self._validate(gamestate)
        self._execute(gamestate)

    def _execute(self, gamestate):
        raise NotImplementedError

    def _validate(self, gamestate):
        raise NotImplementedError


class AbilityActivation(Move, ABC):
    trigger = None

    def __init__(self, card):
        self.card = card

    def _execute(self, gamestate):
        self.activate_ability(gamestate)

    def activate_ability(self, gamestate):
        if self.trigger in [Triggers.SHIP, Triggers.BASE]:
            ability_text = "PRIMARY"
        else:
            ability_text = self.trigger.name

        logging.warning("Activating {}'s {} ability".format(self.card.name, ability_text))
        for effect in self.card.trigger_ability(self.trigger):
            # These need to occur in this order so that effects will apply to this card
            gamestate.last_activated_card = self.card
            effect.apply(gamestate)


class PlayCard(AbilityActivation):
    trigger = Triggers.SHIP

    def _validate(self, gamestate):
        pass  # No validation - allowing KeyError if card is not in hand

    def _execute(self, gamestate):
        logging.warning("{} is PLAYING: {}".format(gamestate.active_player.name, self.card.name))
        self.card.move_to(Zones.IN_PLAY)
        gamestate.active_player.active_factions.update(self.card.active_factions)
        move_list_item(self.card,
                       gamestate.active_player[Zones.HAND],
                       gamestate.active_player[Zones.IN_PLAY])

        if self.card.faction == Factions.BLOB:
            gamestate.blob_cards_played_this_turn += 1

        if self.card.card_type == CardTypes.SHIP:
            if any([isinstance(card, FleetHQ) for card in gamestate[Zones.IN_PLAY]]):
                GainDamage(1).apply(gamestate)
            self.activate_ability(gamestate)


class ActivateBase(AbilityActivation):
    trigger = Triggers.BASE

    def _validate(self, gamestate):
        pass  # No validation - allowing KeyError if Triggers.BASE is unavailable or consumed


class ActivateAlly(AbilityActivation):
    trigger = Triggers.ALLY

    def _validate(self, gamestate):
        if gamestate.active_player.active_factions[self.card.faction] <= 1:
            # This is pretty much just for stealth needle
            if len(self.card.active_factions) > 1:
                other_faction = [f for f in self.card.active_factions if f != self.card.faction][0]
                if gamestate.active_player.active_factions[other_faction] > 1:
                    return
            raise FileNotFoundError


class ActivateScrap(AbilityActivation):
    trigger = Triggers.SCRAP

    def _validate(self, gamestate):
        pass  # No validation - allowing IndexErrors when card is removed from somewhere it isn't

    def _execute(self, gamestate):
        # Both these steps must occur before "moving" card because that move function clears abilities
        self.activate_ability(gamestate)
        gamestate.active_player.active_factions.subtract(self.card.active_factions)

        self.card.move_to(Zones.SCRAP_HEAP)
        gamestate.active_player[Zones.IN_PLAY].remove(self.card)


class AcquireCard(Move):
    def __init__(self, card=None, explorer=True, top_of_deck=False):
        self.top_of_deck = top_of_deck

        if card:
            self.card = card
        elif explorer:
            self.card = Explorer()
        else:
            raise ValueError

    def _validate(self, gamestate):
        if self.top_of_deck:
            if self.card.card_type != CardTypes.SHIP or gamestate.freighter_hauls < 1:
                raise FileNotFoundError
        if gamestate[ValueTypes.TRADE] < self.card.cost:
            raise FileNotFoundError

    def _execute(self, gamestate):
        if gamestate.pending_effects:
            pending_effect = gamestate.pending_effects[0]
            if isinstance(pending_effect, PendAcquireShipToTopForFree):
                pending_effect.resolve(self.card)
        else:
            gamestate.active_player[ValueTypes.TRADE] -= self.card.cost
            if gamestate.freighter_hauls and self.card.card_type == CardTypes.SHIP:
                gamestate.freighter_hauls -= 1
            AcquireEffect(self.card, self.top_of_deck).apply(gamestate)
            logging.warning("{} spent {} TRADE and has {} remaining".format(
                gamestate.active_player.name,
                self.card.cost,
                gamestate.active_player[ValueTypes.TRADE]))


class AttackBase(Move):
    def __init__(self, base):
        self.base = base

    def _validate(self, gamestate):
        if self.base.card_type != CardTypes.OUTPOST:
            if any([c.card_type == CardTypes.OUTPOST for c in gamestate.opponent[Zones.IN_PLAY]]):
                raise FileNotFoundError

    def _execute(self, gamestate):
        gamestate.active_player[ValueTypes.DAMAGE] -= self.base.defense
        DestroyBaseEffect(self.base).apply(gamestate)

        logging.warning("{} has {} DAMAGE remaining".format(
            gamestate.active_player.name,
            gamestate.active_player[ValueTypes.AUTHORITY]))


class AttackOpponent(Move):
    def __init__(self, opponent):
        self.opponent = opponent

    def _validate(self, gamestate):
        opponent_has_outpost = any([c.card_type == CardTypes.OUTPOST for c in gamestate.opponent[Zones.IN_PLAY]])
        if opponent_has_outpost:
            raise FileNotFoundError

    def _execute(self, gamestate):
        logging.warning("{} is ATTACKING {} for {} damage!".format(
            gamestate.active_player.name,
            self.opponent.name,
            gamestate.active_player[ValueTypes.DAMAGE]))

        self.opponent[ValueTypes.AUTHORITY] -= gamestate.active_player[ValueTypes.DAMAGE]
        gamestate.active_player[ValueTypes.DAMAGE] = 0

        logging.warning("{} has {} AUTHORITY remaining".format(self.opponent.name,
                                                               self.opponent[ValueTypes.AUTHORITY]))

        if gamestate.opponent[ValueTypes.AUTHORITY] <= 0:
            gamestate.victor = gamestate.active_player.name


class EndTurn(Move):
    def _validate(self, gamestate):
        pass

    def _execute(self, gamestate):
        logging.warning("{} is ENDING THEIR TURN".format(gamestate.active_player.name))
        gamestate.next_turn()
        if gamestate.forced_discards:
            PendDiscard(up_to=gamestate.forced_discards, mandatory=True).apply(gamestate)
            gamestate.forced_discards = 0


class PendingMove(Move, ABC):
    resolved_effect_type = None

    def __init__(self):
        super().__init__()
        self.effect = None

    def execute(self, gamestate):
        self.effect = [e for e in gamestate.pending_effects if isinstance(e, self.resolved_effect_type)][0]
        self._validate(gamestate)
        self._execute(gamestate)

    def _execute(self, gamestate):
        self._resolve_effect()

    def _resolve_effect(self):
        raise NotImplementedError


class Discard(PendingMove):
    resolved_effect_type = PendDiscard

    def __init__(self, *cards):
        super().__init__()
        self.cards = cards

    def _validate(self, gamestate):
        if self.effect.mandatory\
                and len(self.cards) < self.effect.up_to\
                and len(self.cards) < len(gamestate[Zones.HAND]):
            raise FileNotFoundError

    def _resolve_effect(self):
        self.effect.resolve(self.cards)


class Choose(PendingMove):
    resolved_effect_type = PendChoice

    def __init__(self, choice):
        super().__init__()
        self.choice = choice

    def _validate(self, gamestate):
        if self.choice not in self.effect.choices:
            raise FileNotFoundError

    def _resolve_effect(self):
        self.effect.resolve(self.choice)


class Scrap(PendingMove):
    resolved_effect_type = PendScrap

    def __init__(self, *targets):
        super().__init__()
        self.targets = targets

    def _validate(self, gamestate):
        for target in self.targets:
            if target.location not in self.effect.zones:
                raise FileNotFoundError
        if self.effect.mandatory:
            if len(self.targets) < self.effect.up_to:
                raise FileNotFoundError

    def _resolve_effect(self):
        self.effect.resolve(self.targets)


class DestroyBase(PendingMove):
    resolved_effect_type = PendDestroyBase

    def __init__(self, target=None):
        super().__init__()
        self.target = target

    def _validate(self, gamestate):
        opponent_has_outpost = any([c.card_type == CardTypes.OUTPOST for c in gamestate.opponent[Zones.IN_PLAY]])
        if opponent_has_outpost and self.target.card_type != CardTypes.OUTPOST:
            raise FileNotFoundError

    def _resolve_effect(self):
        self.effect.resolve(self.target)


class CopyShip(PendingMove):
    resolved_effect_type = PendCopyShip

    def __init__(self, ship):
        super().__init__()
        self.ship = ship

    def _validate(self, gamestate):
        if self.ship not in gamestate[Zones.IN_PLAY]:
            raise FileNotFoundError

    def _resolve_effect(self):
        self.effect.resolve(self.ship)


class AcquireShipToTopForFree(PendingMove):
    resolved_effect_type = PendAcquireShipToTopForFree

    def __init__(self, ship=None, explorer=True):
        super().__init__()
        if ship:
            self.ship = ship
        elif explorer:
            self.ship = Explorer()
        else:
            raise ValueError

    def _validate(self, gamestate):
        if self.ship not in gamestate[Zones.TRADE_ROW] and not isinstance(self.ship, Explorer):
            raise FileNotFoundError

    def _resolve_effect(self):
        self.effect.resolve(self.ship)
