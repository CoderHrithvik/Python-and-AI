import random
from typing import List, Dict, Tuple
from supabase_client import supabase


class BadmintonSystem:
    def __init__(self):
        pass  # Supabase stores players now

    # ---------------------------------------------------
    # FETCH PLAYERS FROM SUPABASE BY TEAM (A or B)
    # ---------------------------------------------------
    def get_players_by_team(self, team_name: str) -> List[Dict]:
        response = supabase.rpc("get_players_by_team", {"team_name": team_name}).execute()
        return response.data

    # ---------------------------------------------------
    # GET MATCH COUNTS FOR FAIRNESS
    # ---------------------------------------------------
    def get_match_counts_for_team(self, player_ids: List[str]) -> Dict[str, int]:
        data = supabase.table("match_players").select("player_id").execute().data
        counts = {pid: 0 for pid in player_ids}

        for row in data:
            pid = row["player_id"]
            if pid in counts:
                counts[pid] += 1

        return counts

    # ---------------------------------------------------
    # PICK 8 PLAYERS FAIRLY FOR A TEAM (2 courts)
    # ---------------------------------------------------
    def pick_eight_players(self, team_name: str) -> List[Dict]:
        players = self.get_players_by_team(team_name)
        player_ids = [p["id"] for p in players]

        match_counts = self.get_match_counts_for_team(player_ids)

        # Sort by fewest matches played
        players_sorted = sorted(
            players,
            key=lambda p: match_counts.get(p["id"], 0)
        )

        # Take the 12 least-played players, then randomize
        candidate_pool = players_sorted[:12]
        random.shuffle(candidate_pool)

        # Pick 8 players
        return candidate_pool[:8]

    # ---------------------------------------------------
    # SPLIT 8 PLAYERS INTO 2 COURTS
    # ---------------------------------------------------
    def split_into_two_courts(self, players: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        random.shuffle(players)
        return players[:4], players[4:]

    # ---------------------------------------------------
    # FULL RANDOMIZER FOR A & B TEAMS (2 courts each)
    # ---------------------------------------------------
    def generate_round(self) -> Dict[str, List[Dict]]:
        # A-Team
        a_players = self.pick_eight_players("A")
        a_court1, a_court2 = self.split_into_two_courts(a_players)

        # B-Team
        b_players = self.pick_eight_players("B")
        b_court1, b_court2 = self.split_into_two_courts(b_players)

        return {
            "A Court 1": a_court1,
            "A Court 2": a_court2,
            "B Court 1": b_court1,
            "B Court 2": b_court2
        }

    # ---------------------------------------------------
    # PRETTY PRINT (OPTIONAL)
    # ---------------------------------------------------
    def print_round(self, courts):
        for court, players in courts.items():
            print(f"\n{court}:")
            for p in players:
                print(" -", p["name"])

    # ---------------------------------------------------
    # SAVE ALL 4 COURTS AS MATCHES IN SUPABASE
    # ---------------------------------------------------
    def save_round(self, courts: dict):
        court_number = 1

        for court_name, players in courts.items():
            match_id = self.create_match(court_number)
            self.add_players_to_match(match_id, players)
            court_number += 1

    def create_match(self, court_number: int) -> str:
        response = supabase.table("matches").insert({
            "court_number": court_number,
            "team1_score": 0,
            "team2_score": 0
        }).execute()

        return response.data[0]["id"]
    
    def add_players_to_match(self, match_id: str, players: list):
        # players is a list of 4 dicts
        # First 2 players → team_side = 1
        # Next 2 players → team_side = 2

        rows = []

        for i, p in enumerate(players):
            rows.append({
                "match_id": match_id,
                "player_id": p["id"],
                "team_side": 1 if i < 2 else 2
            })

        supabase.table("match_players").insert(rows).execute()
    
    def update_match_score(self, match_id: str, team1_score: int, team2_score: int):
        # Determine winner
        if team1_score > team2_score:
            winner = 1
        elif team2_score > team1_score:
            winner = 2
        else:
            winner = 0  # draw (optional)

        # Update match in Supabase
        supabase.table("matches").update({
            "team1_score": team1_score,
            "team2_score": team2_score,
            "winner": winner
        }).eq("id", match_id).execute()

        return winner
    
    def award_points(self, match_id: str, winner: int):
        # Get players in the match
        players = supabase.table("match_players").select("*").eq("match_id", match_id).execute().data

        for p in players:
            player_id = p["player_id"]
            team_side = p["team_side"]

            # Winner gets +3, loser gets +1
            points = 3 if team_side == winner else 1

            # Update player points
            supabase.table("players").update({
                "points": supabase.rpc("increment_points", {
                    "player_id": player_id,
                    "points_to_add": points
                })
            })

        def score_match(self, match_id: str, team1_score: int, team2_score: int):
            winner = self.update_match_score(match_id, team1_score, team2_score)
        if winner != 0:
            self.award_points(match_id, winner)