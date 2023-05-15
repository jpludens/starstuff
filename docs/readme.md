# Overview
    Starstuff is a framework for implementing Star Realms gameplay strategies and testing strategies against each other.

# Starstuff
    This is the bare-bones simulator. It pairs "players" (just names, really) with "strategies" (Strategy objects, see
    below) and simulates a Star Realms game.
    To simulate, run starstuff in console and call battle(n), where n is the number of games to simulate.
    
# Strategy
    A Strategy class implements get_moves(gamestate). Starstuff calls get_moves; the Strategy examines the gamestate and
    returns a list of Moves; Starstuff executes the Moves. Starstuff asks for more moves until the game has a winner.
    
    !Important! - Strategies need to pay attention to GameState.pending_effects to see if they need to specify a target
    or make some other kind of choice. See Engine -> Effects and Moves -> PendingEffects and PendingMoves below.

# Engine
## GameState and PlayerState
    GameState manages the Trade Deck and Row, and turn number, pending effects (see below), and various data needed
    for some card abilities (e.g. number of Blob cards played for Blob World). Players' decks, hands, discards, trade,
    authority, and damage are tracked within GameState as a pair of PlayerState objects.

    These classes implement only basic operational methods - e.g. GameState.fill_trade_row(), PlayerState.shuffle().
    State changes are primarily driven by Effects and Moves.
       
## Effects and Moves
    An Effect is an encapsulation of a change to GameState. Effect.apply() accepts and modifies a gamestate argument.
    For example, GainFactionEffect accepts one or more factions, and updates the most previously played card to now have
    those factions. (This is used for Mech World and Stealth Needle.)
    Effects can "delegate": EmbassyYachtDrawEffect checks to see if there are two bases out, and if there are, creates a
    DrawEffect(2) and calls its apply() instead of duplicating the draw logic.
    
    Effects are not validated; Moves are. However, Moves validate themselves, which is fine amongst friends, but it does
    allow a malicious actor to overwrite the validate method with a rubber stamp.

### PendingEffects and PendingMoves
    Not all Moves and Effects are straightforward. Some abilities require additional input, like Machine Cult scrappers,
    or require an explicit choice like Barter World or Patrol Mech. Enter the PendingEffect.
    
    A PendingEffect leaves itself in GameState.pending_effects and waits there for its resolve() method to be called.
    A PendingMove is like a normal move except it has a resolved_effect_type attribute. On execute(), the PendingMove
    finds the PendingEffect and passes the additional input to the effect's resolve(). The resolve method then performs
    whatever changes occur, then removes itself from the GameState's list of pending effects.
    
    An example: Clara's Strategy returns PlayCard(some_missile_bot). She gets her 2 damage and the GameState now has a
    PendScrap effect waiting. If she tries to play another card or activate some ability, that move will fail because it
    will see there is a pending effect. So the next time her Strategy's get_moves is called, it sees the pending scrap
    effect, looks for a Viper, and returns Scrap(some_viper).
    
# Components
    These are generally straightforward but I want to address how Cards work.
    They are aware of their owning player and their location. They track which of their abilities have been activated.
    They are moved around by consumer calls to their "move_to" method, which handles movements to the table, scrap heap,
    etc.
    Abilities are triggered by calling the card's trigger_ability method with a Triggers Enum value. The card returns
    whatever batch of effects are mapped to that trigger.
    Card abilities are implemented as fully instantiated Effects, though some of those Effects are singletons. Every
    single "draw 1 card" ability in this implementation is just the same DrawEffect being re.applied(). This seems like
    it could lead to problems later. Seems like it SHOULD lead to problems now since all cards also share a singleton
    PendingDestroyBaseEffects which requires different input ever time... but the way PendingEffects and PendingMoves
    are implemented, it all works just fine.

         