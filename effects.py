import logging


class Effect(object):
    def __init__(self):
        pass

    def apply(self, gamestate):
        raise NotImplementedError


class ValueEffect(Effect):
    def __init__(self, player_indicator, value_type, amount):
        super().__init__()
        self.player_indicator = player_indicator
        self.value_type = value_type
        self.amount = amount

    def apply(self, gamestate):
        player = gamestate.players[self.player_indicator]
        player[self.value_type] += self.amount
        logging.warning("Adding {} to {}'s {} for a total of {}".format(self.amount,
                                                                        player.name,
                                                                        self.value_type.name,
                                                                        player[self.value_type]))


class DrawEffect(Effect):
    def __init__(self, player_indicator, amount):
        super().__init__()
        self.player_indicator = player_indicator
        self.amount = amount

    def apply(self, gamestate):
        player = gamestate.players[self.player_indicator]
        logging.warning("{} DRAWS {} card{}".format(player.name, self.amount, 's' if self.amount > 1 else ''))
        player.draw(self.amount)


class ChoiceEffect(Effect):
    def __init__(self, player_indicator, choices):
        super().__init__()
        self.player_indicator = player_indicator
        self.choices = choices

    def apply(self, gamestate):
        gamestate.pending_choice = self.choices
        player = gamestate.players[self.player_indicator]
        keys = list(self.choices.keys())
        logging.warning("{} can choose {} {} or {} {}".format(
            player.name, self.choices[keys[0]], keys[0].name, self.choices[keys[1]], keys[1].name))
