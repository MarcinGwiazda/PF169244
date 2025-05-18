"""Unit tests for the Manager class."""

import unittest
import os
from src.player import Player, Position
from src.team import Team
from src.manager import Manager


class TestManager(unittest.TestCase):
    """Test cases for the Manager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.team = Team("FC Barcelona")
        self.manager = Manager(self.team)
        for i in range(11):
            p = Player(f"Player {i}", Position.DEFENDER, 28, 70 + i)
            self.team.add_player(p)

    def test_save_and_load_team(self):
        """Test saving team data to a file and loading it back."""
        filename = "test_team_data.json"
        self.manager.save_team_to_file(filename)
        loaded_team = self.manager.load_team_from_file(filename)
        self.assertEqual(loaded_team.name, "FC Barcelona")
        self.assertEqual(len(loaded_team.players), 11)
        os.remove(filename)

    def test_simulate_match_win_with_stats_update(self):
        """Test simulating a match where manager's team wins and stats are updated."""
        self.team.assign_starting_eleven(self.team.players[:11])

        opponent = Team("Getafe CF")
        for i in range(11):
            p = Player(f"Getafe Player {i}", Position.DEFENDER, 25, 50)
            p.stamina = 50
            opponent.add_player(p)
        opponent.assign_starting_eleven(opponent.players)

        result = self.manager.simulate_match(opponent)

        self.assertIn("wins", result)
        self.assertEqual(self.team.wins, 1)
        self.assertEqual(opponent.losses, 1)

    def test_simulate_match_loss_with_stats_update(self):
        """Test simulating a match where manager's team loses and stats are updated."""
        weak_team = Team("Elche CF")
        weak_players = [Player(f"Elche {i}", Position.MIDFIELDER, 24, 50) for i in range(11)]
        for p in weak_players:
            p.stamina = 40
            weak_team.add_player(p)
        weak_team.assign_starting_eleven(weak_players)

        strong_team = Team("Real Madrid")
        strong_players = [Player(f"RM {i}", Position.FORWARD, 27, 90) for i in range(11)]
        for p in strong_players:
            p.stamina = 90
            strong_team.add_player(p)
        strong_team.assign_starting_eleven(strong_players)

        manager = Manager(weak_team)
        result = manager.simulate_match(strong_team)

        self.assertIn("wins", result)
        self.assertEqual(weak_team.losses, 1)
        self.assertEqual(strong_team.wins, 1)

    def test_simulate_match_draw_with_stats_update(self):
        """Test simulating a draw and updating stats accordingly."""
        self.team.assign_starting_eleven(self.team.players[:11])

        mirror_team = Team("Atletico Madrid")
        mirror_players = [Player(f"ATM {i}", Position.FORWARD, 25, 70 + i) for i in range(11)]
        for p in mirror_players:
            p.stamina = 100
            mirror_team.add_player(p)
        mirror_team.assign_starting_eleven(mirror_players)

        result = self.manager.simulate_match(mirror_team)

        self.assertIn("Draw", result)
        self.assertEqual(self.team.draws, 1)
        self.assertEqual(mirror_team.draws, 1)

    def test_simulate_match_incomplete_team_raises_error(self):
        """Test raising ValueError when starting eleven is incomplete."""
        incomplete_team = Team("Valencia CF")
        for i in range(9):
            incomplete_team.add_player(Player(f"Valencia {i}", Position.MIDFIELDER, 24, 80))

        incomplete_team.starting_eleven = incomplete_team.players

        manager = Manager(incomplete_team)

        with self.assertRaises(ValueError):
            manager.simulate_match(self.team)

    def test_train_team(self):
        """Test training only players who are not injured."""
        self.team.players[0].injure()
        ratings_before = [p.overall_rating for p in self.team.players]

        self.manager.train_team()

        for i, player in enumerate(self.team.players):
            if player.injured:
                self.assertEqual(player.overall_rating, ratings_before[i])
            else:
                self.assertEqual(player.overall_rating, ratings_before[i] + 1)

    def test_rest_team(self):
        """Test resting increases stamina for all players."""
        for p in self.team.players:
            p.stamina = 40
        self.manager.rest_team()
        for p in self.team.players:
            self.assertEqual(p.stamina, 60)

    def test_bench_injured_players(self):
        """Test moving injured players from starting eleven to bench."""
        eleven = self.team.players[:11]
        eleven[2].injure()
        eleven[7].injure()
        self.team.assign_starting_eleven(eleven)

        self.manager.bench_injured_players()

        self.assertEqual(len(self.team.starting_eleven), 9)
        self.assertIn(eleven[2], self.team.bench)
        self.assertIn(eleven[7], self.team.bench)
        self.assertNotIn(eleven[2], self.team.starting_eleven)
        self.assertNotIn(eleven[7], self.team.starting_eleven)

    def test_bench_injured_players_no_starting_eleven(self):
        """Test doing nothing when no starting eleven is assigned."""
        self.manager.bench_injured_players()
        self.assertEqual(len(self.team.starting_eleven), 0)
        self.assertEqual(len(self.team.bench), 0)

    def test_buy_player(self):
        """Test buying a player with sufficient budget and available space."""
        new_player = Player("Erling Haaland", Position.FORWARD, 23, 91)
        self.manager.team.max_players = 20
        self.manager.team.players = self.manager.team.players[:10]
        self.manager.budget = 50

        self.manager.buy_player(new_player, price=30)

        self.assertIn(new_player, self.manager.team.players)
        self.assertEqual(self.manager.budget, 20)

    def test_buy_player_already_in_team_raises_error(self):
        """Test buying a player already in team raises ValueError."""
        existing_player = self.team.players[0]
        with self.assertRaises(ValueError):
            self.manager.buy_player(existing_player, price=10)

    def test_buy_player_to_full_team_raises_error(self):
        """Test buying a player fails when team is at max capacity."""
        self.manager.team.max_players = 11
        new_player = Player("Jude Bellingham", Position.MIDFIELDER, 20, 85)
        with self.assertRaises(ValueError):
            self.manager.buy_player(new_player, price=5)

    def test_buy_player_insufficient_budget_raises_error(self):
        """Test buying a player fails with not enough budget."""
        new_player = Player("Kylian Mbappe", Position.FORWARD, 25, 93)
        self.manager.team.max_players = 20

        cases = [
            (5, 10),
            (0, 1),
            (49, 50),
        ]

        for budget, price in cases:
            with self.subTest(budget=budget, price=price):
                self.manager.budget = budget
                with self.assertRaises(ValueError):
                    self.manager.buy_player(new_player, price=price)

    def test_sell_player(self):
        """Test selling a player removes them and increases budget."""
        player_to_sell = self.team.players[0]
        original_budget = self.manager.budget

        self.manager.sell_player(player_to_sell, price=15)

        self.assertNotIn(player_to_sell, self.team.players)
        self.assertEqual(self.manager.budget, original_budget + 15)

    def test_sell_player_not_in_team_raises_error(self):
        """Test selling a player not in team raises ValueError."""
        outsider = Player("Karim Benzema", Position.FORWARD, 35, 88)
        with self.assertRaises(ValueError):
            self.manager.sell_player(outsider, price=10)