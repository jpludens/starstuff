# Goal: Implement remaining abilities
#    Destroy Base (except Blob Destroyer)
#    Stealth Needle
#          Target move
#    Blob Carrier

#    Blob Destroyer
#         requires multiple pending effects
#         I refuse to treat them as ordered at any point in the code whatsoever
#         card.abilities will map triggers to /lists/
#         values will be a tuple so that initializing cards doesn't require creating a bunch of ValueEffects
#         probably just create ChoiceEffect at the card declaration instead of in trigger_abilities
#         blob destroyers will be a list of effects instead of a single effect
#    Fleet HQ
#           introduce a check that examines all moves for Actions.Play with a card with CardType.SHIP
#           effect needs to end when base leaves play
#           add a "source" field to effects
#    Freighter / Central Office
#         count available topdecks
#         "topdeck" is like buy ... but topdecks. both reduce tracked topdeck counts
#    Embassy Yacht
#           Conditionality
#    Blob World
#          gamestate needs to keep an examinable log of turn actions to be searched for Actions.PLAY/Factions.BLOB

# Goal: Use a Strategy class to trigger deterministic abilities
# Goal: use a Strategy class to mimic app

# Goal: Create a data visualisation scheme for displaying an entire game's log of moves
#       (eg, cards bought each round, additional cards drawn, damage done, etc)
# Goal: Create a data analysis scheme for analyzing decks (and trade row favorablity)
#       (eg, x combat guaranteed y combat possible per cycle; velocity (turns/cycle))
# Goal: Create a data visualation scheme for deck progress throughout a game
#       (eg, graph combat and trade potential over time)

# Goal: Create a web interface for designing strategies

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
        player_1: FactionStrategy(Factions.STAR_EMPIRE),
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
