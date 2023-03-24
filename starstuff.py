# Goal: YAR Yet Another Refactor in advance of remaining abilities
#    Keep Gamestate and Playerstate very dumb and mechanical, move all simplification logic to the strategy layer
#    Every single piece of information required from players constitutes an entire Move
#    So, Gamestate will activate played ships, but if they require a choice (Patrol Mech),
#       state execution halts and a new move is requested. Same with, say, activating Barter World


# Goal: Implement remaining abilities
#    Mech World
#    Destroy Base
#    Blob Carrier
#    Freighter / Central Office
#         change "buy" to "acquire"
#         count available topdecks
#         "buy" is now a special acquire that spends trade
#         "topdeck" is like buy ... but topdecks. both reduce tracked topdeck counts
#    Embassy Yacht
#           Conditionality
#    Scrap Trade
#         Scrap move with targets
#    Scrap / Junkyard
#      Machine Base
#      Brain World
#    Blob World
#          gamestate needs to keep an examinable log of turn actions to be searched for Actions.PLAY/Factions.BLOB
#    Discard
#    Stealth Needle
#          Target move
#    Fleet HQ
#           introduce a check that examines all moves for Actions.Play with a card with CardType.SHIP
#    Recycling Station
#       Discard move with targets

# Goal: Use a Strategy class to trigger deterministic abilities
# Goal: use a Strategy class to mimic app

# Goal: Create a data visualisation scheme for displaying an entire game's log of moves
#       (eg, cards bought each round, additional cards drawn, damage done, etc)
# Goal: Create a data analysis scheme for analyzing decks (and trade row favorablity)
#       (eg, x combat guaranteed y combat possible per cycle; velocity (turns/cycle))
# Goal: Create a data visualation scheme for deck progress throughout a game
#       (eg, graph combat and trade potential over time)

from collections import Counter
from pprint import PrettyPrinter

from enums import Factions, ValueTypes, PlayerIndicators
from gamestate import GameState
from strategies import ExplorerStrategy, FactionStrategy


def play_game():
    # carter_strategy = ExplorerStrategy(max_exp=25,
    #                                    min_exp=6,
    #                                    ratio=2)

    player_1 = "Alice"
    player_2 = "Bob"

    strategies = {
        player_1: FactionStrategy(Factions.BLOB),
        player_2: FactionStrategy(Factions.TRADE_FEDERATION)}

    gamestate = GameState(player_1, player_2)
    while True:
        active_player_name = gamestate[PlayerIndicators.ACTIVE].name
        moves = strategies[active_player_name].get_moves(gamestate)
        for move in moves:
            move.execute(gamestate)

            # Check for Victory
            if gamestate[PlayerIndicators.INACTIVE][ValueTypes.AUTHORITY] <= 0:
                result = (1, gamestate.turn_number) if gamestate[PlayerIndicators.ACTIVE].name == "Alice" \
                    else (2, gamestate.turn_number)
                return result


def battle(n=1):
    results = [play_game() for _ in range(n)]
    print("Player 1 Wins: {}\nPlayer 2 Wins: {}".format(len([r for r in results if r[0] == 1]),
                                                        len([r for r in results if r[0] == 2])))
    print("Player 1 Victory Turn Numbers:")
    PrettyPrinter().pprint(sorted(Counter([result[1] for result in results if result[0] == 1]).items()))
    print("Player 2 Victory Turn Numbers:")
    PrettyPrinter().pprint(sorted(Counter([result[1] for result in results if result[0] == 2]).items()))
