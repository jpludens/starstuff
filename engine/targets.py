from abc import ABC

from enums.enums import Zones, CardTypes


class Targeting(ABC):
    def __init__(self, exactly=None, up_to=None, card_types=None, zones=None):
        pass

    def get_targets(self, gamestate):
        raise NotImplementedError


class TargetEnemyBase(Targeting):
    def get_targets(self, gamestate):
        bases = []
        outposts = []

        for card in gamestate.inactive_player[Zones.IN_PLAY]:
            if card.card_type == CardTypes.BASE:
                bases.append(card)
            elif card.card_type == CardTypes.OUTPOST:
                outposts.append(card)

        return outposts if outposts else bases


class TargetTradeRow(Targeting):
    def get_targets(self, gamestate):
        return gamestate[Zones.TRADE_ROW]


class Target