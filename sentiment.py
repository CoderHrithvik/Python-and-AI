from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"

def mission_feedback(sentiment):
    if sentiment == "positive":
        return "Mission Success! Positive vibes detected, Agent."
    elif sentiment == "negative":
        return "Alert! Negative sentiment detected. Stay strong, Agent."
    else:
        return "Status: Neutral. Maintain communication. Monitoring..."

def start_chat():
    print("Welcome Agent! This is Sentiment Spy: AI Mission.")
    print("Type your message below. Type 'exit' to end the mission.\n")
    while True:
        user_input = input("Your message: ")
        if user_input.lower() == "exit":
            print("Mission terminated. Good work, Agent!")
            break

        sentiment = analyze_sentiment(user_input)
        feedback = mission_feedback(sentiment)

        print(f"Sentiment Detected: {sentiment.upper()}")
        print(f"{feedback}\n")

if __name__ == "__main__":
    start_chat()
