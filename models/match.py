"""Match model representing a paired game between two players."""

# ==========================================
# IMPORTS & DEPENDENCIES
# Objective: Bring in type hints and our Player class
# ==========================================
from typing import List, Tuple
from models.player import Player


# ==========================================
# SECTION 1: MATCH CLASS DEFINITION
# Objective: Store two paired players and their game scores
# ==========================================
class Match:
    """Represents a chess match between two players and their scores."""

    def __init__(
        self,
        player_1: Player,
        player_2: Player,
        score_1: float = 0.0,
        score_2: float = 0.0,
    ):
        # Store first Player object
        self.player_1 = player_1
        # Store second Player object
        self.player_2 = player_2
        # Set player 1 starting score (defaults to 0.0)
        self.score_1 = score_1
        # Set player 2 starting score (defaults to 0.0)
        self.score_2 = score_2

    # ==========================================
    # SECTION 2: MATCH UPDATE METHODS
    # Objective: Update scores when game finishes
    # ==========================================
    def set_result(self, score_1: float, score_2: float) -> None:
        """Updates the match score after a game finishes."""
        # Score values: 1.0 = win, 0.5 = draw, 0.0 = loss
        self.score_1 = score_1
        self.score_2 = score_2

    # ==========================================
    # SECTION 3: TUPLE SERIALIZATION METHODS
    # Objective: Format match as ([player1, score1], [player2, score2]) per spec
    # ==========================================
    def to_tuple(self) -> Tuple[List, List]:
        """Converts match instance to the spec-required list/tuple format."""
        return (
            [self.player_1.to_dict(), self.score_1],
            [self.player_2.to_dict(), self.score_2],
        )

    @classmethod
    def from_tuple(cls, data: list) -> "Match":
        """Reconstructs a Match instance from stored serialized tuple data."""
        # Unpack player data dictionaries and scores
        p1_data, s1 = data[0]
        p2_data, s2 = data[1]
        # Rebuild Player objects
        player_1 = Player.from_dict(p1_data)
        player_2 = Player.from_dict(p2_data)
        return cls(player_1=player_1, player_2=player_2, score_1=s1, score_2=s2)

    # ==========================================
    # SECTION 4: DISPLAY REPRESENTATION
    # Objective: Show clean matchup summary when printed
    # ==========================================
    def __str__(self) -> str:
        return (
            f"{self.player_1.full_name} ({self.score_1}) vs "
            f"{self.player_2.full_name} ({self.score_2})"
        )
