# Football Manager Simulator

A football manager simulation that allows users to manage football teams, simulate matches, train players, and track league standings.

## Features

- **Team Management**: Add/remove players, assign formations, track statistics
- **Player Management**: Train, rest, transfer, loan, and evaluate player performance
- **League System**: Add/remove teams, track top/bottom teams, retrieve stats
- **Match Simulation**: Simulate matches between teams, including draws, wins, and injuries
- **Data Persistence**: Save/load team data to and from JSON files
- **Test Coverage**: Over 100 unit tests with high code coverage

## Project Structure

```
football_manager/
├── src/
│   ├── __init__.py
│   ├── player.py
│   ├── team.py
│   ├── manager.py
│   └── league.py
├── tests/
│   ├── __init__.py
│   ├── test_player.py
│   ├── test_team.py
│   ├── test_manager.py
│   └── test_league.py
├── test_team_file.json
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests:

```bash
python -m unittest discover tests
```


## Code Style

The project follows PEP8 conventions and uses type hints where applicable.

## Usage Examples

```python
from src.player import Player, Position
from src.team import Team
from src.manager import Manager
from src.league import League

# Create team and manager
team = Team("FC Barcelona")
players = [Player(f"Player {i}", Position.MIDFIELDER, 25, 75 + i) for i in range(11)]
for p in players:
    team.add_player(p)
team.assign_starting_eleven(players)
manager = Manager(team)

# Create opponent
opponent = Team("Real Madrid")
rivals = [Player(f"Rival {i}", Position.DEFENDER, 26, 70 + i) for i in range(11)]
for r in rivals:
    opponent.add_player(r)
opponent.assign_starting_eleven(rivals)

# Simulate a match
result = manager.simulate_match(opponent)
print("Match result:", result)
```

Parts of this project — JSON data file, docstrings,
and selected method implementations — were generated or assisted by ChatGPT