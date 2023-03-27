import logging

from cards import Explorer, Card
from effects import PendScrap, PendChoice, PendDiscard
from enums import Zones, CardTypes, Triggers, ValueTypes
from util import move_list_item


class Move(object):
    def execute(self, gamestate):
        raise NotImplementedError


class AbilityActivation(Move):
    def __init__(self, card, trigger):
        self.card = card
        self.trigger = trigger

    def execute(self, gamestate):
        self.activate_ability(gamestate)

    def activate_ability(self, gamestate):
        if self.trigger in [Triggers.SHIP, Triggers.BASE]:
            ability_text = "PRIMARY"
        else:
            ability_text = self.trigger.name

        logging.warning("Activating {}'s {} ability".format(self.card.name, ability_text))
        for effect in self.card.trigger_ability(self.trigger):
            effect.apply(gamestate)


class PlayCard(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.SHIP)

    def execute(self, gamestate):
        logging.warning("{} is PLAYING: {}".format(gamestate.active_player.name, self.card.name))
        self.card.move_to(Zones.IN_PLAY)
        gamestate.active_player.active_factions.update(self.card.active_factions)
        move_list_item(self.card,
                       gamestate.active_player[Zones.HAND],
                       gamestate.active_player[Zones.IN_PLAY])

        if self.card.card_type == CardTypes.SHIP:
            self.activate_ability(gamestate)


class ActivateBase(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.BASE)


class ActivateAlly(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.ALLY)


class ActivateScrap(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.SCRAP)

    def execute(self, gamestate):
        self.activate_ability(gamestate)  # Must occur before "moving" card because that move function clears abilities
        self.card.move_to(Zones.SCRAP_HEAP)
        gamestate.active_player[Zones.IN_PLAY].remove(self.card)
        gamestate.active_player.active_factions.subtract(self.card.active_factions)


class BuyCard(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is BUYING: {}".format(gamestate.active_player.name, self.card.name))

        gamestate.active_player[ValueTypes.TRADE] -= self.card.cost
        if self.card == Explorer:
            pass  # TODO (again)
        else:
            self.card.move_to(Zones.DISCARD, new_owner_id=gamestate.active_player.name)
            move_list_item(self.card, gamestate.trade_row, gamestate.active_player[Zones.DISCARD])
            gamestate.fill_trade_row()

        logging.warning("{} spent {} TRADE and has {} remaining".format(
            gamestate.active_player.name,
            self.card.cost,
            gamestate.active_player[ValueTypes.TRADE]))


class Attack(Move):
    def __init__(self, target):
        self.target = target

    def execute(self, gamestate):
        # Attack Base
        if isinstance(self.target, Card):
            logging.warning("{} is ATTACKING {} for {} damage!".format(
                gamestate.active_player.name,
                self.target.name,
                self.target.defense))

            gamestate.active_player[ValueTypes.DAMAGE] -= self.target.defense
            self.target.move_to(Zones.DISCARD)
            move_list_item(self.target, gamestate.opponent[Zones.IN_PLAY], gamestate.opponent[Zones.DISCARD])

            logging.warning("{} has {} DAMAGE remaining".format(
                gamestate.active_player.name,
                gamestate.active_player[ValueTypes.AUTHORITY]))

        # Attack Opponent
        else:
            logging.warning("{} is ATTACKING {} for {} damage!".format(
                gamestate.active_player.name,
                self.target.name,
                gamestate.active_player[ValueTypes.DAMAGE]))

            self.target[ValueTypes.AUTHORITY] -= gamestate.active_player[ValueTypes.DAMAGE]
            gamestate.active_player[ValueTypes.DAMAGE] = 0

            logging.warning("{} has {} AUTHORITY remaining".format(self.target.name,
                                                                   self.target[ValueTypes.AUTHORITY]))

            if gamestate.opponent[ValueTypes.AUTHORITY] <= 0:
                gamestate.victor = gamestate.active_player.name


class EndTurn(Move):
    def execute(self, gamestate):
        logging.warning("{} is ENDING THEIR TURN".format(gamestate.active_player.name))
        gamestate.next_turn()


class Discard(Move):
    def __init__(self, cards):
        self.cards = cards

    def execute(self, gamestate):
        assert isinstance(gamestate.pending_effect, PendDiscard)
        gamestate.pending_effect.resolve(self.cards)


class Choose(Move):
    def __init__(self, choice):
        self.choice = choice

    def execute(self, gamestate):
        assert isinstance(gamestate.pending_effect, PendChoice)
        assert self.choice in gamestate.pending_effect.choices
        gamestate.pending_effect.resolve(self.choice)


class Scrap(Move):
    def __init__(self, *targets):
        self.targets = targets

    def execute(self, gamestate):
        assert isinstance(gamestate.pending_effect, PendScrap)
        if gamestate.pending_effect.mandatory:
            assert len(self.targets) >= gamestate.pending_effect.up_to
        gamestate.pending_effect.resolve(self.targets)
