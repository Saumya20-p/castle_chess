"""Player model representing a chess tournament participant."""


# ==========================================
# SECTION 1: PLAYER CLASS DEFINITION
# Objective: Store individual player profiles and details
# ==========================================
class Player:
    """Represents a chess player with their profile information."""

    def __init__(
        self,
        chess_id: str,
        first_name: str,
        last_name: str,
        birthdate: str,
    ):
        # Save national chess ID (e.g., AB12345)
        self.chess_id = chess_id
        # Save player's first name
        self.first_name = first_name
        # Save player's last name
        self.last_name = last_name
        # Save date of birth as string
        self.birthdate = birthdate

    # ==========================================
    # SECTION 2: HELPER PROPERTIES
    # Objective: Combine fields into user-friendly attributes
    # ==========================================
    @property
    def full_name(self) -> str:
        """Returns the player's full name."""
        return f"{self.first_name} {self.last_name}"

    # ==========================================
    # SECTION 3: JSON SERIALIZATION METHODS
    # Objective: Convert object back and forth with JSON dictionary format
    # ==========================================
    def to_dict(self) -> dict:
        """Converts the Player instance into a dictionary for JSON storage."""
        return {
            "chess_id": self.chess_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Instantiates a Player object from a JSON-loaded dictionary."""
        return cls(
            chess_id=data["chess_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            birthdate=data["birthdate"],
        )

    # ==========================================
    # SECTION 4: DISPLAY REPRESENTATION
    # Objective: Show human-readable string when printed
    # ==========================================
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.full_name} ({self.chess_id})"
