"""Module defining the Team class for managing football teams."""

from typing import List
from src.player import Player, Position


class Team:
    """Class representing a football team."""

    def __init__(self, name):
        """Initialize a new team with default formation and empty roster.

        Args:
            name (str): Team name.
        """
        self.name = name
        self.players: List[Player] = []
        self.formation = "4-4-2"
        self.starting_eleven: List[Player] = []
        self.bench: List[Player] = []
        self.goals_scored = 0
        self.goals_conceded = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def add_player(self, player):
        """Add a player to the team.

        Args:
            player (Player): The player to add.

        Raises:
            ValueError: If player is already on the team or is retired.
        """
        if player in self.players:
            raise ValueError("Player already in team.")
        if player.retired:
            raise ValueError("Cannot add retired player.")
        self.players.append(player)

    def remove_player(self, player: Player):
        """Remove a player from the team.

        Args:
            player (Player): The player to remove.

        Raises:
            ValueError: If player not found in the team.
        """
        if player not in self.players:
            raise ValueError("Player not found.")
        self.players.remove(player)

    def set_formation(self, formation: str):
        """Set the tactical formation of the team.

        Args:
            formation (str): Formation string (e.g., "4-4-2").

        Raises:
            ValueError: If unsupported formation.
        """
        allowed = ["4-4-2", "4-3-3", "3-5-2"]
        if formation not in allowed:
            raise ValueError("Unsupported formation.")
        self.formation = formation

    def assign_starting_eleven(self, players: List[Player]):
        """Assign starting players for a match.

        Args:
            players (List[Player]): List of 11 starting players.

        Raises:
            ValueError: If list is not exactly 11 or players not in team.
        """
        if len(players) != 11:
            raise ValueError("Starting eleven must contain 11 players.")
        for p in players:
            if p not in self.players:
                raise ValueError(f"{p.name} not in team.")
        self.starting_eleven = players

    def update_match_result(self, goals_for, goals_against):
        """Update team stats after a match."""
        self.goals_scored += goals_for
        self.goals_conceded += goals_against

        if goals_for > goals_against:
            self.wins += 1
        elif goals_for < goals_against:
            self.losses += 1
        else:
            self.draws += 1

    def get_average_rating(self):
        """Calculate average rating of all players.

        Returns:
            float: Average rating or 0 if no players.
        """
        return sum(p.overall_rating for p in self.players) / len(self.players) if self.players else 0

    def get_injured_players(self):
        """List all currently injured players.

        Returns:
            List[Player]: List of injured players.
        """
        return [p for p in self.players if p.injured]

    def get_players_by_position(self, position: Position):
        """Get all players that play on a specific position.

        Args:
            position (Position): Position to filter by.

        Returns:
            List[Player]: Players matching the given position.
        """
        return [p for p in self.players if p.position == position]

    def get_best_player(self):
        """Get the player with the highest overall rating.

        Returns:
            Player: Best player in the team.
        """
        if not self.players:
            return None

        best_player = self.players[0]
        for player in self.players[1:]:
            if player.overall_rating > best_player.overall_rating:
                best_player = player
        return best_player

    def swap_players(self, player_out: Player, player_in: Player):
        """Swap an existing player with a new one.

        Args:
            player_out (Player): Player to remove.
            player_in (Player): Player to add.

        Raises:
            ValueError: If player_out is not in the team.
        """
        if player_out not in self.players:
            raise ValueError("Player to remove is not in the team.")
        self.remove_player(player_out)
        self.add_player(player_in)

    def get_average_age(self):
        """Calculate average age of team players."""
        if not self.players:
            return 0
        return sum(p.age for p in self.players) / len(self.players)

    def get_top_scorer(self):
        """Return player with the most goals."""
        if not self.players:
            return None

        top_scorer = self.players[0]
        for player in self.players[1:]:
            if player.goals > top_scorer.goals:
                top_scorer = player

        return top_scorer

    def get_top_assistant(self):
        """Return player with the most assists."""
        if not self.players:
            return None

        top_assistant = self.players[0]
        for player in self.players[1:]:
            if player.assists > top_assistant.assists:
                top_assistant = player

        return top_assistant

    def get_most_active_player(self):
        """Return player with the most matches played."""
        if not self.players:
            return None

        most_active = self.players[0]
        for player in self.players[1:]:
            if player.matches_played > most_active.matches_played:
                most_active = player

        return most_active

    def get_loaned_players(self):
        """Return all players currently on loan."""
        return [p for p in self.players if p.on_loan]