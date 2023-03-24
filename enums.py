from enum import Enum


class CardTypes(Enum):
    SHIP = "SHIP"
    BASE = "BASE"
    OUTPOST = "OUTPOST"


class Values(Enum):
    AUTHORITY = "AUTHORITY"
    TRADE = "TRADE"
    DAMAGE = "DAMAGE"


class Actions(Enum):
    BUY = "BUY"
    PLAY = "PLAY"
    ALLY = "ALLY"
    SCRAP = "SCRAP"
    ATTACK = "ATTACK"
    END_TURN = "END_TURN"
    ACTIVATE_BASE = "ACTIVATE_BASE"


class Zones(Enum):
    DECK = "DECK"
    HAND = "HAND"
    IN_PLAY = "IN_PLAY"
    DISCARD = "DISCARD"
    TRADE_ROW = "TRADE_ROW"
    TRADE_DECK = "TRADE_DECK"


class Factions(Enum):
    BLOB = "BLOB"
    TRADE_FEDERATION = "TRADE_FEDERATION"
    MACHINE_CULT = "MACHINE_CULT"
    STAR_EMPIRE = "STAR_EMPIRE"


class Abilities(Enum):
    DRAW = "DRAW"
    CHOICE = "CHOICE"
    UNIMPLEMENTED = "UNIMPLEMENTED"
