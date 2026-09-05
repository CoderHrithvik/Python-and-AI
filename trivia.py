import requests
import random
import html

EDUCATION_CATEGORY_ID = 9
API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def get_education_questions():
    responses = requests.get(API_URL)
    if responses.status_code == 200:
        data = responses.json()
        if data['response_code'] == 0 and data['results']:
            return data['results']
    return None

def run_quiz():
    questions = get_education_questions()
    if not questions:
        print("Failed to fetch educational questions.")
        return
    score = 0
    print("Welcome to the Educational Quiz!\n")

    for i, q in enumerate(questions, 1):
        question = html.unescape(q['question'])
        correct = html.unescape(q['correct_answer']) 
        incorrect = [html.unescape(a) for a in q['incorrect_answers']]

        options = incorrect + [correct]
        random.shuffle(options)

        print(f"Question {i}: {question}")
        for idx, option in enumerate(options, 1):
            print(f"  {idx}. {option}")

        while True:
            try:
                 choice = int(input("\nYour answer (1-4): "))
                 if 1 <= choice <= 4:
                     break
            except ValueError:
                 pass
            print("Invalid input. Please enter a number between 1 and 4.")

        if options[choice - 1] == correct:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {correct}\n")

    print(f"Final Score: {score}/{len(questions)}")
    print("Percentage: {score}/{len(questions)} * 100:.1f%")

if __name__ == "__main__":  
    run_quiz()