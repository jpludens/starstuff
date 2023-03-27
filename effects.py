import logging

from enums import Zones


class Effect(object):
    def apply(self, gamestate):
        raise NotImplementedError


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


class ForceDiscardEffect(Effect):
    def apply(self, gamestate):
        if gamestate.forced_discards:
            gamestate.forced_discards += 1
            logging.warning("{} must now DISCARD {} cards".format(gamestate.opponent.name, gamestate.forced_discards))
        else:
            gamestate.forced_discards = 1
            logging.warning("{} must DISCARD 1 card".format(gamestate.opponent.name))


class ScrapEffect(Effect):
    def __init__(self, *zones, up_to=1, mandatory=False):
        super().__init__()
        self.zones = list(zones)
        self.up_to = up_to
        self.mandatory = mandatory

        self.gamestate = None

    def apply(self, gamestate):
        self.gamestate = gamestate
        zone_names = [z.name for z in self.zones]
        if any([gamestate[z] for z in self.zones]):
            gamestate.pending_scrap = self
            logging.warning("{} {} SCRAP from: {}".format(
                gamestate.active_player.name, "must" if self.mandatory else "can", zone_names))
        else:
            logging.warning("{} has no cards to scrap in: {}".format(
                gamestate.active_player.name, zone_names))

    def resolve(self, targets):
        if targets:
            assert len(targets) <= self.up_to

            for target in targets:
                origin_zone = target.location
                logging.warning("{} is scrapping {} from {}".format(
                    self.gamestate.active_player.name,
                    target.name,
                    origin_zone.name))

                target.move_to(Zones.SCRAP_HEAP)
                self.gamestate[origin_zone].remove(target)
                if origin_zone == Zones.TRADE_ROW:
                    self.gamestate.fill_trade_row()

        else:
            logging.warning("{} doesn't scrap anything".format(self.gamestate.active_player.name))

        self.gamestate.pending_scrap = None
        self.gamestate = None


class ChoiceEffect(Effect):
    def __init__(self, choices):
        super().__init__()
        self.choices = choices
        self.gamestate = None

    def apply(self, gamestate):
        self.gamestate = gamestate
        gamestate.pending_choice = self
        # TODO: Reyclying Station: Adjust this log message
        keys = list(self.choices.keys())
        logging.warning("{} can choose {} or {}".format(
            gamestate.active_player.name, keys[0].name, keys[1].name))

    def resolve(self, choice):
        assert choice in self.choices
        self.choices[choice].apply(self.gamestate)
        self.gamestate.pending_choice = None
        self.gamestate = None
