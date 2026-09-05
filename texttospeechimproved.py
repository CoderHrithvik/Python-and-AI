import speech_recognition as sr
import pyttsx3
import random
import time

# -------------------------------------------------
# Text‑to‑Speech Engine (initialized ONCE)
# -------------------------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)

def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

# -------------------------------------------------
# Random fun responses
# -------------------------------------------------
def get_samples():
    return [
        "I'm here and ready to chat.",
        "How can I help you today.",
        "Your wish is my command.",
        "Listening carefully.",
        "I'm all ears.",
        "Ready when you are.",
        "Tell me something interesting.",
        "Let's make some magic happen.",
        "I'm awake and alert.",
        "What’s on your mind."
    ]

# -------------------------------------------------
# Jokes
# -------------------------------------------------
jokes = [
    "Why did the computer go to the doctor? It had a virus.",
    "Why don’t robots panic? They have nerves of steel.",
    "Why was the math book sad? It had too many problems.",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "What do you call fake spaghetti? An impasta."
]

# -------------------------------------------------
# Speech Recognition
# -------------------------------------------------
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("I didn’t quite catch that. Try again.")
        return None
    except sr.RequestError:
        speak("Speech service unavailable at the moment.")
        return None

# -------------------------------------------------
# Main Loop
# -------------------------------------------------
def main():
    speak("Voice Master Plus activated.")
    speak(random.choice(get_samples()))

    while True:
        command = listen()

        if command is None:
            time.sleep(0.5)
            continue

        # Exit command
        if "exit" in command or "quit" in command:
            speak("Goodbye.")
            break

        # Speed control
        elif "speed up" in command:
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate + 20)
            speak("Speed increased.")

        elif "slow down" in command:
            rate = engine.getProperty('rate')
            engine.setProperty('rate', max(80, rate - 20))
            speak("Speed decreased.")

        # Volume control
        elif "increase volume" in command:
            vol = engine.getProperty('volume')
            engine.setProperty('volume', min(1.0, vol + 0.1))
            speak("Volume increased.")

        elif "decrease volume" in command:
            vol = engine.getProperty('volume')
            engine.setProperty('volume', max(0.1, vol - 0.1))
            speak("Volume decreased.")

        # Tell a joke
        elif "joke" in command:
            speak(random.choice(jokes))

        # Greetings
        elif "hello" in command or "hi" in command:
            speak(random.choice(get_samples()))

        # Unknown command
        else:
            speak("I didn’t quite catch that. Try again.")

# -------------------------------------------------
if __name__ == "__main__":
    main()
