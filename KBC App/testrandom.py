from KBCrandomizer import BadmintonSystem
import inspect

system = BadmintonSystem()

print(">>> Methods found in BadmintonSystem:")
print([name for name, _ in inspect.getmembers(system, inspect.ismethod)])

system = BadmintonSystem()

courts = system.generate_round()
system.print_round(courts)

system.save_round(courts)

print("\nMatches saved to Supabase!")