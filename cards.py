class Card(object):
    cost = 0
    trade = 0
    damage = 0


class Scout(Card):
    trade = 1


class Viper(Card):
    damage = 1


class Explorer(Card):
    cost = 2
    trade = 2
    scrap_damage = 2
