class LeaderboardSystem:
    def __init__(self):
        # Points tracked separately
        self.monthly_points = {}     # resets monthly
        self.all_time_points = {}    # never resets

    # -----------------------------
    # PLAYER REGISTRATION
    # -----------------------------
    def register_player(self, name: str):
        """Ensure player exists in both leaderboards."""
        if name not in self.monthly_points:
            self.monthly_points[name] = 0
        if name not in self.all_time_points:
            self.all_time_points[name] = 0

    # -----------------------------
    # RECORDING POINTS
    # -----------------------------
    def add_points(self, name: str, points: int):
        """Adds points to both monthly and all-time leaderboards."""
        self.register_player(name)
        self.monthly_points[name] += points
        self.all_time_points[name] += points

    # -----------------------------
    # LEADERBOARD OUTPUT
    # -----------------------------
    def get_monthly_leaderboard(self):
        """Returns monthly leaderboard sorted by points."""
        return dict(sorted(
            self.monthly_points.items(),
            key=lambda x: x[1],
            reverse=True
        ))

    def get_all_time_leaderboard(self):
        """Returns all-time leaderboard sorted by points."""
        return dict(sorted(
            self.all_time_points.items(),
            key=lambda x: x[1],
            reverse=True
        ))

    # -----------------------------
    # MONTHLY RESET
    # -----------------------------
    def reset_monthly(self):
        """Resets monthly leaderboard (called on 1st of each month)."""
        for p in self.monthly_points:
            self.monthly_points[p] = 0