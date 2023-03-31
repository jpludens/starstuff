import logging
from abc import ABC

from enums import Zones, ValueTypes, Triggers, CardTypes, Factions
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

    def __str__(self):
        return "{} {}".format(self.amount, self.value_type.name)


class GainAuthority(ValueEffect):
    def __init__(self, amount):
        super().__init__(ValueTypes.AUTHORITY, amount)


class GainDamage(ValueEffect):
    def __init__(self, amount):
        super().__init__(ValueTypes.DAMAGE, amount)


class GainTrade(ValueEffect):
    def __init__(self, amount):
        super().__init__(ValueTypes.TRADE, amount)


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


class AcquireEffect(Effect):
    def __init__(self, card, top_of_deck=False):
        self.card = card
        self.top_of_deck = top_of_deck

    def apply(self, gamestate):
        if self.top_of_deck:
            zone = Zones.DECK
            suffix = " to top of deck"
        else:
            zone = Zones.DISCARD
            suffix = ""

        logging.warning("{} ACQUIRES {}{}".format(gamestate.active_player.name, self.card.name, suffix))

        gamestate.remove_from_trade_row(self.card)
        self.card.move_to(zone, new_owner_id=gamestate.active_player.name)
        gamestate.active_player[zone].append(self.card)


class DiscardEffect(Effect):
    def __init__(self, cards):
        self.cards = cards

    def apply(self, gamestate):
        if self.cards:
            for card in self.cards:
                logging.warning("{} DISCARDS {}".format(
                    gamestate.active_player.name, [card.name for card in self.cards]))
                card.move_to(Zones.DISCARD)
                move_list_item(card, gamestate[Zones.HAND], gamestate[Zones.DISCARD])
        else:
            logging.warning("{} DOESN'T DISCARD".format(gamestate.active_player.name))


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


class DestroyBaseEffect(Effect):
    def __init__(self, base=None):
        self.base = base

    def apply(self, gamestate):
        if self.base:
            logging.warning("{} DESTROYS {}".format(gamestate.active_player.name, self.base.name))
            self.base.move_to(Zones.DISCARD)
            move_list_item(self.base,
                           gamestate.opponent[Zones.IN_PLAY],
                           gamestate.opponent[Zones.DISCARD])
        else:
            logging.warning("{} does not destroy a base".format(gamestate.active_player.name))


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


class CopyShipEffect(Effect):
    def __init__(self, ship):
        self.ship = ship

    def apply(self, gamestate):
        logging.warning("{} COPIES {}".format(gamestate.active_player.name, self.ship.name))
        needle = gamestate.last_activated_card
        needle.available_abilities.update(self.ship.abilities)
        for effect in needle.trigger_ability(Triggers.SHIP):
            effect.apply(gamestate)
        if self.ship.faction != Factions.MACHINE_CULT:
            needle.active_factions.update([self.ship.faction])
            gamestate.active_player.active_factions.update([self.ship.faction])


class MachineBaseEffect(Effect):
    def apply(self, gamestate):
        DrawEffect(1).apply(gamestate)
        PendScrap(Zones.HAND, mandatory=True).apply(gamestate)


class BlobWorldDrawEffect(Effect):
    def apply(self, gamestate):
        DrawEffect(gamestate.blob_cards_played_this_turn).apply(gamestate)


class ShopToTopEffect(Effect):
    def apply(self, gamestate):
        gamestate.freighter_hauls += 1


class EmbassyYachtDrawEffect(Effect):
    def apply(self, gamestate):
        if len([c for c in gamestate[Zones.IN_PLAY] if c.card_type in [CardTypes.BASE, CardTypes.OUTPOST]]) >= 2:
            DrawEffect(2).apply(gamestate)


# Pending Effects (requiring additional input from a player)
class PendEffect(Effect, ABC):
    def __init__(self):
        self.gamestate = None

    def apply(self, gamestate):
        self.gamestate = gamestate
        gamestate.pending_effects.append(self)

    def resolve(self, *args, **kwargs):
        self._resolve(*args, **kwargs)
        self.gamestate.pending_effects.remove(self)
        self.gamestate = None

    def _resolve(self, *args, **kwargs):
        raise NotImplementedError


class PendDestroyBase(PendEffect):
    def apply(self, gamestate):
        if any(gamestate.opponent[Zones.IN_PLAY]):
            logging.warning("{} can DESTROY a Base".format(gamestate.active_player.name))
            super().apply(gamestate)

    def _resolve(self, base):
        DestroyBaseEffect(base).apply(self.gamestate)


class PendChoice(PendEffect):
    def __init__(self, choices):
        super().__init__()
        self.choices = {type(c): c for c in choices}

    def apply(self, gamestate):
        super().apply(gamestate)
        logging.warning("{} can choose: {}".format(gamestate.active_player.name, self.choices))

    def _resolve(self, choice):
        logging.warning("{} is CHOOSING {}".format(self.gamestate.active_player.name, choice.__name__))
        self.choices[choice].apply(self.gamestate)


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


class PendCopyShip(PendEffect):
    def apply(self, gamestate):
        if len([c for c in gamestate[Zones.IN_PLAY] if c.card_type == CardTypes.SHIP]) > 1:
            super().apply(gamestate)
        logging.warning("{} can COPY A SHIP".format(gamestate.active_player.name))

    def _resolve(self, ship):
        CopyShipEffect(ship).apply(self.gamestate)


class PendAcquireShipToTopForFree(PendEffect):
    def apply(self, gamestate):
        super().apply(gamestate)
        logging.warning("{} can ACQUIRE A FREE SHIP TO TOP OF DECK".format(gamestate.active_player.name))

    def _resolve(self, ship):
        AcquireEffect(ship, top_of_deck=True).apply(self.gamestate)
