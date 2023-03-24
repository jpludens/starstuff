from enums import Abilities, Actions, CardTypes, Factions, Values


class Card(object):
    name = None
    card_type = None
    faction = None
    cost = None
    defense = None
    abilities = None

    def __init__(self):
        self.available_abilities = {}
        self.active_factions = set()

    def put_in_play(self):
        if self.faction:
            self.active_factions.add(self.faction)
        self.available_abilities.update(self.abilities)

    def use_ability(self, ability_type):
        del self.available_abilities[ability_type]

    def remove_from_play(self):
        self.active_factions.clear()
        self.available_abilities.clear()

    def is_base(self):
        return self.card_type != CardTypes.SHIP

    def is_ship(self):
        return self.card_type == CardTypes.SHIP


# Boring Ships
class Scout(Card):
    card_type = CardTypes.SHIP
    name = "Scout"
    cost = 0
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 1
        }
    }


class Viper(Card):
    card_type = CardTypes.SHIP
    name = "Viper"
    cost = 0
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 1
        }
    }


class Explorer(Card):
    card_type = CardTypes.SHIP
    name = "Explorer"
    cost = 2
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 2
        },
        Actions.SCRAP: {
            Values.DAMAGE: 2
        }
    }


# Blob Ships
class BlobFighter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Fighter"
    cost = 1
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class TradePod(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Trade Pod"
    cost = 2
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 3
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        }
    }


class BattlePod(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Battle Pod"
    cost = 2
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 4
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        }
    }


class Ram(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Ram"
    cost = 3
    abilities = {
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
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Destroyer"
    cost = 4
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 6
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: "Blob Destroyer"
        }
    }


class BlobCarrier(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Carrier"
    cost = 6
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 7
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: "Blob Carrier"
        }
    }


class BattleBlob(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Battle Blob"
    cost = 6
    abilities = {
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
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Mothership"
    cost = 6
    abilities = {
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
    card_type = CardTypes.BASE
    faction = Factions.BLOB
    name = "Blob Wheel"
    cost = 3
    defense = 5
    abilities = {
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 1,
        },
        Actions.SCRAP: {
            Values.TRADE: 3
        }
    }


class TheHive(Card):
    card_type = CardTypes.BASE
    faction = Factions.BLOB
    name = "The Hive"
    cost = 5
    defense = 5
    abilities = {
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 3,
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class BlobWorld(Card):
    card_type = CardTypes.BASE
    faction = Factions.BLOB
    name = "Blob World"
    cost = 8
    defense = 8
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "Blob World Choice"
        }
    }


# Federation Ships
class FederationShuttle(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Federation Shuttle"
    cost = 1
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 2,
        },
        Actions.ALLY: {
            Values.AUTHORITY: 4,
        }
    }


class Cutter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Cutter"
    cost = 2
    abilities = {
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.TRADE: 2,
        },
        Actions.ALLY: {
            Values.DAMAGE: 4,
        }
    }


class EmbassyYacht(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Embassy Yacht"
    cost = 3
    abilities = {
        Actions.PLAY: {
            Values.AUTHORITY: 3,
            Values.TRADE: 2,
            Abilities.UNIMPLEMENTED: "Embassy Draw"
        }
    }


class Freighter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Freighter"
    cost = 4
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 4,
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: "Shop To Top"
        }
    }


class TradeEscort(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Trade Escort"
    cost = 5
    abilities = {
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.DAMAGE: 4,
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class Flagship(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Flagship"
    cost = 6
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 5,
            Abilities.DRAW: 1
        },
        Actions.ALLY: {
            Values.AUTHORITY: 5,
        }
    }


class CommandShip(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Command Ship"
    cost = 8
    abilities = {
        Actions.PLAY: {
            Values.AUTHORITY: 4,
            Values.DAMAGE: 5,
            Abilities.DRAW: 2
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: "Blow Base"
        }
    }


# Trade Federation Bases
class TradingPost(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.TRADE_FEDERATION
    name = "Trading Post"
    cost = 3
    defense = 4
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "1 Authority or Trade"
        },
        Actions.SCRAP: {
            Values.DAMAGE: 3
        }
    }


class BarterWorld(Card):
    card_type = CardTypes.BASE
    faction = Factions.TRADE_FEDERATION
    name = "Barter World"
    cost = 4
    defense = 4
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "2 Authority or Trade"
        },
        Actions.SCRAP: {
            Values.DAMAGE: 5
        }
    }


class DefenseCenter(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.TRADE_FEDERATION
    name = "Defense Center"
    cost = 5
    defense = 5
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "3 Authority or 2 Damage"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2
        }
    }


class PortOfCall(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.TRADE_FEDERATION
    name = "Port Of Call"
    cost = 6
    defense = 6
    abilities = {
        Actions.ACTIVATE_BASE: {
            Values.TRADE: 3
        },
        Actions.SCRAP: {
            Abilities.DRAW: 1,
            Abilities.UNIMPLEMENTED: "Blow Base"
        }
    }


class CentralOffice(Card):
    card_type = CardTypes.BASE
    faction = Factions.TRADE_FEDERATION
    name = "Central Office"
    cost = 7
    defense = 6
    abilities = {
        Actions.ACTIVATE_BASE: {
            Values.TRADE: 2,
            Abilities.UNIMPLEMENTED: "Freighter"
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


# Machine Cult Ships
class TradeBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Trade Bot"
    cost = 1
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 1,
            Abilities.UNIMPLEMENTED: Actions.SCRAP
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class MissileBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Missile Bot"
    cost = 2
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 2,
            Abilities.UNIMPLEMENTED: Actions.SCRAP
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class SupplyBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Supply Bot"
    cost = 3
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 2,
            Abilities.UNIMPLEMENTED: Actions.SCRAP
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class PatrolMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Patrol Mech"
    cost = 4
    abilities = {
        Actions.PLAY: {
            Abilities.UNIMPLEMENTED: "Patrol Mech Choice"
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: Actions.SCRAP
        }
    }


class StealthNeedle(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Stealth Needle"
    cost = 4
    abilities = {
        Actions.PLAY: {
            Abilities.UNIMPLEMENTED: "Stealth Needle"
        }
    }


class BattleMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Battle Mech"
    cost = 5
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 4,
            Abilities.UNIMPLEMENTED: Actions.SCRAP
        },
        Actions.ALLY: {
            Abilities.DRAW: 1
        }
    }


class MissileMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Missile Mech"
    cost = 6
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 6,
            Abilities.UNIMPLEMENTED: "Blow Base"
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
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Battle Station"
    cost = 3
    defense = 5
    abilities = {
        Actions.SCRAP: {
            Values.DAMAGE: 5,
        }
    }


class MechWorld(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Mech World"
    cost = 5
    defense = 6
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "Mech World"
        }
    }


class Junkyard(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Junkyard"
    cost = 6
    defense = 5
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: Actions.SCRAP
        }
    }


class MachineBase(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "MachineBase"
    cost = 7
    defense = 6
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "Machine Base"
        }
    }


class BrainWorld(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Brain World"
    cost = 8
    defense = 6
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "Brain World"
        }
    }


# Star Empire Ships
class ImperialFighter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Imperial Fighter"
    cost = 1
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 2,
            Abilities.UNIMPLEMENTED: "Discard"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class Corvette(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Corvette"
    cost = 2
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 1,
            Abilities.DRAW: 1
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        }
    }


class SurveyShip(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Survey Ship"
    cost = 3
    abilities = {
        Actions.PLAY: {
            Values.TRADE: 3,
            Abilities.DRAW: 1
        },
        Actions.SCRAP: {
            Abilities.UNIMPLEMENTED: "Discard"
        }
    }


class ImperialFrigate(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Imperial Frigate"
    cost = 3
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 4,
            Abilities.UNIMPLEMENTED: "Discard"
        },
        Actions.ALLY: {
            Values.DAMAGE: 2,
        },
        Actions.SCRAP: {
            Abilities.DRAW: 1
        }

    }


class BattleCruiser(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "BattleCruiser"
    cost = 6
    abilities = {
        Actions.PLAY: {
            Values.DAMAGE: 6,
            Abilities.DRAW: 1
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: "Discard"
        },
        Actions.SCRAP: {
            Abilities.UNIMPLEMENTED: "Draw AND Blow Base",
        }
    }


class Dreadnought(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Dreadnought"
    cost = 7
    abilities = {
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
    card_type = CardTypes.OUTPOST
    faction = Factions.STAR_EMPIRE
    name = "Recycling Station"
    cost = 4
    defense = 4
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "Recycling Station"
        }
    }


class SpaceStation(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.STAR_EMPIRE
    name = "Space Station"
    cost = 4
    defense = 4
    abilities = {
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
    card_type = CardTypes.OUTPOST
    faction = Factions.STAR_EMPIRE
    name = "War World"
    cost = 5
    defense = 4
    abilities = {
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            Values.DAMAGE: 4
        }
    }


class RoyalRedoubt(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.STAR_EMPIRE
    name = "Royal Redoubt"
    cost = 6
    defense = 6
    abilities = {
        Actions.ACTIVATE_BASE: {
            Values.DAMAGE: 3
        },
        Actions.ALLY: {
            Abilities.UNIMPLEMENTED: "Discard"
        }
    }


class FleetHQ(Card):
    card_type = CardTypes.BASE
    faction = Factions.STAR_EMPIRE
    name = "FleetHQ"
    cost = 8
    defense = 8
    abilities = {
        Actions.ACTIVATE_BASE: {
            Abilities.UNIMPLEMENTED: "Fleet HQ"
        }
    }
