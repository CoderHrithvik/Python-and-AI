
from transformers import pipeline

def build_sentiment_analyzer():
    return pipeline("sentiment-analysis")

def classify_sentiment(text: str):
    analyzer = build_sentiment_analyzer()
    result = analyzer(text)[0]
    label = result["label"]
    score = result["score"]
    return label, score

def main():
    print("Simple Sentiment Analysis Tool")
    print("Type 'quit' to exit.\n")

    while True:
        text = input("Enter text: ")
        if text.lower() == "quit":
            break

        label, score = classify_sentiment(text)
        if label.upper() in ["POSITIVE", "5 stars"]:
            sentiment = "Positive"
        elif label.upper() in ["NEGATIVE", "1 star"]:
            sentiment = "Negative"
        else:
            sentiment = label

        print(f"Sentiment: {sentiment} (confidence: {score:.2f})\n")

if __name__ == "__main__":
    main()