import logging
from abc import ABC

from enums import Zones
from util import move_list_item


class Effect(object):
    def apply(self, gamestate):
        raise NotImplementedError


# Immediate Effects
class ValueEffect(Effect):
    def __init__(self, value_type, amount):
        super().__init__()
        self.value_type = value_type
        self.amount = amount

    def apply(self, gamestate):
        player = gamestate.active_player
        player[self.value_type] += self.amount
        logging.warning("{} GAINS {} {} ({})".format(
            player.name, self.amount, self.value_type.name, player[self.value_type]))


class DrawEffect(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def apply(self, gamestate):
        player = gamestate.active_player
        for _ in range(self.amount):
            try:
                player.draw(1)
            except IndexError:
                logging.warning("{} DRAWS empty".format(player.name))
            else:
                logging.warning("{} DRAWS a card".format(player.name))


class OpponentDiscardEffect(Effect):
    def apply(self, gamestate):
        if gamestate.forced_discards:
            gamestate.forced_discards += 1
            logging.warning("{} must now DISCARD {} cards at start of turn".format(
                gamestate.opponent.name, gamestate.forced_discards))
        else:
            gamestate.forced_discards = 1
            logging.warning("{} must DISCARD 1 card at start of turn".format(gamestate.opponent.name))


class GainFactionEffect(Effect):
    def __init__(self, *factions):
        self.factions = factions

    def apply(self, gamestate):
        gamestate.active_player.active_factions.update(self.factions)
        gamestate.last_activated_card.active_factions.update(self.factions)


# Pending Effects (requiring additional input from a player)
class PendEffect(Effect, ABC):
    def __init__(self):
        self.gamestate = None

    def apply(self, gamestate):
        self.gamestate = gamestate
        gamestate.pending_effect = self

    def resolve(self, *args, **kwargs):
        self._resolve(*args, **kwargs)
        if self.gamestate.pending_effect == self:  # This line almost on its own supports nesting effects
            self.gamestate.pending_effect = None
        self.gamestate = None

    def _resolve(self, *args, **kwargs):
        raise NotImplementedError


class ChoiceEffect(Effect):
    def __init__(self, choice):
        self.choice = choice

    def apply(self, gamestate):
        self.choice.apply(gamestate)


class PendChoice(PendEffect):
    def __init__(self, choices):
        super().__init__()
        self.choices = choices

    def apply(self, gamestate):
        super().apply(gamestate)
        # TODO: Adjust this log message for Recycling Station (the only Choice that is not a ValueEffect w named key)
        keys = list(self.choices.keys())
        logging.warning("{} can choose {} or {}".format(
            gamestate.active_player.name, keys[0].name, keys[1].name))

    def _resolve(self, choice):
        logging.warning("{} is CHOOSING {}".format(self.gamestate.active_player.name, choice.name))
        ChoiceEffect(self.choices[choice]).apply(self.gamestate)


class ScrapEffect(Effect):
    def __init__(self, cards):
        self.cards = cards

    def apply(self, gamestate):
        if self.cards:
            for card in self.cards:
                origin_zone = card.location
                logging.warning("{} is scrapping {} from {}".format(
                    gamestate.active_player.name,
                    card.name,
                    origin_zone.name))

                card.move_to(Zones.SCRAP_HEAP)
                gamestate[origin_zone].remove(card)
                if origin_zone == Zones.TRADE_ROW:
                    gamestate.fill_trade_row()

        else:
            logging.warning("{} doesn't scrap anything".format(gamestate.active_player.name))


class PendScrap(PendEffect):
    def __init__(self, *zones, up_to=1, mandatory=False):
        super().__init__()
        self.zones = list(zones)
        self.up_to = up_to
        self.mandatory = mandatory

    def apply(self, gamestate):
        zone_names = [z.name for z in self.zones]
        if any([gamestate[z] for z in self.zones]):
            super().apply(gamestate)
            logging.warning("{} {} SCRAP from: {}".format(
                gamestate.active_player.name, "must" if self.mandatory else "can", zone_names))
        else:
            logging.warning("{} has no cards to scrap in: {}".format(
                gamestate.active_player.name, zone_names))

    def _resolve(self, cards):
        ScrapEffect(cards).apply(self.gamestate)


class PendBrainWorld(PendScrap):
    def __init__(self):
        super().__init__(Zones.HAND, Zones.DISCARD, up_to=2, mandatory=False)

    def _resolve(self, scraps):
        ScrapEffect(scraps).apply(self.gamestate)
        DrawEffect(len(scraps)).apply(self.gamestate)


class DiscardEffect(Effect):
    def __init__(self, cards):
        self.cards = cards

    def apply(self, gamestate):
        if self.cards:
            for card in self.cards:
                logging.warning("{} DISCARDS {}".format(gamestate.active_player.name, card.name))
                card.move_to(Zones.DISCARD)
                move_list_item(card, gamestate[Zones.HAND], gamestate[Zones.DISCARD])
        else:
            logging.warning("{} DOESN'T DISCARD".format(gamestate.active_player.name))


class PendDiscard(PendEffect):
    def __init__(self, up_to=1, mandatory=False):
        super().__init__()
        self.up_to = up_to
        self.mandatory = mandatory

    def apply(self, gamestate):
        super().apply(gamestate)
        if self.mandatory:
            logging.warning("{} must DISCARD {}".format(gamestate.active_player.name, self.up_to))
        else:
            logging.warning("{} can DISCARD up to {}".format(gamestate.active_player.name, self.up_to))

    def _resolve(self, cards):
        DiscardEffect(cards).apply(self.gamestate)


class PendRecycle(PendDiscard):
    def __init__(self):
        super().__init__(up_to=2, mandatory=False)

    def _resolve(self, discards):
        DiscardEffect(discards).apply(self.gamestate)
        DrawEffect(len(discards)).apply(self.gamestate)
