from supabase_client import supabase

def add_player(name):
    response = supabase.table("players").insert({"name": name}).execute()
    return response

def get_players():
    response = supabase.table("players").select("*").execute()
    return response.data

# Test it
print("Adding player...")
print(add_player("Hrithvik"))

print("All players:")
print(get_players())