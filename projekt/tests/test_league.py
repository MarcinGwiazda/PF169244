"""Unit tests for the League class."""

import unittest
from src.team import Team
from src.league import League


class TestLeague(unittest.TestCase):
    """Test cases for the League class."""

    def setUp(self):
        """Set up test fixtures."""
        self.league = League("Premier League")
        self.team1 = Team("Arsenal")
        self.team2 = Team("Manchester City")
        self.team3 = Team("Liverpool")

        self.team1.points = 15
        self.team1.goals_scored = 20
        self.team1.goals_conceded = 10

        self.team2.points = 18
        self.team2.goals_scored = 25
        self.team2.goals_conceded = 12

        self.team3.points = 18
        self.team3.goals_scored = 20
        self.team3.goals_conceded = 8

    def test_add_team(self):
        """Test adding a team to the league."""
        self.league.add_team(self.team1)
        self.assertIn(self.team1, self.league.teams)

    def test_add_team_duplicate_raises_error(self):
        """Test raising ValueError when adding a duplicate team."""
        self.league.add_team(self.team1)
        with self.assertRaises(ValueError):
            self.league.add_team(self.team1)

    def test_add_team_wrong_type_raises_error(self):
        """Test raising TypeError when adding a non-Team object."""
        with self.assertRaises(TypeError):
            self.league.add_team("NotATeam")

    def test_remove_team(self):
        """Test removing a team from the league."""
        self.league.add_team(self.team1)
        self.league.remove_team(self.team1)
        self.assertNotIn(self.team1, self.league.teams)

    def test_remove_nonexistent_team_raises_error(self):
        """Test raising ValueError when removing a team not in the league."""
        with self.assertRaises(ValueError):
            self.league.remove_team(self.team1)

    def test_get_team_by_name(self):
        """Test finding a team by its name."""
        self.league.add_team(self.team1)
        result = self.league.get_team_by_name("Arsenal")
        self.assertEqual(result, self.team1)

    def test_get_team_by_name_not_found(self):
        """Test returning None if team name not found."""
        result = self.league.get_team_by_name("Real Madrid")
        self.assertIsNone(result)

    def test_get_top_team(self):
        """Test getting the top team from standings."""
        self.league.add_team(self.team1)
        self.league.add_team(self.team2)
        self.assertEqual(self.league.get_top_team(), self.team2)

    def test_get_top_team_empty(self):
        """Test returning None when league has no teams."""
        self.assertIsNone(self.league.get_top_team())

    def test_get_top_team_with_equal_points(self):
        """Test returning top team based on goal difference when points are equal."""
        team_a = Team("Brighton")
        team_b = Team("Newcastle")

        team_a.points = 10
        team_a.goals_scored = 12
        team_a.goals_conceded = 5  # goal difference = +7

        team_b.points = 10
        team_b.goals_scored = 15
        team_b.goals_conceded = 3  # goal difference = +12

        self.league.add_team(team_a)
        self.league.add_team(team_b)

        top = self.league.get_top_team()
        self.assertEqual(top, team_b)

    def test_get_bottom_team(self):
        """Test getting the bottom team from the league."""
        self.team1.points = 12
        self.team1.goals_scored = 10
        self.team1.goals_conceded = 8

        self.team2.points = 9
        self.team2.goals_scored = 8
        self.team2.goals_conceded = 10

        self.team3.points = 9
        self.team3.goals_scored = 5
        self.team3.goals_conceded = 12

        self.league.add_team(self.team1)
        self.league.add_team(self.team2)
        self.league.add_team(self.team3)

        result = self.league.get_bottom_team()
        self.assertEqual(result, self.team3)

    def test_get_bottom_team_with_equal_points(self):
        """Test returning bottom team based on goal difference when points are equal."""
        team_a = Team("Everton")
        team_b = Team("Sheffield United")

        team_a.points = 10
        team_a.goals_scored = 5
        team_a.goals_conceded = 8  # goal diff = -3

        team_b.points = 10
        team_b.goals_scored = 3
        team_b.goals_conceded = 8  # goal diff = -5

        self.league.add_team(team_a)
        self.league.add_team(team_b)

        bottom = self.league.get_bottom_team()
        self.assertEqual(bottom, team_b)

    def test_get_bottom_team_empty(self):
        """Test returning None when league has no teams."""
        self.assertIsNone(self.league.get_bottom_team())

    def test_get_team_stats(self):
        """Test retrieving statistics for a team by name."""
        self.team1.wins = 5
        self.team1.draws = 0
        self.team1.losses = 0
        self.league.add_team(self.team1)

        stats = self.league.get_team_stats("Arsenal")
        expected = {
            "points": 15,
            "wins": 5,
            "draws": 0,
            "losses": 0,
            "goals_scored": 20,
            "goals_conceded": 10
        }
        self.assertEqual(stats, expected)

    def test_get_team_stats_team_not_found_error(self):
        """Test raising ValueError when team is not found by name."""
        with self.assertRaises(ValueError):
            self.league.get_team_stats("Barcelona")

    def test_has_team(self):
        """Test checking if a team exists in the league by name."""
        self.league.add_team(self.team1)

        test_cases = [
            ("Arsenal", True),
            ("Real Madrid", False),
            ("Manchester United", False),
        ]

        for name, expected in test_cases:
            with self.subTest(team_name=name):
                self.assertEqual(self.league.has_team(name), expected)

    def test_replace_team(self):
        """Test replacing an existing team in the league."""
        self.league.add_team(self.team1)
        new_team = Team("Aston Villa")
        self.league.replace_team(self.team1, new_team)
        self.assertIn(new_team, self.league.teams)
        self.assertNotIn(self.team1, self.league.teams)

    def test_replace_team_not_in_league_raises_error(self):
        """Test raising ValueError when old team is not in the league."""
        new_team = Team("Tottenham Hotspur")
        with self.assertRaises(ValueError):
            self.league.replace_team(self.team1, new_team)