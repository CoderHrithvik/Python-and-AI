print("Are you smart? Yes or No?")
answer = input().lower()
if answer == "yes":
    print("You are not vainav. You are officially smart. Good job!")
elif answer == "no":
    print("You are vainav. You are officially not smart. You are a gula. Better luck next time.")
else:
    print("You are a failure. You cannot even answer a simple question. Get lost.")

print("Do you want to be smart? Yes or No?")
answer2 = input().lower()
if answer2 == "yes":
    print("Do x² - 9x + 14 = 0, what is x? Add the two values of x together and write the answer.")
    x = input()
    if x == "2,7" or x == "7,2" or x == "2,7" or x == "7,2" or x == "7 2" or x == "2 7":
        print("Correct! You are smart.")
    else:
        print("Incorrect. You are not smart.")
elif answer2 == "no":
    print("Okay, you are definetly vainav. You are officially not smart. You are a gula. You are going to have a hard time. Bye Gul.")
else:
    print("You are a failure. You cannot even answer a simple question. Get lost.")
print("What are you good at? Type it in the box below.")
answer3 = input()
print("Wow, you are good at " + answer3 + "! You are smart! Good job!")
if answer3.lower() == "nothing":
    print("You are vainav. You are officially not smart. You are a gula. Better luck next time.")
print("Are you a gula? Yes or No? This is the ultimate question. If you say yes, you are the biggest gula ever. If you say no, you are not a gula. If you say anything else, you are a failure with no future.")
answer4 = input().lower()
if answer4 == "yes":
    print("You are the biggest gula ever. You are vainav. You are officially not smart. Better luck next time.")
elif answer4 == "no":
    print("You are not a gula. You are smart! Good job!")
else:
    print("You are a failure. You cannot even answer a simple question. Get lost.")
print("Congratulations! You have completed the test. You are smart! Good job!")
print("What do you rate this quiz out of 10? Type your answer in the box below.")
answer5 = input()
try:
    rating = int(answer5)
    if rating >= 8:
        print("Thank you for the high rating! You are smart! Good job!")
    elif rating >= 5:
        print("Thank you for the rating! You are smart! Good job!")
    else:
        print("Thank you for the low rating. You are vainav. You are officially not smart. Better luck next time.")
except ValueError:
    print("Please enter a valid number.")
print("Do you want to take the quiz again? Yes or No?")
answer6 = input().lower()
if answer6 == "yes":
    print("Restarting the quiz...")

elif answer6 == "no":
    end = "Thank you for taking the quiz! Goodbye!"
    print(end)