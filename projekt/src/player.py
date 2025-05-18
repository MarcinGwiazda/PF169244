"""Module defining the Player class and Position enum for football manager."""

from enum import Enum, auto


class Position(Enum):
    """Enum representing player positions on the field."""
    GOALKEEPER = auto()
    DEFENDER = auto()
    MIDFIELDER = auto()
    FORWARD = auto()


class Player:
    """Class representing a football player."""

    def __init__(self, name, position, age, overall_rating):
        """Initialize a player with full attributes.

        Args:
            name (str): Player's full name.
            position (Position): Player's position.
            age (int): Player's age (15–50).
            overall_rating (int): Skill rating (0–100).

        Raises:
            ValueError: If age or rating is out of realistic range.
        """
        if overall_rating < 0 or overall_rating > 100:
            raise ValueError("Overall rating must be between 0 and 100.")
        if age < 15 or age > 50:
            raise ValueError("Invalid age for player.")

        self.name = name
        self.position = position
        self.age = age
        self.overall_rating = overall_rating
        self.stamina = 100
        self.injured = False
        self.is_captain = False
        self.goals = 0
        self.assists = 0
        self.matches_played = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.suspended = False
        self.contract_years_left = 3
        self.morale = 70
        self.retired = False
        self.on_loan = False
        self.loaned_to = None  # string with team name
        self.loan_duration = 0  # number of games

    def train(self):
        """Simulate training session.

        Increases rating slightly, decreases stamina.
        """
        if not self.injured:
            self.overall_rating = min(100, self.overall_rating + 1)
            self.stamina = max(0, self.stamina - 10)

    def rest(self):
        """Recover stamina by resting."""
        self.stamina = min(100, self.stamina + 20)

    def injure(self):
        """Set player's injured status to True."""
        self.injured = True

    def is_exhausted(self) -> bool:
        """Check if player's stamina is too low to play."""
        return self.stamina < 30

    def recover_from_injury(self):
        """Set injured to False."""
        if not self.injured:
            raise ValueError("Player is not injured.")
        self.injured = False

    def age_up(self):
        """Increase player's age by 1. Decrease rating only if age > 30."""
        self.age += 1
        if self.age > 30:
            self.overall_rating = max(0, self.overall_rating - 1)

    def change_position(self, new_position: Position):
        """Change the player's position.

        Args:
            new_position (Position): New position to assign.

        Raises:
            TypeError: If new_position is not a Position enum.
        """
        if not isinstance(new_position, Position):
            raise TypeError("new_position must be an instance of Position enum.")
        self.position = new_position

    def promote_to_captain(self):
        """Mark this player as team captain."""
        self.is_captain = True

    def demote_from_captain(self):
        """Remove captain status from the player."""
        self.is_captain = False

    def record_match(self, goals=0, assists=0):
        """Update player's statistics after a match."""
        if goals < 0 or assists < 0:
            raise ValueError("Goals and assists cannot be negative.")
        self.goals += goals
        self.assists += assists
        self.matches_played += 1

    def receive_card(self, card_type):
        """Give player a yellow or red card, and suspend if needed."""
        if card_type == "yellow":
            self.yellow_cards += 1
            if self.yellow_cards == 2:
                self.red_cards += 1
                self.yellow_cards = 0
                self.suspended = True
        elif card_type == "red":
            self.red_cards += 1
            self.suspended = True
        else:
            raise ValueError("Invalid card type.")

    def reset_cards(self):
        """Clear player's cards and suspension status"""
        self.yellow_cards = 0
        self.red_cards = 0
        self.suspended = False

    def renew_contract(self, years):
        """Renew player's contract for a given number of years."""
        if years <= 0:
            raise ValueError("Contract must be for at least 1 year.")
        self.contract_years_left = years

    def is_contract_expiring(self):
        """Check if contract is expiring within a year."""
        return self.contract_years_left <= 1

    def decrement_contract(self):
        """Decrease contract duration by 1 year if not already 0."""
        if self.contract_years_left > 0:
            self.contract_years_left -= 1

    def change_morale(self, amount):
        """Adjust player's morale by a given amount (positive or negative).

        Args:
            amount (int): Value to change morale by.

        Raises:
            ValueError: If amount is not an integer.
        """
        if not isinstance(amount, int):
            raise ValueError("Morale change must be an integer.")
        self.morale = max(0, min(100, self.morale + amount))

    def get_morale_status(self):
        """Return a string describing current morale level."""
        if self.morale >= 80:
            return "Excellent"
        elif self.morale >= 60:
            return "Good"
        elif self.morale >= 40:
            return "Average"
        elif self.morale >= 20:
            return "Low"
        else:
            return "Very Low"

    def check_retirement(self):
        """Automatically retire the player if age exceeds 40."""
        if self.age >= 40:
            self.retired = True

    def loan_to(self, club_name, duration):
        """Loan player to another club."""
        if self.on_loan:
            raise ValueError("Player is already on loan.")
        if duration <= 0:
            raise ValueError("Duration must be positive.")

        self.on_loan = True
        self.loaned_to = club_name
        self.loan_duration = duration

    def return_from_loan(self):
        """Return player from loan."""
        if not self.on_loan:
            raise ValueError("Player is not on loan.")
        self.on_loan = False
        self.loaned_to = None
        self.loan_duration = 0

    def reduce_loan_duration(self):
        """Reduce loan duration after each match/week."""
        if self.on_loan:
            self.loan_duration -= 1
            if self.loan_duration <= 0:
                self.return_from_loan()

    def get_market_value(self):
        """Return player's market value in millions based on rating, age and goals."""
        base = self.overall_rating * 0.4
        age_bonus = max(0, (30 - self.age)) * 0.3
        goal_bonus = self.goals * 0.1
        value = base + age_bonus + goal_bonus
        return round(value, 2)