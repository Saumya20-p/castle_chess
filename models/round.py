"""Round model representing a collection of matches within a tournament."""

# ==========================================
# IMPORTS & DEPENDENCIES
# Objective: Bring in datetime for timestamps and Match class
# ==========================================
from datetime import datetime
from typing import List, Optional
from models.match import Match


# ==========================================
# SECTION 1: ROUND CLASS DEFINITION
# Objective: Manage a collection of matches for a tournament round
# ==========================================
class Round:
    """Represents a single round of chess matches."""

    def __init__(
        self,
        name: str,
        matches: Optional[List[Match]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ):
        self.name = name
        # Initialize empty matches list safely if none provided
        self.matches = matches if matches is not None else []
        # Stamp start time immediately if not loaded from file
        self.start_time = (
            start_time
            if start_time
            else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.end_time = end_time

    # ==========================================
    # SECTION 2: TIMESTAMP CONTROL
    # Objective: Lock in end date/time when round completes
    # ==========================================
    def mark_complete(self) -> None:
        """Records timestamp when all matches in the round complete."""
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================================
    # SECTION 3: JSON SERIALIZATION METHODS
    # Objective: Convert Round and its matches to/from JSON format
    # ==========================================
    def to_dict(self) -> dict:
        """Serializes the Round instance to a dictionary for JSON storage."""
        return {
            "name": self.name,
            "matches": [match.to_tuple() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Round":
        """Instantiates a Round object from JSON data."""
        matches = [Match.from_tuple(m) for m in data.get("matches", [])]
        return cls(
            name=data["name"],
            matches=matches,
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
        )

    # ==========================================
    # SECTION 4: DISPLAY REPRESENTATION
    # Objective: Quick text summary of round status
    # ==========================================
    def __str__(self) -> str:
        return f"{self.name} ({len(self.matches)} matches)"
