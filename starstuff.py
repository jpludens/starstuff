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
