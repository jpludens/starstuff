# Scrap is done, but all the various kajiggering everywhere to see if cards are in places makes it clear:
# Goal: Cards need to be aware of their location and move themselves around the board
# being aware of location means being of which player they belong to
# it's probably time to abandon active/inactive in favor of a player id

# Goal: Get Recycling Station implement since it's the most involved
# (requires a choice, then targets, then has knock-on effects)
# First, get Machine Cult scrap and Star Empire discard working

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
#         MUST scrap
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

from enums import Factions
from gamestate import GameState
from strategies import FactionStrategy


def play_game():
    # carter_strategy = ExplorerStrategy(max_exp=25,
    #                                    min_exp=6,
    #                                    ratio=2)

    player_1 = "Alice"
    player_2 = "Bob"

    strategies = {
        player_1: FactionStrategy(Factions.BLOB),
        player_2: FactionStrategy(Factions.MACHINE_CULT)}

    gamestate = GameState(player_1, player_2)
    while True:
        moves = strategies[gamestate.active_player.name].get_moves(gamestate)
        for move in moves:
            move.execute(gamestate)

            # Check for Victory
            if gamestate.victor:
                return gamestate.victor, gamestate.turn_number


def battle(n=1):
    results = [play_game() for _ in range(n)]
    print("Player 1 Wins: {}\nPlayer 2 Wins: {}".format(len([r for r in results if r[0] == "Alice"]),
                                                        len([r for r in results if r[0] == "Bob"])))
    print("Player 1 Victory Turn Numbers:")
    PrettyPrinter().pprint(sorted(Counter([result[1] for result in results if result[0] == "Alice"]).items()))
    print("Player 2 Victory Turn Numbers:")
    PrettyPrinter().pprint(sorted(Counter([result[1] for result in results if result[0] == "Bob"]).items()))
