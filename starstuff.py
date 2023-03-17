# Goal: Step through a "game" where only Explorers are purchased.
# Build a malleable "strategy" around how many Explorers to buy and when to scrap them for damage.
# Try to determine the best Explorer-only strategy.

from collections import Counter
from pprint import PrettyPrinter
from gamestate import GameState
from cards import Viper, Explorer
from strategies import ExplorerStrategy


def play_game():
    alice_strategy = ExplorerStrategy(max_exp=25,
                                      min_exp=6,
                                      ratio=2)

    bob_strategy = ExplorerStrategy(max_exp=25,
                                    min_exp=6,
                                    ratio=2)

    gamestate = GameState(alice_strategy, bob_strategy)
    gamestate.p1_state.metrics[Explorer] = 0
    gamestate.p2_state.metrics[Explorer] = 0
    while gamestate.p1_state.authority > 0 and gamestate.p2_state.authority > 0:
        # Deal Viper Damage
        viper_damage = gamestate.active_player.hand.count(Viper)
        gamestate.inactive_player.authority -= viper_damage

        # Buy Explorers
        gamestate.active_player.strategy.buy_explorers(gamestate.active_player)

        # Scrap Explorers and Deal Explorer Damage
        gamestate.active_player.strategy.scrap_explorers(gamestate.active_player)

        # Check for Victory
        if gamestate.inactive_player.authority <= 0:
            result = (1, gamestate.turn_number) if gamestate.active_player is gamestate.p1_state \
                else (2, gamestate.turn_number)
            return result

        # End turn
        gamestate.next_turn()


def battle(n=1):
    results = [play_game() for _ in range(n)]
    print("Player 1 Wins: {}\nPlayer 2 Wins: {}".format(len([r for r in results if r[0] == 1]),
                                                        len([r for r in results if r[0] == 2])))
    print("Player 1 Victory Turn Numbers:")
    PrettyPrinter().pprint(Counter([result[1] for result in results if result[0] == 1]))
    print("Player 2 Victory Turn Numbers:")
    PrettyPrinter().pprint(Counter([result[1] for result in results if result[0] == 2]))
