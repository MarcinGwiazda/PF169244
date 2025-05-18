"""Unit tests for the Player class and Position enum."""

import unittest
from src.player import Player, Position


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""

    def setUp(self):
        """Set up test fixtures."""
        self.player = Player("Cristiano Ronaldo", Position.FORWARD, 39, 92)

    def test_player_initialization(self):
        """Test initializing a player with valid attributes."""
        self.assertEqual(self.player.name, "Cristiano Ronaldo")
        self.assertEqual(self.player.position, Position.FORWARD)
        self.assertEqual(self.player.age, 39)
        self.assertEqual(self.player.overall_rating, 92)
        self.assertEqual(self.player.stamina, 100)
        self.assertFalse(self.player.injured)

    def test_train(self):
        """Test increasing rating and reducing stamina after training."""
        self.player.train()
        self.assertEqual(self.player.overall_rating, 93)
        self.assertEqual(self.player.stamina, 90)

    def test_rest(self):
        """Test increasing stamina after resting."""
        self.player.stamina = 50
        self.player.rest()
        self.assertEqual(self.player.stamina, 70)

    def test_injure(self):
        """Test setting injured status to True."""
        self.player.injure()
        self.assertTrue(self.player.injured)

    def test_invalid_rating_raises_error(self):
        """Test raising ValueError when rating is out of range."""
        with self.assertRaises(ValueError):
            Player("Robert Lewandowski", Position.FORWARD, 30, 120)

    def test_invalid_age_raises_error(self):
        """Test raising ValueError when age is out of range."""
        with self.assertRaises(ValueError):
            Player("Adam Young", Position.MIDFIELDER, 10, 80)

    def test_is_exhausted(self):
        """Test returning True when stamina is below 30."""
        self.player.stamina = 25
        self.assertTrue(self.player.is_exhausted())

    def test_is_exhausted_false(self):
        """Test returning False when stamina is 30 or more."""
        for stamina in [30, 50, 80, 100]:
            with self.subTest(stamina=stamina):
                self.player.stamina = stamina
                self.assertFalse(self.player.is_exhausted())

    def test_recover_from_injury(self):
        """Test recovering from injury when injured is True."""
        self.player.injured = True
        self.player.recover_from_injury()
        self.assertFalse(self.player.injured)

    def test_recover_from_if_not_injured_raises_error(self):
        """Test raising ValueError when recovering and not injured."""
        self.player.injured = False
        with self.assertRaises(ValueError):
            self.player.recover_from_injury()

    def test_age_up_rating_drops(self):
        """Test reducing rating if player turns older than 30."""
        veteran = Player("Luka Modric", Position.MIDFIELDER, 30, 85)
        veteran.age_up()
        self.assertEqual(veteran.age, 31)
        self.assertEqual(veteran.overall_rating, 84)

    def test_age_up_rating_unchanged(self):
        """Test keeping rating unchanged if player is 30 or younger."""
        young = Player("Jude Bellingham", Position.MIDFIELDER, 20, 88)
        young.age_up()
        self.assertEqual(young.age, 21)
        self.assertEqual(young.overall_rating, 88)

    def test_change_position(self):
        """Test changing player position to a valid Position enum."""
        self.player.change_position(Position.MIDFIELDER)
        self.assertEqual(self.player.position, Position.MIDFIELDER)

    def test_change_position_invalid_type_raises_error(self):
        """Test raising TypeError when passing invalid position type."""
        with self.assertRaises(TypeError):
            self.player.change_position("Goalkeeper")

    def test_promote_to_captain(self):
        """Test promoting a player to captain sets is_captain to True."""
        self.assertFalse(self.player.is_captain)
        self.player.promote_to_captain()
        self.assertTrue(self.player.is_captain)

    def test_demote_from_captain(self):
        """Test demoting a player sets is_captain to False."""
        self.player.promote_to_captain()
        self.assertTrue(self.player.is_captain)
        self.player.demote_from_captain()
        self.assertFalse(self.player.is_captain)

    def test_record_match(self):
        """Test updating goals, assists and matches played."""
        self.player.record_match(goals=2, assists=1)
        self.assertEqual(self.player.goals, 2)
        self.assertEqual(self.player.assists, 1)
        self.assertEqual(self.player.matches_played, 1)

        self.player.record_match(goals=1, assists=0)
        self.assertEqual(self.player.goals, 3)
        self.assertEqual(self.player.assists, 1)
        self.assertEqual(self.player.matches_played, 2)

    def test_record_match_with_default_values(self):
        """Test calling record_match() without arguments."""
        self.player.record_match()
        self.assertEqual(self.player.goals, 0)
        self.assertEqual(self.player.assists, 0)
        self.assertEqual(self.player.matches_played, 1)

    def test_record_match_negative_values_raises_error(self):
        """Test raising ValueError when using negative goals or assists."""
        with self.assertRaises(ValueError):
            self.player.record_match(goals=-1, assists=0)
        with self.assertRaises(ValueError):
            self.player.record_match(goals=0, assists=-1)

    def test_receive_yellow_card_once(self):
        """Test giving one yellow card increases yellow_cards by 1."""
        self.player.receive_card("yellow")
        self.assertEqual(self.player.yellow_cards, 1)
        self.assertFalse(self.player.suspended)

    def test_receive_two_yellow_cards_converts_to_red(self):
        """Test that two yellow cards convert to one red and suspend the player."""
        self.player.receive_card("yellow")
        self.player.receive_card("yellow")
        self.assertEqual(self.player.yellow_cards, 0)
        self.assertEqual(self.player.red_cards, 1)
        self.assertTrue(self.player.suspended)

    def test_receive_red_card_direct(self):
        """Test receiving a red card directly suspends the player."""
        self.player.receive_card("red")
        self.assertEqual(self.player.red_cards, 1)
        self.assertTrue(self.player.suspended)

    def test_receive_invalid_card_type_raises(self):
        """Test that giving an invalid card type raises ValueError."""
        with self.assertRaises(ValueError):
            self.player.receive_card("blue")

    def test_reset_cards_clears_all(self):
        """Test reset_cards clears all cards and suspension status."""
        self.player.yellow_cards = 1
        self.player.red_cards = 1
        self.player.suspended = True
        self.player.reset_cards()
        self.assertEqual(self.player.yellow_cards, 0)
        self.assertEqual(self.player.red_cards, 0)
        self.assertFalse(self.player.suspended)

    def test_renew_contract(self):
        """Test renewing contract with a valid number of years."""
        self.player.renew_contract(4)
        self.assertEqual(self.player.contract_years_left, 4)

    def test_renew_contract_invalid_years_raises_error(self):
        """Test raising ValueError when renewing with non-positive years."""
        with self.assertRaises(ValueError):
            self.player.renew_contract(0)
        with self.assertRaises(ValueError):
            self.player.renew_contract(-2)

    def test_is_contract_expiring(self):
        """Test checking contract expiration returns True when 1 or 0 years left."""
        self.player.contract_years_left = 1
        self.assertTrue(self.player.is_contract_expiring())
        self.player.contract_years_left = 0
        self.assertTrue(self.player.is_contract_expiring())

    def test_is_contract_expiring_false(self):
        """Test checking contract expiration returns False when more than 1 year left."""
        self.player.contract_years_left = 3
        self.assertFalse(self.player.is_contract_expiring())

    def test_decrement_contract_above_zero(self):
        """Test decreasing contract duration by one year."""
        self.player.contract_years_left = 2
        self.player.decrement_contract()
        self.assertEqual(self.player.contract_years_left, 1)

    def test_decrement_contract_zero_remains_zero(self):
        """Test contract duration does not go below zero."""
        self.player.contract_years_left = 0
        self.player.decrement_contract()
        self.assertEqual(self.player.contract_years_left, 0)

    def test_change_morale(self):
        """Test increasing morale."""
        self.player.morale = 70
        self.player.change_morale(10)
        self.assertEqual(self.player.morale, 80)

    def test_change_morale_negative(self):
        """Test decreasing morale."""
        self.player.morale = 70
        self.player.change_morale(-20)
        self.assertEqual(self.player.morale, 50)

    def test_change_morale_bounds(self):
        """Test morale does not exceed 0–100 bounds."""
        self.player.morale = 95
        self.player.change_morale(10)
        self.assertEqual(self.player.morale, 100)
        self.player.morale = 5
        self.player.change_morale(-10)
        self.assertEqual(self.player.morale, 0)

    def test_change_morale_invalid_type_raises_error(self):
        """Test raising ValueError for non-int morale change."""
        with self.assertRaises(ValueError):
            self.player.change_morale("high")

    def test_get_morale_status(self):
        """Test returning correct morale status string."""
        cases = [
            (85, "Excellent"),
            (65, "Good"),
            (45, "Average"),
            (25, "Low"),
            (10, "Very Low")
        ]
        for value, expected in cases:
            with self.subTest(morale=value):
                self.player.morale = value
                self.assertEqual(self.player.get_morale_status(), expected)

    def test_check_retire(self):
        """Test checking if the player is on retirement"""
        senior = Player("Gianluigi Buffon", Position.GOALKEEPER, 41, 80)
        senior.check_retirement()
        self.assertTrue(senior.retired)

        young = Player("Pedri", Position.MIDFIELDER, 23, 84)
        young.check_retirement()
        self.assertFalse(young.retired)

    def test_loan_to(self):
        """Test loaning a player to another club."""
        self.player.loan_to("Manchester United", 5)
        self.assertTrue(self.player.on_loan)
        self.assertEqual(self.player.loaned_to, "Manchester United")
        self.assertEqual(self.player.loan_duration, 5)

    def test_loan_to_twice_raises_error(self):
        """Test raising error when loaning already loaned player."""
        self.player.loan_to("Real Madrid", 5)
        with self.assertRaises(ValueError):
            self.player.loan_to("PSG", 3)

    def test_return_from_loan(self):
        """Test resetting loan info after returning."""
        self.player.loan_to("Juventus", 5)
        self.player.return_from_loan()
        self.assertFalse(self.player.on_loan)
        self.assertIsNone(self.player.loaned_to)
        self.assertEqual(self.player.loan_duration, 0)

    def test_reduce_loan_duration(self):
        """Test reducing loan duration and auto-return after zero."""
        self.player.loan_to("Al-Nassr", 1)
        self.player.reduce_loan_duration()
        self.assertFalse(self.player.on_loan)

    def test_invalid_loan_duration_raises_error(self):
        """Test loaning with zero or negative duration raises error."""
        with self.assertRaises(ValueError):
            self.player.loan_to("Inter Miami", 0)

    def test_return_from_loan_not_on_loan_raises_error(self):
        """Test raising ValueError when returning a player who is not on loan."""
        self.player.on_loan = False
        with self.assertRaises(ValueError):
            self.player.return_from_loan()

    def test_market_value(self):
        """Test market value calculation"""
        player = Player("Martin Odegaard", Position.MIDFIELDER, 25, 86)
        player.goals = 8
        value = player.get_market_value()
        self.assertEqual(value, 36.7)

        player = Player("Erling Haaland", Position.FORWARD, 24, 91)
        player.goals = 30
        value = player.get_market_value()
        self.assertEqual(value, 41.2)