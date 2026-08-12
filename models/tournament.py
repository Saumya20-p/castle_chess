"""Tournament model representing an entire chess tournament event."""

# ==========================================
# IMPORTS & DEPENDENCIES
# Objective: Bring in Player and Round models to construct full tournament
# ==========================================
from typing import List, Optional
from models.player import Player
from models.round import Round


# ==========================================
# SECTION 1: TOURNAMENT CLASS DEFINITION
# Objective: Hold overall tournament metadata, players, and rounds
# ==========================================
class Tournament:
    """Represents a complete chess tournament."""

    def __init__(
        self,
        name: str,
        location: str,
        start_date: str,
        end_date: str,
        description: str = "",
        number_of_rounds: int = 4,
        current_round_index: int = 0,
        players: Optional[List[Player]] = None,
        rounds: Optional[List[Round]] = None,
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round_index = current_round_index
        # Safely set default empty lists
        self.players = players if players is not None else []
        self.rounds = rounds if rounds is not None else []

    # ==========================================
    # SECTION 2: PLAYER REGISTRATION
    # Objective: Add players ensuring no duplicates by Chess ID
    # ==========================================
    def add_player(self, player: Player) -> None:
        """Adds a player to the tournament if not already registered."""
        if all(p.chess_id != player.chess_id for p in self.players):
            self.players.append(player)

    # ==========================================
    # SECTION 3: JSON SERIALIZATION METHODS
    # Objective: Convert full tournament tree to dictionary for JSON output
    # ==========================================
    def to_dict(self) -> dict:
        """Serializes the Tournament instance into a dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "current_round_index": self.current_round_index,
            "players": [p.to_dict() for p in self.players],
            "rounds": [r.to_dict() for r in self.rounds],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        """Instantiates a Tournament object from JSON data."""
        players = [Player.from_dict(p) for p in data.get("players", [])]
        rounds = [Round.from_dict(r) for r in data.get("rounds", [])]
        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data.get("description", ""),
            number_of_rounds=data.get("number_of_rounds", 4),
            current_round_index=data.get("current_round_index", 0),
            players=players,
            rounds=rounds,
        )

    # ==========================================
    # SECTION 4: DISPLAY REPRESENTATION
    # Objective: Quick tournament summary string
    # ==========================================
    def __str__(self) -> str:
        return f"{self.name} at {self.location} ({len(self.players)} players)"
