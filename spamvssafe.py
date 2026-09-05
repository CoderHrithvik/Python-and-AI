# spam_classifier.py
from transformers import pipeline

def build_spam_classifier():
    # A small SMS spam model on HF
    model_name = "mrm8488/bert-tiny-finetuned-sms-spam-detection"
    return pipeline("text-classification", model=model_name)

def classify_message(text: str):
    classifier = build_spam_classifier()
    result = classifier(text)[0]
    label = result["label"].upper()
    score = result["score"]

    if "SPAM" in label:
        return "Spam", score
    else:
        return "Safe", score

def main():
    print("Spam vs Safe Message Classifier")
    print("Type 'quit' to exit.\n")

    while True:
        msg = input("Enter message: ")
        if msg.lower() == "quit":
            break

        label, score = classify_message(msg)
        print(f"Prediction: {label} (confidence: {score:.2f})\n")

if __name__ == "__main__":
    main()