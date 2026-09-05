import requests

BASE_URL = "https://uselessfacts.jsph.pl/random.json"

def get_random_fact(language="en"):
    params = {"language": language}
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("text"), data.get("source")

def main():
    print("Random Useless Facts")
    print("Press Enter for a new fact, or type 'quit' to exit.\n")

    while True:
        cmd = input("Command: ")
        if cmd.lower() == "quit":
            break

        fact, source = get_random_fact()
        print(f"\nFact: {fact}")
        print(f"Source: {source}\n")

if __name__ == "__main__":
    main()