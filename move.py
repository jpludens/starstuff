import logging

from cards import Explorer, Card
from enums import Zones, CardTypes, Triggers, ValueTypes, PlayerIndicators
from util import move_list_item


class Move(object):
    def execute(self, gamestate):
        raise NotImplementedError


# TODO: Add a 'choice' parameter to execute
# TODO: abstract common Moves behavior to a CardMove or something
class PlayCard(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is PLAYING: {}".format(gamestate[PlayerIndicators.ACTIVE].name, self.card.name))
        move_list_item(self.card,
                       gamestate[PlayerIndicators.ACTIVE][Zones.HAND],
                       gamestate[PlayerIndicators.ACTIVE][Zones.IN_PLAY])
        self.card.initialize_in_play()

        gamestate[PlayerIndicators.ACTIVE].active_factions.update(self.card.active_factions)
        if self.card.card_type == CardTypes.SHIP:
            for effect in self.card.trigger_ability(Triggers.SHIP):
                effect.apply(gamestate)


class ActivateBase(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is ACTIVATING: {}".format(gamestate[PlayerIndicators.ACTIVE].name, self.card.name))
        for effect in self.card.trigger_ability(Triggers.BASE):
            effect.apply(gamestate)


class ActivateAlly(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is TRIGGERING {}'s Ally Ability".format(
            gamestate[PlayerIndicators.ACTIVE].name, self.card.name))
        for effect in self.card.trigger_ability(Triggers.ALLY):
            effect.apply(gamestate)


class ActivateScrap(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is SCRAPPING: {}".format(gamestate[PlayerIndicators.ACTIVE].name, self.card.name))
        gamestate[PlayerIndicators.ACTIVE][Zones.IN_PLAY].remove(self.card)
        gamestate[PlayerIndicators.ACTIVE].active_factions.subtract(self.card.active_factions)
        for effect in self.card.trigger_ability(Triggers.SCRAP):
            effect.apply(gamestate)


class BuyCard(Move):
    def __init__(self, card):
        self.card = card

    def execute(self, gamestate):
        logging.warning("{} is BUYING: {}".format(gamestate[PlayerIndicators.ACTIVE].name, self.card.name))

        gamestate[PlayerIndicators.ACTIVE][ValueTypes.TRADE] -= self.card.cost
        logging.warning("{} spent {} TRADE and has {} remaining".format(
            gamestate[PlayerIndicators.ACTIVE].name,
            self.card.cost,
            gamestate[PlayerIndicators.ACTIVE][ValueTypes.TRADE]))

        if self.card == Explorer:
            # TODO: Explorers aren't working
            gamestate[PlayerIndicators.ACTIVE][Zones.DISCARD].append(self.card())
        else:
            move_list_item(self.card, gamestate.trade_row, gamestate[PlayerIndicators.ACTIVE][Zones.DISCARD])
            gamestate.fill_trade_row()


class Attack(Move):
    def __init__(self, target):
        self.target = target

    def execute(self, gamestate):
        # Attack Base
        if isinstance(self.target, Card):
            logging.warning("{} is ATTACKING {} for {} damage!".format(
                gamestate[PlayerIndicators.ACTIVE].name,
                self.target.name,
                self.target.defense))
            gamestate[PlayerIndicators.INACTIVE].destroy_base(self.target)
            logging.warning("{} has {} DAMAGE remaining".format(
                gamestate[PlayerIndicators.ACTIVE].name,
                gamestate[PlayerIndicators.ACTIVE][ValueTypes.AUTHORITY]))

        # Attack Opponent
        else:
            logging.warning("{} is ATTACKING {} for {} damage!".format(
                gamestate[PlayerIndicators.ACTIVE].name,
                self.target.name,
                gamestate[PlayerIndicators.ACTIVE][ValueTypes.DAMAGE]))
            self.target[ValueTypes.AUTHORITY] -= gamestate[PlayerIndicators.ACTIVE][ValueTypes.DAMAGE]
            gamestate[PlayerIndicators.ACTIVE][ValueTypes.DAMAGE] = 0
            logging.warning("{} has {} AUTHORITY remaining".format(self.target.name,
                                                                   self.target[ValueTypes.AUTHORITY]))

            if gamestate[PlayerIndicators.INACTIVE][ValueTypes.AUTHORITY] <= 0:
                gamestate.victor = gamestate[PlayerIndicators.ACTIVE].name


class EndTurn(Move):
    def execute(self, gamestate):
        logging.warning("{} is ENDING THEIR TURN".format(gamestate[PlayerIndicators.ACTIVE].name))
        gamestate.next_turn()


class Choose(Move):
    def __init__(self, choice):
        self.choice = choice

    def execute(self, gamestate):
        logging.warning("{} is CHOOSING {}".format(gamestate[PlayerIndicators.ACTIVE].name, self.choice.name))
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
