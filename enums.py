from enum import Enum


class CardTypes(Enum):
    SHIP = "SHIP"
    BASE = "BASE"
    OUTPOST = "OUTPOST"


class ValueTypes(Enum):
    AUTHORITY = "AUTHORITY"
    TRADE = "TRADE"
    DAMAGE = "DAMAGE"


class Triggers(Enum):
    SHIP = "SHIP"
    BASE = "BASE"
    ALLY = "ALLY"
    SCRAP = "SCRAP"


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
    SCRAP = "SCRAP"
    CHOICE = "CHOICE"
    UNIMPLEMENTED = "UNIMPLEMENTED"


class PlayerIndicators(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
