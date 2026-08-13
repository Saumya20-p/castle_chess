"""Main console views for terminal user interactions."""

# ==========================================
# IMPORTS & DEPENDENCIES
# ==========================================
from typing import List
from models.player import Player
from models.tournament import Tournament


# ==========================================
# SECTION 1: MAIN VIEW CLASS
# Objective: Display menus and capture user inputs via console
# ==========================================
class MainView:
    """Handles console output formatting and menu user prompts."""

    # ==========================================
    # SECTION 2: HEADER & MENU RENDERING
    # ==========================================
    @staticmethod
    def display_header(title: str) -> None:
        """Prints a styled ASCII section header."""
        print("\n" + "=" * 50)
        print(f"  {title.upper()}")
        print("=" * 50)

    @staticmethod
    def display_main_menu() -> str:
        """Displays the top-level main menu and returns user choice."""
        print("\n=== CASTLE CHESS TOURNAMENT MANAGER ===")
        print("1. Manage Players")
        print("2. Manage Tournaments")
        print("3. Generate Reports")
        print("4. Exit")
        return input("\nSelect an option (1-4): ").strip()

    # ==========================================
    # SECTION 3: PLAYER VIEWS & PROMPTS
    # ==========================================
    @staticmethod
    def display_player_menu() -> str:
        """Displays player management sub-menu choices."""
        print("\n--- PLAYER MANAGEMENT ---")
        print("1. Add New Player")
        print("2. View All Players")
        print("3. Back to Main Menu")
        return input("\nSelect an option (1-3): ").strip()

    @staticmethod
    def get_player_info() -> dict:
        """Prompts user to enter new player information."""
        print("\nEnter Player Details:")
        chess_id = input("National Chess ID (e.g. AB12345): ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        birthdate = input("Birthdate (DD-MM-YYYY): ").strip()
        club = input("Club Name (optional): ").strip()
        return {
            "chess_id": chess_id,
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "club": club,
        }

    @staticmethod
    def display_players_list(players: List[Player]) -> None:
        """Displays a formatted list of players."""
        if not players:
            print("\nNo players registered yet.")
            return

        print(f"\n{'ID':<10} | {'NAME':<25} | {'BIRTHDATE':<12} | {'CLUB'}")
        print("-" * 70)
        for p in players:
            print(
                f"{p.chess_id:<10} | {p.full_name:<25} | "
                f"{p.birthdate:<12} | {p.club}"
            )

    # ==========================================
    # SECTION 4: TOURNAMENT VIEWS & PROMPTS
    # ==========================================
    @staticmethod
    def display_tournament_menu() -> str:
        """Displays tournament management sub-menu choices."""
        print("\n--- TOURNAMENT MANAGEMENT ---")
        print("1. Create New Tournament")
        print("2. Select & Run Active Tournament")
        print("3. View All Tournaments")
        print("4. Back to Main Menu")
        return input("\nSelect an option (1-4): ").strip()

    @staticmethod
    def get_tournament_info() -> dict:
        """Prompts user to enter new tournament parameters."""
        print("\nEnter Tournament Details:")
        name = input("Tournament Name: ").strip()
        location = input("Location/Venue: ").strip()
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        description = input("Description/Notes: ").strip()
        num_rounds_input = input("Number of Rounds (default 4): ").strip()
        number_of_rounds = int(num_rounds_input) if num_rounds_input.isdigit() else 4

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "number_of_rounds": number_of_rounds,
        }

    @staticmethod
    def display_tournaments_list(tournaments: List[Tournament]) -> None:
        """Displays a summary table of tournaments."""
        if not tournaments:
            print("\nNo tournaments found.")
            return

        print(f"\n{'#':<3} | {'NAME':<25} | {'LOCATION':<15} | {'ROUNDS'}")
        print("-" * 60)
        for idx, t in enumerate(tournaments, 1):
            print(
                f"{idx:<3} | {t.name:<25} | {t.location:<15} | "
                f"{t.current_round_index}/{t.number_of_rounds}"
            )
