"""Database Manager for loading and saving JSON data files."""

# ==========================================
# IMPORTS & DEPENDENCIES
# ==========================================
import json
import os
from typing import List
from models.player import Player
from models.tournament import Tournament


# ==========================================
# SECTION 1: DATABASE MANAGER CLASS
# ==========================================
class DatabaseManager:
    """Manages file reading and writing operations for JSON database files."""

    def __init__(
        self,
        clubs_dir: str = "data/clubs",
        tournaments_dir: str = "data/tournaments",
        players_file: str = "data/players.json",
    ):
        self.clubs_dir = clubs_dir
        self.tournaments_dir = tournaments_dir
        self.players_file = players_file
        self._ensure_directories_exist()

    # ==========================================
    # SECTION 2: DIRECTORY SETUP
    # ==========================================
    def _ensure_directories_exist(self) -> None:
        """Creates required data folders if missing."""
        os.makedirs(self.clubs_dir, exist_ok=True)
        os.makedirs(self.tournaments_dir, exist_ok=True)

    # ==========================================
    # SECTION 3: PLAYER DATA OPERATIONS
    # ==========================================
    def load_players(self) -> List[Player]:
        """Loads all players from data/players.json or scans data/clubs/ files."""
        players = []

        # First check local aggregated file
        if os.path.exists(self.players_file):
            try:
                with open(self.players_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [Player.from_dict(p) for p in data]
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Fallback: Scan data/clubs/ directory
        if os.path.exists(self.clubs_dir):
            for filename in os.listdir(self.clubs_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(self.clubs_dir, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            club_data = json.load(f)
                            club_name = club_data.get("name", filename.replace(".json", ""))
                            for p_dict in club_data.get("players", []):
                                p_dict["club"] = club_name
                                players.append(Player.from_dict(p_dict))
                    except (json.JSONDecodeError, FileNotFoundError):
                        continue

        return players

    def save_players(self, players: List[Player]) -> None:
        """Saves active player list to data/players.json."""
        data = [player.to_dict() for player in players]
        with open(self.players_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # ==========================================
    # SECTION 4: TOURNAMENT DATA OPERATIONS
    # ==========================================
    def load_tournaments(self) -> List[Tournament]:
        """Reads all tournament JSON files inside data/tournaments/."""
        tournaments = []
        if not os.path.exists(self.tournaments_dir):
            return tournaments

        for filename in os.listdir(self.tournaments_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.tournaments_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        tournaments.append(Tournament.from_dict(data))
                except (json.JSONDecodeError, FileNotFoundError):
                    continue

        # Sort tournaments descending by start date per technical specification
        tournaments.sort(key=lambda t: t.start_date, reverse=True)
        return tournaments

    def save_single_tournament(self, tournament: Tournament) -> None:
        """Saves or updates an individual tournament JSON file in data/tournaments/."""
        safe_name = "".join(c for c in tournament.name if c.isalnum() or c in (" ", "_", "-")).rstrip()
        filename = f"{safe_name.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.tournaments_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(tournament.to_dict(), f, indent=4)
