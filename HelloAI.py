

print(f"Hello! I am an AI Chat Bot. What is your name?")

name = input()

print(f" Nice to meet you,{name}.")

print(f"How are you feeling? Good or Bad?")
mood = input().lower()

if mood == "good":
    print(f"I am glad to hear that you are feeling fine.")
elif mood == "bad":
    print(f"I am terribly sorry to here that.")
else:
    print(f"I understand. Sometimes it is difficult to convey emotions.")

print("Do you want ideas on what to do if you are bored? Yes or No?")

feel = input().lower()

if feel == "yes":
    print(f" Yes! You could go to your local park, play football, hang out with your friends or even play video games.")
elif feel == "no":
    print(f"No? Okay.")

print(f"It was nice chatting with you,{name}. Bye!")

