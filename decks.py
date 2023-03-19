from cards import *

standard_deck = {
    BlobFighter: 3,
    TradePod: 3,
    BattlePod: 2,
    Ram: 2,
    BlobDestroyer: 2,
    BlobCarrier: 1,
    BattleBlob: 1,
    Mothership: 1,
    FederationShuttle: 3,
    Cutter: 3,
    EmbassyYacht: 2,
    Freighter: 2,
    TradeEscort: 1,
    Flagship: 1,
    CommandShip: 1,
    TradeBot: 3,
    MissileBot: 3,
    SupplyBot: 3,
    PatrolMech: 2,
    StealthNeedle: 1,
    BattleMech: 1,
    MissileMech: 1,
    ImperialFighter: 3,
    Corvette: 2,
    SurveyShip: 3,
    ImperialFrigate: 3,
    BattleCruiser: 1,
    Dreadnought: 1
}


def get_fresh_trade_deck():
    return [c for _c in [[card] * number for card, number in standard_deck.items()] for c in _c]
