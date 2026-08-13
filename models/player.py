"""Player model representing a chess tournament participant."""


# ==========================================
# SECTION 1: PLAYER CLASS DEFINITION
# ==========================================
class Player:
    """Represents a chess player with their profile information."""

    def __init__(
        self,
        chess_id: str,
        first_name: str,
        last_name: str,
        birthdate: str,
        email: str = "",
        club: str = "",
    ):
        self.chess_id = chess_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.club = club

    # ==========================================
    # SECTION 2: HELPER PROPERTIES
    # ==========================================
    @property
    def full_name(self) -> str:
        """Returns the player's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    # ==========================================
    # SECTION 3: SERIALIZATION
    # ==========================================
    def to_dict(self) -> dict:
        """Converts the Player instance into a dictionary for JSON storage."""
        return {
            "chess_id": self.chess_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
            "email": self.email,
            "club": self.club,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Instantiates a Player object from a JSON dictionary."""
        if "name" in data and "first_name" not in data:
            name_parts = data["name"].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
        else:
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")

        birthdate = data.get("birthdate") or data.get("birthday", "")
        email = data.get("email", "")
        club = data.get("club", "")

        return cls(
            chess_id=data["chess_id"],
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            email=email,
            club=club,
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        club_str = f" [{self.club}]" if self.club else ""
        return f"{self.full_name} ({self.chess_id}){club_str}"
