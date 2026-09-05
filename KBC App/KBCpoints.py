class ScoreSystem:
    def __init__(self):
        # Track points separately
        self.monthly_points = {}     # resets monthly
        self.all_time_points = {}    # never resets

    def register_player(self, name: str):
        """Ensure player exists in both leaderboards."""
        if name not in self.monthly_points:
            self.monthly_points[name] = 0
        if name not in self.all_time_points:
            self.all_time_points[name] = 0

    def record_match(self, team1: tuple, team2: tuple, score1: int, score2: int):
        """
        team1 = (P1, P2)
        team2 = (P3, P4)
        score1 = team1 score
        score2 = team2 score
        """

        # Register players if new
        for p in team1 + team2:
            self.register_player(p)

        # Award points based on score
        for p in team1:
            self.monthly_points[p] += score1
            self.all_time_points[p] += score1

        for p in team2:
            self.monthly_points[p] += score2
            self.all_time_points[p] += score2

    def get_monthly_leaderboard(self):
        return dict(sorted(self.monthly_points.items(), key=lambda x: x[1], reverse=True))

    def get_all_time_leaderboard(self):
        return dict(sorted(self.all_time_points.items(), key=lambda x: x[1], reverse=True))

    def reset_monthly(self):
        """Call this on the 1st of every month."""
        for p in self.monthly_points:
            self.monthly_points[p] = 0