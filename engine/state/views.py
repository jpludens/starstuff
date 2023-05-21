from collections import Counter
from enums.enums import ValueTypes, Zones, CardTypes


class GameStateView(object):
    def __init__(self, gamestate):
        self.turn_number = gamestate.turn_number
        self.trade_deck = sorted(gamestate.trade_deck, key=lambda c: c.name)
        self.trade_row = list(gamestate.trade_row)
        self.own_view = PlayerStateOwnView(gamestate)
        self.opponent_view = PlayerStateOpponentView(gamestate)
        self.pending_effects = gamestate.pending_effects


class PlayerStateOwnView(object):
    def __init__(self, gamestate):
        self.authority = gamestate.active_player[ValueTypes.AUTHORITY]
        self.trade = gamestate.active_player[ValueTypes.TRADE]
        self.damage = gamestate.active_player[ValueTypes.DAMAGE]

        self.deck = sorted(gamestate.active_player[Zones.DECK], key=lambda c: c.name)
        self.hand = list(gamestate.active_player[Zones.HAND])
        self.discard = list(gamestate.active_player[Zones.DISCARD])

        self.cards_on_table = list(gamestate[Zones.IN_PLAY])
        self.ships = []
        self.bases = []
        for card in gamestate[Zones.IN_PLAY]:
            if card.card_type == CardTypes.SHIP:
                self.ships.append(card)
            else:
                self.bases.append(card)
        self.active_factions = Counter(gamestate.active_player.active_factions)


class PlayerStateOpponentView(object):
    def __init__(self, gamestate):
        self.authority = gamestate.inactive_player[ValueTypes.AUTHORITY]

        self.deck = []
        self.hand = 0
        self.discard = []
        self.deck = sorted(gamestate.inactive_player[Zones.DECK], key=lambda c: c.name)
        self.discard = list(gamestate.active_player[Zones.DISCARD])

        self.cards_on_table = list(gamestate.inactive_player[Zones.IN_PLAY])
        self.bases = []
        self.outposts = []
        for card in gamestate.inactive_player[Zones.IN_PLAY]:
            if card.card_type == CardTypes.BASE:
                self.bases.append(card)
            elif card.card_type == CardTypes.OUTPOST:
                self.outposts.append(card)
            else:
                raise RuntimeError("Found non-BASE non-OUTPOST card in play for inactive player")
