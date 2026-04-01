import random
from typing import List, Dict, Tuple


class BadmintonSystem:
    def __init__(self):
        # Stores players and how many matches they've played
        self.players: Dict[str, int] = {}

    # -----------------------------
    # PLAYER INPUT / REMOVAL
    # -----------------------------
    def add_player(self, name: str) -> bool:
        """Adds a player if valid. Returns True if added."""
        name = name.strip()

        if not name:
            return False  # empty name

        if name in self.players:
            return False  # already exists

        self.players[name] = 0
        return True

    def remove_player(self, name: str) -> bool:
        """Removes a player if they exist."""
        if name in self.players:
            del self.players[name]
            return True
        return False

    def get_players(self) -> Dict[str, int]:
        """Returns all players and their match counts."""
        return dict(self.players)

    # -----------------------------
    # FAIR RANDOMIZER
    # -----------------------------
    def generate_round(self, max_players: int = 8) -> List[Tuple[str, str, str, str]]:
        """
        Generates fair doubles matches.
        - Picks players with the fewest matches first
        - Randomizes within that group
        - Returns list of matches: (P1, P2, P3, P4)
        """

        if len(self.players) < 4:
            return []  # not enough players for even one match

        # Sort players by matches played (ascending)
        sorted_players = sorted(self.players.items(), key=lambda x: x[1])
        sorted_names = [p[0] for p in sorted_players]

        # Select up to max_players (8 for your club)
        selected = sorted_names[:max_players]

        # Shuffle for randomness
        random.shuffle(selected)

        matches = []
        for i in range(0, len(selected), 4):
            if i + 3 < len(selected):
                match = (selected[i], selected[i+1], selected[i+2], selected[i+3])
                matches.append(match)

        # Update match counts
        for p in selected:
            self.players[p] += 1

        return matches