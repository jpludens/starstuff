# Goal: Step through a "game" where only Explorers are purchased.
# Build a malleable "strategy" around how many Explorers to buy and when to scrap them for damage.
# Try to determine the best Explorer-only strategy.

from collections import Counter
from pprint import PrettyPrinter
from gamestate import GameState
from cards import Viper, Explorer


def play_game():
    gamestate = GameState()

    while gamestate.p1_state.authority > 0 and gamestate.p2_state.authority > 0:
        # Deal Viper Damage
        viper_damage = gamestate.active_player.hand.count(Viper)
        gamestate.inactive_player.authority -= viper_damage

        # Buy Explorers
        explorers_to_buy = gamestate.active_player.strategy.get_explorers_to_buy(gamestate.active_player)
        if explorers_to_buy:
            gamestate.active_player.discard.extend([Explorer] * explorers_to_buy)
            gamestate.active_player.explorer_count += explorers_to_buy
            # print("Buying Explorers! {} snags {}.".format(gamestate.active_player.name, explorers_to_buy))

        # Scrap Explorers and Deal Explorer Damage
        explorers_to_scrap = gamestate.active_player.strategy.get_explorers_to_scrap(gamestate.active_player)

        explorer_damage = 0
        while explorers_to_scrap:
            try:
                gamestate.active_player.hand.remove(Explorer)
            except ValueError:
                break
            else:
                explorer_damage += 2
                gamestate.active_player.explorer_count -= 1

        if explorer_damage:
            gamestate.inactive_player.authority -= explorer_damage
            # print("Scrapping Explorers, {} does {} Damage; {} now has {} Authority".format(
            #     gamestate.active_player.name,
            #     explorer_damage,
            #     gamestate.inactive_player.name,
            #     gamestate.inactive_player.authority))

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
