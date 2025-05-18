"""Module defining the League class for managing football leagues."""

from src.team import Team


class League:
    """Class representing a football league."""

    def __init__(self, name):
        """Initialize a league with a name and empty team list.

        Args:
            name (str): Name of the league.
        """
        self.name = name
        self.teams = []

    def add_team(self, team):
        """Add a team to the league.

        Args:
            team (Team): Team to be added.

        Raises:
            TypeError: If object is not a Team.
            ValueError: If team is already in the league.
        """
        if not isinstance(team, Team):
            raise TypeError("Only Team instances can be added.")
        if team in self.teams:
            raise ValueError("Team already in league.")
        self.teams.append(team)

    def remove_team(self, team):
        """Remove a team from the league.

        Args:
            team (Team): Team to be removed.

        Raises:
            ValueError: If team is not found in the league.
        """
        if team not in self.teams:
            raise ValueError("Team not found in league.")
        self.teams.remove(team)

    def get_team_by_name(self, name):
        """Return a team by its name.

        Args:
            name (str): Team name.

        Returns:
            Team or None: Found team or None if not found.
        """
        for team in self.teams:
            if team.name == name:
                return team
        return None

    def get_top_team(self):
        """Return the team with the most points and best goal difference.

        Returns:
            Team or None: Top team or None if no teams.
        """
        if not self.teams:
            return None

        top_team = self.teams[0]

        for team in self.teams[1:]:
            if team.points > top_team.points:
                top_team = team
            elif team.points == top_team.points:
                top_diff = top_team.goals_scored - top_team.goals_conceded
                team_diff = team.goals_scored - team.goals_conceded
                if team_diff > top_diff:
                    top_team = team

        return top_team

    def get_bottom_team(self):
        """Return the team with the fewest points and worst goal difference.

        Returns:
            Team or None: Bottom team or None if no teams.
        """
        if not self.teams:
            return None

        bottom_team = self.teams[0]

        for team in self.teams[1:]:
            if team.points < bottom_team.points:
                bottom_team = team
            elif team.points == bottom_team.points:
                bottom_diff = bottom_team.goals_scored - bottom_team.goals_conceded
                team_diff = team.goals_scored - team.goals_conceded
                if team_diff < bottom_diff:
                    bottom_team = team

        return bottom_team

    def get_team_stats(self, name):
        """Return statistics of a team by name.

        Args:
            name (str): Name of the team.

        Returns:
            dict: Dictionary with stats (points, wins, draws, losses, goals).

        Raises:
            ValueError: If the team is not found.
        """
        team = self.get_team_by_name(name)
        if team is None:
            raise ValueError("Team not found.")

        return {
            "points": team.points,
            "wins": team.wins,
            "draws": team.draws,
            "losses": team.losses,
            "goals_scored": team.goals_scored,
            "goals_conceded": team.goals_conceded
        }

    def has_team(self, name):
        """Check if a team with given name is in the league.

        Args:
            name (str): Name of the team.

        Returns:
            bool: True if team exists in the league, False otherwise.
        """
        return any(team.name == name for team in self.teams)

    def replace_team(self, old_team, new_team):
        """Replace a team in the league with another team.

        Args:
            old_team (Team): Team to be replaced.
            new_team (Team): New team to insert.

        Raises:
            ValueError: If old_team is not in the league.
        """
        if old_team not in self.teams:
            raise ValueError("Old team not in league.")
        self.teams[self.teams.index(old_team)] = new_team