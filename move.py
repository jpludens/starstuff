import logging

from cards import Explorer, Card
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
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is PLAYING: {}".format(gamestate.active_player.name, self.card.name))
        move_list_item(self.card,
                       gamestate.active_player[Zones.HAND],
                       gamestate.active_player[Zones.IN_PLAY])
        self.card.initialize_in_play()

        gamestate.active_player.active_factions.update(self.card.active_factions)
        if self.card.card_type == CardTypes.SHIP:
            self.activate_ability(gamestate)


class ActivateBase(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.BASE)
        self.card = card


class ActivateAlly(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.ALLY)
        self.card = card


class ActivateScrap(AbilityActivation):
    def __init__(self, card):
        super().__init__(card, Triggers.SCRAP)
        self.card = card

    def execute(self, gamestate):
        gamestate.active_player[Zones.IN_PLAY].remove(self.card)
        gamestate.active_player.active_factions.subtract(self.card.active_factions)
        self.activate_ability(gamestate)


class BuyCard(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is BUYING: {}".format(gamestate.active_player.name, self.card.name))

        gamestate.active_player[ValueTypes.TRADE] -= self.card.cost
        logging.warning("{} spent {} TRADE and has {} remaining".format(
            gamestate.active_player.name,
            self.card.cost,
            gamestate.active_player[ValueTypes.TRADE]))

        if self.card == Explorer:
            # TODO: Explorers aren't working
            gamestate.active_player[Zones.DISCARD].append(self.card())
        else:
            move_list_item(self.card, gamestate.trade_row, gamestate.active_player[Zones.DISCARD])
            gamestate.fill_trade_row()


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
            gamestate.opponent.destroy_base(self.target)
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


class Choose(Move):
    def __init__(self, choice):
        self.choice = choice

    def execute(self, gamestate):
        logging.warning("{} is CHOOSING {}".format(gamestate.active_player.name, self.choice.name))
        gamestate.pending_choice.resolve(self.choice)


class Scrap(Move):
    def __init__(self, *targets):
        self.targets = targets

    def execute(self, gamestate):
        if gamestate.pending_scrap is None:
            logging.error("Scrap Move provided without pending Scrap Effect"
                          " or when a Scrap Effect has no possible targets")
            raise RuntimeError
        gamestate.pending_scrap.resolve(self.targets)


class Target(Move):
    def execute(self, gamestate):
        pass


class Discard(Move):
    def execute(self, gamestate):
        pass
