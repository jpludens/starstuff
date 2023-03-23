# Goal: Implement choices (tuples?)
# Goal: Implement faction abilities
#       need to track availabilityby individual card
# Goal: Implement remaining abilities

# Goal: Create a data visualisation scheme for displaying an entire game's log of moves
#       (eg, cards bought each round, additional cards drawn, damage done, etc)
# Goal: Create a data analysis scheme for analyzing decks (and trade row favorablity)
#       (eg, x combat guaranteed y combat possible per cycle; velocity (turns/cycle))
# Goal: Create a data visualation scheme for deck progress throughout a game
#       (eg, graph combat and trade potential over time)

from collections import Counter
from pprint import PrettyPrinter

from enums import Factions, Values
from gamestate import GameState
from strategies import ExplorerStrategy, SplurgeStrategy, FactionStrategy


def play_game():
    alice_strategy = FactionStrategy(Factions.BLOB)

    bob_strategy = FactionStrategy(Factions.TRADE_FEDERATION)

    carter_strategy = ExplorerStrategy(max_exp=25,
                                       min_exp=6,
                                       ratio=2)

    gamestate = GameState(alice_strategy, bob_strategy)
    while True:
        moves = gamestate.active_player.get_moves(gamestate)
        for move in moves:
            gamestate.do_move(move)

            # Check for Victory
            if gamestate.inactive_player.state.values[Values.AUTHORITY] <= 0:
                result = (1, gamestate.turn_number) if gamestate.active_player.name == "Alice" \
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
