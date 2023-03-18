# Goal: Add all ships (use stubs for all abilities besides auth, trade, combat)
# Goal: Use a "faction" strategy to favor buying one color, see which is best for simple ships

# Goal: Implement card draw abilities
# Goal: Implement faction abilities
#       need to track availabilityby individual card
# Goal: Implement remaining abilities

from collections import Counter
from pprint import PrettyPrinter

from enums import Values
from gamestate import GameState
from strategies import ExplorerStrategy, SplurgeStrategy


def play_game():
    alice_strategy = SplurgeStrategy()

    bob_strategy = ExplorerStrategy(max_exp=25,
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
    PrettyPrinter().pprint(Counter([result[1] for result in results if result[0] == 1]))
    print("Player 2 Victory Turn Numbers:")
    PrettyPrinter().pprint(Counter([result[1] for result in results if result[0] == 2]))
