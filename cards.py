from enums import Abilities, Actions, CardAttrs, Factions, Values


class Card(object):
    data = {}


# Boring Ships
class Scout(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.NAME: "Scout",
        CardAttrs.COST: 0,
        Actions.PLAY: {
            Values.TRADE: 1
        }
    }


class Viper(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.NAME: "Viper",
        CardAttrs.COST: 0,
        Actions.PLAY: {
            Values.DAMAGE: 1
        }
    }


class Explorer(Card):
    data = {
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Blob Fighter",
        CardAttrs.COST: 1,
        Actions.PLAY: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class TradePod(Card):
    data = {
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Battle Blob",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 8
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        },
        Actions.SCRAP: {
            Values.DAMAGE: 4
        }
    }


class Mothership(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Mothership",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 6,
            Abilities.DRAW: 1
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


# Blob Bases
class BlobWheel(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Blob Wheel",
        CardAttrs.COST: 3,
        CardAttrs.DEFENSE: 5,
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 1,
        },
        Actions.SCRAP: {
            Values.TRADE: 3
        }
    }


class TheHive(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "The Hive",
        CardAttrs.COST: 5,
        CardAttrs.DEFENSE: 5,
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 3,
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class BlobWorld(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.FACTION: Factions.BLOB,
        CardAttrs.NAME: "Blob World",
        CardAttrs.COST: 8,
        CardAttrs.DEFENSE: 8,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "Blob World Choice"
        }
    }


# Federation Ships
class FederationShuttle(Card):
    data = {
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Trade Escort",
        CardAttrs.COST: 5,
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.DAMAGE: 4,
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class Flagship(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Flagship",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 5,
            Abilities.DRAW: 1
        },
        Actions.ALLY: {
            Values.AUTHORITY: 5,
        }
    }


class CommandShip(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Command Ship",
        CardAttrs.COST: 8,
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.DAMAGE: 5,
            Abilities.DRAW: 2
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Blow Base"
        }
    }


# Trade Federation Bases
class TradingPost(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Trading Post",
        CardAttrs.COST: 3,
        CardAttrs.DEFENSE: 4,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "1 Authority or Trade"
        },
        Actions.SCRAP: {
            Values.DAMAGE: 3
        }
    }


class BarterWorld(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Barter World",
        CardAttrs.COST: 4,
        CardAttrs.DEFENSE: 4,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "2 Authority or Trade"
        },
        Actions.SCRAP: {
            Values.DAMAGE: 5
        }
    }


class DefenseCenter(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Defense Center",
        CardAttrs.COST: 5,
        CardAttrs.DEFENSE: 5,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "3 Authority or 2 Damage"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        }
    }


class PortOfCall(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Port Of Call",
        CardAttrs.COST: 6,
        CardAttrs.DEFENSE: 6,
        Actions.ACTIVATE_BASE: {
            Values.TRADE: 3
        },
        Actions.SCRAP: {
            Abilities.DRAW: 1,
            CardAttrs.ABILITY: "Blow Base"
        }
    }


class CentralOffice(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.FACTION: Factions.TRADE_FEDERATION,
        CardAttrs.NAME: "Central Office",
        CardAttrs.COST: 7,
        CardAttrs.DEFENSE: 6,
        Actions.ACTIVATE_BASE: {
            Values.TRADE: 2,
            CardAttrs.ABILITY: "Freighter"
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


# Machine Cult Ships
class TradeBot(Card):
    data = {
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Stealth Needle",
        CardAttrs.COST: 4,
        Actions.PLAY: {
            CardAttrs.ABILITY: "Stealth Needle"
        }
    }


class BattleMech(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Battle Mech",
        CardAttrs.COST: 5,
        Actions.PLAY: {
            Values.DAMAGE: 4,
            CardAttrs.ABILITY: Actions.SCRAP
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class MissileMech(Card):
    data = {
        CardAttrs.SHIP: True,
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
            Abilities.DRAW: 1
        }
    }


# Machine Cult Bases
class BattleStation(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Battle Station",
        CardAttrs.COST: 3,
        CardAttrs.DEFENSE: 5,
        Actions.SCRAP: {
            Values.DAMAGE: 5,
        }
    }


class MechWorld(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Mech World",
        CardAttrs.COST: 5,
        CardAttrs.DEFENSE: 6,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "Mech World"
        }
    }


class Junkyard(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Junkyard",
        CardAttrs.COST: 6,
        CardAttrs.DEFENSE: 5,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: Actions.SCRAP
        }
    }


class MachineBase(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "MachineBase",
        CardAttrs.COST: 7,
        CardAttrs.DEFENSE: 6,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "Machine Base"
        }
    }


class BrainWorld(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.MACHINE_CULT,
        CardAttrs.NAME: "Brain World",
        CardAttrs.COST: 8,
        CardAttrs.DEFENSE: 6,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "Brain World"
        }
    }


# Star Empire Ships
class ImperialFighter(Card):
    data = {
        CardAttrs.SHIP: True,
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
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Corvette",
        CardAttrs.COST: 2,
        Actions.PLAY: {
            Values.DAMAGE: 1,
            Abilities.DRAW: 1
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class SurveyShip(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Survey Ship",
        CardAttrs.COST: 3,
        Actions.PLAY: {
            Values.TRADE: 3,
            Abilities.DRAW: 1
        },
        Actions.SCRAP: {
            CardAttrs.ABILITY: "Discard"
        }
    }


class ImperialFrigate(Card):
    data = {
        CardAttrs.SHIP: True,
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
            Abilities.DRAW: 1
        }

    }


class BattleCruiser(Card):
    data = {
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "BattleCruiser",
        CardAttrs.COST: 6,
        Actions.PLAY: {
            Values.DAMAGE: 6,
            Abilities.DRAW: 1
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
        CardAttrs.SHIP: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Dreadnought",
        CardAttrs.COST: 7,
        Actions.PLAY: {
            Values.DAMAGE: 7,
            Abilities.DRAW: 1
        },
        Actions.SCRAP: {
            Values.DAMAGE: 5,
        }
    }


# Star Empire Bases
class RecyclingStation(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Recycling Station",
        CardAttrs.COST: 4,
        CardAttrs.DEFENSE: 4,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "Recycling Station"
        }
    }


class SpaceStation(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Space Station",
        CardAttrs.COST: 4,
        CardAttrs.DEFENSE: 4,
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 2
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        },
        Actions.SCRAP: {
            Values.TRADE: 4
        }
    }


class WarWorld(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "War World",
        CardAttrs.COST: 5,
        CardAttrs.DEFENSE: 4,
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            Values.DAMAGE: 4
        }
    }


class RoyalRedoubt(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.OUTPOST: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "Royal Redoubt",
        CardAttrs.COST: 6,
        CardAttrs.DEFENSE: 6,
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            CardAttrs.ABILITY: "Discard"
        }
    }


class FleetHQ(Card):
    data = {
        CardAttrs.BASE: True,
        CardAttrs.FACTION: Factions.STAR_EMPIRE,
        CardAttrs.NAME: "FleetHQ",
        CardAttrs.COST: 8,
        CardAttrs.DEFENSE: 8,
        Actions.ACTIVATE_BASE: {
            CardAttrs.ABILITY: "Fleet HQ"
        }
    }
