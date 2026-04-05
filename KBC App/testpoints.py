from randomizer import BadmintonSystem

system = BadmintonSystem()

# Generate matches
courts = system.generate_round()
system.print_round(courts)
system.save_round(courts)

# Example: score match 1
match_id = "the-match-id-you-want-to-score"
system.score_match(match_id, 21, 17)

print("Match scored!")