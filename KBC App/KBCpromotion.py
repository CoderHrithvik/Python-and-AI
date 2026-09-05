class TeamSystem:
    def __init__(self):
        self.a_team = []   # list of player names
        self.b_team = []   # list of player names

    def set_initial_teams(self, a_players, b_players):
        """Set starting teams at the beginning of the season."""
        self.a_team = list(a_players)
        self.b_team = list(b_players)

    def promote_and_demote(self, monthly_leaderboard: dict):
        """
        monthly_leaderboard = {player: points}
        Promotes top 4 from B → A
        Demotes bottom 4 from A → B
        """

        # Filter leaderboard to only include players in each team
        a_scores = {p: monthly_leaderboard.get(p, 0) for p in self.a_team}
        b_scores = {p: monthly_leaderboard.get(p, 0) for p in self.b_team}

        # Sort A team (lowest first)
        a_sorted = sorted(a_scores.items(), key=lambda x: x[1])
        # Sort B team (highest first)
        b_sorted = sorted(b_scores.items(), key=lambda x: x[1], reverse=True)

        # Bottom 4 from A team
        demoted = [p[0] for p in a_sorted[:4]]

        # Top 4 from B team
        promoted = [p[0] for p in b_sorted[:4]]

        # Update teams
        for p in promoted:
            if p in self.b_team:
                self.b_team.remove(p)
                self.a_team.append(p)

        for p in demoted:
            if p in self.a_team:
                self.a_team.remove(p)
                self.b_team.append(p)

        return promoted, demoted

    def get_teams(self):
        return {
            "A Team": list(self.a_team),
            "B Team": list(self.b_team)
        }