import logging

from enums import Zones, PlayerIndicators


class Effect(object):
    def __init__(self, player_indicator):
        self.player_indicator = player_indicator

    def apply(self, gamestate):
        raise NotImplementedError


class ValueEffect(Effect):
    def __init__(self, player_indicator, value_type, amount):
        super().__init__(player_indicator)
        self.value_type = value_type
        self.amount = amount

    def apply(self, gamestate):
        player = gamestate.players[self.player_indicator]
        player[self.value_type] += self.amount
        logging.warning("{} GAINS {} {} ({})".format(
            player.name, self.amount, self.value_type.name, player[self.value_type]))


class DrawEffect(Effect):
    def __init__(self, player_indicator, amount):
        super().__init__(player_indicator)
        self.amount = amount

    def apply(self, gamestate):
        player = gamestate.players[self.player_indicator]
        for _ in range(self.amount):
            try:
                player.draw(1)
            except IndexError:
                logging.warning("{} DRAWS empty".format(player.name))
            else:
                logging.warning("{} DRAWS a card".format(player.name))


class ScrapEffect(Effect):
    class Parameters(object):
        def __init__(self, *zones, up_to=1, mandatory=False):
            self.zones = [z if z == Zones.TRADE_ROW else (PlayerIndicators.ACTIVE, z) for z in zones]
            self.up_to = up_to
            self.mandatory = mandatory

    def __init__(self, player_indicator, parameters):
        super().__init__(player_indicator)
        self.player_indicator = player_indicator
        self.zones = parameters.zones
        self.up_to = parameters.up_to
        self.mandatory = parameters.mandatory

        self.gamestate = None

    def apply(self, gamestate):
        self.gamestate = gamestate
        zone_names = [z.name if not isinstance(z, tuple) else z[1].name for z in self.zones]
        if any([gamestate[z] for z in self.zones]):
            gamestate.pending_scrap = self
            logging.warning("{} {} SCRAP from: {}".format(
                gamestate[self.player_indicator].name, "must" if self.mandatory else "can", zone_names))
        else:
            logging.warning("{} has no cards to scrap in: {}".format(
                gamestate[self.player_indicator].name, zone_names))

    def resolve(self, targets):
        if targets:
            assert len(targets) <= self.up_to

            for target in targets:
                for zone in self.zones:
                    # TODO This doesn't work because we're only specifying targets, not locations
                    # Either need to specify location as well, or include location info on cards
                    try:
                        self.gamestate[zone].remove(target)
                    except ValueError:
                        continue
                    else:
                        logging.warning("{} is scrapping {} from {}".format(
                            self.gamestate[self.player_indicator].name,
                            target.name,
                            zone.name if not isinstance(zone, tuple) else zone[1].name))
                        # TODO: Make the Trade Row an object that can handle this by itself,
                        # the act of scrapping shouldn't involve checking and filling the trade row
                        if zone == Zones.TRADE_ROW:
                            self.gamestate.fill_trade_row()
                        break
                else:
                    raise ValueError("bad target")

        elif self.mandatory:
            assert not self.mandatory
            logging.warning("{} doesn't scrap anything".format(self.gamestate[self.player_indicator].name))

        self.gamestate.pending_scrap = None


class ChoiceEffect(Effect):
    def __init__(self, player_indicator, choices):
        super().__init__(player_indicator)
        self.choices = choices
        self.gamestate = None

    def apply(self, gamestate):
        self.gamestate = gamestate
        gamestate.pending_choice = self
        # TODO: Reyclying Station: Adjust this log message
        player = gamestate.players[self.player_indicator]
        keys = list(self.choices.keys())
        logging.warning("{} can choose {} or {}".format(
            player.name, keys[0].name, keys[1].name))

    def resolve(self, choice):
        assert choice in self.choices
        self.choices[choice].apply(self.gamestate)
        self.gamestate.pending_choice = None
