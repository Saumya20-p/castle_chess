"""Swiss-system pairing algorithm for chess tournaments."""

# ==========================================
# IMPORTS & DEPENDENCIES
# ==========================================
import random
from typing import Dict, List, Set, Tuple
from models.match import Match
from models.tournament import Tournament


# ==========================================
# SECTION 1: SWISS PAIRING CLASS DEFINITION
# ==========================================
class SwissPairing:
    """Implements Swiss-system matchmaking logic for tournament rounds."""

    # ==========================================
    # SECTION 2: SCORE CALCULATION
    # ==========================================
    @staticmethod
    def calculate_scores(tournament: Tournament) -> Dict[str, float]:
        """Calculates total scores mapped by player chess_id."""
        scores: Dict[str, float] = {
            p.chess_id: 0.0 for p in tournament.players
        }

        for round_obj in tournament.rounds:
            for match in round_obj.matches:
                p1_id = match.player_1.chess_id
                p2_id = match.player_2.chess_id
                if p1_id in scores:
                    scores[p1_id] += match.score_1
                if p2_id in scores:
                    scores[p2_id] += match.score_2

        return scores

    # ==========================================
    # SECTION 3: PREVIOUS MATCHUP TRACKING
    # ==========================================
    @staticmethod
    def get_past_pairings(tournament: Tournament) -> Set[Tuple[str, str]]:
        """Returns a set of tuples containing chess_ids of previous opponents."""
        past_pairs: Set[Tuple[str, str]] = set()

        for round_obj in tournament.rounds:
            for match in round_obj.matches:
                p1_id = match.player_1.chess_id
                p2_id = match.player_2.chess_id
                past_pairs.add((p1_id, p2_id))
                past_pairs.add((p2_id, p1_id))

        return past_pairs

    # ==========================================
    # SECTION 4: ROUND PAIRING GENERATION
    # ==========================================
    @classmethod
    def generate_next_round_matches(
        cls,
        tournament: Tournament,
    ) -> List[Match]:
        """Generates list of Match objects for the next tournament round."""
        players = list(tournament.players)

        # Round 1: Random shuffle split top vs bottom half
        if not tournament.rounds:
            random.shuffle(players)
            half = len(players) // 2
            top_half = players[:half]
            bottom_half = players[half:]
            matches = []
            for p1, p2 in zip(top_half, bottom_half):
                matches.append(Match(player_1=p1, player_2=p2))
            return matches

        # Subsequent Rounds: Sort by score and avoid rematching
        scores = cls.calculate_scores(tournament)
        past_pairings = cls.get_past_pairings(tournament)

        # Sort players descending by score
        sorted_players = sorted(
            players, key=lambda p: scores.get(p.chess_id, 0.0), reverse=True
        )

        matches = []
        unpaired = list(sorted_players)

        while unpaired:
            p1 = unpaired.pop(0)
            paired = False
            for idx, p2 in enumerate(unpaired):
                # Pair with next available player not previously played against
                if (p1.chess_id, p2.chess_id) not in past_pairings:
                    matches.append(
                        Match(player_1=p1, player_2=unpaired.pop(idx))
                    )
                    paired = True
                    break

            # Fallback if remaining players have already played each other
            if not paired and unpaired:
                p2 = unpaired.pop(0)
                matches.append(Match(player_1=p1, player_2=p2))

        return matches
