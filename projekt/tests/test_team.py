"""Unit tests for the Team class."""

import unittest
from src.player import Player, Position
from src.team import Team


class TestTeam(unittest.TestCase):
    """Test cases for the Team class."""

    def setUp(self):
        """Set up test fixtures."""
        self.team = Team("Manchester City")
        names = [
            "Kevin De Bruyne", "Ilkay Gundogan", "Phil Foden", "Jack Grealish", "Rodri",
            "Bernardo Silva", "Kalvin Phillips", "Riyad Mahrez", "Cole Palmer", "James McAtee",
            "Oscar Bobb", "Joao Cancelo", "Nathan Aké", "Aymeric Laporte", "Kyle Walker"
        ]
        self.players = [Player(name, Position.MIDFIELDER, 25, 70 + i) for i, name in enumerate(names)]
        for player in self.players:
            self.team.add_player(player)

    def test_add_player(self):
        """Test adding a player to the team."""
        self.assertEqual(len(self.team.players), 15)

    def test_add_duplicate_player_raises_error(self):
        """Test raising ValueError when adding a duplicate player."""
        with self.assertRaises(ValueError):
            self.team.add_player(self.players[0])

    def test_add_retired_player_raises_error(self):
        """Test raising ValueError when trying to add a retired player."""
        retired = Player("Zlatan Ibrahimović", Position.FORWARD, 41, 85)
        retired.retired = True
        with self.assertRaises(ValueError):
            self.team.add_player(retired)

    def test_remove_player(self):
        """Test removing a player from the team."""
        self.team.remove_player(self.players[0])
        self.assertEqual(len(self.team.players), 14)

    def test_remove_nonexistent_player_raises_error(self):
        """Test raising ValueError when removing a player not in the team."""
        new_player = Player("Paul Pogba", Position.MIDFIELDER, 30, 75)
        with self.assertRaises(ValueError):
            self.team.remove_player(new_player)

    def test_set_formation(self):
        """Test setting a valid formation for the team."""
        valid_formations = ["4-4-2", "4-3-3", "3-5-2"]

        for formation in valid_formations:
            with self.subTest(formation=formation):
                self.team.set_formation(formation)
                self.assertEqual(self.team.formation, formation)

    def test_set_invalid_formation_raises_error(self):
        """Test raising ValueError when setting an invalid formation."""
        with self.assertRaises(ValueError):
            self.team.set_formation("2-2-6")

    def test_assign_starting_eleven(self):
        """Test assigning 11 players to the starting eleven."""
        eleven = self.players[:11]
        self.team.assign_starting_eleven(eleven)
        self.assertEqual(len(self.team.starting_eleven), 11)

    def test_assign_invalid_starting_eleven_raises_error(self):
        """Test raising ValueError when assigning fewer than 11 players."""
        with self.assertRaises(ValueError):
            self.team.assign_starting_eleven(self.players[:10])

    def test_assign_starting_eleven_with_player_not_in_team_raises_error(self):
        """Test raising ValueError when assigning a player not in the team."""
        outsider = Player("Kylian Mbappe", Position.FORWARD, 24, 92)
        players = self.players[:10] + [outsider]
        with self.assertRaises(ValueError):
            self.team.assign_starting_eleven(players)

    def test_average_rating(self):
        """Test calculating average rating of the team."""
        avg = self.team.get_average_rating()
        self.assertTrue(70 <= avg <= 85)

    def test_get_injured_players_returns_only_injured(self):
        """Test returning only injured players from the team."""
        self.players[0].injured = True
        self.players[2].injured = True
        result = self.team.get_injured_players()
        self.assertIn(self.players[0], result)
        self.assertIn(self.players[2], result)
        self.assertEqual(len(result), 2)

    def test_get_players_by_position(self):
        """Test returning players matching a given position."""
        defenders = [
            Player("Raphael Varane", Position.DEFENDER, 29, 80),
            Player("Sergio Ramos", Position.DEFENDER, 37, 82),
            Player("Jules Kounde", Position.DEFENDER, 25, 81)
        ]
        for p in defenders:
            self.team.add_player(p)

        result = self.team.get_players_by_position(Position.DEFENDER)
        self.assertEqual(len(result), 3)
        for p in defenders:
            self.assertIn(p, result)

    def test_get_best_player(self):
        """Test returning the player with the highest rating."""
        best = Player("Erling Haaland", Position.FORWARD, 23, 99)
        self.team.add_player(best)
        self.assertEqual(self.team.get_best_player(), best)

    def test_get_best_player_empty_team(self):
        """Test returning None when the team has no players."""
        empty_team = Team("Empty FC")
        self.assertIsNone(empty_team.get_best_player())

    def test_swap_players(self):
        """Test swapping a player in the team with a new one."""
        out_player = self.players[0]
        in_player = Player("Jadon Sancho", Position.MIDFIELDER, 24, 78)
        self.team.swap_players(out_player, in_player)
        self.assertIn(in_player, self.team.players)
        self.assertNotIn(out_player, self.team.players)

    def test_swap_players_not_in_team_raises_error(self):
        """Test raising ValueError when player to remove is not in team."""
        outsider = Player("Casemiro", Position.DEFENDER, 31, 83)
        replacement = Player("Luke Shaw", Position.FORWARD, 28, 77)
        with self.assertRaises(ValueError):
            self.team.swap_players(outsider, replacement)

    def test_get_average_age(self):
        """Test calculating average age of players in the team."""
        average_age = self.team.get_average_age()
        self.assertEqual(average_age, 25)

    def test_get_average_age_empty_team(self):
        """Test returning 0 when the team has no players."""
        empty_team = Team("Empty FC")
        self.assertEqual(empty_team.get_average_age(), 0)

    def test_get_top_scorer(self):
        """Test returning player with the most goals."""
        cases = [
            ([5, 3, 1], 0),
            ([0, 0, 10], 2),
            ([1, 1, 1], 0),
            ([0, 4, 2], 1),
        ]

        for goals, expected_index in cases:
            with self.subTest(goals=goals):
                for i, g in enumerate(goals):
                    self.players[i].goals = g
                top = self.team.get_top_scorer()
                self.assertEqual(top, self.players[expected_index])

    def test_get_top_scorer_empty_team(self):
        """Test returning None when team has no players."""
        empty_team = Team("Empty FC")
        self.assertIsNone(empty_team.get_top_scorer())

    def test_get_top_assistant(self):
        """Test returning player with the most assists."""
        self.players[0].assists = 2
        self.players[4].assists = 6
        self.players[5].assists = 4
        top = self.team.get_top_assistant()
        self.assertEqual(top, self.players[4])

    def test_get_top_assistant_empty_team(self):
        """Test returning None when team has no players."""
        empty_team = Team("Empty FC")
        self.assertIsNone(empty_team.get_top_assistant())

    def test_get_most_active_player(self):
        """Test returning player with most matches played."""
        self.players[2].matches_played = 10
        self.players[6].matches_played = 20
        self.players[1].matches_played = 5
        top = self.team.get_most_active_player()
        self.assertEqual(top, self.players[6])

    def test_get_most_active_player_empty_team(self):
        """Test returning None when team has no players."""
        new_team = Team("New Team FC")
        self.assertIsNone(new_team.get_most_active_player())

    def test_get_loaned_players(self):
        """Test returning only players who are on loan."""
        self.players[0].loan_to("Sevilla", 3)
        self.players[1].loan_to("Valencia", 2)

        loaned = self.team.get_loaned_players()

        self.assertIn(self.players[0], loaned)
        self.assertIn(self.players[1], loaned)
        self.assertEqual(len(loaned), 2)