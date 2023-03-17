# Goal: Step through a "game" where no purchases are made.
# Confirm that the game always ends in a small window of turn numbers, and that p1 has an advantage.

from random import shuffle
from pprint import PrettyPrinter as pp
from collections import Counter

scout = "Scout"
viper = "Viper"

alice = "Alice"
bob = "Bob"


# Util
def move_list_contents(from_list, to_list):
    to_list.extend(from_list)
    from_list[:] = []


# States
class PlayerState(object):
    def __init__(self, first_player=False, name=None):
        self.name = name
        self.authority = 50

        self.deck = [scout] * 8 + [viper] * 2
        shuffle(self.deck)

        self.hand = []
        self.draw(3 if first_player else 5)

        self.discard = []

    def shuffle_deck(self):
        assert len(self.deck) == 0
        move_list_contents(self.discard, self.deck)
        shuffle(self.deck)

    def draw(self, n=5):
        for i in range(n):
            try:
                card = self.deck.pop(0)
            except IndexError:
                self.shuffle_deck()
                try:
                    card = self.deck.pop(0)
                except IndexError:
                    return
            self.hand.append(card)


class GameState(object):
    def __init__(self):
        self.p1_state = PlayerState(first_player=True, name="Alice")
        self.p2_state = PlayerState(first_player=False, name="Bob")

        self.active_player = self.p1_state
        self.inactive_player = self.p2_state

        self.turn_number = 1

    def next_turn(self):
        move_list_contents(self.active_player.hand, self.active_player.discard)
        self.active_player.draw()
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.turn_number += 1


# Engine
def play_game():
    gamestate = GameState()

    while gamestate.p1_state.authority > 0 and gamestate.p2_state.authority > 0:
        # "Deal Damage"
        damage = gamestate.active_player.hand.count("Viper")
        gamestate.inactive_player.authority -= damage

        # Check for Victory
        if gamestate.inactive_player.authority <= 0:
            result = (1, gamestate.turn_number) if gamestate.active_player is gamestate.p1_state \
                else (2, gamestate.turn_number)
            # del gamestate
            return result

        # End turn
        gamestate.next_turn()


def battle(n=1):
    results = [play_game() for _ in range(n)]
    print("Player 1 Wins: {}\nPlayer 2 Wins: {}".format(len([r for r in results if r[0] == 1]),
                                                        len([r for r in results if r[0] == 2])))
    print("Player 1 Victory Turn Numbers:")
    pp().pprint(Counter([result[1] for result in results if result[0] == 1]))
    print("Player 2 Victory Turn Numbers:")
    pp().pprint(Counter([result[1] for result in results if result[0] == 2]))
