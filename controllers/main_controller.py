"""Main Controller coordinating application workflow, menus, and tournament execution."""

# ==========================================
# IMPORTS & DEPENDENCIES
# ==========================================
from controllers.database_manager import DatabaseManager
from controllers.swiss_pairing import SwissPairing
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from views.main_view import MainView


# ==========================================
# SECTION 1: MAIN CONTROLLER CLASS
# ==========================================
class MainController:
    """Coordinates interaction between Views, Models, and Storage."""

    def __init__(self):
        self.db = DatabaseManager()
        self.view = MainView()

    # ==========================================
    # SECTION 2: APPLICATION ENTRY POINT
    # ==========================================
    def run(self) -> None:
        """Main application execution loop."""
        while True:
            choice = self.view.display_main_menu()
            if choice == "1":
                self._manage_players()
            elif choice == "2":
                self._manage_tournaments()
            elif choice == "3":
                self._generate_reports()
            elif choice == "4":
                print("\nThank you for using Castle Chess Manager. Goodbye!")
                break
            else:
                print("\nInvalid selection. Please enter 1-4.")

    # ==========================================
    # SECTION 3: PLAYER MANAGEMENT FLOW
    # ==========================================
    def _manage_players(self) -> None:
        """Handles player creation, search, and listing operations."""
        while True:
            choice = self.view.display_player_menu()
            if choice == "1":
                data = self.view.get_player_info()
                player = Player.from_dict(data)
                players = self.db.load_players()
                players.append(player)
                self.db.save_players(players)
                print(f"\nSuccessfully added player: {player.full_name}")
            elif choice == "2":
                players = self.db.load_players()
                sorted_players = sorted(players, key=lambda p: p.last_name)
                self.view.display_players_list(sorted_players)
            elif choice == "3":
                break

    # ==========================================
    # SECTION 4: TOURNAMENT MANAGEMENT FLOW
    # ==========================================
    def _manage_tournaments(self) -> None:
        """Handles tournament creation, selection, and management screens."""
        while True:
            choice = self.view.display_tournament_menu()
            if choice == "1":
                self._create_tournament()
            elif choice == "2":
                self._select_and_manage_tournament()
            elif choice == "3":
                tournaments = self.db.load_tournaments()
                self.view.display_tournaments_list(tournaments)
            elif choice == "4":
                break

    def _create_tournament(self) -> None:
        """Interactively creates a new tournament and registers players."""
        info = self.view.get_tournament_info()
        tournament = Tournament.from_dict(info)

        players = self.db.load_players()
        if not players:
            print("\nNo players available in the database. Please add players first.")
            return

        print(f"\n--- REGISTER PLAYERS FOR {tournament.name.upper()} ---")
        self._register_players_to_tournament(tournament, players)
        self.db.save_single_tournament(tournament)
        print(f"\nTournament '{tournament.name}' successfully created and saved!")

    def _select_and_manage_tournament(self) -> None:
        """Displays available tournaments sorted descending by start date and manages selection."""
        tournaments = self.db.load_tournaments()
        if not tournaments:
            print("\nNo tournaments found.")
            return

        self.view.display_tournaments_list(tournaments)
        choice = input("\nSelect tournament number to manage (or press Enter to cancel): ").strip()
        if not choice.isdigit():
            return

        t_idx = int(choice) - 1
        if 0 <= t_idx < len(tournaments):
            self._manage_single_tournament(tournaments[t_idx])

    def _manage_single_tournament(self, tournament: Tournament) -> None:
        """View/Manage Tournament screen as specified in the technical specifications."""
        while True:
            status = (
                "Completed"
                if tournament.current_round_index >= tournament.number_of_rounds
                else f"Round {tournament.current_round_index + 1} of {tournament.number_of_rounds}"
            )
            print(f"\n=== VIEW/MANAGE TOURNAMENT: {tournament.name.upper()} ===")
            print(f"Venue: {tournament.location}")
            print(f"Dates: {tournament.start_date} to {tournament.end_date}")
            print(f"Status: {status}")
            print(f"Registered Players ({len(tournament.players)}):")
            for p in tournament.players:
                print(f" - {p.full_name} ({p.chess_id}) [{p.club}]")

            print("\nOptions:")
            print("1. Register a Player for this Tournament")
            print("2. Enter Results for Current Round")
            print("3. Advance to Next Round")
            print("4. View Tournament Report")
            print("5. Back to Tournament Menu")

            opt = input("\nSelect an option (1-5): ").strip()

            if opt == "1":
                all_players = self.db.load_players()
                self._register_players_to_tournament(tournament, all_players)
                self.db.save_single_tournament(tournament)
            elif opt == "2":
                self._enter_round_results(tournament)
            elif opt == "3":
                self._advance_to_next_round(tournament)
            elif opt == "4":
                self._show_tournament_report(tournament)
            elif opt == "5":
                break

    # ==========================================
    # SECTION 5: PLAYER SEARCH & REGISTRATION
    # ==========================================
    def _register_players_to_tournament(self, tournament: Tournament, available_players: list) -> None:
        """Supports searching players by Chess ID or case-insensitive name substring and registering them."""
        while True:
            query = input(
                "\nSearch player by Chess ID or name (or type 'all' to add all, 'done' to finish): "
            ).strip()

            if query.lower() == "done":
                break
            if query.lower() == "all":
                for p in available_players:
                    tournament.add_player(p)
                print(f"Registered all {len(available_players)} available players.")
                break

            # Search by exact Chess ID or case-insensitive substring
            results = [
                p for p in available_players
                if query.lower() == p.chess_id.lower() or query.lower() in p.full_name.lower()
            ]

            if not results:
                print("No players found matching search query.")
                continue

            print("\nSearch Results:")
            for idx, p in enumerate(results, 1):
                print(f"{idx}. {p.full_name} ({p.chess_id}) - {p.club}")

            sel = input("\nSelect player number to register (or press Enter to skip): ").strip()
            if sel.isdigit():
                s_idx = int(sel) - 1
                if 0 <= s_idx < len(results):
                    tournament.add_player(results[s_idx])
                    print(f"Successfully registered {results[s_idx].full_name}!")

    # ==========================================
    # SECTION 6: ROUND EXECUTION & PAIRING
    # ==========================================
    def _advance_to_next_round(self, tournament: Tournament) -> None:
        """Prompts for confirmation before advancing and generating next round Swiss pairings."""
        if len(tournament.players) < 2:
            print("\nTournament requires at least 2 registered players to generate pairings.")
            return

        if tournament.current_round_index >= tournament.number_of_rounds:
            print("\nTournament is already marked as completed!")
            return

        # Check if active round matches have scores recorded
        if tournament.rounds:
            latest_round = tournament.rounds[-1]
            if latest_round.end_time is None:
                print("\nPlease enter scores for all matches in the current round before advancing!")
                return

        # Required confirmation prompt per specification PDF
        confirm = input(
            f"\nAre you sure you want to advance to Round {tournament.current_round_index + 1}? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("Operation cancelled.")
            return

        # Generate Swiss pairings and instantiate new round
        round_num = tournament.current_round_index + 1
        matches = SwissPairing.generate_next_round_matches(tournament)
        new_round = Round(name=f"Round {round_num}", matches=matches)

        tournament.rounds.append(new_round)
        self.db.save_single_tournament(tournament)
        print(f"\nSuccessfully advanced to Round {round_num}! {len(matches)} matches paired.")

    def _enter_round_results(self, tournament: Tournament) -> None:
        """Displays current round matches and captures scores (1.0 win, 0.5 tie, 0.0 loss)."""
        if not tournament.rounds:
            print("\nNo active round found. Advance to Round 1 first!")
            return

        current_round = tournament.rounds[-1]
        print(f"\n=== ENTER MATCH RESULTS FOR {current_round.name.upper()} ===")

        for idx, match in enumerate(current_round.matches, 1):
            print(f"\nMatch {idx}: {match.player_1.full_name} vs {match.player_2.full_name}")
            print("Score options: 1 = Player 1 Win, 2 = Player 2 Win, 0 = Tie/Draw")
            res = input("Enter result (1/2/0): ").strip()

            if res == "1":
                match.set_result(1.0, 0.0)
            elif res == "2":
                match.set_result(0.0, 1.0)
            elif res == "0":
                match.set_result(0.5, 0.5)
            else:
                print("Invalid entry. Defaulting to draw (0.5 - 0.5).")
                match.set_result(0.5, 0.5)

        current_round.mark_complete()
        tournament.current_round_index = len(tournament.rounds)
        self.db.save_single_tournament(tournament)
        print(f"\nScores for {current_round.name} saved successfully!")

    # ==========================================
    # SECTION 7: REPORT GENERATION
    # ==========================================
    def _generate_reports(self) -> None:
        """Global report view menu."""
        print("\n--- TOURNAMENT REPORTS ---")
        print("1. All Players (Alphabetical by Last Name)")
        print("2. All Tournaments (Sorted Descending by Date)")
        print("3. View Detailed Tournament Summary & Match History")

        choice = input("\nSelect report option (1-3): ").strip()
        if choice == "1":
            players = self.db.load_players()
            sorted_players = sorted(players, key=lambda p: p.last_name)
            self.view.display_players_list(sorted_players)
        elif choice == "2":
            tournaments = self.db.load_tournaments()
            self.view.display_tournaments_list(tournaments)
        elif choice == "3":
            tournaments = self.db.load_tournaments()
            if not tournaments:
                print("\nNo tournaments found.")
                return
            self.view.display_tournaments_list(tournaments)
            sel = input("\nSelect tournament number: ").strip()
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(tournaments):
                    self._show_tournament_report(tournaments[idx])

    def _show_tournament_report(self, tournament: Tournament) -> None:
        """Displays detailed report with players sorted descending by score."""
        scores = SwissPairing.calculate_scores(tournament)
        sorted_players = sorted(
            tournament.players,
            key=lambda p: scores.get(p.chess_id, 0.0),
            reverse=True,
        )

        print("\n==================================================")
        print(f"       TOURNAMENT REPORT: {tournament.name.upper()}")
        print("==================================================")
        print(f"Venue: {tournament.location}")
        print(f"Dates: {tournament.start_date} to {tournament.end_date}")
        print(f"Description: {tournament.description}")
        print(f"Progress: Round {tournament.current_round_index} of {tournament.number_of_rounds}")

        print("\n--- STANDINGS (SORTED BY POINTS DESCENDING) ---")
        print(f"{'RANK':<5} | {'NAME':<25} | {'CHESS ID':<10} | {'POINTS'}")
        print("-" * 55)
        for rank, p in enumerate(sorted_players, 1):
            pts = scores.get(p.chess_id, 0.0)
            print(f"{rank:<5} | {p.full_name:<25} | {p.chess_id:<10} | {pts}")

        print("\n--- MATCH HISTORY BY ROUND ---")
        if not tournament.rounds:
            print("No rounds played yet.")
        else:
            for r in tournament.rounds:
                print(f"\n[{r.name}] Start: {r.start_time} | End: {r.end_time or 'In Progress'}")
                for m in r.matches:
                    print(f"  * {m}")
        print("=" * 50)
