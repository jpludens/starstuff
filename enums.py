from enum import Enum


class CardAttrs(Enum):
    NAME = "NAME"
    COST = "COST"
NAME = CardAttrs.NAME
COST = CardAttrs.COST


class Values(Enum):
    AUTHORITY = "Authority"
    TRADE = "Trade"
    DAMAGE = "Damage"
AUTHORITY = Values.AUTHORITY
TRADE = Values.TRADE
DAMAGE = Values.DAMAGE


class Actions(Enum):
    BUY = "BUY"
    PLAY = "PLAY"
    SCRAP = "SCRAP"
    ATTACK = "ATTACK"
    END_TURN = "END_TURN"
BUY = Actions.BUY
PLAY = Actions.PLAY
SCRAP = Actions.SCRAP
ATTACK = Actions.ATTACK
END_TURN = Actions.END_TURN


class Zones(Enum):
    DECK = "DECK"
    HAND = "HAND"
    IN_PLAY = "IN_PLAY"
    DISCARD = "DISCARD"
    TRADE_ROW = "TRADE_ROW"
    TRADE_DECK = "TRADE_DECK"
DECK = Zones.DECK
HAND = Zones.HAND
IN_PLAY = Zones.IN_PLAY
DISCARD = Zones.DISCARD
TRADE_ROW = Zones.TRADE_ROW
TRADE_DECK = Zones.TRADE_DECK
