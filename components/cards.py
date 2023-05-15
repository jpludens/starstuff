from engine.effects import ValueEffect, DrawEffect, OpponentDiscardEffect, PendChoice, PendScrap, PendRecycle, \
    GainFactionEffect, PendBrainWorld, PendDestroyBase, GainTrade, GainAuthority, GainDamage, PendCopyShip, \
    BlobWorldDrawEffect, PendAcquireShipToTopForFree, ShopToTopEffect, MachineBaseEffect, EmbassyYachtDrawEffect
from enums.enums import Triggers, CardTypes, Factions, Zones


DRAW_ONE = DrawEffect(1)
SCRAP_FROM_TRADE_ROW = PendScrap(Zones.TRADE_ROW)
SCRAP_FROM_HAND_OR_DISCARD = PendScrap(Zones.HAND, Zones.DISCARD)
DISCARD = OpponentDiscardEffect()
DESTROY_BASE = PendDestroyBase()


class Card(object):
    name = None
    card_type = None
    faction = None
    cost = None
    defense = None
    abilities = None

    def __init__(self, owner_id=None, location=None):
        self.available_abilities = {}
        self.active_factions = set()

        self.owner_id = owner_id
        self.location = location

    def ready(self):
        if self.faction:
            self.active_factions.add(self.faction)
        self.available_abilities.update(self.abilities)

    def exhaust(self):
        self.active_factions.clear()
        self.available_abilities.clear()

    def move_to(self, new_zone, new_owner_id=None):
        if new_zone == Zones.IN_PLAY:
            self.ready()
        elif self.location == Zones.IN_PLAY:
            self.exhaust()

        if new_zone == Zones.SCRAP_HEAP:
            self.owner_id = Zones.SCRAP_HEAP

        self.location = new_zone
        if new_owner_id:
            self.owner_id = new_owner_id

    def has_ability(self, effect_class, triggers=None):
        return any([type(ability) == effect_class
                    for trigger, abilities in self.abilities.items()
                    for ability in abilities if triggers is None or trigger in triggers])

    def trigger_ability(self, trigger):
        effects_data = self.available_abilities.pop(trigger)
        effects = []
        for effect in effects_data:
            if isinstance(effect, tuple):
                effects.append(ValueEffect(effect[0], effect[1]))
            else:
                effects.append(effect)
        return effects

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
            GainTrade(1)
        }
    }


class Viper(Card):
    card_type = CardTypes.SHIP
    name = "Viper"
    cost = 0
    abilities = {
        Triggers.SHIP: {
            GainDamage(1)
        }
    }


class Explorer(Card):
    card_type = CardTypes.SHIP
    name = "Explorer"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            GainTrade(2)
        },
        Triggers.SCRAP: {
            GainDamage(2)
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
            GainDamage(3)
        },
        Triggers.ALLY: {
            DRAW_ONE
        }
    }


class TradePod(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Trade Pod"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            GainTrade(3)
        },
        Triggers.ALLY: {
            GainDamage(2)
        }
    }


class BattlePod(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Battle Pod"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            GainDamage(4),
            SCRAP_FROM_TRADE_ROW
        },
        Triggers.ALLY: {
            GainDamage(2)
        }
    }


class Ram(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Ram"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            GainDamage(5)
        },
        Triggers.ALLY: {
            GainDamage(2)
        },
        Triggers.SCRAP: {
            GainTrade(3)
        }
    }


class BlobDestroyer(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Destroyer"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            GainDamage(6)
        },
        Triggers.ALLY: {
            DESTROY_BASE,
            SCRAP_FROM_TRADE_ROW
        }
    }


class BlobCarrier(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Blob Carrier"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            GainDamage(7)
        },
        Triggers.ALLY: {
            PendAcquireShipToTopForFree()
        }
    }


class BattleBlob(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Battle Blob"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            GainDamage(8)
        },
        Triggers.ALLY: {
            DRAW_ONE
        },
        Triggers.SCRAP: {
            GainDamage(4)
        }
    }


class Mothership(Card):
    card_type = CardTypes.SHIP
    faction = Factions.BLOB
    name = "Mothership"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            GainDamage(6),
            DRAW_ONE
        },
        Triggers.ALLY: {
            DRAW_ONE
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
            GainDamage(1),
        },
        Triggers.SCRAP: {
            GainTrade(3)
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
            GainDamage(3),
        },
        Triggers.ALLY: {
            DRAW_ONE
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
            PendChoice([
                GainDamage(5),
                BlobWorldDrawEffect()
            ])
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
            GainTrade(2),
        },
        Triggers.ALLY: {
            GainAuthority(4),
        }
    }


class Cutter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Cutter"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            GainAuthority(4),
            GainTrade(2),
        },
        Triggers.ALLY: {
            GainDamage(4),
        }
    }


class EmbassyYacht(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Embassy Yacht"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            GainAuthority(3),
            GainTrade(2),
            EmbassyYachtDrawEffect()
        }
    }


class Freighter(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Freighter"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            GainTrade(4),
        },
        Triggers.ALLY: {
            ShopToTopEffect()
        }
    }


class TradeEscort(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Trade Escort"
    cost = 5
    abilities = {
        Triggers.SHIP: {
            GainAuthority(4),
            GainDamage(4),
        },
        Triggers.ALLY: {
            DRAW_ONE
        }
    }


class Flagship(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Flagship"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            GainDamage(5),
            DRAW_ONE
        },
        Triggers.ALLY: {
            GainAuthority(5),
        }
    }


class CommandShip(Card):
    card_type = CardTypes.SHIP
    faction = Factions.TRADE_FEDERATION
    name = "Command Ship"
    cost = 8
    abilities = {
        Triggers.SHIP: {
            GainAuthority(4),
            GainDamage(5),
            DrawEffect(2)
        },
        Triggers.ALLY: {
            DESTROY_BASE
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
            PendChoice({
                GainAuthority(1),
                GainTrade(1)
            })
        },
        Triggers.SCRAP: {
            GainDamage(3)
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
            PendChoice({
                GainAuthority(2),
                GainTrade(2)
            })
        },
        Triggers.SCRAP: {
            GainDamage(5)
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
            PendChoice({
                GainAuthority(3),
                GainDamage(2)
            })
        },
        Triggers.ALLY: {
            GainDamage(2)
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
            GainTrade(3)
        },
        Triggers.SCRAP: {
            DRAW_ONE,
            DESTROY_BASE
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
            GainTrade(2),
            ShopToTopEffect()
        },
        Triggers.ALLY: {
            DRAW_ONE
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
            GainTrade(1),
            SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            GainDamage(2),
        }
    }


class MissileBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Missile Bot"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            GainDamage(2),
            SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            GainDamage(2),
        }
    }


class SupplyBot(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Supply Bot"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            GainTrade(2),
            SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            GainDamage(2),
        }
    }


class PatrolMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Patrol Mech"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            PendChoice([
                GainTrade(3),
                GainDamage(5)])},
        Triggers.ALLY: {
            SCRAP_FROM_HAND_OR_DISCARD
        }
    }


class StealthNeedle(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Stealth Needle"
    cost = 4
    abilities = {
        Triggers.SHIP: {
            PendCopyShip()
        }
    }


class BattleMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Battle Mech"
    cost = 5
    abilities = {
        Triggers.SHIP: {
            GainDamage(4),
            SCRAP_FROM_HAND_OR_DISCARD
        },
        Triggers.ALLY: {
            DRAW_ONE
        }
    }


class MissileMech(Card):
    card_type = CardTypes.SHIP
    faction = Factions.MACHINE_CULT
    name = "Missile Mech"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            GainDamage(6),
            DESTROY_BASE
        },
        Triggers.ALLY: {
            DRAW_ONE
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
            GainDamage(5),
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
            GainFactionEffect(Factions.BLOB, Factions.STAR_EMPIRE, Factions.TRADE_FEDERATION)
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
            SCRAP_FROM_HAND_OR_DISCARD
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
            MachineBaseEffect()
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
            PendBrainWorld()
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
            GainDamage(2),
            DISCARD
        },
        Triggers.ALLY: {
            GainDamage(2),
        }
    }


class Corvette(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Corvette"
    cost = 2
    abilities = {
        Triggers.SHIP: {
            GainDamage(1),
            DRAW_ONE
        },
        Triggers.ALLY: {
            GainDamage(2),
        }
    }


class SurveyShip(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Survey Ship"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            GainTrade(1),
            DRAW_ONE
        },
        Triggers.SCRAP: {
            DISCARD
        }
    }


class ImperialFrigate(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Imperial Frigate"
    cost = 3
    abilities = {
        Triggers.SHIP: {
            GainDamage(4),
            DISCARD
        },
        Triggers.ALLY: {
            GainDamage(2),
        },
        Triggers.SCRAP: {
            DRAW_ONE
        }

    }


class Battlecruiser(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Battlecruiser"
    cost = 6
    abilities = {
        Triggers.SHIP: {
            GainDamage(6),
            DRAW_ONE
        },
        Triggers.ALLY: {
            DISCARD
        },
        Triggers.SCRAP: {
            DRAW_ONE,
            DESTROY_BASE
        }
    }


class Dreadnaught(Card):
    card_type = CardTypes.SHIP
    faction = Factions.STAR_EMPIRE
    name = "Dreadnaught"
    cost = 7
    abilities = {
        Triggers.SHIP: {
            GainDamage(7),
            DRAW_ONE
        },
        Triggers.SCRAP: {
            GainDamage(5)
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
            PendChoice({
                GainTrade(1),
                PendRecycle()
            })
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
            GainDamage(2)
        },
        Triggers.ALLY: {
            GainDamage(2)
        },
        Triggers.SCRAP: {
            GainTrade(4)
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
            GainDamage(3)
        },
        Triggers.ALLY: {
            GainDamage(4)
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
            GainDamage(3)
        },
        Triggers.ALLY: {
            DISCARD
        }
    }


class FleetHQ(Card):
    card_type = CardTypes.BASE
    faction = Factions.STAR_EMPIRE
    name = "FleetHQ"
    cost = 8
    defense = 8
    abilities = {
            # TODO...? This is currently hardcoded into PlayCard,
            # which honestly feels Just Fine unless there are other passive effects
    }
