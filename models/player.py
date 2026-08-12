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
        club: str = "",
    ):
        # Save national chess ID (e.g., AB12345)
        self.chess_id = chess_id
        # Save player's first name
        self.first_name = first_name
        # Save player's last name
        self.last_name = last_name
        # Save date of birth as string
        self.birthdate = birthdate
        # Save club / team name
        self.club = club

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
            "club": self.club,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Instantiates a Player object from a JSON-loaded dictionary."""
        # Handle single 'name' key (e.g., "John Underwood") if first_name missing
        if "name" in data and "first_name" not in data:
            name_parts = data["name"].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
        else:
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")

        # Handle 'birthday' vs 'birthdate' key variations
        birthdate = data.get("birthdate") or data.get("birthday", "")

        # Extract club name (default to empty string if missing)
        club = data.get("club", "")

        return cls(
            chess_id=data["chess_id"],
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            club=club,
        )

    # ==========================================
    # SECTION 4: DISPLAY REPRESENTATION
    # Objective: Show human-readable string when printed
    # ==========================================
    def __str__(self) -> str:
        """Human-readable string representation."""
        club_str = f" [{self.club}]" if self.club else ""
        return f"{self.full_name} ({self.chess_id}){club_str}"
