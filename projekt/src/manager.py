"""Module defining the Manager class for handling teams and simulations."""

import json
from src.team import Team
from src.player import Player, Position


class Manager:
    """Class to manage team operations and simulate matches."""

    def __init__(self, team: Team):
        """Initialize the manager with a team and default budget.

        Args:
            team (Team): Team managed by this manager.
        """
        self.team = team
        self.budget = 100  # in millions

    def save_team_to_file(self, filename):
        """Save team data to a JSON file.

        Args:
            filename (str): Path to the output file.
        """
        data = {
            "team_name": self.team.name,
            "players": [
                {
                    "name": p.name,
                    "position": p.position.name,
                    "age": p.age,
                    "rating": p.overall_rating,
                    "stamina": p.stamina,
                    "injured": p.injured
                } for p in self.team.players
            ]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_team_from_file(self, filename):
        """Load team data from a JSON file.

        Args:
            filename (str): Path to the input file.

        Returns:
            Team: Loaded team object.
        """
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        team = Team(data["team_name"])
        for p in data["players"]:
            player = Player(p["name"], Position[p["position"]], p["age"], p["rating"])
            player.stamina = p["stamina"]
            player.injured = p["injured"]
            team.add_player(player)
        return team

    def simulate_match(self, other_team):
        """Simulate a match based on average rating and stamina. Update stats.

        Args:
            other_team (Team): Opponent team.

        Returns:
            str: Match result string with score.

        Raises:
            ValueError: If either team has fewer than 11 players in starting eleven.
        """
        players_self = self.team.starting_eleven
        players_other = other_team.starting_eleven

        if len(players_self) < 11 or len(players_other) < 11:
            raise ValueError("Match cannot be played due to unavailable players.")

        avg_rating_self = sum(p.overall_rating for p in players_self) / 11
        avg_stamina_self = sum(p.stamina for p in players_self) / 11
        strength_self = (avg_rating_self + avg_stamina_self) / 2

        avg_rating_opp = sum(p.overall_rating for p in players_other) / 11
        avg_stamina_opp = sum(p.stamina for p in players_other) / 11
        strength_opp = (avg_rating_opp + avg_stamina_opp) / 2

        goals_self = int(strength_self) // 20
        goals_opp = int(strength_opp) // 20

        self.team.update_match_result(goals_self, goals_opp)
        other_team.update_match_result(goals_opp, goals_self)

        if goals_self > goals_opp:
            return f"{self.team.name} wins {goals_self}-{goals_opp}!"
        elif goals_opp > goals_self:
            return f"{other_team.name} wins {goals_opp}-{goals_self}!"
        else:
            return f"Draw {goals_self}-{goals_opp}!"

    def train_team(self):
        """Train all players in the team who are not injured."""
        for player in self.team.players:
            if not player.injured:
                player.train()

    def rest_team(self):
        """Rest all players in the team."""
        for player in self.team.players:
            player.rest()

    def bench_injured_players(self):
        """Move injured starting players to the bench."""
        if not self.team.starting_eleven:
            return

        healthy = [p for p in self.team.starting_eleven if not p.injured]
        injured = [p for p in self.team.starting_eleven if p.injured]

        self.team.starting_eleven = healthy
        self.team.bench.extend(injured)

    def buy_player(self, player: Player, price: int):
        """Buy a player and add to team if budget and space allow.

        Args:
            player (Player): The player to purchase.
            price (int): Cost in millions.

        Raises:
            ValueError: If player already in team, budget too low or team is full.
        """
        if player in self.team.players:
            raise ValueError("Player already in team.")
        if len(self.team.players) >= self.team.max_players:
            raise ValueError("Team has reached maximum size.")
        if price > self.budget:
            raise ValueError("Insufficient budget to buy player.")

        self.team.add_player(player)
        self.budget -= price

    def sell_player(self, player: Player, price: int):
        """Sell a player and increase budget.

        Args:
            player (Player): The player to sell.
            price (int): Transfer value in millions.

        Raises:
            ValueError: If player is not in team.
        """
        if player not in self.team.players:
            raise ValueError("Player not found in team.")
        self.team.remove_player(player)
        self.budget += price



