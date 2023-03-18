from enums import Actions, CardAttrs, Factions, Values


class Card(object):
    data = {}


# Boring Ships
class Scout(Card):
    data = {
        CardAttrs.NAME: "Scout",
        CardAttrs.COST: 0,
        Actions.PLAY: {
            Values.TRADE: 1
        }
    }


class Viper(Card):
    data = {
        CardAttrs.NAME: "Viper",
        CardAttrs.COST: 0,
        Actions.PLAY: {
            Values.DAMAGE: 1
        }
    }


class Explorer(Card):
    data = {
        CardAttrs.NAME: "Explorer",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.TRADE: 2
        },
        Actions.SCRAP: {
            Values.DAMAGE: 2
        }
    }


# Blob Ships
class BlobFighter(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Blob Fighter",
        CardAttrs.COST: 1,
        Actions.PLAY: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Draw"
        }
    }


class TradePod(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Trade Pod",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.TRADE: 3
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        }
    }


class BattlePod(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Battle Pod",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.DAMAGE: 4
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        }
    }


class Ram(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Ram",
        CardAttrs.COST: 3,
        Actions.PLAY: {
            Values.DAMAGE: 5
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        },
        Actions.SCRAP: {
            Values.TRADE: 3
        }
    }


class BlobDestroyer(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Blob Destroyer",
        CardAttrs.COST: 4,
        Actions.PLAY: {
            Values.DAMAGE: 6
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Blob Destroyer"
        }
    }


class BlobCarrier(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Blob Carrier",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 7
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Blob Carrier"
        }
    }


class BattleBlob(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Battle Blob",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 8
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Draw"
        },
        Actions.SCRAP: {
            Values.DAMAGE: 4
        }
    }


class Mothership(Card):
    data = {
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Mothership",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 6,
            CardAttrs.ABILITY: "Draw"
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Draw"
        }
    }


# Federation Ships
class FederationShuttle(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Federation Shuttle",
        CardAttrs.COST: 1,
        Actions.PLAY: {
            Values.TRADE: 2,
        },
        Actions.ALLY: {
            Values.AUTHORITY: 4,
        }
    }


class Cutter(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Cutter",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.TRADE: 2,
        },
        Actions.ALLY: {
            Values.DAMAGE: 4,
        }
    }


class EmbassyYacht(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Embassy Yacht",
        CardAttrs.COST: 3,
        Actions.PLAY: {
            Values.AUTHORITY: 3,
            Values.TRADE: 2,
            CardAttrs.ABILITY: "Embassy Draw"
        }
    }


class Freighter(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Freighter",
        CardAttrs.COST: 4,
        Actions.PLAY: {
            Values.TRADE: 4,
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Shop To Top"
        }
    }


class TradeEscort(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Trade Escort",
        CardAttrs.COST: 5,
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.DAMAGE: 4,
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Draw"
        }
    }


class Flagship(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Flagship",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 5,
            CardAttrs.ABILITY: "Draw"
        },
        Actions.ALLY: {
            Values.AUTHORITY: 5,
        }
    }


class CommandShip(Card):
    data = {
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Command Ship",
        CardAttrs.COST: 8,
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.DAMAGE: 5,
            CardAttrs.ABILITY: "Draw TWO"
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Blow Base"
        }
    }


class TradeBot(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Trade Bot",
        CardAttrs.COST: 1,
        Actions.PLAY: {
            Values.TRADE: 1,
            CardAttrs.ABILITY: Actions.SCRAP
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class MissileBot(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Missile Bot",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.DAMAGE: 2,
            CardAttrs.ABILITY: Actions.SCRAP
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class SupplyBot(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Supply Bot",
        CardAttrs.COST: 3,
        Actions.PLAY: {
            Values.TRADE: 2,
            CardAttrs.ABILITY: Actions.SCRAP
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class PatrolMech(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Patrol Mech",
        CardAttrs.COST: 4,
        Actions.PLAY: {
            CardAttrs.ABILITY: "Patrol Mech Choice"
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: Actions.SCRAP
        }
    }


class StealthNeedle(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Stealth Needle",
        CardAttrs.COST: 4,
        Actions.PLAY: {
            CardAttrs.ABILITY: "Stealth Needle"
        }
    }


class BattleMech(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Battle Mech",
        CardAttrs.COST: 5,
        Actions.PLAY: {
            Values.DAMAGE: 4,
            CardAttrs.ABILITY: Actions.SCRAP
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Draw"
        }
    }


class MissileMech(Card):
    data = {
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Missile Mech",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 6,
            CardAttrs.ABILITY: "Blow Base"
        },
        Actions.ALLY: {
            Values.AUTHORITY: 0,
            Values.TRADE: 2,
            Values.DAMAGE: 0,
            CardAttrs.ABILITY: "Draw"
        }
    }


class ImperialFighter(Card):
    data = {
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Imperial Fighter",
        CardAttrs.COST: 1,
        Actions.PLAY: {
            Values.DAMAGE: 2,
            CardAttrs.ABILITY: "Discard"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class Corvette(Card):
    data = {
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Corvette",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.DAMAGE: 1,
            CardAttrs.ABILITY: "Draw"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class SurveyShip(Card):
    data = {
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Survey Ship",
        CardAttrs.COST: 3,
        Actions.PLAY: {
            Values.TRADE: 3,
            CardAttrs.ABILITY: "Draw"
        },
        Actions.SCRAP: {
            CardAttrs.ABILITY: "Discard"
        }
    }


class ImperialFrigate(Card):
    data = {
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Imperial Frigate",
        CardAttrs.COST: 3,
        Actions.PLAY: {
            Values.DAMAGE: 4,
            CardAttrs.ABILITY: "Discard"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        },
        Actions.SCRAP: {
            CardAttrs.ABILITY: "Draw"
        }

    }


class BattleCruiser(Card):
    data = {
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "BattleCruiser",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 6,
            CardAttrs.ABILITY: "Draw"
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Discard"
        },
        Actions.SCRAP: {
            CardAttrs.ABILITY: "Draw AND Blow Base",
        }
    }


class Dreadnought(Card):
    data = {
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Dreadnought",
        CardAttrs.COST: 7,
        Actions.PLAY: {
            Values.DAMAGE: 7,
            CardAttrs.ABILITY: "Draw"
        },
        Actions.SCRAP: {
            Values.DAMAGE: 5,
        }
    }
