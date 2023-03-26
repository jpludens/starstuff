import logging

from effects import ValueEffect, DrawEffect, ChoiceEffect, ScrapEffect
from enums import Abilities, Triggers, CardTypes, Factions, ValueTypes, Zones


DRAW_ONE = DrawEffect(1)
SCRAP_FROM_TRADE_ROW = ScrapEffect(Zones.TRADE_ROW)
SCRAP_FROM_HAND_OR_DISCARD = ScrapEffect(Zones.HAND, Zones.DISCARD)


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

    def initialize_in_play(self):
        if self.faction:
            self.active_factions.add(self.faction)
        self.available_abilities.update(self.abilities)

    def trigger_ability(self, trigger):
        effects_data = self.available_abilities.pop(trigger)
        effects = []
        for k, v in effects_data.items():
            if isinstance(k, ValueTypes):
                effects.append(ValueEffect(k, v))
            elif k == Abilities.DRAW:
                effects.append(v)
            elif k == Abilities.SCRAP:
                effects.append(v)
            elif k == Abilities.CHOICE:
                choices = {ck: ValueEffect(ck, cv) for ck, cv in v.items()}
                effects.append(ChoiceEffect(choices))
            else:
                logging.warning("Ignoring ability - {}: {}".format(k, v))
        return effects

    def deinitialize_from_play(self):
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
        Triggers.SHIP: {
            ValueTypes.TRADE: 1
        }
    }


class Viper(Card):
    card_type = CardTypes.SHIP
    name = "Viper"
    cost = 0
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 1
        }
    }


class Explorer(Card):
    card_type = CardTypes.SHIP
    name = "Explorer"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            ValueTypes.TRADE: 2
        },
        Triggers.SCRAP: {
            ValueTypes.DAMAGE: 2
        }
    }


# Blob Ships
class BlobFighter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Fighter"
    cost = 1
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 3
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
        }
    }


class TradePod(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Trade Pod"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            ValueTypes.TRADE: 3
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2
        }
    }


class BattlePod(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Battle Pod"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 4,
            Abilities.SCRAP: SCRAP_FROM_TRADE_ROW
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2
        }
    }


class Ram(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Ram"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 5
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2
        },
        Triggers.SCRAP: {
            ValueTypes.TRADE: 3
        }
    }


class BlobDestroyer(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Destroyer"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 6
        },
        Triggers.ALLY: {
            Abilities.UNIMPLEMENTED: "Blow Base",
            Abilities.SCRAP: SCRAP_FROM_TRADE_ROW
        }
    }


class BlobCarrier(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Carrier"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 7
        },
        Triggers.ALLY: {
            Abilities.UNIMPLEMENTED: "Blob Carrier"
        }
    }


class BattleBlob(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Battle Blob"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 8
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.SCRAP: {
            ValueTypes.DAMAGE: 4
        }
    }


class Mothership(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Mothership"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 6,
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
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
        Triggers.BASE: {
            ValueTypes.DAMAGE: 1,
        },
        Triggers.SCRAP: {
            ValueTypes.TRADE: 3
        }
    }


class TheHive(Card):
    card_type = CardTypes.BASE
    faction = Factions.BLOB
    name = "The Hive"
    cost = 5
    defense = 5
    abilities = {
        Triggers.BASE: {
            ValueTypes.DAMAGE: 3,
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
        }
    }


class BlobWorld(Card):
    card_type = CardTypes.BASE
    faction = Factions.BLOB
    name = "Blob World"
    cost = 8
    defense = 8
    abilities = {
        Triggers.BASE: {
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
        Triggers.SHIP: {
            ValueTypes.TRADE: 2,
        },
        Triggers.ALLY: {
            ValueTypes.AUTHORITY: 4,
        }
    }


class Cutter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Cutter"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            ValueTypes.AUTHORITY: 4,
            ValueTypes.TRADE: 2,
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 4,
        }
    }


class EmbassyYacht(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Embassy Yacht"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            ValueTypes.AUTHORITY: 3,
            ValueTypes.TRADE: 2,
            Abilities.UNIMPLEMENTED: "Embassy Draw"
        }
    }


class Freighter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Freighter"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            ValueTypes.TRADE: 4,
        },
        Triggers.ALLY: {
            Abilities.UNIMPLEMENTED: "Shop To Top"
        }
    }


class TradeEscort(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Trade Escort"
    cost = 5
    abilities = {
        Triggers.SHIP: {
            ValueTypes.AUTHORITY: 4,
            ValueTypes.DAMAGE: 4,
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
        }
    }


class Flagship(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Flagship"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 5,
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.ALLY: {
            ValueTypes.AUTHORITY: 5,
        }
    }


class CommandShip(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Command Ship"
    cost = 8
    abilities = {
        Triggers.SHIP: {
            ValueTypes.AUTHORITY: 4,
            ValueTypes.DAMAGE: 5,
            Abilities.DRAW: DrawEffect(2)
        },
        Triggers.ALLY: {
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
        Triggers.BASE: {
            Abilities.CHOICE: {
                ValueTypes.AUTHORITY: 1,
                ValueTypes.TRADE: 1
            }
        },
        Triggers.SCRAP: {
            ValueTypes.DAMAGE: 3
        }
    }


class BarterWorld(Card):
    card_type = CardTypes.BASE
    faction = Factions.TRADE_FEDERATION
    name = "Barter World"
    cost = 4
    defense = 4
    abilities = {
        Triggers.BASE: {
            Abilities.CHOICE: {
                ValueTypes.AUTHORITY: 2,
                ValueTypes.TRADE: 2
            }
        },
        Triggers.SCRAP: {
            ValueTypes.DAMAGE: 5
        }
    }


class DefenseCenter(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.TRADE_FEDERATION
    name = "Defense Center"
    cost = 5
    defense = 5
    abilities = {
        Triggers.BASE: {
            Abilities.CHOICE: {
                ValueTypes.AUTHORITY: 3,
                ValueTypes.DAMAGE: 2
            }
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2
        }
    }


class PortOfCall(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.TRADE_FEDERATION
    name = "Port Of Call"
    cost = 6
    defense = 6
    abilities = {
        Triggers.BASE: {
            ValueTypes.TRADE: 3
        },
        Triggers.SCRAP: {
            Abilities.DRAW: DRAW_ONE,
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
        Triggers.BASE: {
            ValueTypes.TRADE: 2,
            Abilities.UNIMPLEMENTED: "Freighter"
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
        }
    }


# Machine Cult Ships
class TradeBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Trade Bot"
    cost = 1
    abilities = {
        Triggers.SHIP: {
            ValueTypes.TRADE: 1,
            Abilities.SCRAP: SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2,
        }
    }


class MissileBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Missile Bot"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 2,
            Abilities.SCRAP: SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2,
        }
    }


class SupplyBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Supply Bot"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            ValueTypes.TRADE: 2,
            Abilities.SCRAP: SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2,
        }
    }


class PatrolMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Patrol Mech"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            Abilities.CHOICE: {
                ValueTypes.TRADE: 3,
                ValueTypes.DAMAGE: 5
            }
        },
        Triggers.ALLY: {
            Abilities.SCRAP: SCRAP_FROM_HAND_OR_DISCARD
        }
    }


class StealthNeedle(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Stealth Needle"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            Abilities.UNIMPLEMENTED: "Stealth Needle"
        }
    }


class BattleMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Battle Mech"
    cost = 5
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 4,
            Abilities.SCRAP: SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
        }
    }


class MissileMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Missile Mech"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 6,
            Abilities.UNIMPLEMENTED: "Blow Base"
        },
        Triggers.ALLY: {
            Abilities.DRAW: DRAW_ONE
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
        Triggers.SCRAP: {
            ValueTypes.DAMAGE: 5,
        }
    }


class MechWorld(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Mech World"
    cost = 5
    defense = 6
    abilities = {
        Triggers.BASE: {
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
        Triggers.BASE: {
            Abilities.SCRAP: SCRAP_FROM_HAND_OR_DISCARD
        }
    }


class MachineBase(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Machine Base"
    cost = 7
    defense = 6
    abilities = {
        Triggers.BASE: {
            Abilities.DRAW: DRAW_ONE,
            Abilities.SCRAP: ScrapEffect(Zones.HAND, mandatory=True)
        }
    }


class BrainWorld(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.MACHINE_CULT
    name = "Brain World"
    cost = 8
    defense = 6
    abilities = {
        Triggers.BASE: {
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
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 2,
            Abilities.UNIMPLEMENTED: "Discard"
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2,
        }
    }


class Corvette(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Corvette"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 1,
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2,
        }
    }


class SurveyShip(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Survey Ship"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            ValueTypes.TRADE: 3,
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.SCRAP: {
            Abilities.UNIMPLEMENTED: "Discard"
        }
    }


class ImperialFrigate(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Imperial Frigate"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 4,
            Abilities.UNIMPLEMENTED: "Discard"
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2,
        },
        Triggers.SCRAP: {
            Abilities.DRAW: DRAW_ONE
        }

    }


class BattleCruiser(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "BattleCruiser"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 6,
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.ALLY: {
            Abilities.UNIMPLEMENTED: "Discard"
        },
        Triggers.SCRAP: {
            Abilities.UNIMPLEMENTED: "Draw AND Blow Base",
        }
    }


class Dreadnought(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Dreadnought"
    cost = 7
    abilities = {
        Triggers.SHIP: {
            ValueTypes.DAMAGE: 7,
            Abilities.DRAW: DRAW_ONE
        },
        Triggers.SCRAP: {
            ValueTypes.DAMAGE: 5,
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
        Triggers.BASE: {
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
        Triggers.BASE: {
            ValueTypes.DAMAGE: 2
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 2
        },
        Triggers.SCRAP: {
            ValueTypes.TRADE: 4
        }
    }


class WarWorld(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.STAR_EMPIRE
    name = "War World"
    cost = 5
    defense = 4
    abilities = {
        Triggers.BASE: {
            ValueTypes.DAMAGE: 3
        },
        Triggers.ALLY: {
            ValueTypes.DAMAGE: 4
        }
    }


class RoyalRedoubt(Card):
    card_type = CardTypes.OUTPOST
    faction = Factions.STAR_EMPIRE
    name = "Royal Redoubt"
    cost = 6
    defense = 6
    abilities = {
        Triggers.BASE: {
            ValueTypes.DAMAGE: 3
        },
        Triggers.ALLY: {
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
        Triggers.BASE: {
            Abilities.UNIMPLEMENTED: "Fleet HQ"
        }
    }
