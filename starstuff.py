from collections import Counter
from pprint import PrettyPrinter

from engine.state.views import GameStateView
from enums.enums import Factions
from engine.state.gamestate import GameState


def play_game():
    player_1 = "Alice"
    player_2 = "Bob"

    # Simulations are closed until a non-spaghetti strategy can be developed.

    # strategies = {
    #     player_1: FactionStrategy(Factions.STAR_EMPIRE),
    #     player_2: FactionStrategy(Factions.MACHINE_CULT)}

    strategies = {}

    gamestate = GameState(player_1, player_2)
    while True:
        view = GameStateView(gamestate)
        moves = strategies[gamestate.active_player.name].get_moves(view)
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
