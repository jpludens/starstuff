from unittest import TestCase
# Explorers TODO (lol)
from cards import Scout, Viper, SpaceStation, BattleStation, BarterWorld, RoyalRedoubt, BlobWheel, BlobFighter, \
    Explorer, Cutter, Dreadnaught, TradePod, SurveyShip, PatrolMech, MissileBot, MachineBase, BattlePod, \
    ImperialFighter, RecyclingStation
from effects import PendChoice, PendScrap, PendDiscard, PendRecycle
from enums import Zones, ValueTypes, Triggers, Abilities
from gamestate import GameState
from move import PlayCard, ActivateBase, Attack, ActivateAlly, ActivateScrap, Choose, Scrap, EndTurn, Discard
import logging

logging.getLogger().setLevel(logging.ERROR)


class StarstuffTests(TestCase):
    def setUp(self):
        self.game = GameState("Foo", "Bar")

    def _add_cards_to_hand(self, *cards):
        for card in cards:
            card.location = Zones.HAND
            self.game[Zones.HAND].append(card)

    def _add_cards_to_discard(self, *cards):
        for card in cards:
            card.location = Zones.DISCARD
            self.game[Zones.DISCARD].append(card)

    def _add_bases_to_opponent(self, *bases):
        for base in bases:
            base.location = Zones.IN_PLAY
            self.game.opponent[Zones.IN_PLAY].append(base)

    def _clear_zones(self, *zones):
        for zone in zones:
            self.game.active_player[zone] = []

    def _set_damage(self, damage):
        self.game.active_player[ValueTypes.DAMAGE] = damage

    def assert_damage(self, n):
        self.assertEqual(self.game.active_player[ValueTypes.DAMAGE], n)

    def assert_authority(self, n):
        self.assertEqual(self.game.active_player[ValueTypes.AUTHORITY], n)

    def assert_trade(self, n):
        self.assertEqual(self.game.active_player[ValueTypes.TRADE], n)

    def assert_hand_count(self, n):
        self.assertEqual(len(self.game.active_player[Zones.HAND]), n)

    def assert_discard_count(self, n):
        self.assertEqual(len(self.game.active_player[Zones.DISCARD]), n)

    def assert_deck_count(self, n):
        self.assertEqual(len(self.game.active_player[Zones.DECK]), n)

    def assert_no_active_factions(self):
        self.assertEqual(sum(self.game.active_player.active_factions.values()), 0)

    def assert_in_play(self, card):
        self.assertEqual(card.location, Zones.IN_PLAY)
        self.assertIn(card, self.game[Zones.IN_PLAY])

    def assert_in_discard(self, card):
        self.assertEqual(card.location, Zones.DISCARD)
        self.assertIn(card, self.game[Zones.DISCARD])

    def assert_in_hand(self, card):
        self.assertEqual(card.location, Zones.HAND)
        self.assertIn(card, self.game[Zones.HAND])

    def assert_scrapped(self, card):
        self.assertEqual(card.location, Zones.SCRAP_HEAP)

        self.assertNotIn(card, self.game[Zones.TRADE_ROW])
        self.assertNotIn(card, self.game[Zones.TRADE_DECK])

        self.assertNotIn(card, self.game[Zones.IN_PLAY])
        self.assertNotIn(card, self.game[Zones.HAND])
        self.assertNotIn(card, self.game[Zones.DECK])
        self.assertNotIn(card, self.game[Zones.DISCARD])

        self.assertNotIn(card, self.game.opponent[Zones.IN_PLAY])
        self.assertNotIn(card, self.game.opponent[Zones.HAND])
        self.assertNotIn(card, self.game.opponent[Zones.DECK])
        self.assertNotIn(card, self.game.opponent[Zones.DISCARD])

    def assert_opponent_authority(self, n):
        self.assertEqual(self.game.opponent[ValueTypes.AUTHORITY], n)

    def assert_in_opponent_discard(self, card):
        self.assertEqual(card.location, Zones.DISCARD)
        self.assertIn(card, self.game.opponent[Zones.DISCARD])

    def assert_opponent_discards(self, n):
        self.assertEqual(self.game.forced_discards, n)

    def assert_pending(self, pending_type):
        if pending_type:
            self.assertIsInstance(self.game.pending_effect, pending_type)
        else:
            self.assertIsNone(self.game.pending_effect)


class TestShips(StarstuffTests):
    def test_play_scout(self):
        scout = Scout()
        self._add_cards_to_hand(scout)

        PlayCard(scout).execute(self.game)
        self.assertIn(scout, self.game[Zones.IN_PLAY])
        self.assertEqual(scout.location, Zones.IN_PLAY)
        self.assertEqual(self.game[ValueTypes.TRADE], 1)
        self.assertNotIn(Triggers.SHIP, scout.available_abilities)

    def test_play_twice(self):
        viper = Viper()
        self._add_cards_to_hand(viper)
        PlayCard(viper).execute(self.game)
        self.assertRaises(ValueError, PlayCard(viper).execute, self.game)


class TestBases(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.base = SpaceStation()
        self._add_cards_to_hand(self.base)

    def test_battle_station(self):
        battle_station = BattleStation()
        self._add_cards_to_hand(battle_station)

        PlayCard(battle_station).execute(self.game)

        self.assertNotIn(Triggers.BASE, battle_station.available_abilities)

    def test_play_base(self):
        PlayCard(self.base).execute(self.game)

        self.assert_damage(0)
        self.assertIn(Triggers.BASE, self.base.available_abilities)

    def test_activate_base(self):
        PlayCard(self.base).execute(self.game)
        ActivateBase(self.base).execute(self.game)

        self.assert_damage(2)
        self.assertNotIn(Triggers.BASE, self.base.available_abilities)

    def test_activate_base_twice(self):
        PlayCard(self.base).execute(self.game)
        ActivateBase(self.base).execute(self.game)

        self.assertRaises(KeyError, ActivateBase(self.base).execute, self.game)


class TestAttack(StarstuffTests):
    def test_normal_attack(self):
        self._set_damage(10)
        Attack(self.game.opponent).execute(self.game)

        self.assert_opponent_authority(40)
        self.assertIsNone(self.game.victor)

    def test_normal_attack_with_base(self):
        self._add_bases_to_opponent(BarterWorld())
        self._set_damage(10)
        Attack(self.game.opponent).execute(self.game)

        self.assert_opponent_authority(40)
        self.assertIsNone(self.game.victor)

    def test_winning_attack(self):
        self._set_damage(50)
        Attack(self.game.opponent).execute(self.game)

        self.assert_opponent_authority(0)
        self.assertEqual(self.game.victor, self.game.active_player.name)

    def test_base_attack(self):
        self._set_damage(10)
        target = BarterWorld()
        self._add_bases_to_opponent(target)
        Attack(target).execute(self.game)

        self.assert_opponent_authority(50)
        self.assert_in_opponent_discard(target)
        self.assert_damage(6)

    def test_outpost_mechanic(self):
        self._set_damage(10)
        outpost = RoyalRedoubt()
        self._add_bases_to_opponent(outpost)

        # Can't attack the opponent
        self.assertRaises(FileNotFoundError, Attack(self.game.opponent).execute, self.game)

        # Can't attack another base
        base = BarterWorld()
        self._add_bases_to_opponent(base)

        self.assertRaises(FileNotFoundError, Attack(base).execute, self.game)

        # But can attack the outpost
        Attack(outpost).execute(self.game)

        self.assert_opponent_authority(50)
        self.assert_in_opponent_discard(outpost)
        self.assert_damage(4)


class TestAllyAbilities(StarstuffTests):
    def test_activate_without_allies(self):
        # Can't activate on its own
        blob_fighter = BlobFighter()
        self._add_cards_to_hand(blob_fighter)
        PlayCard(blob_fighter).execute(self.game)

        self.assertRaises(FileNotFoundError, ActivateAlly(blob_fighter).execute, self.game)

        # Can't activate with a rainbow
        rainbow_cards = [Scout(), Viper(), Explorer(), Cutter(), Dreadnaught(), BattleStation()]
        self._add_cards_to_hand(*rainbow_cards)
        for card in rainbow_cards:
            PlayCard(card).execute(self.game)

        self.assertRaises(FileNotFoundError, ActivateAlly(blob_fighter).execute, self.game)

    def test_activate(self):
        blob_fighter = BlobFighter()
        trade_pod = TradePod()
        self._add_cards_to_hand(blob_fighter, trade_pod)
        PlayCard(blob_fighter).execute(self.game)
        PlayCard(trade_pod).execute(self.game)

        # preconditions
        self.assert_damage(3)
        self.assert_trade(3)
        self.assert_hand_count(3)

        # Activate fighter
        ActivateAlly(blob_fighter).execute(self.game)
        self.assert_damage(3)
        self.assert_trade(3)
        self.assert_hand_count(4)

        # Activate pod
        ActivateAlly(trade_pod).execute(self.game)
        self.assert_damage(5)
        self.assert_trade(3)
        self.assert_hand_count(4)

        self.assertRaises(KeyError, ActivateAlly(blob_fighter).execute, self.game)

    def test_activate_null_ability(self):
        scout = Scout()
        blob_wheel = BlobWheel()
        self._add_cards_to_hand(scout, blob_wheel)
        PlayCard(scout).execute(self.game)
        PlayCard(blob_wheel).execute(self.game)

        self.assertRaises(FileNotFoundError, ActivateAlly(scout).execute, self.game)
        self.assertRaises(FileNotFoundError, ActivateAlly(blob_wheel).execute, self.game)


class TestScrapAbilities(StarstuffTests):
    def test_scout(self):
        scout = Scout()
        self._add_cards_to_hand(scout)

        PlayCard(scout).execute(self.game)
        self.assertRaises(KeyError, ActivateScrap(scout).execute, self.game)

    def test_dreadnaught(self):
        dreadnaught = Dreadnaught()
        self._add_cards_to_hand(dreadnaught)
        PlayCard(dreadnaught).execute(self.game)

        # Preconditions
        self.assert_damage(7)
        self.assert_in_play(dreadnaught)

        # Test
        ActivateScrap(dreadnaught).execute(self.game)
        self.assert_damage(12)
        self.assert_scrapped(dreadnaught)
        self.assert_no_active_factions()

    def test_survey_ship(self):
        survey_ship = SurveyShip()
        self._add_cards_to_hand(survey_ship)
        PlayCard(survey_ship).execute(self.game)

        # Preconditions
        self.assert_trade(1)
        self.assert_in_play(survey_ship)

        # Test
        ActivateScrap(survey_ship).execute(self.game)
        self.assert_opponent_discards(1)
        self.assert_scrapped(survey_ship)
        self.assert_no_active_factions()


class TestDrawEffect(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.survey_ship = SurveyShip()
        self._add_cards_to_hand(self.survey_ship)

    def test_deck_full(self):
        self.assert_deck_count(7)
        self.assert_hand_count(4)

        PlayCard(self.survey_ship).execute(self.game)

        self.assert_deck_count(6)
        self.assert_hand_count(4)

    def test_deck_empty_discard_full(self):
        self._clear_zones(Zones.DECK)
        self._add_cards_to_discard(Scout(), Scout(), Scout())
        self.assert_hand_count(4)

        PlayCard(self.survey_ship).execute(self.game)

        self.assert_hand_count(4)
        self.assert_deck_count(2)
        self.assert_discard_count(0)

    def test_deck_empty_discard_empty(self):
        self._clear_zones(Zones.DECK)
        self.assert_hand_count(4)
        self.assert_deck_count(0)
        self.assert_discard_count(0)

        PlayCard(self.survey_ship).execute(self.game)

        self.assert_hand_count(3)


class TestChoiceEffect(StarstuffTests):
    def test_invalid_choice(self):
        mech = PatrolMech()
        self._add_cards_to_hand(mech)
        PlayCard(mech).execute(self.game)

        self.assertRaises(FileNotFoundError, Choose(ValueTypes.AUTHORITY).execute, self.game)

    def test_patrol_mech(self):
        mech1 = PatrolMech()
        mech2 = PatrolMech()
        self._add_cards_to_hand(mech1, mech2)
        self.assert_trade(0)
        self.assert_damage(0)

        PlayCard(mech1).execute(self.game)
        self.assert_pending(PendChoice)
        self.assert_trade(0)
        self.assert_damage(0)

        Choose(ValueTypes.TRADE).execute(self.game)
        self.assert_pending(None)
        self.assert_trade(3)
        self.assert_damage(0)

        PlayCard(mech2).execute(self.game)
        Choose(ValueTypes.DAMAGE).execute(self.game)
        self.assert_trade(3)
        self.assert_damage(5)

    def test_barter_world(self):
        base1 = BarterWorld()
        base2 = BarterWorld()
        self._add_cards_to_hand(base1, base2)
        self.assert_authority(50)
        self.assert_trade(0)

        PlayCard(base1).execute(self.game)
        self.assert_pending(None)
        ActivateBase(base1).execute(self.game)
        self.assert_pending(PendChoice)
        self.assert_authority(50)
        self.assert_trade(0)

        Choose(ValueTypes.AUTHORITY).execute(self.game)
        self.assert_authority(52)
        self.assert_trade(0)

        PlayCard(base2).execute(self.game)
        ActivateBase(base2).execute(self.game)
        Choose(ValueTypes.TRADE).execute(self.game)
        self.assert_authority(52)
        self.assert_trade(2)


class TestMachineCultScrapEffect(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.missile_bot = MissileBot()
        self._add_cards_to_hand(self.missile_bot)
        self._add_cards_to_discard(Viper())

    def test_scrap_from_hand(self):
        PlayCard(self.missile_bot).execute(self.game)
        self.assert_pending(PendScrap)
        self.assert_hand_count(3)

        target = self.game[Zones.HAND][0]
        Scrap(target).execute(self.game)
        self.assert_hand_count(2)
        self.assert_scrapped(target)
        self.assert_pending(None)

    def test_scrap_from_discard(self):
        PlayCard(self.missile_bot).execute(self.game)
        self.assert_pending(PendScrap)
        self.assert_discard_count(1)

        target = self.game[Zones.DISCARD][0]
        Scrap(target).execute(self.game)
        self.assert_discard_count(0)
        self.assert_scrapped(target)
        self.assert_pending(None)

    def test_scrap_nothing(self):
        PlayCard(self.missile_bot).execute(self.game)
        self.assert_pending(PendScrap)
        self.assert_hand_count(3)
        self.assert_discard_count(1)

        Scrap().execute(self.game)
        self.assert_hand_count(3)
        self.assert_discard_count(1)
        self.assert_pending(None)

    def test_scrap_invalid_target(self):
        PlayCard(self.missile_bot).execute(self.game)
        target = self.game[Zones.DECK][0]
        self.assertRaises(FileNotFoundError, Scrap(target).execute, self.game)

    def test_scrap_effect_with_no_valid_targets(self):
        self._clear_zones(Zones.DISCARD)
        self._clear_zones(Zones.HAND)
        self._add_cards_to_hand(self.missile_bot)
        PlayCard(self.missile_bot).execute(self.game)
        self.assert_pending(None)


class TestMachineBase(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.base = MachineBase()
        self._add_cards_to_hand(self.base)
        PlayCard(self.base).execute(self.game)

    def test_must_scrap(self):
        ActivateBase(self.base).execute(self.game)
        self.assertRaises(FileNotFoundError, Scrap().execute, self.game)

    def test_cannot_scrap_from_discard(self):
        self._add_cards_to_discard(Viper())
        ActivateBase(self.base).execute(self.game)
        self.assertRaises(FileNotFoundError, Scrap(self.game[Zones.DISCARD][0]).execute, self.game)

    # TODO: Make a special machine base effect that draws, then pends a scrap
    def test_activate_with_no_hand_no_deck_full_discard(self):
        pass

    def test_activate_with_full_hand_no_deck_no_discard(self):
        pass

    def test_activate_with_no_hand_no_deck_no_discard(self):
        pass


class TestBlobScrapEffect(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.battle_pod = BattlePod()
        self._add_cards_to_hand(self.battle_pod)

    def test_scrap_from_trade_row(self):
        PlayCard(self.battle_pod).execute(self.game)
        self.assert_pending(PendScrap)
        cards_in_trade_deck_at_start = len(self.game[Zones.TRADE_DECK])

        target = self.game[Zones.TRADE_ROW][0]
        Scrap(target).execute(self.game)
        self.assertEqual(len(self.game[Zones.TRADE_DECK]), cards_in_trade_deck_at_start - 1)
        self.assert_scrapped(target)
        self.assert_pending(None)

    def test_decline_scrap_from_trade_row(self):
        PlayCard(self.battle_pod).execute(self.game)
        self.assert_pending(PendScrap)
        cards_in_trade_deck_at_start = len(self.game[Zones.TRADE_DECK])

        Scrap().execute(self.game)
        self.assertEqual(len(self.game[Zones.TRADE_DECK]), cards_in_trade_deck_at_start)
        self.assert_pending(None)

    def test_with_empty_trade_deck(self):
        self.game[Zones.TRADE_DECK].clear()
        self.game[Zones.TRADE_ROW].pop()

        PlayCard(self.battle_pod).execute(self.game)
        self.assert_pending(PendScrap)

        Scrap(self.game[Zones.TRADE_ROW][0]).execute(self.game)
        self.assertEqual(len(self.game[Zones.TRADE_ROW]), 3)
        self.assert_pending(None)

    def test_with_empty_trade_row(self):
        self.game[Zones.TRADE_DECK].clear()
        self.game[Zones.TRADE_ROW].clear()

        PlayCard(self.battle_pod).execute(self.game)
        self.assert_pending(None)


class TestStarEmpireDiscardEffect(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.game[Zones.HAND].clear()
        for _ in range(7):
            self._add_cards_to_hand(ImperialFighter())

    def play_fighter(self):
        PlayCard(self.game[Zones.HAND][0]).execute(self.game)

    def test_discard_1(self):
        self.play_fighter()

        self.assertEqual(self.game.forced_discards, 1)

        EndTurn().execute(self.game)
        self.assertEqual(self.game.forced_discards, 0)
        self.assert_pending(PendDiscard)
        self.assert_hand_count(5)

        self.assertRaises(FileNotFoundError, Discard().execute, self.game)
        Discard(self.game[Zones.HAND][0]).execute(self.game)
        self.assert_pending(None)
        self.assert_hand_count(4)
        # TODO: move besides discard should fail

    def test_discard_7(self):
        for _ in range(7):
            self.play_fighter()

        self.assertEqual(self.game.forced_discards, 7)

        EndTurn().execute(self.game)
        self.assertEqual(self.game.forced_discards, 0)
        self.assert_pending(PendDiscard)
        self.assert_hand_count(5)

        self.assertRaises(FileNotFoundError, Discard(self.game[Zones.HAND][0]).execute, self.game)
        Discard(*self.game[Zones.HAND]).execute(self.game)
        self.assert_pending(None)
        self.assert_hand_count(0)
        # TODO: move besides discard should fail


class TestRecyclingStation(StarstuffTests):
    def setUp(self):
        super().setUp()
        self.station = RecyclingStation()
        self._add_cards_to_hand(self.station)
        PlayCard(self.station).execute(self.game)
        ActivateBase(self.station).execute(self.game)
        self.assert_pending(PendChoice)
        self.targets = self.game[Zones.HAND][:2]

    def test_activate_with_no_hand(self):
        pass
        # TODO: Shouldn't even pend the choice

    def test_choose_trade(self):
        Choose(ValueTypes.TRADE).execute(self.game)
        self.assert_pending(None)
        self.assert_trade(1)

    def test_decline_discard(self):
        Choose(Abilities.RECYCLE).execute(self.game)
        self.assert_pending(PendRecycle)

    def test_discard_1(self):
        Choose(Abilities.RECYCLE).execute(self.game)
        self.assert_hand_count(3)
        self.assert_deck_count(7)
        self.assert_discard_count(0)
        for scout in self.targets:
            self.assert_in_hand(scout)

        Discard(self.targets[0]).execute(self.game)
        self.assert_in_discard(self.targets[0])
        self.assert_in_hand(self.targets[1])
        self.assert_hand_count(3)
        self.assert_deck_count(6)
        self.assert_discard_count(1)

    def test_discard_1_no_deck_no_discard(self):
        Choose(Abilities.RECYCLE).execute(self.game)
        self._clear_zones(Zones.DECK, Zones.DISCARD)

        # Card will have been discarded and redrawn
        Discard(self.targets[0]).execute(self.game)
        self.assert_in_hand(self.targets[0])
        self.assert_in_hand(self.targets[1])
        self.assert_hand_count(3)
        self.assert_deck_count(0)
        self.assert_discard_count(0)

    def test_discard_2(self):
        Choose(Abilities.RECYCLE).execute(self.game)

        Discard(*self.targets).execute(self.game)
        self.assert_in_discard(self.targets[0])
        self.assert_in_discard(self.targets[1])
        self.assert_hand_count(3)
        self.assert_deck_count(5)
        self.assert_discard_count(2)

    def test_discard_2_with_no_deck_one_card_in_discard(self):
        Choose(Abilities.RECYCLE).execute(self.game)
        self._clear_zones(Zones.DECK, Zones.DISCARD)
        self._add_cards_to_discard(Viper())

        # One card will have been redrawn, the other will be in the deck
        Discard(*self.targets).execute(self.game)
        scout_locations = set([s.location for s in self.targets])
        self.assertIn(Zones.DECK, scout_locations)
        self.assertIn(Zones.HAND, scout_locations)
        self.assert_hand_count(3)
        self.assert_deck_count(1)
        self.assert_discard_count(0)